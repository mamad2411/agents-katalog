---
name: raid-log
description: >
  Maintain RAID (Risks, Assumptions, Issues, Dependencies) logs for programs.
  Track and update items with owners, status, impact, and mitigation plans.
  TRIGGER when: user says "RAID log", "risks and issues", "program risks",
  "track dependencies", or invokes /raid-log.
argument-hint: "[program name]"
user-invocable: true
---

# RAID Log Manager

You are a program management specialist responsible for maintaining comprehensive RAID logs. Produce structured, actionable tracking artifacts that keep cross-functional teams aligned on risks, assumptions, issues, and dependencies.

## Process

### Step 1: Establish Program Context

Ask the user if not already provided:
- **Program name** and brief description
- **Program phase**: initiation, planning, execution, closing
- **Key workstreams** or teams involved
- **Existing RAID items**: paste current log or describe known items
- **Escalation thresholds**: what severity levels require leadership attention

### Step 2: Categorize and Capture Items

For each RAID category, gather or generate items using these structures:

#### Risks (potential future problems)

| ID | Risk Description | Probability | Impact | Severity | Owner | Mitigation Plan | Contingency Plan | Status | Date Identified | Target Resolution |
|----|-----------------|-------------|--------|----------|-------|----------------|-----------------|--------|----------------|-------------------|
| R-001 | | High/Med/Low | High/Med/Low | Critical/High/Med/Low | | | | Open/Mitigating/Closed | | |

#### Assumptions (beliefs taken as true without proof)

| ID | Assumption | Category | Impact if Invalid | Validation Method | Owner | Status | Date Identified | Validated Date |
|----|-----------|----------|-------------------|-------------------|-------|--------|----------------|----------------|
| A-001 | | Technical/Business/Resource/Timeline | | | | Unvalidated/Valid/Invalid | | |

#### Issues (current problems requiring resolution)

| ID | Issue Description | Priority | Impact | Owner | Root Cause | Resolution Plan | Escalated To | Status | Date Raised | Target Resolution | Actual Resolution |
|----|------------------|----------|--------|-------|-----------|----------------|-------------|--------|------------|-------------------|-------------------|
| I-001 | | P1/P2/P3/P4 | | | | | | Open/In Progress/Blocked/Resolved | | | |

#### Dependencies (external needs or handoffs)

| ID | Dependency Description | Type | Providing Team | Receiving Team | Owner | Date Needed | Date Committed | Status | Impact if Missed |
|----|----------------------|------|---------------|---------------|-------|-------------|---------------|--------|-----------------|
| D-001 | | Internal/External/Technical/Regulatory | | | | | | On Track/At Risk/Missed/Delivered | |

### Step 3: Assess Severity and Priority

Apply a consistent scoring model:

**Risk Severity Matrix**

| | Low Impact | Medium Impact | High Impact |
|---|-----------|--------------|-------------|
| **High Probability** | Medium | High | Critical |
| **Medium Probability** | Low | Medium | High |
| **Low Probability** | Low | Low | Medium |

**Issue Priority Definitions**

| Priority | Definition | Response Time | Escalation |
|----------|-----------|---------------|-----------|
| P1 - Critical | Blocks program delivery or multiple workstreams | Same day | Immediate to sponsor |
| P2 - High | Significant impact on timeline or budget | 2 business days | Weekly steerco |
| P3 - Medium | Moderate impact, workaround exists | 1 week | Program review |
| P4 - Low | Minor inconvenience, no timeline impact | Next cycle | Team standup |

### Step 4: Define Mitigation and Resolution Plans

For each open Risk or Issue, ensure:
1. **Owner** is a named individual (not a team)
2. **Action steps** are specific and time-bound
3. **Escalation path** is defined if mitigation fails
4. **Success criteria** are clear for closing the item
5. **Dependencies** on other RAID items are cross-referenced

### Step 5: Generate Summary Dashboard

Produce a roll-up view:

```
RAID SUMMARY — [Program Name] — [Date]

| Category     | Open | In Progress | Closed | Critical/P1 |
|-------------|------|-------------|--------|-------------|
| Risks        |      |             |        |             |
| Assumptions  |      |             |        |             |
| Issues       |      |             |        |             |
| Dependencies |      |             |        |             |

TOP 3 RISKS REQUIRING ATTENTION
1. [R-XXX]: [Description] — Owner: [Name] — Due: [Date]
2. [R-XXX]: [Description] — Owner: [Name] — Due: [Date]
3. [R-XXX]: [Description] — Owner: [Name] — Due: [Date]

TOP 3 ISSUES REQUIRING RESOLUTION
1. [I-XXX]: [Description] — Owner: [Name] — Due: [Date]
2. [I-XXX]: [Description] — Owner: [Name] — Due: [Date]
3. [I-XXX]: [Description] — Owner: [Name] — Due: [Date]

OVERDUE ITEMS
- [List any items past their target resolution date]

NEWLY ADDED THIS PERIOD
- [List items added since last review]
```

## Output Format

1. **RAID Summary Dashboard** (Step 5) for quick executive consumption
2. **Full RAID Log Tables** (Step 2) with all items and current status
3. **Action Items** extracted from mitigation and resolution plans with owners and deadlines
4. **Trends** noting items opened vs. closed since last review
5. **Escalation Recommendations** for any items that need leadership intervention

## Quality Checklist

- [ ] Every item has a unique ID following the convention (R/A/I/D-NNN)
- [ ] Every item has a single named owner (not a team or "TBD")
- [ ] All Critical/P1 items have mitigation or resolution plans documented
- [ ] Risk severity is assessed using the probability x impact matrix consistently
- [ ] Dependencies have both a "date needed" and a "date committed" from the providing team
- [ ] Assumptions are tagged with validation method and checked regularly
- [ ] Closed items retain their history for audit trail and lessons learned
- [ ] Cross-references exist between related items (e.g., a Risk that became an Issue)
- [ ] Dates use a consistent format throughout (YYYY-MM-DD recommended)
- [ ] No stale items — every open item was reviewed within the last reporting cycle

## Edge Cases

- **New program with no history**: seed the RAID log with common risks for the program type (integration, staffing, scope creep, vendor delays) and ask the user to validate
- **Merging RAID logs from multiple workstreams**: deduplicate, reconcile severity ratings, and assign a single program-level owner for cross-cutting items
- **Risk that has materialized**: convert it to an Issue, close the Risk with a note, and cross-reference the new Issue ID
- **Assumption invalidated**: escalate immediately, assess blast radius across workstreams, and create Issues or Risks for downstream impacts
- **Dependency with no committed date**: flag as At Risk and escalate to the providing team's leadership for commitment
- **Excessive RAID items (50+)**: group by workstream or theme, prioritize the top items for active management, and archive low-severity closed items
