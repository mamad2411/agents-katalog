---
name: loop-verify
description: Runs this project's verification contract and decides honestly whether something is verified, a gap, or a lie. Use before calling anything done, and whenever a report says "should work".
---

# Verify for real

Read `.loop/VERIFY.md` and run the slots that apply to what changed. Then write down
what you observed, in the words of what you saw — not in the words of what you hoped.

## The three things that are not verification

1. **A green build.** It proves the code compiles. Nothing else.
2. **"I read the code and it looks right."** The bug you are looking for is exactly
   the one that looks right.
3. **"It should work."** Then it is not verified. Say that instead.

Add two more that fool people constantly:

4. **An exit code of 0** — a command can succeed while doing nothing.
5. **An HTTP 200** — many servers answer 200 for a page that does not exist. Verify
   by finding a **string that only exists in the new behaviour**, not by status code.

## What counts

Each slot must produce an artifact or a direct observation:

- **BUILD** — the project's build/test command, green. Necessary, never sufficient.
- **OBSERVE** — the thing itself, doing its thing: a page rendered in a real browser
  with a clean console and a real interaction (click, type, navigate); a CLI run with
  its real output; an endpoint returning the new field. A screenshot or captured
  output is the artifact.
- **DATA** — query the store and confirm the effect: the row exists, the value
  changed, the wrong value is refused.
- **MONEY** — if money moves, use the provider's test mode and confirm the resulting
  state changed for real. Never test with live money.

## Testing against a real system

If the project has a test database or a seeded environment, use it: set up, run,
tear down. **That is the default.** Working against a live system is an exception
that must be declared in `.loop/VERIFY.md`, and when it is unavoidable: wrap in a
transaction and roll back, or restore the fixtures afterwards and confirm nothing
was left behind.

Two traps worth naming: your own tooling may run with more privileges than a real
user, which hides permission bugs — check with the actual role. And a check that
passes for you may fail for a signed-out visitor — check both.

## The verdict

For each slot: **VERIFIED** (with the one line of what you observed), **GAP**
(with the reason it cannot be checked here — a missing access, no browser, no test
environment), or **FAILED** (go back to building). A slot may not be silently
skipped. If a required slot is a GAP, the item is not done — it is delivered with a
declared gap, and it says so in `.loop/STATE.md`.
