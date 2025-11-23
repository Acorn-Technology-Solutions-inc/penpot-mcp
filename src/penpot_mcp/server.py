"""
Main MCP server for Penpot integration.
"""

import asyncio
import logging
import os
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from penpot_mcp.penpot_client import PenpotClient
from penpot_mcp.tools.advanced import (
    compare_designs_tool,
    generate_design_from_prompt_tool,
    validate_accessibility_tool,
)
from penpot_mcp.tools.analysis import (
    analyze_design_tool,
    extract_colors_tool,
    extract_typography_tool,
    get_components_tool,
)
from penpot_mcp.tools.export import (
    export_design_tokens_tool,
    export_to_png_tool,
    export_to_svg_tool,
)
from penpot_mcp.tools.file_ops import (
    create_file_tool,
    delete_file_tool,
    get_file_tool,
    list_files_tool,
)
from penpot_mcp.tools.shapes import (
    create_circle_tool,
    create_frame_tool,
    create_rectangle_tool,
    create_text_tool,
    delete_shape_tool,
    update_shape_tool,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG", "false").lower() == "true" else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_server() -> Server:
    """
    Create and configure the MCP server.

    Returns:
        Configured MCP server instance.
    """
    server = Server("penpot-mcp")
    client: PenpotClient | None = None

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available MCP tools."""
        return [
            # File Operations
            Tool(
                name="list_files",
                description="List all design files in a team or project. Returns file metadata including IDs, names, and modification dates.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "team_id": {"type": "string", "description": "Team UUID (optional)"},
                        "project_id": {"type": "string", "description": "Project UUID (optional)"},
                    },
                },
            ),
            Tool(
                name="get_file",
                description="Get complete file data including all pages, shapes, colors, and typography. Use this to inspect a design file's contents.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "Penpot file UUID"},
                    },
                    "required": ["file_id"],
                },
            ),
            Tool(
                name="create_file",
                description="Create a new Penpot design file in a project.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project UUID where file will be created",
                        },
                        "name": {"type": "string", "description": "File name"},
                    },
                    "required": ["project_id", "name"],
                },
            ),
            Tool(
                name="delete_file",
                description="Delete a Penpot file permanently.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID to delete"},
                    },
                    "required": ["file_id"],
                },
            ),
            # Design Analysis
            Tool(
                name="analyze_design",
                description="Perform comprehensive AI-powered analysis of a design file. Returns color palette, typography styles, component count, and layout structure.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID to analyze"},
                    },
                    "required": ["file_id"],
                },
            ),
            Tool(
                name="extract_colors",
                description="Extract all colors used in a file with usage statistics. Useful for design system audits.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                    },
                    "required": ["file_id"],
                },
            ),
            Tool(
                name="extract_typography",
                description="Extract all text styles and fonts used in a file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                    },
                    "required": ["file_id"],
                },
            ),
            Tool(
                name="get_components",
                description="List all components and their instances in a file.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                    },
                    "required": ["file_id"],
                },
            ),
            # Shape Operations
            Tool(
                name="create_rectangle",
                description="Create a rectangle shape on a page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "x": {"type": "number", "description": "X position"},
                        "y": {"type": "number", "description": "Y position"},
                        "width": {"type": "number", "description": "Width"},
                        "height": {"type": "number", "description": "Height"},
                        "fill_color": {
                            "type": "string",
                            "description": "Fill color in hex format (e.g., #FF0000)",
                            "default": "#000000",
                        },
                        "name": {"type": "string", "description": "Shape name", "default": "Rectangle"},
                    },
                    "required": ["file_id", "page_id", "x", "y", "width", "height"],
                },
            ),
            Tool(
                name="create_text",
                description="Create a text element on a page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "x": {"type": "number", "description": "X position"},
                        "y": {"type": "number", "description": "Y position"},
                        "text": {"type": "string", "description": "Text content"},
                        "font_size": {
                            "type": "integer",
                            "description": "Font size in pixels",
                            "default": 16,
                        },
                        "font_family": {
                            "type": "string",
                            "description": "Font family name",
                            "default": "Arial",
                        },
                        "fill_color": {
                            "type": "string",
                            "description": "Text color in hex format",
                            "default": "#000000",
                        },
                        "name": {"type": "string", "description": "Element name", "default": "Text"},
                    },
                    "required": ["file_id", "page_id", "x", "y", "text"],
                },
            ),
            Tool(
                name="create_frame",
                description="Create a frame (container) on a page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "x": {"type": "number", "description": "X position"},
                        "y": {"type": "number", "description": "Y position"},
                        "width": {"type": "number", "description": "Width"},
                        "height": {"type": "number", "description": "Height"},
                        "name": {"type": "string", "description": "Frame name", "default": "Frame"},
                        "fill_color": {
                            "type": "string",
                            "description": "Fill color in hex format (optional)",
                        },
                    },
                    "required": ["file_id", "page_id", "x", "y", "width", "height"],
                },
            ),
            Tool(
                name="create_circle",
                description="Create a circle shape on a page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "x": {"type": "number", "description": "Center X position"},
                        "y": {"type": "number", "description": "Center Y position"},
                        "radius": {"type": "number", "description": "Circle radius"},
                        "fill_color": {
                            "type": "string",
                            "description": "Fill color in hex format",
                            "default": "#000000",
                        },
                        "name": {"type": "string", "description": "Shape name", "default": "Circle"},
                    },
                    "required": ["file_id", "page_id", "x", "y", "radius"],
                },
            ),
            Tool(
                name="update_shape",
                description="Update properties of an existing shape (position, size, color, etc.).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "shape_id": {"type": "string", "description": "Shape UUID"},
                        "properties": {
                            "type": "object",
                            "description": "Properties to update (e.g., {x: 100, y: 200, fill_color: '#FF0000'})",
                        },
                    },
                    "required": ["file_id", "shape_id", "properties"],
                },
            ),
            Tool(
                name="delete_shape",
                description="Delete a shape from a page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "shape_id": {"type": "string", "description": "Shape UUID"},
                    },
                    "required": ["file_id", "page_id", "shape_id"],
                },
            ),
            # Export Operations
            Tool(
                name="export_to_svg",
                description="Export a page or specific shapes to SVG format.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "shape_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional array of shape IDs to export",
                        },
                    },
                    "required": ["file_id", "page_id"],
                },
            ),
            Tool(
                name="export_to_png",
                description="Export a page or specific shapes to PNG format.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                        "page_id": {"type": "string", "description": "Page UUID"},
                        "scale": {
                            "type": "number",
                            "description": "Export scale factor (1.0 = 100%, 2.0 = 200%)",
                            "default": 1.0,
                        },
                        "shape_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional array of shape IDs to export",
                        },
                    },
                    "required": ["file_id", "page_id"],
                },
            ),
            Tool(
                name="export_design_tokens",
                description="Export design tokens (colors, spacing, typography) as structured JSON.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                    },
                    "required": ["file_id"],
                },
            ),
            # Advanced Features
            Tool(
                name="generate_design_from_prompt",
                description="Generate a design from a natural language prompt. Example: 'Create a login page with email, password, and submit button'.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string", "description": "Project UUID"},
                        "prompt": {
                            "type": "string",
                            "description": "Natural language design description",
                        },
                        "file_name": {
                            "type": "string",
                            "description": "Optional file name (defaults to AI-generated name)",
                        },
                    },
                    "required": ["project_id", "prompt"],
                },
            ),
            Tool(
                name="validate_accessibility",
                description="Check design for accessibility issues: color contrast, text readability, touch target sizes.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string", "description": "File UUID"},
                    },
                    "required": ["file_id"],
                },
            ),
            Tool(
                name="compare_designs",
                description="Compare two design files and highlight differences in structure, colors, and elements.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_id_1": {"type": "string", "description": "First file UUID"},
                        "file_id_2": {"type": "string", "description": "Second file UUID"},
                    },
                    "required": ["file_id_1", "file_id_2"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
        """Handle tool calls."""
        nonlocal client

        # Initialize client if needed
        if client is None:
            client = PenpotClient()
            await client.connect()

        try:
            # Route to appropriate tool function
            result = None

            if name == "list_files":
                result = await list_files_tool(
                    client, arguments.get("team_id"), arguments.get("project_id")
                )
            elif name == "get_file":
                result = await get_file_tool(client, arguments["file_id"])
            elif name == "create_file":
                result = await create_file_tool(client, arguments["project_id"], arguments["name"])
            elif name == "delete_file":
                result = await delete_file_tool(client, arguments["file_id"])
            elif name == "analyze_design":
                result = await analyze_design_tool(client, arguments["file_id"])
            elif name == "extract_colors":
                result = await extract_colors_tool(client, arguments["file_id"])
            elif name == "extract_typography":
                result = await extract_typography_tool(client, arguments["file_id"])
            elif name == "get_components":
                result = await get_components_tool(client, arguments["file_id"])
            elif name == "create_rectangle":
                result = await create_rectangle_tool(
                    client,
                    arguments["file_id"],
                    arguments["page_id"],
                    arguments["x"],
                    arguments["y"],
                    arguments["width"],
                    arguments["height"],
                    arguments.get("fill_color", "#000000"),
                    arguments.get("name", "Rectangle"),
                )
            elif name == "create_text":
                result = await create_text_tool(
                    client,
                    arguments["file_id"],
                    arguments["page_id"],
                    arguments["x"],
                    arguments["y"],
                    arguments["text"],
                    arguments.get("font_size", 16),
                    arguments.get("font_family", "Arial"),
                    arguments.get("fill_color", "#000000"),
                    arguments.get("name", "Text"),
                )
            elif name == "create_frame":
                result = await create_frame_tool(
                    client,
                    arguments["file_id"],
                    arguments["page_id"],
                    arguments["x"],
                    arguments["y"],
                    arguments["width"],
                    arguments["height"],
                    arguments.get("name", "Frame"),
                    arguments.get("fill_color"),
                )
            elif name == "create_circle":
                result = await create_circle_tool(
                    client,
                    arguments["file_id"],
                    arguments["page_id"],
                    arguments["x"],
                    arguments["y"],
                    arguments["radius"],
                    arguments.get("fill_color", "#000000"),
                    arguments.get("name", "Circle"),
                )
            elif name == "update_shape":
                result = await update_shape_tool(
                    client, arguments["file_id"], arguments["shape_id"], arguments["properties"]
                )
            elif name == "delete_shape":
                result = await delete_shape_tool(
                    client, arguments["file_id"], arguments["page_id"], arguments["shape_id"]
                )
            elif name == "export_to_svg":
                result = await export_to_svg_tool(
                    client, arguments["file_id"], arguments["page_id"], arguments.get("shape_ids")
                )
            elif name == "export_to_png":
                result = await export_to_png_tool(
                    client,
                    arguments["file_id"],
                    arguments["page_id"],
                    arguments.get("scale", 1.0),
                    arguments.get("shape_ids"),
                )
            elif name == "export_design_tokens":
                result = await export_design_tokens_tool(client, arguments["file_id"])
            elif name == "generate_design_from_prompt":
                result = await generate_design_from_prompt_tool(
                    client,
                    arguments["project_id"],
                    arguments["prompt"],
                    arguments.get("file_name"),
                )
            elif name == "validate_accessibility":
                result = await validate_accessibility_tool(client, arguments["file_id"])
            elif name == "compare_designs":
                result = await compare_designs_tool(
                    client, arguments["file_id_1"], arguments["file_id_2"]
                )
            else:
                result = {"success": False, "error": f"Unknown tool: {name}"}

            # Format result as JSON string
            import json

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logger.error(f"Tool {name} failed: {e}", exc_info=True)
            import json

            error_result = {"success": False, "error": str(e), "tool": name}
            return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    return server


async def main() -> None:
    """Main entry point for the server."""
    logger.info("Starting Penpot MCP Server")

    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run() -> None:
    """Synchronous entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
