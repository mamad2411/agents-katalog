---
name: delete-git-submodules
description: Remove a git submodule from the repo: .gitmodules, .git/modules, and working tree
argument-hint: "[submodule-path]"
related:
  - git-commit
  - ship

---
## Goal

Completely remove a git submodule from the repository — from `.gitmodules`, `.git/modules`, and the working tree

## Scope

Use for removing git submodule that are no longer needed, with cleanup of everything related

## Execute

### 1. Deinit Submodule

> Goal: Deinit Submodule

1. Run `git submodule deinit -f <submodule-path>` to remove the submodule from configuration
2. Verify that the submodule was deinitialized successfully

### 2. Remove From Gitmodules

> Goal: Remove From Gitmodules

1. Remove the submodule entry from `.gitmodules`
2. Remove the submodule entry from `.git/config`
3. If no submodules remain, delete the `.gitmodules` file entirely

### 3. Remove From Working Tree

> Goal: Remove From Working Tree

1. Run `git rm -f <submodule-path>` to remove the submodule from the working tree
2. Verify that the submodule folder is deleted

### 4. Clean Git Modules

> Goal: Clean Git Modules

1. Remove the submodule from `.git/modules/<submodule-path>`
2. On Windows, use `Remove-Item .git/modules/<submodule-path> -Recurse -Force`
3. On macOS/Linux, use `rm -rf .git/modules/<submodule-path>`

### 5. Garbage Collect

> Goal: Garbage Collect

1. Run `git gc` to clean up orphaned objects
2. Verify that no references remain

## Rules

### 1. Order Of Operations

- Always run `git submodule deinit` first
- Remove from `.gitmodules` before removing from the working tree
- Remove `.git/modules` only after the working tree is removed
- Run `git gc` as the final step

### 2. Safety Checks

- Check that the submodule has no uncommitted changes before deleting
- Check that no other dependencies reference that submodule
- In a monorepo, check that no other workspace uses that submodule

### 3. Cleanup Completeness

- Remove every part: `.gitmodules`, `.git/config`, `.git/modules`, working tree
- If it was the only submodule, delete `.gitmodules` entirely
- Always run `git gc` after the removal is done

- Use /git-commit if needed
- Use /ship if needed

## Expected Outcome

- The submodule is completely removed from the repository
- No references remain in `.gitmodules`, `.git/config`, `.git/modules`
- The working tree is clean with no submodule folder
- `git gc` completes without errors

