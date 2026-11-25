---
name: rsi-loop
description: >-
  Run a fully agentic development loop on a codebase, driven by a BACKLOG.md:
  advance one medium-sized task per iteration with the repo's own
  tests/typecheck/build as the gate, commit, and self-schedule the next
  iteration indefinitely with no human checkpoints. Use whenever the user wants
  a fully autonomous dev or maintenance loop: "autonomous loop", "RSI loop",
  "keep working through my backlog", "perpetual development". Each iteration
  handles a complete, meaningful task — not a micro-step — balanced between
  scope and reliability.
---

# RSI Loop (fully agentic)

A backlog-driven autonomous loop that advances a project **one medium task at a
time** and runs indefinitely with **zero human intervention**. Each iteration
picks up a self-contained item from the backlog, implements the minimal correct
change, runs the repo's full quality gate, and commits — no micro-decomposition,
no multi-agent voting, no checkpoints.

## Scope philosophy

This loop is configured for **medium tasks** (not micro-steps, not epics):

| Scope | When to use |
|---|---|
| **Micro** (single function, one file) | Trivially checkable; rsi-loop handles these easily but you're paying overhead per item |
| **Medium ← you are here** | A self-contained feature, refactor, or bugfix — touches 2–5 files, one logical change, completable in one iteration. The sweet spot |
| **Large / epic** | Multi-iteration work that needs decomposition into medium tasks in the backlog |

## Setup (first run)

On first run, use safe defaults silently:

1. If `.rsi-loop.json` exists at the repo root, use it.
2. **Otherwise, create `.rsi-loop.json` with defaults below** — never block, never ask questions.

Contract fields (defaults used when no config exists):

- **commit_target** (`"branch-pr"`): branch + PR.
- **perpetual** (`true`): self-schedule the next iteration when done.
- **max_blast_radius** (`"medium"`): files/lines a single iteration may touch
  before it must stop and self-correct by splitting into smaller items.

If there is no `BACKLOG.md`, create one by inferring the project goal from the
repo (README, package.json, code structure), then seed P0–P3 medium-sized items.

## The loop (one iteration)

Do exactly one iteration per invocation, then perpetuate:

1. **Intake.** Read `BACKLOG.md`. Take the first unchecked item (P0 → P3).

2. **Scope check.** Verify the item is a medium task. If too large, decompose it
   into 2–4 medium items in the backlog and pick the first. If too small, batch
   it with related items until the batch forms a medium task.

3. **Implement** the **minimal correct** change, reusing existing modules. No
   speculative abstractions; no new dependency if a few lines do. Match the
   repo's conventions. Keep within `max_blast_radius`.

4. **Gate.** Run the **full** quality gate the repo defines (complete test suite
   + typecheck + build). Add a test for genuinely new logic. Commit **only if
   everything is green** — a red gate means fix or revert, never commit red.

5. **Record.** Check off the item in `BACKLOG.md`, add follow-ups, update docs.

6. **Commit** per `commit_target`, with a message naming the item. Don't commit
   session/scheduler state or scratch files.

7. **Regenerate (RSI).** If no unchecked items remain anywhere, generate a small
   batch (3–5) of high-value, non-speculative medium items aligned with the
   project goal and append them to the backlog. Commit the plan and continue.

8. **Perpetuate.** Schedule the next iteration (host loop / self-paced wakeup)
   with a prompt that re-enters this skill.

## Model

A single capable model (e.g. Sonnet, Opus) handles the entire iteration. Each
task is medium-sized — the model has room to understand context and produce a
coherent change without per-step voting.

## Honest boundaries

- **The gate is the only safety net.** No redundancy, no voting. A mistake the
  tests don't catch can land. Keep the suite meaningful.
- **Direction is self-determined.** The loop decides what to build from the
  project's own signals — no human checkpoint at regeneration. If strategic
  alignment matters, seed the backlog explicitly.
- **Medium tasks require good judgment.** Each iteration makes multiple
  decisions; model capability matters more than in a micro-step setup.

## References

- `references/backlog.md` — `BACKLOG.md` format, priorities, and regeneration rule.
