"""
Custom exceptions for Penpot MCP server.
"""


class PenpotMCPError(Exception):
    """Base exception for all Penpot MCP errors."""

    pass


class PenpotAPIError(PenpotMCPError):
    """Raised when a Penpot API call fails."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(PenpotMCPError):
    """Raised when authentication fails."""

    pass


class ValidationError(PenpotMCPError):
    """Raised when input validation fails."""

    pass


class RateLimitError(PenpotMCPError):
    """Raised when rate limit is exceeded."""

    pass


class ResourceNotFoundError(PenpotMCPError):
    """Raised when a requested resource is not found."""

    pass


class PermissionDeniedError(PenpotMCPError):
    """Raised when user doesn't have permission for an operation."""

    pass
