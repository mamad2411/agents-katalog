---
name: all-workspace
description: Run the same task across every workspace in a monorepo until all packages are done
argument-hint: "[scope]"
related:
  - deep-analyze
  - deep-validate
  - resolve-errors
  - run-build
  - run-test
  - use-subagents
  - refactor

---

## Goal

Work systematically across every workspace in a monorepo.

## Scope

Used for working across every workspace in a monorepo in the appropriate order.

## Execute

### 1. Discover Workspaces

> Goal: Discover Workspaces

Find and identify all workspaces in the monorepo.

1. Run `/deep-analyze` to review the full workspace configuration
2. Read the package manifests to see what workspaces exist
3. Order the workspaces by importance (foundation packages first, applications later)

### 2. Process Each Workspace

> Goal: Process Each Workspace

Work through each workspace in order.

1. Handle the foundation workspaces first (shared packages, utilities)
2. Handle workspaces with complex dependencies later
3. Avoid circular dependencies between workspaces
4. If the per-workspace task is independent and there are many workspaces → run `/use-subagents` to dispatch one agent per workspace/batch for parallel execution
5. If the task is reorganizing files/folders → run `/refactor` structure scope on each workspace one at a time

### 3. Verify Completion

> Goal: Verify Completion

Check that every workspace was processed completely.

1. Run `/deep-validate` to verify correctness
2. Check that no workspace was skipped
3. Check that no workspace has an unresolved issue

## Rules

### 1. Workspace Processing Order

Order the processing by importance.

- Handle the foundation workspaces first (shared packages, utilities)
- Handle workspaces with complex dependencies later
- Avoid circular dependencies between workspaces

### 2. Error Handling

Handle errors systematically.

- Record workspaces with problems for review
- Run `/resolve-errors` to fix issues in the workspaces
- Check that processing does not introduce new problems

### 3. Batch Operations

Use batch processing to improve efficiency.

- Read workspaces in parallel when possible
- Process workspaces sequentially to avoid conflicts
- Group workspaces of similar shape to process them together
- Use /run-build if needed
- Use /run-test all if needed

## Expected Outcome

- Every workspace in the monorepo is processed completely
- Processing follows the defined workflow
- No workspace is skipped or left with an unresolved issue
- The monorepo is in a correct state after processing
