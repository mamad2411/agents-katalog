---
name: ops-status-report
version: 1.0.0
description: Produce a skimmable operational status report with R/Y/G health, KPI trends, risks, and owned action items.
author: matrixx0070
tags: [operations, status, reporting, kpi, health, stakeholders]
capabilities: []
---

# Status Report

## When to use
Use this for a recurring operational or project update to stakeholders, when leadership needs a fast read on health, or ahead of a review meeting where decisions and escalations are expected.

**Not for:** a detailed post-incident writeup, a one-time deep analysis, or an individual task update. This is a periodic, stakeholder-facing health snapshot.

## Method
1. **Set the frame.** State the reporting period, audience, and the initiative or team covered.
2. **Assign overall health.** Choose Green (on track), Yellow (at risk, has a plan), or Red (off track, needs help). Justify in one line. *Decision:* if any critical KPI is red or a blocker has no owner, the overall cannot be Green.
3. **Report KPIs.** Per key metric give current value, target, prior period, and trend arrow. Flag anything off-target.
4. **Summarize progress.** List what was completed this period against what was planned.
5. **Surface risks and blockers.** State each with impact and the ask — what you need from the reader.
6. **List action items.** Each with owner and due date; carry forward open items from last report.
7. **Preview next period.** The top priorities ahead.

Lead with the health color and the asks; detail supports, it does not bury.

## Example
**Period:** June, wk 4 | **Audience:** VP Eng | **Health: Yellow** — deploy pipeline stable, but SLA at risk from vendor outage.
- KPIs: uptime 99.4% (target 99.9%, prior 99.8%, down); tickets closed 142 (target 130, up).
- Done vs. planned: shipped auto-rollback (planned); migration slipped to July.
- Risk: vendor API instability threatens July SLA — **ask:** approve failover vendor spend.
- Actions: finalize failover contract (owner: Ops lead, due Jul 3).

## Pitfalls
- **Green-washing.** Reporting Green with a red KPI or an unowned blocker destroys trust; let the data set the color.
- **Burying the ask.** Readers skim; if what you need from them isn't near the top, it won't happen.
- **KPIs with no target or trend.** A bare number is not status — compare to target and prior period.
- **Action items with no owner or date.** Unowned actions roll forward forever; assign both every time.

## Output format
```
Header:        period | audience | health (R/Y/G) + one-line rationale
KPI table:     metric | current | target | prior | trend | status color
Accomplishments: planned vs. done
Risks/blockers: item | impact | ask
Action items:  item | owner | due | status
Next period:   top priorities
```
