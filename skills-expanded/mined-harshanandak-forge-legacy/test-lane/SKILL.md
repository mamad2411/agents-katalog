---
name: test-lane
description: >
  Use when a push suddenly takes ~10 minutes, when a test run says "unmapped
  pushed files require full unit coverage", or before adding a new top-level
  path or command to Forge. Do not use to skip tests or to raise a timeout —
  this is about routing, not about running less.
---

# test-lane

A slow push is almost never a hang. It is the full-suite lane, and the full-suite
lane is what an **unmapped path** buys you. [Forge #8 ×3]

## The two lists that decide the lane

A changed path stays on the fast targeted lane only if it satisfies **both**:

1. `isKnownTargetablePath(file)` — `scripts/test.js`
   [verified 2026-08-13, around line 181]
2. It resolves to at least one real test file through
   `getTestCandidatesForChangedFile(file)` / `DIRECT_TEST_CANDIDATES` —
   `lib/commands/test.js` [verified 2026-08-13, around lines 30 and 202]

Satisfy one and not the other and you still get the full suite: an unrecognised
path sets `hasUnmappedFiles`, and a recognised path that maps to zero existing
tests sets `hasZeroResolvedTests`. Either flag flips the plan to `full`.

## Diagnose before you guess

```bash
node -e "console.log(JSON.stringify(require('./scripts/test.js').classifyPushTests(process.cwd()), null, 2))"
```

Read `mode` and `reason`. `reason` names the exact cause:
`unmapped pushed files require full unit coverage`,
`known changes did not resolve runnable tests`,
`package-level changes detected`,
or `known changes mapped to targeted tests` when you are on the fast lane.

## Adding a new path

Both edits, in the same commit as the path itself:

- `scripts/test.js` → add the prefix to `isKnownTargetablePath`.
- `lib/commands/test.js` → add the prefix to
  `getTestCandidatesForChangedFile` (or an exact entry in
  `DIRECT_TEST_CANDIDATES`), pointing at tests that **exist**.

Then re-run the classifier above and confirm `mode: "targeted"`.

## Rules

- **Never widen a timeout to make a lane pass.** A slow lane is a routing bug or
  a real regression. Bumping the budget hides both. [Forge #9 ×3]
- **Never delete or vacuously weaken an assertion** to get green. Same class.
  [Forge #9 ×3]
- Markdown that other suites read (README, AGENTS.md, docs/) also pulls in the
  doc-asserting suites automatically — you do not need to list those by hand.
  [verified 2026-08-13 — `selectDocAssertingTests`, `lib/commands/test.js`]
- Local green is not CI green. A targeted lane proves the mapped tests pass on
  your machine, nothing more. Read `gh pr checks` or the shepherd verdict before
  you call anything ready.

## Done when

`classifyPushTests` reports `mode: "targeted"` for your change, the tests it
selected actually ran, and you can name which test file covers the new path.
