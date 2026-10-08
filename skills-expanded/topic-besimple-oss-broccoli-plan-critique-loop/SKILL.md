---
name: plan-critique-loop
description: "Critique and revise an existing plan doc up to 3 iterations, using accept/reject triage and stopping early when no important feedback remains. Use when refining a plan/*.md before implementation."
---

# Plan Critique Loop (up to 3 iterations)

Input: an existing plan doc path (for example: `plan/my-feature.md`).

## Preconditions

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Confirm the plan doc exists: `test -f <plan-doc-path>`
- Ensure git can create commits before running the loop (`user.name`/`user.email` configured).
- Do not start implementation in this skill; only critique and revise the plan.
- Ensure both CLIs are available (`codex` and `claude`) because critic/responder must be different vendors.

## Expected runtime

Typically runs 15–45 minutes, but allow at least 120 minutes.

Do **not** interrupt/restart the subagent if it looks stuck. The loop script owns stuck/timeout handling and will exit on its own when it completes or when `--timeout` is reached. Prefer watching the periodic heartbeat output (`--heartbeat-seconds`) instead of tailing logs.

If you use `--progress-log`, do **not** `tail -f` it into the main context unless you must debug; prefer checking progress via log line counts (for example: `wc -l <progress-log>`) and/or the heartbeat counters.

## Why Claude sometimes looked “stuck”

Claude Code print mode can be silent in `--output-format text` until it finishes (including during tool work). This repo defaults Claude subprocesses to `--output-format stream-json --include-partial-messages` so the wrapper sees measurable progress and inactivity timeouts mainly trigger on true hangs.

## Loop

Run the critique loop script:

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

PLAN_CRITIQUE_LOOP_SKILL_DIR="$(resolve_skill_dir plan-critique-loop)"
python3 "$PLAN_CRITIQUE_LOOP_SKILL_DIR/scripts/run_critique_loop.py" <plan-doc-path>
```

Options:
- `--max-iterations N` (default: 3)
- `--cli codex|claude` (pin responder provider; critic is selected from provider pool and always differs from responder)
- `--provider-pool codex,claude` (provider pool for both subprocesses; critic/responder vendors are always distinct)
- `--codex-model-pool ...` and `--claude-model-pool ...` (random model selection; supports `model@effort`)
- `--progress-log <path>` and `--heartbeat-seconds N`
- `--artifacts-dir <path>` (optional; stores critic outputs for responders to read)
- `--timeout N` (per-subprocess timeout in seconds; default: 7200)

Claude automation knobs (env vars; defaults shown):
- `PROMPT_TEMPLATES_CLAUDE_OUTPUT_FORMAT=stream-json` (`text|json|stream-json`)
- `PROMPT_TEMPLATES_CLAUDE_MIN_VERSION=2.1.33` (fail fast if installed Claude Code is older)
- `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES=10485760` (per invocation; set `0` for unlimited)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_TIMEOUT_SECONDS=180` (set `0` to disable; in `text/json` mode it is disabled unless explicitly set)
- `PROMPT_TEMPLATES_CLAUDE_INACTIVITY_MIN_RUNTIME_SECONDS=30`
- `PROMPT_TEMPLATES_CLAUDE_PROMPT_BUDGET_BYTES=0` (disabled by default; set >0 to enforce)

Behavior:
- Each iteration runs in two fresh subprocesses:
  - Critic subprocess: selected from the provider pool and generates critique feedback (it reads the plan doc from disk).
  - Responder subprocess: triages critic feedback (agree/reject) and applies only agreed edits using the selected responder provider/model (it reads the plan doc from disk and reads critic output from the artifacts dir).
- The script enforces that critic and responder always run on different vendors (codex vs claude).
- Any subprocess that runs on Codex is invoked with `--sandbox danger-full-access`, `-a never`, and `--search`.
- Claude subprocesses run in non-interactive mode with `--dangerously-skip-permissions`, in a native PTY (when available), and have an inactivity timeout.
- On classifiable Claude automation failures the script retries once. If `critic=claude` fails after retry and responder is not pinned to `codex`, it performs a role-swap fallback and re-runs the iteration with `critic=codex,responder=claude`.
- After each iteration, the script stages and commits plan-file edits (if any) before starting the next iteration.
- The script stops early when responder reports no actionable feedback.
- No manual accept/reject input is required for the loop to revise the plan.
- After completion, it appends a deterministic changelog block to the plan doc recording:
  - total iterations executed;
  - which iteration (if any) stopped due to no feedback.
- Default model pools:
  - Codex: `gpt-5.2@high`
  - Claude: `claude-opus-4-6[1m]@high`

Troubleshooting:
- `--progress-log` may include full tool outputs (plan contents, file contents). Treat it as sensitive; stream-json logs are truncated by default via `PROMPT_TEMPLATES_CLAUDE_STREAM_LOG_MAX_BYTES`.
