---
name: cohort-retention-curves
description: >-
  Use when the user wants to see how long customers stay, cohort by cohort -
  to check whether retention levels off, whether newer signups retain better
  than older ones, or to turn a customer list into a cohort table. Also use
  when the user mentions cohort analysis, retention curve, cohort table,
  survival curve, logo retention by month, "does retention flatten",
  "are newer cohorts better", or "how many customers are left after 6 months".
  Builds the chained average curve with a 95% band, finds where it levels off
  and tests newer cohorts against older ones.
license: MIT
metadata:
  search_description: "Build cohort retention curves from a cohort table or a customer list: the average curve with a 95% band, where it levels off, and newer against older cohorts."
  publisher: AAJ
  slug: cohort-retention-curves
  category: Retention & Lifecycle
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Chains cohorts of different ages into one retention curve, finds where it
    levels off and tests newer cohorts against older ones.
  version: 1.0.0
  topic: retention-expansion
  secondary_topics: [analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: A cohort table (one row per cohort, oldest first, customers or revenue retained in each period from period 0, as counts or percent of the start) or one row per customer with a start date and an end date; optionally the levelling-off threshold
  outputs: The chained average retention curve with a 95% band for customer counts, the period it levels off from and the level, period-1 and last-reliable-period retention, newer against older cohorts with a significance test, and findings on the data
  related_aaj:
    - https://aajconsult.com/tools/cohort-retention-curve-builder
    - https://aajconsult.com/tools/churn-nrr-calculator
    - https://aajconsult.com/playbooks/customer-onboarding-retention-playbook
  related: [lifecycle-and-retention, onboarding-activation, unit-economics, saas-growth-efficiency]
  tags: [cohort-analysis, retention-curve, retention, churn, kaplan-meier, survival-curve, saas-metrics]
---

# Cohort Retention Curves

Shows how long customers stay by building one retention curve from cohorts of different ages. It says whether the curve levels off, and whether newer cohorts retain better or worse than older ones.

A plain average of a cohort table goes wrong in the later periods. Only the oldest cohorts have reached them, so a simple column average mixes old and young cohorts and drags the tail down. This skill chains the curve period by period, using only the cohorts that have reached both periods. For customer counts that is the Kaplan-Meier product-limit estimate.

## When to use

The user has signups or customers by month (or week, or quarter) and wants to know how retention behaves over time: where it settles, how much of a cohort is left after six months, whether recent changes helped. Also when the user has a customer list with start and end dates and needs it turned into cohorts.

For one period of revenue movement (NRR, GRR, quick ratio), use `lifecycle-and-retention`. For finding the moment new users decide to stay, use `onboarding-activation`.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, read it for the billing cycle and what counts as an active customer. If not, ask.
2. **Get the data in one of three shapes.** A list of cohorts (`cohorts`), the cohort table as text (`table`), or one row per customer with a start and an end date (`customers`).
3. **Pick the period.** Use the natural buying cycle: monthly for most subscriptions, weekly for products used daily, quarterly for annual contracts. Use the same period for every cohort.
4. **Pick the measure.** Customers (logos) or revenue. Revenue can rise above 100% when accounts expand; customers cannot.
5. **Order cohorts oldest first.** The newer-against-older comparison depends on the order.

## Method

**The chained curve.** Start at 100%. For each later period, multiply by the share retained from the period before, pooled over the cohorts that have reached both periods:

```
S(0) = 1
S(k) = S(k-1) x sum of v_c(k) / sum of v_c(k-1), over cohorts c observed at period k
```

For customer counts this is the product-limit estimator for grouped data (E. L. Kaplan and P. Meier, "Nonparametric estimation from incomplete observations", Journal of the American Statistical Association 53, 1958). Young cohorts count only for the periods they have reached, so they do not drag the tail down.

**The 95% band.** For customer counts with cohort sizes, the band uses Greenwood's variance (M. Greenwood, "The natural duration of cancer", Reports on Public Health and Medical Subjects 33, 1926). There is no band for revenue, for percentages without sizes, or when the pooled cohorts gain customers between two periods.

**Reliable periods.** A period is reliable when at least 3 cohorts have reached it (MIN_COHORTS, a tool rule). Later periods are shown but not used to judge the shape.

**Levelling off.** The curve levels off from period F when every later reliable period moves less than 2 percentage points of the starting cohort, up or down (FLAT_PTS, a tool rule the user can change), judged over at least 2 later periods (FLAT_MIN_AFTER, a tool rule). The level is the average of the curve from F to the last reliable period.

**Newer against older.** At one period, the engine pools the older half and the newer half of the cohorts that reached it and compares their retention. For customers, with cohort sizes, it runs a pooled two-proportion z-test (NIST/SEMATECH e-Handbook of Statistical Methods, section 7.3.3), with the p-value from Abramowitz and Stegun's formula 26.2.17. The period is the latest one, up to 12, that at least 4 cohorts, and at least half of all cohorts, have reached, unless the user sets it.

**A customer list.** Customers are grouped by the month they started. A customer counts as retained in month k when they had not ended before the first day of the k-th month after the start month. Month k counts for a cohort only once its first day is on or before the as-of date.

The three tool rules are AAJ's choices, not benchmarks.

**What to do with it (AAJ's view).** A curve that levels off is a base to build on: what you acquire adds to customers who stay. While the curve keeps falling, fix retention before buying more acquisition, because more customers in only fills a leaking bucket faster.

## Workflow

**Step 1 - Gather the data.** Same period length and the same definition of "active" for every cohort.

**Step 2 - Run the engine.** It refuses data it cannot read and says why. Fix the data rather than dropping the rows.

**Step 3 - Read the shape.** Does it level off, and where? Read the band before reading small differences.

**Step 4 - Read newer against older.** If the difference is significant, ask what changed between the two groups: channel, plan, product, onboarding, pricing.

**Step 5 - Split and re-run.** The curve shows what happened, not why. Split the table by channel or plan and run each part.

## Run the tool

```
node resources/cohort-curve.js --demo
node resources/cohort-curve.js '{"label":"Signups by month","cohorts":[{"label":"2026-01","values":[120,84,70,66,63]},{"label":"2026-02","values":[95,70,57,54]},{"label":"2026-03","values":[140,101,88]},{"label":"2026-04","values":[110,80]}]}'
node resources/cohort-curve.js '{"customers":[{"start":"2026-01-14","end":null},{"start":"2026-01-20","end":"2026-04-02"},{"start":"2026-02-03"}],"asOf":"2026-05-31"}'
node resources/cohort-curve.js --help
```

Other options: `"measure": "revenue"`, `"unit": "percent"` (period 0 is 100; give `size` for every cohort to weight them), `"period": "week"`, `"flatPts": 1.5`, `"comparePeriod": 6`, and `"table"` for the cohort table as CSV text.

`run(config)` returns the curve, the cohorts reaching each period, the band, the last reliable period, where the curve levels off and at what level, the months-active area over the reliable periods (at most the first 12), the newer-against-older comparison, findings, the tool rules and AAJ's view, labelled. It rejects unknown fields, non-numbers, negative values, customer counts that are not whole numbers, a later period larger than the cohort's start (for customers), a blank followed by more numbers, unreadable dates and an end before a start.

## Reference

The free browser version is at https://aajconsult.com/tools/cohort-retention-curve-builder and runs the same engine. It draws the curves and a heatmap, and reads a pasted table or customer list.

## Present the result

1. **The headline**: where the curve levels off and at what level, or that it has not, or that there is too little history.
2. **Key figures**: period-1 retention with its band, retention at the last reliable period, and the months-active area.
3. **The curve**: each period's average, band and number of cohorts. Mark the periods with fewer than 3 cohorts.
4. **Newer against older**: both pooled rates, the difference in points and the p-value.
5. **Findings**, then **AAJ's view**, labelled as such.

**Show where it came from.** Open your answer with "AAJ `cohort-retention-curves` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/cohort-retention-curves`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never average the columns of a cohort table.** Young cohorts pull the later periods down. Use the chained curve.
- **Do not read the tail.** Periods reached by fewer than 3 cohorts are shown, not judged.
- **A curve that has levelled off may still drift.** The reliable part is only as long as the third-oldest cohort.
- **Customers coming back is not retention.** If a cohort gains customers, the data is an activity curve or needs a reactivation rule. The engine flags it.
- **Revenue and customers answer different questions.** Revenue retention includes expansion and can rise above 100% while customers leave. Run both.
- **The curve shows what, not why.** A worse cohort may come from a different channel, plan or an outage. Split and re-run.
- **No benchmarks.** The engine compares the user's cohorts with each other, never with an industry figure.

## Related AAJ resources

- The free tool: https://aajconsult.com/tools/cohort-retention-curve-builder
- One period of churn, NRR and GRR: https://aajconsult.com/tools/churn-nrr-calculator
- Customer Onboarding & Retention Playbook: https://aajconsult.com/playbooks/customer-onboarding-retention-playbook

## Related skills

- `lifecycle-and-retention` - churn, NRR, GRR and the retention plan for one period of revenue movement
- `onboarding-activation` - getting new users to the moment the product works for them, where the first drop in the curve happens
- `unit-economics` - the lifetime value this retention drives
- `saas-growth-efficiency` - how retention feeds growth efficiency

## Credits

Written by AAJ (aajconsult.com). MIT licensed. The curve follows Kaplan and Meier (1958), the band Greenwood (1926), the newer-against-older test the NIST/SEMATECH e-Handbook of Statistical Methods, section 7.3.3, and the normal tail Abramowitz and Stegun (1964), formula 26.2.17.
