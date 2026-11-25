---
name: sales-pipeline-crm
description: B2B/B2C sales pipeline and CRM management — pipeline stages and exit criteria, lead qualification (BANT/MEDDIC), conversion rates per stage, weighted pipeline forecasting, quota and territory planning, CRM data hygiene, win/loss analysis, sales activity metrics, deal review cadence, proposal and follow-up discipline. Use when designing a sales process, forecasting revenue from pipeline, or improving CRM usage.
---

# Sales Pipeline & CRM (stages, qualification, forecasting, hygiene)

## Stages are exit criteria, not feelings

A pipeline stage is defined by a verifiable event that has already happened, never by seller
optimism. "Negotiation" means a proposal was sent and the buyer responded to it — not "I think
they're close."

```
Example B2B ladder (adapt, but keep every criterion buyer-verified):
Lead        → fits ICP, contact responded
Qualified   → need + budget authority + timeline confirmed by the buyer (BANT), or
              MEDDIC fields populated (Metrics, Economic buyer, Decision criteria/process,
              Identified pain, Champion)
Evaluation  → buyer actively evaluating: demo done, success criteria agreed in writing
Proposal    → priced proposal delivered to the economic buyer
Commit      → verbal yes + paper process (legal/procurement) started
Closed won/lost
```

If a deal can sit in a stage with nothing the buyer did to earn it, the stage measures seller mood
and every downstream number is fiction.

## Pipeline math — definitions

```
stage conversion    = deals exiting stage forward / deals entering stage (cohort-based, by entry
                      month — a snapshot ratio mixes deal generations)
sales cycle         = days from qualified → closed (report median; the mean is hostage to zombies)
weighted pipeline   = Σ (deal value × stage probability), probability from YOUR historical
                      stage→win rates, not the CRM vendor defaults
pipeline coverage   = open qualified pipeline / quota for the period (healthy ≈ 3–4×, but derive
                      from your own win rate: coverage needed = 1 / win rate from qualified)
win rate            = won / (won + lost), qualified deals only — counting raw leads flatters nobody
                      consistently
velocity            = (# qualified deals × avg deal size × win rate) / sales cycle days
```

Forecast three ways and reconcile: weighted pipeline, rep commit roll-up, and trend (last N periods'
actuals vs pipeline at the same point in cycle). When they disagree, the trend number usually wins.

## CRM hygiene — the forecast is only as good as the fields

- Mandatory fields per stage transition (amount, close date, next step with a date, economic buyer)
  — enforce at entry, because backfilled data is invented data.
- **Zombie sweep:** any deal with no buyer-side activity in 2× the median cycle time gets closed-lost
  with a reason. A pipeline full of zombies inflates coverage and hides the real gap until quarter
  end.
- Close dates that slip more than twice are a qualification failure, not a timing problem — send the
  deal back down the ladder.
- One owner per account, dedup rules, and a written definition per field; two reps interpreting
  "close date" differently poisons every roll-up.

## Win/loss and activity

- Win/loss interviews with the *buyer* (not the rep's recollection) on a sample of both outcomes;
  rep-reported loss reasons cluster on "price" because it's the only blameless answer.
- Activity metrics (calls, meetings, proposals) are diagnostic inputs, never targets — target them
  and you get activity, not revenue. Use them to explain funnel gaps: thin top-of-funnel is an
  activity problem; good top, bad conversion is a qualification or skill problem.
- Deal reviews on a fixed cadence, focused on the few deals that move the quarter: verify exit
  criteria with evidence, agree the single next step and date. A review that re-tells the deal story
  without testing it is a status meeting.

## Quota and territory

- Quota derives from bottom-up capacity (ramped reps × realistic velocity) reconciled against the
  top-down revenue target; a quota nobody has ever hit is a plan to miss with extra steps.
- Territories balanced on opportunity (ICP account count / spend potential), not geography
  convenience; re-balance on a schedule with grandfathering rules, or every re-org becomes a
  commission war.
- Ramp: new reps carry partial quota on a published schedule; counting them at full quota fabricates
  a coverage gap.

## Failure modes

- Stage probabilities copied from tool defaults, so the weighted forecast is a random number with
  decimal places.
- Sandbagging and happy ears cancelling out in aggregate "accurately" — until the mix shifts.
- 40% of pipeline value in deals with close dates in the last week of the quarter, again.
- CRM as a reporting chore filled in Friday afternoon; the data describes what reps remember, not
  what happened.
- Win rate "improved" because losses stopped being logged.

## Reviewer checklist

- [ ] Every stage has a buyer-verified exit criterion; no stage a seller can grant themselves
- [ ] Stage probabilities computed from own historical cohorts, refreshed on a schedule
- [ ] Conversion and cycle metrics cohort-based; medians reported for cycle time
- [ ] Coverage ratio derived from own win rate, zombies swept before it's computed
- [ ] Forecast triangulated (weighted / commit / trend) with disagreements explained
- [ ] Mandatory fields enforced at stage transition; slipped-twice deals re-qualified
- [ ] Win/loss sourced from buyers on a sample of wins AND losses

## Provenance

Standard B2B sales-operations practice (stage exit criteria, BANT/MEDDIC, cohort funnel math,
forecast triangulation, hygiene rules). Numeric guidance — 3–4× coverage, 2× cycle zombie threshold
— is **derived, unverified** rule of thumb; replace with the team's own measured win rates and cycle
times before setting targets.
