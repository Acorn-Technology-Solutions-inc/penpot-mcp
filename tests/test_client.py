"""
Tests for Penpot client.
"""

import pytest

from penpot_mcp.exceptions import AuthenticationError
from penpot_mcp.penpot_client import PenpotClient


class TestPenpotClient:
    """Test Penpot client functionality."""

    def test_client_init_no_token(self):
        """Test client initialization without token raises error."""
        with pytest.raises(AuthenticationError):
            PenpotClient(access_token=None)

    def test_client_init_with_token(self):
        """Test client initialization with token."""
        client = PenpotClient(access_token="test_token")
        assert client.access_token == "test_token"
        assert client.api_url == "https://design.penpot.app/api"

    def test_client_custom_url(self):
        """Test client with custom API URL."""
        client = PenpotClient(
            api_url="https://custom.penpot.app/api", access_token="test_token"
        )
        assert client.api_url == "https://custom.penpot.app/api"

    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """Test client can be used as async context manager."""
        async with PenpotClient(access_token="test_token") as client:
            assert client.session is not None

        assert client.session is None  # Should be closed
