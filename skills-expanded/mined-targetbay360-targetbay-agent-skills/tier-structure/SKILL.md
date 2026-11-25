---
name: tier-structure
description: Use when deciding whether a loyalty programme should have tiers, how many, at what thresholds, with which benefits, and what happens when a member falls out of one. Also use when existing tiers are not changing behaviour, when a top tier is empty, or when a threshold change is being considered.
license: MIT
metadata:
  targetbay.display_name: Tier Structure
  targetbay.version: "2.0.0"
  targetbay.category: loyalty
  targetbay.requires: loyalty.store_profile, loyalty.program_config, loyalty.tier_config, loyalty.member_profile, loyalty.program_analytics, loyalty.order_intelligence
  targetbay.composes: program-diagnosis, points-economics
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Tier Structure

## Purpose

Decide whether tiers are worth having here, and if so, what shape they take.

Tiers work by naming a distinction that already exists in the value distribution
([../../knowledge/loyalty-principles.md](../../knowledge/loyalty-principles.md)). Where no such
distinction exists, tiers invent a hierarchy members neither perceive nor pursue, and the store pays for
benefits that change nothing.

## When to Use

- Deciding whether to add tiers at all
- Setting or revising thresholds
- A top tier is empty, or a tier holds almost everyone
- Tier benefits cost money and their effect is unknown
- Downgrade policy needs deciding, or is causing complaints
- A qualification window was inherited and never examined

## When Not to Use

- The programme's basic health is unknown. Use
  [program-diagnosis](../program-diagnosis/SKILL.md) — this skill composes it.
- The question is what a point is worth. Use
  [points-economics](../points-economics/SKILL.md) — this skill composes it for benefit costing.
- No programme exists at all. Use [program-design](../program-design/SKILL.md), which decides
  whether tiers belong in the initial shape.
