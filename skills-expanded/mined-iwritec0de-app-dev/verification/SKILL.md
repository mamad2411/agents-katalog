---
name: verification
description: >-
  This skill should be used before claiming any work is complete, before
  committing, before creating PRs, or before reporting task status. Enforces
  fresh verification evidence for all completion claims. Provides the
  verification gate methodology: run commands, read output, then report.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Verification Skill

**Evidence before claims, always. NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION.**

## Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.** If you have not run the verification command in the current session, you cannot claim it passes. Prior knowledge, assumptions, and memory of previous runs do not count. Only fresh output from the current session constitutes evidence.

## The Five-Step Gate

Every completion claim must pass through this gate:

1. **Identify** — Determine which command proves your claim. "Tests pass" requires running the test suite. "No lint errors" requires running the linter. "It builds" requires running the build.
2. **Execute** — Run the command freshly. Not from memory. Not from a previous session. Right now, in the current session.
3. **Read** — Read the FULL output. Do not skim. Do not assume. If the output is long, read all of it. Errors can hide at the end.
4. **Verify** — Confirm the output actually supports your claim. A test suite that prints results but exits with a failure code does not pass. A build that emits warnings about missing dependencies is not clean.
5. **Assert** — Only after steps 1-4 are complete, state your claim and include the evidence. Quote the relevant output.

## JS/TS Verification Checklist

Before claiming work is complete in this project, run each applicable command and confirm clean output:

| Check | Command | What it proves |
|-------|---------|---------------|
| Type checking | `tsc --noEmit` | No type errors across the project |
| Tests | `npx vitest run` or `npm test` | All tests pass |
| Lint | `npx eslint .` | No lint errors or warnings |
| Formatting | `npx prettier --check .` | All files match formatting rules |
| Production build | `next build` | Build succeeds, catches SSR/hydration issues |

Run these in order. A type error caught by `tsc` is cheaper to fix than one discovered during `next build`. A lint error is cheaper to fix before tests run.

If a project uses a different test runner, linter, or build tool, substitute the appropriate commands. The principle is the same: run the real tool, read the real output.

## Red Flags

These phrases are signals that the verification gate has NOT been passed:

- **"should"** — "Tests should pass" means you did not run them.
- **"probably"** — "This probably works" means you did not verify it.
- **"seems to work"** — "It seems to work" means you observed something informal, not a verification command.
- **"I believe"** — "I believe the build is clean" means you are guessing.
- **Premature "Done!"** — Claiming completion without showing command output.
- **"All good!"** — Without evidence, this is an opinion, not a verification.

If you catch yourself using these phrases, stop and run the actual command.

## When to Verify

- **Before every commit** — Run the full checklist. Do not commit code that fails any check.
- **Before marking a task done** — The task is not done until verification proves it.
- **Before creating a PR** — The PR description should reference verification results.
- **Before reporting status** — "Feature complete" means verified, not "I think I finished writing code."
- **Before delegating "completed" work** — If you hand off work as complete, you are vouching for it. Verify first.
