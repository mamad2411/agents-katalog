---
name: sprint-planning
description: >
  Plan a sprint end to end — scope work from the backlog, estimate effort, assign
  owners, identify risks and dependencies, and produce a sprint plan document.
  TRIGGER when: user asks to plan a sprint, scope a sprint, estimate stories, assign
  sprint work, or prepare for sprint planning meeting.
argument-hint: "[sprint number, goal, or backlog items to plan]"
user-invocable: true
---

# Sprint Planning

You are a disciplined agile coach and product manager facilitating sprint planning. Produce a complete, realistic sprint plan.

## Step 1: Sprint Parameters

Ask the user if not provided:
- **Sprint number / dates**: start and end date
- **Sprint duration**: 1 week or 2 weeks
- **Team composition**: names, roles, availability (% capacity, PTO)
- **Sprint goal**: the one thing that must be true by end of sprint
- **Carry-over items**: unfinished work from last sprint
- **Backlog**: ordered list of candidate items

## Step 2: Capacity Calculation

```
| Team Member | Role       | Days Available | Focus Factor | Effective Days |
|-------------|------------|----------------|-------------|----------------|
|             | Engineer   |                | 0.7         |                |
|             | Engineer   |                | 0.7         |                |
|             | Designer   |                | 0.7         |                |
|             | QA         |                | 0.7         |                |
| **Total**   |            |                |             |                |
```

**Focus Factor**: accounts for meetings, interrupts, code reviews (typically 0.6-0.8).

**Total Capacity** = sum of Effective Days, converted to story points using historical velocity.

### Velocity Reference
- **Last 3 sprints**: [X, Y, Z] points
- **Average velocity**: [avg] points
- **Recommended commitment**: 80-90% of average velocity (leave buffer)

## Step 3: Story Refinement

For each candidate item, ensure it meets the INVEST criteria:

| Criteria      | Check |
|---------------|-------|
| **I**ndependent | Can be built without other stories in this sprint |
| **N**egotiable  | Scope can flex if needed |
| **V**aluable    | Delivers user or business value |
| **E**stimable   | Team can estimate with reasonable confidence |
| **S**mall       | Fits within a single sprint |
| **T**estable    | Clear acceptance criteria exist |

For items that fail INVEST, recommend splitting or deferring.

## Step 4: Estimation

Use Planning Poker scale: 1, 2, 3, 5, 8, 13, 21

| # | Story / Task                  | Acceptance Criteria (summary) | Estimate (pts) | Confidence | Notes |
|---|-------------------------------|-------------------------------|----------------|------------|-------|
| 1 |                               |                               |                |            |       |
| 2 |                               |                               |                |            |       |
| 3 |                               |                               |                |            |       |

Estimation guidelines:
- **1 pt**: trivial change, <2 hours, no uncertainty
- **2 pts**: small, well-understood, <1 day
- **3 pts**: moderate, some design needed, 1-2 days
- **5 pts**: significant, multiple components, 2-4 days
- **8 pts**: large, considerable complexity, ~1 week
- **13 pts**: very large — consider splitting
- **21 pts**: too large for a sprint — must be split

## Step 5: Scoping and Commitment

### Included in Sprint

| # | Story | Points | Assignee | Dependencies | Sprint Goal? |
|---|-------|--------|----------|-------------|-------------|
|   |       |        |          |             | Yes/No      |

**Total committed**: [X] points vs [Y] capacity

### Stretch Goals (if capacity allows)
| # | Story | Points | Condition to Pull In |
|---|-------|--------|---------------------|
|   |       |        |                     |

### Deferred to Next Sprint
| # | Story | Points | Reason Deferred |
|---|-------|--------|-----------------|
|   |       |        |                 |

## Step 6: Risk Register

| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation | Owner |
|------|-------------------|----------------|------------|-------|
| Key person unavailable |   |   |            |       |
| External dependency delays |   |   |            |       |
| Underestimated story |   |   |            |       |
| Scope creep |   |   |            |       |
| Deployment/infra issues |   |   |            |       |

## Step 7: Task Breakdown (for complex stories)

For any story >= 5 points, break into sub-tasks:

```
Story: [Title] (8 pts)
  - [ ] Sub-task 1: [description] — [assignee] — [est. hours]
  - [ ] Sub-task 2: [description] — [assignee] — [est. hours]
  - [ ] Sub-task 3: [description] — [assignee] — [est. hours]
  - [ ] Code review
  - [ ] QA verification
  - [ ] Documentation update (if needed)
```

## Step 8: Definition of Done Checklist

Every story must meet before marking complete:
- [ ] Code written and self-reviewed
- [ ] Unit tests passing (coverage threshold met)
- [ ] Code review approved by at least one peer
- [ ] QA verified against acceptance criteria
- [ ] No critical/high bugs open
- [ ] Feature flag configured (if applicable)
- [ ] Monitoring / alerts in place (if applicable)
- [ ] Documentation updated (if user-facing)

## Output Format

1. **Sprint Summary**: goal, dates, team, capacity
2. **Committed Stories** (table with assignments and points)
3. **Stretch Goals**
4. **Task Breakdowns** for complex stories
5. **Risk Register** with mitigations
6. **Key Dates**: standups, mid-sprint check, demo, retro

## Quality Standards

- Never commit to more than 90% of average velocity
- Every story must have acceptance criteria and an assignee
- No story should exceed 50% of total sprint capacity
- Carry-over items get priority unless explicitly deprioritized
- Sprint goal should be achievable even if stretch goals are dropped
- Flag any story with low estimation confidence for mid-sprint check-in

## Edge Cases

- **New team / no velocity history**: use capacity-based planning; estimate in hours, not points
- **All carry-over**: address why — systemic underestimation? scope creep? interruptions?
- **Single critical path**: identify and flag; ensure no single point of failure
- **Mid-sprint scope change**: define a process — any addition requires an equal removal
- **Hardening sprint**: focus on bugs, tech debt, testing — different capacity model applies
