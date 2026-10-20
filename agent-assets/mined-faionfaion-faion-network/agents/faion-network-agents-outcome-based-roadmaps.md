# Outcome Based Roadmaps

## Summary

**One-sentence:** Quarterly outcome roadmap with verb+metric+delta+timeframe outcomes, candidate solutions (to-validate), explicit not-doing list, and a kill signal per outcome.

**One-paragraph:** Quarterly outcome roadmap with verb+metric+delta+timeframe outcomes, candidate solutions (to-validate), explicit not-doing list, and a kill signal per outcome. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Outcome Based Roadmaps on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Quarterly planning where the best solution is still uncertain.
- Stakeholders conflate feature lists with contractual commitments.
- Discovery loop is active and the roadmap must survive the next experiment.
- Multiple teams or contractors need goal alignment without locking solutions.

## Skip If (ANY kills it)

- Contractually committed deliverables (RFPs, enterprise SLAs, regulatory deadlines).
- Pure execution phase with fully scoped and validated work.
- No metrics pipeline; outcome roadmaps require trustworthy baselines.
- Pre-PMF zero-to-one stage where finding any user is the priority.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Analytics baseline per metric | dashboard URL | BI tool |
| Quarterly outcome statement | string | Leadership input |
| Candidate solution list | list | Discovery output |
| Not-doing list | list | Strategy review |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/okr-setting` | Provides upstream metric framing. |
| `solo/product/product-planning/roadmap-design` | Routes between roadmap formats. |

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
| `draft-outcome-based-roadmaps` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-outcome-based-roadmaps` | haiku | Schema check + threshold checks; deterministic. |
| `review-outcome-based-roadmaps` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/outcome-based-roadmaps.json` | JSON skeleton conforming to the output contract schema. |
| `templates/outcome-based-roadmaps.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-outcome-based-roadmaps.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[outcome-based-roadmaps-advanced]]
- [[okr-setting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/outcome-based-roadmaps.json`

```json
{
  "artefact_id": "outcome-based-roadmaps-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "quarter": "quarter value",
  "outcomes": [
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
