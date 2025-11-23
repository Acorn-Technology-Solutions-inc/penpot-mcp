# Penpot MCP API Reference

This document provides detailed API reference for all MCP tools available in the Penpot MCP server.

## Table of Contents

1. [File Operations](#file-operations)
2. [Design Analysis](#design-analysis)
3. [Shape Operations](#shape-operations)
4. [Export Operations](#export-operations)
5. [Advanced Features](#advanced-features)

---

## File Operations

### list_files

List all design files in a team or project.

**Parameters:**
- `team_id` (string, optional): Team UUID
- `project_id` (string, optional): Project UUID to filter

**Returns:**
```json
{
  "success": true,
  "count": 5,
  "files": [
    {
      "id": "file-uuid-123",
      "name": "My Design",
      "project_id": "project-uuid-456",
      "created_at": "2024-01-01T00:00:00Z",
      "modified_at": "2024-01-02T00:00:00Z"
    }
  ]
}
```

**Example:**
```
"List all files in project xyz-123"
```

---

### get_file

Get complete file data including all pages and shapes.

**Parameters:**
- `file_id` (string, required): Penpot file UUID

**Returns:**
```json
{
  "success": true,
  "file": {
    "id": "file-uuid-123",
    "name": "My Design",
    "project_id": "project-uuid-456",
    "page_count": 3
  },
  "data": { /* Complete file data */ }
}
```

**Example:**
```
"Get file xyz-123 and show me its contents"
```

---

### create_file

Create a new Penpot design file.

**Parameters:**
- `project_id` (string, required): Project UUID where file will be created
- `name` (string, required): File name

**Returns:**
```json
{
  "success": true,
  "file": {
    "id": "new-file-uuid",
    "name": "New Design",
    "project_id": "project-uuid-456",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

**Example:**
```
"Create a new file called 'Landing Page Design' in project abc-789"
```

---

### delete_file

Delete a Penpot file permanently.

**Parameters:**
- `file_id` (string, required): File UUID to delete

**Returns:**
```json
{
  "success": true,
  "message": "File xyz-123 deleted successfully"
}
```

**Example:**
```
"Delete file xyz-123"
```

---

## Design Analysis

### analyze_design

Perform comprehensive AI-powered analysis of a design file.

**Parameters:**
- `file_id` (string, required): File UUID to analyze

**Returns:**
```json
{
  "success": true,
  "analysis": {
    "file_id": "file-uuid-123",
    "file_name": "My Design",
    "page_count": 3,
    "total_shapes": 45,
    "shape_types": {
      "rect": 15,
      "text": 20,
      "frame": 10
    },
    "color_palette": [
      {"color": "#3B82F6", "hex": "#3B82F6"}
    ],
    "color_count": 8,
    "typography_styles": [
      {
        "font_family": "Arial",
        "font_size": 16,
        "font_weight": "400"
      }
    ],
    "typography_count": 5
  }
}
```

**Example:**
```
"Analyze the design in file xyz-123"
```

---

### extract_colors

Extract all colors used in a file with usage statistics.

**Parameters:**
- `file_id` (string, required): File UUID

**Returns:**
```json
{
  "success": true,
  "file_id": "file-uuid-123",
  "total_colors": 10,
  "colors": [
    {
      "color": "#3B82F6",
      "hex": "#3B82F6",
      "usage_count": 15
    }
  ]
}
```

**Example:**
```
"Extract all colors from file xyz-123"
```

---

### extract_typography

Extract all text styles and fonts used in a file.

**Parameters:**
- `file_id` (string, required): File UUID

**Returns:**
```json
{
  "success": true,
  "file_id": "file-uuid-123",
  "total_styles": 8,
  "typography_styles": [
    {
      "font_family": "Arial",
      "font_size": 16,
      "font_weight": "400",
      "text_align": "left"
    }
  ]
}
```

**Example:**
```
"Show me all typography styles in file xyz-123"
```

---

### get_components

List all components and their instances in a file.

**Parameters:**
- `file_id` (string, required): File UUID

**Returns:**
```json
{
  "success": true,
  "file_id": "file-uuid-123",
  "total_components": 5,
  "components": [
    {
      "id": "component-uuid-123",
      "name": "Button",
      "path": "Components/Buttons"
    }
  ]
}
```

**Example:**
```
"List all components in file xyz-123"
```

---

## Shape Operations

### create_rectangle

Create a rectangle shape on a page.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `x` (number, required): X position
- `y` (number, required): Y position
- `width` (number, required): Width
- `height` (number, required): Height
- `fill_color` (string, optional): Fill color in hex (default: #000000)
- `name` (string, optional): Shape name (default: "Rectangle")

**Returns:**
```json
{
  "success": true,
  "shape": {
    "id": "shape-uuid-123",
    "type": "rectangle",
    "name": "Blue Box"
  },
  "message": "Rectangle 'Blue Box' created successfully"
}
```

**Example:**
```
"Create a blue rectangle at (100, 100) with size 200x100"
```

---

### create_text

Create a text element on a page.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `x` (number, required): X position
- `y` (number, required): Y position
- `text` (string, required): Text content
- `font_size` (integer, optional): Font size in pixels (default: 16)
- `font_family` (string, optional): Font family name (default: "Arial")
- `fill_color` (string, optional): Text color in hex (default: #000000)
- `name` (string, optional): Element name (default: "Text")

**Returns:**
```json
{
  "success": true,
  "shape": {
    "id": "shape-uuid-456",
    "type": "text",
    "name": "Title",
    "content": "Welcome"
  },
  "message": "Text 'Title' created successfully"
}
```

**Example:**
```
"Add text 'Welcome' at position (150, 50) with font size 24"
```

---

### create_frame

Create a frame (container) on a page.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `x` (number, required): X position
- `y` (number, required): Y position
- `width` (number, required): Width
- `height` (number, required): Height
- `name` (string, optional): Frame name (default: "Frame")
- `fill_color` (string, optional): Fill color in hex

**Example:**
```
"Create a frame at (0, 0) with size 1920x1080"
```

---

### create_circle

Create a circle shape on a page.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `x` (number, required): Center X position
- `y` (number, required): Center Y position
- `radius` (number, required): Circle radius
- `fill_color` (string, optional): Fill color in hex (default: #000000)
- `name` (string, optional): Shape name (default: "Circle")

**Example:**
```
"Create a red circle with radius 50 at center (200, 200)"
```

---

### update_shape

Update properties of an existing shape.

**Parameters:**
- `file_id` (string, required): File UUID
- `shape_id` (string, required): Shape UUID
- `properties` (object, required): Properties to update

**Example:**
```
"Update shape xyz-123 to have blue fill color"
```

---

### delete_shape

Delete a shape from a page.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `shape_id` (string, required): Shape UUID

**Example:**
```
"Delete shape xyz-123 from the page"
```

---

## Export Operations

### export_to_svg

Export a page or specific shapes to SVG format.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `shape_ids` (array, optional): Optional array of shape IDs to export

**Returns:**
```json
{
  "success": true,
  "format": "svg",
  "page_id": "page-uuid-123",
  "shape_count": 10,
  "svg": "<svg>...</svg>",
  "size_bytes": 2048
}
```

**Example:**
```
"Export page xyz-123 to SVG"
```

---

### export_to_png

Export a page or specific shapes to PNG format.

**Parameters:**
- `file_id` (string, required): File UUID
- `page_id` (string, required): Page UUID
- `scale` (number, optional): Export scale factor (default: 1.0)
- `shape_ids` (array, optional): Optional array of shape IDs to export

**Returns:**
```json
{
  "success": true,
  "format": "png",
  "page_id": "page-uuid-123",
  "scale": 2.0,
  "shape_count": 10,
  "png_base64": "iVBORw0KGgoAAAANS...",
  "size_bytes": 4096
}
```

**Example:**
```
"Export page xyz-123 to PNG at 2x scale"
```

---

### export_design_tokens

Export design tokens (colors, spacing, typography) as structured JSON.

**Parameters:**
- `file_id` (string, required): File UUID

**Returns:**
```json
{
  "success": true,
  "file_id": "file-uuid-123",
  "file_name": "Design System",
  "tokens": {
    "colors": {
      "color-1": "#3B82F6",
      "color-2": "#EF4444"
    },
    "typography": {
      "text-style-1": {
        "fontFamily": "Arial",
        "fontSize": "16px",
        "fontWeight": "400"
      }
    },
    "spacing": [8, 16, 24, 32]
  }
}
```

**Example:**
```
"Export design tokens from file xyz-123"
```

---

## Advanced Features

### generate_design_from_prompt

Generate a design from a natural language prompt using AI.

**Parameters:**
- `project_id` (string, required): Project UUID
- `prompt` (string, required): Natural language design description
- `file_name` (string, optional): Optional file name

**Returns:**
```json
{
  "success": true,
  "file": {
    "id": "new-file-uuid",
    "name": "AI Generated - login_form",
    "page_id": "page-uuid-123"
  },
  "design_spec": {
    "type": "login_form",
    "colors": ["#3B82F6", "#FFFFFF"]
  },
  "created_shapes": ["frame", "title", "email_field", "password_field", "submit_button"],
  "message": "Design generated successfully from prompt"
}
```

**Example:**
```
"Create a login form with email and password fields"
```

---

### validate_accessibility

Check design for accessibility issues.

**Parameters:**
- `file_id` (string, required): File UUID

**Returns:**
```json
{
  "success": true,
  "file_id": "file-uuid-123",
  "accessibility_score": 85,
  "total_issues": 2,
  "total_warnings": 3,
  "issues": [
    {
      "type": "text_too_small",
      "severity": "error",
      "page": "Page 1",
      "object_id": "shape-uuid-123",
      "message": "Text size 10px is too small (minimum 12px)"
    }
  ],
  "warnings": [],
  "summary": "85% accessible - 2 issues, 3 warnings"
}
```

**Example:**
```
"Check if file xyz-123 meets accessibility standards"
```

---

### compare_designs

Compare two design files and highlight differences.

**Parameters:**
- `file_id_1` (string, required): First file UUID
- `file_id_2` (string, required): Second file UUID

**Returns:**
```json
{
  "success": true,
  "file1": {
    "id": "file-1-uuid",
    "name": "Design V1",
    "pages": 3,
    "shapes": 45
  },
  "file2": {
    "id": "file-2-uuid",
    "name": "Design V2",
    "pages": 3,
    "shapes": 50
  },
  "similarity_score": 90,
  "differences": [
    {
      "type": "shape_count",
      "file1_value": 45,
      "file2_value": 50,
      "message": "Shape count differs: 45 vs 50"
    }
  ],
  "summary": "1 differences found, 90% similar"
}
```

**Example:**
```
"Compare files abc-123 and def-456"
```

---

## Error Handling

All tools return a consistent error format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "tool": "tool_name"
}
```

Common errors:
- Authentication errors: Invalid or expired access token
- Not found errors: File/shape/page doesn't exist
- Permission errors: User lacks permission for operation
- Rate limit errors: Too many requests
- Validation errors: Invalid input parameters
