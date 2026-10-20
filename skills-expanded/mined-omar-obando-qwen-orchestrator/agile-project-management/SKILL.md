---
name: agile-project-management
description: Use when managing agile projects, facilitating Scrum ceremonies, conducting backlog grooming, sprint planning, velocity tracking, and implementing Kanban workflows. Includes agile metrics, team dynamics, and agile transformation guidance. Based on CSM, CSP, PRINCE2 certifications.
license: MIT
---

# Agile Project Management Skill — Project Manager

## Overview

This skill provides comprehensive guidance for managing agile projects following Scrum, Kanban, and hybrid methodologies. It covers Scrum ceremonies, backlog grooming, sprint planning, velocity tracking, and agile metrics following CSM, CSP, and PRINCE2 certifications.

## When to Use

**Use this skill when:**

- Managing agile projects using Scrum
- Facilitating Scrum ceremonies (standups, planning, reviews, retrospectives)
- Conducting backlog grooming and refinement
- Planning sprints and setting sprint goals
- Tracking team velocity and capacity
- Implementing Kanban workflows
- Managing agile project metrics
- Facilitating agile team meetings
- Coaching teams on agile practices
- Managing agile project documentation
- Implementing agile project governance
- Conducting agile project reviews
- Managing agile project risks
- Implementing agile project quality
- Managing agile project scope
- Conducting agile project estimation
- Implementing agile project scheduling
- Managing agile project stakeholder expectations
- Conducting agile project reporting
- Implementing agile project communication
- Managing agile project dependencies
- Conducting agile project release planning
- Implementing agile project portfolio management

**Do NOT use this skill when:**

- Writing application business logic (use domain-driven skill)
- Designing database schemas (use database-design skill)
- Writing API endpoint specifications (use api-design skill)
- Performing security audits (use security-auditor skill)
- Writing SQL queries (use sql-best-practices skill)
- Designing multi-page website layouts (use design-system skill)
- Analyzing deployment configurations (use deployment skill)
- Writing documentation (use documentation-best-practices skill)

## Scrum Framework

### Scrum Ceremonies

```
┌─────────────────────────────────────────────────────────────┐
│              Scrum Ceremonies                               │
├─────────────────────────────────────────────────────────────┤
│  1. Sprint Planning (2-4 hours)                             │
│     - Set sprint goal                                       │
│     - Select backlog items                                  │
│     - Break down tasks                                      │
│                                                              │
│  2. Daily Standup (15 minutes)                              │
│     - What did you do yesterday?                            │
│     - What will you do today?                               │
│     - Any blockers?                                         │
│                                                              │
│  3. Sprint Review (1-2 hours)                               │
│     - Demo completed work                                   │
│     - Gather feedback                                       │
│     - Update backlog                                        │
│                                                              │
│  4. Sprint Retrospective (60-90 minutes)                    │
│     - What went well?                                       │
│     - What could improve?                                   │
│     - Action items                                          │
└─────────────────────────────────────────────────────────────┘
```

### Sprint Planning Template

```
┌─────────────────────────────────────────────────────────────┐
│              Sprint Planning Agenda                         │
├─────────────────────────────────────────────────────────────┤
│  1. Sprint Goal Definition (15 min)                         │
│     - Clear, measurable goal                                │
│     - Align with product vision                             │
│                                                              │
│  2. Story Selection (30 min)                                │
│     - Review high-priority stories                          │
│     - Estimate effort                                       │
│     - Commit to achievable amount                           │
│                                                              │
│  3. Task Breakdown (30 min)                                 │
│     - Break stories into tasks                              │
│     - Assign task owners                                    │
│     - Identify risks                                        │
│                                                              │
│  4. Commitment & Capacity (15 min)                          │
│     - Verify team capacity                                  │
│     - Confirm sprint goal                                   │
│     - Document commitments                                  │
└─────────────────────────────────────────────────────────────┘
```

## Backlog Management

### Backlog Grooming Template

```
┌─────────────────────────────────────────────────────────────┐
│              Backlog Grooming Session                       │
├─────────────────────────────────────────────────────────────┤
│  Frequency: Weekly, 60-90 minutes                           │
│  Attendees: Product Owner, Tech Lead, Team                  │
│                                                              │
│  1. Review Completed Items (10 min)                         │
│     - Demo completed work                                   │
│     - Accept or reject                                      │
│                                                              │
│  2. Prioritize New Requests (20 min)                        │
│     - Review new requests                                   │
│     - Prioritize using MoSCoW                               │
│     - Assign priority                                       │
│                                                              │
│  3. Refine Upcoming Stories (30 min)                        │
│     - Break down large stories                              │
│     - Add acceptance criteria                               │
│     - Update estimates                                      │
│                                                              │
│  4. Estimate New Stories (20 min)                           │
│     - Use planning poker                                    │
│     - Resolve estimation discrepancies                      │
│     - Update story points                                   │
│                                                              │
│  5. Identify Dependencies (10 min)                          │
│     - Identify cross-team dependencies                      │
│     - Plan coordination                                     │
└─────────────────────────────────────────────────────────────┘
```

### Backlog Prioritization

