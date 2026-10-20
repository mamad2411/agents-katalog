---
name: deep-test
description: Deep test ทุก domain — quick run path หรือ deep workflow ต่อ domain พร้อม orchestrator all
argument-hint: "[domain|all] [scope] [target%]"
related:
  - check-correctness
  - run-test
  - deep-thinking
  - deep-analyze
  - deep-review-codebase
  - deep-validate
  - update-tests
  - resolve-errors
  - review-test
  - check-flaky-tests
  - use-agent-browser
  - use-chrome-devtools
  - follow-tool-playwright
  - report-review
  - use-subagents
  - watch-browser
  - ask-me

---

## Goal

Run testing for any domain in one place — each domain has a `## Run Quick Path` (run the existing suite, or audit it statically in `test-correctness`) and numbered steps (deep workflow: detect → run → classify → report); `all` orchestrates every domain from real signals in fail-fast order (merged all `test-*` skills — there are no separate `test-*` skills anymore; merged the deleted `/check-test-correctness` as the `test-correctness` domain)

## Scope

Use when tests must run or a test domain must be analyzed deeply — unit, integration, e2e, api, cli, contract, component, visual, a11y, property, database, mobile, smoke, load, coverage, mutation, usage, website, test-correctness

- `/run-test [domain]` = thin dispatcher that routes here; the workflows live only in this skill (`references/<domain>.md`)
- Writing or restructuring test specs → `/update-tests`; improving the strategy (flaky, coverage gaps, suite speed) → `/improve tests` + `/deep-review-codebase` (domain `review-test`)
- Interactive browser watch + roleplay → this skill's `references/website.md ## 6 Roleplay Mode` (merged from `/watch-browser-and-test`); continuous watch + console-error fixes → `/watch-browser fix`; the fast post-deploy gate → `references/smoke.md`

## Execute

### 1. Domain Workflows And Signals

> Goal: pick the domain reference that matches the test target

| Domain | Reference | Signals | Coverage |
|--------|-----------|---------|----------|
| unit (default) | [references/unit.md](references/unit.md) | `*.test.*`, `*.spec.*`, vitest/jest/pytest/go test/cargo test | pure functions, edge cases, parameterized tests |
| component | [references/component.md](references/component.md) | `@testing-library/*`, Vitest browser, Playwright CT, Storybook | isolated render, props, events |
| integration | [references/integration.md](references/integration.md) | `*.integration.test.*`, testcontainers, compose | module boundaries, data flow, real deps |
| e2e | [references/e2e.md](references/e2e.md) | `playwright.config.*`, `e2e/` dirs | full user flows in a browser |
| website | [references/website.md](references/website.md) | routes/sitemap, dev/staging URL | real-browser click-through of every route + promote invariants + roleplay mode (user-roleplay subagents per route) |
| api | [references/api.md](references/api.md) | HTTP endpoints, OpenAPI, `*.hurl`, `*.bru` | REST/GraphQL/tRPC/WebSocket, all-routes check (`scripts/check-routes.*` + profile `route-checker` in `## Subagents`) |
| cli | [references/cli.md](references/cli.md) | `bin` field, command defs, `*.cli.test.*`, bats | exit codes, stdout/stderr, flags, error paths |
| contract | [references/contract.md](references/contract.md) | Pact files, shared schemas, `.proto` | consumer/provider both directions, drift |
| visual | [references/visual.md](references/visual.md) | `*-snapshots/`, `toHaveScreenshot`, Percy/Argos | screenshot diff vs baseline |
| a11y | [references/a11y.md](references/a11y.md) | axe/pa11y config, WCAG specs | violations, keyboard, contrast, screen reader |
| property | [references/property.md](references/property.md) | fast-check/proptest/hypothesis, fuzz targets | invariants on generated inputs, shrinking |
| database | [references/database.md](references/database.md) | `migrations/`, ORM config, test DB scripts | ephemeral DB, migration roundtrip, constraints |
| mobile | [references/mobile.md](references/mobile.md) | `.maestro/`, detox, `androidTest/`, `*UITests/` | device/emulator flows, gestures, permissions |
| smoke | [references/smoke.md](references/smoke.md) | `smoke` scripts/tags, health endpoints | fast post-build/deploy gate |
| load | [references/load.md](references/load.md) | k6/autocannon, load scripts, perf concern | throughput, latency percentiles, breaking point |
| coverage | [references/coverage.md](references/coverage.md) | coverage config or defined target | thresholds + gap-closing loop until target (default 100%) |
| mutation | [references/mutation.md](references/mutation.md) | `stryker.conf.*`, cargo-mutants, mutmut | assertion strength (kill rate), survivors |
| test-correctness | [references/test-correctness.md](references/test-correctness.md) | test files with assertions/mocks/snapshots, PR diff | assertions match the spec (not the implementation), vacuous/false-positive tests, mock drift — static audit, never runs the suite |
| usage | [references/usage.md](references/usage.md) | README/USAGE code blocks, package scripts | every documented example really runs (pre-ship gate) |

### 2. Flow

> Goal: run the shared deep flow — think, gather evidence, execute, report

