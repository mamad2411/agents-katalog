---
name: swe-workflow
description: A structured development workflow for coding agents. Use when starting a new feature, working on multi-step tasks, or when you need planning, validation, and quality checks. Follow Understand → Plan → Execute → Reflect phases with built-in safeguards against scope creep and incomplete implementations.
license: MIT
metadata:
  version: "1.0.1"
  author: "Evan Xu"
---

# SWE Workflow

A structured development workflow for coding agents — compatible with Pi, Claude Code, and Cursor.

## Quick Start

| Starting Point | Reference |
|----------------|-----------|
| New task or feature | [require-clarification](references/require-clarification.md) |
| Create plan from clarified request | [create-plan](references/create-plan.md) |
| Resume existing work | [resume-workflow](references/resume-workflow.md) |
| Execute plan step | [execute-step](references/execute-step.md) |

## Workflow Phases

### Phase 1: Understand

**Goal:** Ensure the request is fully understood before any work begins.

1. Read [require-clarification](references/require-clarification.md)
2. Analyze scope, inputs, outputs, success criteria
3. Ask targeted questions if ambiguous
4. Get user confirmation before proceeding

### Phase 2: Plan

**Goal:** Create a structured plan file as single source of truth.

1. Read [create-plan](references/create-plan.md)
2. Use [assets/plan-template.md](assets/plan-template.md) for structure
3. Break work into small, ordered steps (5-15 min each)
4. Save to `plans/<feature-name>.md`

### Phase 3: Execute

**Goal:** Implement one step at a time with validation gates.

For each step:

1. **Execute:** [execute-step](references/execute-step.md) — Implement the step
2. **Validate:** [validate-step](references/validate-step.md) — Check correctness
3. **Test:** [enforce-tests](references/enforce-tests.md) — Ensure coverage
4. **Review:** [review-diff](references/review-diff.md) — Critical self-review
5. **Persist:** [persist-plan](references/persist-plan.md) — Update plan status

### Phase 4: Reflect

**Goal:** Catch issues before they compound.

- Every 2-3 steps: [reflect-after-changes](references/reflect-after-changes.md)
- After all steps: [global-reflection](references/global-reflection.md)

## Reference Guide

| Reference | Purpose | When to Use |
|-----------|---------|-------------|
| [require-clarification](references/require-clarification.md) | Clarify ambiguous requests | Before any planning |
| [create-plan](references/create-plan.md) | Create structured plan | After clarification |
| [resume-workflow](references/resume-workflow.md) | Resume existing work | New session, context switch |
| [execute-step](references/execute-step.md) | Implement one step | Ready to code |
| [persist-plan](references/persist-plan.md) | Update plan status | After any progress |
| [validate-step](references/validate-step.md) | Verify correctness | After implementation |
| [enforce-tests](references/enforce-tests.md) | Ensure test coverage | After validation |
| [review-diff](references/review-diff.md) | Self-review changes | Before completing step |
| [protect-code](references/protect-code.md) | Prevent accidental deletion | Before modifying files |
| [maintain-repo-map](references/maintain-repo-map.md) | Track file locations | During planning & execution |
| [reflect-after-changes](references/reflect-after-changes.md) | Catch complexity | Every 2-3 steps |
| [global-reflection](references/global-reflection.md) | Final review | All steps complete |

## Workflow Guards

**Do NOT proceed if:**

| Condition | Required Action |
|-----------|-----------------|
| No plan file exists | Run create-plan |
| Plan has IN_PROGRESS steps | Complete or revert them |
| Clarification has open questions | Run require-clarification |
| Step validation failed | Fix issues first |
| Tests not written/run | Run enforce-tests |

**Do NOT skip:**

| Phase | Risk of Skipping |
|-------|------------------|
| Clarification | Wasted work on wrong scope |
| Planning | Lost context, scope creep |
| Validation | Bugs, incomplete implementations |
| Testing | No coverage, future breakage |
| Diff review | Artifacts, scope creep |
| Reflection | Accumulating complexity |

## Skill Chain

```
require-clarification → create-plan
                          ↓
                    execute-step → validate-step → enforce-tests → review-diff → persist-plan
                          ↑                                                                      |
                          |                                                                      ↓
                          └────────────────────── (next step) ←─────────────────────────────────┘
                                                          |
                                                          ↓
                                              reflect-after-changes (every 2-3 steps)
                                                          |
                                                          ↓
                                              global-reflection (when all done)
```

## Templates

- **Plan Template:** [assets/plan-template.md](assets/plan-template.md)

## Plan File Structure

All plans saved to `plans/<feature-name>.md` with this structure:

```markdown
# Plan: [Feature Name]

> Status: DRAFT | IN_PROGRESS | COMPLETED

## Goal
[One sentence]

## Assumptions
- [List assumptions]

## Repo Map
### Core Files
| Path | Purpose | Last Updated |
### Related Files
| Path | Why Relevant | Last Updated |
### Key Directories
| Path | Contents | Last Updated |

## Steps

### Step 1: [Title]
**Status:** PENDING
**Plan:** [Bullet list of actions]
**Validation Checklist:** [How to verify]
**Test Checklist:** [Test cases]
```

## Status Values

| Status | Meaning |
|--------|---------|
| PENDING | Not started |
| IN_PROGRESS | Currently being worked on |
| COMPLETED | Done, validated, tested |
| BLOCKED | Cannot proceed (reason documented) |

## Constraints

- **One step at a time** — Never batch multiple steps
- **Stay in scope** — Do not touch files outside the step's scope
- **Trust the plan** — Do not redo completed steps
- **Persist reality** — Keep plan file accurate at all times
- **Validate before complete** — No step passes with known issues