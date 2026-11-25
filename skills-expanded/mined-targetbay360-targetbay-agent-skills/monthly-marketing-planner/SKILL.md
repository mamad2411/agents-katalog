---
name: monthly-marketing-planner
description: Use when planning a month of marketing — "plan next month", building a marketing calendar, or deciding what campaigns to run over an upcoming period. Produces a dated calendar of campaigns with objectives, audiences, channels, offers, content direction, expected outcomes, dependencies and risks, derived from the store's own history rather than a fixed template. The number of campaigns is an output, never an input.
license: MIT
metadata:
  targetbay.display_name: Monthly Marketing Planner
  targetbay.version: "2.0.0"
  targetbay.category: planning
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_management, email_sms.campaign_analytics, email_sms.automation, email_sms.marketing_calendar, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery, campaign-optimization, holiday-marketing, product-launch, revenue-growth
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Monthly Marketing Planner

## Purpose

Produce a dated marketing calendar for an upcoming period: what to send, to whom, on which channel, with
what offer and what expected outcome — built from the store's own performance, catalogue, calendar and
customer base.

The output is a plan a human can review line by line and a system can execute. The campaign count is
derived, not assumed: a store with a thin catalogue and a fatigued list should receive fewer campaigns
than a high-volume store in its peak season, and the plan should say why.

## When to Use

- "Plan next month's marketing" and equivalents
- Building or refreshing a marketing calendar for any forward period
- Reworking a plan after a business change — a launch moving, stock arriving, a target changing
- Establishing a repeatable planning cadence for a store

## When Not to Use

- A single campaign needs planning. Use [audience-discovery](../audience-discovery/SKILL.md) plus
  [campaign-optimization](../campaign-optimization/SKILL.md).
- The period is dominated by one holiday. Use [holiday-marketing](../holiday-marketing/SKILL.md), then
  return here to place the rest of the month around it.
- The question is about triggered journeys. Use
  [automation-strategy](../automation-strategy/SKILL.md).
- A revenue target needs a strategy rather than a calendar. Use
  [revenue-growth](../revenue-growth/SKILL.md) first; this skill schedules what it decides.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Historical campaign performance | Which campaign types work for this store | Partial; plan is structural, confidence lowered |
| Revenue by period and product | Seasonality and what drives the month | Partial |
| Customer lifecycle distribution | Which audiences are available and how large | Blocked |
| Product catalogue, launches, stock posture | What there is to say | Blocked |
| Existing automations | What contacts already receive | Blocked — cadence cannot be planned without it |
| Calendar occupancy for the period | Collisions and existing commitments | Blocked |
| Upcoming holidays and business events relevant to the store | Anchors the calendar | Partial; state which were considered |
| Channel performance and consent | Channel mix | Partial; email-only |
| Recent send cadence | Fatigue headroom | Blocked |

Holidays and events are read from context and store data. This package ships **no hard-coded holiday
calendar** — relevance is store-specific.

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, scale, sending posture |
| `email_sms.customer_intelligence` | Audience availability, lifecycle mix, engagement |
| `email_sms.product_intelligence` | What to promote, launches, categories, stock posture |
| `email_sms.order_intelligence` | Seasonality, revenue concentration, repeat intervals |
| `email_sms.segmentation` | Sizing every planned audience |
| `email_sms.campaign_management` | Existing and draft campaigns; creating the plan after approval |
| `email_sms.campaign_analytics` | What has worked historically |
| `email_sms.automation` | Contact load already committed |
| `email_sms.marketing_calendar` | Occupancy and collisions |
| `email_sms.suppression_and_consent` | Channel eligibility and frequency caps |

## Decision Process

```
1. Read the period            ← what is already scheduled, what is committed
      ↓
2. Read the store's history   ← what worked, when, for whom
      ↓
3. Identify anchors           ← launches, holidays, stock events, business dates
      ↓
4. Identify opportunities     ← lifecycle gaps, dormant value, product pushes
      ↓
5. Establish capacity         ← cadence headroom after automations; F2, F3
      ↓
6. Select campaigns           ← highest expected value that fits the capacity
      ↓
7. Assign audiences           ← delegate to audience-discovery
      ↓
8. Assign channel and timing  ← consent, observed engagement, collision avoidance
      ↓
9. Assign offer and content direction
      ↓
10. Sequence and resolve dependencies
      ↓
11. Validate the whole calendar as one object
      ↓
12. Produce the plan
```

Step 5 comes before step 6 deliberately. Capacity is a constraint on the plan, not something discovered
after the calendar is full.

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md).

- **No fixed campaign count.** Derive it from capacity, available anchors, audience availability and what
  the store genuinely has to say. State the number and its reasoning.
