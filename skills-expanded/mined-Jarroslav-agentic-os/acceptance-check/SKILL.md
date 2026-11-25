---
name: acceptance-check
discoverable: false
description: |-
  Required functional proof for anything user-visible, run right after gate-runner. When a change touches UI or another externally visible surface, it reuses e2e coverage that already exists, or generates a focused Playwright check when none does; either way it captures screenshots, console output, and network errors, and writes verification-evidence.json per feature.
  Not for: unit/integration testing (gate-runner), changes with no externally visible surface, or replacing a full QA pass.
version: 0.1.0
license: Apache-2.0
authors:
  - agentic-os
---

# acceptance-check

`gate-runner` answers one question: did the configured lint/build/test scripts
exit clean. That is a claim about the code, not about the product. A test
suite can be green while the button a user actually clicks does nothing,
because nothing in the suite ever opened a browser and clicked it. This skill
is the second, independent claim — "a real session drove the changed surface
and it behaved" — and it refuses to let the first claim stand in for the
second.

For a managed run, record command and verification evidence through
`evidence.record` or `evidence.ingest` as described in
`../../references/runtime-authority.md`. The JSON verification files are
evidence artifacts, not lifecycle authority; refresh compatibility ledgers with
`legacy.export` rather than appending them directly.

## Inputs

| Input | Source |
|---|---|
| `gate_plan` | `<run_dir>/gate-plan.json`, written by gate-runner |
| `qa_report` | `<run_dir>/qa-report.md`, written by gate-runner |
| `branch` | current feature branch |
| `merge_base` | defaults to `origin/main` |
| `repo_path` | absolute path to the checkout |
| `run_dir` | absolute path to the run's state directory |

## Step A — Decide whether this run even applies

