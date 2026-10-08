---
name: plan-write
description: "Write a detailed, self-contained implementation plan to a new Markdown file under plan/. Use when you already have a sketch/requirements and want a plan doc before coding."
---

# Write Plan Doc

## Preconditions

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Do not start implementation in this skill; only write/update the plan document.
- Plan critique is a separate step (use `plan-critique-loop`); `plan-write` does not run critique internally.

## Expected runtime

Typically runs 15–45 minutes. Callers should allow the full `--timeout` (default 3600s) before interrupting.

If you use `--progress-log`, do **not** `tail -f` it into the main context unless you must debug; prefer checking progress via log line counts (for example: `wc -l <progress-log>`) and/or the heartbeat counters.

## Workflow — Option A (external script, preferred)

Run the plan-write as a standalone CLI invocation:

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

PLAN_WRITE_SKILL_DIR="$(resolve_skill_dir plan-write)"
python3 "$PLAN_WRITE_SKILL_DIR/scripts/run_plan_write.py" sketch/<generated-name>.md
```

Flags:
- `--cli codex|claude` — override auto-detected CLI
- `--model MODEL` — pass a specific model to the CLI
- `--reasoning-effort LEVEL` — pass explicit reasoning effort (`vhigh` aliases to `xhigh`)
- `--timeout N` — CLI invocation timeout in seconds (default: 3600)
- `--progress-log PATH` — optional path to append streamed subagent output
- `--heartbeat-seconds N` — heartbeat cadence in seconds (0 disables)

Default behavior:
- When using Codex and no overrides are provided, the script uses `--model gpt-5.2` with `high` reasoning effort.
- When using Codex, the script always runs with `--sandbox danger-full-access`, `-a never`, and `--search` so it can do bounded official-doc research when “latest” matters.

The first positional argument can be a sketch file path (for example under `sketch/`) or raw sketch text.
The script prints the created plan doc path to stdout on success.

## Workflow — Option B (inline, legacy)

1. Open `references/prompts/plan-output.md`.
2. Provide your sketch/notes/requirements as `$ARGUMENTS`.
3. Ensure the prompt writes a **new** file under `plan/` (kebab-case; do not overwrite).
4. In your response, clearly state the final path you wrote (for example: `plan/<generated-name>.md`).
