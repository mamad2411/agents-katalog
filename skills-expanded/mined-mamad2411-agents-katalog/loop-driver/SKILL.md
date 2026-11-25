---
name: loop-driver
description: |
  Run the outer loop of a loss-function-driven agentic
  cycle: read iteration log, write candidate artifact,
  install it for the agent, run design set, score, log
  iteration, apply forced entropy on stall, repeat.

  Load when a /goal prompt has been pasted into a session
  and the user says "run the loop", "start cycling",
  "drive the loss", or "iterate on the candidate". Also
  load when "the loop isn't converging" and the failure
  is in cycle selection (not the goal prompt or harness).

  The third of three LFD skills: meta-loss-function-
  development produces the /goal prompt, harness-scaffold
  produces the harness tree, this skill runs the cycles.

  Companion skills (install separately if not present):
  - meta-loss-function-development: produces the /goal prompt
  - harness-scaffold: scaffolds the project tree
  - loss-function-design: the 4-piece loss anatomy
  - harness-engineering: what the agent sees
  - cline-orchestration: the Cline runtime (substitute
    your own if not using Cline)
version: 1.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [loop, driver, loss-function-development, lfd, agentic, cycle, outer-loop]
    related_skills: [meta-loss-function-development, harness-scaffold, loss-function-design, harness-engineering, cline-orchestration]
---

# Loop Driver

The third skill in the LFD pipeline. The pipeline is:

1. `meta-loss-function-development` — produces a paste-able
   `/goal` prompt.
2. `harness-scaffold` — scaffolds the project tree from the
   `/goal` prompt.
3. **`loop-driver` (this skill)** — runs the cycles against
   the harness.

This skill is the **outer loop**. It does not write the
candidate artifact itself. It drives the *cycle*:

```
   ┌─────────────────────────────────────┐
   │ 1. Read iteration log               │
   │ 2. Form hypothesis (next change)    │
   │ 3. Write candidate artifact         │
   │ 4. Install artifact for agent       │
   │ 5. Run design set (verifiers)       │
   │ 6. Score (weighted sum + gates)     │
   │ 7. Append to iteration log          │
   │ 8. Update best-cycle if improved    │
   │ 9. Apply forced entropy on stall    │
   │ 10. Check stop conditions           │
   └──────────────┬──────────────────────┘
                  │ continue
                  ▼
   ┌─────────────────────────────────────┐
   │ 1. ...                              │
```

The candidate artifact is written by the **inner agent**
(Cline, Codex, Aider, …) — invoked via the wrapper script
the harness-scaffold generated. The loop driver is the
*driver*; the agent is the *worker*.

## How the user invokes this

The user has a scaffolded project (from `harness-scaffold`)
and wants the loop to run. They say:

> "Run the loop until pass_rate=1.0 or the budget is gone."

Or more specifically:

> "Drive 50 cycles. Stop on plateau or 8h. Apply forced
> entropy on every stall. Log every cycle."

The skill:

1. Confirms the harness is in place (`AGENTS.md`, `GOAL.md`,
   `verifiers/`, `test-tasks/`, `logs/`).
2. Reads the iteration log if it exists; otherwise starts at
   cycle 0 (baseline).
3. Establishes baseline: runs the design set with no
   candidate installed, records the result.
4. Begins cycle 1. For each cycle:
   - Reads the iteration log
   - Forms a hypothesis
   - Invokes the inner agent (via the wrapper) to write the
     candidate
   - Installs the candidate where the agent will pick it up
   - Runs the design set
   - Scores, logs, applies forced entropy if needed
   - Stops on a stop condition
5. Returns the best cycle's score and the iteration log.

The inner agent is whatever the harness was scaffolded for
(Cline by default; Codex, Aider if `--runtime` was passed).
The loop driver is **runtime-agnostic**: it just calls
`verifiers/<runtime>-wrapper.sh`.

## The cycle contract

