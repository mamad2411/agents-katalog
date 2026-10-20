---
name: mcp_server_development
description: Use when building, extending, or debugging MCP (Model Context Protocol) servers for AI agents. Covers FastMCP, tool design, resources, prompts, security, testing, and deployment.
---

# MCP Server Development

## Overview

MCP (Model Context Protocol) is an open protocol by Anthropic for connecting AI agents to data sources, tools, and services. An MCP server exposes capabilities (tools, resources, prompts) that MCP clients (Claude Desktop, Cursor, Cline, etc.) can discover and invoke.

**Core principle:** MCP tools are thin controllers — business logic lives in services. Keep tool functions under 20 lines.

## When to Use

- Building a new MCP server from scratch
- Adding tools/resources/prompts to an existing MCP server
- Choosing between stdio, SSE, or streamable HTTP transport
- Implementing security (auth, sandboxing, validation) for MCP tools
- Testing MCP servers locally or in CI
- Deploying MCP servers to production

## When NOT to Use

- Building a general API (use FastAPI/REST instead)
- When the consumer is not an MCP client
- Simple scripts without structured tool definitions

---

## 1. Project Structure

```
my-mcp-server/
  pyproject.toml
  README.md
  src/
    my_mcp_server/
      __init__.py
      server.py          # FastMCP app instance
      tools.py           # Tool definitions
      resources.py       # Resource templates
      prompts.py         # Prompt templates
      services/          # Business logic
        __init__.py
        search.py
        extract.py
      models/            # Pydantic models
        __init__.py
        schemas.py
      security/          # Sanitization, validation
        __init__.py
        validator.py
```

---

## 2. FastMCP Setup

```python
from fastmcp import FastMCP
from pydantic import BaseModel

app = FastMCP("my-server")

# Register tools
@app.tool(name="search.memories")
async def search_memories(query: str, top_k: int = 10) -> list[dict]:
    """Search memory store for relevant entries."""
    return await search_service.query(query, top_k)

# Register resources
@app.resource("mem://{project}/patterns")
async def get_patterns(project: str) -> str:
    """Get design patterns for a project."""
    patterns = await pattern_service.list(project)
    return "\n\n".join(f"- {p.name}: {p.description}" for p in patterns)

# Register prompts
@app.prompt(name="extract_memory")
def extract_memory_prompt(content: str) -> str:
    return f"""Extract structured memories from the following content:

{content}

Rules:
- One memory per key insight
- Include source, type, and confidence
"""

if __name__ == "__main__":
    app.run(transport="stdio")  # or "sse"
```

---

## 3. Tool Design

### Principles

1. **Single responsibility**: One tool does one thing well
2. **Schema-first**: Use Pydantic models for all inputs/outputs
3. **Descriptive names**: `memory.query` not `mq`
4. **Rich docstrings**: Clients use these as tool descriptions
5. **Graceful degradation**: Return structured errors, not exceptions

### Good Tool Example

```python
from pydantic import BaseModel, Field
from typing import Literal

class QueryResult(BaseModel):
    memory_id: str
    content: str
    relevance: float = Field(ge=0.0, le=1.0)
    source: str

class QueryResponse(BaseModel):
    status: Literal["ok", "degraded", "error"]
    results: list[QueryResult]
    total: int
    message: str | None = None

@app.tool(name="memory.query")
async def memory_query(
    project: str = Field(description="Project namespace"),
    query: str = Field(description="Natural language query"),
    mode: Literal["hybrid", "vector", "graph"] = "hybrid",
    top_k: int = Field(default=10, ge=1, le=100),
) -> QueryResponse:
    """Query project memories using hybrid (vector+graph), vector-only, or graph-only search.
    
    Hybrid mode requires both Qdrant and Neo4j. Falls back to graph-only if vector store
    is unavailable. Returns results sorted by relevance score.
    """
    try:
        results = await search_service.query(project, query, mode, top_k)
        return QueryResponse(status="ok", results=results, total=len(results))
    except VectorStoreUnavailable:
        results = await search_service.graph_only(project, query, top_k)
        return QueryResponse(
            status="degraded",
            results=results,
            total=len(results),
            message="Vector store offline; using graph search only",
        )
```

