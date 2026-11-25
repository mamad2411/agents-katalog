---
name: sveltekit-testing
description: Use when writing or reviewing tests for SvelteKit applications including Vitest unit tests for load functions and actions, Playwright end-to-end tests, and the @sveltejs/kit/testing adapter for component testing with routing context.
---

# SvelteKit Testing

## Specialization

Expert guidance for testing SvelteKit applications. Covers Vitest unit testing for server load functions, form actions, and hooks; the `@sveltejs/kit/testing` adapter for testing components that depend on routing context; Playwright end-to-end testing with `@sveltejs/kit`-aware fixtures; mocking `event.locals`, `event.cookies`, and `event.fetch`; and test organisation patterns for SvelteKit project layouts.

## Trigger Conditions

- Writing a unit test for a SvelteKit server load function, form action, or hook.
- Testing a Svelte component that imports from `$app/state`, `$app/navigation`, or `$app/stores`.
- Setting up end-to-end tests with Playwright for a SvelteKit application.
- Mocking `event.locals.user` or `event.cookies` in a test.
- Diagnosing a test that works locally but fails in CI due to SvelteKit-specific module resolution.
- Structuring a test suite that covers routing, data loading, and form submission end-to-end.

## Scope Boundaries

In scope:

- Vitest configuration for SvelteKit: `vite.config.ts` test block, `@sveltejs/kit/vite` plugin compatibility.
- Unit testing server load functions: constructing a mock `RequestEvent`, asserting on the returned data.
- Unit testing form actions: constructing a mock `RequestEvent` with `request.formData()`, asserting `fail()` and `redirect()` outcomes.
- Unit testing hooks: calling the `handle` function with a mock event and asserting `locals` mutations.
- `@sveltejs/kit/testing` adapter: `render` with routing context, `$app/state` mock support.
- Playwright end-to-end tests: `@playwright/test` setup with SvelteKit dev server, page navigation, form submission, authentication flows.
- `vi.mock('$env/static/private', ...)` pattern for mocking environment variables in unit tests.
- `vi.mock('$app/state', ...)` and `vi.mock('$app/navigation', ...)` for mocking SvelteKit virtual modules.
- Test file placement conventions in SvelteKit projects.
- Coverage configuration with `@vitest/coverage-v8`.

Out of scope:

- Svelte component unit testing unrelated to SvelteKit routing (covered by Svelte's own testing docs).
- Load testing or performance benchmarking.
- Contract testing between SvelteKit and external APIs.
- CI pipeline configuration — covered by `ci-cd-workflows`.

## Inputs

- What is being tested (load function, action, hook, component, or end-to-end flow).
- Test framework preference (Vitest only, or Vitest + Playwright).
- Authentication or `locals` requirements in the test scenario.
- Environment variable dependencies in the code under test.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Vitest configuration | `vite.config.ts` test block with correct SvelteKit plugin and environment settings |
| Unit test for load function | Mock `RequestEvent` construction; assertions on returned data and error cases |
| Unit test for action | Mock `request.formData()`; assertions on `fail()`, `redirect()`, and success outcomes |
| E2E test scaffold | Playwright config targeting SvelteKit dev server; at least one full page flow tested |
| Testing quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Unit test a single server load function | Mock `RequestEvent` created; load function returns expected data under test |
| L2 Practical Delivery | Full unit test suite for load + action + hook | All three layers tested; mocks for `locals`, `cookies`, and `env` in place |
| L3 Specialist Hardening | Component tests with routing context and E2E tests | `@sveltejs/kit/testing` adapter used; Playwright covers at least one authenticated flow |
| L4 Expert Standardisation | Project-wide test strategy with coverage targets and CI integration | Coverage thresholds configured; test utilities extracted; CI runs all suites |

## Workflow

1. Install dependencies: `vitest`, `@vitest/coverage-v8`, `@sveltejs/kit` (includes `@sveltejs/kit/testing`), `@playwright/test`.
2. Configure Vitest in `vite.config.ts`: add a `test` block with `environment: 'jsdom'` (or `'node'` for server-only tests), include the `@sveltejs/kit/vite` plugin, and set `globals: true`.
3. To unit test a **server load function**: import it directly; construct a mock `RequestEvent` with at minimum `params`, `url`, `locals`, `cookies` (as `vi.fn()` objects), and a mock `fetch`; call the function and assert on its return value.
4. To unit test a **form action**: import the action; construct a mock `RequestEvent` with a `request` whose `formData()` returns a `FormData` object; assert on `fail()` being returned for invalid input and on redirect or data being returned for success.
5. To unit test a **hook** (`handle`): import the handle function; construct a mock `RequestEvent` and a `resolve` spy; call `handle({ event, resolve })`; assert `locals` was mutated and `resolve` was called (or not, for short-circuit flows).
6. Mock SvelteKit virtual modules using `vi.mock`:
   - `vi.mock('$env/static/private', () => ({ MY_SECRET: 'test-value' }))` for env vars.
   - `vi.mock('$app/state', () => ({ page: { url: new URL('http://localhost/'), params: {} } }))` for routing state.
7. To test components that use `$app/state` or `$app/navigation`, use `@sveltejs/kit/testing` `render` which provides the full SvelteKit module context without a browser.
8. For Playwright E2E tests: configure `playwright.config.ts` with `webServer: { command: 'npm run build && npm run preview', port: 4173 }`; write tests using `page.goto`, `page.fill`, `page.click`, and `expect(page)` assertions.
9. For authenticated E2E flows, use Playwright's `storageState` to persist a login session across tests; do not re-login in every test.
10. Run the testing quality checklist.

## Testing Quality Checklist

- [ ] Vitest `environment` is set correctly: `'node'` for server-only tests, `'jsdom'` for component tests.
- [ ] All server load function tests construct a complete mock `RequestEvent`; no real cookies or environment variables are used.
- [ ] Form action tests assert on both the failure path (`fail()`) and the success path.
- [ ] Hook tests assert both that `locals` is mutated and that `resolve` is called with the correct event.
- [ ] `vi.mock('$env/static/private', ...)` is used for any test that imports code dependent on private env vars.
- [ ] No test imports from `$env/static/private` directly without mocking; this will fail in jsdom environments.
- [ ] Playwright tests target a built preview server, not `dev` mode, to test realistic behaviour.
- [ ] Authentication state is set up once per Playwright test project using `storageState`, not repeated in each test.
- [ ] Coverage thresholds are configured and enforced in CI; uncovered critical paths (auth, data mutation) are blocked.
- [ ] Tests are co-located with the code they test or placed in `src/tests/`; no stray test files at the project root.

## Security Notes

- Never use real production credentials, API keys, or database connections in unit tests. Mock all external dependencies.
- Playwright E2E tests that test authentication should use dedicated test accounts, not production user accounts.
- Test environment secrets (test API keys) must be stored as CI secrets, not committed to the repository.
- Do not snapshot or log response bodies that may contain sensitive data in Playwright traces or test reports.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Vitest setup | Workflow steps 1–2 |
| Load function unit test | Workflow step 3 |
| Form action unit test | Workflow step 4 |
| Hook unit test | Workflow step 5 |
| Virtual module mocking | Workflow step 6 |
| Component testing with routing context | Workflow step 7 |
| Playwright E2E setup | Workflow step 8 |
| Authenticated E2E flows | Workflow step 9 |
| Security | Security Notes + checklist |
| Quality validation | Testing Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
