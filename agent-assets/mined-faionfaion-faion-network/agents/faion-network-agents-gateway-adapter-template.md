# Gateway Adapter Template

## Summary

**One-sentence:** Produces a gateway-adapter scaffold (Python or TS) that normalises N provider APIs behind one envelope: routing, retries, cost-tagging, telemetry, structured-output enforcement.

**Ефективно для:** Teams calling Anthropic / OpenAI / Gemini directly from app code; every model swap requires editing N callsites. The adapter behind a gateway makes provider changes a config edit.

**One-paragraph:** This methodology pins the recurring decision around "gateway adapter template" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a single accountable owner is named; the decision tree routes preconditions to a run/skip outcome. Source material grounded in: Maxim AI — LLM Gateway architecture / MLflow AI Gateway.

## Applies If (ALL must hold)

- Task is an instance of the recurring "gateway adapter template" decision OR a closely-adjacent variant.
- Operator has the artefacts named in Prerequisites available before starting.
- Output will be consumed by a downstream agent, gate, or named human reviewer.
- A single accountable owner can be named.
- Tier == geek or higher.

## Skip If (ANY kills it)

- Team already maintains a working artefact for this gap — replace, do not duplicate.
- Single-use throwaway task — overhead of the contract is not justified.
- Regulatory regime mandates a vendor governance platform — defer to vendor flow.
- Greenfield prototype with no production users yet.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Last 30 days of context for the recurring "gateway adapter template" task | text / logs | system of record |
| Write access to the artefact store (repo / wiki / decision log) | repo path | repo admin |
| Named owner accountable for the output downstream | handle / email | team roster |
| Baseline conventions (CLAUDE.md / AGENTS.md / CONVENTIONS.md) | md | code repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/llm-integration` | parent operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules customised to "gateway adapter template" | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~1000 |
| `content/06-decision-tree.xml` | essential | Run / skip / variant router with conclusion-ref to rules | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Bounded template fill |
| `synthesize_artefact` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|---|---|
| `templates/gateway-adapter-template.json` | JSON schema for the output contract |
| `templates/gateway-adapter-template.md.j2` | Markdown skeleton with required fields |
| `templates/gateway-adapter-template.md` | Markdown skeleton with required fields Generated from `templates/gateway-adapter-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-gateway-adapter-template.py` | Enforce the output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[cost-quality-tradeoff-framework]] — adjacent framework.
- [[eval-contract-template]] — adjacent eval gate.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question tree: (1) preconditions present? - no = skip; yes (2) variant detected per topic-specific signal? - routes to the appropriate produced variant. Terminal branches reference rules in `content/01-core-rules.xml`.
