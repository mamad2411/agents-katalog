# Product Lifecycle

## Summary

**One-sentence:** Place the product in one of five lifecycle stages (idea / launch / growth / maturity / decline) and apply the stage-specific playbook so the operating model matches reality.

**One-paragraph:** A product's operating model differs per lifecycle stage; running launch tactics in maturity wastes capital, and running maturity tactics at launch starves growth. The template forces a stage assessment with ≥3 signals and routes to the stage-specific playbook.

**Ефективно для:**

- Solo founder unsure whether to keep pouring fuel into growth, defend margins, or sunset gracefully — needs a stage check before the next quarter's plan.

## Applies If (ALL must hold)

- Product has at least 1 user cohort with known behaviour.
- Quarterly planning is happening or imminent.
- Stage is genuinely ambiguous (any two of growth/maturity/decline plausible).

## Skip If (ANY kills it)

- Pre-product phase — lifecycle does not apply.
- Crisis mode — stage assessment after stabilisation, not during.
- Stage is unambiguously known and current playbook fits.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Growth metric history (12+ months ideal) | csv | Analytics |
| Cohort retention curve | chart | Analytics |
| Margin trend | table | Finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/product-analytics` | Signal source for stage assessment. |
| `solo/product/product-manager/roadmap-design` | Downstream artefact the stage decision shapes. |

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
| `draft-product-lifecycle` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-product-lifecycle` | haiku | Schema check + threshold checks; deterministic. |
| `review-product-lifecycle` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-lifecycle.json` | JSON skeleton conforming to the output contract schema. |
| `templates/product-lifecycle.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-lifecycle.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-analytics]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/product-lifecycle.json`

```json
{
  "artefact_id": "product-lifecycle-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "current_stage": "idea",
  "signals": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "confidence": "low",
  "recommended_playbook": "recommended_playbook value",
  "owner": "@solo-founder"
}
```
