---
name: points-economics
description: Use when deciding what a point is worth, what the earn rate should be, how rewards should be priced, whether the programme is affordable, or what to do about rising liability. Also use when redemption is low, when someone proposes expiring points, or when a generosity change is being considered in either direction.
license: MIT
metadata:
  targetbay.display_name: Points Economics
  targetbay.version: "2.0.0"
  targetbay.category: economics
  targetbay.requires: loyalty.store_profile, loyalty.program_config, loyalty.points_ledger, loyalty.reward_catalog, loyalty.redemption, loyalty.program_analytics, loyalty.order_intelligence
  targetbay.composes: program-diagnosis
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Points Economics

## Purpose

Decide what a point is worth, what issuing it costs, and whether the programme's arithmetic works.

Most loyalty decisions that look like marketing decisions are margin decisions in disguise. An earn rate
is a per-order cost carried whether or not it changes behaviour; a reward price is a margin commitment;
outstanding points are debt ([../../knowledge/loyalty-principles.md](../../knowledge/loyalty-principles.md)).

## When to Use

- Setting or changing an earn rate
- Pricing rewards, or adding one to the catalogue
- Liability is rising and the affordability is unclear
- Redemption rate is low and the cause may be reachability
- Someone proposes expiring points
- A generosity increase is being considered
- The programme's cost needs stating before a budget conversation

## When Not to Use

- The question is whether the programme works at all. Use
  [program-diagnosis](../program-diagnosis/SKILL.md) — this skill composes it.
- The question is tier thresholds and benefits. Use
  [tier-structure](../tier-structure/SKILL.md), which composes this skill for the costing.
