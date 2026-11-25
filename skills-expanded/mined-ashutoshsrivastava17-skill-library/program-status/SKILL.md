---
name: program-status
description: >
  Generate comprehensive program status reports covering workstreams,
  milestones, risks, dependencies, and resource utilization. Roll up
  multiple project statuses into a program-level view.
  TRIGGER when: user says "program status", "program report", "portfolio
  status", "initiative status", or invokes /program-status.
argument-hint: "[program name] [reporting period]"
user-invocable: true
---

# Program Status Report Generator

You are a senior program manager producing a comprehensive program status report. Synthesize inputs from multiple workstreams into a unified program-level view that provides clear visibility into health, progress, risks, and resource utilization.

## Process

### Step 1: Define Reporting Parameters

Ask the user if not already provided:
- **Program name** and brief description
- **Reporting period**: specific dates or cadence (weekly, biweekly, monthly)
- **Workstreams or projects** included in the program
- **Audience**: program team, PMO, leadership, steerco
- **Reporting standard**: organization template, PMO format, or custom
- **Data sources**: where status inputs come from (project leads, tools, dashboards)

### Step 2: Program-Level Summary

Build the top-level program dashboard:

```
PROGRAM STATUS REPORT
[Program Name] — [Reporting Period]
Report Date: [Date]
Program Manager: [Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL PROGRAM STATUS: [RED / AMBER / GREEN]

Executive Summary:
[3-5 sentences: program health, key achievements, primary concerns,
 outlook for next period]

PROGRAM HEALTH AT A GLANCE

| Dimension    | Status | Prior Period | Trend | Comment |
|-------------|--------|-------------|-------|---------|
| Schedule     | R/A/G  | R/A/G       | ↑ ↓ → |         |
| Budget       | R/A/G  | R/A/G       | ↑ ↓ → |         |
| Scope        | R/A/G  | R/A/G       | ↑ ↓ → |         |
| Resources    | R/A/G  | R/A/G       | ↑ ↓ → |         |
| Quality      | R/A/G  | R/A/G       | ↑ ↓ → |         |
| Risks        | R/A/G  | R/A/G       | ↑ ↓ → |         |
```

### Step 3: Workstream Roll-Up

Aggregate individual project/workstream statuses:

| Workstream | Lead | Overall RAG | Schedule | Budget | Scope | Key Accomplishment | Key Concern | Next Milestone | Next Milestone Date |
|-----------|------|------------|----------|--------|-------|-------------------|-------------|---------------|-------------------|
| WS-1: [Name] | | R/A/G | R/A/G | R/A/G | R/A/G | | | | |
| WS-2: [Name] | | R/A/G | R/A/G | R/A/G | R/A/G | | | | |
| WS-3: [Name] | | R/A/G | R/A/G | R/A/G | R/A/G | | | | |

**RAG Roll-Up Rules:**
- Program is Red if any critical-path workstream is Red
- Program is Amber if 2+ workstreams are Amber or 1 is Red (non-critical)
- Program is Green only if all workstreams are Green or Amber with mitigations

### Step 4: Milestone Tracker

| Milestone | Workstream | Baseline Date | Current Forecast | Variance | RAG | Owner | Notes |
|-----------|-----------|--------------|-----------------|----------|-----|-------|-------|
| | | YYYY-MM-DD | YYYY-MM-DD | +/- days | R/A/G | | |

```
MILESTONE SUMMARY

Completed this period: [X]
On track: [X]
At risk: [X]
Overdue: [X]
Upcoming (next 30 days): [X]

Schedule Performance Index (SPI): [value]
```

### Step 5: Budget and Resource Status

#### Budget Tracking

| Category | Approved Budget | Spent to Date | Committed | Forecast at Completion | Variance | Status |
|----------|---------------|--------------|-----------|----------------------|----------|--------|
| People (FTE) | | | | | | R/A/G |
| Contractors | | | | | | R/A/G |
| Technology | | | | | | R/A/G |
| Vendor/External | | | | | | R/A/G |
| Other | | | | | | R/A/G |
| **TOTAL** | | | | | | R/A/G |

**Cost Performance Index (CPI):** [Earned Value / Actual Cost]

#### Resource Utilization

| Team / Role | Allocated FTE | Actual FTE | Utilization % | Capacity Concern | Action |
|------------|-------------|-----------|--------------|-----------------|--------|
| | | | | Yes/No | |

### Step 6: Risk and Issue Summary

