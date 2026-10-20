# LangChain Multi-Agent Systems

## Summary

**One-sentence:** Builds LangGraph multi-agent systems using one of three canonical patterns — supervisor routing, debate consensus, or hierarchical teams — with structured-output routing, hard round limits, and isolated unit tests per specialist.

**One-paragraph:** Multi-agent collaboration patterns and testing strategies using LangChain and LangGraph. Three patterns: Supervisor (one router → specialists), Debate (peer agents reach consensus via judge), Hierarchical (teams of teams under a coordinator). Use `with_structured_output(Route)` for routing, set a hard round limit on debates, compile each team subgraph independently. Unit-test specialists with mocked LLMs; integration-test the full graph with real calls.

**Ефективно для:** проєктів з ≥3 спеціалізованими ролями, де лінійний пайплайн неможливий, але мережа має бути auditable і testable.

## Applies If (ALL must hold)

- Workflow has 3+ specialised agent roles.
- Routing decisions are domain-specific (different specialists for different inputs).
- Each specialist's logic is independently testable.

## Skip If (ANY kills it)

- Linear workflow with no branching — use a single LangGraph workflow or LCEL chain.
- Agents need to share complex mutable state — race-condition risk.
- Latency critical — supervisor routing adds an LLM call per request.
- Team size small and no specialisation benefit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Specialist roster | List of role names + responsibilities | Architecture spec |
| Shared state schema | TypedDict | Application code |
| Checkpointer | Redis/Postgres/SQLite for persistence | Infrastructure |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `langchain-agents-architectures` | Each specialist uses one of the three single-agent architectures. |
| `handoff-id-payload` | Handoffs between specialists follow the typed payload contract. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Six rules: structured routing, hard round limit, mock-LLM unit tests, schema-versioning, prompt-injection guard, audit-log | ~1100 |
| `content/02-output-contract.xml` | essential | Route Pydantic + DebateState + HierarchicalState schemas | ~1100 |
| `content/03-failure-modes.xml` | essential | Free-form routing, debate non-convergence, schema mismatch in subgraphs | ~900 |
| `content/06-decision-tree.xml` | essential | Supervisor vs Debate vs Hierarchical | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Supervisor route | sonnet or haiku w/ Route Pydantic | Constrained classification |
| Specialist work | per-role, typically sonnet | Domain reasoning |
| Judge in debate | opus | Synthesises multiple positions |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.json` | Minimum valid Route output for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-langchain-agents-multi-agent.py` | Validates a Route JSON against the schema | Pre-commit on supervisor changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-agents-architectures]]
- [[handoff-id-payload]]
- [[discriminated-union-output]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the work map suits routing (supervisor), consensus (debate), or nested teams (hierarchical).
