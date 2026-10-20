---
name: "advanced-tool-use"
description: "Master advanced tool use patterns including chaining, parallel calls, and error recovery for complex Claude Code workflows"
---

# Advanced Tool Use

## When to activate
User wants to optimize tool use patterns in Claude API applications, reduce tokens from tool definitions or call overhead, improve accuracy on complex tool parameters, or build sophisticated tool-calling workflows.

## When NOT to use
- Simple single-tool workflows where overhead optimization is irrelevant
- Applications using the standard Messages API with fewer than 5 tools and no repeated calls
- Debugging a broken tool definition — fix correctness first, then optimize

## Instructions

### Pattern 1: Programmatic Tool Calling (PTC)
Claude writes Python orchestration code instead of calling tools one-at-a-time. Reduces round trips and tokens.

**Token reduction: ~37% for multi-tool workflows.**

Enable per tool:
```python
{
    "name": "read_file",
    "description": "Read a file",
    "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
    "allowed_callers": ["code_execution_20250825"],
}
```

When enabled, Claude may choose to write a Python loop calling this tool N times instead of making N separate tool_use blocks. Use for: repetitive read/lookup patterns, data transformation pipelines, any tool called >3 times per turn.

Do not enable for tools with side effects (write, delete, deploy) or tools requiring per-call authorization.

---

### Pattern 2: Dynamic Filtering for Web Tools
New built-in tool types for web search and fetch that filter results before they enter context.

**Beta header required:** `anthropic-beta: code-execution-web-tools-2026-02-09`

**Token reduction: ~24% fewer input tokens. Accuracy improvement: +13–16 percentage points.**

```python
import anthropic

client = anthropic.Anthropic(default_headers={"anthropic-beta": "code-execution-web-tools-2026-02-09"})

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2048,
    tools=[
        {"type": "web_search_20260209", "name": "web_search"},
        {"type": "web_fetch_20260209", "name": "web_fetch"},
    ],
    messages=[{"role": "user", "content": "What is the current price of NVDA stock?"}],
)
```

With these tool types, Claude writes filtering code that extracts only the relevant data from search results or fetched pages before the content enters the context window. A full web page that is 50,000 tokens becomes a 200-token extract.

---

### Pattern 3: Tool Search / Deferred Loading
For large tool catalogs, defer infrequently-used tools so they are not loaded into context unless needed.

**Token reduction: ~85% for catalogs with many tools.**

Enable via environment variable:
```
ENABLE_TOOL_SEARCH=auto:N
```
Where N is the threshold — tools beyond the top N most relevant are deferred.

Mark individual tools as deferrable:
```python
{
    "name": "advanced_analytics",
    "description": "Run complex analytics queries",
    "input_schema": {...},
    "defer_loading": True,  # Only load when Claude needs this tool
}
```

Deferred tools are discovered by Claude on-demand via MCPSearch when it determines it needs a capability that is not in the current loaded context. Use for: large MCP tool catalogs, enterprise APIs with hundreds of endpoints, plugin systems where most tools are rarely used.

Do not defer tools that are called in almost every conversation — the discovery overhead eliminates the savings.

---

### Pattern 4: Tool Use Examples (`input_examples`)
Add concrete call examples to tool definitions beyond the JSON schema.

**Accuracy improvement: ~72% → ~90% on complex parameters.**

```python
{
    "name": "query_database",
    "description": "Run a SQL query against the analytics database",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "SQL query to execute"},
            "timeout_seconds": {"type": "integer", "description": "Max execution time"},
            "read_only": {"type": "boolean", "description": "Enforce read-only mode"},
        },
        "required": ["query"],
    },
    "input_examples": [
        {
            "query": "SELECT user_id, count(*) as orders FROM orders WHERE created_at > NOW() - INTERVAL '7 days' GROUP BY user_id ORDER BY orders DESC LIMIT 10",
            "timeout_seconds": 30,
            "read_only": True,
        },
        {
            "query": "SELECT AVG(order_value) FROM orders WHERE status = 'completed'",
            "read_only": True,
        },
    ],
}
```

`input_examples` is most valuable for:
- Tools with non-obvious parameter combinations
- Complex nested schemas
- Parameters where the format matters more than the type (SQL strings, regex, JSON paths)
- Tools where Claude consistently makes the same parameter mistake without examples

---

### Combining Patterns

Maximum efficiency stack for a large tool catalog:

```python
tools = [
    # Frequently used tools — loaded always, PTC enabled, with examples
    {
        "name": "read_file",
        "allowed_callers": ["code_execution_20250825"],
        "input_examples": [{"path": "/src/api/users.ts"}],
        ...
    },
    # Infrequently used tools — deferred
    {
        "name": "run_migration",
        "defer_loading": True,
        ...
    },
    # Last frequent tool — cache everything up to here
    {
        "name": "list_files",
        "cache_control": {"type": "ephemeral"},
        ...
    },
]
```

Use web tool types when web search/fetch is in scope:
```python
tools += [
    {"type": "web_search_20260209", "name": "web_search"},
    {"type": "web_fetch_20260209", "name": "web_fetch"},
]
```

## Example

An agent with 120 tools (full API surface of a SaaS platform):

Without optimization: 120 tool definitions × ~150 tokens each = ~18,000 tokens per call, just for tool definitions. Most tools are never called.

With deferred loading (`ENABLE_TOOL_SEARCH=auto:10`): only the 10 most likely tools are loaded. Token cost for tool definitions drops from 18,000 to ~1,500 — 85% reduction. When Claude needs a rarely-used tool, it searches and loads it on demand, adding ~200 tokens for that turn only.

Adding `input_examples` to the 10 always-loaded tools raises parameter accuracy from 72% to 90% on the tools that matter most.

---
