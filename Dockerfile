# Multi-stage Dockerfile for Penpot MCP Server

FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install build && \
    pip install .

# Copy source code
COPY src/ ./src/

# Install the package
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1000 penpot && \
    chown -R penpot:penpot /app

USER penpot

# Expose port (if running as HTTP server in future)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from penpot_mcp import __version__; print(__version__)" || exit 1

# Run the MCP server
ENTRYPOINT ["python", "-m", "penpot_mcp"]

# Development stage
FROM base as development

USER root

# Install development dependencies
COPY --chown=penpot:penpot . .
RUN pip install -e ".[dev]"

USER penpot

# Run tests by default in dev
CMD ["pytest", "-v"]
