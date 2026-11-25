---
name: holiday-drip-campaign
description: Use when preparing a multi-message sequence around a holiday, festival or seasonal event — "prepare a Diwali campaign", "build our Black Friday sequence". Derives how many stages the sequence needs, which stages they are, how they are spaced, and which channel carries each, from the holiday's importance to this store, its sales window, product cycle, audience size and history. The stage count is derived, never fixed.
license: MIT
metadata:
  targetbay.display_name: Holiday Drip Campaign
  targetbay.version: "2.0.0"
  targetbay.category: seasonal
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_management, email_sms.campaign_analytics, email_sms.marketing_calendar, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Holiday Drip Campaign

## Purpose

Design the message sequence for a holiday or seasonal event: how many stages, which stages, spaced how,
on which channels, to which audiences.

The count of messages is an output of the store's situation, not a template. A store with a two-day sale
window, a small list and one relevant product does not need the same sequence as a store whose peak
season runs for six weeks. This skill derives the number and states the derivation.

## When to Use

- A holiday, festival or seasonal event needs a multi-message sequence
- "Prepare a <holiday> campaign" and equivalents
- An existing seasonal sequence needs restructuring for this year
- A sale period needs a message arc rather than a single send

## When Not to Use

- The holiday's relevance to the store has not been established yet. Use
  [holiday-marketing](../holiday-marketing/SKILL.md) first — it decides whether and how the store should
  participate; this skill builds the sequence once it has.
- One message is sufficient. A single send does not need a drip.
- The trigger is a customer behaviour rather than a date. Use
  [automation-architect](../automation-architect/SKILL.md).
- The whole month needs planning. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md), which composes this skill for the
  holiday portion.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The holiday, its dates, and its relevance to this store | The whole premise | Blocked |
| Prior performance of this holiday for this store | The strongest evidence for stage count and timing | Partial; structural design, lower confidence |
| Sale or promotion window | Determines the arc's length | Blocked |
| Relevant products, stock posture, lead times | What each stage can say | Blocked |
| Audience sizes and segments | Whether audience-specific arcs are viable | Blocked |
| Calendar occupancy around the period | Collisions with other planned sends | Blocked |
| Cadence already committed from automations | Fatigue headroom | Blocked |
| Channel consent and performance | Channel assignment per stage | Partial; email-only |
| Delivery cut-off dates, where relevant | Shapes the urgency and last-chance stages | Partial; omit those stages |

This package ships **no hard-coded holiday dates or calendars**. Dates come from the request or store
context; relevance comes from the store's own data.

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, locale, scale, sending posture |
| `email_sms.customer_intelligence` | Audience availability, engagement, channel preference |
| `email_sms.product_intelligence` | Relevant products, categories, stock posture |
| `email_sms.order_intelligence` | Prior-period revenue shape, purchase timing within the window |
| `email_sms.segmentation` | Sizing each arc's audience |
| `email_sms.campaign_management` | Creating the sequence after approval |
| `email_sms.campaign_analytics` | Last year's performance by stage |
| `email_sms.marketing_calendar` | Collisions across the period |
| `email_sms.suppression_and_consent` | Channel eligibility, quiet hours |

## Decision Process

```
1. Confirm relevance and dates            ← from holiday-marketing or store context
      ↓
2. Read last year's performance           ← revenue shape across the window, stage-level results
      ↓
3. Establish the window                   ← when interest starts, peaks, and ends for this store
      ↓
4. Derive the stage count                 ← see the derivation below
      ↓
5. Select stages from the vocabulary      ← only stages that have something to say
      ↓
6. Space the stages                       ← denser near the peak, sparse in the build-up
      ↓
7. Assign audiences per stage             ← delegate to audience-discovery
      ↓
8. Assign channel per stage               ← email for context, SMS for deadlines
      ↓
9. Assign offer and content direction per stage
      ↓
10. Check cadence and collisions across the whole arc
      ↓
11. Validate, then produce the plan
```

**Deriving the stage count.** The number rises with: the holiday's importance to this store, the length
of the sale window, the length of the product's consideration cycle, audience size and engagement,
evidence from prior years, inventory depth, and how much genuinely different content the store has. It
falls with: a short window, a fatigued or small list, thin stock, a single relevant product, and a
crowded surrounding calendar.

State the derivation in the output. "Five stages because the window is three weeks, last year's revenue
concentrated in the final four days, and the list has headroom" is a decision. "Five stages" is a template.

**Stage vocabulary** — a menu, never a fixed sequence, and never all of them:

`awareness` · `teaser` · `early access` · `product discovery` · `promotion` · `urgency` ·
`last chance` · `post-event` · `retention`

Each selected stage must have something to say that no other stage says. A stage included for symmetry is
removed.

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md).

- **Never fix the stage count in advance.** Derive it and show the derivation.
- Never include a stage that duplicates another stage's message.
- Spacing follows purchase behaviour, not equal intervals. Most holiday revenue concentrates near the
  deadline; the sequence should densify there and stay light in the build-up.
