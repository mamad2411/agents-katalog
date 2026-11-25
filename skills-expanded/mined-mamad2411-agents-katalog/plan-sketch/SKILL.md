---
name: plan-sketch
description: "Do bounded research (official docs first) and produce a high-level implementation sketch in `sketch/<generated-name>.md`. Use when you want an approach and step ordering before implementation."
---

# Plan Sketch

## Preconditions

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Confirm whether web browsing is allowed.
  - If browsing is blocked by sandbox/approvals, ask the user to enable/approve it.
  - If the user says "no web browsing", proceed but clearly label assumptions where "latest" matters.

## Output contract (required)

`plan-sketch` must produce:

1. A sketch markdown file (usually under `sketch/`, or an explicit `--output` path if provided).
2. A small, parseable **Questions for user** block in the subagent's stdout output so wrapper skills can ask the user without reading the sketch content into context.
3. A machine-readable JSON Questions block in stdout so wrapper skills can parse choices programmatically.

The Questions block must cover:
- Any **open questions / unknowns** that change the plan materially.
- Any **assumptions** that should be confirmed.
- Any **high-level approach forks** (architecture, APIs, rollout/testing strategy, migrations).
- If there are multiple viable implementation approaches, include an explicit **choose an approach** question so the user picks one before planning.

Format requirements (strict):

- Do not print the sketch content in the response.
- Print the sketch path (single line) and then print a Questions block bracketed by markers:
  - `BEGIN_USER_QUESTIONS`
  - `END_USER_QUESTIONS`
- In the Questions block:
  - Start with a short instruction telling the user to answer in one batch by label/number.
  - Present all decision-steering questions at once.
  - Number questions as `1)`, `2)`, ... (not bullets).
  - For each question, include 2–4 mutually exclusive options.
  - Label options as `1a)`, `1b)`, `1c)` ... (letters per question), and make the labels easy to copy/paste.
  - Put the recommended option first and include a 1-sentence rationale on the same line.
  - End the block with a single-line summary of recommended picks in the format:
    - `Recommended picks (copy/paste): 1a, 2b, 3a`
  - If there are no meaningful open questions, include at least 1 explicit confirmation question with options.
- After the text Questions block, print a JSON Questions block bracketed by markers:
  - `BEGIN_USER_QUESTIONS_JSON`
  - `END_USER_QUESTIONS_JSON`
- The JSON block must be valid JSON and include:
  - `questions`: array of objects with `id` (number or string) and `options`.
  - Each `options` entry includes `label` (e.g., `1a`) and `text`.
  - Optional: `recommended` boolean on options and `recommended_picks` array at the top level.

## Expected runtime

Typically runs 15–45 minutes. Callers should allow the full `--timeout` (default 3600s) before interrupting.

If you use `--progress-log`, do **not** `tail -f` it into the main context unless you must debug; prefer checking progress via log line counts (for example: `wc -l <progress-log>`) and/or the heartbeat counters.

## Workflow — Option A (external script, preferred)

Run the sketch as a standalone CLI invocation:

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

PLAN_SKETCH_SKILL_DIR="$(resolve_skill_dir plan-sketch)"
python3 "$PLAN_SKETCH_SKILL_DIR/scripts/run_plan_sketch.py" "user's rough idea"
```

Flags:
- `--idea-file PATH` — use a file as the idea input (useful for large/multiline inputs)
- `--output PATH` — optional explicit sketch output path (default: model generates `sketch/<meaningful-name>.md`)
- `--cli codex|claude` — override auto-detected CLI
- `--model MODEL` — pass a specific model to the CLI
- `--reasoning-effort LEVEL` — pass explicit reasoning effort (`vhigh` aliases to `xhigh`)
- `--timeout N` — CLI invocation timeout in seconds (default: 3600)
- `--progress-log PATH` — optional path to append streamed subagent output
- `--heartbeat-seconds N` — heartbeat cadence in seconds (0 disables)

Default behavior:
- When using Codex and no overrides are provided, the script uses `--model gpt-5.2` with `xhigh` reasoning effort.
- When using Codex, the script always runs with `--sandbox danger-full-access` and `-a never`.
- When using Codex, the script enables live web search (`--search`) so it can do bounded research for unstable facts.
- When using Claude, the script runs non-interactive with `--dangerously-skip-permissions`.

The script prints the output file path to stdout on success.

## Workflow — Option B (inline, legacy)

1. Open `references/prompts/plan-sketch.md`.
2. Execute it using the user's rough idea as `$ARGUMENTS`.
3. Do **bounded** web research (official docs first) for unstable facts:
   - Current CLI/tooling behavior, deprecations, APIs, pricing, supported flags, version constraints.
   - Avoid searching any secrets/PII/proprietary code. Use generic queries (vendor + product + version + error message class).
4. Write a **new** sketch file under `sketch/` with a meaningful kebab-case filename and report the final path.
