---
name: agentteams
description: Orchestrate plan execution — analyze a plan tree, score it against expectations, resolve a dependency DAG, slice work into token-budgeted groups, and drive a human-in-the-loop iteration loop with canonical handoff blocks. Use to orchestrate agent teams, run plan analysis, render scoreboards, build punch lists (P0/P1/P2), slice plans by token budget, drive iteration loops, render handoff blocks (Landed / Tested / Acceptance / Next / To Resume), and resume after /clear.
tier: org
dependencies:
  - agent-skills-toolkit
---

# AgentTeams — Orchestrator Skill

## Purpose

Drive a plan from "tree of markdown" to "shipped feature" without losing state across context resets. The skill is a thin contract over six executable subcommands.

## CLI surface

```
agentteams analyze <plan-dir>                    # five-doc bundle: README, fit-matrix, analysis, gaps, schema-deltas, state-flow
agentteams dag     <plan-dir>                    # topo-sorted JSON DAG + cycle report + P0/P1/P2 priorities
agentteams slice   <plan-dir> --budget <P>       # write .ai-harness/groups/NN-<slug>.md per group
agentteams run     <plan-dir> [--group N]        # execute one group; emit handoff block; exit 7 on HITL hard pause
agentteams report  <plan-dir>                    # print the most-recently-emitted handoff block
agentteams resume  <plan-dir>                    # print the exact prompt to paste after /clear
```

## Runtime selection — mjs vs py

The skill ships two parity-tested implementations:

- **`scripts/mjs/`** — Node ESM (primary; broader ecosystem, faster cold start).
- **`scripts/py/`** — Python twin (uv-managed; parity-tested byte-equal JSON).

A single entry point — **`scripts/bin/agentteams`** — picks between them at invocation time:

| `AGENTTEAMS_RUNTIME` | Behavior |
| --- | --- |
| unset / `auto` (default) | Prefer `mjs` if `node` is on `$PATH`; otherwise fall back to `py` via `uv`. |
| `mjs` | Force the Node runtime. Exits 127 if `node` is missing. |
| `py` | Force the Python runtime. Exits 127 if `uv` is missing. |

The Makefile, the install alias (below), and the Claude Code agent wrapper all invoke the shim — none of them hardcodes `node` or `uv`, so swapping runtimes is one env-var flip.

## Install (`agentteams` on $PATH)

The runtime-selecting shim is at `scripts/bin/agentteams` and is not auto-installed globally. Add a shell alias keyed off an env var so the path stays portable across machines:

```sh
# In ~/.zshrc (or ~/.bashrc):
export AGENTTEAMS_HOME="${HOME}/<path-to-this-checkout>"   # adjust per-machine
alias agentteams='"$AGENTTEAMS_HOME/.agents/skills/agentteams/scripts/bin/agentteams"'

# Optional: pin to one runtime
# export AGENTTEAMS_RUNTIME=mjs   # or: py
```

Then `agentteams analyze <plan-dir>` resolves from any working directory and auto-picks mjs/py based on what's installed.

Alternative install paths (all relative to the repo root):

| Method | Command | Notes |
| --- | --- | --- |
| Shell alias (above) | edit `~/.zshrc` | Lightest touch; survives code edits without reinstall. |
| `npm link` (mjs only) | `cd .agents/skills/agentteams/scripts/mjs && npm link` | Symlinks `agentteams-mjs` into the npm global bin, bypassing the shim. Reverse with `npm unlink -g agentteams-mjs`. |
| `uv tool install` (py only) | `uv tool install -e .agents/skills/agentteams/scripts/py` | Installs the py CLI to `~/.local/bin`, bypassing the shim. Reverse with `uv tool uninstall agentteams`. |
| No install | `.agents/skills/agentteams/scripts/bin/agentteams …` | Always works from the repo root; root `Makefile` wraps the common verbs. |

## HITL modes

- `hard` (default, **recommended**) — emit handoff, exit 7. Forces a `/clear` between groups.
- `soft` — emit handoff, then prompt for stdin confirmation before continuing.
- `phase-only` — exit 7 only when the current group ends a phase boundary.

## Budget profiles

| Profile        | Max tokens | Features/group |
| -------------- | ---------: | -------------: |
| conservative   |   ~120,000 |            1–3 |
| comfortable    |   ~180,000 |            2–4 |
| aggressive     |   ~250,000 |            3–5 |

Default: **conservative** (the safest mode against context exhaustion).

## Exit-code matrix

| Code | Meaning |
| ---: | --- |
| 0   | success |
| 1   | generic failure |
| 2   | misuse (bad flag / arg) |
| 3   | plan-not-found |
| 4   | parse-error |
| 5   | cycle-detected |
| 6   | budget-exceeded |
| 7   | hitl-pause (intentional, clean) |
| 8   | gate-failed (testing or acceptance gate) |
| 100 | not-implemented (stub) |

## Canonical handoff block

```
GROUP N COMPLETE — <feature title summary>

Landed: - <feature-id>: <description> — tests <green|red>, <N> files
  • <path/to/file> (new|extended: <what>)

Tests: <pass/total> green. <bullets describing test coverage>

Acceptance: <PASS|FAIL|no gate in this group (gate lands in Group M)>

Next: GROUP <N+1> — <next group title>

To resume: 1) Run /clear to drop this session's context. 2) Paste this prompt:

       implement group <N+1> of <plan-path> per <session-plan-path>
```

## State persistence

`state.json` lives at `<plan-dir>/.ai-harness/state.json`:

```json
{
  "schemaVersion": 1,
  "currentGroup": 2,
  "lastCompletedGroup": 1,
  "hitlMode": "hard",
  "budgetProfile": "conservative",
  "testingMode": "tests+gate",
  "phaseAcceptanceGates": { "phase-1": { "status": "PASS", "timestamp": "..." } }
}
```

Writes are atomic (tmp + rename). `resume` reads this file to pick the next group.

## When to use

- The user names a plan tree under `features/`, `stories/`, `tasks/` and asks to "orchestrate", "drive iteration", "slice by token budget", or "emit handoff".
- The user wants a multi-document plan scoreboard (fit matrix + analysis + punch list).
- The user wants to resume after `/clear` without losing state.

## Skip when

- The plan does not yet exist — use the upstream `plan-feature-story-task` skill to author it first.
- The work is API-package scaffolding rather than execution — use `implement-polyglot-project-plan` instead.

## Project-local overrides

Model id, HITL defaults, and budget profile override live in a sibling `agentteams-config` skill at the consuming project's `.agents/skills/agentteams-config/`. This skill is read-only of those settings; it never authors them.
