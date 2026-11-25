---
name: practice-pulse
description: Read a practice's health from its own timesheet, fee, and staff data. Computes fee burn, earned value, cost performance (CPI), forecast cost at completion, and staff utilisation, flags projects that are overrunning, and shows every formula. Ships a script that runs on plain CSV exports from any timesheet tool. Use when the architect or practice manager wants to know "which projects are losing money", "fee burn", "are we over on this job", "utilisation", "resourcing next month", "project health check", or "practice dashboard". Hands to fee-proposal to price the next job from actual hours, and to client-pushback when an overrun comes from scope creep.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Practice pulse

Most small practices find out a job lost money after it's finished. This skill makes the numbers visible while there's still time to act: renegotiate scope, change the team, or have the conversation with the client.

## When to use

- Monthly or fortnightly project review.
- A job "feels" over and the principal wants the numbers.
- Resourcing: who is overloaded, who has capacity.
- Before pricing a similar job, to see what the last one really cost.

## Input

Three CSV exports (any timesheet or practice-management tool can produce them; map the column names if they differ):
- **timesheets.csv:** `date, person, project, hours`
- **fees.csv:** `project, fee, percent_complete` (optionally `invoiced`). `percent_complete` is the project lead's estimate of work done. Ask for it; don't derive it from hours, which would make the analysis circular.
- **staff.csv:** `person, cost_rate, weekly_capacity_hours`. `cost_rate` is the cost per hour to the practice (salary, on-costs, overhead share), not the charge-out rate. Ask how it was set.

Personal data: timesheets and pay-derived rates are confidential. Process them locally, and don't paste them into third-party tools.

## Process

1. **Map and check the data.** Confirm column mapping, currency, and the non-billable codes (office, leave, training). The script refuses if a person has no rate or a project has hours but no fee row. Fix the data. Don't fill gaps.
2. **Run** [scripts/practice_pulse.py](scripts/practice_pulse.py):
   `uv run scripts/practice_pulse.py timesheets.csv fees.csv staff.csv --from 2026-10-01 --to 2026-10-31`
3. **Read the flags.** A CPI below 0.9 (adjustable with `--flag-cpi`) means spending faster than progressing. Forecast above fee means the job will lose money on current performance.
4. **Explain each flagged project in one line** with the likely cause, if the data shows it (one person's hours spiking, a stage that ran long). Otherwise say the data doesn't show the cause and ask.
5. **Suggest actions** only of the kinds that are the practice's to take: check the % complete estimate, review scope against the appointment, re-plan the team, or raise additional services with the client (hand to `client-pushback`).

## Domain knowledge

- **Earned value in a design practice:** EV = fee x % complete. CPI = EV / cost. A CPI of 0.8 means every 100 spent has earned 80 of fee. It is only as good as the % complete estimate, so treat optimistic estimates with suspicion: an estimate of 90% that stays at 90% for weeks is a common pattern.
- **Fee burn vs progress:** burn ahead of % complete is the early warning. Burn alone isn't.
- **Utilisation:** billable hours / capacity. Very high utilisation over long periods usually means unrecorded overtime or burnout, not efficiency. Over 100% means hours above contracted capacity.
- **Stage fees:** if fees are split by stage (RIBA stages, AIA phases, HOAI Leistungsphasen), run per stage: progress within a stage is clearer than progress on a whole job.

## Output format

```
## Practice pulse: [period]

**Data:** [n] timesheet rows · [p] projects · [s] staff · currency [ ] · non-billable codes [ ]
**Formulas:** burn = cost/fee · EV = fee x %complete · CPI = EV/cost · forecast = cost/%complete

| Project | Hours | Cost | Fee | Burn | % done | EV | CPI | Forecast | Flag |
|---|---|---|---|---|---|---|---|---|---|

**Flagged:** [project: likely cause, or "cause not visible in data"]
**Utilisation:** [table; note anyone above capacity]
**Actions to consider:** [check % estimate / scope review / re-plan / additional services]
**Caveat:** % complete is an estimate by [who]; costs use cost rates set by [who, how].
```

## What you don't do

- Don't derive % complete from hours spent. Ask for the lead's estimate.
- Don't invent cost rates or capacity. Missing data is a refusal, not a default.
- Don't rank or judge individual staff performance from utilisation. It's a resourcing signal, not an appraisal.
- Don't give accounting, tax, or employment-law advice.