Every cycle produces:

| Artifact | Path | Purpose |
|---|---|---|
| Cycle input | `logs/cycle-<N>-input.json` | What the loop saw going into the cycle (hypothesis, prior pass_rate, etc.) |
| Wrapper output | `logs/cycle-<N>/cycle-summary.json` | The wrapper's NDJSON summary of the inner agent run |
| Sub-losses | `logs/cycle-<N>/sub-losses.json` | The 7 sub-losses + weighted sum + gates |
| Iteration log entry | `logs/iteration-log.md` (append) | One-line entry: cycle, hypothesis, expected failure, pass_rate, weighted_sum, gates |
| Best-cycle score | `logs/best-cycle.json` | Updated if this cycle beat the prior best |

The loop driver is **idempotent on the iteration log**: it
appends, never overwrites. The user can grep
`logs/iteration-log.md` to see the descent trace.

## Forced entropy rules

The driver enforces the 4-piece loss spec's forced-entropy
section. Three rules, in order:

1. **Overfit reflection every cycle.** Before invoking the
   inner agent, the driver appends to `logs/iteration-log.md`:
   `cycle N: hypothesis="<one line>", expected_failure="<one line>", generalizing_or_memorizing=<g|m>, pass_rate=<float>`
   If `generalizing_or_memorizing=m`, the next change must
   REMOVE an eval-shaped artifact. The driver reads the
   agent's overfit-reflection and uses it to constrain the
   next cycle's prompt.

2. **Stall entropy.** If the last cycle's weighted sum did
   not improve by ≥ 0.05 over the prior cycle, the driver
   reads the last 5 entries of `logs/iteration-log.md` and
   prompts the agent: "Pick the OPPOSITE of your last
   change." The agent's response is appended to the log.

3. **Iteration log is required.** The driver never silently
   advances the cycle. Every cycle leaves a paper trail. If
   the agent's overfit-reflection is empty, the driver
   rejects the cycle and re-prompts.

## Stop conditions

The driver stops when ANY of:

1. `pass_rate == 1.0` for 2 consecutive cycles AND the last
   2 overfit-reflections say "generalizing" — submit best.
2. Wall-clock budget exhausted — submit best.
3. Token budget exhausted — submit best.
4. 3 consecutive cycles with no improvement AND forced
   entropy applied — submit best.

The driver emits a `STOP` event to `logs/iteration-log.md`
with the reason and the best cycle's score.

## The loop driver's runtime

The driver is **runtime-agnostic**. The runtime is determined
by the wrapper script in the harness:

- `verifiers/cline-wrapper.sh` → Cline
- `verifiers/codex-wrapper.sh` → Codex
- `verifiers/aider-wrapper.sh` → Aider

The driver calls `<wrapper> "<prompt>" --cwd <project_root>
--timeout <budget> --cycle cycle-<N>` and reads the JSON
output.

The driver does **not** care which LLM the inner agent uses.
The model is the inner agent's variable, not the driver's.

## When to load this skill

- The user has a scaffolded project (from `harness-scaffold`)
  and wants the loop to run.
- The user says "drive the cycle", "iterate on the skill",
  "run the loss", "start the loop", "kick off the cycle".
- The user wants to resume a previously-paused loop (read
  `logs/iteration-log.md` and pick up at the last cycle).
- The user is debugging "the loop isn't converging" and the
  failure is in cycle selection (not the goal prompt or the
  harness).

## When NOT to load this skill

- The user wants to write a /goal prompt — that's
  `meta-loss-function-development`.
- The user wants to scaffold a project — that's
  `harness-scaffold`.
- The user wants to debug the inner agent (Cline) — that's
  `cline-orchestration`.
- The user wants to debug the harness design — that's
  `harness-engineering` or `loss-function-design`.

## How the skill's scripts work

`scripts/cycle.sh` (in this skill) is the executable that
runs the loop. It takes:

