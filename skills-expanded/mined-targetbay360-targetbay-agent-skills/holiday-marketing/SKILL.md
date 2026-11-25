---
name: holiday-marketing
description: Use when deciding whether and how a store should participate in a holiday, festival or seasonal event — establishing relevance to this specific store, which products and audiences it applies to, what the strategy and timeline should be, and whether it is worth doing at all. Hand to holiday-drip-campaign to build the message sequence once the strategy is set.
license: MIT
metadata:
  targetbay.display_name: Holiday Marketing
  targetbay.version: "2.0.0"
  targetbay.category: seasonal
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_analytics, email_sms.marketing_calendar
  targetbay.composes: audience-discovery, holiday-drip-campaign
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Holiday Marketing

## Purpose

Decide whether a holiday matters to this store, and if it does, what the store should do about it.

The most valuable output of this skill is sometimes "not this one." Participating in every holiday on a
generic calendar produces a fatigued list and a stream of irrelevant sends. Relevance is established from
the store's own data, not from the fact that the date exists.

## When to Use

- A holiday or seasonal event is approaching and a decision is needed
- Deciding which holidays a store should participate in across a year
- Reviewing last year's holiday performance to plan this year's
- Establishing the strategy before a sequence is built

## When Not to Use

- Relevance is already established and the sequence needs designing. Use
  [holiday-drip-campaign](../holiday-drip-campaign/SKILL.md).
- The whole month needs planning. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md), which composes this skill.
- The event is a store-specific business event such as an anniversary or launch — that is a campaign or
  a [product launch](../product-launch/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The holiday, its dates, and the markets it applies to | The premise | Blocked |
| Prior-period revenue for this store around that date | The strongest relevance evidence | Partial; assess structurally, lower confidence |
| Catalogue relevance to the occasion | Whether the store has anything to say | Blocked |
| Customer locale and market distribution | Whether the holiday applies to this audience | Partial |
| Calendar occupancy and surrounding commitments | Whether there is room | Blocked |
| Competitive intensity of the period for this store | Whether participation is worth the cost | Partial |

This package ships **no hard-coded holiday calendar**. Dates and candidate holidays come from the request
or store context; relevance is always derived.

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, markets, locale, scale |
| `email_sms.customer_intelligence` | Audience locale distribution, engagement, prior participation |
| `email_sms.product_intelligence` | Which products are genuinely occasion-relevant |
| `email_sms.order_intelligence` | Prior-period revenue shape around the date |
| `email_sms.segmentation` | Sizing the audience the holiday applies to |
| `email_sms.campaign_analytics` | Last year's holiday campaign results |
| `email_sms.marketing_calendar` | Surrounding commitments and collisions |

## Decision Process

```
1. Establish relevance          ← prior revenue, catalogue fit, audience locale
2. Decide participation         ← including deciding not to
3. Identify relevant products   ← genuine fit, not forced association
4. Identify target audiences    ← who this occasion actually applies to
5. Review prior performance     ← what worked, what did not
6. Set the strategy             ← objective, offer posture, intensity
7. Set the timeline             ← when interest starts, peaks and ends for this store
8. Hand to holiday-drip-campaign if a sequence is warranted
```

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- Relevance is evidence, not assumption. Prior revenue around the date, catalogue fit, and audience locale
  decide it.
- **"Do not participate" is a valid and sometimes correct recommendation.** State the reasoning.
- Never force a product association that customers would find arbitrary (N1).
- Target only the audience the occasion applies to. A globally distributed list rarely observes the same
  holidays.
- Match intensity to evidence. A period that produced modest revenue last year does not warrant the
  store's largest push this year.
- Check surrounding calendar commitments before committing capacity (C1).
- Peak-period cadence may rise but stays bounded and is followed by a recovery window (F10, F12).
- Discount posture is decided here, before the sequence is built, so that the sequence does not escalate
  by default (C4).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read prior-period revenue, catalogue, audience locale, calendar | `read_only` |
| ANALYZE | Establish relevance, size the addressable audience, review prior results | `analysis` |
| PLAN | Participation decision, products, audiences, strategy, timeline | `plan` |
| PREVIEW | Present the strategy with relevance evidence | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human approves participation and posture | — |
| EXECUTE | Hand to [holiday-drip-campaign](../holiday-drip-campaign/SKILL.md) | `plan` |
| MEASURE | Record period results for next year's relevance evidence | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the participation recommendation with
its relevance evidence; relevant products and why; target audiences with sizes and exclusions; the
objective and offer posture; the timeline — when the period starts, peaks and ends for this store; the
expected outcome; risks; and the handover to sequence design, or an explicit statement that a single send
or no send is sufficient.

## Validation

- [ ] Relevance established from this store's data (G2, G3)
- [ ] Non-participation genuinely considered
- [ ] Product relevance is real, not forced
- [ ] Audience sized and locale-checked (A1)
- [ ] Prior performance reviewed where available
- [ ] Calendar collisions checked (C1)
- [ ] Intensity proportional to evidence
- [ ] Offer posture decided before sequence design (C4)
- [ ] Recovery window planned after the period (F12)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the strategy | `plan` | None |
| Build the sequence | `mutation` | In holiday-drip-campaign; preview then confirm |
| Send or schedule anything | `high_impact` | Explicit, per send |

## Examples

**"Should we do anything for this holiday?"**
Finds no revenue lift around the date in either of the last two years, a catalogue with no natural
connection, and an audience largely outside the markets that observe it. Recommends not participating,
and redirecting the capacity to the period two weeks later where the store's own data shows a consistent
lift. States the reasoning so the decision can be revisited with new evidence.

**"Plan our biggest season."**
Confirms strong relevance from prior-period revenue concentrated in a three-week window. Identifies two
product categories that carry it, three audiences including a prior-year buyer cohort worth early access,
and sets a timeline anchored on the delivery cut-off. Hands to
[holiday-drip-campaign](../holiday-drip-campaign/SKILL.md) with the posture already decided.

## Failure Handling

| Situation | Response |
|---|---|
| No prior-period data | **Partial.** Assess on catalogue fit and audience locale; recommend a deliberately small first attempt as evidence-gathering |
| Catalogue has no relevant products | Recommend non-participation rather than forcing a connection (N1) |
| Audience locale unavailable | **Partial.** Flag that relevance to the audience is unverified |
| Holiday dates ambiguous or regional | Ask; do not assume a date |
| Calendar already committed | Surface the conflict and state what would have to yield |
| Store insists on participating despite weak evidence | Plan a proportionate, low-cost participation and record the evidence gap as a risk |

Degraded outcomes set `status` and populate `unmet_requirements`.
