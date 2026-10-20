# Idempotent Write Tools — Keys + Preview/Apply Pairs

## Summary

**One-sentence:** Requires every write tool to accept an agent-supplied idempotency_key and treat retries as no-op replays, and forces destructive or expensive operations into preview+apply pairs so the agent can show its work before the irreversible commit.

**One-paragraph:** Every tool that mutates state must accept an idempotency_key from the agent and be safe to re-run with the same key (returns the same result without duplicating the side effect). Destructive or expensive operations ship as `*_preview` + `*_apply` pairs, separating the agent's reasoning step from the irreversible commit step. Tools time out, networks flake, agent loops retry on transient errors — un-keyed writes silently double-charge, double-deploy, double-email.

**Ефективно для:** агентських інструментів з побічними ефектами — платежі, email, infra-зміни, видалення файлів, DB writes, external POSTs — будь-де, де "at-least-once" не = "exactly-once".

## Applies If (ALL must hold)

- Tool mutates external state: payments, emails, file deletes, infra, DB writes, external API POSTs.
- Tool side effect is destructive (delete) or expensive (deploy, charge) — split into preview+apply.
- Agent runs in a loop with automatic retry on tool errors.
- Tools exposed via MCP with at-least-once delivery.

## Skip If (ANY kills it)

- Pure reads (`get_*`, `search_*`, `list_*`) — no side effect, no key needed.
- Append-only telemetry where duplicates are tolerable.
- Underlying API already idempotent by content hash (e.g. S3 PUT with same body).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Key store | DB / Redis with TTL >=24h | Infrastructure |
| Tool registry | List of write tools needing keys | Engineering audit |
| Reviewer signoff (for preview/apply) | Human or guard-agent identity | Workflow design |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `handoff-id-payload` | Idempotency keys flow with the task_id through the handoff store. |
| `gateway-fallback-chain` | Gateway retries must respect idempotency keys end-to-end. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: key-on-write, no-key-on-read, key-from-agent, preview/apply for destructive, hash-bound apply | ~1100 |
| `content/02-output-contract.xml` | essential | Tool schemas: write-tool, preview, apply | ~1000 |
| `content/03-failure-modes.xml` | essential | Key generated inside tool, missing preview, side-effecty preview | ~900 |
| `content/04-procedure.xml` | recommended | Audit existing tools → key catalog → wire keys → split destructive into pairs | ~900 |
| `content/06-decision-tree.xml` | essential | Per-tool: needs key? needs preview+apply pair? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Audit existing tools for idempotency | sonnet | Pattern detection + judgement |
| Author preview/apply pair for new destructive tool | opus | Long-tail correctness considerations |
| Add `idempotency_key` to existing tool | haiku | Mechanical schema edit |

## Templates

| File | Purpose |
|------|---------|
| `templates/idempotent_tool.py` | Reference Python implementation (Pydantic + key store) for a write tool with replay semantics |
| `templates/_smoke-test.json` | Minimum valid idempotent-tool call body |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-idempotent-write-tools.py` | Validates a tool call body includes idempotency_key and matches the contract | Pre-commit on tool registry changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[handoff-id-payload]]
- [[gateway-fallback-chain]]
- [[file-reference-passing]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the tool mutates state. Branches then route to: no-key (pure read), key-required (write), or preview+apply pair (destructive/expensive). Each leaf maps to a rule.
