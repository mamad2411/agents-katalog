---
name: run-area-tests
description: Pick and run only the tests a change can affect - the affected-tests selector, one knowledge-map area, or named files - instead of the full suite. Use after each red/green step and before finishing a task step.
---

# Run the affected and area tests

Choose the cheapest layer that proves the behaviour; see `docs/agent/verification.md` for
the full L0-L5 table. Never describe a focused pass as a full-suite pass.

The [scope table](../../../docs/agent/verification.md#choose-the-verification-scope) owns
required checks. Its layer catalog describes available commands, not a cumulative checklist.
For bounded core/harness/engine changes, run the affected L3 suites; harness changes also need
the incident gate. Reserve full verification for broad integration changes or explicit requests.

## Selector

`scripts/affected-tests.mjs` is read-only. It takes changed files from `git diff` against
the merge-base with `origin/dev` plus untracked files, walks each test's import graph, and
merges explicit edges from `tests/test-map.json`.

```sh
node scripts/affected-tests.mjs                     # list L1 (pure) and L3 (rig) tests
node scripts/affected-tests.mjs --json              # machine-readable selection
node scripts/affected-tests.mjs --run               # run L1 with two workers, L3 serially
node scripts/affected-tests.mjs --tier L1 --run     # skip the slow rig group while iterating
node scripts/affected-tests.mjs --files src/shared/chat-activity.ts --run
node scripts/affected-tests.mjs --staged --run      # only what is staged
```

Rig tests (anything reaching `tests/helpers/studio-rig.ts`) are L3 and run with
`--test-concurrency=1`. A change under `src/harness-seed/**` or `src/game-template/**` also
selects the harness gate (`harness-incidents` and `scoreboard`), because rigs copy those
folders instead of importing them.

## Area and named files

- Area ids with their docs and sources: `docs/agent/knowledge-map.json`;
  `npm run review:context -- --area <id>` lists the docs and checks for one area.
- One or more files: `npm test -- tests/conformance/<name>.test.ts [more files]`. This avoids
  building the affected graph, so prefer it for red/green iteration.
- One behaviour while iterating:
  `npm test -- --test-name-pattern='<test name>' tests/conformance/<name>.test.ts`.

## Rules

- Red first: run the new or changed test and see it fail for the right reason.
- A selector that picks nothing for a behaviour change means a test or a
  `tests/test-map.json` edge is missing; add it rather than skipping verification.
- On failure keep the log, decide whether product, expectation, fixture or environment is
  wrong, and rerun only after a specific change. Never raise deadlines to get green.
- Full `npm test` / `npm run verify` only for broad changes or when asked. Full Node tests run
  the fast group with two workers, then rigs serially; rigs still run after fast failures.
- Report which layers and files ran.
