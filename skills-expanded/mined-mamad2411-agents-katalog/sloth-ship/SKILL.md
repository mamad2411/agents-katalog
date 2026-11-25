---
name: sloth-ship
description: "Use when a Maycrest engagement branch is complete and tests pass — gating the handoff: verify the suite first, then choose merge, PR, keep, or discard, and produce a short client handoff package."
---

# Sloth Ship — The Handoff Gate 🦥

## Overview

Finishing a branch is a deliberate handoff, not a `git merge` reflex. The test gate comes
first — nothing merges or PRs until the suite is green. Then a structured choice, then a short
client handoff package so the work is reproducible by whoever runs it next.

**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Hand off → Clean up.

**Announce at start:** "Using sloth-ship to complete this work."

## Step 1: Verify Tests (the gate)

**Before any option, run the project's suite** (`npm test` / `cargo test` / `pytest` / `go test ./...`).

```
Tests failing (<N> failures). Must fix before completing:
[show failures]
Cannot merge or PR until tests pass.
```

Tests fail → **stop.** Do not proceed to Step 2. Tests pass → continue.

## Step 2: Detect Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | None (externally managed) |

## Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main — correct?"

## Step 4: Present Options

**Normal repo / named-branch worktree — exactly these 4:**

```
Implementation complete and tests pass. What would you like to do?
1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
Which option?
```

**Detached HEAD — drop merge, present exactly 3:** (1) push as new branch + PR, (2) keep
as-is, (3) discard.

**Don't add explanation** — keep options concise.

## Step 5: Execute Choice

**Option 1 — Merge locally.** Merge first, verify, then clean up:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
<test command>                       # verify tests on the merged result
# Only after merge succeeds: cleanup worktree (Step 6), then: git branch -d <feature-branch>
```

**Option 2 — Push and create PR.**
```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```
**Do NOT clean up the worktree** — Corey needs it alive to iterate on PR feedback.

**Option 3 — Keep as-is.** "Keeping branch <name>. Worktree preserved at <path>." No cleanup.

**Option 4 — Discard.** Confirm first:
```
This permanently deletes:
- Branch <name>   - Commits: <list>   - Worktree at <path>
Type 'discard' to confirm.
```
Wait for the exact word. Then `cd` to `MAIN_ROOT`, cleanup worktree (Step 6), then
`git branch -D <feature-branch>`.

## Step 6: Cleanup Workspace

**Only for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

- `GIT_DIR == GIT_COMMON`: normal repo, nothing to clean up.
- Worktree under `.worktrees/`, `worktrees/`, or `~/.config/superpowers/worktrees/`: we own it.
  ```bash
  MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
  cd "$MAIN_ROOT"
  git worktree remove "$WORKTREE_PATH"
  git worktree prune
  ```
- Otherwise: the harness owns this workspace. Do NOT remove it — use its exit tool if provided, else leave it.

## Step 7: Client Handoff Package (Options 1 & 2)

A merge or PR is not done until the next person can run it. Produce a short package:

```
HANDOFF — <engagement / branch>
- WHAT CHANGED: 2-4 bullets, plain language (features, fixes, schema/RLS changes)
- HOW TO RUN:   exact commands, e.g. `npm install && npm run dev`; env vars needed (ANTHROPIC_API_KEY, NEXT_PUBLIC_SUPABASE_URL…)
- WHAT WAS VERIFIED: test count + result, manual checks performed, platforms covered
- FOLLOW-UPS: known gaps or anything deferred
```

Keep it tight — the package IS the deliverable record. For a PR, this doubles as the body.

## Example: AOS Sober Living booking app

Branch `aos-booking-intake`. Suite → "Tests passing (38 tests, 0 failures)." Corey picks
Option 2 (PR); push, open it, and the handoff package becomes the PR body: **Changed** —
booking intake form + Supabase persistence + email-required guard. **Run** — `npm install &&
npm run dev`, needs `NEXT_PUBLIC_SUPABASE_URL` + anon key. **Verified** — 38 Vitest cases
green, manual intake submit on iOS Safari + Chrome. **Follow-ups** — SMS confirmation deferred.

## Red Flags

**Never:** proceed with failing tests · merge without verifying tests on the result · delete
work without typed confirmation · force-push without an explicit request · remove a worktree
before confirming merge success · clean up worktrees you didn't create · run `git worktree
remove` from inside the worktree.

**Always:** verify tests first · detect environment before the menu · present exactly 4
options (or 3 for detached HEAD) · get typed "discard" confirmation · clean up worktree for
Options 1 & 4 only · `cd` to main root before removal, then `git worktree prune` · ship the
handoff package on merge/PR.

## Integration with the Maycrest roster

- The branch shipped here is the one [sloth-worktree](../sloth-worktree/SKILL.md) isolated per engagement.
- Run [sloth-verify](../sloth-verify/SKILL.md) before Step 1 so the gate isn't your first look at the suite.
- Hand the package to `maycrest-ops:reality-checker` for the production-readiness verdict before it reaches the client.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
