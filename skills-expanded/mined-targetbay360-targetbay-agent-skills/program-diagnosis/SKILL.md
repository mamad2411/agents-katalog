---
name: program-diagnosis
description: Use when the question is how a loyalty programme is actually performing — whether enrolment converts into earning and redeeming, where members drop out, how liability is ageing, whether tiers do anything, and whether the programme changes behaviour at all. This is the assessment skill every other loyalty skill routes through; use it before designing, repricing or restructuring anything.
license: MIT
metadata:
  targetbay.display_name: Programme Diagnosis
  targetbay.version: "2.0.0"
  targetbay.category: loyalty
  targetbay.requires: loyalty.store_profile, loyalty.program_config, loyalty.member_profile, loyalty.points_ledger, loyalty.redemption, loyalty.program_analytics, loyalty.order_intelligence, loyalty.customer_intelligence
  targetbay.risk_level: analysis
  targetbay.execution_mode: analyze_only
  targetbay.status: foundation
---

# Programme Diagnosis

## Purpose

Establish what a loyalty programme is actually doing, before anyone changes it.

Every other skill in this plugin needs the same foundation: the participation funnel, the liability
position, the redemption picture, and an honest statement of whether the programme changes behaviour.
Deriving it once, here, is what stops five skills inventing five different definitions of a healthy
programme.

## When to Use

- Assessing an existing programme's health
- Before redesigning, repricing or restructuring anything
- Enrolment is growing and nobody knows whether it matters
- Liability is rising and the cause is unclear
- Someone asks whether the programme is worth keeping
- Before claiming the programme drove any result

## When Not to Use

- No programme exists and one is being considered. Use
  [program-design](../program-design/SKILL.md).
- The diagnosis is done and the question is what a point should be worth. Use
  [points-economics](../points-economics/SKILL.md).
- The question is specifically about tier structure. Use
  [tier-structure](../tier-structure/SKILL.md).
