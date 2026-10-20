# Roadmap Design

## Summary

**One-sentence:** Picks the right roadmap format (Now-Next-Later / timeline / outcome-themed) by uncertainty level and stakeholder mix; produces an internal source-of-truth roadmap plus one external derivative view.

**One-paragraph:** Picks the right roadmap format (Now-Next-Later / timeline / outcome-themed) by uncertainty level and stakeholder mix; produces an internal source-of-truth roadmap plus one external derivative view. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Roadmap Design on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Multi-quarter horizon needs a strategic communication artefact.
- ≥2 audiences (internal team, external customer, board) consume the roadmap.
- Uncertainty level is known (low / medium / high).
- Team owns the metric movement, not just delivery dates.

## Skip If (ANY kills it)

- Single sprint / single feature — direct release plan is enough.
- Contract-defined deliverables — timeline format is forced, no design needed.
- Pre-PMF — discovery roadmap not strategic roadmap.
- Pure backlog without strategic intent — keep it flat.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategic horizon (quarters) | integer | Planning |
| Uncertainty assessment | low/medium/high | Team |
| Audience list | table | Stakeholder map |
| Metric tree (optional) | diagram | OKR setting |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/okr-setting` | OKRs as roadmap anchors. |
| `solo/product/product-planning/outcome-based-roadmaps` | Format option for high-uncertainty horizons. |

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
| `draft-roadmap-design` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-roadmap-design` | haiku | Schema check + threshold checks; deterministic. |
| `review-roadmap-design` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/roadmap-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/roadmap-design.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-roadmap-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[outcome-based-roadmaps]]
- [[okr-setting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/roadmap-design.json`

```json
{
  "artefact_id": "roadmap-design-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "horizon_quarters": 1,
  "uncertainty": "low",
  "format": "timeline",
  "internal_rows": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "external_themes": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "not_doing": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "owner": "@solo-founder"
}
```