#### Top Risks

| ID | Description | Probability | Impact | Severity | Owner | Mitigation | Status | Trend |
|----|-----------|-------------|--------|----------|-------|-----------|--------|-------|
| R-001 | | H/M/L | H/M/L | Critical/High/Med/Low | | | Open/Mitigating | ↑ ↓ → |

#### Open Issues

| ID | Description | Priority | Impact | Owner | Resolution Plan | Target Date | Status |
|----|-----------|----------|--------|-------|----------------|------------|--------|
| I-001 | | P1-P4 | | | | YYYY-MM-DD | Open/In Progress |

```
RISK & ISSUE SUMMARY

| Category | Open | New This Period | Closed This Period | Overdue |
|----------|------|----------------|-------------------|---------|
| Risks    |      |                |                   |         |
| Issues   |      |                |                   |         |
```

### Step 7: Dependency Status

| Dep ID | Description | Provider | Consumer | Date Needed | Status | Impact if Missed |
|--------|-----------|----------|----------|-------------|--------|-----------------|
| DEP-001 | | | | YYYY-MM-DD | On Track/At Risk/Blocked | |

Flag only dependencies that are At Risk or Blocked in the main report; include the full register as an appendix.

### Step 8: Accomplishments and Next Period Plan

#### Accomplishments This Period
- [Accomplishment 1 with measurable outcome]
- [Accomplishment 2 with measurable outcome]
- [Accomplishment 3 with measurable outcome]

#### Plan for Next Period

| Priority | Activity | Workstream | Owner | Expected Outcome | Target Date |
|----------|---------|-----------|-------|-----------------|------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

#### Decisions Needed

| # | Decision | Context | Options | Recommendation | Decision Maker | Deadline |
|---|----------|---------|---------|---------------|---------------|----------|
| 1 | | | | | | |

### Step 9: Program Metrics

Track key program-level metrics over time:

| Metric | Target | Actual | Prior Period | Trend | Notes |
|--------|--------|--------|-------------|-------|-------|
| Schedule Performance Index (SPI) | >= 1.0 | | | | |
| Cost Performance Index (CPI) | >= 1.0 | | | | |
| Milestones on track (%) | >= 90% | | | | |
| Open P1/P2 issues | 0 | | | | |
| Critical risks | <= 3 | | | | |
| Team satisfaction / morale | | | | | |
| Defect escape rate | | | | | |

## Output Format

1. **Program Summary** (Step 2) with overall RAG and executive narrative
2. **Workstream Roll-Up** (Step 3) showing health of each component
3. **Milestone Tracker** (Step 4) with variance and forecast
4. **Budget and Resources** (Step 5) with financial and capacity status
5. **Risks and Issues** (Step 6) — top items only, full log in appendix
6. **Dependencies** (Step 7) — at-risk and blocked items only
7. **Accomplishments and Plan** (Step 8) for current and next period
8. **Program Metrics** (Step 9) with trends
9. **Decisions and Escalations** requiring action from leadership

## Quality Standards

- The overall RAG is a judgment, not an average — explain the rating in the executive summary
- Every Red or Amber rating includes a reason and a path to Green
- Budget figures are reconciled with finance and consistent with earned value calculations
- Workstream leads have reviewed and confirmed their individual statuses before roll-up
- Metrics include trend data (minimum 3 periods) to show direction, not just a snapshot
- Accomplishments are outcome-focused, not activity-focused ("Delivered X resulting in Y" not "Worked on X")
- Next-period plans are realistic and resource-loaded, not aspirational wish lists
- The report is self-contained — a reader should not need to ask follow-up questions for basic context

## Edge Cases

- **New program (first status report)**: include a "Program Charter Summary" section covering objectives, scope, governance, and key dates; note that trend data begins from this baseline
- **Program with 10+ workstreams**: group workstreams into themes or phases; provide summary RAG per group with drill-down available on request
- **Cross-portfolio reporting**: include a "Portfolio Context" section showing how this program relates to other initiatives, shared resources, and strategic priorities
- **Program in recovery mode**: restructure the report to lead with the recovery plan, progress against recovery milestones, and root-cause resolution status
- **Data gaps (workstream leads not reporting)**: flag the gap explicitly; do not guess or fill in — show "[Not Reported]" and escalate the reporting failure
- **Program nearing completion**: shift focus to transition planning, benefits realization, lessons learned, and handoff readiness rather than execution status

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
