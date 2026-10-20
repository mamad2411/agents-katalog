# Structured Tool Errors with recoveryHint

## Summary

**One-sentence:** Tool errors are part of the prompt — return a structured `{code, message, recoveryHint, traceId, …}` envelope so the agent loop can branch deterministically.

**One-paragraph:** Produces an error envelope returned by every tool error path with required fields `code` (UPPER_SNAKE), `message` (one human sentence, no stack trace), `recoveryHint` (closed enum `RETRY_LATER | CHECK_INPUT | TRY_ALTERNATIVE | REPORT_TO_USER | NEEDS_AUTH`), `traceId` (correlation ID), and optional `retry_after_seconds` + sanitised `details`. The closed-enum hint maps to one and only one runner action; the agent loop never re-interprets it. Studies (SHIELDA, Kumaran MCP error guide) report 30%+ reduction in dead-end retry loops vs free-form errors.

**Ефективно для:** будь-якого tool / MCP сервера, де агент в циклі retry-ить запити (rate-limits, auth, transient 5xx) і блукає в free-form error-повідомленнях замість дискретного "RETRY_LATER / CHECK_INPUT".

## Applies If (ALL must hold)

- Tool is invoked from an agent loop where the model may retry on its own.
- Tool wraps a flaky upstream (rate-limits, auth, transient 5xx) OR is an MCP server with a public error contract.
- The agent runner has (or will gain) a hint → action dispatcher.
- Errors are returned as JSON bodies the model can read.

## Skip If (ANY kills it)

- Failures are genuinely unrecoverable AND the tool is invoked by deterministic code that never retries.
- Tool is invoked synchronously by a human user only (errors go to a UI, not a model loop).
- Tool emits warnings on a successful path; warnings belong in a separate `warnings: []` field, not the error envelope.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool definition | JSON Schema / Anthropic tool spec / MCP manifest | tool source repo |
| Upstream failure taxonomy | enumerated list | runbook |
| Agent runner hint-dispatch map | YAML | `runner/policy.yml` |
| Existing error responses | sample HTTP bodies | logs / traces |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/idempotent-write-tools` | Retries are only safe on idempotent tools; this companion methodology guarantees the precondition. |
| `geek/ai/ai-agents/headless-cli-four-guards` | Bounds the retry loop with `--max-turns`. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: envelope shape, closed recoveryHint enum, no raw stack traces, runner hint→action map, traceId mandatory | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tool error envelope (already present in templates as `error_envelope.json`) | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: HTTP-code-as-error-code, stack-trace-in-details, missing-traceId, freeform-hint-prose, fabricated-RETRY_LATER | ~700 |
| `content/04-procedure.xml` | medium | Migrate a tool: identify error paths → assign codes → assign hints → wire dispatcher → smoke test | ~800 |
| `content/06-decision-tree.xml` | essential | Picks `recoveryHint` value per failure category | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Inventory existing tool error paths | sonnet | Mechanical AST walk. |
| Assign `recoveryHint` per failure | opus | Risk judgement; opus weighs retry vs escalate. |
| Wire runner hint → action map | sonnet | Boilerplate plumbing. |
| Generate the OpenAPI / MCP error schema | sonnet | Schema translation, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error_envelope.json` | JSON Schema for the tool error envelope — copy into tool / MCP server contract. |
| `templates/recovery_hints.txt` | Closed enum of recovery hints with a one-line semantic for each value. |
| `templates/runner_policy.yaml` | YAML map from `recoveryHint` to runner action with retry budgets and timeouts. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-tool-errors.py` | Validates a sample tool-error JSON body against `02-output-contract.xml` / `error_envelope.json`. | Pre-commit hook on tool definitions; runtime smoke test in tool's test suite. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]] — `RETRY_LATER` is only safe when the tool is idempotent.
- [[headless-cli-four-guards]] — `--max-turns` bounds the retry loop in CLI invocations.
- [[stream-json-orchestration]] — orchestrator observes error envelopes via `tool_result` events.
- [[verb-object-tool-naming]] — tool naming companion; both improve agent error handling.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the `recoveryHint` value from the failure category: rate-limit / transient 5xx → `RETRY_LATER`; 4xx with bad arguments → `CHECK_INPUT`; auth missing/expired → `NEEDS_AUTH`; unrecoverable / 5xx with no retry budget → `REPORT_TO_USER`; resource missing but a peer tool exists → `TRY_ALTERNATIVE`. Use it whenever the question is "which hint do I emit for THIS failure".
