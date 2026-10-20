# Agent Observability Stack Blueprint

## Summary

**One-sentence:** Produces a deployable observability spec wiring OTel + LLM-judge + cost ledger + trajectory storage + drift dashboard into one stack, with a vendor decision tree across LangSmith / Langfuse / Helic...

**One-paragraph:** faion has reference catalogues (llm-observability-stack-2026, llm-observability) but no buildable blueprint. Engineers can't evaluate options without reading 5 docs. This produces a deployable stack diagram + opinionated vendor pick per use case + minimum data model. Output: stack-decision artefact + integration plan + week-1 eval-loop wiring.

**Ефективно для:** teams shipping an LLM agent to production with paying users; engineering leads choosing between LangSmith / Langfuse / Helicone / Phoenix; SREs adding OTel traces to an agent pipeline; PMs requesting a drift dashboard.

## Applies If (ALL must hold)

- Team shipping an LLM agent to production OR pre-prod with paying users
- Eval scores or cost are not currently visible per request
- ≥2 LLM providers OR ≥2 prompt variants are in play
- Owner exists for the dashboard once shipped

## Skip If (ANY kills it)

- Pre-PMF prototype with <100 requests/day — manual logs are cheaper
- Compliance requires fully self-hosted with no external SaaS option
- Team already on a working stack (LangSmith etc.) and just needs prompt-eng

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Agent code | Python / TS source | repo |
| LLM provider list + traffic split | config | team |
| Cost ceiling | USD / month | finance |
| Eval ground-truth set ≥30 examples | JSONL | eval owner |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (r1-r5 plus the skip-methodology rule for the pre-PMF branch) with rationale and source | ~750 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pick vendor | sonnet | Rubric application. |
| Author OTel instrumentation | sonnet | Mechanical from template. |
| Diagnose drift alert | opus | Multi-signal reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/otel-instrumentation.py.tmpl` | Python OTel instrumentation skeleton for LLM/tool/retrieval calls. |
| `templates/_smoke-test.md.j2` | Filled blueprint for a 2-model agent on Langfuse self-host. |
| `templates/_smoke-test.md` | Filled blueprint for a 2-model agent on Langfuse self-host. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-observability-stack-blueprint.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[agent-postmortem-template]]`
- `[[agent-drift-detection-statistical]]`
- `[[agent-eval-harness-bootstrap-recipe]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-observability-stack-blueprint applies: root question — "Is the agent in production OR pre-prod with paying users?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
