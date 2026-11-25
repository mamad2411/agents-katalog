---
name: review-program-audit
description: Use for an open-ended assessment of a store's whole review and UGC programme — when someone asks what is wrong with our reviews, where to start, what to fix first, or wants a review of the programme without naming a specific problem. Scans collection, ratings, display and distribution together and ranks what is most worth fixing.
license: MIT
metadata:
  targetbay.display_name: Review Programme Audit
  targetbay.version: "2.0.0"
  targetbay.category: planning
  targetbay.requires: reviews.store_profile, reviews.product_coverage, reviews.ratings_analytics, reviews.review_requests, reviews.request_analytics, reviews.display_placement, reviews.ugc_media, reviews.moderation, reviews.syndication
  targetbay.composes: review-coverage, review-request-program, rating-diagnosis, proof-placement
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Review Programme Audit

## Purpose

Look at the whole programme — collection, ratings, display, distribution and moderation — and say what is
most worth fixing first.

The four other skills each answer one question well. This skill exists for the case where nobody knows
which question to ask, and its job is to find out rather than to default to collecting more reviews.

## When to Use

- Open-ended: "what's wrong with our reviews", "where do we start"
- Taking over a programme somebody else set up
- Periodic health check
- A proof investment is being considered and its priority is unclear
- Several problems are suspected and their relative size is unknown

## When Not to Use

- The problem is already identified. Go straight to the owning skill:
  [review-coverage](../review-coverage/SKILL.md),
  [review-request-program](../review-request-program/SKILL.md),
  [rating-diagnosis](../rating-diagnosis/SKILL.md) or
  [proof-placement](../proof-placement/SKILL.md).
- Something needs building or sending. This skill recommends; it never executes.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Catalogue size and programme age | The denominator for everything else | Blocked |
| Per-product coverage | Where proof is missing | Blocked |
| Rating distributions and movement | Whether the proof that exists is healthy | Partial |
| Request configuration and performance | Whether collection is working | Partial |
| Current placements | Whether existing proof is reaching anyone | Partial |
| Media inventory | Whether visual proof exists where it matters | Partial |
| Moderation policy and queue state | Whether moderation is consistent or drifting | Partial |
| Syndication state | Whether distribution is a gap or a non-issue | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `reviews.store_profile` | Catalogue size, vertical, programme age |
| `reviews.product_coverage` | Coverage dimension |
| `reviews.ratings_analytics` | Rating health dimension |
| `reviews.review_requests` / `reviews.request_analytics` | Collection dimension |
| `reviews.display_placement` | Display dimension |
| `reviews.ugc_media` | Media dimension |
| `reviews.moderation` | Moderation consistency dimension |
| `reviews.syndication` | Distribution dimension |

## Decision Process

```
1. Size the programme against the catalogue   ← coverage as a proportion, not a count
2. Assess each dimension independently        ← collection, ratings, display, media, moderation, distribution
3. Find the binding constraint                ← which one caps the value of fixing the others
4. Size each gap in outcome terms
5. Rank by value against effort
6. Route each finding to its owning skill
7. State what is healthy and needs nothing
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md), and every domain rule file through
the skills this one composes.

- Find the binding constraint before ranking. Collecting more reviews for a store whose proof is displayed
  nowhere moves nothing; fixing display first changes what collection is worth
  ([../../knowledge/social-proof-principles.md](../../knowledge/social-proof-principles.md)).
- Assess coverage as a proportion of the catalogue, never as a total (G5). A store with 10,000 reviews
  across 200 covered products out of 3,000 has a coverage problem that the total conceals.
- Do not default to "collect more." It is the most common recommendation and frequently the wrong one.
- A falling rating outranks a coverage gap, because volume does not fix a cause
  ([../../rules/response-rules.md#P8](../../rules/response-rules.md)).
- Report healthy dimensions explicitly. An audit that lists only problems cannot be checked for
  completeness, and creates pressure to change what is working.
- Route every finding to the skill that owns it, rather than restating that skill's reasoning here (G14).
- Rank by value against effort, and state the evidence for both (G2). Where value cannot be sized, say so
  and rank on reasoning with lower confidence (G15).
- Never recommend an action this skill would execute. `recommend_only` is the ceiling; the owning skills
  carry the approval requirements.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read every dimension's current state | `read_only` |
| ANALYZE | Assess each dimension; identify the binding constraint | `analysis` |
| PLAN | Size and rank the findings | `recommendation` |
| PREVIEW | Present the ranked findings with their evidence and owning skills | `recommendation` |
| VALIDATE | Run the checks below | — |
| MEASURE | Re-audit after the top findings have been acted on | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: a per-dimension assessment with its
evidence, the binding constraint named explicitly, and a ranked list of findings.

Each finding states what is wrong, the evidence, the estimated value of fixing it, the effort, the owning
skill, and its dependencies on other findings. Recommendations conform to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: the dimensions assessed as healthy, and anything that could not be assessed.

## Validation

- [ ] Every dimension assessed or explicitly reported as unassessable (G15)
- [ ] Coverage stated as a proportion of the catalogue, not a total (G5)
- [ ] Binding constraint named, with the reasoning for why it binds
- [ ] Each finding routed to exactly one owning skill
- [ ] Healthy dimensions reported, not omitted
- [ ] Ranking states value and effort evidence, or declares the confidence is low (G2)
- [ ] No recommendation restates the owning skill's reasoning (G14)
- [ ] No action executed or proposed for execution from this skill

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend and rank | `recommendation` | None |

Every recommendation this skill makes is carried out by a composed skill, under that skill's own
approval requirements.

## Examples

**"Take a look at our reviews and tell us what to do."**
Coverage is thin in proportion but the binding constraint turns out to be display: existing proof sits
below the fold on every template, so the reviews already collected are doing almost nothing. Ranks
placement first, collection second, and notes that fixing collection first would have raised the cost of
the programme without changing conversion. Reports moderation and distribution as healthy.

**"We're about to launch 300 new products — is our review programme ready?"**
Finds the request programme has no trigger that catches products added after it was configured, so new
products acquire proof only by accident. Names that as the binding constraint for the launch, ranks it
above the existing coverage backlog, and routes it to
[review-request-program](../review-request-program/SKILL.md).

## Failure Handling

| Situation | Response |
|---|---|
| `reviews.product_coverage` or `reviews.store_profile` unavailable | **Blocked.** There is no audit without the catalogue and its coverage |
| One or more dimensions unreadable | **Partial.** Audit the rest, name the unassessed dimensions explicitly, and lower the ranking confidence |
| Programme too new to show movement | Report programme age as the finding; assess structure rather than performance |
| Every dimension healthy | Report that, with the evidence. "Nothing is worth changing" is a valid audit result |
| Findings cannot be sized in outcome terms | Rank on reasoning, mark confidence low, and state what data would make sizing possible (G15) |
| Scope resolves to too little to assess | Report it rather than producing a thin audit presented as complete |

Degraded outcomes set `status` and populate `unmet_requirements`.
