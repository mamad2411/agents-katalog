---
name: loop-parallel
description: Parallel dispatch loop. Use when work splits into 3 or more independent pieces — scope non-overlapping file ownership per worker, keep one build/test lane as backpressure, and merge through a single owner.
---

# Parallel Dispatch Loop

Parallel subagents multiply throughput exactly when the split is clean — and multiply
merge conflicts, duplicated work, and corrupted files when it isn't. This loop is the
discipline for deciding *whether* to parallelize, scoping the workers, and merging the
results.

## When to reach for this

- A task decomposes into 3+ pieces with no shared state or files
- A migration/audit sweeps many files with the same transformation
- Multiple review perspectives are wanted on the same artifact (read-only fan-out)
- Tempted to "just spawn some agents" — this loop is the go/no-go check

## Iron law

**No two workers own the same file.** Ownership is assigned before dispatch, in
writing; a worker that needs a file outside its scope stops and reports instead of
editing it.

## The loop

1. **Split test.** Independent goals, disjoint files, no worker consumes another's
   output mid-flight. Anything coupled runs sequentially instead — sequential is a
   result, not a failure.
2. **Write the dispatch table** before spawning anything:

   | Worker | Goal | Owns (files/dirs) | Done-check |
   |---|---|---|---|
   | api | add rate-limit middleware | `src/middleware/`, `src/config.ts` | `npm test -- middleware` |
   | docs | document the new limits | `docs/api.md` | section renders, examples match config |
   | tests | integration coverage | `tests/integration/rate*` | new tests fail before / pass after |

3. **Brief each worker with a complete, self-contained task** — goal, owned paths,
   done-check, conventions to match. Workers do not see the parent conversation and
   cannot talk to each other; anything they need must be in the brief.
4. **One build/test lane.** Read/search work fans out freely; only one worker (or the
   coordinator) runs builds and test suites at a time — concurrent suite runs corrupt
   caches and interleave failures into noise.
5. **Merge through a single owner.** The coordinator integrates results one at a time,
   running the full suite after each integration (`loop-verify`), and reviews the
   combined result as one diff (`loop-review`).

## Rationalizations

| Excuse | Reality |
|---|---|
| "A small file overlap is fine" | Two writers to one file is lost edits, not a small overlap |
| "More agents = faster" | Past the backpressure lane, more agents = more queue and more merge risk |
| "The workers can coordinate between themselves" | They can't — every dependency routes through the coordinator or the split was wrong |
| "I'll figure out ownership as results come in" | Post-hoc ownership is how two workers both 'fix' the same function |

## Pitfalls

- Splitting by *kind of work* (one worker per language) when the coupling is by
  *feature* — the split must follow the dependency structure
- Briefing workers with a summary of the conversation instead of a self-contained task
- Skipping the per-integration test run because "each worker verified their piece" —
  integration is where independent pieces stop being independent
- Leaving a failed worker's partial edits in the tree unrecorded

---
*Related: `loop-review` (gate the integrated result), `loop-verify` (per-integration
evidence), `loop-long-horizon` (parallelism inside one iteration) · output/ADR format:
`playbook-conventions`*
