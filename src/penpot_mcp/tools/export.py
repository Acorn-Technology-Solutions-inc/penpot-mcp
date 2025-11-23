"""
Export operation tools for MCP server.
"""

import base64
import logging
from typing import Any, Dict, List

from penpot_mcp.penpot_client import PenpotClient
from penpot_mcp.tools.analysis import extract_colors_from_objects, extract_typography_from_objects

logger = logging.getLogger(__name__)


async def export_to_svg_tool(
    client: PenpotClient, file_id: str, page_id: str, shape_ids: List[str] | None = None
) -> Dict[str, Any]:
    """
    Export page or shapes to SVG format.

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        shape_ids: Optional list of specific shape IDs to export.

    Returns:
        SVG content as string.
    """
    try:
        # If no shape_ids provided, export the entire page
        if not shape_ids:
            file_data = await client.get_file(file_id)
            data = file_data.get("data", {})
            objects = data.get("objects", {}).get(page_id, {})
            # Get all shape IDs from the page
            shape_ids = [str(obj_id) for obj_id in objects.keys()]

        if not shape_ids:
            return {"success": False, "error": "No shapes found to export"}

        svg_bytes = await client.export_shapes(file_id, shape_ids, "svg")
        svg_content = svg_bytes.decode("utf-8")

        return {
            "success": True,
            "format": "svg",
            "page_id": page_id,
            "shape_count": len(shape_ids),
            "svg": svg_content,
            "size_bytes": len(svg_bytes),
        }
    except Exception as e:
        logger.error(f"Failed to export to SVG: {e}")
        return {"success": False, "error": str(e)}


async def export_to_png_tool(
    client: PenpotClient,
    file_id: str,
    page_id: str,
    scale: float = 1.0,
    shape_ids: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Export page or shapes to PNG format.

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        scale: Export scale factor (1.0 = 100%, 2.0 = 200%).
        shape_ids: Optional list of specific shape IDs to export.

    Returns:
        PNG content as base64 encoded string.
    """
    try:
        # If no shape_ids provided, export the entire page
        if not shape_ids:
            file_data = await client.get_file(file_id)
            data = file_data.get("data", {})
            objects = data.get("objects", {}).get(page_id, {})
            # Get all shape IDs from the page
            shape_ids = [str(obj_id) for obj_id in objects.keys()]

        if not shape_ids:
            return {"success": False, "error": "No shapes found to export"}

        png_bytes = await client.export_shapes(file_id, shape_ids, "png", scale)
        png_base64 = base64.b64encode(png_bytes).decode("utf-8")

        return {
            "success": True,
            "format": "png",
            "page_id": page_id,
            "scale": scale,
            "shape_count": len(shape_ids),
            "png_base64": png_base64,
            "size_bytes": len(png_bytes),
        }
    except Exception as e:
        logger.error(f"Failed to export to PNG: {e}")
        return {"success": False, "error": str(e)}


async def export_design_tokens_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    Export design tokens (colors, spacing, typography) as JSON.

    Args:
        client: Penpot API client.
        file_id: File UUID.

    Returns:
        Design tokens in structured format.
    """
    try:
        file_data = await client.get_file(file_id)
        data = file_data.get("data", {})
        pages_index = data.get("pages-index", {})

        # Collect all design tokens
        all_colors = set()
        all_typography = []
        spacing_values = set()

        for page_data in pages_index.values():
            page_id = page_data.get("id")
            objects = data.get("objects", {}).get(page_id, {})

            # Extract colors
            colors = extract_colors_from_objects(objects)
            all_colors.update(c["color"] for c in colors)

            # Extract typography
            typography = extract_typography_from_objects(objects)
            all_typography.extend(typography)

            # Extract spacing (from positions and sizes)
            for obj in objects.values():
                if isinstance(obj, dict):
                    if "x" in obj:
                        spacing_values.add(obj["x"])
                    if "y" in obj:
                        spacing_values.add(obj["y"])
                    if "width" in obj:
                        spacing_values.add(obj["width"])
                    if "height" in obj:
                        spacing_values.add(obj["height"])

        # Format design tokens
        design_tokens = {
            "colors": {
                f"color-{i}": color for i, color in enumerate(sorted(all_colors), 1)
            },
            "typography": {},
            "spacing": sorted([v for v in spacing_values if isinstance(v, (int, float))])[:20],
        }

        # Format typography
        unique_typography = []
        seen = set()
        for typo in all_typography:
            key = (typo["font_family"], typo["font_size"], typo["font_weight"])
            if key not in seen:
                seen.add(key)
                unique_typography.append(typo)

        for i, typo in enumerate(unique_typography, 1):
            design_tokens["typography"][f"text-style-{i}"] = {
                "fontFamily": typo["font_family"],
                "fontSize": f"{typo['font_size']}px",
                "fontWeight": typo["font_weight"],
                "textAlign": typo["text_align"],
            }

        return {
            "success": True,
            "file_id": file_id,
            "file_name": file_data.get("name"),
            "tokens": design_tokens,
        }
    except Exception as e:
        logger.error(f"Failed to export design tokens: {e}")
        return {"success": False, "error": str(e)}
