"""
Design analysis tools for MCP server.
"""

import logging
from collections import Counter
from typing import Any, Dict, List, Set

from penpot_mcp.penpot_client import PenpotClient

logger = logging.getLogger(__name__)


def extract_colors_from_objects(objects: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract all colors from shape objects.

    Args:
        objects: Dictionary of shape objects.

    Returns:
        List of colors with usage counts.
    """
    colors: List[str] = []

    for obj in objects.values():
        if isinstance(obj, dict):
            # Extract fill colors
            if "fill-color" in obj:
                colors.append(obj["fill-color"])

            # Extract stroke colors
            if "stroke-color" in obj:
                colors.append(obj["stroke-color"])

            # Extract from fills array
            if "fills" in obj:
                for fill in obj.get("fills", []):
                    if "fill-color" in fill:
                        colors.append(fill["fill-color"])

    # Count occurrences
    color_counts = Counter(colors)

    return [
        {"color": color, "count": count, "hex": color}
        for color, count in color_counts.most_common()
    ]


def extract_typography_from_objects(objects: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract typography information from text objects.

    Args:
        objects: Dictionary of shape objects.

    Returns:
        List of unique typography styles.
    """
    typography_styles: Set[tuple] = set()

    for obj in objects.values():
        if isinstance(obj, dict) and obj.get("type") == "text":
            font_family = obj.get("font-family", "Unknown")
            font_size = obj.get("font-size", 16)
            font_weight = obj.get("font-weight", "400")
            text_align = obj.get("text-align", "left")

            typography_styles.add((font_family, font_size, font_weight, text_align))

    return [
        {
            "font_family": style[0],
            "font_size": style[1],
            "font_weight": style[2],
            "text_align": style[3],
        }
        for style in typography_styles
    ]


async def analyze_design_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    AI-powered analysis of design file.

    Returns:
        - Color palette used
        - Typography styles
        - Component count
        - Layout structure
        - Design metrics
    """
    try:
        file_data = await client.get_file(file_id)
        data = file_data.get("data", {})

        # Get all pages
        pages_index = data.get("pages-index", {})
        page_count = len(pages_index)

        # Analyze all objects across all pages
        all_colors: List[str] = []
        all_typography: List[Dict[str, Any]] = []
        shape_counts: Dict[str, int] = {}
        total_shapes = 0

        for page_data in pages_index.values():
            page_id = page_data.get("id")
            objects = data.get("objects", {}).get(page_id, {})

            # Count shape types
            for obj in objects.values():
                if isinstance(obj, dict):
                    shape_type = obj.get("type", "unknown")
                    shape_counts[shape_type] = shape_counts.get(shape_type, 0) + 1
                    total_shapes += 1

            # Extract colors and typography
            colors = extract_colors_from_objects(objects)
            all_colors.extend([c["color"] for c in colors])

            typography = extract_typography_from_objects(objects)
            all_typography.extend(typography)

        # Get unique colors
        unique_colors = list(set(all_colors))
        color_palette = [{"color": c, "hex": c} for c in unique_colors[:20]]  # Top 20

        # Get unique typography
        unique_typography = []
        seen = set()
        for typo in all_typography:
            key = (typo["font_family"], typo["font_size"], typo["font_weight"])
            if key not in seen:
                seen.add(key)
                unique_typography.append(typo)

        return {
            "success": True,
            "analysis": {
                "file_id": file_id,
                "file_name": file_data.get("name"),
                "page_count": page_count,
                "total_shapes": total_shapes,
                "shape_types": shape_counts,
                "color_palette": color_palette,
                "color_count": len(unique_colors),
                "typography_styles": unique_typography[:10],  # Top 10
                "typography_count": len(unique_typography),
            },
        }
    except Exception as e:
        logger.error(f"Failed to analyze design: {e}")
        return {"success": False, "error": str(e)}


async def extract_colors_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    Extract all colors used in file with usage count.

    Args:
        client: Penpot API client.
        file_id: File UUID.

    Returns:
        Dictionary with color palette and usage statistics.
    """
    try:
        file_data = await client.get_file(file_id)
        data = file_data.get("data", {})
        pages_index = data.get("pages-index", {})

        all_colors: List[str] = []

        for page_data in pages_index.values():
            page_id = page_data.get("id")
            objects = data.get("objects", {}).get(page_id, {})
            colors = extract_colors_from_objects(objects)
            all_colors.extend([c["color"] for c in colors])

        color_counts = Counter(all_colors)
        color_palette = [
            {"color": color, "hex": color, "usage_count": count}
            for color, count in color_counts.most_common()
        ]

        return {
            "success": True,
            "file_id": file_id,
            "total_colors": len(color_palette),
            "colors": color_palette,
        }
    except Exception as e:
        logger.error(f"Failed to extract colors: {e}")
        return {"success": False, "error": str(e)}


async def extract_typography_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    Extract all text styles and fonts.

    Args:
        client: Penpot API client.
        file_id: File UUID.

    Returns:
        Dictionary with typography information.
    """
    try:
        file_data = await client.get_file(file_id)
        data = file_data.get("data", {})
        pages_index = data.get("pages-index", {})

        all_typography: List[Dict[str, Any]] = []

        for page_data in pages_index.values():
            page_id = page_data.get("id")
            objects = data.get("objects", {}).get(page_id, {})
            typography = extract_typography_from_objects(objects)
            all_typography.extend(typography)

        # Get unique styles
        unique_typography = []
        seen = set()
        for typo in all_typography:
            key = (typo["font_family"], typo["font_size"], typo["font_weight"])
            if key not in seen:
                seen.add(key)
                unique_typography.append(typo)

        return {
            "success": True,
            "file_id": file_id,
            "total_styles": len(unique_typography),
            "typography_styles": unique_typography,
        }
    except Exception as e:
        logger.error(f"Failed to extract typography: {e}")
        return {"success": False, "error": str(e)}


async def get_components_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    List all components and their instances.

    Args:
        client: Penpot API client.
        file_id: File UUID.

    Returns:
        Dictionary with component information.
    """
    try:
        file_data = await client.get_file(file_id)
        data = file_data.get("data", {})

        # Get components from file data
        components = data.get("components", {})
        component_list = []

        for comp_id, comp_data in components.items():
            component_list.append(
                {
                    "id": comp_id,
                    "name": comp_data.get("name", "Unnamed"),
                    "path": comp_data.get("path", ""),
                }
            )

        return {
            "success": True,
            "file_id": file_id,
            "total_components": len(component_list),
            "components": component_list,
        }
    except Exception as e:
        logger.error(f"Failed to get components: {e}")
        return {"success": False, "error": str(e)}
