# Penpot MCP Examples

This directory contains example scripts demonstrating various features of the Penpot MCP server.

## Setup

1. Install the package:
```bash
pip install -e ..
```

2. Set your Penpot access token:
```bash
export PENPOT_ACCESS_TOKEN="your_token_here"
```

Get your token from: https://design.penpot.app → Settings → Access Tokens

## Examples

### Example 1: Basic Operations
`example_1_basic.py` - Basic file operations and shape creation
- Connect to Penpot API
- Create a new file
- Add shapes (rectangle, text, circle)
- Retrieve file information

```bash
python example_1_basic.py
```

### Example 2: Design Analysis
`example_2_analysis.py` - Analyze existing designs
- Comprehensive design analysis
- Extract color palette
- Extract typography styles
- Get component information

```bash
python example_2_analysis.py
```

### Example 3: AI Generation
`example_3_ai_generation.py` - AI-powered design generation
- Generate designs from natural language
- Create login forms, buttons, etc.
- Validate accessibility

```bash
python example_3_ai_generation.py
```

## MCP Usage

These examples show how to use the Penpot client directly. When using the MCP server with Claude or other AI assistants, the AI will call these functions automatically based on natural language requests.

For example, you can say:
- "Create a new design file called 'Landing Page'"
- "Analyze the colors in file xyz-123"
- "Generate a login form with blue styling"
- "Check if my design meets accessibility standards"

The AI will use the appropriate MCP tools to fulfill your requests.
