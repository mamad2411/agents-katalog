# Technical Debt Management

## Summary

**One-sentence:** Maintain a debt register, budget 10-20% of capacity for debt work per sprint, prioritise by interest rate (cost-of-living-with × likelihood-of-incident), and refuse zero-debt sprints.

**One-paragraph:** Tech debt is treated as a managed liability, not a moral failing. Each item carries an interest rate (cost of carrying × likelihood of incident); each sprint pays a 10-20% budget; the register prevents debt from being invisible. Zero-debt sprints are forbidden because they always reappear as crisis sprints.

**Ефективно для:**

- Solo dev with a 14-month codebase already groaning under inherited choices; needs a forcing function to keep paying down debt without sacrificing every feature.

## Applies If (ALL must hold)

- Codebase ≥3 months old.
- Team capacity is measurable per sprint / cycle.
- Stakeholder pressure to ship features risks crowding out debt work.

## Skip If (ANY kills it)

- Greenfield <1 month old — no debt accumulated.
- Pure throwaway prototype — never going to maintain.
- Crisis sprint stabilising production — debt work pauses.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Codebase access | credential | Repo |
| Sprint capacity (person-days) | integer | Team plan |
| Interest-rate rubric | table | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/backlog-management` | Debt register is a state in the backlog. |
| `solo/dev/code-quality (free tier)` | Practices that reduce new debt creation. |

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
| `draft-technical-debt-management` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-technical-debt-management` | haiku | Schema check + threshold checks; deterministic. |
| `review-technical-debt-management` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/technical-debt-management.json` | JSON skeleton conforming to the output contract schema. |
| `templates/technical-debt-management.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-technical-debt-management.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[backlog-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/technical-debt-management.json`

```json
{
  "artefact_id": "technical-debt-management-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "register": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "debt_budget_pct": 1.0,
  "interest_rate_rubric": {
    "key": "value"
  },
  "sprint_review_cadence": "sprint_review_cadence value",
  "owner": "@solo-founder"
}
```
