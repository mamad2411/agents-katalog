---
name: forecast-monthly-sales
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Produce a monthly sales forecast from CRM pipeline using close dates, stages, forecast categories, and rep judgment.

## Preconditions

- Access to CRM opportunities or deals and forecast views.
- Current month forecast period and quota or target.
- Updated deal stages, amounts, close dates, and next steps.

## Steps

1. **Open the forecast view or report.** [BRANCH: Salesforce | HubSpot | generic] open Forecasts or an opportunity report in Salesforce; open Forecast or deal report in HubSpot; in another CRM, open pipeline forecast analytics. → *Expect:* current-month deals are visible.
2. **Filter to the month.** Select deals with close dates inside the target month and exclude closed-lost, duplicates, and test deals. → *Expect:* the report shows only relevant monthly pipeline.
3. **Review deal hygiene.** Check stage, amount, close date, next step, last activity, and owner for each material deal. → *Expect:* obvious stale or incorrect fields are identified.
4. **Classify forecast categories.** Set commit, best case, pipeline, omitted, or local equivalents based on evidence. → *Expect:* each material deal has an appropriate forecast category.
5. **Calculate totals.** Summarize closed-won, commit, best case, weighted pipeline, and gap to target. → *Expect:* forecast numbers are visible by owner or team.
6. **Add rep or manager judgment.** Adjust commentary for risk, upside, timing, procurement, and known blockers without changing source data inaccurately. → *Expect:* the forecast includes context behind the numbers.
7. **Save or export the forecast.** Save the CRM forecast/report or export only if policy allows. → *Expect:* stakeholders can access the monthly forecast.

## Decision points

- If close date is unrealistic → update it before including the deal in the month.
- If a deal lacks next step or recent activity → mark risk or remove from commit.
- If multi-currency reporting applies → use the company's approved conversion method.

## Failure modes & recovery

- **F1 Stale pipeline:** detect deals with old activity or past close dates → update, push out, or close out those deals.
- **F2 Forecast overstatement:** detect weak evidence in commit deals → reclassify as best case or pipeline.
- **F3 Missing material deal:** detect known active deal absent from report → correct close date, owner, or filters.

## Verification

The forecast shows current-month closed-won, commit, best-case, pipeline, and gap totals, with material deals reviewed for stage, amount, close date, and next step.

## Variations

- Rep forecast: focus on owned deals and personal commit.
- Manager forecast: roll up by rep, segment, or territory.
- Board forecast: use summarized totals and key risks, not raw deal detail.

## Safety & privacy

Forecasts expose revenue expectations and customer deal details. Share only with authorized stakeholders and keep commentary factual rather than speculative or personal.
