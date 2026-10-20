# Record-Replay Debugging

## Summary

**One-sentence:** Produces a debugging spec wiring record-replay for agent runs: persist every LLM call + tool result; replay deterministically against a frozen recording.

**One-paragraph:** Agent failures are hard to reproduce: non-deterministic models + flaky tools + race conditions. Record-replay captures every LLM call + tool result + timestamp into a recording file; replay reads from the recording instead of hitting live services. Bug surfaces deterministically; fix lands in one iteration.

**Ефективно для:** team that can't reproduce a production agent failure; the only artefact is one user report and a stale trace.

## Applies If (ALL must hold)

- Production agent failures are hard to reproduce.
- Multi-step agents with tool calls.
- Cost or risk prevents re-running against live services.

## Skip If (ANY kills it)

- Single-call no-tool agents.
- Read-only agents.
- Prototype with no production failures.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `agent-entrypoints.yaml` | list of entrypoints to wrap | operator |
| `recording_store_uri` | S3/local-fs | infra |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Background (what record must capture, why replay is a fix-verification harness) + 9 testable rules: r1-record-all-calls; r2-deterministic-replay; r3-redact-secrets; r4-version-recording-format; r5-replay-in-ci; r6-replay-zero-network; r7-tag-side-effects; r8-mutate-one-axis; r9-promote-trace-to-eval; source links. | ~1650 |
| `content/02-output-contract.xml` | essential | JSON Schema for the config artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (sampled recording, silent mismatch, secrets in trace, no version, partial recording, replay-once). | ~550 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure. | ~600 |
| `content/05-examples.xml` | recommended | Worked spec example; ReplayLLM strict-guard vs silent-fallthrough; mutation-replay one-axis vs three-axes (python). | ~850 |
| `content/06-decision-tree.xml` | essential | Decision branches mapped to rule ids (r1, r7, r9, r5). | ~450 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_input` | haiku | Mechanical. |
| `classify_drivers` | sonnet | Subjective tradeoffs. |
| `audit_output` | opus | Cross-cutting subtleties. |
| `emit_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/record-replay-debugging-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/record-replay-debugging-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/record-replay-debugging-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-record-replay-debugging.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
