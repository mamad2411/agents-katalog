---
name: referral-program
description: Use when designing, pricing or fixing a referral programme — deciding the incentive on each side, what event qualifies a referral, how and where members are asked, what fraud controls are needed, and whether referred customers are actually worth acquiring. Also use when referral volume is high but the customers do not stick.
license: MIT
metadata:
  targetbay.display_name: Referral Programme
  targetbay.version: "2.0.0"
  targetbay.category: referral
  targetbay.requires: loyalty.store_profile, loyalty.referral_program, loyalty.member_profile, loyalty.order_intelligence, loyalty.customer_intelligence, loyalty.program_analytics, loyalty.suppression_and_consent
  targetbay.composes: program-diagnosis, points-economics
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Referral Programme

## Purpose

Decide what a referred customer is worth, what it is sensible to pay for one, and how the programme is
structured so that what it pays for is a customer rather than a signup.

Referral shares a member identity with loyalty and almost nothing else: it is an acquisition channel, and
it is costed, measured and defended against fraud like one
([../../rules/referral-rules.md#F1](../../rules/referral-rules.md)).

## When to Use

- Designing a referral programme
- Setting or revising the incentive on either side
- Referral volume is high but referred customers do not return
- Deciding what event qualifies a referral
- Fraud or incentive farming is suspected
- Deciding where and when members are asked to refer

## When Not to Use

- The question is about rewarding existing behaviour rather than acquiring customers. Use
  [points-economics](../points-economics/SKILL.md) or
  [tier-structure](../tier-structure/SKILL.md).
- No programme exists at all and the whole shape is undecided. Use
  [program-design](../program-design/SKILL.md), which delegates here.
- Members are going quiet. Use [member-recovery](../member-recovery/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Existing referral configuration | What already runs | Blocked when one exists |
| Referred-cohort retention | Whether referred customers are worth acquiring | Partial; value unsizable |
| Acquisition cost from other channels | The comparison that prices the incentive | Partial; incentive unpriceable |
| Customer value by acquisition source | Whether referral customers differ | Partial |
| Existing acquisition offers | The incentive must not beat them | Blocked |
| Consent and messaging state | Where and how members can be asked | Partial |
| Fraud signals and controls available | What the design can actually defend against | Partial; controls unverifiable |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `loyalty.store_profile` | Currency, margin posture, vertical |
| `loyalty.referral_program` | Current configuration, incentives, fraud controls, results |
| `loyalty.member_profile` | Who refers, and how often |
| `loyalty.order_intelligence` | Referred-cohort orders, AOV, repeat behaviour |
| `loyalty.customer_intelligence` | Retention of referred customers against other sources |
| `loyalty.program_analytics` | Referral volume, qualification and conversion |
| `loyalty.suppression_and_consent` | Where and how members may be asked |

## Decision Process

```
1. Measure referred-cohort retention          ← against other acquisition sources
2. Derive what a referred customer is worth
3. Compare against other acquisition costs    ← the ceiling on the incentive
4. Choose the qualifying event                ← a retained order, not a signup
5. Decide the split and justify each side
6. Design fraud controls, and cost them
7. Decide where and when members are asked
8. Define the measurement as retention, not volume
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/referral-rules.md](../../rules/referral-rules.md),
[../../rules/economics-rules.md](../../rules/economics-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Price the incentive against other acquisition costs and the referred customer's observed value (F1),
  never against the referrer's enthusiasm.
- Qualify on a completed, retained order past the return window (F2). An incentive on signup buys signups.
- State the split and justify each side separately from this store's data (F3). Two-sided is not
  automatically correct.
- Design fraud controls at design time and state what they cost in legitimate referrals blocked (F4).
- Check the incentive against existing acquisition offers before proposing it (F5). If referring pays
  better than buying, the programme is an arbitrage.
- Measure referred-cohort retention, not referral volume (F6). Report volume only alongside retention.
- Never claim referred customers are better without accounting for selection (G5, E9) — members refer
  people like themselves.
- Asking is part of the design and is bound by consent and frequency (F7, G13). Reconcile it with whatever
  else is contacting the member.
- Any point-denominated incentive carries its liability projection (E3,
  [#S3](../../rules/safety-rules.md)).
- Activating a referral programme is `high_impact` — it creates obligations and reaches people outside the
  store's own list ([#S5](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read current configuration, cohorts, acquisition costs, offers, consent | `read_only` |
| ANALYZE | Referred-cohort retention and value; the incentive ceiling | `analysis` |
| PLAN | Qualifying event, split, fraud controls, asking surfaces, measurement | `plan` |
| PREVIEW | State the incentive, its cost at expected volume, and its liability | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves activation specifically | — |
| EXECUTE | Stage referral configuration | `mutation` |
| EXECUTE | Activate the programme | `high_impact` |
| VERIFY | Confirm live configuration matches what was approved | `read_only` |
| MEASURE | Referred-cohort retention against other sources, over a full purchase cycle | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: referred-cohort retention against
other acquisition sources, the derived value of a referred customer, the incentive ceiling and the proposed
split with justification for each side, the qualifying event, the fraud controls with their cost in blocked
legitimate referrals, the asking plan within consent, and the measurement definition.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: what was rejected, particularly any incentive that failed the comparison against existing offers.

## Validation

- [ ] Referred-cohort retention measured against other acquisition sources (F6)
- [ ] Incentive priced against acquisition cost and observed value (F1)
- [ ] Qualifying event is a completed, retained order (F2)
- [ ] Split stated with a justification for each side (F3)
- [ ] Fraud controls designed and their cost in legitimate referrals stated (F4)
- [ ] Incentive checked against existing acquisition offers (F5)
- [ ] Selection accounted for in any quality claim (G5, E9)
- [ ] Asking plan sits inside consent and frequency (F7, G13)
- [ ] Point-denominated incentives carry a liability projection (E3, S3)
- [ ] Measurement defined as retention, with volume reported alongside not instead

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the design | `plan` | None |
| Stage referral configuration | `mutation` | Preview, then confirm |
| Activate the programme | `high_impact` | Explicit, with cost at expected volume shown |
| Change an incentive members are already earning against | `destructive` | Explicit, with affected count (S2) |

## Examples

**"Referrals are up 300% but revenue hasn't moved."**
Finds the programme qualifies on signup, so it is paying for email addresses. Referred-cohort retention is
far below every other acquisition source, and a cluster of referrals shares payment instruments with their
referrers. Recommends moving qualification to a retained first order, adding the collusion control, and
states what the control will cost in legitimate referrals. Reframes the measurement as referred-cohort
retention, because volume was never the thing worth counting.

**"What should we pay for a referral?"**
Derives referred-customer value from the existing cohort and compares it against paid acquisition cost,
which sets the ceiling. Finds the proposed two-sided incentive would exceed the store's own new-customer
welcome offer, so members would be better off referring than buying. Recommends a lower referrer-side
incentive and a referred-side incentive matched to the existing welcome offer, and states the liability
projection for the points-denominated half.

## Failure Handling

| Situation | Response |
|---|---|
| `loyalty.referral_program` unavailable | **Blocked** when a programme exists; cannot read what already runs |
| Referred-cohort data unavailable | **Partial.** Design on reasoning, state that the incentive ceiling is unverified, lower confidence |
| Acquisition cost from other channels unavailable | **Partial.** Report the incentive as unpriceable against alternatives and say what data would price it (F1) |
| Existing acquisition offers unknown | **Blocked.** F5 cannot be checked, and an unchecked incentive can be an arbitrage |
| Fraud signals not exposed | **Partial.** State which controls cannot be implemented and what exposure that leaves (F4) |
| Cohort too small to measure retention | **Partial.** Report the volume, state that retention is not yet measurable, and define when it will be |
| Asked to reward shares or clicks | Refuse, cite [F2](../../rules/referral-rules.md), and state what that would buy |

Degraded outcomes set `status` and populate `unmet_requirements`.
