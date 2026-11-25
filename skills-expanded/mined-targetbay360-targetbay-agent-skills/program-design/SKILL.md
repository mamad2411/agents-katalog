---
name: program-design
description: Use when a store has no loyalty programme and is deciding whether to run one and what shape it should take, or when an existing programme is being rebuilt from scratch. Decides whether a programme is warranted at all, what it rewards, how members enrol, and which mechanics belong in the first version.
license: MIT
metadata:
  targetbay.display_name: Programme Design
  targetbay.version: "2.0.0"
  targetbay.category: planning
  targetbay.requires: loyalty.store_profile, loyalty.program_config, loyalty.order_intelligence, loyalty.customer_intelligence, loyalty.reward_catalog, loyalty.suppression_and_consent
  targetbay.composes: program-diagnosis, points-economics, tier-structure, referral-program
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Programme Design

## Purpose

Decide whether this store should run a loyalty programme, and what the first version of it looks like.

The honest answer is sometimes no. A store whose customers buy once by nature, or whose margin cannot
carry issuance, gets a cost and a maintenance burden rather than retention
([../../knowledge/loyalty-principles.md](../../knowledge/loyalty-principles.md)). This skill establishes
that first and designs second.

## When to Use

- No programme exists and one is being considered
- An existing programme is being rebuilt rather than adjusted
- Deciding what the first version should and should not include
- Deciding how members enrol and what the programme rewards
- Someone wants a programme because a competitor has one

## When Not to Use

- A programme exists and needs assessing. Use
  [program-diagnosis](../program-diagnosis/SKILL.md).
- Only the economics need revisiting. Use
  [points-economics](../points-economics/SKILL.md).
