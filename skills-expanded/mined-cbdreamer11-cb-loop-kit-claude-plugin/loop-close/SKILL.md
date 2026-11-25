---
name: loop-close
description: Closes a slice or a session - adversarial audit of the diff, ledger entry, selective commit, honest report, and the handoff for the next session. Use before considering anything finished.
---

# Close

Closing is not paperwork. It is the step that makes the next session cheap and stops
the same work from being done twice.

## 1 · Audit before you close

Dispatch the **`loop-auditor`** agent on the full diff, with the item's
non-negotiables from `.loop/STATE.md`. Its job is to refute. Iterate until there are
**zero CONFIRMED findings** — and do that *before* anything is published, not after.

If the auditor finds a real bug, also look for **the class of that bug**: search for
its siblings elsewhere in the codebase and close them in the same session, or record
them as their own items. One fixed instance and three live ones is not a fix.

## 2 · Commit

- Stage **only your own files**. Never `git add -A` when someone else has
  uncommitted work in the tree.
- A descriptive message: what changed and why, not "fixes".
- On the working branch. **Never the protected branch** — publishing is the owner's
  action, and it stays that way even when it is obviously fine.
- Team mode: open the pull request, make sure CI is green, assign a reviewer. Done
  means merged, not "it works on my machine".

## 3 · Write the record

- `.loop/STATE.md` — item to `[x]` plus one line of *what was verified and how*.
  Anything unverified becomes `GAP: <why>`. Anything blocked becomes
  `PARKED: <why> + exactly what is missing`.
- `.loop/DECISIONS.md` — any real choice made, with the rejected alternative.
- `.loop/GOTCHAS.md` — anything that fooled you: the symptom, why it was convincing,
  and how to detect it next time. This file is the compound interest of the method.

## 4 · Report honestly

Three lists, no softening:

- **Verified** — with what you observed for each, in one line.
- **Gaps** — what is not verified and why (a missing access, no browser, no test
  environment). Never dress a gap as done.
- **Blocked on the owner** — a key, real money, a business or legal decision, or
  permission to publish. State the exact thing needed, not a vague ask.

If something failed, say it failed and show the output. A report that reads better
than the work is the one failure this method cannot recover from.

## 5 · Hand off

Leave `.loop/STATE.md` so the next session needs no instructions: the next unchecked
item is next, and the command to run it is written beside it. Print that command.