- Urgency must be real — a real cut-off, real stock, a real delivery deadline (N3).
- Channel sequencing: email carries context and discovery, SMS carries deadlines and cut-offs. Never send
  the same content on both at once ([../../knowledge/sms-principles.md](../../knowledge/sms-principles.md)).
- Audience-specific arcs are created only where they pass
  [../../rules/audience-rules.md#A3](../../rules/audience-rules.md) — commonly early access for VIPs, a
  shorter arc for low-engagement contacts.
- Purchasers exit the promotional arc. Someone who bought on day two should not receive last-chance
  urgency on day six — this is the most visible failure mode of a holiday sequence.
- Higher peak-period cadence is legitimate, but bounded, and followed by a recovery window (F10, F12).
- Plan the post-event stage deliberately: holiday buyers are frequently first-time buyers, and the
  handover to retention is where their value is won or lost.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read prior performance, products, audiences, calendar, consent | `read_only` |
| ANALYZE | Revenue shape across the window, audience headroom, stock posture | `analysis` |
| PLAN | Derive stage count, select and space stages, assign audience/channel/offer | `plan` |
| PREVIEW | Present the arc with the derivation and per-stage justification | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human approves the arc | — |
| EXECUTE | Create campaigns as drafts | `mutation` |
| — | **Scheduling or sending each stage** | `high_impact`, separate approval |
| MEASURE | Record stage-level results for next year | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing a sequence plan — a
[workflow](../../schemas/workflow.schema.json) of type `drip`. Per stage:

- Stage name from the vocabulary, and its purpose
- Date or offset within the window
- Audience, size, exclusions — including purchaser exit
- Channel and the reason for it
- Offer or reason to act
- Content direction with a single call to action
- Expected outcome and measure

Plus: the stage-count derivation, the stages considered and rejected, the cadence summary for the period,
the recovery window after the event, and dependencies — stock, creative, delivery cut-offs.

## Validation

- [ ] Stage count derived and the derivation stated
- [ ] Every stage says something no other stage says
- [ ] Spacing justified by purchase behaviour, not evenly distributed by default
- [ ] Purchaser exit defined for every promotional stage
- [ ] Every audience resolved and sized (A1)
- [ ] Total cadence across the arc plus automations within limits (F2, F3, F10)
- [ ] No collisions with other planned sends (F8, C1)
- [ ] SMS stages consent-checked and quiet-hours aware (A10, F9)
- [ ] Every urgency claim backed by a real deadline or real stock (N3)
- [ ] Recovery window planned after the event (F12)
- [ ] Post-event retention handover defined
- [ ] Dependencies stated (C12)
- [ ] No invented prior-year figures (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read prior performance and catalogue | `read_only` | None |
| Produce the sequence plan | `plan` | None |
| Create segments and campaign drafts | `mutation` | Preview, then confirm |
| **Schedule or send any stage** | `high_impact` | **Explicit, per stage** (S2, S9) |
| Send SMS stages | `high_impact` | Explicit; state recipient count and cost |

Approving the arc is not approving its sends. Staged approval is preferred: approve the early stages,
measure, then decide the later ones.

## Examples

**"Prepare a Diwali campaign."**
Confirms relevance through prior-period revenue and the store's catalogue. Last year's revenue
concentrated in the final five days of a three-week interest window. The list has headroom; two product
categories are clearly relevant; stock is deep on one and thin on the other. Derives five stages:
awareness early, product discovery mid-window, promotion at the start of the sale, urgency two days
before the delivery cut-off, and post-event retention. Teaser and early access are rejected — the store
has no exclusivity mechanic and the VIP audience is too small to justify a separate arc. SMS carries only
the urgency stage. Purchasers exit at the promotion stage.

**"Build our Black Friday sequence."**
Same process, different derivation: a short, intense window with an engaged list and deep stock produces a
denser arc with early access for prior-year buyers and two urgency stages, followed by an explicit
recovery window and a retention handover for the large cohort of first-time buyers the period produces.

Full trace: [../../examples/holiday-drip.md](../../examples/holiday-drip.md).

## Failure Handling

| Situation | Response |
|---|---|
| Holiday relevance not established | Run [holiday-marketing](../holiday-marketing/SKILL.md) first, or ask |
| No prior-year data | **Partial.** Design a deliberately shorter arc, label the stage count provisional, mark spacing testable |
| Sale window undecided | Ask. The window determines the arc; guessing it invalidates everything downstream |
| List has no cadence headroom | Return a shorter arc and say why, rather than planning sends that will fatigue the list |
| Stock unconfirmed | Plan with stock as a stated dependency; never promise availability that is unverified (N3, P9) |
| SMS capability unavailable | Design email-only; record where SMS would have carried urgency |
| Delivery cut-off unknown | Omit the deadline-based urgency stage rather than inventing a date |
| Audience too small for variant arcs | Return a single arc with personalisation and say why |
| Calendar already crowded | Surface the conflict and propose what yields, before adding stages |

Degraded outcomes set `status` and populate `unmet_requirements`. Never invent prior-year performance,
cut-off dates or stock levels to complete an arc (G3).
