"""
Authentication utilities for Penpot API.
"""

import os
from typing import Dict


def get_auth_headers(access_token: str | None = None) -> Dict[str, str]:
    """
    Get authentication headers for Penpot API requests.

    Args:
        access_token: Optional access token. If not provided, will try to get from environment.

    Returns:
        Dictionary of headers including authorization.

    Raises:
        ValueError: If no access token is available.
    """
    token = access_token or os.getenv("PENPOT_ACCESS_TOKEN")

    if not token:
        raise ValueError(
            "No access token provided. Set PENPOT_ACCESS_TOKEN environment variable "
            "or pass access_token parameter."
        )

    return {
        "Authorization": f"Token {token}",
        "Content-Type": "application/transit+json",
        "Accept": "application/transit+json",
    }
