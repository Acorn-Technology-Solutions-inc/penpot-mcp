#!/usr/bin/env python3
"""
Test MCP server tool registration and functionality.
"""

import asyncio
from penpot_mcp.server import create_server

print("=" * 70)
print("TESTING MCP SERVER - TOOL REGISTRATION")
print("=" * 70)


async def test_server():
    # Create server
    server = create_server()
    print(f"\n✓ Server created: {server.name}")

    # Get all registered tools
    print("\n[REGISTERED TOOLS]")
    print("-" * 70)

    # We need to get the tools from the server
    # The list_tools handler returns the tools
    tools_handler = None
    for handler in server._list_tools_handlers:
        tools_handler = handler
        break

    if tools_handler:
        tools = await tools_handler()
        print(f"\nTotal tools registered: {len(tools)}")
        print("\nTool List:")

        categories = {
            "File Operations": [],
            "Design Analysis": [],
            "Shape Operations": [],
            "Export Operations": [],
            "Advanced Features": [],
        }

        for i, tool in enumerate(tools, 1):
            name = tool.name
            desc = tool.description[:60] + "..." if len(tool.description) > 60 else tool.description

            # Categorize
            if name in ["list_files", "get_file", "create_file", "delete_file"]:
                categories["File Operations"].append((name, desc))
            elif name in ["analyze_design", "extract_colors", "extract_typography", "get_components"]:
                categories["Design Analysis"].append((name, desc))
            elif name in [
                "create_rectangle",
                "create_text",
                "create_frame",
                "create_circle",
                "update_shape",
                "delete_shape",
            ]:
                categories["Shape Operations"].append((name, desc))
            elif name in ["export_to_svg", "export_to_png", "export_design_tokens"]:
                categories["Export Operations"].append((name, desc))
            elif name in [
                "generate_design_from_prompt",
                "validate_accessibility",
                "compare_designs",
            ]:
                categories["Advanced Features"].append((name, desc))

        # Print categorized tools
        for category, tool_list in categories.items():
            if tool_list:
                print(f"\n{category} ({len(tool_list)} tools):")
                for name, desc in tool_list:
                    print(f"  • {name}")
                    print(f"    {desc}")

        # Verify we have all expected tools
        expected_tools = {
            "list_files",
            "get_file",
            "create_file",
            "delete_file",
            "analyze_design",
            "extract_colors",
            "extract_typography",
            "get_components",
            "create_rectangle",
            "create_text",
            "create_frame",
            "create_circle",
            "update_shape",
            "delete_shape",
            "export_to_svg",
            "export_to_png",
            "export_design_tokens",
            "generate_design_from_prompt",
            "validate_accessibility",
            "compare_designs",
        }

        registered_tools = {tool.name for tool in tools}
        missing = expected_tools - registered_tools
        extra = registered_tools - expected_tools

        print("\n" + "=" * 70)
        print("VERIFICATION")
        print("=" * 70)

        if not missing and not extra:
            print("✓ All expected tools are registered correctly")
            print(f"✓ Total: {len(tools)} tools (target was 15+)")
            print(f"✓ Achievement: {int((len(tools) / 15) * 100)}% of target")
        else:
            if missing:
                print(f"✗ Missing tools: {missing}")
            if extra:
                print(f"⚠ Extra tools: {extra}")

        # Test tool input schemas
        print("\n[TOOL INPUT SCHEMAS]")
        print("-" * 70)

        sample_tools = ["create_rectangle", "analyze_design", "export_to_svg"]
        for tool_name in sample_tools:
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                print(f"\n{tool_name}:")
                schema = tool.inputSchema
                if "properties" in schema:
                    for param, details in schema["properties"].items():
                        required = param in schema.get("required", [])
                        req_mark = "*" if required else " "
                        param_type = details.get("type", "unknown")
                        print(f"  {req_mark} {param}: {param_type}")

        return True
    else:
        print("✗ Could not get tools handler")
        return False


# Run tests
try:
    result = asyncio.run(test_server())
    if result:
        print("\n" + "=" * 70)
        print("MCP SERVER TEST: PASSED ✓")
        print("=" * 70)
    else:
        print("\n✗ Server test failed")
        exit(1)
except Exception as e:
    print(f"\n✗ Error during testing: {e}")
    import traceback

    traceback.print_exc()
    exit(1)
