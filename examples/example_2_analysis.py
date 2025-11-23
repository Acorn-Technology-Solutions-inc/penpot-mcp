"""
Example 2: Design analysis and color extraction.

This example demonstrates:
1. Analyzing an existing design file
2. Extracting color palette
3. Extracting typography
4. Getting component information
"""

import asyncio
import os

from penpot_mcp.penpot_client import PenpotClient
from penpot_mcp.tools.analysis import (
    analyze_design_tool,
    extract_colors_tool,
    extract_typography_tool,
)


async def main():
    """Run analysis example."""
    if not os.getenv("PENPOT_ACCESS_TOKEN"):
        print("Error: PENPOT_ACCESS_TOKEN environment variable not set")
        return

    # You need to provide a file ID to analyze
    file_id = input("Enter a Penpot file ID to analyze: ").strip()
    if not file_id:
        print("No file ID provided!")
        return

    async with PenpotClient() as client:
        print(f"Analyzing file: {file_id}\n")

        # Comprehensive design analysis
        print("=" * 60)
        print("DESIGN ANALYSIS")
        print("=" * 60)
        analysis = await analyze_design_tool(client, file_id)
        if analysis.get("success"):
            data = analysis["analysis"]
            print(f"File: {data['file_name']}")
            print(f"Pages: {data['page_count']}")
            print(f"Total Shapes: {data['total_shapes']}")
            print(f"\nShape Types:")
            for shape_type, count in data["shape_types"].items():
                print(f"  - {shape_type}: {count}")
            print(f"\nColors Found: {data['color_count']}")
            print(f"Typography Styles: {data['typography_count']}")
        else:
            print(f"Error: {analysis.get('error')}")

        # Extract colors
        print("\n" + "=" * 60)
        print("COLOR PALETTE")
        print("=" * 60)
        colors = await extract_colors_tool(client, file_id)
        if colors.get("success"):
            print(f"Total unique colors: {colors['total_colors']}\n")
            for i, color in enumerate(colors["colors"][:10], 1):  # Top 10
                print(f"{i}. {color['hex']} (used {color['usage_count']} times)")
        else:
            print(f"Error: {colors.get('error')}")

        # Extract typography
        print("\n" + "=" * 60)
        print("TYPOGRAPHY STYLES")
        print("=" * 60)
        typography = await extract_typography_tool(client, file_id)
        if typography.get("success"):
            print(f"Total unique styles: {typography['total_styles']}\n")
            for i, style in enumerate(typography["typography_styles"][:10], 1):  # Top 10
                print(f"{i}. {style['font_family']} - {style['font_size']}px")
                print(f"   Weight: {style['font_weight']}, Align: {style['text_align']}")
        else:
            print(f"Error: {typography.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
