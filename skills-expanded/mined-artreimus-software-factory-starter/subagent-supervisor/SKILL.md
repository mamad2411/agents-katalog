---
name: subagent-supervisor
description: Use when splitting complex work into independent subagent tasks with clear ownership, evidence, and integration responsibilities.
---

# Subagent Supervisor

## Workflow

1. Define the main objective and critical path.
2. Keep immediate blocking work local.
3. Delegate only independent sidecar tasks with clear scope.
4. Assign disjoint file ownership for write tasks.
5. Tell subagents they are not alone in the repo and must not revert others' work.
6. Collect evidence, changed files, and validation results.
7. Integrate results locally and run final validation.

## Good Delegation Targets

- read-only codebase mapping
- independent docs/spec review
- bounded implementation in a disjoint module
- independent PR or diff review
- validation that can run while implementation continues

## Output

Return the task split, each subagent's scope, accepted findings or changes, rejected findings with rationale, and final validation.
