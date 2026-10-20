# LangChain Agent Architectures and Tools

## Summary

**One-sentence:** Picks among the three LangChain/LangGraph agent architectures — ReAct (reason+act loop), Plan-and-Execute (upfront plan + step execution), and LATS (tree search with backtracking) — and wires tools with error handlers, max_iterations caps, output truncation, and LangSmith tracing for production reliability.

**One-paragraph:** Implement tool-using agents with LangChain and LangGraph. Three architectures: ReAct (reason + act in a loop), Plan-and-Execute (plan upfront, then execute), and LATS (tree search for complex reasoning). Master tool definition, error handling, state management. ReAct is the simplest and most debuggable; Plan-and-Execute reduces error propagation on multi-step tasks; LATS adds backtracking when the solution path is uncertain. All three need max_iterations caps, tool error handlers, output truncation, and LangSmith tracing in production.

**Ефективно для:** будь-яких tool-using агентів, де потрібен повторюваний, спостережуваний паттерн з вибором архітектури під конкретну задачу.

## Applies If (ALL must hold)

- Building a tool-using agent with verifiable step-by-step reasoning.
- LangChain/LangGraph is the chosen framework.
- Tools have clear input schemas and error semantics.

## Skip If (ANY kills it)

- Single-tool, single-step retrieval — plain LLM call suffices.
- Hard latency &lt; 1s — ReAct + LATS add round-trips.
- Solution path is already known — use a deterministic pipeline.
- Tool schemas cannot be written (undocumented APIs).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool inventory | List of `@tool`-decorated callables with docstrings | Application code |
| State schema | TypedDict for LangGraph state machines | Application code |
| LangSmith config | env vars or config file | Observability stack |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `idempotent-write-tools` | LangGraph retries must be safe; use idempotency keys. |
| `headless-cli-four-guards` | Agent CLIs need the four guards in production. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Six rules: cap max_iterations, handle_tool_error=True, validate plan, truncate outputs, structured supervisor, LangSmith mandatory | ~1100 |
| `content/02-output-contract.xml` | essential | Tool docstring contract + state schema + supervisor decision | ~1100 |
| `content/03-failure-modes.xml` | essential | Tool hallucination, plan staleness, LATS cost, context bloat | ~900 |
| `content/04-procedure.xml` | recommended | Architecture-pick → tools → graph → tracing | ~1000 |
| `content/05-examples.xml` | recommended | ReAct, Plan-and-Execute, LATS worked examples | ~900 |
| `content/06-decision-tree.xml` | essential | ReAct vs P&amp;E vs LATS by task shape | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Build ReAct agent | sonnet | Standard implementation |
| Design Plan-and-Execute state graph | opus | State design + re-plan logic |
| Author tool docstrings | sonnet | Docstrings are agent-facing prompts |
| LATS scoring | haiku | Constrained scoring task |

## Templates

| File | Purpose |
|------|---------|
| `templates/react-agent.py` | Minimal ReAct agent with `create_react_agent`, tools, error handling |
| `templates/_smoke-test.json` | Minimum valid tool-invocation result for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-langchain-agents-architectures.py` | Validates a tool-invocation result and confirms max_iterations + error handling are configured | Pre-commit on agent module changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]]
- [[headless-cli-four-guards]]
- [[handoff-id-payload]]

## Decision tree

See `content/06-decision-tree.xml`. Root question asks whether the solution path is uncertain. Branches route to ReAct (debuggable default), Plan-and-Execute (multi-step with upfront plan), or LATS (uncertain path with backtracking). Each leaf maps to a rule in `01-core-rules.xml`.
