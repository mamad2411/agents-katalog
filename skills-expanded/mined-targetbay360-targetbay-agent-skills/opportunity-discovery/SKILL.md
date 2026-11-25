---
name: opportunity-discovery
description: Use when nobody has named the problem — "what should we be working on?", "where should we focus?", "review our programme", or a sense that something is off with no specific symptom. Runs an open-ended scan across revenue, lifecycle leakage, automation coverage, campaign performance, list health and deliverability, channel mix, cadence, catalogue and content, then ranks whatever is most worth fixing or building next. Use revenue-growth when the objective is already framed as revenue.
license: MIT
metadata:
  targetbay.display_name: Opportunity Discovery
  targetbay.version: "2.1.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.product_intelligence, email_sms.segmentation, email_sms.campaign_analytics, email_sms.automation, email_sms.automation_analytics, email_sms.suppression_and_consent, email_sms.marketing_calendar
  targetbay.composes: revenue-analysis, automation-strategy, campaign-optimization, deliverability-qa
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Opportunity Discovery

## Purpose

Scan the whole programme and report what is most worth doing next, when nobody has said what to look at.

Every other skill in this package answers a framed question. This one exists for the unframed one, and its
discipline is breadth: it must look everywhere before ranking, or it will simply confirm whatever the
operator already suspected.

## When to Use

- "What should we be working on?"
- Periodic programme review
- Inheriting a store and needing to know where it stands
- A sense that something is wrong without a specific symptom
- Before planning a quarter, to check nothing obvious is being missed

## When Not to Use

- The objective is already framed as revenue. Use [revenue-growth](../revenue-growth/SKILL.md).
- A specific thing is known to be broken. Use the skill that owns it.
- A new store with no history. Use [store-onboarding](../store-onboarding/SKILL.md) — there is nothing to
  discover yet.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Revenue history and decomposition | The largest single lens | Blocked |
| Lifecycle distribution and transition rates | Where customers leak | Blocked |
| Automation portfolio and per-journey performance | Coverage gaps and decayed journeys | Blocked |
| Campaign performance history | Underperformers and patterns | Partial |
| List health: engagement, unsubscribes, complaints | Deliverability exposure | Partial; a real blind spot |
| Channel consent and mix | Unused reach, or overused channels | Partial |
| Calendar occupancy and cadence | Fatigue exposure and unused capacity | Partial |
| Catalogue and stock posture | Products with no marketing attached | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Scale and context for what "normal" looks like |
| `email_sms.customer_intelligence` | Lifecycle leaks, value concentration, engagement decay |
| `email_sms.order_intelligence` | Revenue decomposition, intervals, AOV |
| `email_sms.product_intelligence` | Unmarketed products, affinity left unused |
| `email_sms.segmentation` | Sizing every candidate opportunity |
| `email_sms.campaign_analytics` | Underperformance patterns |
| `email_sms.automation` / `email_sms.automation_analytics` | Coverage gaps, decayed journeys |
| `email_sms.suppression_and_consent` | List health, unused consented reach |
| `email_sms.marketing_calendar` | Fatigue and unused capacity |

## Decision Process

```
Scan every lens before ranking any of them:

  revenue        ← which term is weakest; what changed
  lifecycle      ← which transition leaks most
  automation     ← uncovered transitions; decayed or duplicated journeys
  campaigns      ← persistent underperformance; manual sends simulating triggers
  list health    ← unengaged share, complaint trend, who should leave the population
  deliverability ← authentication, reputation trajectory, one provider turning against the store
  channel        ← consented reach unused; a channel overused
  cadence        ← fatigue exposure, or unused capacity
  catalogue      ← products carrying revenue with no marketing attached
  content        ← systematic weaknesses across messages
  contention     ← campaigns and automations reaching the same contacts in the same window
        ↓
  size every finding
        ↓
  rank by expected value ÷ effort
        ↓
  assign an owning skill per finding
```

The routing is fixed, so a finding is never left without a destination:

```
revenue        -> revenue-analysis, then revenue-growth
lifecycle      -> customer-lifecycle
automation     -> automation-strategy, or automation-optimization for a live journey
campaigns      -> campaign-optimization
list health    -> list-hygiene
deliverability -> deliverability-qa
channel        -> channel-optimization
cadence        -> consent-verification, which owns the ceiling
contention     -> campaign-conflict-resolver
catalogue      -> product-recommendation-strategy, or product-launch
content        -> content-optimization
```

Ranking before scanning is the failure mode. The first plausible finding is rarely the largest.

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/deliverability-rules.md](../../rules/deliverability-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md).

- Scan every lens, including the ones nobody asked about. Report which lenses could not be scanned.
- Size every finding before ranking it. An interesting finding affecting few customers is not a priority.
- Rank by expected value against effort, and state the criteria (G14).
- Prefer fixing a leak over adding volume. A leaking programme scaled up leaks faster.
- Deliverability and list-health findings outrank most revenue findings, because they suppress everything
  else the store sends.
