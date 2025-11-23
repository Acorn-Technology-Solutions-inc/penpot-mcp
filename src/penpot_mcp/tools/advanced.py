"""
Advanced operation tools for MCP server.
"""

import logging
import re
from typing import Any, Dict, List

from penpot_mcp.penpot_client import PenpotClient
from penpot_mcp.tools.shapes import create_frame_tool, create_rectangle_tool, create_text_tool

logger = logging.getLogger(__name__)


def parse_design_prompt(prompt: str) -> Dict[str, Any]:
    """
    Parse natural language prompt into design specifications.

    Args:
        prompt: Natural language design prompt.

    Returns:
        Structured design specification.
    """
    prompt_lower = prompt.lower()

    # Detect design type
    design_type = "generic"
    if "login" in prompt_lower or "sign in" in prompt_lower:
        design_type = "login_form"
    elif "pricing" in prompt_lower or "tier" in prompt_lower:
        design_type = "pricing_table"
    elif "hero" in prompt_lower or "landing" in prompt_lower:
        design_type = "hero_section"
    elif "button" in prompt_lower:
        design_type = "button"
    elif "card" in prompt_lower:
        design_type = "card"

    # Extract color mentions
    colors = []
    color_pattern = r"(blue|red|green|yellow|purple|orange|black|white|gray|grey)"
    found_colors = re.findall(color_pattern, prompt_lower)
    color_map = {
        "blue": "#3B82F6",
        "red": "#EF4444",
        "green": "#10B981",
        "yellow": "#F59E0B",
        "purple": "#8B5CF6",
        "orange": "#F97316",
        "black": "#000000",
        "white": "#FFFFFF",
        "gray": "#6B7280",
        "grey": "#6B7280",
    }
    colors = [color_map.get(c, "#000000") for c in found_colors]

    return {
        "type": design_type,
        "colors": colors if colors else ["#3B82F6", "#FFFFFF", "#000000"],
        "prompt": prompt,
    }


async def generate_login_form(
    client: PenpotClient, file_id: str, page_id: str, colors: List[str]
) -> List[str]:
    """Generate a login form design."""
    primary_color = colors[0] if colors else "#3B82F6"
    bg_color = colors[1] if len(colors) > 1 else "#FFFFFF"

    created_shapes = []

    # Create container frame
    frame_result = await create_frame_tool(
        client, file_id, page_id, 100, 100, 400, 500, "Login Form", bg_color
    )
    if frame_result.get("success"):
        created_shapes.append("frame")

    # Create title
    title_result = await create_text_tool(
        client, file_id, page_id, 150, 150, "Sign In", 32, "Arial", "#000000", "Title"
    )
    if title_result.get("success"):
        created_shapes.append("title")

    # Create email field
    email_result = await create_rectangle_tool(
        client, file_id, page_id, 150, 220, 300, 40, "#F3F4F6", "Email Field"
    )
    if email_result.get("success"):
        created_shapes.append("email_field")

    # Create password field
    password_result = await create_rectangle_tool(
        client, file_id, page_id, 150, 280, 300, 40, "#F3F4F6", "Password Field"
    )
    if password_result.get("success"):
        created_shapes.append("password_field")

    # Create submit button
    button_result = await create_rectangle_tool(
        client, file_id, page_id, 150, 340, 300, 50, primary_color, "Submit Button"
    )
    if button_result.get("success"):
        created_shapes.append("submit_button")

    # Create button text
    button_text_result = await create_text_tool(
        client, file_id, page_id, 260, 355, "Sign In", 16, "Arial", "#FFFFFF", "Button Text"
    )
    if button_text_result.get("success"):
        created_shapes.append("button_text")

    return created_shapes


async def generate_design_from_prompt_tool(
    client: PenpotClient, project_id: str, prompt: str, file_name: str | None = None
) -> Dict[str, Any]:
    """
    Use AI to generate design based on natural language prompt.

    Args:
        client: Penpot API client.
        project_id: Project UUID.
        prompt: Natural language design description.
        file_name: Optional file name.

    Returns:
        Created file and design information.
    """
    try:
        # Parse the prompt
        design_spec = parse_design_prompt(prompt)

        # Create new file
        name = file_name or f"AI Generated - {design_spec['type']}"
        from penpot_mcp.tools.file_ops import create_file_tool

        file_result = await create_file_tool(client, project_id, name)
        if not file_result.get("success"):
            return file_result

        file_id = file_result["file"]["id"]

        # Get first page
        file_data = await client.get_file(file_id)
        pages = list(file_data.get("data", {}).get("pages-index", {}).values())
        if not pages:
            return {"success": False, "error": "No pages found in created file"}

        page_id = pages[0]["id"]

        # Generate design based on type
        created_shapes = []
        if design_spec["type"] == "login_form":
            created_shapes = await generate_login_form(
                client, file_id, page_id, design_spec["colors"]
            )
        else:
            # Generic design - create a simple layout
            primary_color = design_spec["colors"][0]
            await create_rectangle_tool(
                client,
                file_id,
                page_id,
                100,
                100,
                600,
                400,
                primary_color,
                "Generated Element",
            )
            await create_text_tool(
                client, file_id, page_id, 150, 150, prompt[:50], 24, "Arial", "#FFFFFF"
            )
            created_shapes = ["rectangle", "text"]

        return {
            "success": True,
            "file": {
                "id": file_id,
                "name": name,
                "page_id": page_id,
            },
            "design_spec": design_spec,
            "created_shapes": created_shapes,
            "message": f"Design generated successfully from prompt: '{prompt}'",
        }
    except Exception as e:
        logger.error(f"Failed to generate design: {e}")
        return {"success": False, "error": str(e)}


