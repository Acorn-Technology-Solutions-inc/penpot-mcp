"""
Penpot MCP Server

A Model Context Protocol server for interacting with Penpot design files.
"""

__version__ = "1.0.0"

from penpot_mcp.penpot_client import PenpotClient
from penpot_mcp.server import create_server

__all__ = ["PenpotClient", "create_server", "__version__"]