- Every campaign has exactly one objective (C2).
- Campaign slots are filled by expected value, not by filling the grid. An empty week is a valid output.
- Count automation contact against cadence before adding campaigns (F2, F3).
- Check the calendar for existing commitments before proposing anything (C1).
- Never duplicate a campaign that already exists or recently ran (C3).
- Justify every discount, and work down the reason-to-act list before reaching for one (C4).
- Sequence sends to the same audience; resolve collisions explicitly (C7, F8).
- Every row carries an expected outcome and how it will be measured (C8).
- Declare dependencies — stock, creative, launch dates, prior campaigns (C12).
- Reserve headroom. A calendar planned to the cadence ceiling has no room for the opportunity that
  appears mid-month.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read calendar, history, customers, products, automations, consent | `read_only` |
| ANALYZE | Seasonality, opportunity, capacity, audience availability | `analysis` |
| PLAN | Select, date, target, channel, offer, content direction per campaign | `plan` |
| PREVIEW | Present the calendar with evidence and risks | `plan` |
| VALIDATE | Run the checks below across the whole calendar | `plan` |
| APPROVE | Human approves the calendar, or campaigns individually | — |
| EXECUTE | Create drafts via `email_sms.campaign_management` | `mutation` |
| — | **Scheduling or sending each campaign** | `high_impact`, separate approval |
| MEASURE | Feed results to [campaign-optimization](../campaign-optimization/SKILL.md) | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing a calendar. Every row carries:

| Field | Meaning |
|---|---|
| `date` | Planned send date, and window if flexible |
| `campaign` | Working name |
| `objective` | The single business outcome |
| `audience` | Definition, size, exclusions |
| `channel` | Email, SMS, or a sequence |
| `product` | What is promoted, if applicable |
| `offer` | Offer or the non-discount reason to act |
| `content_direction` | Angle, proof, single call to action |
| `expected_outcome` | What success looks like and how it is measured |
| `dependencies` | Stock, creative, launch, prior campaign |
| `risk` | Fatigue, collision, margin, inventory, thin evidence |

Plus: the cadence summary per audience, the campaigns considered and rejected, and the stated reasoning
for the total campaign count.

## Validation

- [ ] Every audience resolved and sized (A1)
- [ ] Cadence per audience computed across campaigns **and** automations, within limits (F2, F3)
- [ ] No unresolved collisions in the calendar (F8, C7)
- [ ] No duplication of existing or recent campaigns (C3, G5)
- [ ] Every campaign has exactly one objective (C2)
- [ ] Every row has an expected outcome and a measure (C8)
- [ ] Every discount justified (C4)
- [ ] Dependencies stated (C12)
- [ ] Channel assignments consent-checked (A10)
- [ ] Campaign count justified, not templated
- [ ] Headroom left for mid-period opportunities
- [ ] No invented performance figures or benchmarks (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read history and calendar | `read_only` | None |
| Produce the plan | `plan` | None |
| Create segments the plan needs | `mutation` | Preview, then confirm |
| Create campaign drafts | `mutation` | Preview, then confirm |
| **Schedule or send any campaign** | `high_impact` | **Explicit, per campaign** (S2, S9) |

Approving a calendar is not approving its sends. Each send is approved on its own terms.

## Examples

**"Plan next month's marketing."**
Reads the calendar and finds two committed sends and a product launch mid-month. Automations already
contact the engaged segment roughly weekly, leaving limited headroom. Seasonality shows the category
that drives the month. Produces six campaigns rather than a default cadence, with the launch anchoring
the middle two weeks, a win-back push in the quiet first week, and the final week deliberately left light
because the following month opens with a major sale. States the reasoning for six.

**"Plan next month, we need 20% more revenue."**
Same process, different intensity. Pulls forward the highest-value opportunities, proposes an AOV
mechanic instead of a blanket discount, and states plainly which part of the target the plan can
evidence and which part it cannot.

Full trace: [../../examples/plan-next-month.md](../../examples/plan-next-month.md).

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.marketing_calendar` unavailable | **Blocked.** Planning blind risks collisions with committed sends |
| Campaign history unavailable | **Partial.** Plan structurally, lower confidence, mark choices testable |
| Automations unreadable | **Blocked.** Cadence cannot be computed (F2) |
| New store, no history | Produce a coverage-first starter calendar, label every assumption, keep it deliberately light |
| No audience headroom | Return a smaller calendar and say why, rather than planning sends that will fatigue the list |
| Revenue target not supportable by evidence | Plan what is supportable, state the gap explicitly, do not pad the calendar to close it |
| Launch dates unconfirmed | Plan around them as dependencies and flag them as unconfirmed |
| Consent data unavailable | Plan email-only; record the gap |

Degraded outcomes set `status` to `partial` or `blocked` with populated `unmet_requirements`. Never fill
a calendar with campaigns that exist only to fill it (G7).