1. Run `/deep-thinking` to analyze scope, test goals, and pass/fail criteria before starting
2. Pick the domain: from the argument (`/deep-test api` → `references/api.md`) or from the signals table above; no/unknown domain → `/ask-me`
3. Choose the depth: quick run → follow that reference's `## Run Quick Path`; deep → follow its numbered steps
4. Every domain run is pre-checked with the matching review domain (`/deep-review-codebase` — `review-api`, `review-cli`, `review-test`, `review-coverage`, per the global rules)
5. Fix failures through `/resolve-errors` — never suppress; unclear cause → gather evidence like `/deep-analyze` (exit code, log, screenshot) first; flaky → `/check-flaky-tests`
6. Write/change test specs → `/update-tests`; report per domain → the reference's report path + `/report-review` in chat
7. `all` → `### 3` orchestrator

### 3. Run All Domains (orchestrator, merged from `/test-all`)

> Goal: run only the domains a real signal justifies, cheapest failures first — never runs tests itself, never runs every type without a signal

1. `/run-lint` + `/run-typecheck` first; fix those errors — they are not test failures
2. Detect applicable domains from the signals table; no tests or incomplete coverage → `/update-tests` first; record the chosen list + reasons
3. Fail-fast order: unit → property → component → database/integration → api/cli/contract (per signals) → e2e → mobile → visual → a11y; load only with a perf signal; smoke as a post-deploy gate, not part of a suite run — record result/duration/failures per domain; the static `test-correctness` domain is never part of the run order — audit it separately (or as a pre-`/run-verify` gate)
4. Validate + classify: `/deep-validate` the source and `/deep-review-codebase` the tests — wrong source → `/resolve-errors`, wrong test → `/update-tests`, unclear → report; never fix without evidence
5. Fix per the classification and rerun; the same failure repeating ≥3 times → stop + report
6. Coverage: if a target exists → measure and run the gap-closing loop (`/deep-review-codebase coverage` + `/update-tests`) until the target (default 100%)
7. Report → persist `.devin/temp/report/<workspace>/test-all-<time>.md`; all passing → `/run-verify` (fail → `/resolve-errors`, retry ≤3)

## Rules

### 1. Discipline

- Always start with `/deep-thinking` and summarize from real run evidence like `/deep-analyze`; never guess
- Every domain isolates tests, cleans up side effects, and reports per its reference; each domain persists its own report under `.devin/temp/report/<workspace>/`
- Never `.skip`/`.only`/`xit`, never weaken assertions, never change source code to fit a wrong test
- Pick domains only from real signals; unsure → `/ask-me`
- Independent domains may run in parallel via `/use-subagents`; the API route groups use the `route-checker` profile in `## Subagents`

### 2. Boundaries

- This skill runs and analyzes tests; it does not author specs (`/update-tests`), not manage strategy/coverage gaps (`/improve tests`); overall test strategy/quality → `/deep-review-codebase` (domain `review-test`), while the assertion-vs-spec audit is this skill's static `test-correctness` domain
- General "is X correct?" questions across artifact types (docs claims, types, config, data) start at `/check-correctness`, which routes the tests domain here
- Dispatcher only: `/run-test` forwards here — never duplicate domain workflows there
- One workflow per domain: the reference file is the SSOT; other skills link to `/deep-test <domain>` instead of restating it
- Browser tooling for website/e2e/visual/mobile: `/use-agent-browser` (default), `/use-chrome-devtools` to inspect a failure; authored suites → `/follow-tool-playwright`

## Subagents

> Goal: independent work that can be spawned to run in parallel — the profile lives right in this section, no separate file needed

### route-checker — test one API route group and return pass/fail per route with evidence

- **Inputs**: `route-group` (the list of routes it owns, e.g. `GET /api/users`, `GET /api/users/{id}`), `base-url` (target, e.g. `http://localhost:3000`), `method-policy` (safe methods only by default, or `allow-write` once the user confirms), `headers` (optional — auth headers, e.g. `Authorization: Bearer <token>`; the parent must mask before reporting), `timeout`/`slow-threshold` (optional — default timeout and `slow` threshold)
- **Tools**: `exec` — run `bun <skill-dir>/scripts/check-routes.ts` or the `scripts/check-routes.ps1` fallback (only `bun *check-routes.ts *` and `*check-routes.ps1 *` are allowed), `read` — read the manifest/results file
- **Execute**: 1) write the group's route list to a temp routes file or pass it via `--routes` 2) run `bun scripts/check-routes.ts --base <base-url> --routes-file <file> --out <result-file>` 3) dynamic segments `{id}` are replaced with `1` by the script 4) classify each route: `ok` (2xx/expected), `redirect` (3xx), `protected` (401/403), `slow` (>3000ms), `critical` (4xx/5xx/timeout/DNS/TLS), `skipped` (non-safe method), `missing` (404) 5) if every route fails with the same pattern → flag it as a group-level issue (e.g. wrong base path), not per-route
- **Output**: a per-route table `| No. | Method | Route | Status | Expected | Time (ms) | Severity | Evidence |` ending with a group summary (tested, skipped, ok, protected, critical, missing) plus the persisted result file path
- **Constraints**: fire only `GET`/`HEAD`/`OPTIONS` unless the parent passes `allow-write` confirmed by the user; never fire at production if the parent did not state confirmation; always mask credentials/tokens — never return real secrets; every route must have a tested or skipped result with a reason — never guess a status; only handle the assigned route group, do not fire routes outside the group; read-only — no `write`/`edit`

## Expected Outcome

- the selected domain runs through its reference (quick path or deep steps) to completion with a persisted report
- failures are classified as source/test/environment and routed to the suitable fix skill
- `all` runs every domain that has a signal in fail-fast order and ends at `/run-verify` or a blocker report
