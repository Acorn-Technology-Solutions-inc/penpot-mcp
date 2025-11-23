# Contributing to Penpot MCP Server

Thank you for your interest in contributing to the Penpot MCP Server! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Code Style](#code-style)
7. [Submitting Changes](#submitting-changes)
8. [Reporting Bugs](#reporting-bugs)
9. [Feature Requests](#feature-requests)

---

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/penpot-mcp.git
   cd penpot-mcp
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-org/penpot-mcp.git
   ```

---

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Penpot access token
   ```

4. **Verify setup**:
   ```bash
   pytest
   ```

---

## Making Changes

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

   Commit message format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=penpot_mcp

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for common setup
- Aim for high test coverage (>80%)

Example:
```python
import pytest
from penpot_mcp.penpot_client import PenpotClient

@pytest.mark.asyncio
async def test_create_file():
    client = PenpotClient(access_token="test_token")
    # Test implementation
```

---

## Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all public functions

### Formatting

```bash
# Format code with Black
black src/

# Check with Ruff
ruff check src/

# Type checking with mypy
mypy src/
```

### Documentation Style

- Use Google-style docstrings
- Include parameter types and return types
- Add examples for complex functions

Example:
```python
async def create_file(self, project_id: str, name: str) -> Dict[str, Any]:
    """
    Create a new Penpot file.

    Args:
        project_id: Project UUID where file will be created.
        name: File name.

    Returns:
        Created file object with id.

    Raises:
        PenpotAPIError: If API call fails.

    Example:
        >>> async with PenpotClient() as client:
        ...     file = await client.create_file("proj-123", "My Design")
        ...     print(file["id"])
    """
```

---

## Submitting Changes

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**:
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template with:
     - Description of changes
     - Related issue number (if applicable)
     - Testing performed
     - Screenshots (if applicable)

3. **Address review feedback**:
   - Respond to comments
   - Make requested changes
   - Push updates to your branch

4. **Wait for approval**:
   - At least one maintainer approval required
   - All tests must pass
   - Code review feedback must be addressed

---

## Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported
2. Verify it's actually a bug
3. Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Do this
2. Then do this
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g., macOS 14.0]
- Python version: [e.g., 3.12]
- Package version: [e.g., 1.0.0]
- Penpot instance: [Cloud/Self-hosted]

**Additional context**
Any other relevant information.
```

---

## Feature Requests

### Before Requesting

1. Check if the feature has been requested
2. Consider if it aligns with project goals
3. Think about implementation approach

### Feature Request Template

```markdown
**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
How would you like it to work?

**Alternatives Considered**
What other approaches did you consider?

**Additional Context**
Any other relevant information.
```

---

## Development Guidelines

### Adding New Tools

1. Create tool function in appropriate file under `src/penpot_mcp/tools/`
2. Add tool to server in `src/penpot_mcp/server.py`
3. Write tests in `tests/`
4. Update API documentation in `docs/API.md`
5. Add example usage in `examples/`

### Modifying API Client

1. Update `PenpotClient` in `src/penpot_mcp/penpot_client.py`
2. Update data models if needed
3. Add/update tests
4. Update documentation

### Documentation Changes

- Update relevant `.md` files
- Keep code examples up to date
- Update API reference for tool changes
- Add examples for new features

---

## Questions?

- 💬 [Open a discussion](https://github.com/your-org/penpot-mcp/discussions)
- 📧 Email: maintainers@example.com
- 🐛 [Report an issue](https://github.com/your-org/penpot-mcp/issues)

Thank you for contributing! 🎉
