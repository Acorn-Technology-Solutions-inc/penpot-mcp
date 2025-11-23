"""
Async HTTP client for Penpot RPC API.
"""

import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp

from penpot_mcp.exceptions import (
    AuthenticationError,
    PenpotAPIError,
    PermissionDeniedError,
    ResourceNotFoundError,
)
from penpot_mcp.utils.auth import get_auth_headers
from penpot_mcp.utils.cache import Cache
from penpot_mcp.utils.rate_limit import RateLimiter

logger = logging.getLogger(__name__)


class PenpotClient:
    """
    Async HTTP client for Penpot RPC API.

    Provides methods for interacting with Penpot files, pages, shapes, and other resources.
    Includes built-in rate limiting, caching, and error handling.
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        access_token: Optional[str] = None,
        rate_limiter: Optional[RateLimiter] = None,
        cache: Optional[Cache] = None,
    ):
        """
        Initialize Penpot client.

        Args:
            api_url: Penpot API base URL. Defaults to PENPOT_API_URL env var.
            access_token: Penpot access token. Defaults to PENPOT_ACCESS_TOKEN env var.
            rate_limiter: Optional rate limiter. Creates default if not provided.
            cache: Optional cache. Creates default if not provided.
        """
        self.api_url = api_url or os.getenv("PENPOT_API_URL", "https://design.penpot.app/api")
        self.access_token = access_token or os.getenv("PENPOT_ACCESS_TOKEN")

        if not self.access_token:
            raise AuthenticationError(
                "No access token provided. Set PENPOT_ACCESS_TOKEN environment variable."
            )

        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = rate_limiter or RateLimiter(
            max_requests=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
            window_seconds=int(os.getenv("RATE_LIMIT_WINDOW", "60")),
        )
        self.cache = cache or Cache(
            default_ttl=int(os.getenv("CACHE_TTL_SECONDS", "300")),
            enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true",
        )

    async def __aenter__(self) -> "PenpotClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Create HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=get_auth_headers(self.access_token))
            logger.info("Penpot client connected")

    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("Penpot client closed")

    async def _call(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, use_cache: bool = True
    ) -> Any:
        """
        Make RPC call to Penpot API.

        Args:
            endpoint: RPC endpoint name (e.g., 'get-file').
            data: Request payload.
            use_cache: Whether to use cache for this request.

        Returns:
            Response data from API.

        Raises:
            PenpotAPIError: If API call fails.
            RateLimitError: If rate limit is exceeded.
        """
        if self.session is None:
            await self.connect()

        # Check rate limit
        await self.rate_limiter.acquire()

        # Check cache for GET operations
        cache_key = f"{endpoint}:{str(data)}" if data else endpoint
        if use_cache and endpoint.startswith("get-"):
            cached = self.cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit for {endpoint}")
                return cached

        url = f"{self.api_url}/rpc/command/{endpoint}"
        logger.debug(f"Calling {endpoint} with data: {data}")

        try:
            assert self.session is not None
            async with self.session.post(url, json=data or {}) as response:
                response_text = await response.text()

                if response.status == 401:
                    raise AuthenticationError("Invalid or expired access token")
                elif response.status == 403:
                    raise PermissionDeniedError(f"Permission denied for {endpoint}")
                elif response.status == 404:
                    raise ResourceNotFoundError(f"Resource not found: {endpoint}")
                elif response.status != 200:
                    raise PenpotAPIError(
                        f"API call failed: {response.status} - {response_text}", response.status
                    )

                # Parse JSON response
                result = await response.json()

                # Cache successful GET responses
                if use_cache and endpoint.startswith("get-"):
                    self.cache.set(cache_key, result)

                return result

        except aiohttp.ClientError as e:
            raise PenpotAPIError(f"HTTP request failed: {str(e)}")

    # ============================================================================
    # Profile & Team Operations
    # ============================================================================

    async def get_profile(self) -> Dict[str, Any]:
        """
        Get current user profile.

        Returns:
            User profile data including teams.
        """
        return await self._call("get-profile")

    async def get_teams(self) -> List[Dict[str, Any]]:
        """
        Get list of teams user belongs to.

        Returns:
            List of team objects.
        """
        profile = await self.get_profile()
        return profile.get("teams", [])

    # ============================================================================
    # Project Operations
    # ============================================================================

    async def list_projects(self, team_id: str) -> List[Dict[str, Any]]:
        """
        List all projects in a team.

        Args:
            team_id: Team UUID.

        Returns:
            List of project objects.
        """
        return await self._call("get-projects", {"team-id": team_id})

    async def create_project(self, team_id: str, name: str) -> Dict[str, Any]:
        """
        Create a new project.

        Args:
            team_id: Team UUID.
            name: Project name.

        Returns:
            Created project object.
        """
        result = await self._call("create-project", {"team-id": team_id, "name": name})
        self.cache.invalidate_pattern(f"get-projects:{team_id}")
        return result

    # ============================================================================
    # File Operations
    # ============================================================================

    async def list_files(
        self, project_id: Optional[str] = None, team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List files in a project or team.

        Args:
            project_id: Optional project UUID.
            team_id: Optional team UUID.

        Returns:
            List of file objects.
        """
        if project_id:
            return await self._call("get-project-files", {"project-id": project_id})
        elif team_id:
            return await self._call("get-team-files", {"team-id": team_id})
        else:
            raise ValueError("Either project_id or team_id must be provided")

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        Get complete file data including all pages and shapes.

        Args:
            file_id: File UUID.

        Returns:
            Complete file object with pages, shapes, colors, typography.
        """
        return await self._call("get-file", {"id": file_id})

    async def create_file(self, project_id: str, name: str) -> Dict[str, Any]:
        """
        Create a new Penpot file.

        Args:
            project_id: Project UUID where file will be created.
            name: File name.

        Returns:
            Created file object with id.
        """
        result = await self._call("create-file", {"project-id": project_id, "name": name})
        self.cache.invalidate_pattern(f"get-project-files:{project_id}")
        return result

    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            file_id: File UUID to delete.

        Returns:
            Deletion confirmation.
        """
        result = await self._call("delete-file", {"id": file_id})
        self.cache.delete(f"get-file:{{'id': '{file_id}'}}")
        return result

    async def update_file(
        self, file_id: str, changes: List[Dict[str, Any]], revn: int = 0
    ) -> Dict[str, Any]:
        """
        Update a file with a list of changes.

        Args:
            file_id: File UUID.
            changes: List of change operations.
            revn: Revision number (use 0 for latest).

        Returns:
            Update result.
        """
        result = await self._call(
            "update-file",
            {"id": file_id, "session-id": file_id, "revn": revn, "changes": changes},
        )
        self.cache.delete(f"get-file:{{'id': '{file_id}'}}")
        return result

    # ============================================================================
    # Page Operations
    # ============================================================================

    async def create_page(self, file_id: str, name: str) -> Dict[str, Any]:
        """
        Create a new page in a file.

        Args:
            file_id: File UUID.
            name: Page name.

        Returns:
            Created page object.
        """
        changes = [{"type": "add-page", "id": None, "name": name}]
        return await self.update_file(file_id, changes)

    async def delete_page(self, file_id: str, page_id: str) -> Dict[str, Any]:
        """
        Delete a page from a file.

        Args:
            file_id: File UUID.
            page_id: Page UUID to delete.

        Returns:
            Deletion result.
        """
        changes = [{"type": "del-page", "id": page_id}]
        return await self.update_file(file_id, changes)

    # ============================================================================
    # Shape Operations
    # ============================================================================

    async def add_shape(
        self, file_id: str, page_id: str, shape_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a shape to a page.

        Args:
            file_id: File UUID.
            page_id: Page UUID.
            shape_data: Shape properties.

        Returns:
            Add shape result.
        """
        changes = [{"type": "add-obj", "page-id": page_id, "obj": shape_data}]
        return await self.update_file(file_id, changes)

    async def update_shape(
        self, file_id: str, shape_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update shape properties.

        Args:
            file_id: File UUID.
            shape_id: Shape UUID.
            properties: Properties to update.

        Returns:
            Update result.
        """
        changes = [{"type": "mod-obj", "id": shape_id, "operations": properties}]
        return await self.update_file(file_id, changes)

    async def delete_shape(self, file_id: str, page_id: str, shape_id: str) -> Dict[str, Any]:
        """
        Delete a shape from a page.

        Args:
            file_id: File UUID.
            page_id: Page UUID.
            shape_id: Shape UUID to delete.

        Returns:
            Deletion result.
        """
        changes = [{"type": "del-obj", "page-id": page_id, "id": shape_id}]
        return await self.update_file(file_id, changes)

    # ============================================================================
    # Export Operations
    # ============================================================================

    async def export_shapes(
        self, file_id: str, shape_ids: List[str], export_type: str = "svg", scale: float = 1.0
    ) -> bytes:
        """
        Export shapes to a specific format.

        Args:
            file_id: File UUID.
            shape_ids: List of shape UUIDs to export.
            export_type: Export format ('svg', 'png', 'jpeg').
            scale: Export scale factor (for bitmap formats).

        Returns:
            Exported file content as bytes.
        """
        url = f"{self.api_url}/export/{export_type}/{file_id}"
        params = {"shapes": ",".join(shape_ids), "scale": scale}

        if self.session is None:
            await self.connect()

        await self.rate_limiter.acquire()

        assert self.session is not None
        async with self.session.get(url, params=params) as response:
            if response.status != 200:
                raise PenpotAPIError(f"Export failed: {response.status}", response.status)

            return await response.read()
