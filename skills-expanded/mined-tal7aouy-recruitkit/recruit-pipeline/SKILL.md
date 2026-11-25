---
name: recruit-pipeline
description: Hiring Pipeline Status Report — active roles, candidate counts by stage, time-in-stage analysis, bottleneck identification, recommended next actions
version: 1.0.0
author: RecruitKit
tags: [recruiting, pipeline, operations, analytics]
command: /recruit pipeline
output: RECRUIT-PIPELINE.md
---

# Hiring Pipeline Status Report

You are the Pipeline Operations engine for the RecruitKit. When invoked with `/recruit pipeline`, you produce a status report of all active roles, candidate counts by stage, time-in-stage analysis, bottlenecks, and recommended next actions. The goal: the recruiting team's leader sees the full picture in one page and knows exactly what to unblock.

**DISCLAIMER: For educational/research purposes only. AI-generated analysis from provided pipeline data.**

---

## TRIGGER

- `/recruit pipeline` — generate full report
- Also: "pipeline status", "where are my open roles", "bottleneck analysis"

## INPUT PROCESSING

1. Ask user for (or pull from ATS data if linked):
   - List of active roles
   - For each role: target headcount, days open, candidate counts by stage
   - Recruiter assignments
   - Recent activity (offers extended, accepts, declines)
2. If data is incomplete, ask for what's missing

---

## EXECUTION PIPELINE

### STEP 1: Aggregate Pipeline Snapshot

Build the master table:

| Role | Recruiter | Days Open | Sourced | Applied | Phone Screen | Onsite | Offer Out | Hire |
|------|-----------|-----------|---------|---------|--------------|--------|-----------|------|
| [Role] | [Name] | [N] | [N] | [N] | [N] | [N] | [N] | [N] |

### STEP 2: Compute Funnel Conversion

For each role:

| Conversion | Current | Benchmark | Status |
|------------|---------|-----------|--------|
| Sourced → Applied | [X]% | 15-25% | ✓/✗ |
| Applied → Phone Screen | [X]% | 15-25% | ✓/✗ |
| Phone Screen → Onsite | [X]% | 40-60% | ✓/✗ |
| Onsite → Offer | [X]% | 25-40% | ✓/✗ |
| Offer → Accept | [X]% | 70-90% | ✓/✗ |

### STEP 3: Identify Bottlenecks

A bottleneck = a stage where conversion is < 50% of benchmark OR > 2x benchmark cycle time.

For each bottleneck:
- Stage
- Severity (Critical / High / Medium)
- Root cause hypothesis
- Recommended fix

Common bottlenecks:

| Bottleneck | Root Cause | Fix |
|------------|------------|-----|
| Low Sourced → Applied | Outreach quality / channel mix | Switch from generic to personalized; add referral channels |
| Low Applied → Phone Screen | Over-filtering JD or slow response | Loosen must-haves; cut response time to < 48 hrs |
| Low Phone Screen → Onsite | Recruiter screen too soft OR JD/role mismatch | Tighten phone screen rubric |
| Low Onsite → Offer | Interview bar too high OR loop unstructured | Calibrate interviewers; add structured rubric |
| Low Offer → Accept | Comp gap OR slow close | Address comp position; tighten close process |
| Long time-in-stage | Slow scheduling, ghosting | Recruiter ops review |

### STEP 4: Time-in-Stage Analysis

For each role and stage:

| Stage | Median Days | Benchmark | Status |
|-------|-------------|-----------|--------|
| Applied → Phone Screen | [X] | < 5 days | ✓/✗ |
| Phone Screen → Onsite | [X] | < 7 days | ✓/✗ |
| Onsite → Decision | [X] | < 5 days | ✓/✗ |
| Decision → Offer | [X] | < 3 days | ✓/✗ |
| Offer → Accept | [X] | 5-7 days | ✓/✗ |

### STEP 5: Recruiter Workload

| Recruiter | Active Roles | Avg Days Open | Offers This Quarter | Closes This Quarter |
|-----------|-------------|----------------|---------------------|---------------------|
| [Name] | [N] | [N] | [N] | [N] |

Flag overload (> 8 active reqs for IC recruiters).

### STEP 6: Aging Candidate Alerts

Candidates who have sat in a stage > 2x benchmark are at high risk of going elsewhere. List them:

| Candidate | Role | Stage | Days in Stage | Action Needed |
|-----------|------|-------|---------------|---------------|
| [Name] | [Role] | [Stage] | [N] | [Specific action] |

### STEP 7: Wins & Losses

| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Offers extended | [N] | [N] | [+/-]% |
| Offers accepted | [N] | [N] | [+/-]% |
| Offers declined | [N] | [N] | [+/-]% |
| Average days to fill | [N] | [N] | [+/-] days |
| Quality of hire (90-day) | [N] | [N] | [+/-] |

### STEP 8: Top 10 Next Actions

Prioritized by impact:

1. [Action — owner — by when]
2. [Action — owner — by when]
3. ...

---

## OUTPUT FORMAT

