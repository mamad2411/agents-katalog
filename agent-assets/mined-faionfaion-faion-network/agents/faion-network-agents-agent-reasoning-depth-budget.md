# Agent Reasoning Depth Budget

## Summary

**One-sentence:** Produces a per-task thinking-token budget table with eval evidence, under-/over-thinking detectors, and an inter-turn compression rule — keeping reasoning spend bounded without crashing quality.

**One-paragraph:** faion has reasoning-first-architectures, plan-execute-vs-react, previous-response-id-reasoning-reuse. Missing: the operating discipline of choosing budget with eval evidence. Mechanism: start small, expand until score plateaus; under/over detectors; inter-turn compression. Output: per-task budget table + eval evidence + drift triggers.

**Ефективно для:** agents using extended-thinking (Claude), reasoning effort (OpenAI o-series), thinking tokens (Gemini); multi-turn agents whose context budget is dominated by prior reasoning traces; teams whose bill is reasoning-token-driven.

## Applies If (ALL must hold)

- Agent uses extended-thinking / chain-of-thought / reasoning-token APIs
- Eval scores exist for the task at multiple budgets
- Cost ceiling is defined and reasoning tokens are a measurable line item
- Multi-turn agent where prior thinking accumulates in context

## Skip If (ANY kills it)

- Single-turn deterministic task — budget is a constant
- No eval suite — cannot measure plateau
- Cost is dominated by non-reasoning tokens (long retrieval contexts) — solve that first

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval suite ≥30 examples with scoring rubric | JSONL + judge | eval owner |
| Reasoning-token API access | provider SDK | team |
| Cost ceiling per task / per day | USD | finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-eval-harness-bootstrap-recipe]]` | Harness to run budget sweeps |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (r1-r5 plus the skip-methodology routing rule) with rationale and source | ~600 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author sweep + Pareto pick | sonnet | Mechanical from harness output. |
| Diagnose under/over-thinking | opus | Pattern recognition on traces. |
| Author compression prompt | sonnet | Template application. |

## Templates

| File | Purpose |
|------|---------|
| `templates/under-over-detector.py.tmpl` | Detector skeleton from trace stream. |
| `templates/_smoke-test.md.j2` | Filled example for a 5-class task agent. |
| `templates/_smoke-test.md` | Filled example for a 5-class task agent. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-reasoning-depth-budget.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[agent-eval-harness-bootstrap-recipe]]`
- `[[agent-eval-cost-budget-policy]]`
- `[[agent-observability-stack-blueprint]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-reasoning-depth-budget applies: root question — "Does the agent use extended-thinking / reasoning tokens?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
