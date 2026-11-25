---
name: member-recovery
description: Use when members are going quiet — earning has slowed or stopped, balances are ageing without redemption, members are about to fall out of a tier, or points are approaching expiry. Decides who is worth intervening with, what the intervention is, and where intervening is not worth it.
license: MIT
metadata:
  targetbay.display_name: Member Recovery
  targetbay.version: "2.0.0"
  targetbay.category: retention
  targetbay.requires: loyalty.store_profile, loyalty.member_profile, loyalty.points_ledger, loyalty.redemption, loyalty.tier_config, loyalty.customer_intelligence, loyalty.order_intelligence, loyalty.suppression_and_consent, loyalty.messaging
  targetbay.composes: program-diagnosis
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Member Recovery

## Purpose

Find members who are leaving the programme, decide which of them are worth an intervention, and choose the
intervention that fits what is actually happening.

A member whose earning slows is usually still buying; a member whose earning stopped often stopped buying
earlier ([../../knowledge/member-lifecycle.md](../../knowledge/member-lifecycle.md)). The gap between
those two states is the window this skill works in.

## When to Use

- Member activity is declining and the size of the problem is unknown
- Balances are ageing without redemption
- Members are approaching a tier downgrade
- Points are approaching expiry and nobody has decided what to do
- Deciding which quiet members are worth contacting at all

## When Not to Use

- The whole programme's health is in question. Use
  [program-diagnosis](../program-diagnosis/SKILL.md) — this skill composes it.
- Members never activated in the first place. That is reachability; use
  [points-economics](../points-economics/SKILL.md).
- The tier structure itself is the problem. Use
  [tier-structure](../tier-structure/SKILL.md).
- The customer has lapsed from the store entirely and the question is general win-back rather than
  programme-specific — that belongs to the email and SMS marketing product, not here.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Member activity relative to own pattern | "Quiet" is relative to that member, not to a store threshold | Blocked |
| Balance and its ageing | Distinguishes engaged-unredeemed from departed-holding | Blocked |
| Redemption history | Whether the member ever activated | Partial |
| Tier state and proximity to downgrade | The strongest available intervention moment | Partial |
| Expiry schedule | What is about to be lost, and to whom | Partial |
| Purchase behaviour | Whether the member left the programme or the store | Partial; intervention misdirected |
| Consent and frequency headroom | Whether they can be contacted at all | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `loyalty.store_profile` | Currency, vertical, plan limits |
| `loyalty.member_profile` | Activity recency, tier, balance |
| `loyalty.points_ledger` | Earn and burn pattern, balance ageing, expiry exposure |
| `loyalty.redemption` | Whether the member ever redeemed |
| `loyalty.tier_config` | Downgrade thresholds and timing |
| `loyalty.customer_intelligence` | Whether disengagement extends beyond the programme |
| `loyalty.order_intelligence` | Purchase pattern and its own interval |
| `loyalty.suppression_and_consent` | Eligibility, channel, frequency headroom |
| `loyalty.messaging` | Dispatch — only after explicit approval |

## Decision Process

