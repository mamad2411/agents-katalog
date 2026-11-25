---
name: review-coverage
description: Use when the question is where a store is short of social proof — which products, categories or price bands carry no reviews, too few, stale ones, or no photos — and what that absence is costing. This is the targeting skill every other review skill routes through; use it before planning requests, placements or a rating response, and whenever someone asks "which products need reviews."
license: MIT
metadata:
  targetbay.display_name: Review Coverage
  targetbay.version: "2.0.0"
  targetbay.category: proof
  targetbay.requires: reviews.store_profile, reviews.product_coverage, reviews.ratings_analytics, reviews.ugc_media
  targetbay.risk_level: analysis
  targetbay.execution_mode: analyze_only
  targetbay.status: foundation
---

# Review Coverage

## Purpose

Locate where this store is missing proof, and rank the gaps by what closing them is worth.

Every other skill in this plugin needs the same answer: which products matter and which are unproven.
Deriving it once, here, is what keeps the four skills that compose it from inventing four different
definitions of "needs reviews" ([../../rules/global-rules.md#G5](../../rules/global-rules.md)).

## When to Use

- Deciding which products to request reviews for next
- A product page converts badly and proof is a candidate explanation
- The catalogue has grown and nobody knows what the new products carry
- Before planning placements, so the placement plan knows what there is to place
- Any question of the form "which products need reviews"

## When Not to Use

- The rating is falling and the question is why. Use
  [rating-diagnosis](../rating-diagnosis/SKILL.md).
- The gap is already known and the question is how to ask. Use
  [review-request-program](../review-request-program/SKILL.md).
- The question is where existing proof should appear. Use
  [proof-placement](../proof-placement/SKILL.md).
- The whole programme needs assessing, not one dimension. Use
  [review-program-audit](../review-program-audit/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Per-product review count and rating | The gap itself | Blocked |
| Product traffic or order volume | Separates a gap that costs money from one that does not | Partial; ranking becomes weak |
| Review recency per product | Stale proof reads as a discontinued product | Partial |
| Media presence per product | Visual categories need photographs, not text | Partial |
| Catalogue structure — category, price band | Lets the gap be described as a pattern, not a list | Partial |
| Rating distribution | Distinguishes thin proof from bad proof | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `reviews.store_profile` | Catalogue size, vertical, programme age — the denominator |
| `reviews.product_coverage` | Per-product counts, ratings, recency, media presence |
| `reviews.ratings_analytics` | Distribution behind each average, and its movement |
| `reviews.ugc_media` | Which products have photographs and which have none |

## Decision Process

```
1. Size the catalogue and the programme        ← what exists, how long it has been running
2. Measure coverage per product                ← count, rating, recency, media
3. Weight each product by exposure             ← traffic or orders; an unseen gap costs nothing
4. Classify the gap type                       ← none / thin / stale / text-only / contested
5. Look for the pattern                        ← is it new products, a category, a price band, a supplier
6. Size what closing each gap is worth
7. Rank, and state what was deliberately left alone
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/placement-rules.md](../../rules/placement-rules.md).

- Coverage is per product; a store average is not an answer (G5).
- Rank by exposure, not by catalogue position. A gap on a product nobody views is not a gap worth money.
- Distinguish the five gap types, because they have different fixes: **none** needs a request, **thin**
  needs volume, **stale** needs velocity, **text-only** needs a media ask
  ([../../rules/request-rules.md#R8](../../rules/request-rules.md)), **contested** — proof exists but is
  mixed — is a [rating-diagnosis](../rating-diagnosis/SKILL.md) problem, not a coverage one.
- Read the distribution, never the average alone (G4).
- Describe the gap as a pattern where one exists. "Everything added since the catalogue expansion" is
  actionable; a list of two hundred product identifiers is not.
- Do not assert what a review count "should" be. Derive the store's own relationship between coverage and
  conversion where the data supports it, and say so where it does not (G3).
- A product with no traffic and no reviews is a merchandising finding, not a proof finding. Report it as
  such rather than queuing it for outreach.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read catalogue, per-product coverage, media, distributions | `read_only` |
| ANALYZE | Weight by exposure, classify gap type, find the pattern | `analysis` |
| PLAN | Rank gaps and size them | `analysis` |
| PREVIEW | Present the ranked gap map with its evidence | `analysis` |
| VALIDATE | Run the checks below | — |
| MEASURE | Re-read coverage after outreach has had a full request cycle | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing a ranked coverage map: per gap, the
products or pattern it covers, the gap type, the exposure behind it, what closing it is estimated to be
worth and on what evidence, and the skill that owns the fix.

Plus: the store's coverage distribution, the pattern behind the gap where one was found, and what was
examined and deliberately not flagged.

No recommendations to act are produced here — this skill is `analyze_only`, and the acting skills compose
it.

## Validation

- [ ] Coverage measured per product from store data, not assumed (G3, G5)
- [ ] Every gap weighted by actual exposure, not catalogue position
- [ ] Gap type classified for every entry, and the type implies the owning skill
- [ ] Distribution read, not just the average (G4)
- [ ] Pattern stated where one exists, or its absence stated explicitly
- [ ] Products excluded by `constraints` listed, not silently dropped
- [ ] Any capability that was unavailable recorded in `unmet_requirements` (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |

Every action this skill implies is owned by a composing skill, which carries its own approval
requirements.

## Examples

**"Which products need reviews?"**
Finds that coverage is healthy across the original catalogue and absent across everything added in the
last two seasonal ranges — a pattern, not a list. Ranks by page views, notes that a third of the gap sits
on products with no traffic either, and separates those out as a merchandising question rather than a
proof one. Hands the remainder to
[review-request-program](../review-request-program/SKILL.md).

**"Our best-selling category converts worse than the rest of the site."**
Coverage in that category is not thin — it is stale, with the most recent review predating a supplier
change. Classifies the gap as `stale` rather than `none`, which changes the fix from a backlog request to
sustained velocity, and flags that reviews written before the change may describe a different product.

## Failure Handling

| Situation | Response |
|---|---|
| `reviews.product_coverage` unavailable | **Blocked.** There is no coverage analysis without per-product data |
| No traffic or order data per product | **Partial.** Report gaps unranked, state that exposure weighting was not possible, lower confidence |
| `reviews.ugc_media` unavailable | **Partial.** Report text coverage only; do not infer media presence |
| Catalogue too new for recency to mean anything | Report programme age as the finding; recency classification is withheld rather than guessed |
| Distribution unavailable, only averages | **Partial.** Flag every average as unverified against its distribution (G4) |
| Scope resolves to no products | Report it. An empty scope is a finding about the scope, not a coverage result |

Degraded outcomes set `status` and populate `unmet_requirements`.
