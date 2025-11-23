# Penpot MCP Server

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-ready Model Context Protocol (MCP) server that enables AI assistants (Claude, GPT-4, etc.) to interact with Penpot design files programmatically.

## Features

✨ **15+ MCP Tools** - Comprehensive API for design operations
🎨 **Design Analysis** - AI-powered analysis of colors, typography, and layouts
🔄 **CRUD Operations** - Create, read, update, and delete design elements
📤 **Export Support** - Export to SVG, PNG, and design tokens
🤖 **AI Integration** - Natural language design generation
🔒 **Secure** - Built-in rate limiting and authentication
☁️ **Multi-Instance** - Supports both Penpot Cloud and self-hosted instances

## Quick Start

### Installation

```bash
pip install penpot-mcp
```

### Configuration

1. Create a `.env` file:

```bash
cp .env.example .env
```

2. Add your Penpot access token:

```env
PENPOT_API_URL=https://design.penpot.app/api
PENPOT_ACCESS_TOKEN=your_token_here
```

To get an access token:
1. Go to https://design.penpot.app
2. Login to your account
3. Go to Settings > Access Tokens
4. Create a new token

### Usage with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "penpot": {
      "command": "python",
      "args": ["-m", "penpot_mcp"],
      "env": {
        "PENPOT_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Usage with Cursor

Add to your Cursor MCP configuration:

```json
{
  "penpot": {
    "command": "python",
    "args": ["-m", "penpot_mcp"],
    "env": {
      "PENPOT_API_URL": "https://design.penpot.app/api",
      "PENPOT_ACCESS_TOKEN": "your_token_here"
    }
  }
}
```

## Available Tools

### File Operations
- `list_files` - List all design files in a team/project
- `get_file` - Get complete file data with all pages and shapes
- `create_file` - Create a new design file
- `delete_file` - Delete a file

### Design Analysis
- `analyze_design` - AI-powered comprehensive design analysis
- `extract_colors` - Extract color palette with usage statistics
- `extract_typography` - Extract all text styles and fonts
- `get_components` - List all components and instances

### Shape Operations
- `create_rectangle` - Create rectangle shapes
- `create_text` - Create text elements
- `create_frame` - Create container frames
- `update_shape` - Update shape properties
- `delete_shape` - Delete shapes

### Export Operations
- `export_to_svg` - Export designs to SVG format
- `export_to_png` - Export designs to PNG format
- `export_design_tokens` - Export design tokens as JSON

### Advanced Features
- `generate_design_from_prompt` - AI-powered design generation
- `validate_accessibility` - Check accessibility compliance
- `compare_designs` - Compare two design files

## Examples

### Example 1: Create a Simple Design

```python
# The AI assistant can now:
# "Create a new design file called 'Landing Page' in my project"
# "Add a blue rectangle at position 100,100 with size 200x100"
# "Add text that says 'Welcome' at the top"
```

### Example 2: Analyze a Design

```python
# "Analyze the design in file xyz-123 and tell me about the colors used"
# "Extract all typography styles from my design"
# "Check if my design meets accessibility standards"
```

### Example 3: Export Design

```python
# "Export the first page of file xyz-123 as SVG"
# "Export design tokens from my design system file"
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/your-org/penpot-mcp.git
cd penpot-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=penpot_mcp  # With coverage
```

### Code Quality

```bash
black src/
ruff check src/
mypy src/
```

## Architecture

```
penpot-mcp/
├── src/penpot_mcp/
│   ├── server.py              # Main MCP server
│   ├── penpot_client.py       # Penpot API client
│   ├── tools/                 # MCP tool implementations
│   │   ├── file_ops.py
│   │   ├── analysis.py
│   │   ├── shapes.py
│   │   └── export.py
│   ├── models/                # Data models
│   │   ├── file.py
│   │   └── shape.py
│   └── utils/                 # Utilities
│       ├── auth.py
│       ├── rate_limit.py
│       └── cache.py
├── tests/
└── examples/
```

## API Reference

See [docs/API.md](docs/API.md) for detailed API documentation.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/your-org/penpot-mcp/issues)
- 💬 [Discussions](https://github.com/your-org/penpot-mcp/discussions)

## Acknowledgments

- [Penpot](https://penpot.app) - Open-source design platform
- [Anthropic MCP](https://modelcontextprotocol.io) - Model Context Protocol
- [Anthropic](https://anthropic.com) - Claude AI assistant

## Related Projects

- [Penpot](https://github.com/penpot/penpot) - The design platform
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Official MCP servers
