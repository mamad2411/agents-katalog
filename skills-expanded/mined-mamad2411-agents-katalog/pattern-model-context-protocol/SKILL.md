---
name: pattern-model-context-protocol
description: Standardize external capabilities via the Model Context Protocol (FastMCP), separating tool provider runtimes from agent host clients.
metadata:
  category: agent-architecture
  tier: advanced
  chapter: 10
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Model Context Protocol (MCP) Pattern

## 1. Overview & Intent

Standardize external capabilities via the Model Context Protocol (FastMCP), separating tool provider runtimes from agent host clients.

> **Intent & Scope:** Use when connecting agents to external databases, filesystems, APIs, or developer utilities across language and process boundaries.

---

## 2. Architectural Blueprint

```
[Agent Host / Client] <---(JSON-RPC over stdio / SSE)---> [FastMCP Server]
       |                                                         |
  (List Tools)                                             (Registered Tools)
  (Call Tool)                                              (Resources & Prompts)
```

---

## 3. Core Implementation Principles

- Standardize on official MCP specifications for cross-language compatibility.\n- Keep server implementations lightweight using FastMCP or standard SDKs.\n- Use stdio transport for local sidecars and SSE/HTTP for remote microservices.\n- Expose tools with precise type annotations, docstrings, and clean error schemas.

---

## 4. Reference Implementation Pattern

```python
from fastmcp import FastMCP

mcp = FastMCP("DataService")

@mcp.tool()
def query_record(record_id: str) -> dict:
    """Fetch record attributes by unique identifier."""
    return {"id": record_id, "status": "active", "tier": "enterprise"}

if __name__ == "__main__":
    mcp.run()

```

---

## 5. Verification & Failure Modes

- **Verification Checklist:**
  - [ ] Inputs are validated via strict typed schemas before processing.
  - [ ] Error cascades and timeouts are bounded.
  - [ ] Intermediate artifacts and trace telemetry are logged.
  - [ ] Verification criteria are objectively evaluated before task completion.

- **Common Failure Modes:**
  - **Cascading Hallucination:** Unchecked intermediate model drift polluting downstream stages.
  - **Infinite Looping:** Lack of maximum iteration guards or convergence detection.
  - **Context Bloat:** Carrying unpruned conversational history or verbose tool errors across turns.
