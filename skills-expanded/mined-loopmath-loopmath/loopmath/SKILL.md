---
name: loopmath
description: "Start here when the user mentions loopmath without naming a job, for example 'use loopmath', 'use the loopmath skill', 'what can loopmath do' or 'what next with loopmath'. Checks the store in one command and moves straight into the right job: onboarding, bringing existing runs, updating the fit, planning a task or recording a run."
allowed-tools: Bash(loopmath:*)
---

# loopmath: start here

loopmath helps choose the workflow, models and effort for coding agent tasks, and learns from how the runs went. It predicts, records and refits. It never starts agents itself. Every command you need is in the loopmath skills and in `reference.md` next to this file; never run `--help`.

## Do this

1. Run `loopmath status --json`. Read `exists`, `counts.runs`, `open_runs[]`, `fit.latest`, `fit.usable`, `fit.problem`. If `loopmath` is not found, tell the user to install it (`pipx install loopmath` or `uv tool install loopmath`) and stop.

2. Pick the job from what the user said, then from the store, and follow that skill at once without asking:

   | The user said, or the store shows | Job (skill) |
   |---|---|
   | set up, onboard, start, try | `loopmath-onboard` |
   | names OCP files, a folder of runs, an experiment's output | `loopmath-import-runs` |
   | update, refresh or rerun the fit; what did loopmath learn | `loopmath-update-fit` |
   | a task to do, which workflow, model or effort to use, or `option N: ...` pasted from a planning page | `loopmath-plan-task` |
   | a task is done, or record, log or save a run | `loopmath-record-run` |
   | nothing specific, and `exists` is false or `counts.runs` is 0 | `loopmath-onboard` |
   | nothing specific, and `open_runs` is not empty | `loopmath-record-run` for those runs |
   | nothing specific, and `fit.latest` is set but `fit.usable` is false (say `fit.problem` in one line) | `loopmath-update-fit` |
   | nothing specific otherwise | tell the user in 3 lines what loopmath knows (`counts.runs` runs, fit `fit.latest`), then offer: plan the next task, bring existing runs, or see the results page (`loopmath posterior --html`) |

3. When the job's skill is not loaded, read its `SKILL.md` in the sibling folder (for example `../loopmath-onboard/SKILL.md`) and follow it.

## Never

- Do not start agents because loopmath said so, without the user's choice.
- Do not edit files under `~/.loopmath` or `$LOOPMATH_HOME` by hand.
- Do not record another person's sessions.