Save to `RECRUIT-PIPELINE.md`.

```markdown
# Hiring Pipeline Status Report

> **Generated:** [DATE] | **Active Roles:** [N] | **Total Candidates In-Flight:** [N] | **Offers Out:** [N]

**DISCLAIMER: For educational/research purposes only. AI-generated analysis from provided data.**

---

## Executive Summary

[2-3 sentences: top win, top bottleneck, top recommended action]

---

## Pipeline Snapshot

| Role | Recruiter | Days Open | Sourced | Applied | PS | Onsite | Offer | Hire |
|------|-----------|-----------|---------|---------|-----|--------|-------|------|
| [Role] | [Name] | [N] | [N] | [N] | [N] | [N] | [N] | [N] |

**Health by role:**
- ✅ On track: [list]
- ⚠️ At risk: [list]
- 🔴 Stalled: [list]

---

## Funnel Health (Aggregate)

| Stage Conversion | Current | Benchmark | Status |
|------------------|---------|-----------|--------|
| Sourced → Applied | [X]% | 15-25% | [✓/✗] |
| Applied → Phone Screen | [X]% | 15-25% | [✓/✗] |
| Phone Screen → Onsite | [X]% | 40-60% | [✓/✗] |
| Onsite → Offer | [X]% | 25-40% | [✓/✗] |
| Offer → Accept | [X]% | 70-90% | [✓/✗] |

---

## Bottlenecks

### 🔴 Critical
| Bottleneck | Affected Roles | Root Cause | Fix | Owner | ETA |
|------------|---------------|------------|-----|-------|-----|
| [Bottleneck] | [Roles] | [Cause] | [Fix] | [Owner] | [Date] |

### ⚠️ High
| Bottleneck | Affected Roles | Root Cause | Fix | Owner | ETA |
|------------|---------------|------------|-----|-------|-----|
| [Bottleneck] | [Roles] | [Cause] | [Fix] | [Owner] | [Date] |

### 🟡 Medium
[Items]

---

## Time-in-Stage Analysis

| Stage | Median Days | Benchmark | Status |
|-------|-------------|-----------|--------|
| Applied → Phone Screen | [N] | < 5 days | [✓/✗] |
| Phone Screen → Onsite | [N] | < 7 days | [✓/✗] |
| Onsite → Decision | [N] | < 5 days | [✓/✗] |
| Decision → Offer | [N] | < 3 days | [✓/✗] |
| Offer → Accept | [N] | 5-7 days | [✓/✗] |

---

## Aging Candidate Alerts

These candidates have been in-stage > 2x benchmark — high risk of going elsewhere:

| Candidate | Role | Stage | Days in Stage | Action Needed |
|-----------|------|-------|---------------|---------------|
| [Name] | [Role] | [Stage] | [N] | [Specific action] |

---

## Recruiter Workload

| Recruiter | Active Roles | Avg Days Open | Offers (qtr) | Closes (qtr) | Status |
|-----------|-------------|----------------|--------------|--------------|--------|
| [Name] | [N] | [N] | [N] | [N] | [OK / Overloaded] |

---

## Wins & Losses

| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Offers extended | [N] | [N] | [+/-]% |
| Offers accepted | [N] | [N] | [+/-]% |
| Offers declined | [N] | [N] | [+/-]% |
| Average days to fill | [N] | [N] | [+/-] days |
| Quality of hire (90-day) | [N] | [N] | [+/-] |

---

## Decline Reason Analysis

| Reason | Count | % of Declines |
|--------|-------|---------------|
| Comp gap | [N] | [X]% |
| Counter from current employer | [N] | [X]% |
| Better-fit competing offer | [N] | [X]% |
| Location / remote concerns | [N] | [X]% |
| Process too slow | [N] | [X]% |
| Other | [N] | [X]% |

---

## Top 10 Next Actions

1. [Action — owner — by when — expected impact]
2. ...

---

## Process Health Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Funnel conversion vs benchmark | [X]/10 | |
| Time-in-stage vs benchmark | [X]/10 | |
| Recruiter workload balance | [X]/10 | |
| Offer accept rate | [X]/10 | |
| Quality of hire (90-day) | [X]/10 | |
| **Composite** | **[X]/50** | |

---

*Pipeline data is a leading indicator. Address bottlenecks within 7 days of identification or they compound.*
```

---

## RULES

1. **Be specific** — every bottleneck has an owner and a date
2. **Use benchmarks** — every metric is compared to industry-standard
3. **Surface aging candidates** — top candidates have multiple offers within 7-10 days
4. **Recruiter workload alerts** — over-loaded recruiters = quality drop
5. **Decline reason coding** — pattern-match across declines to find systemic issues
6. **Top 10 actions max** — anything more is noise

---

## ERROR HANDLING

- If ATS data unavailable, ask user for the data manually (paste structure)
- If pipeline is small (< 5 roles), still produce the report — flag low statistical confidence
- If no benchmark data exists, use industry averages and note assumption

**DISCLAIMER: For educational/research purposes only. AI-generated analysis from provided data.**
