# MLP Planning

## Summary

**One-sentence:** Plan a Minimum Lovable Product: one 'wow' moment, ≥1 thoughtful UX detail, real polish on the critical path, but everything else stays MVP-level.

**One-paragraph:** An MLP layers one designed-for-delight moment on top of an MVP. The methodology forces choice — exactly one wow moment, not three — and gates polish to the critical path so the rest of the product still ships in MVP shape. The goal is love, not feature-completeness.

**Ефективно для:**

- Solo founder whose MVP-shaped product gets 'meh' reactions; ready to invest a delight sprint on one polished moment without rebuilding everything.

## Applies If (ALL must hold)

- Have an MVP that ships and works.
- Goal is love / word-of-mouth, not just learning.
- ≤5 dev-days available for delight investment.

## Skip If (ANY kills it)

- MVP still failing core utility test — fix that first.
- Goal is learning, not love — use MVP frame.
- Audience tolerates rough edges (e.g. internal tooling).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Working MVP | url | Product |
| User feedback on MVP | log | Feedback funnel |
| Critical-path map | diagram | UX doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/minimum-product-frameworks` | Frame selection that points to MLP. |
| `solo/ux/ui-designer` | Design layer for the wow moment. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-mlp-planning` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-mlp-planning` | haiku | Schema check + threshold checks; deterministic. |
| `review-mlp-planning` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mlp-planning.json` | JSON skeleton conforming to the output contract schema. |
| `templates/mlp-planning.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mlp-planning.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[minimum-product-frameworks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/mlp-planning.json`

```json
{
  "artefact_id": "mlp-planning-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "wow_moment": "wow_moment value",
  "critical_path_steps": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "polish_budget_days": 1.0,
  "non_polish_scope": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "owner": "@solo-founder"
}
```
