---
name: relay-dispatch
argument-hint: "<repo-path> (-b <branch> | --run-id <id>) -p <prompt> [options]"
description: Dispatch implementation tasks via worktree isolation. Use when delegating work to an executor, running background dispatches, or parallelizing independent tasks.
compatibility: Requires executor CLI (e.g., codex), git, and Node.js 18+.
metadata:
  related-skills: "relay, relay-plan, relay-review, relay-merge"
---

# Relay Dispatch

Create a worktree and dispatch a task to an executor.

## Usage

```bash
# Foreground (blocking — simple tasks, default executor: codex)
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . -b feature-auth -p "..."

# Same-run resume after a changes-requested review
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . --run-id issue-42-20260403120000000 --prompt-file review-round-2-redispatch.md

# With explicit executor
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . -e codex -b feature-auth -p "..."

# Claude Code as executor (no Codex required)
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . -e claude -b feature-auth -p "..."
```

For background and parallel dispatch, see "Background & Parallel" section below.

## Options

| Flag | Description |
|---|---|
| `--branch, -b` | Branch name (required) |
| `--run-id` | Resume an existing retained relay run |
| `--manifest` | Resume an existing retained relay run by manifest path |
| `--prompt, -p` | Task prompt (include Context + Done Criteria + self-review) |
| `--prompt-file` | Read prompt from file (for large prompts) |
| `--executor, -e` | Executor: `codex` (default), `claude` |
| `--model, -m` | Model override |
| `--sandbox` | `workspace-write` (default) or `read-only` |
| `--copy <files>` | Additional files to copy |
| `--timeout` | Timeout in seconds (default: 1800) |
| `--register` | Register session in executor's app (keeps worktree) |
| `--no-cleanup` | Compatibility alias; worktree is retained by default |
| `--dry-run` | Show plan without executing |
| `--json` | Structured JSON output (for background dispatch) |

Creates worktree → writes a relay run manifest → runs executor → collects result.
Exits with non-zero code on failure.

Each dispatch writes a manifest to `~/.relay/runs/<repo-slug>/<run-id>.md` and appends lifecycle evidence to `~/.relay/runs/<repo-slug>/<run-id>/events.jsonl`. `run_id` is the canonical identity for re-dispatch, review, merge, close, and reporting.

### Timeout guidance

| Task type | Timeout | Rationale |
|---|---|---|
| Simple implementation | `1800` (default) | No self-review needed |
| With self-review loop | `3600` | Executor iterates 2-3 times |
| Complex / multi-file | `5400` | Deep implementation + thorough self-review |

## Verify Success

After dispatch completes, confirm before proceeding to review:

```bash
# JSON output: status, runId, manifestPath, runState, cleanupPolicy
# "completed" + "review_pending" → proceed to relay-review
# "completed-with-warning" + "review_pending" → inspect uncommitted work, then review
# "failed" + "escalated" → inspect error, fix or re-dispatch
gh pr list --head <branch> --json number,url,title
```

Successful dispatches retain the worktree by default. Use the returned `runId`, manifest, and worktree to continue review. Resume only from `changes_requested`; dispatch reuses the same run and worktree.

On re-dispatch, previous Score Log + reviewer feedback are auto-prepended to the prompt. Record attempt data via `captureAttempt()` before transitioning to `changes_requested`. Storage: `~/.relay/runs/<slug>/<run-id>/previous-attempts.json`.

### Handling Failures

| Failure | Action |
|---|---|
| Timeout (with commits) | `completed-with-warning` — check worktree for uncommitted changes, proceed to review |
| Timeout (no commits) | Increase `--timeout` or split task into smaller pieces |
| Executor error / no commits | Read result file; revise prompt and re-dispatch |
| No PR created | Check `git log` in worktree; push manually or re-dispatch |
| Branch conflicts | Resolve in worktree or create fresh worktree from updated main |
| Network/transient error | Wait 30s, retry once. If it fails again, escalate to user |

## Background & Parallel

### Background dispatch

Run dispatch asynchronously so the orchestrator can continue other work (planning, reviewing, user interaction) while the executor runs.

> **Platform examples — async dispatch:**
> Claude Code: `Bash(run_in_background=true)` | Codex: shell `&` or platform async | Other: any non-blocking execution

```bash
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . -b task-42 --prompt-file tasks/42.md --json --timeout 3600
# Run this command in the background using your platform's async mechanism
# When executor finishes → proceed to relay-review
```

### Parallel dispatch (independent tasks)

Launch multiple independent dispatches concurrently:

```bash
# Each dispatch runs independently in the background
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . -b task-42 --prompt-file tasks/42.md --json &
${CLAUDE_SKILL_DIR}/scripts/dispatch.js . -b task-43 --prompt-file tasks/43.md --json &
# Each completes independently → review each PR via relay-review
```

## `create-worktree.js` — Standalone worktree creation

Create a worktree without dispatching, or register an existing worktree in Codex App:

```bash
# Create worktree in ~/.relay/worktrees/
${CLAUDE_SKILL_DIR}/scripts/create-worktree.js <repo> -b <branch>

# Register an existing worktree in Codex App (optional)
${CLAUDE_SKILL_DIR}/scripts/create-worktree.js <repo> --worktree-path <path> -b <branch> -t "Title" --register
```

## Worktree Cleanup

Successful dispatches keep their worktree by default. Cleanup moves later in the lifecycle, typically after review or merge.

`--no-cleanup` remains accepted as a compatibility alias. `--register` still matters because it also opens the retained worktree in the executor app.

To prune stale retained worktrees safely from this repo:
```bash
${CLAUDE_SKILL_DIR}/scripts/cleanup-worktrees.js --repo .              # clean terminal runs > 24h old
${CLAUDE_SKILL_DIR}/scripts/cleanup-worktrees.js --repo . --all         # ignore age threshold
${CLAUDE_SKILL_DIR}/scripts/cleanup-worktrees.js --repo . --dry-run     # show what would be removed
${CLAUDE_SKILL_DIR}/scripts/close-run.js --repo . --run-id <run-id> --reason "stale_non_terminal_run"
${CLAUDE_SKILL_DIR}/scripts/reliability-report.js --repo . --json
```

## Caveats

- **Timeout**: Use `--timeout 3600`+ when self-review is included
- **App restart** (Codex-specific): Codex App needs restart to show new worktree threads
- **Exit codes**: dispatch.js exits non-zero on failure — check before proceeding to review
- **Parallel merges**: If parallel PRs touch the same files, merge one at a time and rebase the other
