---
name: dedup
description: "Dedupe-only pass for BASE_SHA..HEAD: remove duplicate code introduced by the diff or reuse existing shared utils; applies changes + commits."
---

# Dedup Loop (dedupe-only)

Input: a git base SHA/ref to dedupe against.
Default/recommended is `auto`, which resolves a branch-wide merge-base from integration/default refs first, then falls back to upstream (`@{u}`).

## Preconditions

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Ensure you have a branch-wide base commit SHA (the fork-point/common-ancestor with the integration branch).
- Start from a clean working tree (required):
  - `git status --porcelain` should be empty.
- Ensure git can create commits (stop if missing):
  - If commits fail due to missing identity, configure `user.name` and `user.email`.
- Ensure both CLIs are available (`codex` and `claude`) because reviewer/responder must be different vendors.

## Scope / intent

- This is **NOT** a general code review.
- Only act on:
  - duplicate code introduced/expanded by `BASE_SHA..HEAD`, and/or
  - code introduced by `BASE_SHA..HEAD` that reimplements an existing shared util already in the repo.
- Do not apply unrelated fixes (style, perf, security, naming, error handling) unless strictly required to complete a dedupe/reuse change safely.

## Expected runtime

Typically runs 10–30 minutes, but allow at least 60 minutes.

Do **not** interrupt/restart the subagent if it looks stuck. The loop script owns stuck/timeout handling and will exit on its own when it completes or when `--timeout` is reached. Prefer watching the periodic heartbeat output (`--heartbeat-seconds`) instead of tailing logs.

## Why Claude sometimes looked “stuck”

Claude Code print mode can be silent in `--output-format text` until it finishes (including during tool work). This repo defaults Claude subprocesses to `--output-format stream-json --include-partial-messages` so the wrapper sees measurable progress and inactivity timeouts mainly trigger on true hangs.

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

DEDUP_SKILL_DIR="$(resolve_skill_dir dedup)"
python3 "$DEDUP_SKILL_DIR/scripts/run_dedup_loop.py" auto
```

Explicit branch-base example (if you want to pin it yourself):

```bash
INTEGRATION_REF="$(
  git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null \
    || { git show-ref --verify --quiet refs/remotes/origin/main && echo origin/main; } \
    || { git show-ref --verify --quiet refs/remotes/origin/master && echo origin/master; } \
    || echo "@{u}"
)"
BASE_SHA="$(git merge-base --fork-point "$INTEGRATION_REF" HEAD 2>/dev/null || git merge-base "$INTEGRATION_REF" HEAD)"
python3 "$DEDUP_SKILL_DIR/scripts/run_dedup_loop.py" "$BASE_SHA"
```

Options:
- `--max-iterations N` (default: 1)
- `--cli codex|claude` (pin responder provider; reviewer is selected from provider pool and always differs from responder)
- `--provider-pool codex,claude` (provider pool for both subprocesses; reviewer/responder vendors are always distinct)
- `--codex-model-pool ...` and `--claude-model-pool ...` (supports `model@effort`)
- `--progress-log <path>` and `--heartbeat-seconds N`
- `--artifacts-dir <path>` (optional; stores reviewer outputs for responders to read)
- `--timeout N` (per-subprocess timeout in seconds; default: 3600)
- `--review-only` (responder does not apply fixes/commit)
- `--scope <pathspec>` (repeatable; restricts `git diff` to those paths)

Claude automation knobs (env vars; defaults shown):
- `PROMPT_TEMPLATES_CLAUDE_OUTPUT_FORMAT=stream-json` (`text|json|stream-json`)
- `PROMPT_TEMPLATES_CLAUDE_MIN_VERSION=2.1.33` (fail fast if installed Claude Code is older)
- `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES=10485760` (per invocation; set `0` for unlimited)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_TIMEOUT_SECONDS=180` (set `0` to disable; in `text/json` mode it is disabled unless explicitly set)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_MIN_RUNTIME_SECONDS=30`
- `PROMPT_TEMPLATES_CLAUDE_PROMPT_BUDGET_BYTES=0` (disabled by default; set >0 to enforce)

Behavior:
- Each iteration runs in two fresh subprocesses:
  - Reviewer subprocess: generates **dedupe-only** findings from `BASE_SHA..HEAD` (it fetches the diff locally via `git diff`).
  - Responder subprocess: agrees/rejects each finding; applies only agreed dedupe/reuse fixes; runs obvious checks; commits (it fetches the diff locally via `git diff` and reads reviewer output from the artifacts dir).
- The script enforces that reviewer and responder always run on different vendors (codex vs claude).
- Claude subprocesses run in a native PTY (when available) and have an inactivity timeout; on classifiable Claude automation failures the script retries once.
- If `reviewer=claude` fails after retry and responder is not pinned to `codex`, the script performs a role-swap fallback and re-runs the iteration with `reviewer=codex,responder=claude` (it prints a `CLAUDE_FALLBACK: ...` line when this happens).
- When the responder subprocess runs on Codex, it is invoked with `--sandbox danger-full-access` and `-a never` so it can run git commands (including committing fixes) without getting stuck on approvals or `.git` lock writes.
- In non-`--review-only` mode, the script enforces commit hygiene per iteration: if responder leaves working-tree changes, it auto-commits them before the next iteration; if responder accepts findings but produces no committed changes, the loop stops.

Troubleshooting:
- `--progress-log` may include full tool outputs (diffs, file contents). Treat it as sensitive; stream-json logs are truncated by default via `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES`.
