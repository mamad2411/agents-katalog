---
name: sprint-planning
description: "Helps PMs scope sprints, draft sprint goals tied to product outcomes, flag dependency risks, and balance capacity across new work, tech debt, and bug fixes. Grounded in Scrum methodology with practical adaptations for product-led teams."
category: execution
default_depth: standard
---

# Sprint Planning Support

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Helps PMs scope sprints, draft sprint goals tied to product outcomes, flag dependency risks, and balance capacity across new work, tech debt, and bug fixes. Grounded in Scrum methodology with practical adaptations for product-led teams.

## When to Use

- Preparing for sprint planning ceremonies
- Drafting sprint goals that connect to product outcomes
- Balancing competing priorities within a fixed capacity
- Identifying dependency risks before committing scope

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Small team, continuation sprint with minimal new scope | Define the Sprint Goal, Story Selection & Commitment |
| **Standard** | Regular sprint with new scope and cross-team touchpoints | All sections |
| **Deep** | Sprint with hard deadline, major dependencies, or team composition changes | All sections + individual capacity risk flags, contingency scope ladder (cut list priority order), daily stand-up focus prompts |

**Omit rules:** At Light depth, condense capacity and dependency analysis. Produce the goal and estimated story list. Label scope proposed until the team confirms capacity and material dependencies; an estimate alone is not a commitment.

## Framework

### Step 1: Define the Sprint Goal

A sprint goal is NOT a list of tickets. It's a single outcome statement the team commits to.

**Template:**
```
This sprint, we will [action] so that [outcome].
We'll know we succeeded when [measurable result].
```

**Good sprint goals:**
- "Enable self-serve onboarding so that new users can reach first value without sales assistance. Success: 30% of trial signups complete onboarding unassisted."
- "Resolve the top 3 data export reliability issues so that enterprise customers can trust automated reports. Success: Export error rate drops from 12% to < 2%."

**Bad sprint goals:**
- "Complete JIRA-1234, JIRA-1235, JIRA-1236" (that's a task list, not a goal)
- "Make progress on the dashboard redesign" (not measurable)

### Step 2: Capacity Planning

```markdown
## Sprint Capacity

### Team Availability
| Team Member | Role | Available Days | Notes |
|---|---|---|---|
| [Name] | [Eng/Design/QA] | [N] of [total] | [PTO, on-call, etc.] |

### Total Capacity: [N] person-days

### Allocation Guidelines
| Category | Target % | Person-Days | Rationale |
|---|---|---|---|
| Sprint goal work | 60-70% | [N] | New feature / initiative work |
| Bug fixes | 10-15% | [N] | Customer-reported and critical bugs |
| Tech debt | 10-15% | [N] | Reliability, performance, maintainability |
| Buffer | 10% | [N] | Unknowns, support escalations, reviews |
```

### Step 3: Story Selection & Commitment

```markdown
## Candidate Stories (ordered by sprint goal alignment)

### Sprint Goal Stories
| Story | Points/Days | Dependencies | Risk | Notes |
|---|---|---|---|---|
| [Story 1] | [est.] | None | Low | Core to sprint goal |
| [Story 2] | [est.] | Story 1 | Med | Needs design review |

### Bug Fixes (prioritized)
| Bug | Severity | Points/Days | Customer Impact |
|---|---|---|---|
| [Bug 1] | Critical | [est.] | [N] customers affected |

### Tech Debt
| Item | Points/Days | Benefit |
|---|---|---|
| [Item 1] | [est.] | [What it improves] |

### Total Committed: [N] points/days out of [capacity]
### Utilization: [X]% (target: 80-85%)
```

### Step 4: Dependency & Risk Check

```markdown
## Dependency Map
| Story | Depends On | Owner | Status | Risk Level |
|---|---|---|---|---|
| [Story] | [External API ready] | [Platform team] | [In progress] | HIGH |
| [Story] | [Design mockups] | [Designer] | [Complete] | LOW |

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [Design not finalized] | Medium | High | [Timebox: if not done by day 3, descope to v1] |
| [External dependency slips] | Low | High | [Parallel workstream ready] |
```

### Step 5: Sprint Agreement

```markdown
## Sprint [N] Agreement

**Sprint Goal:** [outcome statement]
**Duration:** [start], [end]
**Capacity:** [N] person-days

**We commit to:**
- [Story list with estimates]

**We'll stretch to (if capacity allows):**
- [Stretch story 1]

**We will NOT do this sprint:**
- [Explicitly deferred item], Reason: [why]

**Definition of Done for this sprint:**
- [ ] All committed stories meet their acceptance criteria
- [ ] Sprint goal metric is measurable (instrumentation in place)
- [ ] No critical bugs introduced
- [ ] Demo-ready for sprint review
```

## Minimum Evidence Bar

**Required inputs:** A prioritized backlog with estimated stories, team roster with availability for the sprint period, and a product goal or roadmap context for the sprint.

**Acceptable evidence:** Groomed backlog with story point estimates, team capacity spreadsheet or PTO calendar, prior sprint velocity data, and dependency status from upstream teams.

**Insufficient evidence:** If stories are unestimated or the team roster is unknown, stop and recommend running backlog grooming or capacity planning before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Team availability, known PTO, confirmed dependencies, and historical velocity must be grounded in evidence.
- **Hypotheses:** Story point estimates and sprint goal achievement probability are hypotheses -- label them as such and note estimation confidence.

## Output Format

Produce a Sprint Plan with:
1. **Sprint Goal**, outcome-oriented commitment
2. **Capacity Plan**, team availability and allocation
3. **Committed Scope**, stories with estimates, ordered by priority
4. **Dependencies & Risks**, flagged and mitigated
5. **Sprint Agreement**, what's in, what's stretch, what's out

**Shipwright Signature (required closing):**
6. **Decision Frame**, sprint scope recommendation with capacity utilization rationale, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, unconfirmed external dependencies, stories with low estimation confidence, untested capacity assumptions for new team members
8. **Pass/Fail Readiness**, PASS for commitment if the goal is outcome-oriented, estimates fit the agreed capacity with an explicit buffer, and material dependencies are confirmed. A Light proposal may list unresolved checks but must not claim committed scope. FAIL for commitment when those checks are missing.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Overcommitting**, Leave 10-15% buffer; things always take longer than expected
- **No sprint goal**, Without one, the sprint is just a random batch of work
- **Ignoring tech debt**, Zero tech debt allocation leads to compounding slowdowns
- **Hidden dependencies**, Surface cross-team deps before the sprint starts, not during
- **100% utilization**, Teams at 100% have no capacity for the unexpected; target 80-85%

## Weak vs. Strong Output

**Weak:**
> Sprint Goal: Work on dashboard and fix bugs. Committed: JIRA-101, JIRA-102, JIRA-103, JIRA-104, JIRA-105.

A task list with no outcome, no capacity check, and no way to evaluate whether the sprint succeeded.

**Strong:**
> Sprint Goal: Reduce dashboard load time so that enterprise users on 50k+ row datasets can interact without perceived lag. Success: p95 load time drops from 8s to under 2s. **Committed:** 42 points against 50-point capacity (84% utilization, 3-sprint velocity avg: 48). **Stretch:** DASH-220 (chart caching) if DASH-218 closes early.

Outcome-oriented goal with a measurable target, capacity grounded in historical velocity, and an explicit stretch/cut boundary.