Diff `<merge_base>...HEAD` by name only. A user-visible surface changed if any
touched path matches `gate_plan.ui_globs`, looks like a new entry point
(`*.html`, `index.tsx`, `index.jsx`, `App.tsx`, anything under `pages/`,
`app/`, or `routes/`), or is a manifest edit that changes what ships to the
client (e.g. a new export added to a UI library's `package.json`).

No match anywhere in the diff → this skill is a no-op for the run. Write
`verification-evidence.json` as `{"applies": false, "reason": "no
user-visible surface in diff"}`, return `{"required": false, "verified":
true}`, and stop. A match sends you to Step B.

## Step B — Pick the browser tool

Check the host project for these signals, in order, and stop at the first
hit:

1. A Playwright config file, or `@playwright/test` in `package.json` → `playwright`.
2. A Cypress config file, or `cypress` in `package.json` → `cypress`.
3. A configured Storybook interaction test runner → `storybook-test`.
4. `feature_verification.command` set in `.agentic/agentic-sdlc/config.json` → `custom`, using that command verbatim.
5. None of the above → `unconfigured`.

Cache the resolved tool at `<run_dir>/acceptance-check-plan.json` so later
phases don't re-detect it.

## Step C — Assemble what to run

| Tool | How it runs | Target |
|---|---|---|
| `playwright` | `npx playwright test`, narrowed to a per-file pattern when one applies | the project's own `baseURL` |
| `cypress` | `npx cypress run --spec <pattern>` | the project's own `baseUrl` |
| `storybook-test` | `npx test-storybook` | the built Storybook |
| `custom` | exactly the configured command | as configured |
| `unconfigured` | nothing to assemble yet | — |

For each changed UI file, first look for an existing sibling test
(`<file>.spec.ts`, `<file>.test.tsx`, or a matching `tests/<feature>.e2e.ts`).
Reusing that beats writing anything new. Only when nothing matches do you
build a fresh check:

1. Infer the route or story from the framework's own layout conventions
   (`app/`, `pages/`, `routes/`, a Storybook story, router config) — never
   guess a URL that isn't backed by one of these.
2. Infer the behavior to assert from the task's acceptance criteria plus
   whichever text/selectors/props actually changed in the diff.
3. If the project already has an e2e directory and Playwright configured,
   drop the new spec there rather than inventing a separate location.
4. If there's no e2e directory but Playwright is available, generate
   `<run_dir>/dynamic-tests/<feature-id>.spec.ts` against a Playwright config
   you point at the running host app.
5. If you can't tell how to start the host app, check the common script
   names (`dev`, `start`, `preview`) and the project config; if that still
   comes up empty, stop with status `BLOCKED` and name the missing start
   command.

A generated check has to exercise the behavior that changed — at least one
real interaction or assertion drawn from the criteria — not merely confirm
the page renders.

## Step D — Execute and capture

If the tool resolved to `unconfigured` but a surface did change, try the
dynamic Playwright path from Step C — but only when the project is
Node-based and installing a dependency is allowed. If that path isn't viable
either, halt with `BLOCKED` and write:

```json
{
  "schema": 1,
  "applies": true,
  "result": "BLOCKED",
  "reason": "UI surface changed but no browser verification tool is configured",
  "remediation": "Install Playwright (npm i -D @playwright/test && npx playwright install) or set feature_verification.command in .agentic/agentic-sdlc/config.json"
}
```

Otherwise, run the resolved (or freshly generated) command and capture:

- exit code
- the last ~50 lines of stdout/stderr
- any console errors the browser session reported
- any monitored request that came back 4xx/5xx
- one screenshot of the verified end state, at `<run_dir>/evidence/screenshots/<feature>.png`

## Step E — One evidence file per feature

A "feature" here is one covered unit: a reused spec, a generated dynamic
test, or one coherent group of changed files that a single check exercises.
For each, write `<run_dir>/evidence/verification/<feature-id>.json`:

```json
{
  "schema": 1,
  "feature_id": "<derived id, e.g. checkout-summary>",
  "applies": true,
  "tool": "playwright | cypress | storybook-test | custom",
  "coverage_source": "existing-test | generated-test | manual-command",
  "test_command": "npx playwright test checkout.spec.ts",
  "generated_test_path": "<run_dir>/dynamic-tests/checkout-summary.spec.ts",
  "app_url": "http://localhost:3000/checkout",
  "browser_steps": [
    "navigate to /checkout",
    "add item to cart",
    "apply promo code SAVE10",
    "click button[type=submit]",
    "expect total to reflect discount"
  ],
  "assertions": [
    "discounted total matches expected value",
    "no console errors",
    "no failed network requests"
  ],
  "screenshot_path": "evidence/screenshots/checkout-summary.png",
  "console_errors": [],
  "network_failures": [],
  "result": "PASS | FAIL | INCONCLUSIVE",
  "captured_at": "<ISO>",
  "duration_ms": 3980
}
```

Decide `result` this way:

- All listed assertions held, zero console errors, zero network failures → `PASS`.
- Any assertion missed, or a non-zero exit code → `FAIL`.
- The check ran but leaves a real coverage gap — an empty test body, a check
  that only confirms the page loaded, or a route that never reached the
  changed feature → `INCONCLUSIVE`.

## Step F — Roll up and return

Append to `<run_dir>/qa-report.md`:

```markdown
## Did it actually work

**Status**: PASSED | BLOCKED | FAILED
**Driven with**: playwright
**Why it ran**: a UI surface changed

| Feature | Result | Driven by | Console | Network |
|---------|--------|-----------|---------|---------|
| checkout-summary | PASS | npx playwright test checkout.spec.ts | 0 | 0 |
| account-settings | PASS | npx playwright test dynamic-tests/account-settings.spec.ts | 0 | 0 |
```

And return to the caller:

```json
{
  "required": true,
  "verified": false,
  "tool": "playwright",
  "results": [
    {"feature_id": "checkout-summary", "result": "PASS"},
    {"feature_id": "account-settings", "result": "INCONCLUSIVE"}
  ],
  "blocking": true
}
```

`blocking` is `true` the moment any per-feature `result` is FAIL,
INCONCLUSIVE, or BLOCKED — one weak result blocks the whole gate.

## Non-negotiables

- `verified: true` requires a `verification-evidence.json` with `result:
  "PASS"` behind every changed user-visible surface — no exceptions on
  partial coverage.
- Every verification command runs from inside the host project root, never
  from anywhere else.
- Any console error anywhere in a captured session is a hard fail on its
  own — there is no "minor" console error.
- A `PASS` without a screenshot doesn't count; the screenshot is the
  artifact a human actually checks.
- A generated test starts life as verification evidence, not product code.
  Promote it into the permanent test suite only once it's stable and
  idiomatic; until then it stays under `<run_dir>/dynamic-tests/`.
- If Step A found no surface change, this skill has nothing further to do —
  exit clean, touch nothing else.
