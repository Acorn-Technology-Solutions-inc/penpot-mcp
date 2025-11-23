"""
File operation tools for MCP server.
"""

import logging
from typing import Any, Dict, List, Optional

from penpot_mcp.penpot_client import PenpotClient

logger = logging.getLogger(__name__)


async def list_files_tool(
    client: PenpotClient, team_id: Optional[str] = None, project_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all design files in a team or project.

    Args:
        client: Penpot API client.
        team_id: Penpot team UUID (optional).
        project_id: Optional project UUID to filter.

    Returns:
        Dictionary with list of files and metadata.
    """
    try:
        if project_id:
            files = await client.list_files(project_id=project_id)
        elif team_id:
            files = await client.list_files(team_id=team_id)
        else:
            # Get all teams and list files from each
            profile = await client.get_profile()
            teams = profile.get("teams", [])
            all_files: List[Dict[str, Any]] = []
            for team in teams:
                team_files = await client.list_files(team_id=team["id"])
                all_files.extend(team_files)
            files = all_files

        return {
            "success": True,
            "count": len(files),
            "files": [
                {
                    "id": f.get("id"),
                    "name": f.get("name"),
                    "project_id": f.get("project-id"),
                    "created_at": f.get("created-at"),
                    "modified_at": f.get("modified-at"),
                }
                for f in files
            ],
        }
    except Exception as e:
        logger.error(f"Failed to list files: {e}")
        return {"success": False, "error": str(e)}


async def get_file_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    Get complete file data including all pages and shapes.

    Args:
        client: Penpot API client.
        file_id: Penpot file UUID.

    Returns:
        Complete file object with pages, shapes, colors, typography.
    """
    try:
        file_data = await client.get_file(file_id)

        # Extract summary information
        pages = file_data.get("data", {}).get("pages-index", {}).values()
        page_count = len(list(pages))

        return {
            "success": True,
            "file": {
                "id": file_data.get("id"),
                "name": file_data.get("name"),
                "project_id": file_data.get("project-id"),
                "created_at": file_data.get("created-at"),
                "modified_at": file_data.get("modified-at"),
                "page_count": page_count,
            },
            "data": file_data.get("data", {}),
        }
    except Exception as e:
        logger.error(f"Failed to get file: {e}")
        return {"success": False, "error": str(e)}


async def create_file_tool(
    client: PenpotClient, project_id: str, name: str
) -> Dict[str, Any]:
    """
    Create a new Penpot file.

    Args:
        client: Penpot API client.
        project_id: Project UUID where file will be created.
        name: File name.

    Returns:
        Created file object with id.
    """
    try:
        file_data = await client.create_file(project_id, name)

        return {
            "success": True,
            "file": {
                "id": file_data.get("id"),
                "name": file_data.get("name"),
                "project_id": file_data.get("project-id"),
                "created_at": file_data.get("created-at"),
            },
        }
    except Exception as e:
        logger.error(f"Failed to create file: {e}")
        return {"success": False, "error": str(e)}


async def delete_file_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    Delete a Penpot file.

    Args:
        client: Penpot API client.
        file_id: File UUID to delete.

    Returns:
        Deletion confirmation.
    """
    try:
        await client.delete_file(file_id)

        return {"success": True, "message": f"File {file_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete file: {e}")
        return {"success": False, "error": str(e)}
