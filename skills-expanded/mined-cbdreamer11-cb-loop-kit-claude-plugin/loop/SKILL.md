---
name: loop
description: The build loop - locate yourself, investigate the real code, build one slice completely, verify it for real, fix and re-verify, then close and hand off. Use for any session that is implementing something from the plan.
---

# The loop

**Nothing is done until it has been observed working.** A green build, "I read the
code and it looks right", and "this should work" are not verification. The only
valid signal is observed behaviour.

Run these six steps for every item. Do not skip 0 and do not skip 5.

## 0 · Locate yourself

- Read `.loop/STATE.md` (what is done, what is next, what is parked) and
  `.loop/GOTCHAS.md` (traps this project has already sprung).
- `git log --oneline -15` and `git status`. **Anything already committed is not
  rebuilt.** A lot of what a document calls missing is already built and just not
  visible — confirm against the code before redoing it.
- Uncommitted files that are not yours may belong to a parallel session. Do not
  touch them, and do not reuse a shared counter they may have taken (see the shared
  resource in `.loop/VERIFY.md` — read its true state with the command declared there).
- The next item is the first unchecked `[ ]` in `.loop/STATE.md`. You do not need
  new instructions to continue.

## 1 · Investigate

Open the real files you are about to change. Map what exists, what is editable,
what is missing. Never work from memory of an API or a schema.
If a question is genuinely open — or the item touches money, permissions, auth, or
schema — run the `loop-council` skill *before* writing code, not after.

## 2 · Build, completely

One item at a time, finished. If completing it requires one more thing, that thing
gets built too: it is not reported as a leftover and it is not offered as a question.
An item is complete only if it would be **safe to leave exactly as it is, forever** —
no dead end, no control that does not do what it says, no setting with no effect.

## 3 · Verify for real

Run the slots in `.loop/VERIFY.md` that apply. The rule for each: it must produce an
**artifact or an observation** — a rendered page, a row, a file, a screenshot, a log
line that only exists if the new code ran. Forbidden as evidence: an exit code, an
HTTP 200, and "the build passed". Those prove the code compiled, not that it works.

## 4 · If it fails, fix it and verify again

Repeat 2 → 3 → 4 until it actually works. This is the loop. Do not move on with
something unverified, and do not describe a failure as a partial success.

## 5 · Close

- Commit on the working branch, staging **only your own files** (never `git add -A`
  when someone else has uncommitted work). Never push to the protected branch.
- Update `.loop/STATE.md`: mark the item `[x]` and add one line — *what you verified
  and how*. Record anything you could not verify as `GAP: <why>`.
- If you were blocked, write `PARKED: <why> + exactly what is missing` and move to
  the next item. **Park, never abandon, and never get stuck** on one item.
- Add to `.loop/DECISIONS.md` if you chose between real alternatives, and to
  `.loop/GOTCHAS.md` if something fooled you — the next session should not fall for it.
- Report the delta honestly: what is verified, what is a GAP, what is blocked on the
  owner. Then continue with the next item. Do not ask "am I done, shall I continue?".

## When to actually ask the owner

Only for what only they can unblock: a key or an access you do not have, moving real
money, a business/legal/pricing decision, or publishing. Everything technical you
decide yourself. "Do you want me to test it?" is never a valid question — if it
matters, you already tested it.
