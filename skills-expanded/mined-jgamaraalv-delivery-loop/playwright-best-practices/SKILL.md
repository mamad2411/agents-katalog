---
name: playwright-best-practices
description: Write, debug, and maintain Playwright tests — flaky tests, Page Object Model, locators/waits, fixtures, network mocking, auth, CI/CD. Covers E2E, component, API, visual, a11y, and extension testing.
---

# Playwright Best Practices

Comprehensive guidance for Playwright test development — writing, debugging, and maintaining E2E, component, API, visual, accessibility, security, Electron, and extension tests. Every detail lives in the reference files below; this page only routes you to the right one.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

### `core/` — the foundation every test relies on

- `core/test-suite-structure.md` — organizing specs, suites, and API mocking baseline · read when scaffolding a new spec or structuring a suite.
- `core/locators.md` — stable, user-facing selectors (`getByRole`/`getByLabel`/`getByText`/`data-testid`) over brittle CSS/XPath · read when picking or fixing selectors.
- `core/assertions-waiting.md` — web-first assertions and auto-waiting instead of fixed timeouts · read when adding assertions, fixing timeouts, or removing explicit waits.
- `core/page-object-model.md` — POM structure and refactoring toward it · read when implementing or refactoring to Page Objects.
- `core/fixtures-hooks.md` — custom fixtures, `beforeEach`/`afterEach`, per-worker isolation · read when extracting setup/teardown or isolating data between workers.
- `core/test-data.md` — test-data factories and seeding · read when creating reusable test data.
- `core/configuration.md` — `playwright.config` setup · read when configuring a project.
- `core/annotations.md` — `skip`/`fixme`/`slow`, conditional execution, test steps · read when annotating or grouping tests for reporting.
- `core/test-tags.md` — `@smoke`/`@fast`/`@critical` tags and `--grep` filtering · read when tagging or running a subset of tests.
- `core/global-setup.md` — global setup & teardown · read when sharing one-time setup across the run.
- `core/projects-dependencies.md` — projects and project dependencies · read when wiring multi-project or dependent setups.

### `testing-patterns/` — what kind of test you're writing

- `testing-patterns/component-testing.md` — component tests · read when testing a component in isolation.
- `testing-patterns/api-testing.md` — API request testing · read when testing endpoints directly.
- `testing-patterns/graphql-testing.md` — GraphQL request/mocking · read when testing or mocking GraphQL.
- `testing-patterns/visual-regression.md` — screenshot/visual regression · read when adding visual snapshots.
- `testing-patterns/canvas-webgl.md` — canvas/WebGL/chart testing · read when asserting on canvas-rendered UI.
- `testing-patterns/accessibility.md` — axe-core a11y testing · read when testing accessibility.
- `testing-patterns/security-testing.md` — XSS/CSRF/auth security tests · read when testing security surfaces.
- `testing-patterns/forms-validation.md` — form and validation flows · read when testing forms.
- `testing-patterns/drag-drop.md` — drag-and-drop interactions · read when testing drag/drop.
- `testing-patterns/file-operations.md` + `testing-patterns/file-upload-download.md` — file upload/download · read when testing file I/O.
- `testing-patterns/i18n.md` — internationalization/locale testing · read when testing localized UI.
- `testing-patterns/electron.md` — Electron app testing · read when testing an Electron app.
- `testing-patterns/browser-extensions.md` — browser-extension testing · read when testing an extension.
- `testing-patterns/performance-testing.md` — performance budgets, Web Vitals, Lighthouse · read when asserting on performance.

### `advanced/` — complex flows, auth, and network

- `advanced/authentication.md` + `advanced/authentication-flows.md` — auth setup and complex flows (MFA, reset) · read when handling login/auth state.
- `advanced/network-advanced.md` — network interception, mocking, HAR record/playback · read when mocking responses or intercepting requests.
- `advanced/multi-context.md` — multi-tab/popup and OAuth popup flows · read when testing multiple tabs/contexts.
- `advanced/multi-user.md` — multiple users, roles, real-time collaboration · read when testing multi-user/role scenarios.
- `advanced/third-party.md` — OAuth/SSO, payments, email/SMS verification · read when integrating third-party services.
- `advanced/clock-mocking.md` — date/time mocking · read when testing time-dependent behavior.
- `advanced/mobile-testing.md` — device emulation, touch gestures, viewport/breakpoints · read when testing mobile/responsive layouts.

### `browser-apis/` — browser capabilities

- `browser-apis/browser-apis.md` — geolocation, permissions, clipboard, camera/microphone mocking · read when testing browser APIs.
- `browser-apis/websockets.md` — WebSocket/real-time testing · read when testing live connections.
- `browser-apis/iframes.md` — iframe testing · read when interacting with iframes.
- `browser-apis/service-workers.md` — service workers, PWA, offline-first · read when testing SW/PWA behavior.

### `debugging/` — when a test fails or flakes

- `debugging/debugging.md` — trace viewer, error context, general debugging · read when investigating any failure.
- `debugging/flaky-tests.md` — flakiness, race conditions, isolation, state leaks, parallel-run flakiness · read when a test is flaky.
- `debugging/console-errors.md` — console/JS error monitoring, fail-on-console-error · read when watching console output.
- `debugging/error-testing.md` — error boundaries, network failures, offline, loading/validation states · read when testing error/edge cases.

### `architecture/` — choosing the right approach

- `architecture/pom-vs-fixtures.md` — POM vs fixtures decision · read when deciding how to structure shared logic.
- `architecture/test-architecture.md` — test-type selection · read when planning what to test at which level.
- `architecture/when-to-mock.md` — mock vs real services · read when deciding to mock or hit the real thing.

### `frameworks/` — framework-specific guidance

- `frameworks/react.md` · `frameworks/angular.md` · `frameworks/vue.md` · `frameworks/nextjs.md` — read the one matching the app under test.

### `infrastructure-ci-cd/` — running tests at scale

- `infrastructure-ci-cd/ci-cd.md` — CI/CD pipeline setup · read when wiring tests into CI.
- `infrastructure-ci-cd/github-actions.md` · `infrastructure-ci-cd/gitlab.md` · `infrastructure-ci-cd/other-providers.md` — provider-specific CI config · read for your provider.
- `infrastructure-ci-cd/docker.md` — containerized runs · read when running in Docker.
- `infrastructure-ci-cd/parallel-sharding.md` — parallel execution and sharding · read when scaling out the run.
- `infrastructure-ci-cd/performance.md` — test-suite performance and worker isolation · read when speeding up the suite.
- `infrastructure-ci-cd/test-coverage.md` — coverage collection · read when measuring coverage.
- `infrastructure-ci-cd/reporting.md` — reporters and artifacts · read when configuring reports/artifacts.

## Validation loop

After writing or modifying tests: run `npx playwright test --reporter=list`; on failure, inspect the trace (`npx playwright show-trace`), fix locators/waits/assertions, and re-run; only proceed when green; for critical tests, confirm stability with `npx playwright test --repeat-each=5`.