- `--project-root PATH` (required) — the scaffolded project
- `--max-cycles N` (default 100) — hard cap on cycles
- `--delta FLOAT` (default 0.05) — improvement threshold
- `--max-stall N` (default 3) — consecutive no-improvement
  cycles before forced entropy counts as "applied"

The script is designed to be **invoked by a long-running
agent session** (the inner agent), which in turn invokes
the inner agent's wrapper per cycle. The session is the
*driver of the driver* — Hermes, a shell script, a CI
runner, or another agent.

## Pitfalls when using this skill

- **The driver doesn't write the candidate.** The driver
  prompts the inner agent; the inner agent writes the
  candidate. If the user wants the driver to also write,
  they want `harness-scaffold` or a manual `cline` call.
- **The driver is not a substitute for the inner agent.**
  The inner agent is the model; the driver is the
  optimizer. Don't run the driver without a working inner
  agent.
- **The driver is not interactive.** Once it starts, it
  runs cycles autonomously until a stop condition fires.
  The user can pause it (Ctrl-C) and resume later; the
  driver reads `logs/iteration-log.md` and picks up.
- **The driver is not safe to run on untrusted code.** The
  inner agent has full filesystem access (per the
  `AGENTS.md` "Surface" rules). The driver is the
  *amplifier* of that access. Sandbox appropriately.
- **The driver emits a lot of log noise.** Each cycle writes
  4-5 files. The `logs/` directory grows. Use the
  `iteration-log.md` for human review; the per-cycle JSON
  is for the driver itself.
- **If `scripts/cycle.sh` exits silently with no error
  message, it's almost always one of three `set -euo
  pipefail` failure modes.** Unbound variable + `set -u`,
  subshell non-zero + `set -e`, or `wc -l` containing a
  trailing newline. See
  `references/set-euo-pipefail-pitfalls.md` for the
  diagnostic recipe.
- **If `cycle.sh` works on Linux but errors on macOS, you
  introduced a GNU-ism.** BSD `grep`/`sed` on macOS don't
  implement `grep -P`, `sed \w`, or `sed \{1,\}`. Always
  use POSIX ERE with character classes and `*` quantifiers.
  See `references/posix-shell-portability.md` for the
  verified substitutions.

## Related skills (install separately if not present)

- `meta-loss-function-development` — produces the /goal
  prompt this skill consumes.
- `harness-scaffold` — scaffolds the project tree the
  driver runs against.
- `loss-function-design` — the 4-piece loss anatomy.
- `harness-engineering` — what the agent sees.
- `cline-orchestration` — the Cline runtime (substitute
  your own if not using Cline).

## References in this skill

- `references/cycle-protocol.md` — the step-by-step
  protocol for one cycle.
- `references/forced-entropy-rules.md` — the forced-entropy
  rules, with examples of when each fires.
- `references/stop-conditions.md` — the stop conditions,
  with worked examples.
- `references/log-format.md` — the iteration log format.
- `references/set-euo-pipefail-pitfalls.md` — the three
  bash failure modes that cause `scripts/cycle.sh` to
  "exit silently" and how to debug them.
- `references/posix-shell-portability.md` — the GNU-isms
  that break on macOS (BSD `grep`/`sed`) and the verified
  POSIX substitutions. Read this before changing
  `cycle.sh` or `run-loop.sh`.
- `references/integration-test-recipe.md` — the 5-step
  end-to-end test using `templates/fake-cline.sh` and a
  real `grade.sh`. ~30 seconds, no LLM in the loop.
- `templates/cycle-input.json` — the cycle input JSON
  template.
- `templates/fake-cline.sh` — a fake `cline` binary for
  integration testing. See `references/integration-test-recipe.md`.
- `scripts/cycle.sh` — the cycle runner.
- `scripts/score-cycle.py` — the per-cycle scorer.
- `examples/cycle-1.md` — a worked example of one cycle.
