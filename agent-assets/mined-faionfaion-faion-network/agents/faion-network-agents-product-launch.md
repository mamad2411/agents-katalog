# Product Launch

## Summary

**One-sentence:** Coordinated launch plan with positioning, channels, assets, team readiness, and day-of execution — kicks off 6-8 weeks pre-launch and ends with a 30-day post-launch retrospective.

**One-paragraph:** Coordinated launch plan with positioning, channels, assets, team readiness, and day-of execution — kicks off 6-8 weeks pre-launch and ends with a 30-day post-launch retrospective. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Product Launch on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Product or material feature is shippable within 6-8 weeks.
- Target segment + positioning is documented (or being authored now).
- Owner has budget + capacity for channel activation (content, email, ads).
- Success metric (signups, revenue, activation) is named and instrumented.

## Skip If (ANY kills it)

- Silent shipping (internal tool, dark-launch behind flag) — use feature-flag rollout instead.
- Pre-PMF where 'launch' is premature — keep iterating in discovery.
- Compliance / regulator-mandated release with no marketing surface.
- Single-customer enterprise deploy — use account-handoff playbook.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Ship-ready product or feature | build artefact | Engineering |
| Positioning statement | 1-page doc | PM |
| Channel inventory | table (email, social, blog, paid) | Marketing |
| Launch budget + capacity | estimate | Founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/release-planning` | Inputs: release plan + ship date. |
| `solo/product/product-planning/product-discovery` | Inputs: validated positioning + segment. |

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
| `draft-product-launch` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-product-launch` | haiku | Schema check + threshold checks; deterministic. |
| `review-product-launch` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-launch.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-launch.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[release-planning]]
- [[product-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
