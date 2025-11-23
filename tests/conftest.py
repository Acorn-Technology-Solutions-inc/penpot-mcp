"""
Pytest configuration and fixtures.
"""

import os

import pytest


@pytest.fixture
def mock_api_token():
    """Provide a mock API token for testing."""
    return "test_token_12345"


@pytest.fixture
def mock_file_id():
    """Provide a mock file ID for testing."""
    return "file-uuid-1234"


@pytest.fixture
def mock_page_id():
    """Provide a mock page ID for testing."""
    return "page-uuid-5678"


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("PENPOT_ACCESS_TOKEN", "test_token")
    monkeypatch.setenv("CACHE_ENABLED", "false")
    monkeypatch.setenv("DEBUG", "false")
