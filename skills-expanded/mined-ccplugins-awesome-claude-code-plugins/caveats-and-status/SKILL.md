---
name: caveats-and-status
description: Use when about to report any nontrivial task as complete — requires closing with a Caveats & status section stating what was verified, what was assumed, and what's unresolved.
---

# Caveats & Status

## Overview

"Done" without a status check is a guess wearing a confident voice. This skill defines the closing
format every nontrivial completed task uses, so what wasn't verified is always visible rather than
buried in an upbeat summary.

**Core principle:** state what you checked, not just what you did.

## When this applies

Any response that reports a task as complete, fixed, or passing — code changes, file scaffolding,
investigations with a conclusion. Skip it for pure Q&A with no action taken, and for the `quick`
flow's trivial one-liners where the verification step itself already says everything needed (don't
pad a two-line change with a boilerplate section that adds nothing).

## The format

End the response with:

```
**Caveats & status**
- Verified: <what you actually ran/observed, with the result>
- Assumed: <anything taken on faith because it couldn't be checked here>
- Not covered: <what's explicitly out of scope or unverified>
```

Omit a line entirely if it's genuinely empty (e.g. "Assumed: none" is fine to state plainly, but
don't stretch to fill a line that has nothing real to say).

## Rules

- "Verified" requires a command actually run or a behavior actually observed in this session —
  not "should work," not a previous run, not extrapolation from a partial check.
- If verification wasn't possible (no test environment, no way to run the app), say so explicitly
  in "Not covered" rather than silently omitting it — an honest gap beats an implied guarantee.
- Run the verification and read its actual output *before* writing the "Verified" line — the
  claim comes after the evidence, never before. Report failures honestly, with the actual error
  output, not a softened summary. This format stands alone; it does not depend on any other
  plugin being installed.
