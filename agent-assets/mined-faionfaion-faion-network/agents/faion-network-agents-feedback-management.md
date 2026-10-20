# Feedback Management

## Summary

**One-sentence:** Capture user feedback through a single inbound channel, triage daily, classify by theme + severity, close the loop with the user, and feed verified themes into the roadmap.

**One-paragraph:** Operational pipeline: capture → triage → classify → close-the-loop → roadmap-feed. Daily triage prevents the inbox from rotting; theme classification turns anecdote into signal; explicit close-the-loop keeps the channel trusted so feedback keeps coming.

**Ефективно для:**

- Solo founder receiving feedback through 5 channels (email, X, Discord, support, in-app); needs a single funnel that turns chatter into prioritised themes without dropping anyone.

## Applies If (ALL must hold)

- Product has ≥1 active user channel receiving feedback.
- Volume ≥3 messages/week — high enough to need a system.
- Founder commits ≥30 min/day to triage.

## Skip If (ANY kills it)

- Pre-launch phase with no users.
- Established support team handling triage already.
- Founder cannot commit any daily triage time.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inbound channels list | list | Ops doc |
| Theme taxonomy (seed list) | list | PM doc |
| Daily triage slot in calendar | calendar event | Calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/product-analytics` | Quant signal that triangulates qual themes. |
| `solo/product/product-manager/roadmap-design` | Where verified themes land downstream. |

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
| `draft-feedback-management` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-feedback-management` | haiku | Schema check + threshold checks; deterministic. |
| `review-feedback-management` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feedback-management.json` | JSON skeleton conforming to the output contract schema. |
| `templates/feedback-management.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feedback-management.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-analytics]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feedback-management.json`

```json
{
  "artefact_id": "feedback-management-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "inbound_channels": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "triage_cadence": "triage_cadence value",
  "theme_taxonomy": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "close_loop_sla_days": 3,
  "owner": "@solo-founder"
}
```
