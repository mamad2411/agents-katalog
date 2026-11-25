---
name: marketing-calendar
description: Use when the planning horizon is a year or a quarter rather than a single month — building the annual calendar, sequencing the year's major moments against each other, reserving capacity for known peaks, and keeping that long-horizon plan current as commitments change. Answers "plan our marketing for the year", "build a quarterly calendar" and "what does the next twelve months look like?". Use monthly-marketing-planner for a single period, which this skill composes.
license: MIT
metadata:
  targetbay.display_name: Marketing Calendar
  targetbay.version: "2.0.1"
  targetbay.category: planning
  targetbay.requires: email_sms.store_profile, email_sms.order_intelligence, email_sms.product_intelligence, email_sms.customer_intelligence, email_sms.campaign_analytics, email_sms.automation, email_sms.marketing_calendar
  targetbay.composes: monthly-marketing-planner, holiday-marketing, product-launch
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Marketing Calendar

## Purpose

Plan and maintain a multi-period marketing calendar: where the store's major moments sit, how they
sequence against each other, how much capacity each consumes, and what stays deliberately empty.

A month planned in isolation is planned blind to the month after it. This skill holds the horizon that
[monthly-marketing-planner](../monthly-marketing-planner/SKILL.md) plans inside.

## When to Use

- Building a quarterly or annual calendar
- Sequencing major moments — peak seasons, launches, sales — against each other
- Deciding which holidays and events the store commits to for the year
- Maintaining a rolling calendar as commitments change
- Reserving capacity ahead of a known peak

## When Not to Use

- One month needs planning in detail. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md).
- One holiday needs assessing. Use [holiday-marketing](../holiday-marketing/SKILL.md).
- The question is strategy rather than scheduling. Use
  [revenue-growth](../revenue-growth/SKILL.md) first.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Revenue seasonality across at least one full cycle | Where the peaks actually are for this store | Blocked |
| Committed dates: launches, sales, business events | The fixed points everything else sits around | Blocked |
| Existing calendar occupancy across the horizon | What is already promised | Blocked |
| Automation contact load | Baseline cadence the calendar sits on top of | Blocked |
| Prior-year performance by period | Which moments earn their capacity | Partial; lower confidence |
| Catalogue and stock rhythm | Whether the store has something to say when planned | Partial |
| Team capacity | How much can actually be built | Partial; state the assumption |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, markets, scale |
| `email_sms.order_intelligence` | Seasonality and revenue concentration by period |
| `email_sms.product_intelligence` | Catalogue rhythm, launches, stock cycles |
| `email_sms.customer_intelligence` | Audience availability and engagement across the horizon |
| `email_sms.campaign_analytics` | Prior-period performance |
| `email_sms.automation` | Baseline contact load |
| `email_sms.marketing_calendar` | Occupancy and commitments across the horizon |

## Decision Process

```
1. Map the store's own seasonality      ← from revenue, not from a generic retail calendar
2. Place the fixed points               ← committed launches, sales, business events
3. Assess candidate moments             ← delegate each holiday to holiday-marketing
4. Rank moments by evidenced value
5. Allocate capacity                    ← peaks get more, and the rest gets correspondingly less
6. Reserve recovery windows after peaks
7. Leave deliberate slack               ← for the opportunity that has not happened yet
8. Hand each period to monthly-marketing-planner
```

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../knowledge/campaign-principles.md](../../knowledge/campaign-principles.md).

- Seasonality comes from the store's own revenue history, never from a generic retail calendar (G3).
- **The calendar has finite capacity.** Attention is a shared budget; a year planned at maximum intensity
  produces a fatigued list by the second peak.
- Peaks earn extra capacity; the periods around them give it back. Intensity is borrowed, not created
  (F10, F12).
- Every peak is followed by a reserved recovery window (F12).
- Leave slack. A calendar with no unallocated capacity cannot respond to anything.
- A moment is committed only when evidence supports it. Uncommitted candidates stay on the calendar as
  candidates, clearly marked.
- Declare dependencies between periods: stock, creative lead time, a launch that must land before a push
  (C12).
- Sequence competing moments explicitly. Two peaks close together need one of them scaled down.
- Revisit rather than freeze. A calendar is a rolling plan, and the assumptions behind each entry are
  recorded so they can be rechecked.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read seasonality, commitments, occupancy, automation load, prior performance | `read_only` |
| ANALYZE | Map peaks, assess candidate moments, compute capacity across the horizon | `analysis` |
| PLAN | Place moments, allocate capacity, reserve recovery and slack | `plan` |
| PREVIEW | Present the calendar with capacity and dependency reasoning | `plan` |
| VALIDATE | Run the checks below across the whole horizon | `plan` |
| APPROVE | Human approves the shape, not the individual sends | — |
| EXECUTE | Each period handed to [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md) | `plan` |
| MEASURE | Compare each period's outcome to its allocated capacity, and re-plan | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the store's own seasonality map; the
horizon calendar with each moment's dates, objective, allocated capacity and status (committed, planned,
candidate); reserved recovery windows; unallocated slack; cross-period dependencies; candidate moments
assessed and declined with reasons; and the assumptions each entry rests on.

## Validation

- [ ] Seasonality derived from this store's revenue (G3)
- [ ] Every committed date placed and accounted for
- [ ] Capacity computed across the horizon, including automation load (F2, F3)
- [ ] Peaks balanced by reduced intensity elsewhere (F10)
- [ ] Recovery window reserved after every peak (F12)
- [ ] Unallocated slack left deliberately
- [ ] Cross-period dependencies stated (C12)
- [ ] Candidate moments assessed on evidence, not on the date existing
- [ ] Declined moments recorded with reasons
- [ ] Assumptions recorded per entry so they can be rechecked

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the horizon calendar | `plan` | None |
| Plan a period in detail | `plan` | In monthly-marketing-planner |
| Create drafts | `mutation` | Preview, then confirm |
| **Any send** | `high_impact` | **Explicit, per send** (S9) |

Approving a year's shape approves no sends at all.

## Examples

**"Plan our marketing for the year."**
Seasonality shows two genuine peaks, one of them much larger than the generic retail calendar would
suggest and the other absent from it entirely. Places both, allocates the larger share of annual capacity
to the bigger one, scales the quarter before it down deliberately, reserves recovery after each, and
leaves roughly a fifth of capacity unallocated. Four candidate holidays are declined on evidence, with the
reasons recorded so the decision can be revisited next year.

**"We've moved our launch to the week before our peak."**
Recalculates capacity for the collision. Reports that both moments at full intensity exceed the audience's
tolerance, and recommends scaling the launch to an affinity-targeted wave rather than a full-list
announcement — preserving the peak, which the evidence says is worth more.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.marketing_calendar` unavailable | **Blocked.** Planning blind to commitments risks collisions |
| Less than one full seasonal cycle of history | **Partial.** Plan on committed dates and catalogue rhythm; mark seasonality provisional |
| Automation load unreadable | **Blocked.** Capacity cannot be computed (F2) |
| Two peaks unavoidably collide | Surface it and recommend which one scales down, with the evidence |
| Capacity insufficient for committed events | Report the overage plainly rather than planning a calendar the list cannot absorb |
| Team capacity unknown | State the assumption and flag it as the calendar's weakest input |

Degraded outcomes set `status` and populate `unmet_requirements`.
