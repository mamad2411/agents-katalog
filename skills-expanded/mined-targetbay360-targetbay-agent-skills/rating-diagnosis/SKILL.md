---
name: rating-diagnosis
description: Use when a rating is falling, a product is attracting low ratings, negative reviews are clustering around a theme, or someone asks why a score dropped and what to do about it. Produces the cause and a response, including which reviews warrant a public reply. Use before any plan that tries to raise a rating.
license: MIT
metadata:
  targetbay.display_name: Rating Diagnosis
  targetbay.version: "2.0.0"
  targetbay.category: moderation
  targetbay.requires: reviews.store_profile, reviews.review_content, reviews.ratings_analytics, reviews.product_coverage, reviews.review_replies, reviews.order_intelligence
  targetbay.composes: review-coverage
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Rating Diagnosis

## Purpose

Find out why a rating moved, and decide what to do about the cause rather than about the number.

A falling rating is a symptom with several possible causes — a product change, a fulfilment change, a
listing that promises the wrong thing, a supplier swap, or a genuine quality problem. Responding before
the cause is known produces public apologies for the wrong thing
([../../rules/response-rules.md#P1](../../rules/response-rules.md)).

## When to Use

- A store or product rating is drifting down
- Low ratings are clustering on one product, category or period
- The same complaint keeps recurring in review text
- A reply strategy is needed and nobody knows what to reply to
- Someone proposes raising a rating with volume and the cause is unknown

## When Not to Use

- The product has no reviews at all. That is coverage; use
  [review-coverage](../review-coverage/SKILL.md).
- The rating is fine and the goal is more reviews. Use
  [review-request-program](../review-request-program/SKILL.md).
- Proof exists and is good but is not being shown. Use
  [proof-placement](../proof-placement/SKILL.md).
- The whole programme needs assessing. Use
  [review-program-audit](../review-program-audit/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Rating distribution over time | A rating is a distribution, not a number | Blocked |
| Review text for the affected products | The cause lives in the text, not the score | Blocked |
| Period boundaries of the movement | Locates what changed just before it | Partial; cause becomes speculative |
| Product and order context | Separates product problems from fulfilment problems | Partial |
| Existing replies | What has already been said publicly | Partial |
| Verified-buyer state | Distinguishes customer experience from other traffic | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `reviews.store_profile` | Vertical and catalogue context for interpreting the movement |
| `reviews.review_content` | The text, rating, date, product and verified state of each review |
| `reviews.ratings_analytics` | Distribution and its movement across periods |
| `reviews.product_coverage` | Whether the affected products are thinly or well covered |
| `reviews.review_replies` | What has already been replied to, and how |
| `reviews.order_intelligence` | Fulfilment and return signals that separate product from delivery causes |

## Decision Process

```
1. Establish the baseline distribution        ← what was normal here
2. Locate the movement in time and product    ← which products, which weeks
3. Read the low-rating text                   ← what do they actually say
4. Extract the recurring attribute            ← the subject, not the sentiment
5. Correlate with what changed                ← supplier, listing, fulfilment, price, packaging
6. Classify the cause                         ← product / fulfilment / expectation / isolated
7. Decide the response per class              ← fix, listing change, reply, or nothing
8. Select the individual reviews worth a reply
9. Draft replies for human review, never for direct publication
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/response-rules.md](../../rules/response-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Diagnose before responding (P1). A response plan without a cause is rejected.
- Read the distribution, never the average alone (G4).
- Reply to the pattern, not to every review (P2). Reply count is not an outcome.
- A recurring attribute across reviews of one product is a product, listing or fulfilment finding, and is
  surfaced as such rather than answered thirty times (P7).
- Never dispute the customer's experience; the reply is written for the next reader (P4).
- Never propose suppressing, rejecting or deleting a truthful review to protect a rating
  ([#S4](../../rules/safety-rules.md)). Moderation is proposed only on a stated policy ground.
- Never offer anything in exchange for a review being changed or removed (P6,
  [#S3](../../rules/safety-rules.md)).
- Do not propose volume as a rating fix on its own (P8). Where volume is part of the plan, state the
  arithmetic — how many reviews at what rating move the average how far — rather than asserting recovery.
- Every reply is drafted for a human to read and approve individually (P3,
  [#S5](../../rules/safety-rules.md), [#S10](../../rules/safety-rules.md)).
- A cause that cannot be established from evidence is reported as unknown, with the candidates ranked and
  the evidence that would distinguish them (G2, G15).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read distributions, review text, replies, order and return signals | `read_only` |
| ANALYZE | Baseline, locate movement, extract attributes, correlate with changes | `analysis` |
| PLAN | Classify cause; decide response per class; select reviews for reply | `recommendation` |
| PREVIEW | Present cause, evidence, proposed responses and draft reply text | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves each reply on its own text | — |
| EXECUTE | Publish approved replies | `high_impact` |
| VERIFY | Confirm published text matches approved text | `read_only` |
| MEASURE | Re-read the distribution after enough new orders to be meaningful | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) stating: the baseline, the movement with its
period and products, the recurring attributes found in the text with their frequency, the classified
cause with its evidence and confidence, and the response plan.

The response plan separates: findings routed out of the review system entirely (product, listing,
fulfilment), reviews selected for a public reply with draft text, and anything explicitly not worth
responding to.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

## Validation

- [ ] Baseline established before the movement is called a movement (G2)
- [ ] Distribution read, not the average (G4, P1)
- [ ] Attributes extracted from actual review text, never paraphrased from memory (G3)
- [ ] Cause classified, with evidence, or explicitly reported as unknown with ranked candidates
- [ ] Product, listing and fulfilment findings routed out of the reply plan (P7)
- [ ] No moderation proposed on rating grounds (S4)
- [ ] No incentive tied to review content anywhere in the plan (P6, S3)
- [ ] Volume-based recovery, if proposed, carries its arithmetic (P8)
- [ ] Each reply drafted as reviewable text and approved individually (P3, S10)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Diagnose and recommend | `recommendation` | None |
| Publish a merchant reply | `high_impact` | Explicit, per reply, on the exact text |
| Reject or unpublish a review | `destructive` | Explicit, after inspection, on a stated policy ground (S8) |

## Examples

**"Our rating dropped from 4.6 to 4.1 — fix it."**
Baseline shows the drop is confined to one product line and one eight-week window. Review text clusters on
a single attribute — the item arriving damaged — and return data corroborates it. Classifies the cause as
fulfilment, routes it to packaging as a finding, proposes replies on the four reviews that describe the
problem most clearly, and explicitly rejects a proposal to raise the average with new requests, showing
the arithmetic of how little that would move.

**"Should we reply to all our negative reviews?"**
Finds most one-star reviews are isolated and unrelated. Recommends replying to the three that share a
recurring, correctable misunderstanding about a specification, and not to the rest — because the reply
exists for the next reader, and thirty near-identical apologies read worse than none.

## Failure Handling

| Situation | Response |
|---|---|
| `reviews.review_content` unavailable | **Blocked.** A rating cannot be diagnosed from scores alone |
| `reviews.ratings_analytics` unavailable | **Blocked.** No distribution, no baseline (G4) |
| Too few reviews in the window | **Partial.** Report that the movement is not distinguishable from noise, and say what volume would be |
| Order and return data unavailable | **Partial.** Product and fulfilment causes cannot be separated; report both as candidates |
| Cause not establishable | Report it as unknown with ranked candidates and the evidence that would decide (G15). Do not respond publicly to a guess |
| `reviews.review_replies` unavailable | **Partial.** Diagnose and recommend; state that replies must be published by hand |
| Asked to remove negative reviews | Refuse, cite [#S4](../../rules/safety-rules.md), and produce the diagnosis instead |

Degraded outcomes set `status` and populate `unmet_requirements`.
