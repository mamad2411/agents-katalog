---
name: squad-quality-bar
description: Tests passing is necessary but not sufficient. Before committing, run the self-review checklist — no commented-out code, no TODOs, no PM traces, no defensive checks for impossible cases, no half-finished implementations.
allowed-tools:
  - Bash
  - Read
disable-model-invocation: false
---

# The quality bar before commit

If you would not defend the code in review, do not ship it. The checklist below is the bar a customer who would churn over one bad weekend would hold you to. Hold it.

## When to use this skill

Invoke this skill immediately before running `git commit` on any code change. Use it as the explicit checkpoint between "tests pass" and "ready to land."

## The checklist

Walk through each item; each must be a clean "yes" or you are not done.

- **No commented-out code.** Delete it. Git remembers.
- **No `TODO`, `FIXME`, or "future work" comments.** If it is worth doing, file an item. If not, it is not worth a comment. Never defer work via TODO.
- **No defensive checks for things that cannot happen.** Trust internal invariants; only validate at system boundaries (user input, external APIs).
- **Minimum comments. Default to none.** Delete anything that restates what the code says. Only keep a comment when the WHY is genuinely non-obvious — a hidden constraint, a workaround for a specific bug, a subtle invariant. No test-function docstrings. No multi-line prose explaining a 3-line function. If in doubt, cut it.
- **No project-management traces in code.** The backlog lives outside the codebase; code does not reference it. Never put item IDs in filenames, identifiers, comments, or commit messages. Name tests by the behavior they assert, not the tracker ID that surfaced the bug.
- **No premature abstraction.** Three similar lines beats a wrong abstraction. Do not extract a helper until the third caller exists.
- **No half-finished implementations.** Either it works end-to-end against the AC, or it is not done. "Mostly working" is open, not done.
- **AC literally checked off.** Re-read the item's `## Acceptance criteria`. Each box maps to a test you wrote or a verification step you actually performed — not "I am pretty sure that works."

## Why this matters

Tests passing means the code worked once, against the cases you imagined. The quality bar is what makes the code stay working: future agents reading the diff six months from now should see clean code without dead branches, stale comments, or PM-trace pollution. The cost of meeting the bar at commit time is minutes; the cost of not meeting it is the slow accumulation of cruft that eventually makes the codebase unworkable.

## How to apply

1. Open the diff (`git diff --staged` or `git diff main...HEAD`).
2. Read every line of every file. Yes, every line.
3. For each new line, ask: would this survive review? If no, delete or refactor.
4. For each new file, ask: is the smallest possible diff still here, or has scope crept?
5. For comments specifically: would a reader who has not seen the commit message understand WHY this comment exists? If no, delete.
6. Re-read the AC. Walk each box mentally against the diff.

## Escape hatch

If you genuinely cannot meet the bar in this session — for example, the right fix requires a refactor outside scope — that is fine. Set `status: review` instead of `done`, write what is wrong in the resolution notes, file the follow-up item. Better to leave it open and honest than ship and hide.

## Anti-patterns to avoid

- Shipping a `TODO` because "I will get back to it." You will not. File the item.
- Leaving a one-line comment that says what the next line of code says. Delete it.
- Adding a nil check at a call site where the value provably cannot be nil. Trust the invariant.
- "Improving" code outside the item's scope while you are in there. File a DEBT, do not fold it in silently.
- Telling yourself "it is good enough." If you would defend it in review, it is good enough; if not, it is not.
