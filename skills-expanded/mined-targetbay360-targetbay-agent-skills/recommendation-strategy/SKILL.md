---
name: recommendation-strategy
description: Use when deciding which product recommendations belong on which surface, which strategy should drive them, what must be excluded, and what a placement is actually worth. Also use when a recommendation widget shows irrelevant products, when engagement is high but revenue is not, or when a new placement is being considered.
license: MIT
metadata:
  targetbay.display_name: Recommendation Strategy
  targetbay.version: "2.0.0"
  targetbay.category: merchandising
  targetbay.requires: onboarding.store_context, onboarding.consent_and_tracking, onboarding.recommendation_placement, onboarding.recommendation_analytics, onboarding.product_intelligence, onboarding.visitor_intelligence, onboarding.experience_analytics
  targetbay.composes: surface-inventory
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Recommendation Strategy

## Purpose

Decide what to recommend, where, and to whom — and what the placement is worth once cannibalisation is
accounted for.

The strategy follows from the decision the surface hosts, not from whichever algorithm is available
([../../rules/surface-rules.md#U3](../../rules/surface-rules.md)). A product page hosts a substitution or
complement decision; a cart hosts a completion decision; a category page hosts a narrowing decision. These
want different things.

## When to Use

- Choosing or changing the strategy behind a placement
- A widget shows products that are already in the cart, out of stock or recently bought
- Engagement on a placement is high and revenue effect is not
- Deciding whether a new placement is worth adding
- Deciding what an anonymous visitor sees on a personalised surface

## When Not to Use

- The inventory of what currently runs is unknown. Use
  [surface-inventory](../surface-inventory/SKILL.md) — this skill composes it.
- The question is about an offer or a popup rather than products. Use
  [offer-targeting](../offer-targeting/SKILL.md).
- The question is about search results and queries. Use
  [onsite-search](../onsite-search/SKILL.md).
- The change needs testing rather than deciding. Use
  [experience-experimentation](../experience-experimentation/SKILL.md), which this skill hands off to.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent and tracking state | Decides which strategies are permissible at all | Blocked |
| Current placements and strategies | What already runs, and what a change displaces | Blocked |
| Per-placement performance | Whether a strategy is earning anything | Partial; value unassessable |
| Product affinity and co-purchase data | The substance behind any strategy | Blocked |
| Inventory and margin posture | What should not be recommended, and what is worth promoting | Partial |
| Session behaviour signals | The anonymous path | Partial; anonymous path becomes generic |
| Page performance baselines | The comparison for incrementality | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.consent_and_tracking` | Which strategies are permissible, and for which traffic |
| `onboarding.store_context` | Catalogue size, traffic volume, vertical |
| `onboarding.recommendation_placement` | Reading current placements; creating or amending them |
| `onboarding.recommendation_analytics` | Impressions, clicks, attributed revenue, cannibalisation signals |
| `onboarding.product_intelligence` | Affinity, co-purchase, categories, price bands, margin, stock |
| `onboarding.visitor_intelligence` | Session signals for the anonymous path |
| `onboarding.experience_analytics` | Page baselines the placement is measured against |

## Decision Process

```
1. Read consent; establish permissible strategies
2. Delegate the inventory                      ← surface-inventory maps what exists
3. Name the decision the surface hosts
4. Choose the strategy from the decision       ← not from the algorithm menu
5. Design the exclusions                       ← before anything else about the widget
6. Design the anonymous path explicitly
7. Design the empty state
8. State what the placement displaces
9. Define the measurement, including cannibalisation
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/surface-rules.md](../../rules/surface-rules.md),
[../../rules/targeting-rules.md](../../rules/targeting-rules.md),
[../../rules/measurement-rules.md](../../rules/measurement-rules.md).

- Read consent first; a strategy requiring visitor history is not available for traffic that has not
  granted it (G19, [#S15](../../rules/safety-rules.md)).
- Match the strategy to the surface's decision, not to the catalogue or the available algorithm (U3).
- Design exclusions before the strategy (U4). Items in the cart, recently purchased, and out of stock are
  excluded at design time — this is the most visible failure mode there is
  ([../../knowledge/personalization-principles.md](../../knowledge/personalization-principles.md)).
- State the anonymous path explicitly and design it (T2, G23). It is the majority path.
- Prefer session intent over historical profile for anonymous traffic (T6).
- Design the empty state: what shows when the strategy returns too few results or stock is thin (U6).
- State what a new placement displaces (U2, G20).
- Check cannibalisation before claiming incremental revenue (U5, M3). A placement that moved a purchase
  between products has not added any.
- Evaluate on outcome, not impressions (U7, G17).
- Do not replace a well-performing default with an unproven variant (T7); route the comparison through
  [experience-experimentation](../experience-experimentation/SKILL.md) where the traffic supports it (M5).
- Prefer the simplest mechanism that produces the result (G22). A rules-based placement that fails visibly
  is preferable to a model that fails quietly and cannot be explained.
- Publishing a placement is `high_impact` — live visitors see it immediately
  ([#S5](../../rules/safety-rules.md), [#S4](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, placements, performance, affinity, inventory, sessions | `read_only` |
| ANALYZE | Name surface decisions; assess current strategies; find cannibalisation | `analysis` |
| PLAN | Strategy, exclusions, anonymous path, empty state, displacement | `plan` |
| PREVIEW | State each change, the traffic it reaches, and its measurement | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves per surface | — |
| EXECUTE | Stage placement configuration | `mutation` |
| EXECUTE | Publish to live traffic | `high_impact` |
| VERIFY | Confirm live configuration matches what was approved | `read_only` |
| MEASURE | Outcome against non-carrying pages, with cannibalisation checked | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing, per placement: the surface, the
decision it hosts, the chosen strategy and why that strategy follows from that decision, the exclusion
list, the anonymous path, the empty state, what it displaces, and the measurement definition including how
cannibalisation will be checked.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: current strategies as read, and placements considered and rejected with the reason.

## Validation

- [ ] Consent read first; permissible strategies established (G19, S15)
- [ ] Every placement's surface decision named, and the strategy derived from it (U3)
- [ ] Exclusions designed, covering cart, recent purchase and stock (U4)
- [ ] Anonymous path designed, not inherited as a fallback (T2, G23)
- [ ] Empty state specified (U6)
- [ ] Displacement stated for every addition (U2, G20)
- [ ] Cannibalisation check defined before any incrementality claim (U5, M3)
- [ ] Measurement stated in outcome terms with metric, comparison and horizon (M1, U7)
- [ ] Well-performing defaults not replaced without a test where traffic supports one (T7, M5)
- [ ] Publication treated as `high_impact` with reached traffic stated (S5, S4)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the plan | `plan` | None |
| Stage placement configuration | `mutation` | Preview, then confirm |
| Publish to live traffic | `high_impact` | Explicit, per surface, with traffic share shown |
| Remove an existing placement | `destructive` | Explicit, after reporting what it currently carries (S19) |

## Examples

**"Our 'you may also like' widget recommends things people just bought."**
The placement runs a store-wide bestseller strategy with no exclusions. Redesigns exclusions first — cart
contents, recent purchases, out-of-stock — then replaces the strategy with a complement strategy, because
the product page hosts a complement decision rather than a popularity one (U3). Specifies the empty state
for thin-affinity products, and defines the measurement as add-to-cart on carrying templates against
non-carrying ones.

**"The homepage carousel is our best-performing placement — can we add more like it?"**
Attributed revenue is high, but the cannibalisation check shows most of it is demand that would have
reached the same products through the navigation. Reports the placement as high-attribution and
low-incremental, declines to replicate it, and identifies the cart surface — which hosts a real completion
decision and carries nothing — as the better addition.

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.consent_and_tracking` unavailable | **Blocked.** Strategy permissibility cannot be established (S15, G19) |
| `onboarding.product_intelligence` unavailable | **Blocked.** There is no strategy without affinity or catalogue data |
| Inventory state unavailable | **Partial.** Design exclusions for cart and recent purchase; state that out-of-stock exclusion cannot be guaranteed (U4) |
| Per-placement analytics unavailable | **Partial.** Recommend on reasoning; state that current placement value is unmeasured |
| Cannibalisation not observable | Report attribution only, and state explicitly that no incrementality claim can be made (U5, M3) |
| Session signals unavailable | **Partial.** The anonymous path degrades to a contextual default; say so rather than leaving it implicit (T2) |
| Traffic too low to test a replacement | State it; recommend on reasoning with lower confidence rather than running an underpowered test (M5) |

Degraded outcomes set `status` and populate `unmet_requirements`.
