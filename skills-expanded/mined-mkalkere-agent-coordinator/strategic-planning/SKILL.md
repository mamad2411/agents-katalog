---
name: strategic-planning
version: 1.0.0
description: Decompose goals into actionable plans with tasks, dependencies, and contingencies
uses:
  - analysis/deep-analysis
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - planning:execute
  requires_approval: false
---

# Strategic Planning

Decompose goals into actionable plans with tasks, dependencies, priorities, effort estimates, and contingencies.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `create_plan` is invoked, you (the agent) decompose the goal using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `planning/strategic-planning` in its skill list.

## When to Use

- A goal is too complex to accomplish in a single step
- Multiple workstreams need coordination
- Dependencies between tasks need to be identified and managed
- Stakeholders need visibility into what will happen and when
- Risks need contingency plans before execution begins
- Resources are constrained and work must be prioritized

## Methodology

### 1. Clarify the Goal

Before decomposing, ensure the goal is well-defined:
- **Outcome**: What does "done" look like? Define measurable success criteria
- **Scope**: What is included and excluded?
- **Constraints**: Budget, time, people, technology, regulatory limits
- **Stakeholders**: Who cares about this, and what do they need?

If the goal is vague, refine it. A plan built on a vague goal produces vague results.

### 2. Decompose into Workstreams

Break the goal into 3-7 major workstreams (themes of work):
- Each workstream should be independently understandable
- Workstreams map to logical domains, not organizational boundaries
- Name them by outcome, not activity ("User Authentication" not "Backend Work")

### 3. Decompose Workstreams into Tasks

For each workstream, identify concrete tasks:
- **Atomic**: Each task has a single, verifiable deliverable
- **Estimable**: Effort can be reasonably estimated (T-shirt sizes: S/M/L/XL)
- **Assignable**: A single person or team could own it
- **Ordered**: Position in sequence is clear

For each task, define:
- **Description**: What needs to be done (imperative voice)
- **Deliverable**: What artifact or outcome proves it's done
- **Effort**: S (hours), M (1-2 days), L (3-5 days), XL (1-2 weeks)
- **Priority**: Critical / High / Medium / Low

### 4. Map Dependencies

Identify relationships between tasks:
- **Blocks**: Task A must complete before Task B can start
- **Informs**: Task A's output influences Task B's approach (but B can start)
- **Parallel**: Tasks with no dependency can run simultaneously

Visualize as a dependency graph. Identify the **critical path** — the longest chain of dependent tasks that determines minimum total duration.

### 5. Identify Risks

For each significant risk:
- **Risk**: What could go wrong?
- **Likelihood**: Low / Medium / High
- **Impact**: Low / Medium / High
- **Mitigation**: How to reduce likelihood or impact
- **Contingency**: What to do if the risk materializes

Focus on risks that affect the critical path — these have the most impact on the plan.

### 6. Define Milestones

Set checkpoints that mark meaningful progress:
- Milestones are outcomes, not activities ("MVP deployed" not "coding done")
- Space them to provide regular feedback (every 1-2 weeks for long projects)
- Each milestone should be objectively verifiable

### 7. Resource Allocation

Map tasks to available resources:
- Identify bottlenecks (one person on the critical path)
- Balance workload across team members
- Flag resource conflicts explicitly
- Note skills required vs. skills available

## Output Format

```
## Plan: [Goal Name]

### Goal
[Clear statement of the desired outcome]

### Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Workstreams

#### WS1: [Workstream Name]
| # | Task | Deliverable | Effort | Priority | Depends On |
|---|------|-------------|--------|----------|------------|
| 1.1 | [Task description] | [Deliverable] | S/M/L/XL | Critical/High/Med/Low | — |
| 1.2 | [Task description] | [Deliverable] | M | High | 1.1 |

#### WS2: [Workstream Name]
| # | Task | Deliverable | Effort | Priority | Depends On |
|---|------|-------------|--------|----------|------------|
| 2.1 | [Task description] | [Deliverable] | L | Critical | — |

### Critical Path
[1.1] → [1.2] → [2.3] → [3.1]
Estimated total: [duration]

### Risks
| Risk | Likelihood | Impact | Mitigation | Contingency |
|------|-----------|--------|------------|-------------|
| [Risk 1] | High | High | [Action] | [Fallback] |

### Milestones
| Milestone | Target | Criteria |
|-----------|--------|----------|
| [M1 name] | [When] | [Verifiable outcome] |

### Open Questions
- [Question that needs answering before execution]
```

## Quality Criteria

- Goal has measurable success criteria
- Tasks are atomic and have clear deliverables
- Every dependency is explicitly mapped
- Critical path is identified
- Risks have both mitigations and contingencies
- Milestones are verifiable outcomes
- No circular dependencies
- Effort estimates use consistent scale

## Common Mistakes

- **Planning without a clear goal**: If you can't state success criteria, stop and clarify the goal first
- **Tasks too large**: If a task is XL, decompose it further. No task should be a "mini-project"
- **Missing dependencies**: Walk through the plan chronologically — "Can I really start B without A?"
- **Ignoring the critical path**: Optimizing non-critical tasks doesn't reduce total duration
- **No contingencies**: Every High-impact risk needs a Plan B
- **Over-planning**: Match plan detail to project complexity. A 2-day task doesn't need a Gantt chart
- **Circular dependencies**: If A depends on B and B depends on A, one dependency is wrong — break the cycle
- **Assuming perfect execution**: Build buffer into estimates. Things take longer than expected

## Completion

Planning is complete when:
- The goal is clearly defined with measurable success criteria
- All tasks are atomic, estimable, and have clear deliverables
- Dependencies are mapped and the critical path is identified
- Key risks have mitigations and contingencies
- Milestones provide verifiable progress checkpoints
- Open questions are documented for resolution before execution
