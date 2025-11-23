# Installation Guide

This guide covers different ways to install and use the Penpot MCP server.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Your Penpot Access Token](#getting-your-penpot-access-token)
3. [Installation Methods](#installation-methods)
4. [Claude Desktop Integration](#claude-desktop-integration)
5. [Cursor IDE Integration](#cursor-ide-integration)
6. [Standalone Usage](#standalone-usage)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.12 or higher
- A Penpot account (either on https://design.penpot.app or self-hosted)
- Penpot access token

---

## Getting Your Penpot Access Token

1. Go to https://design.penpot.app (or your self-hosted instance)
2. Login to your account
3. Click on your profile icon (top-right)
4. Go to **Settings** → **Access Tokens**
5. Click **Create New Token**
6. Give it a name (e.g., "MCP Server")
7. Copy the token (you won't be able to see it again!)

---

## Installation Methods

### Method 1: Install from PyPI (Recommended)

Once published:

```bash
pip install penpot-mcp
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/your-org/penpot-mcp.git
cd penpot-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Method 3: Install for Development

```bash
# Clone and install with dev dependencies
git clone https://github.com/your-org/penpot-mcp.git
cd penpot-mcp
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Run code formatting
black src/
ruff check src/
```

---

## Claude Desktop Integration

### macOS

1. Install penpot-mcp:
   ```bash
   pip install penpot-mcp
   ```

2. Locate your Claude Desktop config:
   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

3. Add the Penpot server:
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

4. Restart Claude Desktop

### Windows

1. Install penpot-mcp:
   ```cmd
   pip install penpot-mcp
   ```

2. Locate your Claude Desktop config:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

3. Add the Penpot server (same as macOS)

4. Restart Claude Desktop

### Linux

1. Install penpot-mcp:
   ```bash
   pip install penpot-mcp
   ```

2. Locate your Claude Desktop config:
   ```bash
   ~/.config/Claude/claude_desktop_config.json
   ```

3. Add the Penpot server (same as macOS)

4. Restart Claude Desktop

---

## Cursor IDE Integration

1. Install penpot-mcp:
   ```bash
   pip install penpot-mcp
   ```

2. Open Cursor settings (⌘+, or Ctrl+,)

3. Search for "MCP" in settings

4. Add to your MCP configuration:
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

5. Restart Cursor

---

## Standalone Usage

You can also use the Penpot client directly in your Python code:

```python
import asyncio
from penpot_mcp import PenpotClient

async def main():
    async with PenpotClient(access_token="your_token") as client:
        # List files
        files = await client.list_files(team_id="team-uuid")

        # Get file data
        file_data = await client.get_file("file-uuid")

        # Create shapes
        await client.add_shape(
            file_id="file-uuid",
            page_id="page-uuid",
            shape_data={
                "type": "rect",
                "x": 100,
                "y": 100,
                "width": 200,
                "height": 100,
                "fill-color": "#3B82F6"
            }
        )

asyncio.run(main())
```

---

## Configuration Options

### Environment Variables

Create a `.env` file in your project:

```env
# Required
PENPOT_ACCESS_TOKEN=your_token_here

# Optional
PENPOT_API_URL=https://design.penpot.app/api
DEBUG=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
CACHE_TTL_SECONDS=300
CACHE_ENABLED=true
```

### Self-Hosted Penpot

If you're using a self-hosted Penpot instance:

```env
PENPOT_API_URL=https://your-penpot-instance.com/api
PENPOT_ACCESS_TOKEN=your_token
```

---

## Verification

### Test the Installation

```bash
# In Python
python -c "from penpot_mcp import PenpotClient; print('✓ Penpot MCP installed successfully')"
```

### Test in Claude Desktop

After configuration, ask Claude:
```
"Can you list my Penpot files?"
```

If configured correctly, Claude will use the Penpot MCP server to list your files.

---

## Troubleshooting

### Issue: "Module not found: penpot_mcp"

**Solution:** Make sure you've installed the package:
```bash
pip install penpot-mcp
# or
pip install -e .  # if installing from source
```

### Issue: "Authentication failed"

**Solution:**
1. Check your access token is correct
2. Make sure the token hasn't expired
3. Verify you have the right permissions
4. For self-hosted, check the API URL is correct

### Issue: Claude Desktop not showing Penpot tools

**Solution:**
1. Verify the config file path is correct
2. Check JSON syntax is valid
3. Make sure you restarted Claude Desktop
4. Check Claude Desktop logs for errors

### Issue: "Rate limit exceeded"

**Solution:**
1. Wait for the rate limit window to reset
2. Increase rate limits in environment variables:
   ```env
   RATE_LIMIT_REQUESTS=200
   RATE_LIMIT_WINDOW=60
   ```

### Issue: Self-hosted Penpot connection fails

**Solution:**
1. Verify the API URL includes `/api` suffix
2. Check SSL certificate is valid
3. Ensure network access to your instance
4. Verify API is accessible from your machine

### Getting Help

- 📖 [Documentation](../README.md)
- 🐛 [Issue Tracker](https://github.com/your-org/penpot-mcp/issues)
- 💬 [Discussions](https://github.com/your-org/penpot-mcp/discussions)

---

## Next Steps

- Read the [API Reference](API.md)
- Try the [Examples](../examples/)
- Check out the [Developer Guide](DEVELOPMENT.md)