```
┌─────────────────────────────────────────────────────────────┐
│              Prioritization Techniques                      │
├─────────────────────────────────────────────────────────────┤
│  MoSCoW Method:                                             │
│  - Must have: Critical for MVP                              │
│  - Should have: Important but not critical                  │
│  - Could have: Nice to have                                 │
│  - Won't have: Not in current scope                         │
│                                                              │
│  Value vs Effort Matrix:                                    │
│  High Value ──┐    ●    ●                                   │
│               │  ●                                          │
│               │                                             │
│  Low Value ──└───────────────► Low Effort                   │
│                                                              │
│  RICE Scoring:                                              │
│  Score = (Reach × Impact × Confidence) / Effort             │
└─────────────────────────────────────────────────────────────┘
```

## Velocity Tracking

### Velocity Calculation

```
┌─────────────────────────────────────────────────────────────┐
│              Velocity Tracking                              │
├─────────────────────────────────────────────────────────────┤
│  Sprint 1: 24 points completed                              │
│  Sprint 2: 28 points completed                              │
│  Sprint 3: 22 points completed                              │
│  Sprint 4: 26 points completed                              │
│                                                              │
│  Velocity = (24 + 28 + 22 + 26) / 4 = 25 points             │
│                                                              │
│  Capacity Planning:                                         │
│  Team Capacity = Velocity × (1 - Buffer)                    │
│  Buffer = 30% (meetings, unplanned, learning)               │
│  Capacity = 25 × 0.7 = 17.5 points                          │
└─────────────────────────────────────────────────────────────┘
```

### Velocity Chart

```
┌─────────────────────────────────────────────────────────────┐
│              Velocity Chart                                 │
├─────────────────────────────────────────────────────────────┤
│  30 ┤                  ●                                    │
│  28 ┤               ●    ●                                  │
│  26 ┤            ●           ●                              │
│  24 ┤         ●                                             │
│  22 ┤      ●                                                │
│     └───────────────────────────────────────               │
│       S1    S2    S3    S4    S5    S6    S7               │
│                                                              │
│  Trend: Stable velocity (22-28 points)                      │
│  Action: Continue current pace                              │
└─────────────────────────────────────────────────────────────┘
```

## Kanban Methodology

### Kanban Board

```
┌─────────────────────────────────────────────────────────────┐
│              Kanban Board                                   │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐│
│  │  Backlog  │  │  To Do    │  │ In Progress│  │  Done     ││
│  │  [15]     │  │  [3]      │  │  [5]      │  │  [20]     ││
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘│
│         │             │             │             │          │
│         └─────────────┴─────────────┴─────────────┘          │
│                              │                               │
│                    ┌─────────▼─────────┐                     │
│                    │  WIP Limit: 5     │                     │
│                    └───────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### Kanban Metrics

```
┌─────────────────────────────────────────────────────────────┐
│              Kanban Metrics                                 │
├─────────────────────────────────────────────────────────────┤
│  Cycle Time: Time from start to completion                  │
│  Lead Time: Time from request to completion                 │
│  Throughput: Number of items completed per time period      │
│  WIP: Work in Progress                                      │
│                                                              │
│  Example:                                                   │
│  - Average Cycle Time: 3 days                               │
│  - Average Lead Time: 5 days                                │
│  - Weekly Throughput: 8 items                               │
│  - Current WIP: 5 (limit: 5)                                │
└─────────────────────────────────────────────────────────────┘
```

## Agile Metrics

### burndown Chart

```
┌─────────────────────────────────────────────────────────────┐
│              Burndown Chart                                 │
├─────────────────────────────────────────────────────────────┤
│  Stories Remaining                                          │
│  20 ┤    ╱                                                  │
│  15 ┤   ╱                                                   │
│  10 ┤  ╱                                                    │
│   5 ┤ ╱                                                     │
│   0 └───────────────────────────────────────               │
│     Day 1  Day 5  Day 10  Day 15  Day 20                   │
│                                                              │
│  Trend: On track (blue line)                                │
│  Action: Continue current pace                              │
└─────────────────────────────────────────────────────────────┘
```

### Agile Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│              Agile Dashboard                                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Velocity   │  │  Sprint     │  │  Burnup     │         │
│  │  Chart      │  │  Progress   │  │  Chart      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Blockers   │  │  Team       │  │  Quality    │         │
│  │  List       │  │  Capacity   │  │  Metrics    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Real-World Impact

**Before this skill:**

- Unstructured project management
- Missed deadlines
- Scope creep
- Team confusion
- No visibility

**After this skill:**

- Structured agile project management
- On-time delivery
- Clear scope and priorities
- Team alignment
- Transparent progress

## Cross-References

- **`product-owner`** - For backlog management and user stories
- **`scrum-master`** - For facilitating Agile ceremonies
- **`devops-pipeline`** - For CI/CD and deployment strategies

## References

- [Scrum Guide](https://scrumguides.org/)
- [Agile Manifesto](https://agilemanifesto.org/)
- [PRINCE2 Manual](https://www.axelos.com/certifications/prince2)
- [Kanban by David Anderson](https://kanbandivision.com/)
