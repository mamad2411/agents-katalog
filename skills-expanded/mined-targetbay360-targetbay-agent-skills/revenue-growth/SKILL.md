---
name: revenue-growth
description: Use when the objective is stated as revenue — "increase revenue this month", "we need to hit a number", "where is our growth going to come from". Identifies where the store's revenue can realistically grow, ranks the opportunities by evidence and expected value, and decides which campaigns, automations and audiences should carry them. Produces a strategy that other skills execute, not a calendar.
license: MIT
metadata:
  targetbay.display_name: Revenue Growth
  targetbay.version: "2.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_analytics, email_sms.automation, email_sms.automation_analytics, email_sms.marketing_calendar
  targetbay.composes: audience-discovery, automation-strategy, campaign-optimization, revenue-analysis, aov-growth
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Revenue Growth

## Purpose

Find where revenue can grow for this specific store, rank the opportunities by evidence and expected
value, and say which instrument should carry each one.

The discipline this skill enforces: every opportunity is tied to a term of the revenue equation, sized
against real data, and ranked honestly — including saying when a stated target is not supportable by the
evidence available.

## When to Use

- "Increase revenue", with or without a target
- Quarterly or monthly strategy before the calendar is built
- Diagnosing flat or declining revenue
- Deciding where limited marketing capacity should go
- Establishing a growth baseline for a store

## When Not to Use

- The strategy is already agreed and needs scheduling. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md).
- One campaign underperforms. Use [campaign-optimization](../campaign-optimization/SKILL.md).
- The question is specifically about retention, win-back, AOV or a single lever — those skills go deeper
  than this one does.
- The question is what *happened* to revenue rather than what to do about it. Use
  [revenue-analysis](../revenue-analysis/SKILL.md), which this skill composes for the decomposition.
- The store wants a financial forecast. This skill finds marketing opportunities; it does not model revenue.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Revenue history by period, product and customer type | The baseline everything is measured against | Blocked |
| Customer lifecycle distribution and value concentration | Where revenue is leaking or concentrated | Blocked |
| Purchase frequency and repeat intervals | Frequency-term opportunities | Partial |
| AOV distribution | AOV-term opportunities | Partial |
| Product performance, margin signals, stock posture | What can carry a push | Partial |
| Campaign and automation performance | Which channels and journeys already work | Partial; lower confidence |
| Calendar occupancy and cadence headroom | Whether anything can actually be executed | Blocked |
| Stated target and period | Calibrates ambition | Optional; plan to the evidence instead |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, scale, constraints |
| `email_sms.customer_intelligence` | Lifecycle distribution, value bands, churn and purchase signals |
| `email_sms.product_intelligence` | Product and category performance, affinity, stock |
| `email_sms.order_intelligence` | Revenue decomposition, frequency, AOV, discount dependence |
| `email_sms.segmentation` | Sizing every opportunity's audience |
| `email_sms.campaign_analytics` | What has produced revenue before |
| `email_sms.automation` / `email_sms.automation_analytics` | Existing journey coverage and revenue |
| `email_sms.marketing_calendar` | Executable capacity in the period |

## Decision Process

