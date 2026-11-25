---
name: experience-experimentation
description: Use when an onsite change needs proving rather than asserting — designing an A/B or multivariate test, deciding whether the traffic can resolve it at all, setting the stopping condition, or reading a result honestly. Also use when a test is being called early, when results look too good, or when several changes are being bundled into one test.
license: MIT
metadata:
  targetbay.display_name: Experience Experimentation
  targetbay.version: "2.0.0"
  targetbay.category: experimentation
  targetbay.requires: onboarding.store_context, onboarding.consent_and_tracking, onboarding.experimentation, onboarding.experience_analytics, onboarding.audience_definition, onboarding.recommendation_analytics, onboarding.offer_analytics
  targetbay.composes: surface-inventory
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Experience Experimentation

## Purpose

Decide whether an onsite change can be proved here, design the test that would prove it, and read the
result without flattering it.

The most common failure is not a badly designed test but a test this store's traffic could never resolve,
run anyway, and then acted on ([../../rules/measurement-rules.md#M5](../../rules/measurement-rules.md)).
The second most common is stopping when it looks good.

## When to Use

- An onsite change needs proving before rollout
- Designing an A/B or multivariate test
- Deciding whether the traffic can detect an effect worth acting on
- Setting or checking a stopping condition
- Reading a completed test's result
- Someone wants to call a test early, or bundle several changes into one

## When Not to Use

- The change is what to recommend. Use
  [recommendation-strategy](../recommendation-strategy/SKILL.md), which hands off to this skill.
- The change is an offer's audience. Use [offer-targeting](../offer-targeting/SKILL.md).
- The change is search configuration. Use [onsite-search](../onsite-search/SKILL.md).
- Nothing is being changed and the question is what to fix first. Use
  [personalization-audit](../personalization-audit/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Baseline rate for the target metric | Without it, no effect size can be computed | Blocked |
| Traffic volume on the affected surface | Whether the test can resolve anything | Blocked |
| Consent state | Whether variant assignment is permissible for the traffic | Blocked |
| Existing tests in flight | Overlapping tests contaminate each other | Blocked |
| Current experiment configuration | Whether stopping conditions are honoured by the platform | Partial |
| Seasonality and known events in the window | Whether the horizon is representative | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.consent_and_tracking` | Whether variant assignment is permissible for this traffic |
| `onboarding.store_context` | Traffic volume and vertical |
| `onboarding.experimentation` | Reading tests in flight and configuration; creating and running tests |
| `onboarding.experience_analytics` | Baseline rates and funnel context |
| `onboarding.audience_definition` | The population the test runs against, and its size |
| `onboarding.recommendation_analytics` / `onboarding.offer_analytics` | Element-level baselines for the thing under test |

## Decision Process

```
1. Read consent and tests in flight          ← permissibility and contamination
2. State the change as exactly one change
3. Read the baseline for the target metric
4. Compute the detectable effect at this traffic and horizon
5. Decide whether to test at all             ← "cannot resolve" is a valid answer
6. Set allocation, duration and stopping condition — before starting
7. State what a negative result means and what happens then
8. Run, then read against the declared condition only
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/measurement-rules.md](../../rules/measurement-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Declare the metric, the comparison and the horizon before the change (M1, G24).
- Compute whether this store's traffic can detect an effect worth acting on within a plausible horizon
  (M5). Where it cannot, say so and recommend deciding on reasoning instead — an underpowered test is worse
  than no test, because it produces a number people believe.
- The current experience is the baseline and is presumed adequate (M2). The burden sits on the variant.
- One change per test (M6). Where several must ship together, state that the test measures the bundle and
  cannot attribute within it.
- Declare the stopping condition and honour it (M4). Never stop early because it is winning
  ([#S20](../../rules/safety-rules.md)); a test stopped for any other reason is reported as inconclusive,
  never as a result.
- Report the losers (M7): what the change cost, which segment converted worse, what traffic saw nothing.
- Check novelty decay where the horizon permits (M8). A first-period effect is not a durable one.
- Refuse to run a test that overlaps an in-flight test on the same surface without stating the
  contamination and how it will be handled.
- Consent must permit variant assignment for the traffic in question (G19,
  [#S15](../../rules/safety-rules.md)).
- Starting a test is `high_impact` — a share of live traffic receives the variant
  ([#S5](../../rules/safety-rules.md), [#S4](../../rules/safety-rules.md)).
- Never claim a result the test did not measure. A test on one template says nothing about another (G2).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, tests in flight, baselines, traffic volume | `read_only` |
| ANALYZE | Compute detectable effect; decide whether the test is worth running | `analysis` |
| PLAN | Allocation, duration, stopping condition, negative-result plan | `plan` |
| PREVIEW | State traffic share, duration, revenue at risk, stopping condition | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the test start specifically | — |
| EXECUTE | Start the test | `high_impact` |
| VERIFY | Confirm allocation and configuration match what was approved | `read_only` |
| MEASURE | Read only at the declared stopping condition | `read_only` |
| OPTIMIZE | Roll out, revert, or report inconclusive — per the declared plan | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the change stated as one change, the
baseline, the minimum detectable effect at this traffic and horizon, and an explicit recommendation on
whether to test at all.

Where a test is warranted: allocation, duration, stopping condition, the metric with its comparison, what a
negative result means, and what happens in that case.

Where one is not: the reasoning-based decision and what data would change the answer.

Recommendations conform to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

## Validation

- [ ] Metric, comparison and horizon declared before the change (M1, G24)
- [ ] Minimum detectable effect computed against actual traffic (M5)
- [ ] "Do not test" considered as a genuine outcome
- [ ] Exactly one change under test, or the bundle declared as unattributable (M6)
- [ ] Stopping condition declared before the start, and no early call permitted (M4, S20)
- [ ] Negative-result plan stated before the start
- [ ] In-flight test overlap checked and handled
- [ ] Consent permits variant assignment for the target traffic (G19, S15)
- [ ] Losers reported alongside gains (M7)
- [ ] Novelty decay checked where the horizon permits (M8)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce the design | `plan` | None |
| Stage a test configuration | `mutation` | Preview, then confirm |
| Start a test on live traffic | `high_impact` | Explicit, with traffic share and revenue at risk shown |
| End a test before its stopping condition | `destructive` | Explicit, and the result is reported as inconclusive (S20, M4) |

## Examples

**"A/B test the new product page layout."**
Baseline conversion and traffic on that template give a minimum detectable effect far larger than any
plausible layout gain, so a test would either return noise or run for most of a year. Recommends not
testing, deciding on reasoning instead, and states what would make a test viable — a higher-traffic
template, or a metric closer to the change such as add-to-cart rather than purchase.

**"The variant is up 18% after three days — can we roll it out?"**
Three days is short of the declared stopping condition and inside the novelty window. States that the
interim result is not a result (S20, M8), that stopping now would convert noise into a decision, and that
the test should run to its declared condition. Notes what the reading would be worth at that point, and
that if the effect is real it will still be there.

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.experimentation` unavailable | **Blocked.** No test can be designed against an unknown experimentation surface |
| Baseline unavailable | **Blocked.** Effect size cannot be computed without it (M1) |
| Traffic volume unavailable | **Blocked.** Whether the test can resolve anything is the first question (M5) |
| Consent does not permit variant assignment | **Blocked** for that traffic. Report which traffic can be tested, if any (S15) |
| Platform auto-promotes an interim winner | Report it as a conflict with [#S20](../../rules/safety-rules.md); design around it or decline to test |
| An overlapping test is in flight | **Blocked** until the overlap is resolved; state the contamination |
| Traffic cannot resolve the effect | Recommend not testing, with the arithmetic, and decide on reasoning instead (M5) |
| Asked to bundle several changes | Run it as a bundle test and state plainly that no change can be attributed within it (M6) |

Degraded outcomes set `status` and populate `unmet_requirements`.
