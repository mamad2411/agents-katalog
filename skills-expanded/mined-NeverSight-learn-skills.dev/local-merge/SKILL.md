---
name: local-merge
description: Use when merging a branch to main without touching the primary worktree directly, when /ship or /reflect needs to integrate work, or when autonomous mode blocks direct main commits
---

# /local-merge

Merge a branch into a target branch via a disposable shallow clone, then propagate to the primary worktree non-destructively. Defaults to main if no target specified.

## Inputs

| Input | Required | Default | Example |
|-------|----------|---------|---------|
| `BRANCH` | yes | — | `feat/local-merge-skill` |
| `TARGET` | no | `main` | `develop`, `release/v2` |
| `PRIMARY` | no | First line of `git worktree list` | `/Users/you/projects/repo` |
| `MESSAGE` | no | `merge: $BRANCH into $TARGET` | `merge: feat/auth into main` |

## Phase 1 — Remote Merge (mechanical)

All commands are explicit. No reasoning required.

### 1a. Calculate clone depth

```bash
git fetch origin "$TARGET" "$BRANCH"
DEPTH=$(( $(git rev-list --count origin/"$TARGET"..origin/"$BRANCH") + 10 ))
```

### 1b. Clone, merge, push

Validate inputs before shell interpolation — branch names must match git's allowed character set:

```bash
# Validate branch names (reject shell metacharacters)
case "$BRANCH$TARGET" in *['$`\!']*) echo "Invalid branch name"; exit 1 ;; esac

MERGE_DIR="${CLAUDE_SESSION_DIR:-$TMPDIR}/local-merge"
[ -d "$MERGE_DIR" ] && rm -rf "$MERGE_DIR"
git clone --depth "$DEPTH" --branch "$TARGET" "$(git remote get-url origin)" "$MERGE_DIR"

git -C "$MERGE_DIR" fetch origin "$BRANCH"
git -C "$MERGE_DIR" merge FETCH_HEAD -m "$MESSAGE"
git -C "$MERGE_DIR" push
```

### 1c. Non-fast-forward recovery

```bash
git -C "$MERGE_DIR" pull --rebase
git -C "$MERGE_DIR" push
```

Max 3 retries. After 3 failures, stop and report. Do not force-push.

### 1d. Cleanup

Always runs after Phase 1, success or failure:

```bash
rm -rf "$MERGE_DIR" 2>/dev/null || true
```

If `rm -rf` is denied (sandbox, permission prompt), log it and move on — the temp dir is in `$TMPDIR` and will be cleaned by the OS. Do not block the merge on cleanup failure.

## Phase 2 — Propagate to Primary (reasoning required)

Bring the primary worktree's `$TARGET` up to date with the newly-pushed remote. Steps 2a-2c are mechanical. Step 2d requires agent judgment. Steps 2e-2g depend on that judgment.

### 2a. Guard: is primary on TARGET?

```bash
git -C "$PRIMARY" branch --show-current
```

**Not on `$TARGET`? Stop.** Report: "Primary is on `<branch>`, not `$TARGET`. Remote updated; local not forwarded." Done.

### 2b. Protect dirty state

```bash
git -C "$PRIMARY" status --porcelain
```

If output is non-empty, shelter uncommitted work. Use `add -u` (tracked files only) to avoid staging sensitive untracked files (.env, credentials):

```bash
git -C "$PRIMARY" add -u
git -C "$PRIMARY" commit -m "wip: preserve local state before remote sync"
```

Record `WIP_CREATED=true` for step 2g. If clean, skip.

### 2c. Fetch updated TARGET

```bash
git -C "$PRIMARY" fetch origin "$TARGET"
```

### 2d. Analyze divergence (agent reasoning)

Run all five commands, then assess using the decision matrix:

```bash
git -C "$PRIMARY" rev-list --count HEAD..origin/"$TARGET"    # commits behind
git -C "$PRIMARY" rev-list --count origin/"$TARGET"..HEAD     # commits ahead
git -C "$PRIMARY" diff HEAD..origin/"$TARGET" --stat          # changed files
git -C "$PRIMARY" log HEAD..origin/"$TARGET" --oneline        # incoming commits
git -C "$PRIMARY" log origin/"$TARGET"..HEAD --oneline        # local-only commits
```

| Behind | Ahead | Assessment | Action |
|--------|-------|------------|--------|
| N > 0 | 0 | Fast-forward | `--ff-only` (2e) |
| N > 0 | M > 0 | Diverged | Inspect diff for file overlap + semantic risk (2e) |
| 0 | 0 | Already current | Skip, report, done |
| 0 | M > 0 | Local-only commits | Unexpected — escalate to copilot (2f) |

Beyond textual conflicts, assess semantic risk: two agents editing related config in different files can silently break things even when git sees no conflict.

### 2e. Execute merge

**Fast-forward** (behind > 0, ahead = 0):

```bash
git -C "$PRIMARY" merge --ff-only origin/"$TARGET"
```

**Non-conflicting divergence** (different files, low semantic risk):

```bash
git -C "$PRIMARY" merge origin/"$TARGET" --no-edit
```

If merge produces conflicts, abort immediately:

```bash
git -C "$PRIMARY" merge --abort
```

Then escalate to copilot (2f).

**Uncertain or risky**: do not attempt merge. Go to 2f.

### 2f. Copilot escalation

1. Invoke `/copilot` to enter copilot mode
2. Present the analysis from 2d: behind/ahead counts, diff stat, commit logs
3. State what blocked automatic resolution
4. Let the user drive the merge
5. When resolved, invoke `/autonomous` to restore previous mode

### 2g. Restore WIP state

Only if `WIP_CREATED=true`:

```bash
git -C "$PRIMARY" reset --soft HEAD~1
```

Preserves all changes in the index and working tree exactly as they were before the skill ran.

## Safety Invariants

- **No force-push.** Non-fast-forward retries use `pull --rebase`, never `--force`.
- **No work lost.** Dirty state is WIP-committed before any merge, restored after.
- **No direct commits to main.** Phase 1 uses a disposable clone for multi-agent isolation regardless of target. Phase 2 only fast-forwards or merges from origin.
- **Conflict = stop.** Conflicts trigger `merge --abort` and copilot escalation, never auto-resolution.
- **Cleanup always runs.** The shallow clone is removed regardless of outcome.

## Integration

| Caller | Context |
|--------|---------|
| `/ship` | CI-down path after review approval |
| `/reflect` | Post-task consolidation to main |
| `/copilot` | Receives escalation from Phase 2f |
| `/autonomous` | Restored after copilot resolves conflict |
