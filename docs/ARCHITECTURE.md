# Penpot MCP Server - Architecture

This document describes the architecture and design decisions of the Penpot MCP Server.

## Overview

The Penpot MCP Server is a Model Context Protocol implementation that enables AI assistants to interact with Penpot design files programmatically. It acts as a bridge between AI language models and the Penpot API.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Assistant                            │
│                  (Claude, GPT-4, etc.)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ MCP Protocol (JSON-RPC)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  Penpot MCP Server                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Tool Registry                            │   │
│  │  • File Operations    • Shape Operations             │   │
│  │  • Design Analysis    • Export Operations            │   │
│  │  • Advanced Tools     • AI Generation                │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │           Penpot API Client                          │   │
│  │  • Authentication    • Rate Limiting                 │   │
│  │  • Caching          • Error Handling                 │   │
│  └──────────────────────┬───────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │ HTTPS/JSON
                          │
┌─────────────────────────▼─────────────────────────────────────┐
│                    Penpot API                                  │
│              (Cloud or Self-Hosted)                            │
└───────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. MCP Server Layer (`server.py`)

**Responsibilities:**
- MCP protocol implementation
- Tool registration and routing
- Request/response handling
- Integration with AI assistants

**Key Features:**
- Implements MCP SDK server interface
- Registers 20+ tools
- Handles JSON-RPC communication
- Manages tool lifecycle

**Code Structure:**
```python
Server
├── list_tools() - Returns available tools
├── call_tool() - Routes tool calls to handlers
└── Tool Handlers - Individual tool implementations
```

### 2. Penpot API Client (`penpot_client.py`)

**Responsibilities:**
- HTTP communication with Penpot API
- Authentication management
- Session handling
- Low-level API operations

**Key Features:**
- Async/await design
- Connection pooling
- Automatic retry logic
- Context manager support

**API Methods:**
```python
PenpotClient
├── File Operations
│   ├── get_file()
│   ├── create_file()
│   ├── update_file()
│   └── delete_file()
├── Page Operations
│   ├── create_page()
│   └── delete_page()
├── Shape Operations
│   ├── add_shape()
│   ├── update_shape()
│   └── delete_shape()
└── Export Operations
    └── export_shapes()
```

### 3. Tool Layer (`tools/`)

**Responsibilities:**
- Business logic implementation
- Data transformation
- Error handling
- Response formatting

**Tool Categories:**

#### File Operations (`file_ops.py`)
- `list_files_tool` - List files in team/project
- `get_file_tool` - Get file details
- `create_file_tool` - Create new file
- `delete_file_tool` - Delete file

#### Design Analysis (`analysis.py`)
- `analyze_design_tool` - Comprehensive design analysis
- `extract_colors_tool` - Color palette extraction
- `extract_typography_tool` - Typography analysis
- `get_components_tool` - Component listing

#### Shape Operations (`shapes.py`)
- `create_rectangle_tool` - Create rectangles
- `create_text_tool` - Create text elements
- `create_frame_tool` - Create frames
- `create_circle_tool` - Create circles
- `update_shape_tool` - Update shapes
- `delete_shape_tool` - Delete shapes

#### Export Operations (`export.py`)
- `export_to_svg_tool` - SVG export
- `export_to_png_tool` - PNG export
- `export_design_tokens_tool` - Design tokens export

#### Advanced Tools (`advanced.py`)
- `generate_design_from_prompt_tool` - AI design generation
- `validate_accessibility_tool` - Accessibility validation
- `compare_designs_tool` - Design comparison

### 4. Utilities Layer (`utils/`)

**Responsibilities:**
- Cross-cutting concerns
- Shared functionality
- Infrastructure services

**Components:**

#### Authentication (`auth.py`)
- Token management
- Header generation
- Credential validation

#### Rate Limiting (`rate_limit.py`)
- Request throttling
- Token bucket algorithm
- Per-window limits

#### Caching (`cache.py`)
- In-memory caching
- TTL management
- Pattern-based invalidation

### 5. Data Models (`models/`)

**Responsibilities:**
- Data validation
- Type safety
- API format conversion

**Models:**

#### Shape Model (`shape.py`)
```python
ShapeModel
├── type: ShapeType enum
├── position: (x, y)
├── size: (width, height)
├── styling: colors, strokes
├── content: text, images
└── to_penpot_format() - API serialization
```

#### File Model (`file.py`)
```python
FileModel
├── metadata: id, name, dates
├── pages: List[PageModel]
└── data: nested design data
```

## Data Flow

### Request Flow Example: Creating a Rectangle

```
1. AI Assistant Request
   "Create a blue rectangle at position 100,100"

2. MCP Server
   ├── Parse request
   ├── Validate parameters
   └── Route to create_rectangle_tool

3. Shape Tool
   ├── Create ShapeModel
   ├── Validate dimensions
   └── Call PenpotClient.add_shape()

4. Penpot Client
   ├── Check rate limit
   ├── Format request
   ├── Make HTTP POST
   └── Handle response

5. Penpot API
   ├── Authenticate
   ├── Validate request
   ├── Create shape
   └── Return shape ID

6. Response Flow (reverse)
   API → Client → Tool → Server → AI
```

