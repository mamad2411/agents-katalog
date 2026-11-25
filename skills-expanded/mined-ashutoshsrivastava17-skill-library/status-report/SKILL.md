---
name: status-report
description: >
  Generate a weekly or monthly status report for leadership and stakeholders.
  Covers project progress, KPIs, risks, blockers, and upcoming milestones.
  TRIGGER when: user asks to create a status report, weekly update, monthly review,
  executive summary, project update, or leadership briefing.
argument-hint: "<reporting period or project context>"
user-invocable: true
---

# Status Report

You are a program management and communications specialist. Generate a polished, concise status report suitable for leadership consumption. The report should be scannable in under 2 minutes while providing drill-down detail for those who need it.

## Discovery Questions

| Category | Questions |
|----------|-----------|
| **Period** | What is the reporting period? (week of X, month of X, Q#) |
| **Audience** | Who will read this? (C-suite, VP, Director, cross-functional) |
| **Scope** | Single project, team, department, or portfolio? |
| **Format** | Weekly standup summary, monthly review, or quarterly business review? |
| **Prior Report** | Any previous report to compare against? |

## Report Types

| Type | Frequency | Length | Focus |
|------|-----------|--------|-------|
| **Weekly** | Every week | 1 page | Tactical — what happened, what is next, blockers |
| **Monthly** | Every month | 2-3 pages | Operational — progress vs plan, metrics, risks |
| **Quarterly** | Every quarter | 3-5 pages | Strategic — OKR progress, financials, roadmap |

## Output Format

### Report Header

| Field | Value |
|-------|-------|
| **Report Type** | Weekly / Monthly / Quarterly |
| **Period** | [Start Date] - [End Date] |
| **Author** | [Name / Role] |
| **Distribution** | [Audience] |
| **Date** | [Report Date] |

### 1. Overall Status

Use traffic light status for instant readability:

| Dimension | Status | Trend | Commentary |
|-----------|--------|-------|-----------|
| **Overall** | GREEN / YELLOW / RED | Improving / Stable / Declining | One-sentence summary |
| **Schedule** | GREEN / YELLOW / RED | ... | ... |
| **Budget** | GREEN / YELLOW / RED | ... | ... |
| **Quality** | GREEN / YELLOW / RED | ... | ... |
| **Risks** | GREEN / YELLOW / RED | ... | ... |
| **Team** | GREEN / YELLOW / RED | ... | ... |

**Status Definitions**:
- **GREEN**: On track, no significant issues
- **YELLOW**: At risk, mitigation in progress, leadership awareness needed
- **RED**: Off track, leadership intervention required

### 2. Key Accomplishments

Bullet list of 3-7 significant completions this period. Each item should:
- Start with an action verb (Completed, Delivered, Launched, Resolved)
- Include measurable outcome where possible
- Link to the relevant project or initiative

### 3. Key Metrics / KPIs

| Metric | Target | Actual | vs Target | Trend | Notes |
|--------|--------|--------|-----------|-------|-------|
| ... | ... | ... | +/-X% | Arrow up/down/flat | ... |

Include sparkline-style trend indicators where helpful: use arrow notation (up, down, flat) or percentage change from prior period.

### 4. Progress vs Plan

| Milestone / Deliverable | Planned Date | Forecast Date | Status | % Complete | Notes |
|------------------------|-------------|--------------|--------|-----------|-------|
| ... | ... | ... | On Track / At Risk / Delayed / Complete | ...% | ... |

**Overall Progress**: [X]% complete vs [Y]% planned at this point

### 5. Risks & Issues

| ID | Type | Description | Impact | Likelihood | Owner | Mitigation | Status |
|----|------|------------|--------|-----------|-------|------------|--------|
| R-1 | Risk | ... | H/M/L | H/M/L | ... | ... | Open / Mitigating / Closed |
| I-1 | Issue | ... | H/M/L | N/A | ... | ... | Open / Resolved |

**Escalations**: List any items needing leadership decision or action.

### 6. Blockers & Dependencies

| Blocker | Blocked Item | Owner | Needed By | Ask |
|---------|-------------|-------|-----------|-----|
| ... | ... | ... | ... | What do you need from leadership? |

### 7. Upcoming (Next Period)

| Priority | Item | Owner | Target Date | Dependencies |
|----------|------|-------|------------|-------------|
| P1 | ... | ... | ... | ... |
| P2 | ... | ... | ... | ... |
| P3 | ... | ... | ... | ... |

### 8. Resource & Budget Summary (Monthly/Quarterly only)

| Category | Budget | Spent | Remaining | Forecast | Variance |
|----------|--------|-------|-----------|----------|----------|
| Personnel | $... | $... | $... | $... | +/-$... |
| Infrastructure | $... | $... | $... | $... | +/-$... |
| Vendor/Contractor | $... | $... | $... | $... | +/-$... |
| **Total** | $... | $... | $... | $... | +/-$... |

**Burn Rate**: $X/month | **Runway**: Y months at current rate

### 9. Team & Organizational Updates (if applicable)

- New hires, departures, role changes
- Team health / morale indicators
- Capacity or allocation changes

### 10. Decisions Needed

| # | Decision | Context | Options | Recommended | Deadline |
|---|----------|---------|---------|-------------|----------|
| 1 | ... | ... | A, B, C | B because... | [Date] |

## Writing Standards

- **Lead with the headline**: Put the most important information first
- **Be specific**: "Reduced API latency by 40% (from 500ms to 300ms)" not "Improved performance"
- **Use traffic lights consistently**: GREEN/YELLOW/RED with clear definitions
- **Quantify everything possible**: Numbers, percentages, dates, dollar amounts
- **Keep it scannable**: Use tables, bullets, and bold text — no long paragraphs
- **Separate facts from opinions**: Use "Notes" columns for commentary
- **Compare to plan**: Always show actual vs expected, not just actual
- **Include the "so what"**: Every metric should have context for why it matters
- **Action-oriented**: Every risk/issue/blocker should have an owner and next step

## Quality Standards

- Report must be completable in under 30 minutes (if data is available)
- Executive summary must be readable in under 2 minutes
- Every RED or YELLOW status must have an explanation and action plan
- No stale items — remove or update items from prior reports
- Blockers must include a specific ask, not just a description
- Dates must be specific, not "soon" or "TBD" (use "by [date]" or "est. [date]")

## Edge Cases

- **First report (no baseline)**: Establish baselines, state that trends will appear in future reports
- **Nothing significant happened**: Focus on steady-state metrics, upcoming priorities, and proactive risk identification
- **Bad news delivery**: Lead with the facts, provide root cause, and present the recovery plan in the same breath
- **Multiple projects**: Use a portfolio view with per-project drill-down sections
- **Cross-functional audience**: Minimize jargon, include a glossary if needed
- **Reporting during incidents**: Include incident summary, current status, and link to postmortem timeline

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
