---
name: offer-targeting
description: Use when deciding who should see an onsite offer, popup, banner or bar — the audience, the trigger, the frequency, the exclusions, and whether the offer should exist at all. Also use when popups are hurting the experience, when offers are being shown to people who already converted, or when discounting onsite is being considered.
license: MIT
metadata:
  targetbay.display_name: Offer Targeting
  targetbay.version: "2.0.0"
  targetbay.category: onsite
  targetbay.requires: onboarding.store_context, onboarding.consent_and_tracking, onboarding.offers, onboarding.offer_analytics, onboarding.audience_definition, onboarding.visitor_intelligence, onboarding.product_intelligence, onboarding.experience_analytics
  targetbay.composes: surface-inventory
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Offer Targeting

## Purpose

Decide who sees an onsite offer, when, how often, and — first — whether the offer should exist.

Offers are the most intrusive personalization a store runs and the easiest to over-apply. They interrupt,
they compete with each other for the same visitor tolerance, and they frequently discount purchases that
were already happening ([../../rules/targeting-rules.md#T8](../../rules/targeting-rules.md)).

## When to Use

- Designing or revising an onsite offer, popup, banner or bar
- Deciding the audience, trigger and frequency for one
- Popups are suspected of hurting the experience
- Offers are reaching visitors who already converted or already hold the item
- Onsite discounting is being considered and its cost is unclear

## When Not to Use

- The inventory of what currently runs is unknown. Use
  [surface-inventory](../surface-inventory/SKILL.md) — this skill composes it.
- The question is which products to show rather than which offer. Use
  [recommendation-strategy](../recommendation-strategy/SKILL.md).
- The question is about search queries. Use [onsite-search](../onsite-search/SKILL.md).
- The offer needs testing rather than designing. Use
  [experience-experimentation](../experience-experimentation/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent and tracking state | Decides which targeting is permissible | Blocked |
| Current offers, triggers and frequency | What already competes for the same visitor | Blocked |
| Per-offer engagement and dismissal | Whether existing offers are tolerated | Partial |
| Conversion baseline without the offer | Whether the offer is discounting existing demand | Partial; incrementality unassessable |
| Session behaviour signals | Trigger and intent | Partial; triggers become generic |
| Margin posture | What a discount offer costs | Partial; discount offers withheld |
| Audience sizes | Whether a segment can produce a measurable result | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.consent_and_tracking` | Which targeting is permissible, and for which traffic |
| `onboarding.store_context` | Traffic volume, currency, margin posture |
| `onboarding.offers` | Reading current offers; creating or amending them |
| `onboarding.offer_analytics` | Engagement, dismissal, conversion per offer |
| `onboarding.audience_definition` | Segment definitions and sizes; creating them |
| `onboarding.visitor_intelligence` | Session signals for triggers and intent |
| `onboarding.product_intelligence` | Margin and stock behind any product-specific offer |
| `onboarding.experience_analytics` | Conversion baseline the offer is measured against |

## Decision Process

```
1. Read consent; establish permissible targeting
2. Delegate the inventory                     ← what already interrupts this visitor
3. Test whether the offer should exist        ← what does it buy that the default does not
4. Define the audience from the intended difference
5. Define the exclusions first
6. Choose the trigger from session intent
7. Set frequency per visitor across all surfaces
8. State the anonymous path
9. Define the measurement, including the discount cost
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/targeting-rules.md](../../rules/targeting-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/measurement-rules.md](../../rules/measurement-rules.md).

- Read consent first (G19, [#S15](../../rules/safety-rules.md)).
- Ask whether the offer should exist before designing it. An offer shown to visitors who were converting
  anyway is a discount on existing demand, and the baseline says which
  ([#M3](../../rules/measurement-rules.md)).
- Start from the intended difference, not from available attributes (T1). A segment that would see the
  same thing as everyone else should not exist (G21).
- Design exclusions before the audience (T4): already converted, already holds the item, already
  dismissed, in an active flow from another system, out of region.
- Size every segment and say plainly when one is too small to evaluate at this store's volume (T3).
- Never target on a sensitive attribute or a proxy for one (T5,
  [#S16](../../rules/safety-rules.md)). Name the proxy when rejecting.
- Never vary price by visitor under any framing ([#S17](../../rules/safety-rules.md)). Varying which offer
  is shown is merchandising; varying the price of the same item is not.
- The offer carries a dismissal that works and a frequency cap that holds, with no pattern making
  declining harder than accepting ([#S18](../../rules/safety-rules.md)).
- Frequency is per visitor across all surfaces, not per offer (T8). Count the offer against everything else
  already interrupting that visitor.
- Prefer session intent for triggers over historical profile (T6).
- State the anonymous path (T2, G23).
- Define the measurement before the change, and include the discount cost against margin (M1, G24).
- Publishing an offer is `high_impact` — live visitors see it immediately
  ([#S5](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, current offers, performance, baselines, sessions, margin | `read_only` |
| ANALYZE | Test whether the offer earns its interruption; size audiences | `analysis` |
| PLAN | Audience, exclusions, trigger, frequency, anonymous path, measurement | `plan` |
| PREVIEW | State the audience size, traffic share, frequency and discount cost | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves per offer | — |
| EXECUTE | Stage audience and offer configuration | `mutation` |
| EXECUTE | Publish to live traffic | `high_impact` |
| VERIFY | Confirm live configuration matches what was approved | `read_only` |
| MEASURE | Conversion against the baseline, with discount cost counted | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing, per offer: whether it should exist and
on what evidence, the audience with its size and traffic share, the exclusion list, the trigger, the
per-visitor frequency accounting for all other surfaces, the anonymous path, the discount cost against
margin, and the measurement definition.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: current offers as read, the visitor's total interruption count before and after, and offers
considered and rejected with the reason.

## Validation

- [ ] Consent read first; targeting permissibility established (G19, S15)
- [ ] The offer's existence justified against the no-offer baseline (M3)
- [ ] Audience derived from the intended difference, not from available attributes (T1, G21)
- [ ] Exclusions designed and stated (T4)
- [ ] Every segment sized, with unevaluable segments named as such (T3)
- [ ] No sensitive attribute or proxy anywhere in the targeting (T5, S16)
- [ ] No price variation by visitor (S17)
- [ ] Dismissal works and frequency caps hold; no pressure patterns (S18)
- [ ] Frequency counted per visitor across all surfaces (T8)
- [ ] Anonymous path stated (T2, G23)
- [ ] Measurement defined before the change, including discount cost (M1, G24)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the plan | `plan` | None |
| Create a draft audience or staged offer | `mutation` | Preview, then confirm |
| Publish an offer to live traffic | `high_impact` | Explicit, with audience size and traffic share shown |
| Remove an existing offer | `destructive` | Explicit, after reporting what it currently does (S19) |

## Examples

**"Add an exit-intent popup with 10% off."**
The conversion baseline shows exit-intent traffic on the cart page converts substantially on its own, so
the offer would discount purchases already happening. Reports the estimated discount cost against the
incremental conversion it could plausibly add, and recommends restricting the offer to first-time visitors
with no prior session — a smaller audience with a defensible case — while excluding returning visitors who
already convert. Counts the popup against the two interruptions those visitors already receive.

**"Show a free-shipping bar to people likely to abandon."**
Finds the proposed likelihood model draws on browsing signals that act as a proxy for financial
circumstances, and rejects that targeting under T5, naming the proxy. Proposes cart-value-based targeting
instead — a stated, visible threshold that applies to everyone at that cart value — which achieves the
intended effect without profiling anybody.

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.consent_and_tracking` unavailable | **Blocked.** Targeting permissibility cannot be established (S15, G19) |
| `onboarding.offers` unavailable | **Blocked.** Cannot read what already interrupts this visitor (T8) |
| Conversion baseline unavailable | **Partial.** State that the offer's incrementality cannot be assessed and that it may be discounting existing demand |
| Margin unavailable | **Partial.** Withhold discount-bearing offers; propose non-discount alternatives and state why |
| Audience sizes unavailable | **Blocked.** An unsized segment cannot be evaluated or approved (T3, S4) |
| Frequency state not exposed per visitor | **Partial.** State that the cap cannot be honoured across surfaces, and treat that as a reason not to add an interruption (T8) |
| Targeting depends on a sensitive proxy | Refuse that targeting, name the proxy, and propose a non-profiling alternative (T5, S16) |
| Asked to vary price by visitor | Refuse, cite [#S17](../../rules/safety-rules.md), and propose offer-level differentiation instead |

Degraded outcomes set `status` and populate `unmet_requirements`.
