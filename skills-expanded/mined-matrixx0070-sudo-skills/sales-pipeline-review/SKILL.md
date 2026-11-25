---
name: sales-pipeline-review
version: 1.0.0
description: Inspect pipeline health — coverage, stage distribution, hygiene, and per-deal risk — and prescribe one specific corrective move per priority and at-risk deal.
author: matrixx0070
tags: [sales, pipeline, deal-review, coaching, hygiene]
capabilities: []
---

# Sales Pipeline Review

## When to use
Use this for a weekly or ad-hoc pipeline inspection when you have a list of open deals and need to know which to push, which to fix, which to cut, and whether coverage is enough.

**Not for:** producing the committed number (use sales-forecast); ranking today's actions (use sales-daily-briefing); prepping a single call (use sales-call-prep).

## Method
1. **Set the frame.** Confirm the quota/target and the period so coverage math is meaningful.
2. **Measure health.** Compute total pipeline, coverage ratio vs. target, and stage distribution. **Decision point:** coverage under ~3x → the headline finding is a pipeline-generation gap, not deal execution.
3. **Check hygiene.** Find deals with stale next steps, past close dates, no activity in N days, or missing key fields. Bad data hides real risk.
4. **Score each deal.** Rate on value, stage, momentum, and multithreading. Rank the ones worth the rep's hours.
5. **Flag risks.** Single-threaded deals, no economic buyer engaged, unaddressed competitor, or slipping timelines.
6. **Diagnose the shape.** Note stage-to-stage conversion or velocity problems, not just individual deals. **Decision point:** deals bunched in early stages → flag a late-stage drought that will hit next period.
7. **Prescribe actions.** For each priority and at-risk deal, give one specific next move and owner.

## Example
Target $500K, pipeline $1.1M → coverage 2.2x (under 3x, flag). Distribution: 70% in Stage 1-2 → thin late stage. Hygiene: 4 deals with close dates in the past, 2 missing amount. Top priority: $150K Stage-4 deal with momentum but single-threaded → action: multithread to the CFO this week. At-risk: $90K deal silent 21 days → action: break-up email or cut. Systemic flag: Stage 2→3 conversion is the leak; too many demos, too few POCs.

## Pitfalls
- **Coverage math without hygiene.** A big pipeline full of dead deals is fiction; clean first.
- **Deal-by-deal only.** Missing the conversion/velocity pattern treats symptoms, not the disease.
- **No cut decisions.** A review that never kills a deal just grows a bloated pipeline.
- **Vague prescriptions.** "Follow up" is not a move; name the action and the owner.

## Output format
```
Health summary: total $<> | coverage <>x | stage distribution <>
Top priorities (ranked):
  - <deal> — reason: <> — next move: <owner>
At-risk deals:
  - <deal> — <risk> — corrective action: <>
Hygiene issues:
  - <deal> — <missing data / stale next step>
Systemic flags: <conversion/velocity problems observed>
Recommended focus: <where the rep should spend this week>
```
