---
name: boyscout
description: "Use when editing an existing file, to leave it slightly cleaner without derailing into a refactor. Picks small, safe, in-scope improvements next to the change — a better name, a deleted dead line, a clarified condition — and keeps them separate from the behavior change so review stays clean."
---

# Boy Scout

## The failure mode this fixes

Two opposite failures rot codebases. One: never cleaning up, so entropy compounds until the file is a no-go zone. The other: a "quick change" balloons into a 600-line refactor that's impossible to review and ships three bugs. Agents swing wildly between both — either touching nothing around the change or rewriting the whole file uninvited.

The Boy Scout Rule threads the needle: leave the code a little better than you found it. Small, bounded, in-scope, separate from the behavior change. This skill enforces the *little* — disciplined cleanup, not a crusade.

## When to Use This Skill

- You're editing an existing file to make a change (any non-trivial edit)
- You notice something adjacent that's mildly wrong (a vague name, a dead line, a muddy condition)
- A reviewer asked "while you're in there, can you also..."

**Don't use when:** the file is brand new (nothing to clean), or the cleanup is large enough to deserve its own PR. If cleanup would exceed roughly a third of the size of your actual change, stop and file it as separate work — the cleanup is the tip, not the meal. For a *deliberate* dead-code sweep across a module, use `delete-this` instead — this skill is only for small, opportunistic, in-scope cleanup riding along with a change you're already making.

## Instructions

### 1. Make your real change first

Do the thing you came to do. Get it working and verified. The cleanup is a tip, not the meal — never let it block or bloat the actual change.

### 2. Scan only what you touched (the blast radius)

Look at the functions and lines your change touched, plus their immediate neighbors. **Do not** scan the whole file for sins — that's how scope explodes. The rule applies to the campsite you used, not the whole forest.

### 3. Pick improvements that pass the cheapness test

An improvement qualifies only if it is **all** of:
- **Small** — a name, a deleted dead line, one extracted helper, a clarified boolean, a fixed comment
- **Safe** — provably behavior-preserving (no logic change)
- **In-scope** — adjacent to your change, in code you already had to understand
- **Self-evident in review** — a reviewer sees instantly why it's better

If an idea fails any of these, it's not a Boy Scout fix — it's a separate task. Write it down (step 5) and move on.

### 4. Separate cleanup from behavior

Keep the cleanup in its own commit, distinct from the behavior change. The behavior commit must be readable on its own; the cleanup commit must contain zero logic changes. This keeps review honest and bisecting possible.

A qualifying cleanup may borrow a sibling skill at small scale — a better name (`name-things`), a deleted dead line (`delete-this`), a split that makes one thing testable (`seams`) — as long as it still passes the cheapness test in step 3. The discipline is the smallness, not the technique.

**If you're not committing** (editing a working tree for a human to commit, or running where commits aren't yours to make): still keep the two apart — clearly delineate in your diff and summary which changes are the behavior change and which are cleanup, so the human can split them or review them separately. The separation is the point; the commit is just the usual vehicle for it.

### 5. Park the big stuff

Anything that failed the cheapness test goes into a short "deferred" list — a TODO, an issue, or a note to the human — so it's captured without derailing the current change. This list is for cleanup only: a confirmed bug you tripped over is not a deferral candidate, it goes to `fix-it-now`.

## Output format

```
REAL CHANGE
  <the behavior change you came to make — its own commit>

CAMPSITE CLEANUP (separate commit, no logic changes)
  - <small safe improvement> @ <file:line>
  - ...

DEFERRED (too big for now — filed, not done)
  - <larger refactor idea> — why it's out of scope
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| The "while I'm here" rewrite | A 10-line change becomes 400 lines and three bugs. Bound the scope. |
| Cleanup mixed into the behavior commit | Reviewer can't tell what actually changed; bisect points at the wrong line. |
| Reformatting the whole file | Drowns the real change in whitespace noise and conflicts. |
| Cleaning code you didn't touch | Out of scope. Note it, don't do it. |
| Skipping cleanup entirely | The other failure mode — entropy wins by default. Leave it a little better. |

## Mental Model

> Leave the campsite cleaner than you found it — the campsite, not the forest. Small, safe, separate. The discipline is the smallness.
