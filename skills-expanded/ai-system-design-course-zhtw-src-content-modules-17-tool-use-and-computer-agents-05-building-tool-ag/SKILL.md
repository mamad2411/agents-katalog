---
title: Building Tool-Use Agents
order: 1704
difficulty: L4
description: Building Tool-Use Agents
---

# Building Tool-Use Agents

This chapter covers the practical engineering of tool-use agents: designing tool schemas that LLMs can call reliably, building MCP servers to host those tools, composing tools into workflows, and testing the entire system. These are the patterns that separate a demo from a production deployment.

## Table of Contents

- [Designing Tool Schemas for LLMs](#designing-tool-schemas-for-llms)
- [MCP Server Creation](#mcp-server-creation)
- [Tool Registration and Discovery](#tool-registration-and-discovery)
- [Input Validation and Output Formatting](#input-validation-and-output-formatting)
- [Tool Composition: Chaining Tools](#tool-composition-chaining-tools)
- [Building Custom Agent Skills](#building-custom-agent-skills)
- [Creating Function-Calling Endpoints](#creating-function-calling-endpoints)
- [Testing Tool-Use Agents](#testing-tool-use-agents)
- [Observability for Tool Use](#observability-for-tool-use)
- [Common Mistakes and Anti-Patterns](#common-mistakes-and-anti-patterns)
- [Tool Versioning and Backwards Compatibility](#tool-versioning-and-backwards-compatibility)
- [Interview Questions](#interview-questions)
- [References](#references)

---

## Designing Tool Schemas for LLMs

The tool schema is the contract between the LLM and your system. A well-designed schema reduces hallucinated arguments, prevents misuse, and makes the model's tool selection more reliable.

### Anatomy of a Good Tool Definition

```json
{
  "name": "search_customers",
  "description": "Search for customers by name, email, or account ID. Returns up to 10 matching customer records. Use this when the user asks about a specific customer. Do NOT use this for aggregate queries like 'how many customers do we have'.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search term: customer name, email address, or account ID (e.g., 'john@acme.com' or 'ACC-12345')"
      },
      "limit": {
        "type": "integer",
        "description": "Max results to return (1-10). Default: 5",
        "default": 5,
        "minimum": 1,
        "maximum": 10
      }
    },
    "required": ["query"]
  }
}
```

### Schema Design Rules

**1. Name precisely**: Use `verb_noun` format. `search_customers` not `search` or `customer_tool`.

**2. Describe when NOT to use**: The model needs negative examples. "Do NOT use for aggregate queries" prevents misuse better than only listing valid uses.

**3. Give argument examples**: Include example values in the description string. The model uses these to calibrate its outputs.

**4. Constrain ranges**: Use `minimum`, `maximum`, `enum`, and `pattern` to prevent invalid arguments at the schema level rather than in your handler.

**5. Keep tools atomic**: One tool does one thing. Avoid a `manage_customer` tool that creates, reads, updates, and deletes -- split into four tools.

**6. Use `strict: true`**: Anthropic's strict mode guarantees the model output matches the schema exactly. Always enable it in production.

```
Good Tool Design:                    Bad Tool Design:

+-------------------+                +-------------------+
| search_customers  |                | customer_tool     |
| - query (string)  |                | - action (string) |
| - limit (int 1-10)|                | - data (object)   |
+-------------------+                | - options (any)   |
| create_customer   |                +-------------------+
| - name (string)   |                "action" can be
| - email (string)  |                "search", "create",
+-------------------+                "update", "delete"
| update_customer   |                => model confused,
| - id (string)     |                   schema too loose,
| - fields (object) |                   hard to validate
+-------------------+
```

---

## MCP Server Creation

An MCP server is a standalone process that exposes tools, resources, and prompts to any MCP-compatible client (Claude, GPT, Llama-based agents). You write the server once and any LLM can use it.

### MCP Architecture

```
+------------------+          JSON-RPC           +------------------+
|                  |  ========================>  |                  |
|   MCP Client     |                             |   MCP Server     |
|   (AI App)       |  <========================  |   (Your Code)    |
|                  |                             |                  |
|  - Claude Code   |  Transport:                 |  Exposes:        |
|  - Custom Agent  |  - stdio (local)            |  - Tools         |
|  - IDE Plugin    |  - Streamable HTTP (remote)  |  - Resources     |
|                  |                             |  - Prompts       |
+------------------+                             +------------------+
```

### TypeScript MCP Server

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "customer-service", version: "1.0.0" });

server.tool(
  "search_customers",
  "Search customers by name, email, or ID. Returns up to 10 matches.",
  {
    query: z.string().describe("Search term: name, email, or account ID"),
    limit: z.number().min(1).max(10).default(5).describe("Max results"),
  },
  async ({ query, limit }) => ({
    content: [{ type: "text",
      text: JSON.stringify(await db.customers.search(query, limit), null, 2) }],
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python MCP Server (FastMCP)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("customer-service")

@mcp.tool()
async def search_customers(query: str, limit: int = 5) -> str:
    """Search customers by name, email, or ID. Returns up to 10 matches.
    Args:
        query: Search term - customer name, email, or account ID
        limit: Max results to return (1-10, default 5)
    """
    return json.dumps(await db.customers.search(query, limit), indent=2)
```

Both SDKs follow the same pattern: create a server, register tools with typed schemas, connect a transport. The TypeScript SDK uses Zod for validation; Python uses type hints and docstrings.

### Deployment Modes

| Mode | Transport | Use Case |
|------|-----------|----------|
| Local (stdio) | stdin/stdout pipe | Desktop tools, IDE plugins |
| Remote (Streamable HTTP) | HTTP + SSE | Cloud services, shared servers |
| Hybrid | Both | Develop local, deploy remote |

---

## Tool Registration and Discovery

In production, agents need to discover available tools dynamically rather than hardcoding them.

### Static Registration

Declare MCP servers in a config file (e.g., `claude_desktop_config.json`). Each entry maps a server name to a command, args, and optional env vars. Simple but inflexible -- every server loads on startup regardless of relevance.

### Dynamic Discovery (Tool Search)

Anthropic's Tool Search (2025) solves schema overload. Instead of loading 200 tool schemas into context (which degrades reasoning), the agent sends a lightweight search query and receives only the 3-5 relevant tool schemas. This keeps the context window focused on reasoning rather than parsing unused schemas.

### MCP Discovery Protocol

MCP clients discover capabilities via standard JSON-RPC methods: `tools/list` returns available tools, `resources/list` returns data resources, `prompts/list` returns prompt templates. This enables runtime discovery without hardcoding.

---

## Input Validation and Output Formatting

### Input Validation Layers

```
+---------------------+
|  Schema Validation   |  <-- JSON Schema / Zod / Pydantic
|  (type, range, enum) |      Catches: wrong types, out-of-range
+----------+----------+
           |
           v
+---------------------+
|  Business Validation |  <-- Your handler code
|  (exists, permitted) |      Catches: invalid IDs, unauthorized
+----------+----------+
           |
           v
+---------------------+
|  Execution           |  <-- Actual operation
+---------------------+
```

Always validate at both layers. Schema validation catches malformed input. Business validation catches semantically invalid input.

```python
@mcp.tool()
async def transfer_funds(
    from_account: str,
    to_account: str,
    amount: float
) -> str:
    """Transfer funds between accounts."""
    # Schema already enforced types via type hints

    # Business validation
    if amount <= 0:
        return "Error: Amount must be positive."
    if amount > 10000:
        return "Error: Transfers over $10,000 require manual approval."
    if from_account == to_account:
        return "Error: Cannot transfer to the same account."

    from_acct = await db.accounts.get(from_account)
    if not from_acct:
        return f"Error: Account {from_account} not found."

    # Execute
    result = await db.transfers.execute(from_account, to_account, amount)
    return f"Transferred ${amount:.2f}. Confirmation: {result.id}"
```

### Output Formatting

Return structured data when the model needs to reason about it. Return human-readable text when the result is final.

```python
# Good: structured for further reasoning
return json.dumps({
    "customers": [
        {"id": "ACC-123", "name": "Jane Smith", "email": "jane@acme.com"},
        {"id": "ACC-456", "name": "John Doe", "email": "john@acme.com"}
    ],
    "total_matches": 2,
    "has_more": False
})

# Bad: unstructured blob
return "Found Jane Smith (ACC-123, jane@acme.com) and John Doe (ACC-456, john@acme.com)"
```

---

## Tool Composition: Chaining Tools

Real tasks require multiple tools called in sequence. There are two composition patterns:

### Pattern 1: LLM-Orchestrated Chaining

The LLM decides which tool to call next based on previous results:

```
User: "Find customer Jane Smith and create a high-priority ticket for her billing issue"

Turn 1:  LLM -> search_customers("Jane Smith")
         Result: {"id": "ACC-123", "name": "Jane Smith", ...}

Turn 2:  LLM -> create_ticket("ACC-123", "Billing issue", "...", "high")
         Result: "Ticket TK-789 created."

Turn 3:  LLM -> "I found Jane Smith (ACC-123) and created ticket TK-789."
```

Each tool call is a separate API round-trip. The model reasons about results between calls.

### Pattern 2: Programmatic Tool Calling

Anthropic's programmatic tool calling (2025) lets the model write code that chains tools without round-trips:

```
LLM generates code:
  customer = search_customers("Jane Smith")
  if customer.results:
    ticket = create_ticket(customer.results[0].id, ...)
    return f"Created {ticket.id} for {customer.results[0].name}"
  else:
    return "Customer not found"
```

This executes as a single API call, reducing latency from 3 round-trips to 1.

### Pattern 3: Server-Side Composition

Compose tools inside the MCP server itself -- a single `resolve_customer_issue` tool internally calls search and create_ticket, hiding the multi-step logic from the LLM. Use this for fixed, well-defined workflows where the LLM does not need to reason between steps.

### When to Use Each

| Pattern | Latency | Flexibility | Best For |
|---------|---------|-------------|----------|
| LLM-orchestrated | High (N round-trips) | Very high | Complex, branching logic |
| Programmatic | Low (1 round-trip) | High | Linear chains, batches |
| Server-side | Lowest | Low | Fixed, common workflows |

---

## Building Custom Agent Skills

Agent Skills (Anthropic, 2025) are bundled sets of instructions, tools, and resources that an agent loads dynamically. A skill is a folder:

```
my-skill/
  SKILL.md          # Instructions the agent loads into system prompt
  tools/            # MCP tool implementations
  resources/        # Data files, templates, schemas
  tests/            # Evaluation cases
```

At runtime, a SkillManager registers available skills and activates them on demand -- injecting the skill's instructions into the system prompt and adding its tools to the available tool set. This keeps the base agent lightweight while enabling deep specialization.

---

## Creating Function-Calling Endpoints

To make your API callable by any LLM, expose it via FastAPI with Pydantic models. The auto-generated OpenAPI spec (`/openapi.json`) doubles as a tool schema for function calling. Alternatively, wrap the same logic in an MCP server for direct integration with Claude, GPT, or other MCP-compatible clients.

---

## Testing Tool-Use Agents

### Three Testing Layers

```
+---------------------------+
|   Eval Suites             |  End-to-end: does the agent
|   (Agent + LLM + Tools)  |  complete the task?
+-------------+-------------+
              |
+-------------v-------------+
|   Integration Tests       |  Does tool X work correctly
|   (Tool + Dependencies)   |  with real DB / API?
+-------------+-------------+
              |
+-------------v-------------+
|   Unit Tests              |  Does validation logic
|   (Tool Logic Only)       |  handle edge cases?
+---------------------------+
```

### Unit Tests for Tools

Test each tool handler in isolation with mocked dependencies. Cover: input validation edge cases (out-of-range values, missing fields), error message quality (does it guide the model to recover?), and output format (valid JSON, correct schema).

### Eval Suites for Agent Behavior

Build a dataset of 100+ realistic queries with expected outcomes:

```python
eval_cases = [
    {
        "input": "Find Jane Smith's account and check her last payment",
        "expected_tools": ["search_customers", "get_payment_history"],
        "max_tool_calls": 5,
    },
    {
        "input": "What is the meaning of life?",
        "expected_tools": [],  # Should NOT call any tools
        "max_tool_calls": 0,
    },
]
```

For each case, measure: tool selection accuracy (right tool?), argument quality (correct args?), task completion rate, and efficiency (number of tool calls). Run evals on every model version change and every tool schema change.

---

## Observability for Tool Use

Every tool call should log: trace/span IDs, timestamp, tool name, input args, output size, latency, status, model used, token usage, and session ID.

### Key Metrics

| Metric | What It Measures | Alert Threshold |
|--------|-----------------|-----------------|
| Tool call success rate | % of calls returning valid results | < 95% |
| Tool selection accuracy | Was the right tool chosen? | < 90% |
| Avg tool calls per task | Efficiency of tool use | > 2x baseline |
| Latency per tool call | Response time of tool handlers | > 5s (p99) |
| Hallucinated arguments | Invalid args despite schema | > 2% |
| Cost per task | Total LLM + tool execution cost | > budget |

### Tracing Architecture

```
+-------------+     +----------------+     +--------------+
|  Agent      |---->|  Tool Handler  |---->|  Backend     |
|  (LLM call) |     |  (MCP Server)  |     |  (DB/API)    |
+------+------+     +--------+-------+     +------+-------+
       |                     |                     |
       v                     v                     v
+------+---------------------+---------------------+------+
|                    Trace Collector                       |
|              (OpenTelemetry / Langfuse)                  |
+---------------------------+------------------------------+
                            |
                            v
                   +--------+--------+
                   |   Dashboard     |
                   |   - Success %   |
                   |   - Latency     |
                   |   - Cost        |
                   +-----------------+
```

---

## Common Mistakes and Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Tool overload | 50+ tools degrades selection accuracy | Dynamic discovery, load 5-10 per turn |
| Vague descriptions | "Handles customer operations" -- too vague | Include when to use, when NOT to use, examples |
| God tools | One tool with `action` param does everything | Split into atomic tools, one operation each |
| Missing error context | Tool returns "Error" with no details | Actionable messages: "ACC-999 not found. Use search_customers..." |
| Unstructured output | Tool returns prose the model must parse | Return JSON for structured reasoning |
| No idempotency | `create_ticket` called twice creates duplicates | Accept idempotency key, check before creating |
| Exposing internal IDs | Tool requires database UUIDs model cannot know | Accept human-readable identifiers, resolve internally |
| Ignoring rate limits | Agent loops 100 API calls, gets throttled | Backoff in handlers, return "retry in X seconds" |

---

## Tool Versioning and Backwards Compatibility

As tools evolve, you must maintain compatibility with agents that depend on them.

**Rules:**
1. **Additive changes** (new optional params): No version bump needed. Old calls still work.
2. **Breaking changes** (rename, remove param, change semantics): Create a new tool name with the new schema. Keep the old tool running and add "DEPRECATED: Use new_tool instead" to its description. Log every deprecated call for monitoring.
3. **Never remove a tool** until you verify no active agents depend on it.

---

## Interview Questions

### Q: You need to give an LLM agent access to 200 internal tools. How do you handle schema overload?

**Strong answer:**
I would not load all 200 tool schemas into the context. Instead, I would implement a two-phase approach. First, a tool discovery phase where the agent describes what it needs to do, and a lightweight search (embedding similarity or keyword match) returns the 5-10 most relevant tool schemas. Second, a tool execution phase where only the selected tools are included in the context for the actual LLM call.

This mirrors Anthropic's Tool Search pattern. The discovery step can be a separate, cheaper LLM call or even a non-LLM search. The key insight is that context window space used by irrelevant tool schemas directly reduces the model's reasoning quality. I would measure tool selection accuracy as a key metric -- if the agent calls `search_customers` when it should call `get_customer_by_id`, the discovery phase needs tuning.

For the MCP implementation, I would group tools into domain-specific servers (customer-service, billing, analytics) and only connect to the servers relevant to the current conversation.

### Q: Design a testing strategy for a tool-use agent that handles customer support.

**Strong answer:**
I would test at three layers. First, unit tests for each tool handler: validate input edge cases, error messages, and output format. These run in CI on every commit with mocked dependencies.

Second, integration tests that verify tools work against real (staging) databases. For example, `create_ticket` actually creates a record and `search_customers` returns it. These catch schema drift between the tool and the backend.

Third, eval suites that test the full agent -- LLM plus tools. I would build a dataset of 100+ realistic customer queries with expected tool call sequences and output criteria. The eval measures tool selection accuracy (did it pick the right tool?), argument quality (were the arguments correct?), task completion rate (did it solve the problem?), and efficiency (how many tool calls did it take?).

I would run evals on every model version change and every tool schema change. A 2% drop in tool selection accuracy after a schema change means the description needs revision, not the model.

---

## References

- Anthropic. "Tool Use with Claude" API Documentation (2025)
- Model Context Protocol. "Build an MCP Server" (2025)
- MCP TypeScript SDK: github.com/modelcontextprotocol/typescript-sdk
- MCP Python SDK: github.com/modelcontextprotocol/python-sdk
- Anthropic. "Introducing Advanced Tool Use" (2025)
- Anthropic. "Agent Skills" Beta Documentation (2025)

---

*Previous: [Computer-Use Agents](04-computer-use-agents.md)*
