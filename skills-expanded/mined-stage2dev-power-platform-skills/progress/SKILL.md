---
name: progress
description: "Use when you want to know where a kit Power Apps project stands and which command to run now: shows the STATE.md panel (stages done, in progress and pending), the build queue, overdue pending items and the next step. Also explains the pipeline to someone who has not started yet. Do not use to execute a stage (run the command it points to)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:progress — Orchestrator: coordinates and tracks

Shows where the project is and returns the next command. Read-only: it changes no file.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.

## Steps

1. `estado.py mostrar`.
   - **Exit 2 (no `STATE.md`):** explain the pipeline in up to 6 lines, from table §2 of
     `KIT/skills/power-platform/references/pipeline.md` (idea → definition → identity → build
     → delivery, one command per stage, a new session per stage) and finish with the "Next
     step" block pointing to `/pp-en:new`. If the folder already has an app (screens, flows), say that the
     pipeline is for a new app and that, for an existing app, you just describe the problem: the
     `power-platform` orchestrator picks the path.
   - **Exit 0:** show the output as it came.
2. **Build queue** (only if `GOAL.md` exists): per wave, tasks ✅ / total and the 🔴 waiting for the
   human, with what each one asks for.
3. **Pending items** (`D-xx` in `prd.md` and `GOAL.md`): the open ones, with owner and deadline;
   highlight the overdue ones with ⚠.
4. **Inconsistency** between `STATE.md` and the disk (stage completed without the file it delivers,
   e.g. design completed without `ux-design-system.md`): flag it with ⚠ and say which stage to run again.

## Wrap up

The "Next step" block exactly as `estado.py` printed it. Do not execute the stage in this
session: the user opens a new session and runs the command.
