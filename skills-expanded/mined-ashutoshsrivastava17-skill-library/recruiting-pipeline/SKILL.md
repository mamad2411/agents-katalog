---
name: recruiting-pipeline
description: >
  Manage and report on the recruiting pipeline — track candidates across
  stages, measure funnel conversion, forecast hiring, and identify bottlenecks.
  TRIGGER when: user asks about recruiting pipeline, hiring funnel, candidate
  tracking, recruiting metrics, sourcing report, pipeline review, hiring
  forecast, or recruitment status.
argument-hint: "[--role <role>] [--stage <sourcing|screen|interview|offer|closed>] [--report]"
user-invocable: true
---

# Recruiting Pipeline Management

You are a recruiting operations expert. Help the user track, analyze, and optimize their hiring pipeline from sourcing through close.

## Step 1: Gather Context

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| Role(s) | No | All open roles | Specific role or all |
| Department | No | All | Filter by department |
| Pipeline Data | Yes | — | Ask user for current candidate data or help them structure it |
| Reporting Period | No | Current quarter | For metrics and trends |
| Hiring Goals | No | — | Target number of hires and by-when |
| ATS in Use | No | — | Greenhouse, Lever, Ashby, etc. |

## Step 2: Pipeline Stages

### Standard Recruiting Funnel

| Stage | Definition | Typical Actions | Owner |
|-------|-----------|-----------------|-------|
| 1. Sourced / Applied | Candidate identified or applied | Resume review, initial screen | Sourcer / Recruiter |
| 2. Recruiter Screen | Phone/video screen with recruiter | Assess basics, interest, logistics | Recruiter |
| 3. Hiring Manager Screen | Conversation with the hiring manager | Assess role fit, experience depth | Hiring Manager |
| 4. Technical / Skills Assessment | Skills evaluation round | Coding challenge, case study, portfolio | Interview panel |
| 5. Onsite / Final Round | Comprehensive interview loop | Behavioral, technical, culture | Full panel |
| 6. Debrief | Interview panel decision meeting | Score review, calibration, decision | All interviewers |
| 7. Offer | Offer extended to candidate | Comp package, negotiation | Recruiter + HM |
| 8. Offer Accepted | Candidate accepts | Pre-boarding initiated | Recruiter |
| 9. Closed - Hired | Candidate starts | Handoff to onboarding | HR |
| 10. Closed - Rejected/Withdrawn | Candidate exits pipeline | Rejection sent, feedback logged | Recruiter |

## Step 3: Pipeline Tracker

### 3.1 Role-Level Pipeline View

```
PIPELINE SUMMARY — {Role}
═════════════════════════

Hiring Manager: {name}       Recruiter: {name}
Opened: {date}               Target Close: {date}
Priority: {P0/P1/P2}         Status: {On Track / At Risk / Behind}

Stage Breakdown:
  Sourced/Applied:     {XXX} candidates
  Recruiter Screen:    {XX}  candidates
  HM Screen:           {XX}  candidates
  Technical Round:     {X}   candidates
  Final Round:         {X}   candidates
  Offer:               {X}   candidates
  Accepted:            {X}   candidates
```

### 3.2 Candidate Tracker Table

| Candidate | Current Stage | Days in Stage | Source | Recruiter | Next Action | Due Date | Notes |
|-----------|--------------|---------------|--------|-----------|-------------|----------|-------|
| — | — | — | — | — | — | — | — |

### 3.3 Multi-Role Dashboard

| Role | Department | Priority | Pipeline Size | Offer Stage | Days Open | Status |
|------|-----------|----------|--------------|-------------|-----------|--------|
| — | — | — | — | — | — | — |

## Step 4: Funnel Metrics & Conversion Rates

### 4.1 Conversion Funnel

| Stage Transition | Volume | Conversion Rate | Benchmark | Status |
|-----------------|--------|----------------|-----------|--------|
| Applied -> Screen | — | — | 15-25% | — |
| Screen -> HM Screen | — | — | 40-60% | — |
| HM Screen -> Technical | — | — | 50-70% | — |
| Technical -> Final | — | — | 40-60% | — |
| Final -> Offer | — | — | 30-50% | — |
| Offer -> Accept | — | — | 80-90% | — |
| **Top of Funnel -> Hire** | — | — | **1-3%** | — |

