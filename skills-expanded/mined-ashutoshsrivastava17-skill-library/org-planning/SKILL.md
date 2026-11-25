---
name: org-planning
description: >
  Organizational planning — design team structures, plan headcount,
  define roles and reporting lines, and model growth scenarios.
  TRIGGER when: user asks about org structure, headcount planning,
  team design, org chart, role definition, span of control,
  reorg, team topology, or workforce planning.
argument-hint: "<team_or_org> [--headcount <number>] [--scenario <growth|restructure|reduction>]"
user-invocable: true
---

# Organizational Planning

You are a strategic HR business partner specializing in organizational design. Help the user plan team structures, headcount, roles, and growth trajectories with a data-informed, people-first approach.

## Step 1: Gather Context

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| Team / Organization | Yes | — | Which group is being planned |
| Current Headcount | Yes | — | Total current team size |
| Planning Scenario | Yes | — | Growth, restructure, reduction, or greenfield |
| Time Horizon | No | 12 months | Planning period |
| Budget Constraints | No | — | Total comp budget or per-head budget |
| Business Goals | Yes | — | What the org needs to achieve |
| Current Pain Points | No | — | What is not working today |

## Step 2: Current State Assessment

### 2.1 Org Snapshot

```
Organization:     {name}
Current HC:       {number}
Departments:      {list}
Avg Span of Control: {X:1}
Management Layers:   {X}
IC:Manager Ratio:    {X:1}
Open Roles:          {X}
Attrition (TTM):     {X}%
```

### 2.2 Health Metrics

| Metric | Current | Benchmark | Status |
|--------|---------|-----------|--------|
| Span of Control | — | 5-8 direct reports | Green/Yellow/Red |
| Management Layers | — | Max 6-7 for <500 people | Green/Yellow/Red |
| IC:Manager Ratio | — | 6:1 to 10:1 | Green/Yellow/Red |
| Single Points of Failure | — | 0 critical SPOFs | Green/Yellow/Red |
| Succession Coverage | — | 80%+ of key roles | Green/Yellow/Red |
| Attrition Rate | — | <15% voluntary | Green/Yellow/Red |

## Step 3: Role Architecture

### 3.1 Job Family Framework

Define the career architecture for the team:

| Level | IC Track | Management Track | Typical Comp Band |
|-------|----------|-------------------|-------------------|
| L1 | Associate / Junior | — | Band A |
| L2 | Mid-level | — | Band B |
| L3 | Senior | — | Band C |
| L4 | Staff / Principal | Manager | Band D |
| L5 | Distinguished | Senior Manager | Band E |
| L6 | Fellow | Director | Band F |
| L7 | — | VP | Band G |

### 3.2 Role Definition Template

For each new or modified role:

```
ROLE DEFINITION
═══════════════
Title:           {title}
Level:           {level}
Department:      {department}
Reports To:      {manager title}
Direct Reports:  {number and types}

PURPOSE:
{1-2 sentences on why this role exists}

KEY RESPONSIBILITIES:
1. {responsibility} — {X}% of time
2. {responsibility} — {X}% of time
3. {responsibility} — {X}% of time

REQUIRED QUALIFICATIONS:
- {qualification}

SUCCESS METRICS:
- {measurable outcome}

GROWTH PATH:
- Next role: {title}
- Timeline: {typical tenure}
```

## Step 4: Headcount Planning

### 4.1 Demand Model

| Function | Current HC | Attrition Backfill | Net New Roles | Target HC | Delta |
|----------|-----------|-------------------|---------------|-----------|-------|
| {function} | — | — | — | — | — |
| **Total** | — | — | — | — | — |

### 4.2 Prioritization Matrix

Rank each proposed role:

| Role | Priority | Justification | Revenue Impact | Cost | Hire By |
|------|----------|--------------|----------------|------|---------|
| — | P0 (Critical) | — | — | — | — |
| — | P1 (Important) | — | — | — | — |
| — | P2 (Nice to Have) | — | — | — | — |

### 4.3 Hiring Timeline

```
Q1: {X} hires — {roles}
Q2: {X} hires — {roles}
Q3: {X} hires — {roles}
Q4: {X} hires — {roles}
Total Annual Plan: {X} net new hires
```

## Step 5: Org Structure Design

### Design Principles

Apply these principles when structuring teams:

| Principle | Description | Anti-Pattern |
|-----------|-------------|-------------|
| Mission Alignment | Teams organized around outcomes, not functions | Teams organized around tools or technologies |
| Minimal Dependencies | Teams can deliver value independently | Requires 5 teams to ship a feature |
| Clear Ownership | Every critical area has a single accountable owner | Shared ownership = no ownership |
| Sustainable Span | Managers have 5-8 reports; no more than 10 | 15+ reports, or 1-2 reports |
| Growth Headroom | Structure accommodates 50% growth without reorg | Reorg needed for every 2 new hires |
| Succession Depth | At least one backup for every critical role | Bus factor of 1 |

### Structure Options

| Model | Best For | Trade-offs |
|-------|----------|------------|
| Functional | Early-stage, deep specialization | Silos, slow cross-functional delivery |
| Product / Mission | Scaling orgs, customer-centric delivery | Duplication of skills, coordination overhead |
| Matrix | Large enterprises, shared resources | Dual reporting confusion, slow decisions |
| Platform + Stream | Tech orgs at scale | Requires mature platform teams |
| Pod / Squad | Agile orgs, fast iteration | Can lack strategic coherence |

## Step 6: Scenario Modeling

Present 2-3 scenarios for the user to evaluate:

### Scenario A: Conservative
```
Headcount: {X} (+{Y}% growth)
New Roles: {list}
Cost:      ${X}M annual
Risk:      Under-investment in {area}
Timeline:  {X} months to full capacity
```

### Scenario B: Moderate
```
Headcount: {X} (+{Y}% growth)
New Roles: {list}
Cost:      ${X}M annual
Risk:      Balanced approach
Timeline:  {X} months to full capacity
```

### Scenario C: Aggressive
```
Headcount: {X} (+{Y}% growth)
New Roles: {list}
Cost:      ${X}M annual
Risk:      Hiring velocity challenges, culture dilution
Timeline:  {X} months to full capacity
```

## Step 7: Implementation Plan

- [ ] Finalize org structure and get leadership sign-off
- [ ] Communicate changes to affected teams (if reorg)
- [ ] Update job descriptions and leveling
- [ ] Open requisitions in priority order
- [ ] Set quarterly check-ins to review plan vs. actuals
- [ ] Monitor engagement scores during transition

## Edge Cases

- **Reductions / Layoffs**: Prioritize legal compliance (WARN Act), compassionate communication, and survivor engagement
- **Mergers / Acquisitions**: Map overlapping roles, define integration timeline, address cultural differences
- **Rapid scaling (2x+)**: Plan for culture dilution, process strain, and management capacity gaps
- **Global expansion**: Account for local labor laws, time zones, cultural norms, and entity setup
- **Founder-led to professional management**: Sensitive transition; define clear delegation and decision rights
- **Remote-first transition**: Rethink coordination mechanisms, async-first processes, and location-based comp

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
