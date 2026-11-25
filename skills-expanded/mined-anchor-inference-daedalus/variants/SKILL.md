---
name: variants
description: Changing something and measuring the result — benchmark tuning, a performance hunt, prompt work, a flaky test. Frozen results, one fixed run command, a tree of variants that builds on its own winners. Use before the second attempt at anything you measure.
requires: board
---
# Variants you can compare

Any work where you change something and measure what it does — a benchmark score, a runtime, a
pass rate, a token count — goes wrong in the same three ways, whatever the domain:

- the code that produced a number is edited afterwards, so the number no longer means anything;
- the command changes between attempts, so two results are not comparable;
- every attempt starts from the original state, so wins never accumulate.

This is the protocol that prevents all three. It needs no new tooling: **git branches hold the
variants, the board holds the round, `Verify` holds the results.**

## The two cardinal rules

**1. A node freezes the moment a run answers it.** A variant exists to establish a baseline or to
test one idea. A run that *answered* it — produced the number the variant was after, good, bad or
absurd — freezes the branch it ran from: never edit that branch again, branch a child instead. A
disappointing result is a result, not a reason to go back and adjust.

A run that *died* answered nothing — an out-of-memory, a missing dependency, a typo, a timeout —
so there is nothing to protect: fix the branch in place and re-run the same variant. The exception
is a variant whose question *is* about memory or runtime; then the crash is its answer.

**Repair cap: two runs in a row that answer nothing on one variant, then stop and ask the
operator.** Different errors still count. If the same failure hits a second variant, that is one
setup problem, not two variants — ask then.

**2. The run command is a fixed contract.** One command measures the whole tree, inherited
verbatim by every variant: same entry point, same dataset, same seeds, same environment
variables, same machine where that matters. Variants differ **only in committed code**. The
moment you want a different command, you are asking a different question: that is a new baseline
with its own tree, not a sibling in this one.

Write the command down once — in the board task, in `AGENTS.md`, in the round's note — and run it
through `Verify` so every result is a receipt with an exit code and an output digest behind it,
not a sentence you wrote afterwards.

## Shape: stacked bushes, not a flat fan or a noodle

```
FLAT FAN (wrong)         NOODLE (wrong)        STACKED BUSHES (right)
base                     base                  base
├ a ├ b ├ c … ├ n        └ a                   └ cache-head       ┐ round 1:
                           └ b                    ├ lru           │ the options of
                             └ c                  └ arena         ┘ one decision
                               └ d …                 └ winner ── batching-head   ┐ round 2:
                                                        ├ batch 8               │ descends onto
                                                        └ batch 32              ┘ round 1's winner
```

- **Flat fan** — every attempt hangs off the baseline, so every result is measured against the
  start and the work never compounds.
- **Noodle** — a single chain where each step does not actually build on the one above it; depth
  for its own sake.
- **Stacked bushes** — a small fan *within* a round (the open options of one decision), then the
  next round descends onto that round's winner.

**The parent test.** Before you make X a child of Y, name what Y established that X builds on.

- You can name it ("Y is the cache that won; X keeps that cache and changes the batch size") →
  real depth: X is a child of Y.
- You can't, because X and Y are co-equal options you are trying at the same time (LRU vs arena) →
  they are **siblings** in one bush.

So width is the open options of one decision; depth is the decisions already settled, stacked. A
new round never hangs off the baseline — it hangs off the previous round's winner.

## The loop

1. **Set the baseline.** A branch with the starting code and the run command, measured once with
   `Verify`. That number is what everything is compared against. Put the round on the board with
   `BoardAdd`: the decision it settles, the command, and the acceptance criterion.
2. **Form one round's hypotheses** — the co-equal options of a *single* decision, each a concrete
   change you can make and measure. Do not mix decisions from different rounds into one batch;
   that is what produces the flat fan.
3. **Branch each option off the round's parent** (the baseline for the first round, the previous
   winner afterwards), commit only the change that option is about, and leave the command alone.
   Where this installation gives you a worktree tool for its own repositories, use it; for anything
   else — and on an installation that does not change its own code — `git worktree add` in the
   workspace does the same. One branch per variant, named for the idea.
4. **Measure with the fixed command through `Verify`**, one variant at a time, or in parallel when
   nothing is shared (do not measure two variants at once on a machine where they contend for the
   same CPU, GPU or port — that measures the contention). Record the receipt id against the
   variant on the board, and cite it when you report.
5. **Decide, per finished run:** *repair* (it answered nothing — fix the branch, re-run, cap of
   two), *refill* (mediocre — move to the next option), *promote* (a clear win — this branch is
   the parent of the next round), or *stop* (goal met, or the line is exhausted).
6. **Stop** when the goal is met, or after about three consecutive results that fail or regress.
   Then write up the tree: one line per variant with what it changed, its result and its receipt.

Frozen branches stay untouched throughout: promotion moves where the *next* round starts, it never
rewrites something that already measured a number.

## What to keep

- One branch per variant, kept until the write-up is done: the diff against its parent is the only
  honest answer to "what did this variant actually change?".
- The board task is the round's log — which options are open, which are done, which won, and why.
- The result of a variant is its `Verify` receipt, not a number in your reply. Cite the receipt.
- Write the deliverable (the comparison, the recommendation) into its own directory in the
  workspace, with the scripts that produced it beside it.

## What not to build

This is a protocol, not a subsystem. Do not build a variant database, a tree viewer or a run
archive: git already stores the code, the board already stores the round, and `Verify` already
stores the results. Everything above is discipline, and discipline costs nothing to keep.
