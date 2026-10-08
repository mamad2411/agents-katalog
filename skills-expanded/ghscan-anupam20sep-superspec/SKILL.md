---
name: superspec-ship
description: Use when implementation is complete, validation has passed, and you need to decide how to integrate the work - runs SuperSpec's clean-validation gate, then guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# SuperSpec Ship

## Overview

Guide completion of development work by confirming validation is clean, then presenting clear options and handling the chosen workflow.

**Core principle:** Confirm clean validation → Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the superspec-ship skill to complete this work."

## The Process

### Step 0: Confirm Clean Validation (SuperSpec addition — not part of the copied source process)

**This gate does not exist upstream.** It is SuperSpec-specific and runs before anything else in this skill. Do not present the finish menu until it passes.

1. Look for a recent `superspec-validate` report for this feature.
   - If one exists and its Final Status reads `COMPLETE` / `FEATURE READY FOR RELEASE` (all of: coverage matrix 0 gaps, plan quality 0 critical findings, Principle 1 and Principle 2 evidence confirmed, execution-map gates signed off): the gate passes. Continue to Step 1.
   - If no recent report exists, or you cannot confirm it reflects the current state of the code: do not assume. Re-run the checks directly using the same tools `superspec-validate` uses — `build-matrix` and `lint-plan` from `@superspec-dev/core` (see `packages/core/src/mcp-server.ts`) — and confirm 0 gaps from `build-matrix` and 0 critical findings from `lint-plan` before proceeding.

2. **If the last known state is NOT clean** — the matrix has gaps, or a Critical/Important gate failure was reported (Principle 1 or Principle 2 violation, or an execution-map gate unsigned/failing) — **STOP**. Do not present the finish menu. Report exactly what is failing, using the same categories `superspec-validate` reports (Coverage Gap, Plan Quality, Principle 1/2 Violation, Gate Failure), and point back to:
   - `superspec-forge` — if the gap is in implementation or plan (fix loop), or
   - `superspec-validate` — if you need to re-run verification to get current evidence.

   ```
   Cannot ship: validation is not clean.

   1. **Coverage Gap (CRITICAL)**
      - FR-003: "User can share document" has no task
      - Action: → superspec-forge, then re-run superspec-validate

   Not proceeding to the finish menu until this is resolved.
   ```

3. **If clean:** continue to Step 1. Note in your own status that this check passed (e.g., "Validation gate: clean — build-matrix 0 gaps, lint-plan 0 critical findings").

### Step 1: Verify Tests

Step 0 covers coverage, plan quality, and constitution/gate compliance for the SuperSpec artifacts — but a project can have tests that live outside what `build-matrix` and `lint-plan` inspect (e.g., end-to-end suites, tests not yet wired into a task). Treat this as a final sanity layer, not a duplicate of Step 0.

**Before presenting options, verify the full test suite passes:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Detect Environment

**Determine workspace state before presenting options:**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

This determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | No cleanup (externally managed) |

### Step 3: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 4: Present Options

**Normal repo and named-branch worktree — present exactly these 4 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD — present exactly these 3 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>

# Only after merge succeeds: cleanup worktree (Step 6), then delete branch
```

Then: Cleanup worktree (Step 6), then delete branch:

```bash
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>
```

**Do NOT clean up worktree** — user needs it alive to iterate on PR feedback.

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then: Cleanup worktree (Step 6), then force-delete branch:
```bash
git branch -D <feature-branch>
```

### Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If `GIT_DIR == GIT_COMMON`:** Normal repo, no worktree to clean up. Done.

**If worktree path is under `.worktrees/` or `worktrees/`:** this workflow created this worktree — we own cleanup.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**Otherwise:** The host environment owns this workspace. Do NOT remove it. If your environment provides a workspace-exit tool, use it. Otherwise, leave the workspace in place.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes (force) |

## Common Mistakes

**Skipping the validation gate (Step 0)**
- **Problem:** Ship a feature with coverage gaps or unresolved Principle 1/2 violations
- **Fix:** Always confirm a clean `superspec-validate` report — or fresh `build-matrix`/`lint-plan` output — before presenting the finish menu

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly 4 structured options (or 3 for detached HEAD)

**Cleaning up worktree for Option 2**
- **Problem:** Remove worktree user needs for PR iteration
- **Fix:** Only cleanup for Options 1 and 4

**Deleting branch before removing worktree**
- **Problem:** `git branch -d` fails because worktree still references the branch
- **Fix:** Merge first, remove worktree, then delete branch

**Running git worktree remove from inside the worktree**
- **Problem:** Command fails silently when CWD is inside the worktree being removed
- **Fix:** Always `cd` to main repo root before `git worktree remove`

**Cleaning up harness-owned worktrees**
- **Problem:** Removing a worktree the harness created causes phantom state
- **Fix:** Only clean up worktrees under `.worktrees/` or `worktrees/`

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Present the finish menu without a clean validation gate (Step 0)
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Remove a worktree before confirming merge success
- Clean up worktrees you didn't create (provenance check)
- Run `git worktree remove` from inside the worktree

**Always:**
- Confirm `superspec-validate` is clean (or re-run `build-matrix`/`lint-plan` directly) before offering options
- Verify tests before offering options
- Detect environment before presenting menu
- Present exactly 4 options (or 3 for detached HEAD)
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only
- `cd` to main repo root before worktree removal
- Run `git worktree prune` after removal

---

**See also:**
- `superspec-validate` — produces the report this skill's Step 0 gate checks; re-run it if the last report is stale
- `superspec-forge` — fix coverage gaps, plan quality issues, or gate failures found by Step 0
- `packages/core/src/mcp-server.ts` — `build-matrix` and `lint-plan` tool definitions

<!-- Adapted from SP: skills/finishing-a-development-branch/SKILL.md (MIT). See /NOTICE. -->