- No programme exists yet. Use [program-design](../program-design/SKILL.md).
- The cost in question is an acquisition incentive. Use
  [referral-program](../referral-program/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Current earn and burn configuration | The starting arithmetic | Blocked |
| Reward catalogue with point prices and costs | Derives the point's monetary value | Blocked |
| Outstanding liability with ageing | What is already owed | Blocked |
| Redemption rate and behaviour | Expected cost of issuance | Partial; cost becomes a range |
| Margin posture | Whether the rate is affordable at all | Partial; rate cannot be responsibly set |
| AOV and purchase frequency | Time to the first meaningful reward | Blocked |
| Reward stock and fulfilment capacity | Whether a reward can be honoured | Partial; catalogue changes withheld |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `loyalty.store_profile` | Currency, margin posture, plan limits |
| `loyalty.program_config` | Earn rules, expiry policy as configured |
| `loyalty.points_ledger` | Issuance, redemption, outstanding liability and ageing |
| `loyalty.reward_catalog` | Point prices, costs, stock; creating or amending rewards |
| `loyalty.redemption` | Observed redemption rate and what converts |
| `loyalty.program_analytics` | Earn and burn by tier and cohort |
| `loyalty.order_intelligence` | AOV and frequency, for reachability arithmetic |

## Decision Process

```
1. Derive the point's monetary value           ← from the catalogue, not asserted
2. Measure observed redemption rate            ← the expected-cost multiplier
3. Compute current cost of issuance            ← point value × redemption × volume, against margin
4. Read liability and its ageing
5. Derive time to the first meaningful reward  ← in orders, from this store's AOV
6. Identify which side is broken               ← issuance, reachability, or catalogue
7. Model the proposed change                   ← cost, liability, reachability, all three
8. Check redemption capacity for any new reward
9. Stage the change so it is observable before it is complete
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/economics-rules.md](../../rules/economics-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- State the point's monetary value explicitly, derived from the reward catalogue (E1).
- Never recommend an earn rate without its liability projection over a stated horizon (E3,
  [#S3](../../rules/safety-rules.md)).
- Cost issuance against margin, not against revenue (E2, E10). Where margin is unavailable, state that the
  rate cannot be responsibly set and report the gap rather than choosing one anyway.
- Treat redemption rate as the health metric; a low rate is a finding about reachability or catalogue, not
  a saving (E4).
- Breakage is not a business model (E5). A recommendation whose economics depend on points going unredeemed
  is rejected, and the reason is stated.
- Derive time to the cheapest meaningful reward in orders, from this store's AOV and frequency (E6). Never
  assert a target in points.
- Check cost, stock and fulfilment capacity before proposing any reward
  ([#S11](../../rules/safety-rules.md), E7).
- Any change that reduces what members already earned — devaluation, reward repricing upward, expiry — is
  stated as its own finding with the affected count and value, and approved separately (G12,
  [#S2](../../rules/safety-rules.md)).
- Expiry is `destructive` and requires inspection, notice and explicit approval (E8,
  [#S8](../../rules/safety-rules.md)).
- Never claim a generosity change caused a behaviour change without accounting for selection (G5, E9).
- Stage changes so the first cohort's redemption response is observed before the rest (G16).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read configuration, catalogue, ledger, redemptions, orders | `read_only` |
| ANALYZE | Point value, issuance cost, liability ageing, reachability | `analysis` |
| PLAN | Model the change across cost, liability and reachability | `recommendation` |
| PREVIEW | State each change with its arithmetic and its affected population | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves; any member-facing reduction approved separately | — |
| EXECUTE | Amend rewards or earn configuration | `mutation` |
| EXECUTE | Publish a change members can see, or expire points | `high_impact` / `destructive` |
| VERIFY | Confirm live configuration matches what was approved | `read_only` |
| MEASURE | Redemption rate and liability trajectory over a full purchase cycle | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) stating: the derived point value with its
derivation, current issuance cost against margin, liability with ageing, time to first meaningful reward in
orders, and which side of the system is broken.

Each proposed change carries its cost arithmetic, its liability projection over a stated horizon, its
reachability effect, and — where it reduces anything members hold — its affected count and value as a
separate finding. Recommendations conform to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: what was rejected, particularly any proposal whose economics relied on breakage.

## Validation

- [ ] Point value derived from the catalogue and stated (E1)
- [ ] Every rate recommendation carries a liability projection with a horizon (E3, S3)
- [ ] Cost computed against margin, or the absence of margin data declared (E2)
- [ ] Redemption rate reported; a low rate treated as a finding (E4)
- [ ] No recommendation depends on breakage (E5)
- [ ] Reachability expressed in orders, derived from store AOV (E6)
- [ ] Stock and fulfilment capacity checked for every proposed reward (E7, S11)
- [ ] Any member-facing reduction stated separately with count and value (G12, S2)
- [ ] Expiry, if proposed, carries inspection, notice and its own approval (E8, S8)
- [ ] Changes staged so the first cohort is observable (G16)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Amend a draft reward or staged configuration | `mutation` | Preview, then confirm |
| Publish a change members can see | `high_impact` | Explicit, with affected count and value shown |
| Reduce earned value, reprice upward, or expire points | `destructive` | Explicit, after inspection, with notice period stated (S2, S8) |

## Examples

**"Can we double our points earn rate to boost loyalty?"**
Derives the current point value from the catalogue, computes issuance cost at the observed redemption rate,
and projects liability under the doubled rate. Finds the cost lands below the store's stated margin floor
only if redemption stays at its current low level — which is to say, the proposal is affordable only if it
does not work. Rejects it, and identifies reachability as the actual constraint: the cheapest reward is far
enough away in orders that most members never reach it. Recommends repricing the entry reward instead,
staged on one cohort.

**"Our liability is too high — let's expire points older than a year."**
Reports how many members and how much value the expiry would touch, and that a substantial share sits with
members who are currently active. Flags the proposal as `destructive` under
[#S8](../../rules/safety-rules.md), requiring inspection, a notice period and separate approval. Notes that
the liability is a symptom of low redemption and proposes addressing redemption first, since expiry
converts an obligation into a customer-experience problem without changing the underlying arithmetic.

## Failure Handling

| Situation | Response |
|---|---|
| `loyalty.points_ledger` unavailable | **Blocked.** No liability position means no responsible economics (G4) |
| `loyalty.reward_catalog` unavailable | **Blocked.** Point value cannot be derived (E1) |
| Margin data unavailable | **Partial.** State that the earn rate cannot be responsibly set, report the cost as a range against revenue, and record the gap (E2) |
| Redemption data unavailable | **Partial.** Present issuance cost as a range across plausible redemption rates, and say so |
| AOV or frequency unavailable | **Blocked.** Reachability cannot be derived, and reachability is usually the binding constraint (E6) |
| Stock or capacity unknown for a proposed reward | Withhold that reward from the recommendation (E7, S11) |
| Asked to plan around breakage | Refuse, cite [E5](../../rules/economics-rules.md), and report what redemption would need to be for the programme to work |
| Programme too new for redemption behaviour | **Partial.** Model across a range and state that the range is not yet narrowed by evidence |

Degraded outcomes set `status` and populate `unmet_requirements`.
