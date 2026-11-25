---
name: arena
description: >-
  Run 2-4 independent attempts at the same task in parallel, score them against one acceptance check,
  pick the best as the base and graft in the strongest parts of the others. Use for "arena this",
  "try a few approaches", "give me options and pick the best", or when one attempt at a design-heavy,
  open-ended or hard-to-get-right piece of work is likely to come out mediocre.
---

# Arena

When there are several reasonable ways to do something, a single attempt picks one of them by
accident. An arena tries a few on purpose, judges them on the same test, and keeps the best parts.

## When it applies

- The result depends on choices more than on effort: an algorithm, an API shape, a data model, a UI
  layout, a prompt, a piece of copy.
- An earlier attempt came back mediocre and it's not clear why.
- The work is small enough that 2-4 copies are affordable.

Skip it for mechanical work (a rename, a known fix, a dependency bump), where every attempt converges
on the same answer and the arena only multiplies cost.

Say the cost before starting: N attempts cost roughly N times one attempt, plus judging.

## Procedure

### 1. Write the spec and the acceptance check first

Both are shared by every attempt and written before any attempt starts:

- the spec: what to build, inputs and outputs, constraints, what's out of scope;
- the check: something that runs and scores. Tests that must pass, a benchmark with a target, a
  screenshot compared at three widths, a rubric with numbered criteria for copy. If the check can't
  tell the attempts apart, sharpen it before going on.

### 2. Make the attempts different on purpose

Identical briefs to identical models give near-identical results. Vary one thing per attempt:

- the approach ("use a state machine", "use a lookup table", "stream it");
- the model or model family;
- the priority ("simplest that passes", "fastest", "most readable").

### 3. Run them isolated and in parallel

Give each attempt its own git worktree and branch so they can't step on each other:

```bash
git worktree add ../arena-a -b arena/a
git worktree add ../arena-b -b arena/b
```

Start every attempt at once (parallel subagents, or separate CLI runs), each told to work only in its
own worktree and to report what it built, how it scored on the check, and the assumptions it made.

### 4. Judge

Run the acceptance check yourself on every attempt; don't take an attempt's word for its own score.
Then read the ones that pass. Lay out a table:

```
| Attempt | Check | Size | Strongest part | Weakest part |
| a | 14/14 tests, 38 ms | +210 lines | error handling | naming |
| b | 13/14 (fails empty input) | +120 lines | the core loop | no validation |
```

### 5. Pick a base, then graft

Pick the attempt that passes the check and is simplest to keep as the base. Bring over the strongest
part of each other attempt only where it makes the base better on the check or clearly simpler.
Grafting everything produces a patchwork; graft only what earns its place.

Run the check again on the result. It must score at least as well as the best single attempt.

### 6. Clean up

Remove the worktrees and branches you created (`git worktree remove`, `git branch -D`), keeping only
the merged result. Report the table, what was grafted from where, and the final check output.

## Rules

- The acceptance check exists before the first attempt starts, and the same check judges all of them.
- You run the check; attempts don't grade themselves.
- Two attempts is a valid arena. Four is the most that's usually worth it.
- If no attempt passes, the spec or the check is probably wrong. Fix that, don't add attempts.