- Deliverability and list health are **separate lenses with separate owners** (D1). A rising complaint
  rate is a population question for [list-hygiene](../list-hygiene/SKILL.md); an authentication or
  reputation trajectory is a layer above it and belongs to
  [deliverability-qa](../deliverability-qa/SKILL.md). Reporting them as one finding sends the remedy
  to the wrong place (D8).
- Never assert inbox placement from sending data (D7). Where the deliverability lens runs, it reports
  trends and labels its proxies.
- The contention lens counts campaigns and automations together (F2, F3). A programme can be healthy
  on every other lens and still be contacting its best customers four times a week.
- Report findings that have no action attached as observations, clearly separated from recommendations.
- Every finding names the skill that owns it. A finding with no owner is not actionable.
- Say what was scanned and found healthy. A report that only lists problems reads as a programme in
  crisis, and hides the fact that most of it works.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read across every capability | `read_only` |
| ANALYZE | Run each lens; size every finding | `analysis` |
| PLAN | Rank, assign owning skills, separate observations from recommendations | `recommendation` |
| PREVIEW | Present findings with evidence and coverage of the scan itself | `recommendation` |
| VALIDATE | Run the checks below | — |

This skill never mutates and never plans execution; `targetbay.execution_mode` is `recommend_only`. Each finding is
handed to its owning skill.

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the lenses scanned and the lenses
skipped with reasons; ranked findings conforming to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json), each with size,
evidence, owning skill, effort and risk; observations without actions, separated; and what was checked and
found healthy.

## Validation

- [ ] Every lens either scanned or reported as unscannable
- [ ] Every finding sized (A1)
- [ ] Every finding carries evidence with period and sample size (G2)
- [ ] Ranking criteria stated (G14)
- [ ] List-health and deliverability findings weighted above ordinary revenue findings
- [ ] Deliverability reported separately from list health, with separate owners (D1, D8)
- [ ] No placement claim asserted from sending data (D7)
- [ ] Contention lens counts campaigns and automations together (F2, F3)
- [ ] Every finding names an owning skill
- [ ] Observations separated from recommendations
- [ ] Healthy areas reported, not only problems
- [ ] No finding invented to fill a lens (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Report findings | `recommendation` | None |
| Act on any finding | varies | In the owning skill |

## Examples

**"What should we be working on?"**
Scans all nine lenses. Revenue looks stable, which is where a narrower skill would have stopped. List
health shows a large unengaged share and a rising complaint trend — suppressing inbox placement for
everything else the store sends. That ranks first, above a larger-looking but slower revenue opportunity
in automation coverage, because it caps the ceiling on every other finding. Reports campaigns, cadence and
catalogue as healthy.

**"Something feels off but our numbers look fine."**
Scans everything and finds revenue, campaigns and automations all within their own ranges — which is
why a narrower skill would have returned nothing. The deliverability lens finds engagement has fallen
sharply at one receiving domain over recent sends while holding steady elsewhere, which the
programme-wide averages had absorbed. Ranks it first, because it caps every other finding, and hands
it to deliverability-qa rather than to list-hygiene: nothing yet indicates the population is the
problem, and suppressing contacts would be a remedy aimed at a layer that may not be broken. Reports
that placement itself could not be observed and that the domain-level trend is a proxy.

**"Review our programme before we plan the quarter."**
Finds three items: a decayed automation with an expired offer inside it, a consented SMS audience that has
never been used, and a manual campaign sent monthly that should be a triggered journey. Ranks by effort
against value — the decayed automation is a small fix with immediate effect and goes first.

## Failure Handling

| Situation | Response |
|---|---|
| Several capabilities unavailable | **Partial.** Scan what is reachable and name every lens that could not run |
| New store with no history | Recommend [store-onboarding](../store-onboarding/SKILL.md) instead |
| No findings above the size threshold | Report that plainly. "The programme is sound" is a valid output |
| Everything looks like a finding | Size first; most will fall below the threshold |
| Findings conflict with each other | Report the conflict and rank the one that unblocks the other first |
| Operator disagrees with the ranking | Present the evidence and criteria; re-rank on stated constraints, not on preference |
| Deliverability lens cannot run | **Partial.** Name it as unscanned rather than concluding the programme is sound; it is the lens whose absence hides the most (S12) |
| Engagement cannot be split by receiving domain | **Partial.** The deliverability lens reports programme-wide only, and says a single-provider cause cannot be ruled out (D6) |
| Contention lens cannot see live automations | **Partial.** Report campaign-only cadence and state that delivered contact is understated (F3) |

Degraded outcomes set `status` and populate `unmet_requirements`.
