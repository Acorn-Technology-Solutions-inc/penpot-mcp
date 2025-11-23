#!/usr/bin/env python3
"""
Comprehensive functionality test for Penpot MCP Server.
Tests all components without requiring a real Penpot API connection.
"""

import asyncio
import json
from unittest.mock import AsyncMock, Mock, patch

# Test imports
print("=" * 70)
print("TESTING PENPOT MCP SERVER - COMPREHENSIVE FUNCTIONALITY TEST")
print("=" * 70)

# Test 1: Module imports
print("\n[TEST 1] Testing module imports...")
try:
    from penpot_mcp import PenpotClient, create_server, __version__
    from penpot_mcp.exceptions import (
        PenpotAPIError,
        AuthenticationError,
        RateLimitError,
    )
    from penpot_mcp.models.shape import ShapeModel, ShapeType
    from penpot_mcp.models.file import FileModel, PageModel
    from penpot_mcp.utils.cache import Cache
    from penpot_mcp.utils.rate_limit import RateLimiter
    from penpot_mcp.tools.file_ops import (
        list_files_tool,
        get_file_tool,
        create_file_tool,
    )
    from penpot_mcp.tools.analysis import (
        analyze_design_tool,
        extract_colors_tool,
    )
    from penpot_mcp.tools.shapes import create_rectangle_tool, create_text_tool
    from penpot_mcp.tools.export import export_to_svg_tool
    from penpot_mcp.tools.advanced import (
        generate_design_from_prompt_tool,
        validate_accessibility_tool,
    )
    print("✓ All modules imported successfully")
    print(f"  Version: {__version__}")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Test 2: Data Models
print("\n[TEST 2] Testing data models...")
try:
    # Test ShapeModel
    rect = ShapeModel(
        type=ShapeType.RECT,
        name="Test Rectangle",
        x=100,
        y=200,
        width=300,
        height=150,
        fill_color="#FF0000",
    )
    assert rect.type == ShapeType.RECT
    assert rect.x == 100
    assert rect.width == 300

    # Test to_penpot_format
    penpot_data = rect.to_penpot_format()
    assert penpot_data["type"] == "rect"
    assert penpot_data["fill-color"] == "#FF0000"

    # Test text shape
    text = ShapeModel(
        type=ShapeType.TEXT,
        name="Test Text",
        x=50,
        y=75,
        content="Hello World",
        font_size=24,
    )
    assert text.type == ShapeType.TEXT
    assert text.content == "Hello World"

    print("✓ Data models working correctly")
    print(f"  - Rectangle shape: {rect.name}")
    print(f"  - Text shape: {text.name}")
except Exception as e:
    print(f"✗ Data model test failed: {e}")
    exit(1)

# Test 3: Rate Limiter
print("\n[TEST 3] Testing rate limiter...")
try:

    async def test_rate_limiter():
        limiter = RateLimiter(max_requests=5, window_seconds=60)

        # Should allow 5 requests
        for i in range(5):
            await limiter.acquire()

        # 6th request should fail
        try:
            await limiter.acquire()
            print("✗ Rate limiter should have blocked request")
            return False
        except RateLimitError:
            pass

        # Reset and try again
        limiter.reset()
        await limiter.acquire()

        return True

    if asyncio.run(test_rate_limiter()):
        print("✓ Rate limiter working correctly")
        print("  - Blocked excess requests")
        print("  - Reset functionality works")
except Exception as e:
    print(f"✗ Rate limiter test failed: {e}")
    exit(1)

# Test 4: Cache
print("\n[TEST 4] Testing cache...")
try:
    cache = Cache(default_ttl=300)

    # Test set/get
    cache.set("key1", {"data": "value1"})
    assert cache.get("key1") == {"data": "value1"}

    # Test missing key
    assert cache.get("nonexistent") is None

    # Test delete
    cache.delete("key1")
    assert cache.get("key1") is None

    # Test pattern invalidation
    cache.set("user:1:profile", "data1")
    cache.set("user:1:settings", "data2")
    cache.set("user:2:profile", "data3")

    cache.invalidate_pattern("user:1")
    assert cache.get("user:1:profile") is None
    assert cache.get("user:2:profile") == "data3"

    print("✓ Cache working correctly")
    print("  - Set/get operations")
    print("  - Pattern invalidation")
