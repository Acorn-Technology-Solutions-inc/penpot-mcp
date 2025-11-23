"""
Shape operation tools for MCP server.
"""

import logging
import uuid
from typing import Any, Dict

from penpot_mcp.models.shape import ShapeModel, ShapeType
from penpot_mcp.penpot_client import PenpotClient

logger = logging.getLogger(__name__)


async def create_rectangle_tool(
    client: PenpotClient,
    file_id: str,
    page_id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    fill_color: str = "#000000",
    name: str = "Rectangle",
) -> Dict[str, Any]:
    """
    Create a rectangle shape.

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        x: X position.
        y: Y position.
        width: Width.
        height: Height.
        fill_color: Fill color (hex).
        name: Shape name.

    Returns:
        Created shape information.
    """
    try:
        shape = ShapeModel(
            id=str(uuid.uuid4()),
            type=ShapeType.RECT,
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            fill_color=fill_color,
        )

        shape_data = shape.to_penpot_format()
        result = await client.add_shape(file_id, page_id, shape_data)

        return {
            "success": True,
            "shape": {"id": shape.id, "type": "rectangle", "name": name},
            "message": f"Rectangle '{name}' created successfully",
        }
    except Exception as e:
        logger.error(f"Failed to create rectangle: {e}")
        return {"success": False, "error": str(e)}


async def create_text_tool(
    client: PenpotClient,
    file_id: str,
    page_id: str,
    x: float,
    y: float,
    text: str,
    font_size: int = 16,
    font_family: str = "Arial",
    fill_color: str = "#000000",
    name: str = "Text",
) -> Dict[str, Any]:
    """
    Create a text element.

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        x: X position.
        y: Y position.
        text: Text content.
        font_size: Font size in pixels.
        font_family: Font family name.
        fill_color: Text color (hex).
        name: Shape name.

    Returns:
        Created text element information.
    """
    try:
        shape = ShapeModel(
            id=str(uuid.uuid4()),
            type=ShapeType.TEXT,
            name=name,
            x=x,
            y=y,
            content=text,
            font_size=font_size,
            font_family=font_family,
            fill_color=fill_color,
        )

        shape_data = shape.to_penpot_format()
        result = await client.add_shape(file_id, page_id, shape_data)

        return {
            "success": True,
            "shape": {"id": shape.id, "type": "text", "name": name, "content": text},
            "message": f"Text '{name}' created successfully",
        }
    except Exception as e:
        logger.error(f"Failed to create text: {e}")
        return {"success": False, "error": str(e)}


async def create_frame_tool(
    client: PenpotClient,
    file_id: str,
    page_id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    name: str = "Frame",
    fill_color: str | None = None,
) -> Dict[str, Any]:
    """
    Create a frame (container).

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        x: X position.
        y: Y position.
        width: Width.
        height: Height.
        name: Frame name.
        fill_color: Optional fill color (hex).

    Returns:
        Created frame information.
    """
    try:
        shape = ShapeModel(
            id=str(uuid.uuid4()),
            type=ShapeType.FRAME,
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            fill_color=fill_color,
        )

        shape_data = shape.to_penpot_format()
        result = await client.add_shape(file_id, page_id, shape_data)

        return {
            "success": True,
            "shape": {"id": shape.id, "type": "frame", "name": name},
            "message": f"Frame '{name}' created successfully",
        }
    except Exception as e:
        logger.error(f"Failed to create frame: {e}")
        return {"success": False, "error": str(e)}


async def create_circle_tool(
    client: PenpotClient,
    file_id: str,
    page_id: str,
    x: float,
    y: float,
    radius: float,
    fill_color: str = "#000000",
    name: str = "Circle",
) -> Dict[str, Any]:
    """
    Create a circle shape.

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        x: Center X position.
        y: Center Y position.
        radius: Circle radius.
        fill_color: Fill color (hex).
        name: Shape name.

    Returns:
        Created shape information.
    """
    try:
        # Circle is created as a square with width/height = diameter
        diameter = radius * 2
        shape = ShapeModel(
            id=str(uuid.uuid4()),
            type=ShapeType.CIRCLE,
            name=name,
            x=x - radius,  # Adjust to center
            y=y - radius,
            width=diameter,
            height=diameter,
            fill_color=fill_color,
        )

        shape_data = shape.to_penpot_format()
        result = await client.add_shape(file_id, page_id, shape_data)

        return {
            "success": True,
            "shape": {"id": shape.id, "type": "circle", "name": name, "radius": radius},
            "message": f"Circle '{name}' created successfully",
        }
    except Exception as e:
        logger.error(f"Failed to create circle: {e}")
        return {"success": False, "error": str(e)}


async def update_shape_tool(
    client: PenpotClient, file_id: str, shape_id: str, properties: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update shape properties (position, size, color, etc.).

    Args:
        client: Penpot API client.
        file_id: File UUID.
        shape_id: Shape UUID.
        properties: Properties to update.

    Returns:
        Update confirmation.
    """
    try:
        # Convert property names to Penpot format
        penpot_properties = {}
        for key, value in properties.items():
            # Convert camelCase/snake_case to kebab-case
            penpot_key = key.replace("_", "-")
            penpot_properties[penpot_key] = value

        result = await client.update_shape(file_id, shape_id, penpot_properties)

        return {
            "success": True,
            "shape_id": shape_id,
            "updated_properties": list(properties.keys()),
            "message": f"Shape {shape_id} updated successfully",
        }
    except Exception as e:
        logger.error(f"Failed to update shape: {e}")
        return {"success": False, "error": str(e)}


async def delete_shape_tool(
    client: PenpotClient, file_id: str, page_id: str, shape_id: str
) -> Dict[str, Any]:
    """
    Delete a shape.

    Args:
        client: Penpot API client.
        file_id: File UUID.
        page_id: Page UUID.
        shape_id: Shape UUID.

    Returns:
        Deletion confirmation.
    """
    try:
        result = await client.delete_shape(file_id, page_id, shape_id)

        return {
            "success": True,
            "shape_id": shape_id,
            "message": f"Shape {shape_id} deleted successfully",
        }
    except Exception as e:
        logger.error(f"Failed to delete shape: {e}")
        return {"success": False, "error": str(e)}
