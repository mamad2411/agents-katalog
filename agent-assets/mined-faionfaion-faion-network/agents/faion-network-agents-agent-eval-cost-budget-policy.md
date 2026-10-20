# Agent Eval Cost Budget Policy

## Summary

**One-sentence:** Produces a 3-cadence eval policy: nightly full suite, per-PR fast subset, weekly adversarial — with sampling rules and a judge-model fallback when budget breached.

**One-paragraph:** Evals can cost more than production traffic. Need a policy: nightly full / per-PR fast-subset / weekly adversarial; sampling rules; judge-model fallback when budget breached. No methodology today. This produces a versioned policy record + per-cadence schema + breach playbook.

**Ефективно для:** production agents with daily eval spend ≥$50; teams whose CI cost is dominated by evals; pre-GA agents that need both fast PR feedback and deep nightly coverage.

## Applies If (ALL must hold)

- Eval cost is a measurable line item ≥$50/month
- ≥1 PR per day touches the agent
- Ground-truth set ≥30 examples exists
- Cost ceiling defined and visible

## Skip If (ANY kills it)

- Pre-MVP — manual eval is cheaper than authoring policy
- No CI pipeline yet — author CI first
- Single nightly cadence already works and costs <$10/day

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval suite + judge rubric | JSONL + rubric | eval owner |
| Per-run cost telemetry | table | observability |
| Cost ceiling per cadence | USD | finance |
| Cheap-judge fallback model | API access | ML platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agent-eval-harness-bootstrap-recipe]]` | Harness to schedule cadences |
| `[[agent-eval-test-set-curation]]` | Test set partitioned into fast subset |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~550 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Stratified-sample fast subset | sonnet | Mechanical. |
| Pick fallback judge | sonnet | Vendor selection. |
| Tune ceiling vs cadence | opus | Cost / quality trade-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stratified-sample.py.tmpl` | Stratified subset selector. |
| `templates/fallback-judge.py.tmpl` | Cheap-judge fallback switch. |
| `templates/_smoke-test.md.j2` | Filled example for a 200-example suite. |
| `templates/_smoke-test.md` | Filled example for a 200-example suite. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-eval-cost-budget-policy.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- `[[agent-eval-harness-bootstrap-recipe]]`
- `[[agent-eval-test-set-curation]]`
- `[[agent-drift-detection-statistical]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether agent-eval-cost-budget-policy applies: root question — "Is eval spend ≥$50/month AND ≥1 PR/day touches the agent?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
