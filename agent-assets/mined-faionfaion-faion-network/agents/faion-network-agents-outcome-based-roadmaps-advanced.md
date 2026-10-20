# Outcome Based Roadmaps Advanced

## Summary

**One-sentence:** Decomposes business goals into product outcomes → leading indicators → falsifiable experiments with confidence levels (High/Med/Low/Exploring) and four audience-tailored artefacts (customer, board, engineering, sales) emitted from one source.

**One-paragraph:** Decomposes business goals into product outcomes → leading indicators → falsifiable experiments with confidence levels (High/Med/Low/Exploring) and four audience-tailored artefacts (customer, board, engineering, sales) emitted from one source. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Outcome Based Roadmaps Advanced on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Stakeholder demands feature timelines while the team owns outcome metrics.
- Quarterly OKR has just been published and must be decomposed.
- Multiple audiences (board, customer, engineering, sales) need the same roadmap reformatted.
- Outcome roadmap (basic) is already in place and needs decomposition depth.

## Skip If (ANY kills it)

- Pre-PMF — no product outcomes to track yet.
- Compliance / regulatory work where the outcome is dictated externally.
- Teams without analytics instrumentation for leading indicators.
- One-off internal tools with binary success criterion.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Business goal statement | sentence with metric+target+deadline | Leadership |
| Analytics instrumentation | dashboard inventory | BI |
| Outcome-based roadmap (basic) in place | artefact | Prior methodology |
| Audience list | table | Stakeholder map |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/outcome-based-roadmaps` | Provides the basic outcome roadmap as decomposition input. |
| `solo/product/product-planning/roadmap-design` | Format-selection upstream. |

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
| `draft-outcome-based-roadmaps-advanced` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-outcome-based-roadmaps-advanced` | haiku | Schema check + threshold checks; deterministic. |
| `review-outcome-based-roadmaps-advanced` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/outcome-based-roadmaps-advanced.json` | JSON skeleton conforming to the output contract schema. |
| `templates/outcome-based-roadmaps-advanced.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-outcome-based-roadmaps-advanced.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[outcome-based-roadmaps]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/outcome-based-roadmaps-advanced.json`

```json
{
  "artefact_id": "outcome-based-roadmaps-advanced-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "business_goal": "business_goal value",
  "product_outcomes": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "leading_indicators": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "experiments": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "confidence_labels": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "owner": "@solo-founder"
}
```
