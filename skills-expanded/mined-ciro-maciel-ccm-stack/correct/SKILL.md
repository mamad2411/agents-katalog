---
name: correct
description: Turn a mistake the person corrected twice into a check that refuses it: structure, then hook or lint, then test, text last. Use for /ccm-stack:correct.
---

# Turn corrections into checks

Assume every contributor is an agent that saw only the files it opened, copies the nearest example, and takes the shortest path that works. A rule written in a document fails silently whenever an agent skips it. A check does not.

## Find the classes

Read recent commits and reverts, review comments, the agent instruction files (`CLAUDE.md`, `AGENTS.md`), saved memories of corrections, and comments that explain workarounds. Group mistakes into classes. A class counts when it happened twice.

## Fix each class at the highest level that works

1. **Structure: make it impossible.** One owner per piece of state, one supported way per task. Hide internals so the wrong import fails. Replace lists kept in sync by hand with one source. Delete the old way an agent would copy.
2. **A check that refuses.** A hook, a lint rule or a script whose error message names the file, function or command to use instead. If the bad pattern is already common, fail only when a change adds one more.
3. **A test of the behavior.** Fix or delete any test that stays green when the behavior breaks.
4. **Text last**, only for judgment calls nothing can check. Text still needs proof: add an eval case (the `evals` skill) that fails without the new text and passes with it.

In CCM Stack, a new hook-enforced rule is three edits: an entry in `rules.json`, a function in `lib/checks.js`, and two test cases in `test/checks.test.js` (one it refuses, one it allows). For a rule that is only yours, use your config instead: add it to `forbiddenCommands` with the message that says what to do.

## Prove each check

Break the code on purpose, or replay a real past mistake, and watch the check fail. A check that has never failed has never been tested. Then put the code back and watch it pass.

## Keep the table

Keep a table in the agent instruction file that pairs each rule with what enforces it: a hook, a lint, a test, or "text only". When the person corrects something already marked "text only", it is a repeat: raise its level in the same piece of work. Remove a rule once its mistake can no longer happen.

**Reply:** each class with its evidence, the level you chose, and why a higher level did not work.
