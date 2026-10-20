# A/B Testing

## Summary

**One-sentence:** Run a pre-registered controlled experiment (control vs variant) on a live population with a primary metric, guardrails, and pre-calculated sample size to decide ship/hold on evidence.

**One-paragraph:** Run a pre-registered controlled experiment (control vs variant) on a live population with a primary metric, guardrails, and pre-calculated sample size to decide ship/hold on evidence.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Change has one clear primary metric (conversion, click-through, retention).
- Traffic supports at least 1,000 conversions per month per variant.
- Exactly one variable changes between control and variant.
- Engineering can route traffic and tag events at session granularity.
- Stakeholders agree to stop or extend strictly per pre-registered rule.

## Skip If (ANY kills it)

- Traffic below ~1,000 conversions per month — results will be inconclusive.
- Major redesign with multiple simultaneous changes — confounds prevent attribution.
- Question is 'why' users behave a certain way — run user interviews instead.
- Regulatory or safety-critical change — split exposure carries risk.
- Early-stage product where the primary metric is itself unclear.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hypothesis with metric and MDE | markdown | PM + analyst pair |
| Sample-size calculation | spreadsheet | Statistician tool |
| Experimentation platform config | yaml / dashboard | Growth platform |
| Tracking spec | markdown | Analytics team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/usability-testing` | Qualitative session footage explains quantitative deltas. |
| `solo/ux/ux-ui-designer/competitive-analysis` | External benchmarks inform realistic MDE values. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ab-testing.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ab-testing.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[usability-testing]]
- [[heuristic-evaluation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ab-testing.json`

```json
{
  "artefact_id": "ab-testing-example",
  "method": "Method used for the report (e.g. interview / heuristic / test).",
  "sample_size": 6,
  "findings": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "severity_breakdown": {
    "high": 1,
    "medium": 2,
    "low": 0
  },
  "recommendations": [
    "item-1",
    "item-2"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "lint_status": "pass",
  "owner": "@solo-founder"
}
```
