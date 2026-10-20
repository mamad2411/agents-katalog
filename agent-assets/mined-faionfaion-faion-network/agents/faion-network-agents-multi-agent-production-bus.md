# Multi-Agent Production Bus

## Summary

**One-sentence:** Produces a production multi-agent-system spec wired to a central async MessageBus with three switchable strategies (hierarchical / parallel / sequential).

**One-paragraph:** Simple sync multi-agent patterns break in production: one slow worker blocks downstream agents; no audit trail of inter-agent messages; cost per run is invisible; coordination logic is hard-coded. This methodology emits a deterministic spec: MessageBus + structured Message schema + handler timeouts + per-strategy dispatch + cost gate + observability hookup (agentops / LangSmith).

**Ефективно для:** team running 5+ specialised agents in production where current synchronous orchestration is hitting timeouts and the audit trail is the worst part of every postmortem.

## Applies If (ALL must hold)

- Production system needs to switch strategy at runtime without rewriting agent code.
- Audit trail of every inter-agent message is required (compliance or debugging).
- Async environment available (asyncio or equivalent).
- Cost attribution per agent role is required.
- ≥3 worker agents in the system.

## Skip If (ANY kills it)

- Simple two-agent sync pipeline — bus adds setup overhead with no value.
- Prototype where iteration speed beats auditability.
- Sync-only environment (no asyncio).
- Single-agent loop — no bus needed.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `agent-roster.yaml` | list of {name, role, model, budget_tokens} | operator |
| `default_strategy` | hierarchical / parallel / sequential | operator |
| `handler_timeout_seconds` | integer | ops |
| `observability_backend` | agentops / langsmith / none | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[max-turns-circuit-breaker]] | Strategy execution must cap turns. |
| [[manifest-then-fetch]] | Inter-agent payloads should follow the manifest protocol. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: structured Message only, timeout-wrap handlers, broadcast excludes sender, no circular awaits, cost gate per agent, observability tags. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the multi-agent-system-spec. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: free-form string content, missing handler timeout, deadlock circular await, cost explosion, untagged tokens. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: enumerate roles → pick strategies → wire bus → set budgets → tag observability. | ~700 |
| `content/05-examples.xml` | recommended | Reference MessageBus + ProductionMultiAgentSystem worked example. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks sequential vs parallel vs hierarchical from drivers. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_roster` | haiku | Mechanical YAML→typed list. |
| `pick_strategies` | sonnet | Tradeoff between throughput and traceability. |
| `audit_deadlock_paths` | opus | Cross-agent circular-await detection — subtle. |
| `emit_system_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/message-bus.py` | MessageBus + Message + CommunicationType reference impl. |
| `templates/_smoke-test.yaml` | Minimum 2-agent roster. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-multi-agent-production-bus.py` | Validates spec against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-conversational]]
- [[max-turns-circuit-breaker]]
- [[manifest-then-fetch]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `subtasks_independent` (yes → parallel; no → continue), then on `chain_shape` (linear → sequential; dependent_dag → hierarchical with planner). Each leaf cites a rule id.