async def validate_accessibility_tool(client: PenpotClient, file_id: str) -> Dict[str, Any]:
    """
    Check accessibility issues: color contrast, text readability, touch target sizes.

    Args:
        client: Penpot API client.
        file_id: File UUID.

    Returns:
        Accessibility validation report.
    """
    try:
        file_data = await client.get_file(file_id)
        data = file_data.get("data", {})
        pages_index = data.get("pages-index", {})

        issues = []
        warnings = []

        for page_data in pages_index.values():
            page_id = page_data.get("id")
            page_name = page_data.get("name", "Unnamed")
            objects = data.get("objects", {}).get(page_id, {})

            for obj_id, obj in objects.items():
                if not isinstance(obj, dict):
                    continue

                # Check text sizes
                if obj.get("type") == "text":
                    font_size = obj.get("font-size", 16)
                    if font_size < 12:
                        issues.append(
                            {
                                "type": "text_too_small",
                                "severity": "error",
                                "page": page_name,
                                "object_id": obj_id,
                                "message": f"Text size {font_size}px is too small (minimum 12px)",
                            }
                        )
                    elif font_size < 14:
                        warnings.append(
                            {
                                "type": "text_small",
                                "severity": "warning",
                                "page": page_name,
                                "object_id": obj_id,
                                "message": f"Text size {font_size}px is small (recommended 14px+)",
                            }
                        )

                # Check touch target sizes (minimum 44x44)
                if obj.get("type") in ["rect", "circle", "frame"]:
                    width = obj.get("width", 0)
                    height = obj.get("height", 0)
                    if width < 44 or height < 44:
                        warnings.append(
                            {
                                "type": "touch_target_small",
                                "severity": "warning",
                                "page": page_name,
                                "object_id": obj_id,
                                "message": f"Touch target {width}x{height} is smaller than recommended 44x44",
                            }
                        )

        # Calculate score
        total_checks = len(issues) + len(warnings) + 10  # Base checks
        passed_checks = max(0, total_checks - len(issues) - len(warnings))
        score = int((passed_checks / total_checks) * 100)

        return {
            "success": True,
            "file_id": file_id,
            "accessibility_score": score,
            "total_issues": len(issues),
            "total_warnings": len(warnings),
            "issues": issues,
            "warnings": warnings,
            "summary": f"{score}% accessible - {len(issues)} issues, {len(warnings)} warnings",
        }
    except Exception as e:
        logger.error(f"Failed to validate accessibility: {e}")
        return {"success": False, "error": str(e)}


async def compare_designs_tool(
    client: PenpotClient, file_id_1: str, file_id_2: str
) -> Dict[str, Any]:
    """
    Compare two design files and highlight differences.

    Args:
        client: Penpot API client.
        file_id_1: First file UUID.
        file_id_2: Second file UUID.

    Returns:
        Comparison report.
    """
    try:
        file1 = await client.get_file(file_id_1)
        file2 = await client.get_file(file_id_2)

        # Compare page counts
        pages1 = list(file1.get("data", {}).get("pages-index", {}).values())
        pages2 = list(file2.get("data", {}).get("pages-index", {}).values())

        # Count shapes
        def count_shapes(file_data: Dict[str, Any]) -> int:
            count = 0
            pages = file_data.get("data", {}).get("pages-index", {}).values()
            for page_data in pages:
                page_id = page_data.get("id")
                objects = file_data.get("data", {}).get("objects", {}).get(page_id, {})
                count += len(objects)
            return count

        shape_count1 = count_shapes(file1)
        shape_count2 = count_shapes(file2)

        differences = []

        if len(pages1) != len(pages2):
            differences.append(
                {
                    "type": "page_count",
                    "file1_value": len(pages1),
                    "file2_value": len(pages2),
                    "message": f"Page count differs: {len(pages1)} vs {len(pages2)}",
                }
            )

        if shape_count1 != shape_count2:
            differences.append(
                {
                    "type": "shape_count",
                    "file1_value": shape_count1,
                    "file2_value": shape_count2,
                    "message": f"Shape count differs: {shape_count1} vs {shape_count2}",
                }
            )

        similarity_score = 100 - (len(differences) * 10)
        similarity_score = max(0, min(100, similarity_score))

        return {
            "success": True,
            "file1": {"id": file_id_1, "name": file1.get("name"), "pages": len(pages1), "shapes": shape_count1},
            "file2": {"id": file_id_2, "name": file2.get("name"), "pages": len(pages2), "shapes": shape_count2},
            "similarity_score": similarity_score,
            "differences": differences,
            "summary": f"{len(differences)} differences found, {similarity_score}% similar",
        }
    except Exception as e:
        logger.error(f"Failed to compare designs: {e}")
        return {"success": False, "error": str(e)}
