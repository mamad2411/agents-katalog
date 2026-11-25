---
name: large-refactor-migration
description: "Group skill: Large refactor/migration — audit, plan, parallel analysis, context save, execute, tests, review, and deploy."
risk: high
source: self
---

# 🔄 Large Refactor / Migration

> **Group Skill** — Orchestrates sub-skills for refactoring a codebase or migrating to a new framework.
> Activate by saying: "Refactor the codebase" or "plan a migration"

## When to Use

- Refactoring a large codebase
- Migrating to a new framework or architecture
- Need to ensure nothing breaks during the transition

## Step-by-Step Workflow

### Step 1: Audit
**Skill**: `codebase-audit-pre-push` / `vibe-code-auditor`
- Assess current codebase state
- Identify problem areas
- Measure technical debt

### Step 2: Plan
**Skill**: `orchestrate-batch-refactor`
- Create dependency-aware work packets
- Order changes by dependency
- Identify parallelizable work

### Step 3: Parallel Analysis
**Skill**: `parallel-agents`
- Run multiple agents analyzing simultaneously
- Split analysis by module
- Gather comprehensive insights

### Step 4: Context Save
**Skill**: `context-management-context-save`
- Preserve context across sessions
- Save analysis findings
- Track decisions made

### Step 5: Execute
**Skill**: `executing-plans`
- Implement changes with checkpoints
- Work through dependency order
- Validate at each step

### Step 6: Tests
**Skill**: `tdd-workflow` / `test-automator`
- Ensure nothing breaks
- Write tests for new code
- Run regression suite

### Step 7: Review
**Skill**: `code-reviewer` / `comprehensive-review-full-review`
- Quality gate review
- Check for regressions
- Verify migration completeness

### Step 8: Deploy
**Skill**: `deployment-engineer`
- Plan safe rollout
- Implement feature flags
- Monitor for issues

## Completion

Codebase is refactored with full test coverage and safe rollout. 🔄

## Sub-Skills Referenced

1. `codebase-audit-pre-push`
2. `vibe-code-auditor`
3. `orchestrate-batch-refactor`
4. `parallel-agents`
5. `context-management-context-save`
6. `executing-plans`
7. `tdd-workflow`
8. `test-automator`
9. `code-reviewer`
10. `comprehensive-review-full-review`
11. `deployment-engineer`
