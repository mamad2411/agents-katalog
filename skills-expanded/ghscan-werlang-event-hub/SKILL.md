---
name: test-first-delivery
description: Deliver feature work, frontend test design, and refactors in this Academic Events repository with tests or explicit validation. Use when changing behavior, adding features, fixing regressions, updating tests, reviewing missing coverage, validating browser interactions, or documenting testing gaps across api/ and web/.
---

# Test-First Delivery

Use this skill whenever a task changes behavior in `api/` or `web/`.

## Default Quality Contract

- Code changes alone are not done.
- If the touched area already has automated coverage, update that coverage and run it.
- API feature work must update and run the committed Jest unit suite in `api/tests/unit` via `docker compose -f compose.dev.yaml exec api npm run test:unit`.
- API test runs must finish at `100%` passing tests before the task is considered complete.
- New or changed API behavior should add real-life success cases plus meaningful edge cases, not only happy-path assertions.
- Prefer the highest practical coverage for the touched API area, especially branches around validation, authorization, fallback defaults, and error handling.
- If automation is missing, choose between a small service-local bootstrap and explicit manual validation.
- Run the narrowest relevant validation path, fix failures, and rerun before finishing.
- Report what was validated, what was not, and why.

## Repository Reality

- This repo is split into two independent Node/Express services: `api/` and `web/`.
- `api/` now has a committed Jest unit suite rooted at `api/tests/unit` with coverage output in `api/tests/coverage`.
- The verified API validation command is `docker compose -f compose.dev.yaml exec api npm run test:unit`.
- `web/` now has a committed Node test suite rooted at `web/tests` for route, template, bundle-contract, and UI-state coverage.
- `web/package.json` defines `npm test` and `npm run build`.
- The practical automated web validation path is `docker compose -f compose.dev.yaml exec web npm test`, plus `docker compose -f compose.dev.yaml exec web npm run build` when assets changed.
- The web suite already supports three stable shapes: pure helper/contract tests, `jsdom` plus VM workflow tests, and spawned Express route/template checks.
- Manual validation is still required for browser-only interaction work, but it is no longer the default for SSR, template, or many client contract checks.
- For frontend interaction changes, manual validation should include a real browser pass over the affected page, not only a compile or static DOM review.
- The maintained route-level browser smoke path lives in [references/browser-smoke-checklist.md](references/browser-smoke-checklist.md); use it as the default manual pass for `/`, `/login`, `/week`, and `/dashboard` before adding task-specific notes.
- For skeptical frontend review or bug-finding work, pair this skill with [../frontend-bug-review/SKILL.md](../frontend-bug-review/SKILL.md).

## Web Test Design

- Match the narrowest honest harness to the frontend change.
- Prefer pure module assertions for query parsing, filter normalization, sorting, formatting, permission helpers, and other deterministic helpers.
- Prefer `jsdom` plus VM tests when the change lives in page boot logic, DOM mutations, tabs, modals, submit order, storage-aware helpers, or callback wiring.
- Prefer spawned web-server tests when the contract lives in SSR route output, template variables, bundle tags, or checked-in HTML shell structure.
- Prefer edge cases that can realistically regress in this repo: partial query strings, default date hydration, redirect sanitization, dashboard role or hidden-state logic, empty/error/busy states, and `datetime-local` to ISO conversion.
- Do not add large snapshot-heavy tests when a smaller semantic assertion can prove the contract.

## Workflow

1. Identify which service owns the behavior change: `api/`, `web/`, or both.
2. Check whether the touched service already has automated tests or whether the task is also adding a small service-local harness.
3. Choose the validation path using [references/testing-decision-tree.md](references/testing-decision-tree.md).
4. For API behavior changes, add or update Jest unit tests under `api/tests/unit` alongside the production code change.
5. For web behavior changes covered by the existing suite, add or update the relevant tests under `web/tests` alongside the production code change, using the smallest honest harness for the behavior.
6. Run the relevant commands and checks from [references/validation-commands.md](references/validation-commands.md).
7. For frontend interaction changes, open the affected page in a browser session and exercise the changed controls or flows, starting from [references/browser-smoke-checklist.md](references/browser-smoke-checklist.md) when the work touches `/`, `/login`, `/week`, or `/dashboard`.
8. Fix failures and rerun the validated scope until it passes with no failing tests.
9. Finish with explicit reporting:
   - tests or commands run
   - manual checks performed
   - remaining gaps or unvalidated risk

## Done Criteria

A behavior-changing task is complete only when:

- the implementation is in place,
- automated tests were updated and run when they existed or were intentionally bootstrapped,
- API tasks updated the Jest unit suite for both common and edge-case behavior when the API code changed,
- web tasks updated the committed `web/tests` coverage when the touched behavior already had route, template, helper, workflow, or contract assertions,
- API test execution finished with `100%` passing tests,
- relevant web test execution finished with `100%` passing tests,
- otherwise the manual validation checklist was executed for the touched flow,
- any web asset change was rebuilt through the repo's real workflow,
- frontend interaction changes were checked in a real browser session when the environment made that possible, and the absence of that pass was called out plainly when it was not,
- and the final report calls out remaining coverage or environment gaps plainly.
