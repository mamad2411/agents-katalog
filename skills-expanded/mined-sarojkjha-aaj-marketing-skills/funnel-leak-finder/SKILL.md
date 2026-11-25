---
name: funnel-leak-finder
description: >-
  Use when the user wants to know which funnel stage is costing them wins,
  purchases or paid subscribers - after a weak month or quarter, before a
  pipeline review, or when deciding where to spend fix-it effort. Also use
  when the user mentions funnel leak, where the funnel leaks, conversion drop,
  stage conversion, MQL to SQL rate, add-to-cart or checkout rate, install to
  paid, biggest drop-off, "why did wins fall", or "which stage should we fix".
  Works for a B2B funnel, an ecommerce store or a subscription app. Compares
  each stage's rate with a baseline the user gives (last period or their own
  targets), counts what each shortfall cost, ranks them and flags changes
  that may be noise. Never names a leak from raw drop-off.
license: MIT
metadata:
  search_description: "Find the funnel stage that cost you the most wins, measured against last period or your own targets, with a check for changes that may be noise."
  publisher: AAJ
  slug: funnel-leak-finder
  category: Analytics & Experimentation
  phase: Diagnose
  difficulty: Starter
  card: >-
    Names the stage that cost the most wins against your own baseline, never
    from raw drop-off, and flags changes that may be noise.
  version: 1.1.0
  topic: analytics-budget
  secondary_topics: [sales-pipeline, website-conversion]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: This period's funnel counts for one of three funnels - B2B (sessions, leads, MQLs, SQLs, opportunities, wins), ecommerce (sessions, product page views if you have them, add to cart, checkout, purchases) or subscription app (installs, sign-ups, activated, started trial if you have it, paid); at least 3 consecutive stages - and a baseline, which is last period's counts or your target rate per stage, with where the targets come from; optionally revenue per win, purchase or paid subscriber, and your margin on it
  outputs: Each stage's rate against its baseline in points and relative terms, the wins, purchases or paid subscribers (and revenue and profit) each shortfall cost, the stages ranked, the leak named, a noise check per stage, and a plain statement when no baseline was given
  related_aaj:
    - https://aajconsult.com/tools/funnel-leak-finder
    - https://aajconsult.com/tools/marketing-kpi-report
    - https://aajconsult.com/tools/pipeline-forecast-calculator
  related: [marketing-report, pipeline-and-forecast, ab-test-significance, lead-handoff-sla, website-conversion-audit]
  tags: [funnel, conversion-rate, funnel-leak, stage-conversion, mql-to-sql, pipeline, diagnostics, ecommerce, subscription-app]
---

# Funnel Leak Finder

Names the funnel stage that cost the most wins this period, measured against a baseline the user gives. It never names a leak from raw drop-off.

It reads three funnels: B2B (the default), an ecommerce store and a subscription app. The method is the same for all three. Below, "wins" means the last stage of the funnel: wins, purchases or paid subscribers.

Raw drop-off misleads for two reasons. Each stage's rate has its own scale: sessions to leads might be 2% while opportunities to wins is 25%, so the top of the funnel will show the biggest drop whether or not anything is wrong there. And in a funnel, wins are the top-of-funnel count times every stage rate, so a 10% relative lift at any stage gives the same 10% more wins. The only useful question is which stage fell short of what it should have done, and what that shortfall cost.

## When to use

Wins or pipeline fell and the user wants to know where; a monthly or quarterly review needs "where the funnel leaks"; or the user is about to spend effort on one stage and wants to check it is the right one.

For the full KPI report (CAC, efficiency, attainment, period deltas), use `marketing-report`. For whether open pipeline covers the target, use `pipeline-and-forecast`.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, read it for the funnel definitions (what counts as an MQL or SQL). If not, ask.
2. **Pick the funnel and get this period's counts** for at least three consecutive stages:
   - B2B, the default, using the marketing-report names: `sessions`, `leads`, `mqls`, `sqls`, `opps`, `wins`.
   - Ecommerce, with `"funnel": "ecommerce"`: `sessions`, `views` (optional), `carts`, `checkouts`, `purchases`. Count sessions at each stage (sessions that viewed a product page, sessions with an add to cart, sessions that reached checkout, sessions that ended in an order), not events, so no stage is larger than the one before.
   - Subscription app, with `"funnel": "app"`: `installs`, `signups`, `activated`, `trials` (optional), `paid`. Count the people who installed in the period and how far each got. Ask the user what "activated" means in their product; the engine does not define it. Count paid within the same number of days after install in both periods.
   - An optional stage may be left out in the middle; the step then runs across it (`sessionsToCarts`, `activatedToPaid`). When the user has it, include it: it narrows the leak to a smaller step.
