---
name: MCP Advanced Patterns
description: Use when extending the TheSearch MCP server with compositional tools, resource templates, prompt templates, error handling, multi-tenant isolation, or choosing transport layers.
---

# MCP Advanced Server Patterns

## Overview

TheSearch exposes its memory system via an MCP server built with FastMCP. The server currently provides tools (`memory.query`, `memory.upsert`, `memory.ingest_raw`, graph CRUD), resources (`mem://`, `graph://`), and prompts for extraction. This skill covers advanced patterns for evolving this server.

**Core principle:** MCP tools are thin controllers — delegate to services. Keep tool functions under 20 lines.

## When to Use

- Adding compositional or conditional tools
- Creating dynamic resource templates
- Building prompt templates for guided interactions
- Implementing error handling and graceful degradation
- Designing multi-tenant isolation
- Testing and debugging the MCP server
- Choosing between stdio, SSE, and streamable HTTP

## Current Server Structure

```
server/
  main.py        → FastMCP app, transport config
  tools.py       → register_tools(app, container)
  resources.py   → register_resources(app, container)
  prompts.py     → register_prompts(app, container)
  container.py   → ServiceContainer (DI)
  mcp_compat.py  → FastMCP import shim

services/
  hybrid_search_service.py
  extraction_service.py
  admission_service.py
  persistence_service.py
  ... (26 services)
```

**Tools:** 20+ tools across `memory.*`, `graph.*`, `graph.catalog.*`, `memory.pr.*` namespaces.

**Resources:** `graph://projects`, `mem://project/{project}/top-patterns`, `mem://domain/{domain}/rules`, etc.

## 1. Compositional Tools

Tools that orchestrate multiple service calls in a single MCP invocation:

```python
@app.tool(name="memory.smart_ingest")
async def memory_smart_ingest(
    content: str,
    project: str,
    source_kind: str = "manual",
    reflect_on_failure: bool = True,
) -> dict:
    """Full pipeline: sanitize → extract → reflect if needed → admit → persist.
    Use when ingesting content and wanting automatic quality improvement."""
    try:
        c.sanitization.validate_payload_size(content)
        sanitized = c.sanitization.sanitize(content)
        
        candidates = await c.extraction.extract_candidates(sanitized, project)
        
        if not candidates and reflect_on_failure:
            candidates = await _reflective_retry(c, sanitized, project)
        
        return await _process_candidates(c, candidates)
    except (MemoryServiceError, SanitizationError) as error:
        return _as_error(error)
```

**Rules for compositional tools:**
- Single responsibility: one pipeline, not a god function
- Reuse existing services, don't duplicate logic
- Return structured dict with `status`, `results`, `errors`

### Conditional Tools

Tools that expose different behavior based on server configuration:

```python
@app.tool(name="memory.search")
async def memory_search(
    project: str,
    query: str,
    mode: str = "hybrid",
) -> list[dict]:
    """Search memories. mode: 'hybrid' (vector+graph), 'vector', or 'graph'.
    Hybrid mode requires Qdrant + Neo4j. Falls back to graph-only if Qdrant unavailable."""
    if mode == "hybrid" and c.qdrant.is_available():
        return await c.search.search(query_text=query, project=project, top_k=10)
    if mode == "vector" and c.qdrant.is_available():
        return await c.qdrant.search(query, project=project, top_k=10)
    return await c.neo4j.query_by_project(project, top_k=10)
```

## 2. Resource Templates for Dynamic Data

### Paginated Resources

```python
@app.resource("mem://project/{project}/memories?page={page}&limit={limit}")
async def project_memories_paginated(project: str, page: int = 1, limit: int = 20) -> str:
    offset = (page - 1) * limit
    items = await c.neo4j.query_by_project(project, skip=offset, limit=limit)
    total = await c.neo4j.count_memories(project)
    return json.dumps({
        "items": items,
        "page": page,
        "total_pages": -(-total // limit),
        "total": total,
    })
```

### Filtered Resources

```python
@app.resource("mem://project/{project}/category/{category}/top")
async def category_top(project: str, category: str) -> str:
    items = await c.neo4j.query_by_project(
        project, category=category, limit=10
    )
    return _format_items(items)
```

### Computed Resources

```python
@app.resource("mem://stats/distribution")
async def stats_distribution() -> str:
    return json.dumps(await c.neo4j.category_distribution())
```

## 3. Prompt Templates for Guided Interactions

```python
@app.prompt()
def guided_ingest(task_type: str, project: str) -> str:
    """Interactive prompt for structured memory creation."""
    return f"""You are helping extract durable knowledge for project '{project}'.

Task type: {task_type}

Available categories:
- BusinessRule: domain rules, constraints, validations
- DesignPattern: reusable solutions, architectural patterns
- DesignRule: naming conventions, coding standards
- ArchitecturalDecision: ADRs, technology choices

For each piece of knowledge found, provide:
1. **Title** — concise, technical, descriptive
2. **Category** — one of the above
3. **Summary** — what it is, in 1-2 sentences
4. **Details** — full explanation with context
5. **Evidence** — where this knowledge came from

If no durable knowledge exists, respond with empty list."""

@app.prompt()
def consolidation_review(project: str) -> str:
    """Prompt for reviewing consolidation candidates."""
    return f"""Review these memory consolidation candidates for project '{project}'.

For each pair, decide:
1. MERGE — same knowledge, different wording (keep the more complete one)
2. KEEP_BOTH — related but distinct knowledge
3. DEPRECATE — one supersedes the other

Output format: JSON array of decisions with rationale."""
```

## 4. Error Handling & Graceful Degradation

### Error Taxonomy