- Specific members are going quiet. Use [member-recovery](../member-recovery/SKILL.md).
- The question is about acquiring new customers through members. Use
  [referral-program](../referral-program/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Current programme configuration | What the rules actually are | Blocked |
| Member population by state | The participation funnel | Blocked |
| Points ledger with ageing | Liability position and what it means | Blocked |
| Redemption events and outcomes | Whether the promise is being kept | Partial; health unassessable |
| Order history for members and non-members | Behaviour comparison | Partial; effect not isolatable |
| Pre-enrolment behaviour per member | The only honest way to isolate effect | Partial; confidence lowered |
| Tier population and movement | Whether tiers do anything | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `loyalty.store_profile` | Vertical, currency, margin posture, programme age |
| `loyalty.program_config` | The rules as currently configured |
| `loyalty.member_profile` | Enrolment, tier, balance, activity recency |
| `loyalty.points_ledger` | Earn and burn events, outstanding liability and its ageing |
| `loyalty.redemption` | Redemption rate, what is redeemed, whether it converts |
| `loyalty.program_analytics` | Enrolment, activity and spend by tier |
| `loyalty.order_intelligence` | Member and non-member purchase behaviour |
| `loyalty.customer_intelligence` | Lifecycle stage and engagement, inside and outside the programme |

## Decision Process

```
1. Read the configuration as it actually is    ← not as anyone remembers it
2. Build the participation funnel              ← enrolled / earning / redeeming
3. Measure time to first redemption            ← the activation event
4. Read liability and its ageing               ← size means nothing without age
5. Measure redemption rate and its direction
6. Assess tier structure against behaviour     ← do tiers change anything
7. Attempt to isolate programme effect         ← and say so honestly when it cannot be
8. Name the binding constraint on the programme
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/economics-rules.md](../../rules/economics-rules.md),
[../../rules/tier-rules.md](../../rules/tier-rules.md).

- Report the participation funnel, not enrolment
  ([../../knowledge/member-lifecycle.md](../../knowledge/member-lifecycle.md)). A member who never earned
  is not participating.
- Read liability with its ageing, never as a total (E4). A large recent balance and a large old balance
  are opposite findings.
- Treat a falling redemption rate as a problem, not a saving (E4, E5).
- Never report the member/non-member difference as programme effect without naming the selection problem
  (G5, E9). Where a pre-enrolment or matched-cohort comparison is possible, use it and say which; where it
  is not, report the raw difference as raw.
- Assess each tier against whether members behave differently to reach or keep it (T3, G8). A tier that
  changes nothing is reported as such.
- State the point's monetary value, derived from the catalogue (E1). A programme whose point value cannot
  be stated is itself a finding.
- Derive time-to-first-reward in orders, from this store's AOV and frequency (E6).
- Name the binding constraint. A programme can be healthy on issuance and broken on reachability, and
  fixing the wrong one changes nothing.
- Report what is healthy as well as what is not. An assessment that lists only problems cannot be checked.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read configuration, members, ledger, redemptions, orders | `read_only` |
| ANALYZE | Funnel, liability ageing, redemption, tier behaviour, effect isolation | `analysis` |
| PLAN | Name the binding constraint and rank the findings | `analysis` |
| PREVIEW | Present the assessment with its evidence and its confidence | `analysis` |
| VALIDATE | Run the checks below | — |
| MEASURE | Re-diagnose after a full purchase cycle has elapsed post-change | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the configuration as read, the
participation funnel with its drop-offs, time to first redemption, liability with its ageing profile,
redemption rate and direction, per-tier behaviour assessment, the stated point value, and an effect
statement that names its own method and confidence.

Plus: the binding constraint, the findings ranked, the dimensions that are healthy, and anything that
could not be assessed.

No recommendations to act are produced here — this skill is `analyze_only`, and the acting skills compose
it.

## Validation

- [ ] Participation reported as a funnel, not as enrolment (G1)
- [ ] Liability reported with ageing, not as a total (E4)
- [ ] Redemption rate reported with direction, and a fall treated as a problem (E4)
- [ ] Effect statement names its method, or states that effect is not isolated (G5, E9)
- [ ] Point value stated and derived from the catalogue, not asserted (E1, G3)
- [ ] Time to first reward expressed in orders, derived from store data (E6)
- [ ] Every tier assessed against actual behaviour (T3)
- [ ] Binding constraint named with its reasoning
- [ ] Healthy dimensions reported explicitly
- [ ] Anything unassessable recorded in `unmet_requirements` (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |

Every action this skill implies is owned by a composing skill, which carries its own approval
requirements.

## Examples

**"Is our loyalty programme working?"**
Enrolment is strong and rising. The funnel shows most enrolled members never earned a second time and
almost none have redeemed, with liability concentrated in balances more than two years old. Names
reachability as the binding constraint — the cheapest reward is many orders away at this store's AOV — and
reports the raw member/non-member spend gap as raw, stating that pre-enrolment behaviour was unavailable
so programme effect is not isolated.

**"Our loyalty liability has doubled — should we expire points?"**
Ageing shows the growth is in recent balances from active members, not dormant ones. Reports that the
liability is a sign of participation rather than of neglect, that expiry would remove value from currently
engaged members, and routes the underlying question — whether the earn rate is affordable — to
[points-economics](../points-economics/SKILL.md) rather than answering it here.

## Failure Handling

| Situation | Response |
|---|---|
| `loyalty.program_config` unavailable | **Blocked.** A programme cannot be diagnosed without its rules |
| `loyalty.points_ledger` unavailable | **Blocked.** No ledger, no liability position, no funnel (G4) |
| Ledger has no ageing, only totals | **Partial.** Report the total, state explicitly that its meaning is undetermined without ageing |
| `loyalty.redemption` unavailable | **Partial.** Report issuance only, and state that programme health cannot be assessed from it |
| Pre-enrolment behaviour unavailable | **Partial.** Report the raw difference as raw, name the selection problem, lower confidence (G5) |
| Programme too new for a purchase cycle | Report programme age as the finding; assess structure rather than performance |
| No tiers configured | Not a failure. Report it, and assess whether the value distribution suggests any |
| Everything healthy | Report that, with the evidence. "Nothing is worth changing" is a valid result |

Degraded outcomes set `status` and populate `unmet_requirements`.
