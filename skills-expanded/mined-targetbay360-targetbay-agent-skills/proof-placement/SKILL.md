---
name: proof-placement
description: Use when reviews and UGC exist but are not working — deciding where proof should appear on the site, which proof belongs on which page, whether to add badges, carousels or galleries, and whether existing photo and video can be reused in email, ads or social. Also use when a placement was added and nothing changed.
license: MIT
metadata:
  targetbay.display_name: Proof Placement
  targetbay.version: "2.0.0"
  targetbay.category: display
  targetbay.requires: reviews.store_profile, reviews.product_coverage, reviews.review_content, reviews.ratings_analytics, reviews.ugc_media, reviews.display_placement, reviews.syndication
  targetbay.composes: review-coverage
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Proof Placement

## Purpose

Decide where proof earns its place, which proof to show there, and what a placement is actually worth.

A store can have healthy coverage and get nothing from it, because proof only compounds where it is seen
([../../knowledge/social-proof-principles.md](../../knowledge/social-proof-principles.md)). This skill
treats display and distribution as a separate problem from collection.

## When to Use

- Reviews exist but conversion has not moved
- Deciding which product-page widgets, carousels, badges or galleries to run
- Photo and video have accumulated and nobody is using them
- Considering reuse of UGC in email, ads or social
- Considering syndication beyond the store
- A placement was added and its effect is unknown

## When Not to Use

- There is no proof to place. Use [review-coverage](../review-coverage/SKILL.md), then
  [review-request-program](../review-request-program/SKILL.md).
- The proof that exists is bad and the rating is falling. Use
  [rating-diagnosis](../rating-diagnosis/SKILL.md).
- The question is the whole programme's health. Use
  [review-program-audit](../review-program-audit/SKILL.md).
- The change being considered is a general onsite personalisation decision rather than a proof one — that
  belongs to the onsite skills in
  [targetbay-onboarding](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-onboarding/skills/README.md),
  not here.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Current placements and their configuration | What already runs, and what a new placement displaces | Blocked |
| Per-product coverage and distribution | Whether a page has proof worth showing | Blocked |
| Media inventory and rights status | Whether UGC may be reused at all | Partial; reuse withheld |
| Review text | Which attributes the proof actually addresses | Partial |
| Page performance by surface | What a placement is worth, and against what baseline | Partial; effect unsizable |
| Syndication state | Whether distribution already exists elsewhere | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `reviews.store_profile` | Catalogue and vertical context for what proof matters here |
| `reviews.product_coverage` | Whether a page has its own proof or none |
| `reviews.review_content` | Which attributes the available proof speaks to |
| `reviews.ratings_analytics` | Count and distribution behind any aggregate shown |
| `reviews.ugc_media` | Media inventory, moderation state and rights status |
| `reviews.display_placement` | Reading current placements; creating or amending them |
| `reviews.syndication` | Current distribution state; enabling or changing it |

## Decision Process

