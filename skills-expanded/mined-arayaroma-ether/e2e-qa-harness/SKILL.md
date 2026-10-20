---
name: e2e-qa-harness
description: Verify a UI-facing change in a real browser with Playwright and a fixed checklist before writing evidence.md in the verify phase — for changes that touch a frontend app.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# E2E QA harness

Use during the `verify` phase (see `ether-phase-dag`) for any change whose
`tasks.md`'s `## Files` section touches a frontend app (Next.js/React/etc,
not a backend-only change). It is a companion to `ether-tdd`'s regression
check, not a replacement — `ether-tdd` proves the unit/integration suite
still passes; this proves the change actually renders and works in a real
browser. No LLM calls, no vision model, no API tokens spent by the harness
itself — it is a plain Playwright process. Cost to you is only the few
hundred tokens to paste its text output into `evidence.md`.

## Why a fixed checklist, not "does this look right?"

An LLM asked to freely judge a screenshot is unreliable (generation ≈
open-ended judgment). An LLM — or a script — scoring a small, fixed,
extractable checklist (element visible, href correct, URL changed, network
call fired) is not. This harness never asks an open visual question; every
checklist item is a concrete Playwright assertion. Extend
`references/checklist-templates.md` with new item types before reaching for
free-form visual review.

## Run

Start the frontend app's dev server yourself first (its own README/CLAUDE.md
has the exact command and port). Then, from anywhere:

```bash
node <path-to-this-skill>/scripts/run-e2e.mjs \
  --app-dir /path/to/frontend-app \
  --tasks-md .ether/changes/<change-id>/tasks.md \
  --base-url http://localhost:3001
```

- `--app-dir` must be the directory containing the frontend app's own
  `package.json`/`node_modules` (Playwright resolves `@playwright/test` from
  there — the temp spec/config dir is generated inside it for that reason).
  Add `@playwright/test` as a devDependency there once
  (`pnpm add -D @playwright/test && npx playwright install chromium`) if not
  already present.
- `--tasks-md` supplies both the task description (used to pick a checklist
  template and guess a route) and the claimed file scope: its `## Files`
  section — the same list `ether-tdd` already requires for test coverage —
  doubles as the scope claim here, so there is no second format to keep in
  sync.
- The generated scenario is a starting smoke check (route loads, and for
  `footer/nav visibility` tasks, footer visibility). tasks.md prose written
  with explicit routes/element names in mind produces a more useful default;
  for anything beyond the smoke check, edit the generated `items` in
  `scripts/run-e2e.mjs`'s output run once, or hand-write a spec using the
  same per-type patterns in `references/checklist-templates.md`.

## Reading the output

Three independent signals print every run:

- **checklist**: `[x]`/`[ ]` per assertion, with the failure detail inline —
  paste this block into `evidence.md` verbatim (not a paraphrase).
- **scope**: compares the actual git diff in `--app-dir` against tasks.md's
  claimed files. A failure here in a clean single-change worktree is a real
  finding (untracked side effect); in a shared/dirty worktree it just means
  scope can't be attributed cleanly — say so in evidence.md rather than
  ignoring it.
- **exit code**: non-zero on any checklist failure, scope violation, or
  inability to launch the browser (missing Playwright install, dev server
  not running, etc — these show as "browser unavailable", not a silent
  pass).

## Known sharp edges (already fixed once, don't reintroduce)

- Generate the Playwright config + spec files *inside* `--app-dir`, never in
  a bare OS temp dir — Node's ESM resolver walks up from the config file's
  own directory looking for `node_modules`, and a temp dir outside the app
  never reaches it, so `@playwright/test` fails to resolve.
- The Playwright JSON reporter nests specs one level deeper than the
  top-level suite whenever `test.describe` is used — a scorer that reads
  `report.suites[i].specs` directly will always see zero items; recurse
  through `suite.suites` (see `checklist-scorer.mjs`).
- Each Playwright `test()` gets a fresh page — a `page.goto()` in one item
  does not carry over to the next; every item that needs a specific route
  must navigate itself.
- Scope link/element assertions to the actual component under test (e.g.
  `page.locator('footer').getByRole('link', ...)`), not the whole page —
  unrelated pre-existing elements with the same accessible name elsewhere on
  the page will otherwise cause a false strict-mode failure (and are worth
  reporting separately if found, not silently worked around).
- Compare `href`/URL assertions with tolerance for a trailing slash
  (`new RegExp('^' + href + '/?$')`) — frameworks with `trailingSlash: true`
  (e.g. Next.js) normalize paths and an exact-string match will false-fail.
