---
name: autoresearch
description: "Autonomous hill-climbing on any measurable problem: qualify the four legs, freeze an eval referee, then loop mutate-evaluate-keep/revert until the stopping condition fires. Works on tests, latency, bundle size, cost."
disable-model-invocation: true
---

# Autoresearch

Autonomous **hill-climbing** over a **mutable artifact**, judged by a **frozen
referee**, advanced by a **git ratchet**: keep what measurably improves,
revert what doesn't, never stop until the stopping condition fires. The human
programs the protocol; you run the experiments; the referee decides.
Generalized from [karpathy/autoresearch](https://github.com/karpathy/autoresearch).

**Continue mode**: if invoked as `continue` (or the repo already has a
`PROTOCOL.md` and `results.tsv` on an `autoresearch/*` branch), read both,
skip to phase 4, and resume the loop under the existing protocol.

## 1. Qualify

The pattern stands on four legs. Name each concretely before anything else:

| Leg | Question | Example |
|---|---|---|
| Mutable artifact | Which files may the loop edit? | `src/translator/**` |
| Quantitative metric | One number; which direction is better? | tests passed, higher |
| Bounded eval | One command, fixed budget, prints the metric | `pnpm eval`, ~30s |
| Keep/discard | Can a bad change be fully reverted? | git commit / reset |

A missing metric or eval command is normal: you construct it in phase 3. But
if the artifact isn't revertible or nothing is measurable even in principle,
say so and stop. This problem does not hill-climb.

## 2. Align: grill the protocol out of the user

Invoke the `grill-with-docs` skill on the proposed run (fall back to
`grilling` if unavailable). The grilling must pin down, at minimum:

- **Objective**: the single metric and its direction. Secondary metrics are
  constraints, never co-objectives.
- **Stopping condition**: a target value, an experiment budget, a wall-clock
  budget, or a plateau (no keep in the last K experiments). "Run until
  interrupted" is allowed only if the user says so explicitly.
- **Frozen zone**: everything the loop must never touch (eval harness, data,
  dependencies, rule checks).
- **Eval budget**: fixed time per experiment, so results stay comparable.
- **Constraints and the simplicity criterion**: resource ceilings, rules, and
  how much added complexity a marginal gain is worth. Deleting code for equal
  results is a win.

Write the answers into `PROTOCOL.md` at the target repo root, using the
[protocol template](references/protocol-template.md). The protocol is the
human's program: the human iterates on `PROTOCOL.md`, the loop iterates on
the artifact. Done when the user confirms the protocol.

## 3. Freeze the referee

Build the evaluation harness. Domain recipes, the referee contract, noise
handling, and the anti-Goodhart checklist live in
[harness recipes](references/harness-recipes.md); consult it before building.

Hard gates, all of them, before the loop may start:

- One command prints one machine-parseable metric line (`metric: <value>`)
  and exits non-zero on failure.
- **Baseline twice**: run the referee two or three times on the unchanged
  artifact. The spread is the **noise floor**; if noise swamps the expected
  effect size, fix the harness before proceeding.
- The referee and `PROTOCOL.md` are now **frozen**: only the human may change
  them. If mid-loop you feel the urge to "fix" the referee, that is Goodhart
  knocking. Stop and ask.

Record the baseline as the first journal row.

## 4. The loop

One-time setup: branch `autoresearch/<tag>` off the current branch; journal
`results.tsv` (tab-separated, untracked, never committed) with header
`commit	metric	status	description`.

LOOP until the stopping condition fires:

1. Pick the next idea: protocol idea seeds, near-misses in the journal, or
   your own judgment.
2. Edit the artifact. `git commit`.
3. Run the referee: `<eval-cmd> > run.log 2>&1`, then grep the metric line.
   Never stream run output into context.
4. Empty grep means crash: read the log tail. A dumb bug (typo, import), fix
   and rerun once or twice. A fundamentally broken idea, journal `crash`,
   reset, move on.
5. Journal the row: short commit hash, metric (0 for crash), status
   (`keep`/`discard`/`crash`), one-line description.
6. Improved beyond the noise floor: **keep**, the ratchet advances. Anything
   else: **discard**, `git reset --hard` to the last keep.
7. Stopping condition unmet: loop. Do not pause to ask whether to continue;
   the protocol already decided. Out of ideas means think harder: re-read the
   artifact, combine near-misses, try something more radical.

Kill any run exceeding 2x the eval budget and treat it as a crash.

**Long runs**: to keep the loop alive across sessions or overnight, tell the
user to start it as `/loop /autoresearch continue` (self-paced re-invocation;
continue mode picks the run back up each time).

## 5. Report

When the stopping condition fires, report: baseline vs best metric, counts of
keeps/discards/crashes, the cumulative diff of surviving changes
(`git diff <baseline-commit>..HEAD --stat`), and the journal. The branch holds
the result; merging it is the user's call.
