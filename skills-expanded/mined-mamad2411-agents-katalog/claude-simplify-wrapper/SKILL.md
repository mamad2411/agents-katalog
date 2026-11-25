---
name: claude-simplify-wrapper
description: "Run Claude's built-in /simplify skill on BASE_SHA..HEAD, validate checks, and commit."
---

# Simplify Loop

Input: a git base SHA/ref to simplify against (for example: `<sha>` or `HEAD~1`).

## Preconditions

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Ensure you have a base commit SHA (prefer the commit from before the change set).
- Start from a clean working tree (required):
  - `git status --porcelain` should be empty.
- Ensure git can create commits (stop if missing):
  - If commits fail due to missing identity, configure `user.name` and `user.email`.
- Only `claude` CLI is required (no codex dependency).

## Scope / intent

- This is a **simplification pass**, not a general code review.
- Invokes Claude's built-in `/simplify` skill which runs three parallel agents internally:
  - Code reuse (find and eliminate duplication)
  - Code quality (simplify convoluted logic)
  - Code efficiency (remove unnecessary work)
- Changes are validated (build/lint/test) and committed automatically.

## Architecture

Two-phase per iteration:

1. **Simplify subprocess** — Invokes `claude` with the `/simplify` prompt. The built-in skill handles its own three parallel agents and applies fixes directly to the working tree.
2. **Validate+commit subprocess** — A second `claude` subprocess that runs the repo's standard build/lint/test commands, fixes only breakages introduced by the simplify phase, stages and commits all changes, and emits `LOOP_STATUS: {...}` so the wrapper can decide whether to continue.

The loop stops when:
- The simplify phase produces no working-tree changes (nothing to simplify)
- The validate phase fails to make checks green
- Max iterations reached

## Expected runtime

Typically runs 5–20 minutes per iteration. Allow at least 30 minutes for a single iteration.

Do **not** interrupt/restart the subagent if it looks stuck. The loop script owns stuck/timeout handling and will exit on its own when it completes or when `--timeout` is reached.

## Run

```bash
resolve_skill_dir() {
  local name="$1"
  local repo_root=""
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

  local candidates=(
    "$repo_root/.agents/skills/$name"
    "$repo_root/.claude/skills/$name"
    "$HOME/.agents/skills/$name"
    "$HOME/.codex/skills/$name"
    "$HOME/.claude/skills/$name"
  )

  for d in "${candidates[@]}"; do
    if [[ -d "$d" ]]; then
      echo "$d"
      return 0
    fi
  done

  echo "Error: skill '$name' not found in repo-scoped or user-scoped skill dirs." >&2
  return 1
}

SIMPLIFY_SKILL_DIR="$(resolve_skill_dir claude-simplify-wrapper)"
python3 "$SIMPLIFY_SKILL_DIR/scripts/run_simplify_loop.py" <base-sha>
```

Options:
- `--max-iterations N` (default: 1)
- `--model <model>` (default: `claude-sonnet-4-6`)
- `--effort <effort>` (default: `high`)
- `--progress-log <path>` and `--heartbeat-seconds N`
- `--artifacts-dir <path>` (optional; stores subprocess outputs)
- `--timeout N` (per-subprocess timeout in seconds; default: 3600)
- `--review-only` (run simplify phase only; do not validate or commit)
- `--scope <pathspec>` (repeatable; restricts `git diff` to those paths)

Claude automation knobs (env vars; defaults shown):
- `PROMPT_TEMPLATES_CLAUDE_OUTPUT_FORMAT=stream-json` (`text|json|stream-json`)
- `PROMPT_TEMPLATES_CLAUDE_MIN_VERSION=2.1.33` (fail fast if installed Claude Code is older)
- `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES=10485760` (per invocation; set `0` for unlimited)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_TIMEOUT_SECONDS=180` (set `0` to disable)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_MIN_RUNTIME_SECONDS=30`
- `PROMPT_TEMPLATES_CLAUDE_PROMPT_BUDGET_BYTES=0` (disabled by default; set >0 to enforce)

Behavior:
- Each iteration runs in two fresh Claude subprocesses (claude-only, no codex required).
- Phase 1 invokes the bundled `/simplify` skill which applies fixes directly.
- Phase 2 validates changes, fixes any breakages, and commits.
- Claude subprocesses run in a native PTY (when available) and have an inactivity timeout; on classifiable Claude automation failures the script retries once.
- The script enforces commit hygiene per iteration: if the validator leaves working-tree changes, it auto-commits them before the next iteration.

Troubleshooting:
- `--progress-log` may include full tool outputs (diffs, file contents). Treat it as sensitive; stream-json logs are truncated by default via `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES`.