```
1. Decompose current revenue        ← delegated to revenue-analysis; customers × frequency × AOV
      ↓
2. Locate the leaks                 ← which lifecycle transitions lose the most value
      ↓
3. Locate the concentrations        ← which products, categories and cohorts carry revenue
      ↓
4. Generate opportunities per term  ← acquisition/reactivation, frequency, AOV, retention
      ↓
5. Size each opportunity            ← audience × plausible effect, from this store's own history
      ↓
6. Check executability              ← capacity, cadence headroom, stock, lead time
      ↓
7. Rank by expected value ÷ effort
      ↓
8. Assign an instrument per opportunity   ← campaign, automation, audience work, optimisation
      ↓
9. State what the evidence does and does not support
      ↓
10. Hand execution to the owning skills
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- Every opportunity names the revenue term it moves. An opportunity that cannot be tied to one is not an
  opportunity.
- AOV-term opportunities are delegated to [aov-growth](../aov-growth/SKILL.md), which chooses between
  threshold, bundle, tier and attachment levers rather than assuming one.
- Size from this store's own data. Never use an external benchmark as if it were a projection (G3).
- Prefer retention and frequency levers over acquisition for established stores — the base already exists
  and costs nothing to reach
  ([../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md)).
- Fix leaks before adding volume. A store losing first-time buyers does not need more first-time buyers.
- Prefer durable instruments over one-off pushes where both would work: an automation earns repeatedly,
  a campaign earns once (G7, G16).
- Justify every discount-led opportunity, and state its margin cost, not just its revenue (C4).
- Check executability before ranking. An opportunity that cannot be sent in the period is not this
  period's opportunity.
- If the target exceeds what the evidence supports, say so plainly and show the gap. Never close the gap
  with optimistic assumptions (G3, G15).
- Rank, with the ranking criteria stated (G14).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read revenue, customers, products, campaigns, automations, calendar | `read_only` |
| ANALYZE | Decompose revenue, locate leaks and concentrations, size opportunities | `analysis` |
| PLAN | Rank, assign instruments, state the evidence gap | `recommendation` |
| PREVIEW | Present ranked opportunities with evidence and risks | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Delegate to the owning skills; each mutation approved there | `plan` → `mutation` |
| MEASURE | Re-run after the period to compare outcome against expectation | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) whose recommendations conform to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json). Per opportunity:

- The opportunity, stated as an action
- The revenue term it moves
- Audience and size
- Expected effect, with the evidence it rests on — period and sample size
- Instrument: campaign, automation, audience work, or optimisation, and which skill owns it
- Effort and dependencies
- Risks, including margin cost and cadence cost
- Rank and confidence

Plus: the revenue decomposition that produced them, opportunities considered and rejected, and — where a
target was given — an explicit statement of how much of it the evidence supports.

## Validation

- [ ] Revenue decomposed before opportunities generated
- [ ] Every opportunity tied to a revenue term
- [ ] Every audience resolved and sized (A1)
- [ ] Every expected effect traced to this store's own data (G2, G3)
- [ ] Executability checked against calendar and cadence (F2, C1)
- [ ] Discount-led opportunities carry their margin cost (C4)
- [ ] Ranking criteria stated (G14)
- [ ] Gap between target and evidence stated explicitly, if any
- [ ] Rejected opportunities recorded
- [ ] No external benchmarks presented as projections (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce ranked opportunities | `recommendation` | None |
| Build anything recommended | `mutation` | In the owning skill; preview then confirm |
| Send or schedule anything | `high_impact` | Explicit, per send |

## Examples

**"Increase revenue this month."**
Decomposes revenue and finds frequency, not acquisition, is the weak term: a large first-time cohort from
the previous quarter has not returned, and no second-purchase journey exists. Ranks: build the
second-purchase automation (durable, large audience, no margin cost), run a win-back campaign against the
dormant cohort with the strongest prior affinity, and add a threshold mechanic to the two campaigns
already scheduled. Rejects a sitewide discount — it would move revenue forward from full-price buyers at
a margin cost the evidence does not justify.

**"We need 30% more revenue next quarter."**
Sizes each opportunity honestly and reports that the evidence supports roughly half the target through
marketing levers alone, names what would have to change for the rest — acquisition volume, catalogue,
margin policy — and plans the supportable half rather than padding the calendar.

Full trace: [../../examples/increase-revenue.md](../../examples/increase-revenue.md).

## Failure Handling

| Situation | Response |
|---|---|
| Order or revenue data unavailable | **Blocked.** Revenue work without revenue data is speculation |
| Customer intelligence unavailable | **Blocked.** Leaks cannot be located |
| Campaign and automation history unavailable | **Partial.** Structural opportunities only, lower confidence |
| New store, no history | Return a coverage-first baseline: lifecycle basics before optimisation, labelled pre-data |
| Target far beyond evidence | Plan the supportable portion, state the gap, name what else would have to change |
| No cadence headroom | Prioritise automations and AOV levers over additional sends, and say why |
| Margin constraints unknown | Ask once; otherwise rank non-discount levers first and flag the assumption |

Degraded outcomes set `status` and populate `unmet_requirements`. Never size an opportunity with an
invented figure (G3).
