---
name: code-review-loop
description: "Iterative review+fix loop for BASE_SHA..HEAD: generate findings, apply accepted fixes, run checks, commit, and re-review up to 3 iterations or until clean."
---

# Code Review Loop (up to 3 iterations)

Input: a git base SHA (or other explicit range) to review against (for example: `<sha>` or `HEAD~1`).

## Preconditions

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Ensure you have a base commit SHA (prefer the commit from before the change set).
  - If none was provided and you cannot choose confidently, ask the user for the correct base SHA.
- Start from a clean working tree (recommended):
  - `git status --porcelain` should be empty.
  - If it’s not empty, either commit/stash first or ask the user what to do (don’t mix unrelated changes into review fixes).
- Ensure both CLIs are available (`codex` and `claude`) because reviewer/responder must be different vendors.

## Expected runtime

Typically runs 15–45 minutes, but allow at least 120 minutes.

Do **not** interrupt/restart the subagent if it looks stuck. The loop script owns stuck/timeout handling and will exit on its own when it completes or when `--timeout` is reached. Prefer watching the periodic heartbeat output (`--heartbeat-seconds`) instead of tailing logs.

## Why Claude sometimes looked “stuck”

Claude Code print mode can be silent in `--output-format text` until it finishes (including during tool work). This repo defaults Claude subprocesses to `--output-format stream-json --include-partial-messages` so the wrapper sees measurable progress and inactivity timeouts mainly trigger on true hangs.

## Loop

Run the review loop script:

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

CODE_REVIEW_LOOP_SKILL_DIR="$(resolve_skill_dir code-review-loop)"
python3 "$CODE_REVIEW_LOOP_SKILL_DIR/scripts/run_review_loop.py" <base-sha>
```

Options:
- `--max-iterations N` (default: 3)
- `--cli codex|claude` (pin responder provider; reviewer is selected from provider pool and always differs from responder)
- `--provider-pool codex,claude` (provider pool for both subprocesses; reviewer/responder vendors are always distinct)
- `--codex-model-pool ...` and `--claude-model-pool ...` (random model selection; supports `model@effort`)
- `--progress-log <path>` and `--heartbeat-seconds N`
- `--artifacts-dir <path>` (optional; stores reviewer outputs for responders to read)
- `--timeout N` (per-subprocess timeout in seconds; default: 7200)
- `--review-only` (responder does not apply fixes/commit)

Claude automation knobs (env vars; defaults shown):
- `PROMPT_TEMPLATES_CLAUDE_OUTPUT_FORMAT=stream-json` (`text|json|stream-json`)
- `PROMPT_TEMPLATES_CLAUDE_MIN_VERSION=2.1.33` (fail fast if installed Claude Code is older)
- `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES=10485760` (per invocation; set `0` for unlimited)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_TIMEOUT_SECONDS=180` (set `0` to disable; in `text/json` mode it is disabled unless explicitly set)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_MIN_RUNTIME_SECONDS=30`
- `PROMPT_TEMPLATES_CLAUDE_PROMPT_BUDGET_BYTES=0` (disabled by default; set >0 to enforce)

Behavior:
- Each iteration runs in two fresh subprocesses:
  - Reviewer subprocess: selected from the provider pool and generates review findings from `BASE_SHA..HEAD` (it fetches the diff locally via `git diff`).
  - Responder subprocess: agrees/rejects findings and applies only agreed fixes (it fetches the diff locally via `git diff` and reads reviewer output from the artifacts dir).
- The script enforces that reviewer and responder always run on different vendors (codex vs claude).
- Claude subprocesses run in a native PTY (when available) to avoid non-termination/hang modes that require a TTY.
- Claude subprocesses have an inactivity timeout; on classifiable Claude automation failures the script retries once.
- If `reviewer=claude` fails after retry and responder is not pinned to `codex`, the script performs a role-swap fallback and re-runs the iteration with `reviewer=codex,responder=claude` (it prints a `CLAUDE_FALLBACK: ...` line when this happens).
- Reviewer subprocesses stop early once a valid reviewer JSON object has been emitted (Codex) or once Claude emits a terminal `type=result` event (stream-json).
- When the responder subprocess runs on Codex, it is invoked with `--sandbox danger-full-access` and `-a never` so it can run git commands (including committing fixes) without getting stuck on approvals or `.git` lock writes.
- In non-`--review-only` mode, the script enforces commit hygiene per iteration: if responder leaves working-tree fix changes, it auto-commits them before the next iteration; if responder accepts findings but produces no committed changes, the loop stops.
- The script stops early when reviewer reports no findings, or when the responder agrees with none of the feedback.
- After completion, it emits a required `REVIEW_PROGRESS` log summary including:
  - total iterations completed;
  - which iteration (if any) terminated early due to no feedback or no agreement.
- Default model pools:
  - Codex: `gpt-5.2@high`
  - Claude: `claude-opus-4-6[1m]@high`

Troubleshooting:
- Look for `CLAUDE_RETRY:` / `CLAUDE_FALLBACK:` lines on stderr to confirm retry/fallback behavior.
- Heartbeats include `idle_seconds=...` and byte counters; PTY mode uses `pty_bytes=...`.
- `--progress-log` may include full tool outputs (diffs, file contents). Treat it as sensitive; stream-json logs are truncated by default via `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES`.
- If you see `CLAUDE_FALLBACK_UNAVAILABLE: ... responder is pinned to codex`, rerun with `--cli claude` to allow the role-swap fallback.
