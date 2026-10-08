---
name: self-critique
description: Use after any non-trivial work (build, refactor, migration, non-trivial edit). Before saying "done," list 3 failure modes and check you didn't hit them. Then update priors.
---

# Self-Critique

After any non-trivial work, before you emit your `build.complete` event:

1. **List 3 ways this could be wrong.** Not "did I make a typo" — real failure modes:
   - Concurrency / race conditions
   - Off-by-one, null input, empty list, huge list, negative number
   - Cross-platform (Windows path separators, line endings, shell differences)
   - Did I break an existing contract? Does the existing test still pass?
   - Did I update the spec / docs to match?
   - Did I leave a debug `console.log` or `print`?
   - Did I commit a secret I shouldn't have?
   - Does this work on first run, or only after my warm-up state?

2. **Check each one.** Run a test. Grep for callers. Read the file. Whatever proves the failure mode doesn't apply.

3. **Update the prior.** If you found a real issue (even one you fixed), append to `.opencode/blackboard/priors.md`:
   ```
   - <iso>  <mode>: <one-line description of failure mode + the check that catches it>
   ```

4. **If you found a blocker you can't fix in 2 minutes**, set `next_action: wait_human` and surface it. Don't ship a known-broken change.

## Why

The fastest way to ship bugs is to not check. Senior engineers do this in their head constantly. The system makes it explicit so the agent has to slow down.

## Cost

~30-60 seconds per turn. Pays for itself the first time it catches a real bug.

## When to skip

- Trivial one-line edits (typo fix, comment update)
- Pure refactors that don't change behavior (but still run tests)
- Doc-only changes

## When you MUST do it

- Any change to a public API
- Any change to authentication, schema, or money
- Any change that touches tests
- Any change after a "weird" failure in a prior turn (read the prior in `priors.md` first)