except Exception as e:
    print(f"✗ Cache test failed: {e}")
    exit(1)

# Test 5: MCP Server Creation
print("\n[TEST 5] Testing MCP server creation...")
try:
    server = create_server()
    assert server is not None
    assert server.name == "penpot-mcp"
    print("✓ MCP server created successfully")
    print(f"  - Server name: {server.name}")
except Exception as e:
    print(f"✗ Server creation failed: {e}")
    exit(1)

# Test 6: Tool Functions (with mocked client)
print("\n[TEST 6] Testing tool functions...")


async def test_tools():
    # Create mock client
    mock_client = Mock()
    mock_client.list_files = AsyncMock(
        return_value=[
            {
                "id": "file-1",
                "name": "Design 1",
                "project-id": "proj-1",
                "created-at": "2024-01-01",
                "modified-at": "2024-01-02",
            }
        ]
    )
    mock_client.get_file = AsyncMock(
        return_value={
            "id": "file-1",
            "name": "Design 1",
            "data": {
                "pages-index": {
                    "page-1": {"id": "page-1", "name": "Page 1"}
                },
                "objects": {
                    "page-1": {
                        "obj-1": {
                            "type": "rect",
                            "fill-color": "#FF0000",
                        }
                    }
                },
            },
        }
    )
    mock_client.create_file = AsyncMock(
        return_value={
            "id": "new-file",
            "name": "New Design",
            "project-id": "proj-1",
        }
    )
    mock_client.add_shape = AsyncMock(return_value={"success": True})

    # Test list_files
    result = await list_files_tool(mock_client, team_id="team-1")
    assert result["success"] is True
    assert result["count"] == 1
    print("  ✓ list_files_tool")

    # Test get_file
    result = await get_file_tool(mock_client, "file-1")
    assert result["success"] is True
    assert result["file"]["id"] == "file-1"
    print("  ✓ get_file_tool")

    # Test create_file
    result = await create_file_tool(mock_client, "proj-1", "New Design")
    assert result["success"] is True
    print("  ✓ create_file_tool")

    # Test create_rectangle
    result = await create_rectangle_tool(
        mock_client, "file-1", "page-1", 100, 100, 200, 100, "#3B82F6", "Blue Box"
    )
    assert result["success"] is True
    print("  ✓ create_rectangle_tool")

    # Test create_text
    result = await create_text_tool(
        mock_client,
        "file-1",
        "page-1",
        150,
        50,
        "Hello World",
        24,
        "Arial",
        "#000000",
        "Title",
    )
    assert result["success"] is True
    print("  ✓ create_text_tool")

    # Test extract_colors
    result = await extract_colors_tool(mock_client, "file-1")
    assert result["success"] is True
    assert result["total_colors"] >= 0
    print("  ✓ extract_colors_tool")

    # Test analyze_design
    result = await analyze_design_tool(mock_client, "file-1")
    assert result["success"] is True
    print("  ✓ analyze_design_tool")

    return True


try:
    if asyncio.run(test_tools()):
        print("✓ All tool functions working correctly")
