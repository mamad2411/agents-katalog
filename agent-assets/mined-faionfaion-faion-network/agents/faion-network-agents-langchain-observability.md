# LangChain Observability

## Summary

**One-sentence:** Configures LangSmith tracing + structured callbacks + streaming on a LangChain chain and emits a tracing-config decision-record with rule citations.

**One-paragraph:** Production LangChain chains running without tracing are nearly impossible to debug retroactively — intermediate steps, token usage, and tool calls are only captured at run time. This methodology turns a runtime profile (latency target, cost cap, PII posture) into a deterministic tracing configuration: LangSmith on/off, callback set, streaming mode, redaction rules. Output is a JSON decision-record + env snippet ready to drop into the deployment.

**Ефективно для:** solopreneur deploying a multi-tool LangChain agent to production who has to debug failures without re-running them.

## Applies If (ALL must hold)

- Production or pre-production LangChain (or LangGraph) deployment.
- Chain has ≥2 tools, retrievers, or sub-chains (debugging single calls is trivial).
- You can set environment variables on the runtime.
- Cost or latency matters — you need numbers per turn.
- Failures are intermittent enough that you cannot reproduce them on demand.

## Skip If (ANY kills it)

- Throwaway notebook with no users — printf-debugging is fine.
- Hard PII ban on sending traces to any external service (then build a local-only callback).
- Single LLM call, no tools, no retrieval — trace adds zero signal.
- Customer contractually forbids LangSmith — use OpenTelemetry instead and apply a different methodology.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `runtime-profile.yaml` | YAML with `latency_target_ms`, `cost_cap_per_turn_usd`, `pii_posture`, `tracing_backend` | author writes; ≤15 lines |
| `LANGCHAIN_API_KEY` | env var | LangSmith project settings |
| Chain entrypoint | Python module path | the runnable to instrument |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[langchain-basics]] | Need to know what a Runnable is. |
| [[langchain-production-patterns]] | Tracing pairs with retries and fallbacks. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Tracing-from-day-one + callback + streaming rules | ~1000 |
| `content/02-output-contract.xml` | essential | tracing-config JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Silent-no-trace, PII leak, callback exception swallow | ~600 |
| `content/04-procedure.xml` | recommended | 5-step instrumentation procedure | ~800 |
| `content/06-decision-tree.xml` | essential | tracing backend + redaction tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Backend selection + redaction rules | sonnet | Needs cost + PII reasoning. |
| Env snippet emission | haiku | Templated. |
| PII review | opus | Subtle leakage paths; do not skimp. |

## Templates

| File | Purpose |
|---|---|
| `templates/runtime-profile.yaml` | Input contract — 6 fields. |
| `templates/tracing-config.env` | Output: LANGCHAIN_* env vars filled in. |
| `templates/structured-callback.py` | Working CallbackHandler scaffold with redaction. |
| `templates/_smoke-test.yaml` | Minimum-viable profile. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-langchain-observability.py` | Validates tracing-config JSON against schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-production-patterns]] — pairs retries + tracing for full prod hardening.
- [[max-turns-circuit-breaker]] — tracing without a turn cap is half a safety net.
- [[llamaindex-production-gotchas]] — sibling observability concerns in LlamaIndex.

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `pii_posture` first (no-export → local-only OpenTelemetry; else LangSmith), then on `latency_target_ms` (≤500ms → streaming required; else optional), then on `cost_cap_per_turn_usd` (≤$0.01 → token logging only, no full payload). Each leaf cites a rule in 01-core-rules.xml.