3. **Get a baseline. Without one, no leak can be named.** Either last period's counts for the same stages (`prior`), or a target rate per stage transition (`targets`), with where the targets come from (`targetSource`, such as "2026 plan"). Never supply industry rates as targets on the user's behalf: targets come from the user's plan or a source the user names.
4. **Check definitions did not change** between the two periods. A new MQL rule, a CRM migration, a tracking change, a new checkout or a moved paywall moves rates without anything leaking.

## Method

**Rates.** For each transition, rate now = next stage / this stage. Baseline rate = the same ratio last period, or the user's target.

**Margin.** With a revenue figure, the user can add `margin` (a fraction: 40% is 0.4), their margin on that revenue. The engine then shows profit lost beside revenue lost. In AAJ's view a store should act on profit. Never supply a margin on the user's behalf.

**Wins lost at a stage.** What the last stage would have been with that one stage at its baseline rate, holding the top-of-funnel count and every other stage at this period's rates, minus what it actually was:

```
lost_i = top count x baseline_i x (product of this period's rates at every other stage) - last stage count
       = last stage count x (baseline_i / rate_i - 1), when rate_i is above 0
```

This ranks stages by relative shortfall, not points: a 1-point drop on a 3% rate costs far more wins than a 1-point drop on a 40% rate. Revenue lost = wins lost x revenue per win, when the user gives it.

**The leak** is the stage with the most wins lost. Stages at or above baseline are holding. Each stage's figure holds the others still, so the figures do not add up to the total change; the engine says so. Against a prior period, a change in top-of-funnel volume is reported separately as volume, not ranked as a leak.