### 4.2 Efficiency Metrics

| Metric | Value | Benchmark | Notes |
|--------|-------|-----------|-------|
| Time to Fill (days) | — | 30-60 days | From req open to offer accept |
| Time to Hire (days) | — | 20-40 days | From first contact to offer accept |
| Time in Stage (avg) | — | <7 days/stage | Identify bottleneck stages |
| Interviews per Hire | — | 4-8 | Too many = inefficient process |
| Sourcing Yield | — | 5-15% | Sourced candidates who become hires |
| Passthrough Rate | — | Varies | By stage, see funnel above |
| Offer Decline Rate | — | <15% | High rate = comp or process issue |

### 4.3 Source Effectiveness

| Source | Candidates | Hires | Conversion | Cost per Hire | Quality (90-day retention) |
|--------|-----------|-------|------------|--------------|---------------------------|
| LinkedIn | — | — | — | — | — |
| Referrals | — | — | — | — | — |
| Job Boards | — | — | — | — | — |
| Agency | — | — | — | — | — |
| Inbound/Careers Page | — | — | — | — | — |
| Events/University | — | — | — | — | — |

## Step 5: Pipeline Health Analysis

### Bottleneck Detection

For each stage with above-average dwell time or below-benchmark conversion:

```
BOTTLENECK IDENTIFIED
═════════════════════
Stage:           {stage name}
Avg Dwell Time:  {X} days (benchmark: {Y} days)
Conversion Rate: {X}% (benchmark: {Y}%)

Root Causes:
- {cause 1}
- {cause 2}

Recommended Actions:
1. {action} — Expected impact: {improvement}
2. {action} — Expected impact: {improvement}
```

### Pipeline Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Insufficient top-of-funnel volume | — | — | Increase sourcing, add channels |
| High offer decline rate | — | — | Review comp competitiveness, speed up process |
| Key candidates dropping out | — | — | Improve candidate experience, reduce time-in-process |
| Hiring manager availability | — | — | Block interview slots, use async options |
| Competing offers | — | — | Expedite strong candidates, prepare competitive counters |

## Step 6: Hiring Forecast

### Forecast Model

```
HIRING FORECAST — {Period}
══════════════════════════

Target Hires:        {X}
Current Pipeline:    {X} candidates across all stages
Expected Hires from Current Pipeline: {X} (based on conversion rates)
Gap:                 {X} additional hires needed

To close the gap, need:
  Additional Sourced Candidates: {X} (at {Y}% overall conversion)
  Additional Screens:            {X}
  Estimated Time to Fill Gap:    {X} weeks

Confidence Level: {High / Medium / Low}
```

## Step 7: Reporting & Communication

### Weekly Pipeline Update (for hiring managers)

```
WEEKLY PIPELINE UPDATE — {Date}
═══════════════════════════════

New this week:     {X} candidates added
Moved forward:     {X} candidates progressed
Rejected/Withdrew: {X} candidates exited
Offers extended:   {X}
Offers accepted:   {X}
Hires started:     {X}

Key highlights:
- {highlight 1}
- {highlight 2}

Action items:
- [ ] {action needed from hiring manager}
- [ ] {action needed from recruiter}
```

### Monthly Recruiting Report (for leadership)

Include:
- Hires vs. plan (actual/target)
- Pipeline health by department
- Time-to-fill trends
- Source mix and effectiveness
- Diversity pipeline metrics
- Cost-per-hire and budget utilization
- Forecast for upcoming month

## Edge Cases

- **Confidential searches**: Mark roles as confidential; restrict visibility in reports; use anonymized tracking
- **High-volume hiring**: Batch processing, group interviews, automated screening — adjust metrics for scale
- **Executive searches**: Longer timelines (90-120 days), smaller pipelines (5-10 candidates), agency-driven
- **Internal candidates**: Track separately; ensure fair process alongside external candidates
- **Referral-heavy pipelines**: Monitor for diversity impact; ensure referral bonus structure does not create bias
- **Hiring freezes**: Maintain warm pipelines; communicate transparently with candidates in process
- **Re-opened roles**: When an offer falls through or a hire does not work out, restart with urgency metrics

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
