---
name: loop
description: "Run a long-running, self-driving agent loop (the 'let the model drive' pattern) with separated planner/generator/evaluator roles, an on-disk contract, and taste scoring. Use when the user runs /loop, says 'loop on this', 'let it run for a while', 'set up a generator/evaluator loop', or wants one agent to keep building-and-grading against a rubric until it converges. This is the operator entry point that sets up state and drives the cycle; the loop-planner, loop-generator, and loop-evaluator skills are the three roles it coordinates."
---

# /loop — the loop is the unit of work

Run a task as a **loop**, not a prompt. A prompt is typed once and forgotten; a
loop runs while you sleep. The five verbs are `gather · reason · act · verify ·
repeat`; everything below is a footnote on those verbs.

This skill is grounded in the field notes distilled in
[references/principles.md](references/principles.md) (Karpathy, *LOOPS.md*). Read
it once — the prompts here encode those nine rules.

## When to use

- The user wants an agent to keep working toward a goal with little supervision.
- The task has a **gradable** outcome (tests, a rubric, or taste axes you can write down).
- You would otherwise be re-typing a message at 3am. Close the tab; write the loop.

Do **not** loop a one-shot task, a task with no verification, or anything whose
"done" you cannot describe in a contract.

## The three roles (never blur them)

One task, three context windows, three system prompts. Mixing roles is the most
common failure: the model turns sycophantic the moment it grades its own work
and the loop converges on slop.

- **Planner** — turns the vague human sentence into a sprint spec. Never touches code. → `/loop-planner`
- **Generator** — writes everything. Forbidden from grading its own output. → `/loop-generator`
- **Evaluator** — reads diffs, runs the app, and is told from message one that the code is broken and its job is to prove it. → `/loop-evaluator`

You (this skill) are the **operator**: you set up state, kick off each role,
route the contract, score, and decide continue / restart / stop. Run the roles
as separate sessions (live-paired) or as separate headless invocations
(orchestrated) — the state on disk is identical either way.

## Setup

1. Pick a `loop-id`: `<repo-name>-<short-slug>` (e.g. `bestie-onboarding-polish`).
2. Create the loop directory `.TerMinal/loops/<loop-id>/` and initialize state per
   [references/state.md](references/state.md): `contract.md`, `feature_list.json`,
   `progress.md`, append-only `log.md`, `events.jsonl`, `scores/`.
3. Create an isolated worktree for the generator so a restart is a clean delete:
   `git worktree add -B loop/<loop-id> ../.worktrees/<repo>/loop-<loop-id>`.
4. Append the kickoff to `log.md`: `## [YYYY-MM-DD] init | <one-line goal>`.

## The cycle

Repeat until a stop condition. Every step reads and writes disk, never relies on
context memory (context compacts, rots, and lies — a file does not).

1. **Negotiate the contract first.** Before the generator writes a line, the
   planner drafts `contract.md` and the evaluator pushes back. They argue in
   markdown until they agree on a checklist of **testable assertions** (roughly
   10–30 for a small app; ten is usually too few and gets rubber-stamped). The
   planner's spec is the boundary; the **contract is what gets graded.** This one
   step moves runs from broken demos to working products.
2. **Generate.** The generator implements the next unmet contract items in its
   worktree, updates `feature_list.json` + `progress.md`, and appends `log.md`.
3. **Evaluate.** The evaluator reads the diff and traces (not vibes — see
   principle VII), runs the app / tests, and marks each contract assertion
   pass/fail with evidence. It is adversarial by construction.
4. **Score the subjective.** For taste-bearing work, the evaluator also scores
   the four axes in [references/taste.md](references/taste.md) → a number in
   `[0,1]` plus a paragraph naming the gap. Write it to `scores/NNNN.md`.
5. **Decide.**
   - **Continue** if assertions remain and progress is real.
   - **Restart** if the run has gone sideways (see below).
   - **Stop** if the contract is met and the taste score has plateaued.

## Let the loop restart

The best behavior from a good model is the willingness to throw everything away
and start over when a run goes sideways — delete the worktree at iteration nine
and ship a working version at iteration eleven. **Do not interrupt a restart.**
The restart is the loop working correctly. A restart is just:

```
git worktree remove --force ../.worktrees/<repo>/loop-<loop-id>
git worktree add -B loop/<loop-id> ../.worktrees/<repo>/loop-<loop-id>
```

...keeping `contract.md` (the agreed goal survives; the code does not).

## When to insert a human (HITL gate)

Insert a human **only when the contract itself is wrong**, not when the build is.
File HITL (see the `notify` skill for AFK) for exactly these:

- The contract no longer matches what the user actually wants.
- A destructive / irreversible / outward-facing action, a protected-branch merge,
  or credential handling.
- A genuine product-choice ambiguity the contract can't resolve.

A failing build, a bad iteration, or a restart are **not** human-gate events —
they are the loop doing its job.

## Stop conditions

- Every contract assertion passes and the last two taste scores are within ~0.02.
- A hard iteration or budget cap is hit (record it in `log.md`; never silently continue).
- The user stops the loop.

## Discipline (carry these into every role prompt)

- **Bounded reads.** Never feed a whole transcript, scrollback, test log, or diff
  into the model. Default 80 lines / 12k chars; prefer file refs, commit ids, test
  names. Use `scripts/bounded_context.py` from the `loop-supervisor` skill.
- **Read the traces.** Every debugging insight comes from the raw transcript, not
  another experiment. Grep for the moment judgment diverged; fix the prompt for
  that exact moment.
- **Delete the harness.** Re-read this scaffold against each model release and
  delete anything the model now does for free. A harness that only grows is one
  you've stopped reading.
- **Watch the bottleneck move.** When coding stops being the bottleneck, planning
  is; then verification; then taste. Surface the current one in `progress.md`.