- Only the tiers need revisiting. Use [tier-structure](../tier-structure/SKILL.md).
- Only referral needs designing. Use [referral-program](../referral-program/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Purchase frequency and repeat behaviour | Whether repeat purchase is possible in this category at all | Blocked |
| Value distribution | Whether there is a distinction worth naming | Blocked |
| Margin posture | Whether issuance is affordable | Partial; economics withheld |
| AOV | Reachability of any reward | Blocked |
| Existing programme state, if any | What members already hold | Blocked when one exists |
| Consent and messaging state | How a programme would be communicated | Partial |
| Product catalogue shape | What can be offered as a reward | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `loyalty.store_profile` | Vertical, currency, margin posture, plan limits |
| `loyalty.program_config` | Whether a programme exists and what it currently is |
| `loyalty.order_intelligence` | Frequency, AOV, value distribution, repeat behaviour |
| `loyalty.customer_intelligence` | Lifecycle distribution and engagement |
| `loyalty.reward_catalog` | What can be offered, at what cost |
| `loyalty.suppression_and_consent` | How the programme could be communicated at all |

## Decision Process

```
1. Test whether repeat purchase is possible here   ← category, frequency, catalogue
2. Test whether the margin can carry issuance      ← delegate to points-economics
3. Decide whether a programme is warranted at all  ← "no" is a legitimate output
4. Decide what the programme rewards               ← spend, frequency, or behaviour
5. Decide enrolment                                ← automatic, opt-in, or purchase-triggered
6. Derive the entry reward and its reachability
7. Decide which mechanics belong in v1             ← fewest that change behaviour
8. Delegate tiers and referral as separate decisions
9. Define the measurement before launch
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/economics-rules.md](../../rules/economics-rules.md),
[../../rules/tier-rules.md](../../rules/tier-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Establish that repeat purchase is possible in this category before designing anything for it. A store
  selling a once-in-a-decade purchase does not have a loyalty problem to solve, and saying so is the
  correct output.
- "A competitor has one" is not evidence (G2). Design against this store's own behaviour data.
- Delegate affordability to [points-economics](../points-economics/SKILL.md) rather than estimating it
  here (E2, E3).
- Prefer the fewest mechanics that change behaviour (G7). Tiers, multipliers and challenges are each
  additions to v1 that must earn their place; the default v1 has none of them
  ([../../knowledge/loyalty-principles.md](../../knowledge/loyalty-principles.md)).
- Delegate tiers to [tier-structure](../tier-structure/SKILL.md), which will frequently answer that the
  value distribution does not support them (T1).
- Delegate referral to [referral-program](../referral-program/SKILL.md); it is an acquisition decision with
  different economics (F1).
- Derive the entry reward so it is reachable in a plausible number of orders (E6). This is the single most
  influential parameter and it is derived, never chosen.
- Decide downgrade and expiry policy at design time, not after members hold something (T5, E8).
- Enrolment must not be treated as marketing consent (G13). State how the programme is communicated within
  existing consent, and reconcile it with whatever else contacts these customers.
- Define the measurement before launch, accounting for selection (G5, E9). A programme launched without a
  pre-enrolment baseline can never be evaluated honestly.
- Launching is `high_impact`: it creates obligations to real members and is approved explicitly
  ([#S5](../../rules/safety-rules.md)).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read behaviour, distribution, margin, catalogue, consent, existing state | `read_only` |
| ANALYZE | Test feasibility; delegate affordability and structure | `analysis` |
| PLAN | Shape, enrolment, entry reward, v1 mechanics, policies, measurement | `plan` |
| PREVIEW | State the whole design, its cost, its obligations and its baseline | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the launch specifically | — |
| EXECUTE | Stage programme configuration and catalogue | `mutation` |
| EXECUTE | Launch to members | `high_impact` |
| VERIFY | Confirm live configuration matches what was approved | `read_only` |
| MEASURE | Against the pre-launch baseline, over a full purchase cycle | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing either a reasoned recommendation not to
run a programme, or a complete v1 design: what it rewards, how members enrol, the entry reward and its
reachability in orders, the mechanics included and — explicitly — the mechanics excluded from v1 and why,
the expiry and downgrade policies, the communication plan within consent, and the measurement design with
its pre-launch baseline.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

## Validation

- [ ] Repeat-purchase feasibility tested before design begins
- [ ] Affordability delegated to `points-economics`, not estimated here (E2)
- [ ] Entry reward reachability derived in orders from this store's AOV (E6)
- [ ] v1 mechanics justified individually; excluded mechanics listed with reasons (G7, G8)
- [ ] Tiers delegated, and their absence from v1 treated as the default (T1, T8)
- [ ] Referral delegated as a separate decision (F1)
- [ ] Expiry and downgrade policy decided at design time (T5, E8)
- [ ] Communication planned within consent; enrolment not treated as consent (G13)
- [ ] Pre-launch baseline captured, and the measurement accounts for selection (G5, E9)
- [ ] "Do not run a programme" considered as a genuine option

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the design | `plan` | None |
| Stage configuration and catalogue | `mutation` | Preview, then confirm |
| Launch the programme to members | `high_impact` | Explicit, with obligations and expected cost shown |

## Examples

**"Our competitor launched a loyalty programme — we need one."**
Finds the store's customers buy roughly once every eighteen months in a category where that is normal.
Reports that a points programme cannot influence a purchase cycle that long, and that the retention
question here is a product and lifecycle one rather than a loyalty one. Recommends against a programme,
with the frequency distribution as evidence, and states what would change the answer.

**"Design us a loyalty programme."**
Frequency and value distribution support one. Delegates affordability, which sets the earn rate ceiling,
and derives an entry reward reachable in three orders at this store's AOV. Recommends a v1 with no tiers —
the distribution shows a single cluster — no multipliers and no challenges, enrolment triggered on first
purchase, and expiry policy decided now rather than later. Captures the pre-enrolment baseline as a launch
prerequisite, because without it the programme's effect can never be separated from selection.

## Failure Handling

| Situation | Response |
|---|---|
| `loyalty.order_intelligence` unavailable | **Blocked.** Feasibility, reachability and distribution all depend on it |
| Margin unavailable | **Partial.** Produce the shape; withhold the earn rate and state that affordability is unverified (E2) |
| A programme already exists | Route to [program-diagnosis](../program-diagnosis/SKILL.md) first; designing over an existing programme risks changing what members hold (G6, S2) |
| Repeat purchase not plausible in this category | Recommend against a programme, with evidence. This is a successful result, not a failure |
| Consent state unreadable | **Partial.** Produce the design; state that the communication plan is unverified and must not be executed |
| Catalogue cannot support a reachable reward | Report it as the binding constraint; the design question becomes a catalogue question |
| Asked to launch without a baseline | State that the programme will not be evaluable and require an explicit decision to accept that (G5) |

Degraded outcomes set `status` and populate `unmet_requirements`.