```
1. Read current placements                    ← what is already shown, and where
2. Delegate coverage                          ← review-coverage says which pages have proof
3. Map each surface to the decision it hosts  ← where does hesitation actually occur
4. Match available proof to the live doubt    ← the attribute, not the star count
5. Decide what a new placement displaces      ← space is finite
6. Check rights before planning any reuse
7. Decide distribution separately from display
8. Define the measurement before proposing the change
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/placement-rules.md](../../rules/placement-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Place proof where the decision is made, not where there is space (D1).
- Show product-specific proof where it exists; decide deliberately what to show where it does not (D2).
  "Show nothing yet" is a legitimate answer for an unproven product.
- Never display an aggregate that the distribution does not support — a star average without its count
  overstates thin evidence and is a misrepresentation (D3, [#S2](../../rules/safety-rules.md)).
- Reuse requires confirmed rights and attribution (D4). Unknown rights means not yet.
- Every new placement states what it displaces, or why the page genuinely had room (D6).
- A placement is evaluated on conversion, add-to-cart or return-rate movement, never on impressions (D5).
  Define that measurement before proposing the change, not after.
- Match the proof to the doubt the page raises. A carousel of five-star text on a page whose reviews all
  discuss sizing answers the wrong question (G1).
- Enabling syndication is `high_impact`: it publishes store content to third parties and is hard to
  retract. Approve it explicitly, on the specific destination
  ([#S5](../../rules/safety-rules.md), [#S7](../../rules/safety-rules.md)).
- Do not propose a placement whose value cannot be measured; say what would make it measurable instead.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read placements, coverage, media, rights, surface performance | `read_only` |
| ANALYZE | Map surfaces to decisions; match proof to doubts; find the gaps | `analysis` |
| PLAN | Choose placements, displacements, reuse and distribution | `recommendation` |
| PREVIEW | State each change, its surface, what it displaces, and its measurement | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves; syndication approved separately per destination | — |
| EXECUTE | Create or amend placements | `mutation` |
| EXECUTE | Enable syndication or publish reused UGC | `high_impact` |
| VERIFY | Confirm what is live matches what was approved | `read_only` |
| MEASURE | Compare carrying pages against non-carrying pages over the defined window | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing, per proposed placement: the surface,
the decision it sits in front of, which proof it shows and why that proof matches the doubt, what it
displaces, its risk class, and the measurement that will decide whether it stays.

Separately: a reuse plan covering only media with confirmed rights, and a distribution recommendation
treated as its own decision.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: current placements as read, and placements considered and rejected with the reason.

## Validation

- [ ] Current placements read before any addition is proposed
- [ ] Every placement sits in front of a stated decision (D1)
- [ ] Product-level proof preferred where it exists; the fallback stated deliberately (D2)
- [ ] No aggregate displayed without the count and distribution behind it (D3, S2)
- [ ] Rights confirmed for every item in the reuse plan; unknown rights excluded (D4)
- [ ] Every addition states what it displaces (D6)
- [ ] Measurement defined before the change, in outcome terms not impressions (D5)
- [ ] Syndication proposed as a separate, explicitly approved decision per destination
- [ ] Any placement whose effect cannot be measured flagged as such

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend placements | `recommendation` | None |
| Create or amend a placement | `mutation` | Preview, then confirm |
| Publish reused UGC outside the store | `high_impact` | Explicit, per asset set |
| Enable or change syndication | `high_impact` | Explicit, per destination |
| Remove an existing placement | `destructive` | Explicit, after reporting what it currently carries (S8) |

## Examples

**"We have 4,000 reviews and conversion hasn't moved."**
Finds proof is displayed only in a tab below the fold, on a template where the hesitation happens at the
size selector. Recommends surfacing the sizing-related review attributes next to that selector, states
what moves down to make room, and defines the measurement as conversion on carrying templates against
non-carrying ones — not widget impressions. Rejects adding a homepage carousel as decoration under D1.

**"Can we put customer photos in our next email campaign?"**
Inventories media and finds rights status confirmed for a minority of it. Plans reuse from that subset
only, excludes the rest pending rights, and notes which products have visual doubts worth answering with
photographs — handing the collection gap back to
[review-request-program](../review-request-program/SKILL.md) as a media ask.

## Failure Handling

| Situation | Response |
|---|---|
| `reviews.display_placement` unavailable | **Blocked.** Cannot read what is shown; proposing placements blind risks duplicating them |
| Coverage unavailable | **Blocked.** Composed skill blocked; no basis for what a page can show |
| Page performance unavailable | **Partial.** Recommend placements on reasoning, state that value cannot be sized, and define the measurement to enable later |
| Rights status unknown for all media | **Partial.** Withhold the entire reuse plan (D4); report the rights gap as the finding |
| `reviews.syndication` unavailable | **Partial.** Report distribution as unverified for this store and plan onsite only |
| A surface has proof but no traffic | Report as a merchandising finding, not a placement one |
| Asked to show an average on a product with very few reviews | Refuse the aggregate, propose showing the reviews themselves with their count (D3, S2) |

Degraded outcomes set `status` and populate `unmet_requirements`.
