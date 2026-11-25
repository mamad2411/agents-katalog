---
name: benchmark-run
description: Save a benchmark of a finished Ork run, and every run it called, into a folder - cost, tokens, working and waiting time, the Ork version, by node, what went wrong - compare it with an estimate of the same change made in plain Claude Code sessions, and publish its safe parts to the repository's public benchmarks/. Use when asked to benchmark a run. Arguments - the run id, the folder to save into, and optionally a name.
argument-hint: <run> <folder> [name]
---

# Benchmark a run

Arguments: `$ARGUMENTS`, which are a run id (or prefix), the folder that holds
the benchmarks, and an optional name. If the run or the folder is missing, ask
for it. Never guess the folder.

The numbers come from scripts, not from you: `pnpm benchmark` measures and
`pnpm benchmark:control` estimates the control (`tools/benchmark/`, whose files
say how). Your part is the name, the result commits when a run committed none
itself, and the README's account of what happened.

## Rules

- **Working time** leaves out every minute the run waited on the maintainer:
  gates, `workflow.call` nodes waiting on their run, a node blocked on its own
  open question or permission prompt, and a leader waiting on a child that is
  blocked. Wall time and waiting time are reported beside it, never instead of
  it.
- The run's whole call tree is one benchmark: a `start` run with the `plan` and
  `build` runs it called.
- The scripts read a consistent copy of `~/.ork/state.db`. Never write to the
  store.
- **Carried weight** is a proxy (characters of a tool result times the later
  turns), never a cost, and `carried.json` holds only names of roles and kinds
  and numbers. Never add a path, a command or result text to it.
- A benchmark folder is never overwritten. Pick another name.
- **The README is public.** The publish step copies it to `benchmarks/` in this
  public repository, so write it for someone who has never seen Ork: no local
  paths, no names but "the maintainer", nothing from a prompt or a plan that
  isn't already public, and commits linked on GitHub.

## Steps

1. **Check that it ended.** Run `ork ps --project all` and find the run. If it is
   still `running` (or waiting at a gate), say so and stop; benchmark it once it
   ends.
2. **Name it.** Use the name given. Otherwise take a short kebab-case name for
   the work: the plan's file name in `.ai/plans/`, or a few words from the
   brief, such as `cli-drivers-only` or `for-each-run-2`. Say which name you
   chose.
3. **Measure:**
   ```sh
   pnpm benchmark <run> <folder> --name <name>
   ```
   This writes `<folder>/<name>/` with `summary.json` (with `ork`, the Ork
   version the runs recorded, or the one at their start commit), `usage.csv`,
   `brief.md`,
   `spec.md` (the plan or spec that was built) and `workflow/` (the workflows,
   `project.yaml` and agents at the commit the run started from).
   It also writes `carried.json` (the carried weight by role and kind, turns per
   session, calls to `extract`) when the sessions' transcripts are on this
   machine, else it says so and writes none. `pnpm benchmark:carried <run>`
   prints the same report alone; see `benchmarks/method.md#carried-weight`.
4. **Carried weight.** Read the printed totals (or `carried.json`) and give the
   biggest roles and kinds, mean turns, and `extract` calls in the report; a
   before/after comparison of the same work needs both runs' `carried.json`;
   `pnpm benchmark:arms <folder> <name>…` sets several runs of the same tasks
   side by side by arm.
   Say when `missing_transcripts` is not empty.
5. **Result commits.** `summary.json`'s `result_commits` lists the commits the
   run's tool nodes printed (a `publish` step). If it is empty because the
   maintainer committed the change by hand, find that commit with
   `git log --since=<run start>` and its diff, and confirm it with the
   maintainer. Then add it to `result_commits` in `summary.json`. If nothing was
   kept, leave it empty: the control then has no row for this run.
6. **Control:**
   ```sh
   pnpm benchmark:control <folder>
   ```
   This rewrites `<folder>/CONTROL.md` and `control.json` for every benchmark
   in the folder, with this run's row among them.
7. **What happened.** Read `ork logs <id>` for each run in the tree
   (`summary.json`'s `runs`), and `summary.json`'s `activations`, to find:
   failed sessions and why (turn cap, budget, an error, an Ork bug), review
   rounds, what each permission request asked, conflicts, and how builders
   overlapped (from the activations' starts and minutes, by owner).
8. **Write `<folder>/<name>/README.md`** for the public, in the shape of the
   published ones in `benchmarks/` (read one first):
   - `# <what was built>`, then one paragraph: what Ork built, the run id, the
     date, the Ork version from `summary.json`'s `ork`, the driver, and the
     result commit as a GitHub link with its stat (`git show --shortstat`).
   - `## At a glance`: status, cost and the workflow's `limits.budgetUsd`,
     working, waiting and wall minutes, sessions (failed), turns, all tokens
     by kind, questions and permission requests.
   - `## By node`: from `by_node`: node, model, sessions, cost, output, cache
     read and cache write.
   - `## How it ran`: the shape of the run; for a leader, when builders ran and
     how many at once; review rounds and what they found.
   - `## What went wrong`: one bullet per problem, each saying whether Ork, the
     agent or the workflow caused it, and the fix if one was made. "Nothing
     failed" when nothing did.
   - `## Against a manual session`: this benchmark's row from `CONTROL.md`, and
     one sentence reading it, linking `../method.md#the-manual-baseline`.
   - `## Files`: `summary.json`, `usage.csv`, `carried.json` when there is one,
     and `inputs/` (the brief, and the workflow, `project.yaml` and agents at
     the start commit).
9. **Publish** with `pnpm benchmark:publish <folder> <name>` from this
   repository. It copies only what may be public into `benchmarks/<name>/`,
   rewrites `benchmarks/results.json` and the README's results table, and
   refuses (writing nothing) on a path, an email, a token or a local name.
   If the overview in `benchmarks/README.md` ("What they show so far") no
   longer matches the table, update it with the new totals. Run
   `pnpm benchmarks:check`, and commit only when the maintainer asks.
10. **Report** the headline numbers to the maintainer (cost, working, waiting and
   wall minutes, the control's median and range), and anything that went wrong.