## Design Patterns

### 1. Async/Await Pattern

All I/O operations use async/await for non-blocking execution:

```python
async with PenpotClient() as client:
    file = await client.get_file(file_id)
    shapes = await analyze_shapes(file)
```

### 2. Context Manager Pattern

Resource management using context managers:

```python
async def __aenter__(self):
    await self.connect()
    return self

async def __aexit__(self, *args):
    await self.close()
```

### 3. Factory Pattern

Tool creation and registration:

```python
def create_server() -> Server:
    server = Server("penpot-mcp")

    @server.list_tools()
    async def list_tools():
        return [Tool(...), Tool(...)]
```

### 4. Repository Pattern

API client abstracts data access:

```python
class PenpotClient:
    async def get_file(self, file_id: str):
        return await self._call("get-file", {"id": file_id})
```

## Error Handling Strategy

### Exception Hierarchy

```
PenpotMCPError (base)
├── PenpotAPIError - API call failures
├── AuthenticationError - Auth failures
├── ValidationError - Input validation
├── RateLimitError - Rate limit exceeded
├── ResourceNotFoundError - 404 errors
└── PermissionDeniedError - 403 errors
```

### Error Flow

```python
try:
    result = await client.create_file(...)
except AuthenticationError:
    return {"success": False, "error": "Invalid token"}
except RateLimitError:
    return {"success": False, "error": "Too many requests"}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"success": False, "error": str(e)}
```

## Performance Optimizations

### 1. Caching Strategy

- **File metadata**: 5 minute TTL
- **User profile**: 10 minute TTL
- **Design data**: No caching (always fresh)
- **Invalidation**: On write operations

### 2. Rate Limiting

- Default: 100 requests per 60 seconds
- Per-client limits
- Token bucket algorithm
- Configurable via environment

### 3. Connection Pooling

- Single session per client instance
- Automatic connection reuse
- Graceful connection closing

### 4. Parallel Requests

Tools can be called in parallel when independent:

```python
# Sequential
file1 = await get_file("id1")
file2 = await get_file("id2")

# Parallel
file1, file2 = await asyncio.gather(
    get_file("id1"),
    get_file("id2")
)
```

## Security Considerations

### 1. Authentication

- Token-based authentication
- No password storage
- Environment variable injection
- Secure token transmission

### 2. Input Validation

- All inputs validated with Pydantic
- Type checking enforced
- Sanitization of user data
- SQL injection prevention (N/A for REST API)

### 3. Rate Limiting

- Prevents abuse
- Protects Penpot API
- Per-user limits
- Configurable thresholds

### 4. Error Messages

- Generic errors to users
- Detailed logs for debugging
- No sensitive data leakage
- Structured error responses

## Scalability

### Current Limitations

- Single-threaded async execution
- In-memory caching (not distributed)
- Stateful client connections
- No horizontal scaling

### Future Improvements

- Redis for distributed caching
- Load balancer support
- Stateless architecture
- Worker pool for parallel processing

## Testing Strategy

### Unit Tests

- Individual component testing
- Mock external dependencies
- 80%+ code coverage
- Fast execution (<1s)

### Integration Tests

- Real API calls (optional)
- End-to-end workflows
- Authentication testing
- Error scenario validation

### Performance Tests

- Load testing
- Latency measurements
- Memory profiling
- Concurrent request handling

## Deployment Models

### 1. Claude Desktop Integration

```
Claude Desktop
└── Spawns Python process
    └── penpot-mcp server
        └── Communicates via stdio
```

### 2. Standalone Server

```
Terminal
└── python -m penpot_mcp
    └── Runs as long-lived process
```

### 3. Docker Container

```
Docker
└── penpot-mcp:latest
    └── Isolated environment
        └── Production-ready
```

## Configuration Management

### Environment Variables

```
PENPOT_ACCESS_TOKEN    - Required: API authentication
PENPOT_API_URL         - Optional: API endpoint
DEBUG                  - Optional: Debug logging
RATE_LIMIT_REQUESTS    - Optional: Rate limit config
CACHE_TTL_SECONDS      - Optional: Cache duration
CACHE_ENABLED          - Optional: Cache toggle
```

### Configuration Hierarchy

1. Environment variables
2. .env file
3. Default values
4. Runtime overrides

## Monitoring and Logging

### Log Levels

- `DEBUG`: Detailed operation info
- `INFO`: Important events
- `WARNING`: Potential issues
- `ERROR`: Failures and exceptions

### Logged Events

- API calls (endpoint, duration)
- Authentication attempts
- Rate limit hits
- Cache hits/misses
- Errors and exceptions

### Metrics (Future)

- Request count
- Response times
- Error rates
- Cache hit ratio
- Active connections

## Future Architecture Improvements

1. **GraphQL Support**: More efficient queries
2. **WebSocket Support**: Real-time updates
3. **Batch Operations**: Multiple operations in one call
4. **Webhook Integration**: Event-driven updates
5. **Plugin System**: Extensible tool framework
6. **Multi-tenancy**: Support multiple Penpot instances
7. **Offline Mode**: Local caching and sync

---

## References

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Penpot API Documentation](https://help.penpot.app/technical-guide/integration/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
