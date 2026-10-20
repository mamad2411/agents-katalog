# User Story Mapping

## Summary

**One-sentence:** Arrange user activities as a left-to-right backbone with tasks stacked vertically by priority; the walking skeleton is one task per activity, and every release slice spans the full backbone.

**One-paragraph:** Arrange user activities as a left-to-right backbone with tasks stacked vertically by priority; the walking skeleton is one task per activity, and every release slice spans the full backbone. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run User Story Mapping on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Feature spans ≥3 user activities and benefits from a 2D view.
- Backlog is flat and lost journey context.
- Cross-functional team needs a shared journey picture before sprint planning.
- MVP / walking-skeleton needs to be identified from a larger scope.

## Skip If (ANY kills it)

- Pure technical work (refactor / infra) — no user-facing backbone.
- Tiny single-flow feature — direct user stories suffice.
- No shared journey understanding yet — do journey-mapping or JTBD first.
- Single-screen UI — story map is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User persona + journey scope | doc | Discovery |
| Backlog or feature list | ticket export | Backlog tool |
| Workshop participants | PM + design + eng | Team |
| Workshop space (digital or physical) | Miro / sticky wall | Logistics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/mvp-scoping` | Walking skeleton feeds MVP scope cut. |
| `solo/product/product-planning/release-planning` | Release slices feed release plan. |

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
| `draft-user-story-mapping` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-user-story-mapping` | haiku | Schema check + threshold checks; deterministic. |
| `review-user-story-mapping` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-story-mapping.json` | JSON skeleton conforming to the output contract schema. |
| `templates/user-story-mapping.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-story-mapping.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[mvp-scoping]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/user-story-mapping.json`

```json
{
  "artefact_id": "user-story-mapping-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "persona": "persona value",
  "backbone": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "tasks": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "walking_skeleton": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "release_slices": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "owner": "@solo-founder"
}
```