### Compositional Tools

```python
@app.tool(name="memory.smart_ingest")
async def smart_ingest(content: str, project: str) -> dict:
    """Full pipeline: sanitize → extract → admit → persist.
    Use when ingesting content and wanting automatic quality improvement."""
    sanitized = await security.sanitize(content)
    candidates = await extraction.extract(sanitized, project)
    admitted = await admission.validate(candidates)
    persisted = await persistence.store(admitted)
    return {
        "status": "ok",
        "extracted": len(candidates),
        "admitted": len(admitted),
        "persisted": len(persisted),
    }
```

---

## 4. Security

### Input Validation

```python
from pydantic import BaseModel, validator
import re

class SafeQuery(BaseModel):
    query: str
    
    @validator("query")
    def no_injection(cls, v):
        # Block common prompt injection patterns
        if re.search(r"ignore previous|system prompt|<?xml", v, re.I):
            raise ValueError("Potential injection detected")
        if len(v) > 10000:
            raise ValueError("Query too long")
        return v
```

### Sanitization

```python
import presidio_analyzer
import presidio_anonymizer

class SanitizationService:
    def __init__(self):
        self.analyzer = presidio_analyzer.AnalyzerEngine()
        self.anonymizer = presidio_anonymizer.AnonymizerEngine()
    
    def sanitize(self, text: str) -> str:
        results = self.analyzer.analyze(text=text, language="en")
        return self.anonymizer.anonymize(text=text, analyzer_results=results).text
```

### Permission Model

```python
class PermissionChecker:
    VALID_TOOLS = {
        "memory.query", "memory.upsert", "memory.delete",
        "graph.catalog.read", "graph.catalog.write",
    }
    
    def check(self, tool_name: str, user: User) -> bool:
        if tool_name not in self.VALID_TOOLS:
            return False
        # Additional RBAC checks
        return user.has_permission(tool_name)
```

---

## 5. Testing

### Unit Tests

```python
import pytest
from fastmcp.testing import Client

@pytest.fixture
def client():
    return Client(my_server.app)

@pytest.mark.asyncio
async def test_memory_query(client):
    result = await client.call_tool("memory.query", {
        "project": "test",
        "query": "design patterns",
        "top_k": 5,
    })
    assert result.status == "ok"
    assert len(result.results) <= 5
    assert all(r.relevance >= 0.0 for r in result.results)
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_smart_ingest_pipeline(client):
    result = await client.call_tool("memory.smart_ingest", {
        "content": "We decided to use JWT for auth. Secret is abc123.",
        "project": "test",
    })
    # Secret should be sanitized
    assert "abc123" not in str(result)
    assert result.persisted > 0
```

---

## 6. Deployment

### Local Development

```bash
# stdio transport (for Claude Desktop)
python -m my_mcp_server

# SSE transport (for web clients)
python -m my_mcp_server --transport sse --port 8000
```

### Claude Desktop Config

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install .
COPY src/ ./src/
CMD ["python", "-m", "my_mcp_server"]
```

---

## 7. Transport Comparison

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **stdio** | Claude Desktop, local tools | Simple, no network | Single client, no concurrency |
| **SSE** | Web apps, multi-client | Real-time, HTTP-based | Requires server infrastructure |
| **Streamable HTTP** | Production APIs | Standard HTTP, cacheable | Less real-time than SSE |

---

## 8. Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| God tools | Split into composable, single-purpose tools |
| Missing error handling | Always return structured errors |
| No input validation | Pydantic schemas with constraints |
| Leaking secrets | Sanitize both input and output |
| No timeouts | Set max execution time on all tools |
| Tight coupling | Business logic in services, not tools |

---

## 9. References

- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- knowledge/12_agentic_ai_frontier_2026.md (MCP Ecosystem section)
- skills/29_mcp_advanced_patterns/SKILL.md
