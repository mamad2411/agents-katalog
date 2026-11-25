---
name: product-launch
description: Use when a new product, collection, restock or category is being introduced and needs a marketing plan — deciding who hears about it first, how the announcement is sequenced, which channels carry it, and how the launch converts into ongoing demand rather than a single spike.
license: MIT
metadata:
  targetbay.display_name: Product Launch
  targetbay.version: "2.0.1"
  targetbay.category: acquisition
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_management, email_sms.campaign_analytics, email_sms.marketing_calendar, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery, cross-sell
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Product Launch

## Purpose

Plan the marketing for a new product, collection, restock or category: audience sequencing, message arc,
channel mix, and the handover from launch spike to sustained demand.

The two failure modes this skill guards against: announcing to everyone at once and learning nothing, and
producing a spike with no follow-through, so the product's second week is empty.

## When to Use

- A new product, collection or category is launching
- A significant restock of a previously sold-out product
- A product needs relaunching after weak initial performance
- Deciding who gets early access and who hears later

## When Not to Use

- The launch is tied to a holiday and the holiday is the anchor. Use
  [holiday-marketing](../holiday-marketing/SKILL.md) first.
- The product already launched and needs ongoing promotion — that is campaign work.
- The launch needs placing in a wider calendar. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md), which composes this skill.
- The message is a per-contact alert rather than an announcement — a back-in-stock notice to people
  who asked for one, a price-drop notice, or a waitlist collected before the product exists. Use
  [stock-and-price-alerts](../stock-and-price-alerts/SKILL.md). Announcing a restock to a broad
  audience stays here.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Product details: category, price band, attributes, positioning | Determines audience and angle | Blocked |
| Stock depth and replenishment lead time | Determines launch intensity and sequencing | Blocked |
| Affinity for the product's category and price band | Who is likely to respond | Blocked |
| Prior launch performance | What this store's launches actually do | Partial; lower confidence |
| Calendar occupancy | Room for the launch arc | Blocked |
| Channel consent and engagement | Channel mix | Partial; email-only |
| Existing customers who own predecessors | Early-access and upgrade candidates | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, scale, positioning |
| `email_sms.product_intelligence` | Product attributes, category, price band, affinity, stock |
| `email_sms.customer_intelligence` | Affinity, value, engagement, prior ownership |
| `email_sms.order_intelligence` | Prior launch revenue shape, price-band behaviour |
| `email_sms.segmentation` | Sizing each launch wave |
| `email_sms.campaign_management` | Creating the launch campaigns after approval |
| `email_sms.campaign_analytics` | Prior launch results |
| `email_sms.marketing_calendar` | Collisions across the launch window |
| `email_sms.suppression_and_consent` | Channel eligibility |

## Decision Process

```
1. Understand the product         ← category, price band, attributes, who it is for
2. Check stock against ambition   ← a launch that sells out in a day was under-stocked or over-marketed
3. Identify the audience waves    ← strongest affinity first, broadest last
4. Decide the sequence            ← early access, launch, broad, follow-up
5. Decide the channel per wave
6. Decide the content arc         ← what makes this product worth attention
7. Plan the follow-through        ← the second week, not just the launch day
8. Validate cadence and collisions, then produce the plan
```

**Wave sequencing.** Launching to the highest-affinity audience first is both a revenue decision and an
information decision: the response of the first wave tells you whether the broader waves are worth
sending and what angle works, before the whole list has been spent on a weak message.

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- Sequence waves by affinity strength. Never announce to the entire list at once unless stock and
  evidence justify it.
- Match intensity to stock. Marketing depth the store cannot supply produces disappointed customers and
  wasted sends (P9, N3).
- Exclude prior purchasers of the product from launch announcements, and route owners of a predecessor
  into an upgrade angle instead.
- Early access is a recognition mechanism for high-value customers and works without discounting (C4,
  [../../knowledge/customer-lifecycle.md](../../knowledge/customer-lifecycle.md)).
- Plan the follow-through before the launch: what the product's second and third weeks look like, and
  whether it enters an automation for ongoing demand (C11).
- Never promise availability that is unverified (N3, P9).
- Count the launch arc against existing cadence (F2, F3).
- Let the first wave inform the later ones. Build the later waves as planned, not as committed.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read product, stock, affinity, prior launches, calendar | `read_only` |
| ANALYZE | Size waves, check stock against ambition, review prior launch shape | `analysis` |
| PLAN | Wave sequence, channels, content arc, follow-through | `plan` |
| PREVIEW | Present the plan with wave sizes and stock dependency | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human approves the arc | — |
| EXECUTE | Create campaign drafts | `mutation` |
| — | **Sending each wave** | `high_impact`, separate approval |
| MEASURE | Wave-level response; adjust later waves before sending them | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the wave sequence with audience,
size, exclusions, channel, timing and content direction per wave; the stock dependency; the
follow-through plan; expected outcome per wave; and risks — stock, cadence, collision, thin affinity
evidence.

## Validation

- [ ] Waves sequenced by affinity, not sent simultaneously
- [ ] Every wave's audience resolved and sized (A1)
- [ ] Prior purchasers and predecessor owners handled explicitly (A4)
- [ ] Stock checked against planned reach (P9)
- [ ] No unverified availability claims (N3)
- [ ] Follow-through planned beyond launch day
- [ ] Cadence counted across the arc (F2, F3)
- [ ] Calendar collisions resolved (C1, F8)
- [ ] Later waves left adjustable on first-wave evidence

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the launch plan | `plan` | None |
| Create segments and drafts | `mutation` | Preview, then confirm |
| **Send each wave** | `high_impact` | **Explicit, per wave** (S9) |

## Examples

**"We're launching a new collection next month."**
Affinity analysis identifies a strong prior-category cohort, a moderate adjacent cohort, and the rest of
the list. Stock supports roughly the first two waves at expected conversion. Plans early access for
high-value prior-category buyers, a launch-day send to the full affinity cohort, a broad send three days
later contingent on remaining stock, and an entry into the post-purchase journey for buyers. The broad
wave is planned but explicitly not committed.

**"Restocking our bestseller."**
Targets the waitlist and prior sold-out-period visitors first, then prior buyers of the category.
Recommends SMS for the restock notification where consent exists, because the value is entirely in
immediacy, and email for the broader announcement.

## Failure Handling

| Situation | Response |
|---|---|
| Stock position unknown | **Partial.** Plan conservatively, state stock as an unverified dependency |
| No affinity data for a new category | **Partial.** Sequence on value and engagement instead, and say so |
| No prior launch history | Plan a smaller first wave explicitly as evidence-gathering |
| Launch date unconfirmed | Plan relative offsets rather than absolute dates, and flag it |
| Stock too thin for a broad launch | Recommend a limited arc and say why; over-marketing thin stock costs trust |
| Calendar already full | Surface the conflict and state what would have to move |

Degraded outcomes set `status` and populate `unmet_requirements`.