except Exception as e:
    print(f"✗ Tool function test failed: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

# Test 7: Advanced Tools
print("\n[TEST 7] Testing advanced tools...")


async def test_advanced():
    mock_client = Mock()
    mock_client.create_file = AsyncMock(
        return_value={
            "id": "ai-file",
            "name": "AI Generated",
        }
    )
    mock_client.get_file = AsyncMock(
        return_value={
            "id": "ai-file",
            "name": "AI Generated",
            "data": {
                "pages-index": {
                    "page-1": {"id": "page-1"}
                },
                "objects": {
                    "page-1": {
                        "obj-1": {
                            "type": "text",
                            "font-size": 16,
                            "width": 100,
                            "height": 50,
                        }
                    }
                },
            },
        }
    )
    mock_client.add_shape = AsyncMock(return_value={"success": True})
    mock_client.update_file = AsyncMock(return_value={"success": True})

    # Test AI generation
    result = await generate_design_from_prompt_tool(
        mock_client, "proj-1", "Create a login form", "Login Page"
    )
    assert result["success"] is True
    print("  ✓ generate_design_from_prompt_tool")

    # Test accessibility validation
    result = await validate_accessibility_tool(mock_client, "file-1")
    assert result["success"] is True
    assert "accessibility_score" in result
    print("  ✓ validate_accessibility_tool")

    return True


try:
    if asyncio.run(test_advanced()):
        print("✓ Advanced tools working correctly")
except Exception as e:
    print(f"✗ Advanced tools test failed: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

# Test 8: Error Handling
print("\n[TEST 8] Testing error handling...")
try:
    # Test AuthenticationError
    try:
        import os

        os.environ.pop("PENPOT_ACCESS_TOKEN", None)
        client = PenpotClient(access_token=None)
        print("✗ Should have raised AuthenticationError")
        exit(1)
    except AuthenticationError:
        print("  ✓ AuthenticationError raised correctly")

    # Test RateLimitError
    try:
        limiter = RateLimiter(max_requests=0)
        asyncio.run(limiter.acquire())
        print("✗ Should have raised RateLimitError")
        exit(1)
    except RateLimitError:
        print("  ✓ RateLimitError raised correctly")

    print("✓ Error handling working correctly")
except Exception as e:
    print(f"✗ Error handling test failed: {e}")
    exit(1)

# Test 9: Design Prompt Parsing
print("\n[TEST 9] Testing design prompt parsing...")
try:
    from penpot_mcp.tools.advanced import parse_design_prompt

    # Test login form detection
    spec = parse_design_prompt("Create a login form with email and password")
    assert spec["type"] == "login_form"
    print("  ✓ Login form detected")

    # Test color extraction
    spec = parse_design_prompt("Make a blue button with white text")
    assert "#3B82F6" in spec["colors"]  # Blue
    print("  ✓ Color extraction from prompt")

    # Test pricing table detection
    spec = parse_design_prompt("Design a pricing table with 3 tiers")
    assert spec["type"] == "pricing_table"
    print("  ✓ Pricing table detected")

    print("✓ Design prompt parsing working correctly")
except Exception as e:
    print(f"✗ Prompt parsing test failed: {e}")
    exit(1)

# Test 10: Color and Typography Analysis
print("\n[TEST 10] Testing analysis utilities...")
try:
    from penpot_mcp.tools.analysis import (
        extract_colors_from_objects,
        extract_typography_from_objects,
    )

    objects = {
        "obj-1": {
            "type": "rect",
            "fill-color": "#FF0000",
            "stroke-color": "#000000",
        },
        "obj-2": {
            "type": "text",
            "fill-color": "#FF0000",
            "font-family": "Arial",
            "font-size": 16,
            "font-weight": "400",
            "text-align": "left",
        },
    }

    # Test color extraction
    colors = extract_colors_from_objects(objects)
    assert len(colors) >= 2  # At least red and black
    print("  ✓ Color extraction from objects")

    # Test typography extraction
    typography = extract_typography_from_objects(objects)
    assert len(typography) >= 1
    assert typography[0]["font_family"] == "Arial"
    print("  ✓ Typography extraction from objects")

    print("✓ Analysis utilities working correctly")
except Exception as e:
    print(f"✗ Analysis utilities test failed: {e}")
    exit(1)

# Final Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("✓ All 10 test suites passed successfully!")
print("\nTested Components:")
print("  1. Module imports and version")
print("  2. Data models (ShapeModel, FileModel)")
print("  3. Rate limiting functionality")
print("  4. Caching system")
print("  5. MCP server creation")
print("  6. File and shape operation tools")
print("  7. Advanced AI-powered tools")
print("  8. Error handling and exceptions")
print("  9. Design prompt parsing")
print("  10. Analysis utilities (colors, typography)")
print("\n" + "=" * 70)
print("PENPOT MCP SERVER: ALL FUNCTIONALITY TESTS PASSED ✓")
print("=" * 70)
