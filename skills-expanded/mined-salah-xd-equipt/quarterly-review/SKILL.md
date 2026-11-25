---
name: quarterly-review
description: "Creates quarterly business review documents with metric analysis, goal tracking, and strategic adjustments. Use when conducting end-of-quarter business performance reviews."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Quarterly Review

## When to Use This Skill

Use this skill when you need to:
- Conduct a structured quarterly business review
- Analyze performance against goals and OKRs
- Identify what worked, what did not, and what to adjust
- Set priorities and goals for the next quarter

**DO NOT** use this skill for weekly check-ins, annual planning, or financial-only reports. This is for comprehensive quarterly business reviews.

---

## Core Principle

A QUARTERLY REVIEW IS NOT A REPORT CARD — IT IS A STRATEGIC RECALIBRATION. THE GOAL IS TO DECIDE WHAT TO DO NEXT, NOT JUST DOCUMENT WHAT HAPPENED.

---

## Phase 1: Gather Data

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Quarter** | "Which quarter are you reviewing? (Q1, Q2, Q3, Q4 + year)" | Previous quarter |
| **Goals set for this quarter** | "What were your goals or OKRs for this quarter?" | No default — must be provided |
| **Key metrics** | "What are your core business metrics? (revenue, customers, growth, etc.)" | Revenue, customers, profit |
| **Revenue this quarter** | "What was total revenue this quarter?" | No default — must be provided |
| **Biggest wins** | "What were the top 3 wins this quarter?" | No default — must be provided |
| **Biggest challenges** | "What were the top 3 challenges or failures?" | No default — must be provided |

**GATE: Do not proceed without quarterly goals and actual results.**

---

## Phase 2: Performance Review

```
## Quarterly Business Review: [Q# Year]

### Goal Scorecard
| Goal | Target | Actual | Status | Notes |
|------|--------|--------|--------|-------|
| [Goal 1] | [Target] | [Actual] | Hit / Missed / Partial | [Context] |
| [Goal 2] | [Target] | [Actual] | Hit / Missed / Partial | |
| [Goal 3] | [Target] | [Actual] | Hit / Missed / Partial | |

**Goals hit:** [X] of [X] ([X]%)

### Financial Summary
| Metric | This Quarter | Last Quarter | QoQ Change | YTD |
|--------|-------------|-------------|-----------|-----|
| Revenue | $[X] | $[X] | +/-[X]% | $[X] |
| Expenses | $[X] | $[X] | +/-[X]% | $[X] |
| Net profit | $[X] | $[X] | +/-[X]% | $[X] |
| Profit margin | [X]% | [X]% | +/-[X]% | [X]% |
| Customers | [X] | [X] | +/-[X]% | |
| [Key metric] | [X] | [X] | +/-[X]% | |

### Monthly Breakdown
| | Month 1 | Month 2 | Month 3 | Quarter Total |
|--|---------|---------|---------|--------------|
| Revenue | $[X] | $[X] | $[X] | $[X] |
| Expenses | $[X] | $[X] | $[X] | $[X] |
| Net profit | $[X] | $[X] | $[X] | $[X] |
```

---

## Phase 3: Analysis

### What Worked

```
## Wins and Insights

### Top 3 Wins
1. **[Win]** — [What happened, quantified impact, why it worked]
2. **[Win]** — [Description and impact]
3. **[Win]** — [Description and impact]

### Key Insights
- [Insight about customers, market, or operations learned this quarter]
- [Insight]
```

### What Did Not Work

```
## Challenges and Lessons

### Top 3 Challenges
1. **[Challenge]** — [What happened, impact, root cause]
2. **[Challenge]** — [Description and root cause]
3. **[Challenge]** — [Description and root cause]

### Lessons Learned
- [Lesson — what will you do differently?]
- [Lesson]
```

### Strategic Questions

```
## Strategic Assessment

### Questions to Answer
1. Are we focused on the right priorities?
2. What should we START doing next quarter?
3. What should we STOP doing next quarter?
4. What should we CONTINUE doing next quarter?
5. Is our current strategy still the right one given what we learned?
```

---

## Phase 4: Next Quarter Plan

```
## [Next Quarter] Priorities

### Top 3 Goals
| Goal | Target | Metric | Owner | Deadline |
|------|--------|--------|-------|----------|
| [Goal 1] | [Specific target] | [How measured] | [Who] | [Date] |
| [Goal 2] | [Specific target] | [How measured] | [Who] | [Date] |
| [Goal 3] | [Specific target] | [How measured] | [Who] | [Date] |

### Key Initiatives
1. **[Initiative]** — [What, why, expected impact]
2. **[Initiative]** — [What, why, expected impact]
3. **[Initiative]** — [What, why, expected impact]

### Resource Allocation Changes
- [Any budget shifts, new hires, tool changes, or process improvements]

### Risks to Monitor
- [Risk 1] — Mitigation: [Plan]
- [Risk 2] — Mitigation: [Plan]
```

---

## Example: Solo Consultant Q4 Review

**Goals:** 1) Hit $45K revenue (Actual: $42K — 93%), 2) Launch group coaching (Done — 8 enrolled), 3) Reduce client concentration below 40% (Missed — top client still 48%).

**Key win:** Group coaching launched and immediately profitable at $2,400/month recurring.
**Key challenge:** Over-reliance on one client creates risk. Plan for Q1: add 2 new clients to reduce concentration to 35%.

---

## Anti-Patterns

- **Skipping the review entirely** — the quarter ends and you jump into the next one without reflection. Dedicate 2-3 hours to this.
- **All numbers, no narrative** — metrics without interpretation are just data. Explain what drove the numbers.
- **Setting the same goals after missing them** — if you missed a goal, analyze why. Either adjust the goal, change the approach, or remove it.
- **Too many goals** — 3-5 goals per quarter maximum. More than that dilutes focus.
- **No accountability mechanism** — write the review down and share it with someone (advisor, mastermind, partner) for accountability.

---

## Recovery

- **No goals were set last quarter:** Use this review to establish a baseline. Set 3 goals for next quarter and commit to reviewing them.
- **Terrible quarter (everything missed):** Focus on root causes, not symptoms. One bad quarter is a data point. Two bad quarters is a pattern that needs strategic change.
- **No financial tracking:** Use bank statements to reconstruct revenue and expenses. Set up proper tracking for next quarter.
- **Solo founder with no one to review with:** Write the review anyway. The act of documenting forces clarity. Share with a mentor, advisor, or mastermind group.
