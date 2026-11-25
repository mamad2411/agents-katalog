---
name: lead-handoff-sla
description: >-
  Use when the user wants to check whether the marketing-to-sales lead handoff
  works: MQLs followed up within the SLA, sales accepting what marketing sends,
  and the MQL threshold in the right place. Also use when the user mentions lead
  response time, speed to lead, MQL SLA, SLA compliance, MQL rejection, sales
  acceptance rate, lead scoring threshold, or "sales never follows up our
  leads." Produces SLA compliance, acceptance and conversion rates with honest
  intervals, a threshold check by score band, the volume-promise check, and
  three fixes.
license: MIT
metadata:
  search_description: "Check the marketing-to-sales lead handoff: SLA compliance, acceptance and conversion rates with honest intervals, an MQL threshold check, and three fixes."
  publisher: AAJ
  slug: lead-handoff-sla
  category: Sales & Pipeline
  phase: Execute
  difficulty: Intermediate
  card: >-
    Checks whether MQLs get worked on time, whether sales takes them, and whether
    the threshold is in the right place.
  version: 1.0.0
  sprint: gtm-pipeline
  topic: sales-pipeline
  secondary_topics: [analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The lead scoring model (fit criteria, behavior signals, MQL threshold), the SLA terms, and a lead export with MQL, first-touch and outcome times.
  outputs: SLA compliance, never-touched MQLs, acceptance and conversion rates with 90% ranges, a threshold check by score band, the volume-promise check, and a verdict with three fixes.
  related_aaj:
    - https://aajconsult.com/tools/lead-handoff-sla-checker
    - https://aajconsult.com/templates/lead-scoring-and-sla-sheet
    - https://aajconsult.com/blog/sales-marketing-alignment
  tags: [lead-scoring, sla, mql, speed-to-lead, sales-marketing-alignment, lead-handoff]
---

# Lead Handoff & SLA Check

Check the marketing-to-sales handoff against the SLA both teams signed, with numbers each side can verify, so the weekly review argues about fixes instead of anecdotes.

## When to use

When marketing says sales ignores its leads and sales says the leads are junk; when an SLA exists but nobody measures it; before changing the MQL threshold or the scoring points; or as the monthly check on a lead scoring and SLA sheet.

## Before you start

1. **Read the brand/product context first.** Pull the ICP and the sales motion from `.agents/product-marketing.md` (or `.agents/aaj-brand.md`). If none exists, ask the user for the essentials.
2. **Gather inputs:**
   - **Scoring model:** fit criteria and behavior signals with points, and the MQL threshold. If the team uses the AAJ Lead Scoring and SLA Sheet, take them from its Fit criteria, Behavior criteria and Stages sheets.
   - **SLA terms:** the first-touch target in hours, the window for sales to accept or reject, marketing's promised MQLs per week, and the compliance target. If any is missing, say so; a term nobody wrote down cannot be checked.
   - **Lead export** (CSV from the CRM): id, created_at, fit and behavior points (or the criteria each lead met), became_mql_at, first_sales_touch_at, outcome (accepted, rejected, converted, open), and ideally decided_at and a rejection reason.
3. **Confirm the objective:** a check of the handoff the team already agreed, not a new scoring model. If there is no scoring model or SLA yet, build those first with the AAJ sheet, then come back.

## Method

A handoff fails in a few countable ways: MQLs touched late, MQLs never touched, MQLs nobody accepts or rejects, leads sales turns down, a threshold in the wrong place, or too few MQLs. Measure each from timestamps, never from impressions. Every rate carries its count and a 90% Wilson interval, and any rate on fewer than 30 leads is labelled directional (30 is AAJ's rule of thumb, not a statistical law). The threshold is judged by conversion per score band: if MQLs just above the line convert clearly worse than higher-scoring ones, it is too low; if leads below the line that sales worked anyway convert as well, it may be too high. "Clearly" means the 90% ranges do not overlap; anything less is a hint.

## Workflow

1. **Collect** the model, the SLA terms and the export. Keep every time column in the same time zone.
2. **Run the engine** (below) on the JSON. Do not compute the rates by hand.
3. **Read the data notes first.** Unreadable dates, outcomes without touch times and leads that scored as MQLs but were never marked change what the rates mean.
4. **Report response time:** compliance against target with its range, the median time to first touch and how many leads it covers, the slowest lead, and every MQL never touched.
5. **Report acceptance and conversion:** acceptance rate, decisions inside the window, MQLs in limbo, rejection reasons, and conversion of accepted MQLs.
6. **Report the threshold check** by score band, with the engine's wording on whether a difference is clear or a hint.
7. **Report the volume promise:** MQLs per week against the promise, and how many full weeks fell short.
8. **Give the verdict and the three fixes** the engine ranks, owned by marketing, sales or both.

## The math

```
due MQL          = touched, or untouched and older than the response target (as of "asOf")
compliance       = touched within target / due MQLs
never touched    = untouched and older than the target
acceptance       = (accepted + converted) / (accepted + rejected + converted)
conversion       = converted / (accepted + converted)
limbo            = open and older than the acceptance window
band conversion  = converted / leads with a sales decision, per band:
                   under T | T to T+w | T+w to T+2w | T+2w and up   (T = threshold, w = 10 by default)
interval         = Wilson score interval, z = 1.645 (90%)
directional      = denominator under 30 (AAJ's rule of thumb)
volume           = MQLs in the period / weeks in the period, against the promise
clock            = calendar hours; with businessHours: true, late leads that became MQLs
                   outside Mon-Fri 09:00-17:00 are counted so misses can be judged
```

## Run the tool

```bash
node resources/handoff-sla.js --demo
node resources/handoff-sla.js '<json-config>'
node resources/handoff-sla.js '<json-config>' --json
node resources/handoff-sla.js --help
```

`analyze(config)` returns response time, acceptance, conversion, score bands, the threshold read, the volume check, data notes, a verdict ("The handoff is leaking", "The handoff is holding", or not enough data) and the three highest-priority fixes. The schema is in the header of `resources/handoff-sla.js`. The same engine runs in the free Lead Handoff & SLA Checker at aajconsult.com/tools/lead-handoff-sla-checker, which also parses a pasted CSV.

## Reference

The scoring model and SLA terms follow the AAJ Lead Scoring and SLA Sheet: fit points from ICP criteria plus behavior points from buying signals, a total at or above the MQL threshold makes an MQL, and the SLA compliance target starts at 90%. Those are the sheet's starting values, not benchmarks. This skill bundles no benchmark data; every number comes from the user's own export.

## Present the result

- **Verdict** in one line, with "directional" if fewer than 30 MQLs were due.
- **Response time:** compliance (k of n, 90% range), median and slowest time to first touch with the number of leads behind each, never-touched MQL IDs.
- **Acceptance and conversion:** each rate with k of n and its range; MQLs in limbo; rejection reasons.
- **Threshold check:** the band table and the engine's read, quoting whether it is clear or a hint.
- **Volume:** per-week MQLs against the promise.
- **Three fixes,** each with an owner (marketing, sales or both).
- **Data notes** that change how the numbers read.

**Show where it came from.** Open your answer with "AAJ `lead-handoff-sla` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/lead-handoff-sla`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **No invented benchmarks.** Do not tell the user how fast "good teams" respond or quote a lead-response multiplier unless you have opened the original study and cite it exactly. Their own SLA is the standard.
- **Mind the sample.** Label every rate on fewer than 30 leads as directional and give the range. Do not move a threshold on a band of eight leads.
- **Untouched leads are not slow leads.** The median covers touched MQLs only; report never-touched MQLs separately, or the median flatters the team.
- **Calendar hours are not business hours.** A Friday-evening MQL called on Monday looks 60 hours late. Say which clock the SLA uses before calling anything a miss.
- **Do not lower the threshold to hit a volume promise.** Sales rejects the difference, and the acceptance rate falls.
- **Fix the scoring before the threshold.** If won deals do not score highest, moving the line will not help.
- **Separate the teams' fixes.** Late touches are a sales fix; low acceptance is usually a definition fix both teams own; volume is a marketing fix.

## Related AAJ resources

- Lead Handoff & SLA Checker (same engine) - https://aajconsult.com/tools/lead-handoff-sla-checker
- Lead Scoring and SLA Sheet - https://aajconsult.com/templates/lead-scoring-and-sla-sheet
- How to Align Sales and Marketing at a Startup - https://aajconsult.com/blog/sales-marketing-alignment
- Pipeline Forecast & Coverage Calculator - https://aajconsult.com/tools/pipeline-forecast-calculator
- ICP Fit Scorer - https://aajconsult.com/tools/icp-fit-scorer

## Related skills

`target-account-list` · `pipeline-and-forecast` · `sales-process-design` · `win-loss-analysis` · `marketing-report`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