```python
class MCPError(BaseModel):
    error: str
    type: str
    recoverable: bool
    suggestion: str

def _as_mcp_error(error: Exception) -> dict:
    if isinstance(error, SanitizationError):
        return MCPError(
            error=str(error),
            type="sanitization",
            recoverable=False,
            suggestion="Remove PII/sensitive data and retry.",
        ).model_dump()
    if isinstance(error, MemoryServiceError):
        return MCPError(
            error=str(error),
            type="service",
            recoverable=True,
            suggestion="Retry the operation. If persistent, check Neo4j/Qdrant connectivity.",
        ).model_dump()
    return MCPError(
        error=str(error),
        type="unknown",
        recoverable=False,
        suggestion="Check server logs for details.",
    ).model_dump()
```

### Fallback Patterns

```python
async def resilient_search(query: str, project: str) -> list[dict]:
    try:
        return await c.search.search(query_text=query, project=project)
    except Exception:
        try:
            return await c.neo4j.query_by_project(project)
        except Exception:
            return [{"error": "All search backends unavailable", "status": "degraded"}]
```

## 5. Multi-Tenant MCP Patterns

### Project Isolation

```python
TENANT_PROJECT_MAP = {
    "tenant-alpha": ["CORE", "ALPHA"],
    "tenant-beta": ["CORE", "BETA"],
}

def require_project_access(tenant: str, project: str) -> bool:
    allowed = TENANT_PROJECT_MAP.get(tenant, [])
    return project in allowed

@app.tool(name="memory.query")
async def memory_query_tenant(
    project: str,
    query_text: str | None = None,
    top_k: int = 10,
    _tenant: str = "",
) -> list[dict] | dict:
    if _tenant and not require_project_access(_tenant, project):
        return {"error": "Access denied", "project": project}
    return await _memory_query_impl(project, query_text, top_k)
```

### Qdrant Multitenancy

```python
# Use payload filtering for tenant isolation in Qdrant
await qdrant.search(
    collection="memories",
    query_vector=embedding,
    query_filter={
        "must": [
            {"key": "project", "match": {"value": project}},
        ]
    },
    limit=top_k,
)
```

### Neo4j Project Scoping

```cypher
-- Always scope queries by project for tenant isolation
MATCH (m:MemoryItem {project: $project, status: 'active'})
-- Never query without project filter in multi-tenant context
```

## 6. Testing & Debugging

### Tool Testing Pattern

```python
import pytest

@pytest.fixture
def container():
    return ServiceContainer(test_mode=True)

async def test_memory_query_returns_results(container):
    result = await container.search.search(
        query_text="design rules", project="CORE", top_k=5
    )
    assert isinstance(result, list)
    if result:
        assert "memory_id" in result[0]
        assert "title" in result[0]

async def test_memory_ingest_raw_pipeline(container):
    result = await tools.memory_ingest_raw(
        source_kind="test",
        payload="Use guard clauses for early returns in all service methods.",
        project_hint="CORE",
    )
    assert result["status"] == "received"
    assert result["candidates_extracted"] >= 0
```

### MCP Inspector Debugging

```bash
# Run MCP server with inspector for live debugging
npx @anthropic/mcp-inspector python -m server.main

# Or use the built-in FastMCP dev mode
fastmcp dev server/main.py
```

### Logging Pattern

```python
import structlog

logger = structlog.get_logger()

@app.tool(name="memory.query")
async def memory_query(project: str, query_text: str | None = None, top_k: int = 10):
    logger.info("memory_query_called", project=project, has_query=query_text is not None, top_k=top_k)
    try:
        results = await c.search.search(query_text=query_text, project=project, top_k=top_k)
        logger.info("memory_query_success", project=project, result_count=len(results))
        return results
    except Exception as e:
        logger.error("memory_query_failed", project=project, error=str(e))
        return _as_error(e)
```

## 7. Transport Layer Selection

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **stdio** | Local CLI, single user, development | Simple, no network, secure | One client only |
| **Streamable HTTP** | Remote server, web clients, multi-user | HTTP-native, SSE streaming, resumable | Needs auth, network exposure |
| **SSE (deprecated)** | Legacy | — | Replaced by Streamable HTTP |

```python
# server/main.py
import os

transport = os.getenv("MCP_TRANSPORT", "stdio")

if transport == "stdio":
    mcp.run(transport="stdio")
elif transport == "http":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=int(os.getenv("MCP_PORT", "8080")))
```

**TheSearch recommendation:** `stdio` for local development, `streamable-http` when serving multiple clients or integrating with web UIs.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Putting business logic in tool functions | Tools are controllers — delegate to services |
| Not returning structured errors | Always return `_as_error(error)` with type and suggestion |
| Using `str` return for tools | Return `dict` or `list[dict]` for structured data |
| Forgetting to add `@app.tool()` decorator | Undecorated functions are invisible to MCP |
| Hardcoding transport in main.py | Use env var for transport flexibility |
| Testing without DI container | Use `ServiceContainer(test_mode=True)` with mocks |
| Not logging tool calls | Use structlog for structured audit logging |
| Returning raw exceptions to client | Sanitize error messages — no stack traces in MCP responses |

## References

- MCP Specification: tools, resources, prompts, transport layers
- FastMCP: `gofastmcp.com` — Python framework for MCP servers
- MCP Python SDK: `github.com/modelcontextprotocol/python-sdk`
- A2A Protocol: agent-to-agent communication for future multi-agent
- Semantic Kernel: enterprise SDK with MCP integration patterns
- OpenAI Agents SDK: tool integration patterns
- Source: `knogdement/03_multi_agent_systems.md`, `knogdement/10_thesearch_related.md`