- Members in a tier are going quiet. Use [member-recovery](../member-recovery/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Customer value distribution | Tier count and thresholds derive from where customers cluster | Blocked |
| Current tier configuration | What members already hold | Blocked |
| Tier population and movement | Whether tiers currently do anything | Partial |
| Purchase frequency | The qualification window must match the purchase cycle | Blocked |
| Benefit costs | Tier benefits are ongoing margin commitments | Partial; structure withheld |
| Member behaviour by tier | Whether members act differently to reach or keep a tier | Partial; confidence lowered |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `loyalty.store_profile` | Currency, margin posture, vertical |
| `loyalty.program_config` | Programme rules the tiers sit inside |
| `loyalty.tier_config` | Current tiers; creating or amending definitions |
| `loyalty.member_profile` | Tier population, qualification state, activity |
| `loyalty.program_analytics` | Spend and behaviour by tier, and tier movement |
| `loyalty.order_intelligence` | Value distribution and purchase frequency |

## Decision Process

```
1. Read the value distribution               ← where do customers actually cluster
2. Decide whether tiers are warranted at all ← no clustering, no tiers
3. Derive the tier count from the clusters
4. Set thresholds and state the population under each
5. Choose benefits members would notice
6. Cost each benefit at its expected population
7. Decide the qualification window from purchase frequency
8. Decide downgrade policy at design time
9. Check no existing member is silently demoted
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/tier-rules.md](../../rules/tier-rules.md),
[../../rules/economics-rules.md](../../rules/economics-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Derive tier count from the value distribution, never from convention (T1). "Three tiers" is not a
  starting point.
- State the proportion of the base below, within reach of, and above every threshold (T2). A tier nobody
  enters is decoration and is reported as such.
- Every tier carries a benefit a member would notice, stated in member terms (T3). If it cannot be, the
  tier does not exist (G8).
- Cost every benefit at its expected tier population before proposing the structure (T4,
  [../../rules/economics-rules.md#E2](../../rules/economics-rules.md)).
- Decide downgrade policy at design time (T5). Deciding it later means changing what members hold.
- Never propose a threshold change that silently demotes qualified members (T6). If the structure has that
  effect, state it as its own finding with the affected count, and approve it separately (G12,
  [#S2](../../rules/safety-rules.md)).
- Derive the qualification window from observed purchase frequency (T7), not from the calendar year.
- Prefer fewer tiers where the distribution is ambiguous (T8) — adding a tier later is cheap, removing one
  members earned is not.
- Publishing a tier change is `high_impact` because members can see it
  ([#S5](../../rules/safety-rules.md)), and is approved with its affected counts
  ([#S6](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read distribution, current tiers, populations, frequency, benefit costs | `read_only` |
| ANALYZE | Locate clusters, assess current tiers against behaviour | `analysis` |
| PLAN | Count, thresholds, benefits, window, downgrade policy | `plan` |
| PREVIEW | State population under each threshold and every member movement it causes | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves; any demotion approved as a separate decision | — |
| EXECUTE | Stage tier definitions | `mutation` |
| EXECUTE | Publish the structure to members | `high_impact` |
| VERIFY | Confirm live tiers and populations match what was approved | `read_only` |
| MEASURE | Tier movement and per-tier behaviour over a full qualification window | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the value distribution and the
clusters found in it, the recommendation on whether tiers are warranted, and — where they are — the
proposed structure with, per tier, its threshold, the proportion of the base it captures, its benefits,
the cost of those benefits at expected population, and the behaviour it is meant to change.

Plus: the qualification window with its derivation, the downgrade policy, an explicit statement of any
existing member whose tier would change, and what was rejected.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

## Validation

- [ ] Value distribution read; tier count derived from clusters, not convention (T1)
- [ ] Population below, within reach of, and above each threshold stated (T2)
- [ ] Every tier has a benefit stated in member terms (T3)
- [ ] Every benefit costed at expected population (T4)
- [ ] Qualification window derived from purchase frequency (T7)
- [ ] Downgrade policy decided and stated (T5)
- [ ] Any existing member movement stated with counts, as its own finding (T6, G12, S2)
- [ ] The option of no tiers, or fewer tiers, explicitly considered (T8, G7)
- [ ] Publication treated as `high_impact` with counts shown (S5, S6)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the structure | `plan` | None |
| Stage tier definitions | `mutation` | Preview, then confirm |
| Publish the structure to members | `high_impact` | Explicit, with per-tier counts |
| Demote members who already qualified | `destructive` | Explicit, separate, with count and notice (S2, S8) |

## Examples

**"We want gold, silver and bronze tiers."**
The value distribution shows two clusters, not three, with a long thin tail above. Recommends two tiers
rather than three, states the proportion captured by each, and notes that a third tier at the level
requested would hold under one percent of the base — decoration under T2. Prefers the smaller structure on
T8, since adding a third tier later is cheap.

**"Our top tier benefits are too expensive."**
Costs each benefit at its actual tier population and finds one benefit accounts for most of the spend while
appearing in no member behaviour. Recommends removing that benefit rather than raising the threshold,
because raising the threshold would demote members who already qualified — a separate, `destructive`
decision under T6 that the cost problem does not justify.

## Failure Handling

| Situation | Response |
|---|---|
| `loyalty.order_intelligence` unavailable | **Blocked.** Thresholds cannot be derived without a value distribution (T1, T2) |
| `loyalty.tier_config` unavailable | **Blocked.** Cannot read what members currently hold; risk of silent demotion (T6) |
| Purchase frequency unavailable | **Blocked.** The qualification window would be arbitrary (T7) |
| Benefit costs unavailable | **Partial.** Propose structure without benefits costed, state that affordability is unverified, withhold the recommendation to publish |
| Tier movement data unavailable | **Partial.** Assess structure on distribution alone; state that current tier effectiveness is unmeasured |
| Distribution shows no clusters | Recommend no tiers, with the evidence. That is a valid and frequently correct answer (T1, G8) |
| Proposed change demotes existing members | Stop, state the count and value, and require separate approval before continuing (T6, S2) |

Degraded outcomes set `status` and populate `unmet_requirements`.
