---
name: finishing-a-development-branch
description: Use when all implementation tasks are complete and verified - provides structured workflow to verify tests, present merge options, and execute cleanup
---

# Finishing a Development Branch

## Overview

Verify tests pass, present options, execute choice, and clean up.

**Core principle:** Test verification before any merge or PR action.

## The Process

### Step 1: Verify Tests

**Before anything else, verify tests pass:**

Run appropriate test command for project type.

**Cannot proceed with merge/PR until tests pass.**

### Step 2: Present Options

Present exactly four choices:

1. **Merge back to base branch locally**
2. **Push and create Pull Request**
3. **Keep the branch as-is for later**
4. **Discard the work entirely**

Keep explanations minimal - just present options.

### Step 3: Execute Choice

Based on user selection:
- **Option 1:** Merge, remove worktree
- **Option 2:** Push, create PR, preserve worktree
- **Option 3:** No changes, preserve worktree
- **Option 4:** Confirm (require typed "discard"), then remove worktree

### Step 4: Cleanup

Remove worktrees only for:
- Option 1 (merge)
- Option 4 (discard)

Preserve worktrees for:
- Option 2 (PR creation)
- Option 3 (keep branch)

## Safety Measures

- **Test gate:** Must pass before any merge/PR
- **Discard confirmation:** Requires typed confirmation
- **Selective cleanup:** Only removes worktrees when appropriate

## Common Pitfalls

- Skipping test verification
- Asking vague follow-up questions
- Automatic cleanup that removes needed worktrees
