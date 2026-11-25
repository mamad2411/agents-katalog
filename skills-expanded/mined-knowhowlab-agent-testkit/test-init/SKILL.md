---
name: test-init
description: Analyze the current repository and generate (or update) its test plans — TESTS_E2E.md for autonomous integration runs and TESTS_MANUAL.md for guided hand-testing — at the repo root. Use whenever the user wants to set up e2e or manual testing, create or refresh a test plan, "init the tests", bootstrap acceptance testing, or after a feature lands and the plans need updating. Also use when test-e2e or test-manual report a missing plan file.
---

# test-init — Generate the project's test plans

**Goal**: Produce two reviewable, versioned plan files at the repository
root — `TESTS_E2E.md` (consumed by the `test-e2e` skill) and
`TESTS_MANUAL.md` (consumed by `test-manual`) — that together cover the
project's acceptance surface. Both follow plan format v1: read
`references/plan-format.md` in this skill's directory **before writing
anything**, and `references/coverage-map.md` before the recon.

## Mode detection

If `TESTS_E2E.md` or `TESTS_MANUAL.md` already exists at the repo root →
**update mode**. Otherwise → **create mode**. If the user's request names
only one of the two files, still keep the sibling in sync where coverage
overlaps (parity rule), but don't rewrite it wholesale.

## Create mode

1. **Recon first, questions second.** Work through the recon checklist in
   `references/coverage-map.md`: task runners, build files, compose files,
   CI workflows, docs and quickstarts, existing test trees, health
   endpoints, previous protocol files. Read; do not execute the stack.
2. **Draft the coverage arc.** Map findings onto the universal arc (gates
   → build → static validation → live → verification → failure/recovery →
   matrix → lifecycle → packaging → teardown → wrap-up). Note per phase
   whether it belongs in E2E, MANUAL, or both.
3. **Interview.** One batched message with only the questions recon
   couldn't answer (the list is in coverage-map.md): canonical commands,
   known flakes → Facts, credentials pointer, manual-only vs e2e-only
   flows, wanted scopes, destructive fences, flaky external dependencies.
   Wait for answers.
4. **Write both files** per the format contract. Non-negotiables:
   - Every step has a concrete `Expect:` — no "run it and see".
   - Same phase numbers where the two files cover the same ground;
     mode-exclusive phases appended after the shared ones.
   - E2E steps are fully assertable by a machine; MANUAL steps are one
     action each, copy-paste-ready, with GUI actions as `Do:` lines.
   - Secrets never inline — pointers to where they live.
   - Known caveats and flakes land under `## Facts` so executors won't
     "fix" expected behavior.
   - Long commands become helper scripts under `tests/manual/helpers/`,
     listed as Fixtures.
   - Stamp the marker comment: `<!-- agent-testkit plan · format v1 ·
     generated YYYY-MM-DD by test-init -->`.
5. **Static sanity pass.** Verify every file, script, and path the plans
   reference actually exists, and every command's binary is plausibly
   available (`command -v`, manifest inspection). Fix the plans, not the
   repo. Do not start services.
6. **Report.** Show the user: phases per file, scopes defined, Facts
   recorded, anything you could not determine (marked `TODO(user)` in the
   plan). Recommend a first run: `test-manual` once by hand to shake out
   the plan, then `test-e2e` for regressions.

## Update mode

1. Read the existing plans; note `Source docs` from Meta and any
   `<!-- lock -->` fences (locked sections are never rewritten).
2. Re-run recon focused on drift: new scripts, changed CI gates, new
   services in compose, new specs/quickstarts since the `generated` date,
   phases referencing commands or paths that no longer exist.
3. Propose changes as a compact summary (added / changed / removed per
   phase) **before** editing. Apply on confirmation. Preserve the user's
   hand-edits outside the drifted sections; update the marker comment date.
4. Run the same static sanity pass and report.

## Rules

1. **Plans are artifacts, not scratch.** They will be reviewed in PRs.
   Write them tight, imperative, and self-explaining.
2. **Never run the stack during init.** Recon is read-only; the sanity
   pass checks existence, not behavior.
3. **Don't invent coverage.** If recon and interview leave a phase's
   commands unknown, write the phase with `TODO(user)` markers rather
   than guessing plausible-looking commands.
4. **Respect repo conventions.** If the project already has protocol
   directories, naming habits, or helper-script conventions, adopt them
   in Meta instead of imposing defaults.

## Defaults (when the user has no preference)

- Protocol dirs: `tests/integration/` (e2e), `tests/manual/` (manual).
- Protocol prefixes: `test-e2e-protocol`, `test-manual-protocol`.
- Scopes offered: `quick` (skip `slow`-tagged phases), `no-build`,
  `keep-up` (skip teardown).
- Retry default: connection refused / initializing → wait 15–30 s, retry
  once, then investigate.