```
1. Define quiet relative to each member's own pattern
2. Separate programme disengagement from store disengagement
3. Classify the state                        ← never activated / engaged-unredeemed / slowing / departed
4. Size each group and its held value
5. Decide which groups are worth an intervention at all
6. Choose the intervention per state         ← the moment matters more than the message
7. Check frequency headroom against everything else contacting them
8. Stage so the first cohort's response informs the rest
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/economics-rules.md](../../rules/economics-rules.md),
[../../rules/tier-rules.md](../../rules/tier-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Derive "quiet" from the member's own interval, never a store-wide fixed number (G3).
- Separate programme disengagement from store disengagement before choosing an intervention. A member who
  left the store is not recovered by a points reminder, and treating the two the same wastes the contact.
- Classify by state, because the interventions differ: a **never activated** member needs reachability, an
  **engaged-unredeemed** member needs a redemption prompt, a **slowing** member needs the tier or expiry
  moment, a **departed** member usually needs nothing from this product.
- Intervene at the moment, not on a schedule. Approaching a downgrade or an expiry is a real deadline, and
  it is the strongest lever the programme has — which is also why it is the one most easily abused
  ([../../knowledge/loyalty-principles.md](../../knowledge/loyalty-principles.md)).
- Never manufacture urgency. An expiry warning states a real date; a tier warning states a real threshold.
  Inventing either is inventing data (G3).
- Never propose a balance adjustment as a recovery tactic without its count, value and liability impact
  ([#S4](../../rules/safety-rules.md), E3).
- Programme messaging is marketing and competes for the same frequency budget as everything else
  contacting the member (G13). Count it, and where headroom is absent, recommend replacing a lower-value
  contact rather than adding one.
- State explicitly which groups are not worth intervening with, and why. Recovering everybody is how a
  recovery programme becomes a fatigue programme.
- Dispatch is `high_impact`: staged, sized, approved per cohort
  ([#S5](../../rules/safety-rules.md), [#S6](../../rules/safety-rules.md),
  [#S10](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read member activity, balances, ageing, tiers, orders, consent | `read_only` |
| ANALYZE | Derive per-member intervals; classify state; size each group | `analysis` |
| PLAN | Choose interventions and moments; check frequency headroom | `recommendation` |
| PREVIEW | State each cohort's size, channel, timing and message intent | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the first cohort specifically | — |
| EXECUTE | Dispatch to the approved cohort | `high_impact` |
| VERIFY | Confirm what was sent matches what was approved | `read_only` |
| MEASURE | Earning and redemption resumption over a full purchase interval | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the member population classified by
state with each group's size and held value, the intervention chosen per group with its moment and its
evidence, the groups deliberately left alone with the reason, the frequency headroom check, and the staging
plan with per-cohort counts.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

## Validation

- [ ] "Quiet" derived per member from their own interval, not a fixed threshold (G3)
- [ ] Programme disengagement separated from store disengagement
- [ ] Every member classified into a state, and the intervention follows from the state
- [ ] Each group sized, with its held value
- [ ] Groups not worth intervening with named explicitly, with reasons
- [ ] No manufactured urgency; every stated deadline is a real one (G3)
- [ ] Any balance adjustment carries count, value and liability impact (S4, E3)
- [ ] Frequency headroom counted against all other contact (G13)
- [ ] Cohorts sized before approval and approved individually (S6, S10)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Contact members | `high_impact` | Explicit, per cohort, with the count shown |
| Adjust balances as an intervention | `high_impact` | Explicit, with count, value and liability impact (S4) |

## Examples

**"Our loyalty members are going quiet."**
Splits the quiet population and finds most of it is members who never redeemed once — a reachability
problem rather than a recovery one — and routes that group to
[points-economics](../points-economics/SKILL.md). Of the remainder, one cohort is slowing while still
purchasing and sits close to a tier threshold; recommends the downgrade-proximity moment for that group
only. Identifies a third group that stopped buying from the store entirely months ago and recommends no
programme intervention for them at all, since a points reminder does not address why they left.

**"Points are about to expire for 12,000 members."**
Sizes the held value and separates members who are still active — for whom the expiry notice is a genuine,
useful deadline — from members long departed, for whom it is a message about something they no longer care
about. Recommends notifying the first group with the real date, notes that the second group's expiry is a
liability question rather than a messaging one, and checks frequency headroom before proposing any send.

## Failure Handling

| Situation | Response |
|---|---|
| `loyalty.points_ledger` unavailable | **Blocked.** Balance ageing is the basis for classification |
| `loyalty.suppression_and_consent` unavailable | **Blocked.** Contacting members without eligibility data is not permitted (S12) |
| Order history unavailable | **Partial.** Programme and store disengagement cannot be separated; state that interventions may be misdirected |
| Per-member intervals underivable | **Partial.** Use programme-level activity with lower confidence, and say the threshold is not member-relative (G3) |
| `loyalty.messaging` unavailable | **Partial.** Produce the cohorts and the plan; state that dispatch is owned elsewhere and stop before it |
| No frequency headroom | Recommend replacing an existing lower-value contact rather than adding one (G13) |
| Most quiet members never activated | Report that as the finding and route it out; this is a reachability problem, not a recovery one |

Degraded outcomes set `status` and populate `unmet_requirements`.
