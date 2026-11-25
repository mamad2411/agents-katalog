---
name: sustained-execution
description: Keeps long, multi-session, or compaction-spanning tasks on track using an external task ledger, checkpoints, and resumable state. Use when work spans many steps/hours, may hit context limits, or must survive a reset. Pairs with decomposing-tasks (the plan), context-budgeting (the window), and operating-autonomously (unattended runs).
license: Apache-2.0
metadata:
  author: Adrian Paredez
  version: "1.0"
  tier: "2"
  layer: meta/control
compatibility: Requires filesystem read+write for the ledger. Works on any runtime; benefits from but does not require automatic compaction.
---

# Sustained execution

Long tasks fail not from lack of capability but from **lost state**: the window fills,
gets compacted, and the agent forgets where it was. The fix is an **external ledger** -
durable memory that survives compaction and resets. The context window is scratch; the
ledger is truth.

## Use this when
- Work spans many steps, multiple sessions, or hours.
- The run will likely hit the context hard ceiling (see `context-budgeting`).
- The task must be **resumable** if interrupted.
- **Skip** for short tasks that finish within one comfortable window.

## The ledger (single source of truth)

Maintain one file (e.g. `notes/ledger.md`) holding:

```
GOAL + DONE criteria         (verbatim, from decomposing-tasks)
PLAN with step states        ([x] done / [>] active / [ ] pending)
DECISIONS log                (what + why/constraint, append-only)
CHECKPOINTS                  (digest pointers, newest last)
ARTIFACTS                    (paths/URLs the run produced or depends on)
NEXT ACTION                  (the single next concrete step, always current)
```

The **NEXT ACTION** line is the resume anchor: any fresh agent reads the ledger, finds
NEXT ACTION, and continues without re-deriving anything.

## The loop

```
- [ ] INIT     write GOAL+PLAN to the ledger (from decomposing-tasks)
- [ ] before each step: read NEXT ACTION
- [ ] do the step
- [ ] after each step: update step state + DECISIONS + NEXT ACTION  (write-through)
- [ ] at context soft ceiling: offload detail, keep ledger pointers  (context-budgeting)
- [ ] at hard ceiling: write CHECKPOINT digest -> reinitialize -> reload goal+ledger
- [ ] on resume/interrupt: read ledger -> NEXT ACTION -> continue
- [ ] at end: confirm every DONE criterion; close the ledger
```

## Principles

1. **Write-through, not write-back.** Update the ledger *immediately* after each step, not
   "later." A crash/compaction between step and write loses that step.
2. **The ledger is append-mostly.** DECISIONS and CHECKPOINTS append; PLAN step-states and
   NEXT ACTION mutate. Never rewrite history you might need.
3. **One current NEXT ACTION.** Always exactly one concrete next step recorded. If you
   can't write it, you don't know what to do next, re-plan.
4. **Checkpoints are resume points.** A checkpoint = a `context-budgeting` digest, saved,
   pointer added to the ledger. After a checkpoint, context holds only goal + ledger +
   active step.
5. **Verify before you record DONE.** A step isn't done because you ran it; it's done when
   its outcome passes its check (`verifying-reasoning` for critical ones).
6. **Idempotent resume.** Re-reading the ledger and re-doing the NEXT ACTION should be
   safe; design steps so a repeated step doesn't corrupt state (esp. one-way doors -
   record "done" only after the irreversible action confirmed).

## Resume protocol (the payoff)

On any fresh start (new session, post-compaction, after interruption):
```
1. Read the ledger.
2. Reload GOAL + DONE + PLAN states + latest CHECKPOINT + ARTIFACTS pointers.
3. Go to NEXT ACTION. Continue. (Do not re-explore solved sub-problems.)
```

## Runtime adaptation
- **Minimum:** filesystem read+write. The ledger is a plain Markdown file.
- **If the runtime auto-compacts:** still keep the ledger, auto-summaries are lossy and
  not under your control; the ledger is.
- **If a memory/state mechanism exists** (e.g. a memory dir, KV store): use it as the
  ledger store, same protocol.
- **Multi-agent:** the ledger is the shared contract; each agent reads NEXT ACTION.

## Files
- `references.md`, ledger schema, checkpoint cadence, crash-safety.
- `examples.md`, a multi-session build walked end to end.
- `templates/ledger.md`, the ledger to copy.
- `templates/checkpoint.md`, checkpoint entry format.
- `checklists/resume.md`, the resume protocol as a checklist.
- `benchmarks/`, resumability and long-run completion method.
