---
name: code-review-craft
version: 1.0.0
description: How to give an effective, specific code review — severity classification, what to look for beyond syntax, how to tell whether a new test is capable of failing, and how to phrase feedback that's actionable rather than vague. Load before reviewing a diff.
---

# Code Review Craft

## Form your own expectation before reading the diff

Read the linked requirement/ADR/ticket first and decide independently what a correct implementation looks like — approach, edge cases, contract — *before* reading the diff. Reviewing the diff first and reasoning backward from what the author built is the single most common way a reviewer ends up rubber-stamping the wrong thing: it silently substitutes "is this internally consistent" for "is this correct." If your expectation changes after seeing the implementation, say so and say why (this is `code-reviewer`'s §4 contamination guard).

## Severity classification

Every finding gets exactly one severity label: **must fix** (bug, security issue, regression, breaks a requirement), **should fix** (real improvement, not blocking), or **nit** (style preference, optional) — plus a confidence label (**high** / **medium** / **low**) stating how directly the finding was observed vs. inferred. Mixing these into undifferentiated feedback makes a reviewer's most important point indistinguishable from their least important one, and asserting low-confidence inference as fact is its own failure mode.

## What to look for beyond syntax

Correctness against the stated requirement; edge cases and error paths, not just the happy path; test coverage that actually exercises the new logic (read the tests, don't infer from "tests added"); whether this diff quietly introduces a new pattern/dependency/coupling that should have gone through architecture review; security-sensitive input handling; performance red flags (N+1, unbounded loops) proportionate to expected scale.

### Ask whether a new test has ever been seen red

A test added alongside a fix, only ever observed green, is indistinguishable from a test that asserts nothing — and reviewing it by reading is exactly how that goes unnoticed. For each new assertion, ask: what change to the production code would make *this line* fail? If you can't name one, that's a **must fix** on the test. The failure shapes to look for while reading: it inspects state the code already replaced (a re-rendered document, a reset fixture, a stale handle); the value it searches for was never present to begin with; a defensive layer elsewhere (a framework, the browser, a validator) masks the defect independently, so the test would pass with the change reverted; or it checks one encoding of a value while the leak occurs in another (`encodeURIComponent` vs. `URLSearchParams`, which encodes a space as `+`). Ask the author which assertion they watched go red, for which cause — one change at a time, not a batch revert. "It passes" is not the evidence; "it failed for this reason before the fix" is.

Fixtures deserve the same read. A check exercised against one shape of input proves something about that shape alone — if every case in a fixture is the same element type, content type, or lifecycle stage, any defect specific to the shapes left out passes silently. Flag a fixture whose cases don't vary over the dimension the invariant is stated across.

## Phrasing feedback

Be specific: reference file:line, state what's wrong and why it matters, and where possible suggest the fix rather than just naming the problem. "This could be cleaner" is not actionable; "this loop does an unindexed lookup per iteration — O(n²) — for a collection that can reach 10K rows in production" is.

## What review is not

Not a rubber stamp, and not an opportunity to relitigate scope or impose unrelated stylistic rewrites — review the diff for what it claims to do, correctly and safely, and flag out-of-scope observations separately rather than blocking on them.

A reviewer that only reads static code cannot confirm runtime behavior (concurrency timing, actual load behavior, an integration's real response shape) — flag anything that needs execution to confirm as a hypothesis for `qa-engineer` to verify, rather than asserting it as a closed finding either way.

## Not a patch generator

A code review's output is findings and a suggested direction, never a rewritten diff — producing the fix yourself removes the accountability boundary between "the author owns the change" and "the reviewer owns the critique," and risks the reviewer's own untested fix silently replacing the original bug with a new one.