**The noise check.** Against a prior period: a pooled two-proportion z-test (NIST/SEMATECH e-Handbook of Statistical Methods, section 7.3.3). Against a target: a one-proportion z-test (section 7.2.4). A change "may be noise" when |z| is below 1.96 (95%, two-sided), or when the counts are too small for the test: fewer than 5 conversions or 5 non-conversions in either period, or, against a target, the stage count times the target or times one minus the target below 5 (NIST 7.2.4's condition). The 95% level and applying the 5-count condition to both periods are AAJ's choices. When the top-ranked leak may be noise, the engine says so and names the largest shortfall that clears the check, if there is one.

**What to do first (AAJ's view).** Fix the named leak before adding top-of-funnel volume: more volume through a stage that is below baseline buys fewer wins per unit of spend.

## Workflow

**Step 1 - Gather the counts.** This period, and the baseline period or targets. Same stage definitions, same period length.

**Step 2 - Run the engine.** With no baseline it shows the rates and says plainly that no leak can be named; it computes nothing else.

**Step 3 - Read the leak and its noise check.** If the leak may be noise, say so and suggest confirming it next period, or acting on the firm shortfall the engine names.

**Step 4 - Diagnose the stage, not the funnel.** Ask what changed at that hand-off: lead source mix, the MQL rule, response time, sales capacity, pricing, a competitor. The engine finds the stage; it does not know why.

## Run the tool

```
node resources/funnel-leak.js --demo
node resources/funnel-leak.js '{"period":"Q3 2026","sessions":120000,"leads":3000,"mqls":1050,"sqls":252,"opps":126,"wins":28,"revenuePerWin":18000,"prior":{"period":"Q2 2026","sessions":110000,"leads":2860,"mqls":1001,"sqls":320,"opps":150,"wins":36}}'
node resources/funnel-leak.js '{"leads":800,"mqls":300,"sqls":90,"opps":40,"wins":9,"targets":{"leadsToMqls":0.35,"mqlsToSqls":0.3,"sqlsToOpps":0.5},"targetSource":"2026 plan"}'
node resources/funnel-leak.js '{"contacts":[{"leads":"2026-07-03","mqls":"2026-07-20","sqls":null}],"dates":{"from":"2026-07-01","to":"2026-09-30"},"priorDates":{"from":"2026-04-01","to":"2026-06-30"}}'
node resources/funnel-leak.js '{"funnel":"ecommerce","period":"Oct 2026","sessions":40000,"carts":2400,"checkouts":1200,"purchases":684,"revenuePerPurchase":60,"prior":{"period":"Sep 2026","sessions":38000,"carts":2660,"checkouts":1330,"purchases":798}}'
node resources/funnel-leak.js '{"funnel":"ecommerce","sessions":40000,"views":16000,"carts":2400,"checkouts":1200,"purchases":684,"revenuePerPurchase":60,"margin":0.4,"prior":{"sessions":38000,"views":15200,"carts":2660,"checkouts":1330,"purchases":798}}'
node resources/funnel-leak.js '{"funnel":"app","installs":20000,"signups":9000,"activated":3600,"paid":288,"revenuePerPaid":40,"targets":{"activatedToPaid":0.1},"targetSource":"2026 plan"}'
node resources/funnel-leak.js --help
```

Every number in these examples is invented, for the fictional Example Co.

Transition keys for `targets`, as fractions (30% is 0.3):

| Funnel | Transition keys | Revenue field |
|---|---|---|
| `b2b` (default) | `sessionsToLeads`, `leadsToMqls`, `mqlsToSqls`, `sqlsToOpps`, `oppsToWins` | `revenuePerWin` |
| `ecommerce` | `sessionsToCarts`, `cartsToCheckouts`, `checkoutsToPurchases`; with `views`: `sessionsToViews`, `viewsToCarts` | `revenuePerPurchase` |
| `app` | `installsToSignups`, `signupsToActivated`, `activatedToPaid`; with `trials`: `activatedToTrials`, `trialsToPaid` | `revenuePerPaid` |

Any funnel also takes `margin`, a fraction, with its revenue field.

A stage or revenue field from another funnel is rejected, with a hint naming the funnel it belongs to.

**Counts from CRM contacts (B2B only).** When the numbers come from a CRM, do not count them yourself. Give `contacts` (one object per contact, with the date it entered each stage: `leads`, `mqls`, `sqls`, `opps`, `wins`), `dates` and, for a prior-period baseline, `priorDates`. The engine counts each period as a cohort: a contact belongs to a period if its first stage date falls in it, and counts for a stage if it entered that stage or a later one by the period's last day. Sessions are not in a CRM; add `sessions` and `priorSessions` if you have them.

`run(config)` returns each transition with its rate, baseline rate, change in points and relative terms, status (leaking, holding, no baseline), wins and revenue lost, rank and noise check; the leak, and the firmest leak when the top one may be noise; top-of-funnel volume against the prior period; the verdict; notes; and AAJ's view, labelled. It rejects unknown fields, non-numbers, counts that are not whole numbers, gaps between stages, a stage larger than the one before it, both baselines at once, and rates written as whole percentages.

## Reference

The free browser version is at https://aajconsult.com/tools/funnel-leak-finder and runs the same engine. It also links each stage to AAJ material on fixing it.

## Present the result

1. **The verdict line**: the leak, its rate against the baseline, and the wins (and revenue) it cost; or "no leak" or "no baseline".
2. **The table**: each transition's rate, baseline, change, wins lost and noise check.
3. **The notes**: volume change, stages without a target, the figures-do-not-add note.
4. **AAJ's view**, labelled as such.

**Show where it came from.** Open your answer with "AAJ `funnel-leak-finder` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/funnel-leak-finder`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never name a leak from the biggest drop-off.** Without a baseline, say no leak can be named.
- **Never invent target rates.** No "typical MQL to SQL rate". Targets come from the user's plan or a source the user names, and the engine records that source.
- **Do not act on a change that may be noise.** Say so, and wait a period or act on the firm shortfall.
- **Counts in one period are not one cohort.** Wins this quarter partly come from opportunities created last quarter; with a long sales cycle, compare lagged stages or longer periods.
- **Sessions are not people.** The z-test treats each count as an independent trial; for sessions to leads, or sessions to add to cart, that overstates certainty when people visit many times.
- **Ecommerce counts are sessions, not events.** One session can add to cart five times. Count the sessions that did it at least once, or a later stage can come out larger than the one before and the engine will refuse it.
- **Never invent a consumer benchmark either.** No "typical add-to-cart rate" or "typical trial conversion". The baseline is the user's own last period or their own target.
- **Do not add the stage figures up.** Each holds the other stages still.

## Related AAJ resources

- The free tool: https://aajconsult.com/tools/funnel-leak-finder
- The monthly marketing KPI report: https://aajconsult.com/tools/marketing-kpi-report
- Pipeline coverage and forecast: https://aajconsult.com/tools/pipeline-forecast-calculator

## Related skills

- `marketing-report` - the full KPI report these counts come from
- `pipeline-and-forecast` - whether open pipeline covers the target
- `ab-test-significance` - testing the fix once you change the leaking stage
- `lead-handoff-sla` - when the leak is between MQL and SQL, at the hand-off to sales
- `website-conversion-audit` - when the leak is between sessions and leads, or sessions and add to cart

## Credits

Written by AAJ (aajconsult.com). MIT licensed. The noise check follows the NIST/SEMATECH e-Handbook of Statistical Methods, sections 7.2.4 (one proportion against a requirement) and 7.3.3 (two proportions).
