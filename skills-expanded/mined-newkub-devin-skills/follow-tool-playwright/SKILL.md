---
name: follow-tool-playwright
description: Install and set up Playwright for E2E testing
argument-hint: "[scope]"
related:
  - use-agent-browser
  - use-chrome-devtools
  - use-astgrep
  - follow-tool-aube
  - follow-tool-usage
  - follow-best-practice
  - setup-cicd
  - run-test

---

## Goal

Set up Playwright as the main E2E testing framework for a web project

## Scope

Install and configure Playwright for end-to-end testing in single projects and monorepos

- Use this skill for a real browser E2E suite — for a quick check/smoke without building a suite, use `/use-agent-browser` (CLI/record) or `/use-chrome-devtools` (inspect/debug via the registered MCP) as a stopgap — choose per `/use-chrome-devtools` `## Tool Selection`
- For API mocking in unit/integration tests → use `/follow-lib-mswjs` instead

- Latest: `@playwright/test@1.63.0` (verified 2026-09-13)

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

| Topic | Workflow |-------|----------| setup | `workflows/setup-playwright/SKILL.md` — install, browsers install, basic config | config | `workflows/config-projects/SKILL.md` — projects, devices, baseURL, retries, reporters | migrate | `workflows/migrate-from-cypress/SKILL.md` — cypress→playwright API mapping, page objects, verify 
1. If the argument matches a topic → read and follow `workflows/<name>/SKILL.md` instead of the steps below
2. Otherwise → follow the steps below as normal

### 1. Installation

> Goal: install Playwright and browsers

1. Install Playwright with `bun add -D @playwright/test`
2. Run `bunx playwright install` to install browsers
3. Install the VS Code extension for IDE integration
4. Add a test script in `package.json`
5. Check the Node.js version (>= v20.0.0 — Node 18 is no longer supported)
6. Always update Playwright to the latest version with `bun add -D @playwright/test@latest`

### 2. Configuration

> Goal: create playwright.config.ts with browsers and options

1. Create `playwright.config.ts` at the root
2. Configure browsers (chromium, firefox, webkit) via `projects`
3. Set `testDir` for the test files location
4. Set `timeout` for test execution (default 30,000ms)
5. Set `retries: process.env.CI ? 2 : 0` for flaky tests
6. Set `workers: process.env.CI ? 4 : undefined` for parallel execution
7. Set `fullyParallel` for parallel tests within files
8. Set `trace: 'on-first-retry'` for debugging
9. Set `screenshot: 'only-on-failure'` for failure artifacts
10. Set `reporter` to `html` for local and `blob` for CI sharding
11. Set `forbidOnly: !!process.env.CI` to prevent `test.only` in CI
12. Set `webServer: { command, url, reuseExistingServer: !process.env.CI }` so Playwright starts the dev server itself

### 3. Monorepo Setup

> Goal: configure Playwright for monorepo workspaces

1. Set `testDir` per workspace
2. Use the workspace protocol for internal dependencies
3. Set `--project` to run tests on a specific workspace
4. Use shared fixtures across workspaces
5. Set config extends from the root config

### 4. Writing Tests

> Goal: write E2E tests following best practices

1. Use `test` from `@playwright/test`
2. Use the `page` fixture for browser automation
3. Use `expect` for auto-waiting web-first assertions
4. Organize test files by features or pages
5. Use `test.describe` for grouping related tests
6. Use `test.beforeEach`, `test.afterEach` for setup/teardown
7. Use `test.describe.configure({ mode: 'parallel' })` for parallel tests in a file
8. Use `test('name', { lock: 'shared-resource' }, ...)` (v1.63+) when tests share one resource — tests with the same lock name never run concurrently

### 5. Page Object Model

> Goal: use the Page Object Model for reusable code

1. Create Page Object classes for each page
2. Separate selectors and actions from test files
3. Use locators instead of legacy selectors
4. Use `page.locator()` for element selection
5. Use `waitFor()` for waiting strategies

### 6. Locators Strategy

> Goal: pick resilient and maintainable locators

1. Use `getByRole()` for role-based selectors (preferred)
2. Use `getByText()` for text-based selectors
3. Use `getByLabel()` for form elements
4. Use `getByTestId()` for test IDs (only when role/text won't work)
5. Avoid fragile CSS selectors
6. Use `codegen` to generate resilient locators
7. Use locator chaining and filtering to narrow down
8. Use `locator.visible()` (v1.63+) instead of the `:visible` CSS pseudo-class
9. Use `page.frameLocator()` without a selector to search elements across all frames (v1.63+)

### 7. Assertions And Matchers

> Goal: use auto-waiting web-first assertions

1. Use `expect(page).toHaveURL()` for URL assertions
2. Use `expect(locator).toBeVisible()` for visibility
3. Use `expect(locator).toHaveText()` for text content
4. Use `expect(locator).toHaveCount()` for element count
5. Use `expect(apiResponse).toBeOK()` for API assertions
6. Use `expect(locator).toMatchAriaSnapshot()` for accessibility tree verification

### 8. Authentication Setup

> Goal: set up authentication reuse via storageState

1. Create a setup project that logs in once
2. Save the `storageState` to disk
3. Use the `storageState` in the main project so every test starts authenticated
4. Use project `dependencies` to run setup before main tests
5. Use `BrowserContext.setStorageState()` to clear and set new state

### 9. Running Tests And All-Routes Coverage

> Goal: run tests with CLI options and cover every route

1. Run tests with `bunx playwright test`
2. Run tests in headed mode with `--headed`
3. Run tests in debug mode with `--debug`
4. Run tests on a specific browser with `--project`
5. Run tests in UI mode with `--ui` for authoring and debugging
6. Use `--last-failed` to re-run only failed tests
7. List routes from `/report-uxui-all-routes` or route config/filesystem routes
8. Create a smoke spec that visits every route and asserts: page load 200, no console errors, no uncaught page errors
9. For critical routes → write a dedicated spec with interaction tests (click, form submit, navigation)
10. If there's no suite yet and you just need a quick check → use `agent-browser` headless (`agent-browser open <url>` + `snapshot -i` + `console`/`errors`) or `chrome-devtools-mcp` (`new_page` + `take_snapshot` + `list_console_messages`) as a stopgap instead of a temporary Playwright suite
11. Track route gaps — a route without a test must be recorded

### 10. CI/CD Integration

> Goal: configure Playwright in the CI/CD pipeline

1. Install browsers in the CI pipeline with `bunx playwright install`
2. Use `--shard=x/y` for parallel execution across machines
3. Set `retries` for the CI environment
4. Use the `blob` reporter for sharding and `bunx playwright merge-reports` to combine
5. Upload test reports as CI artifacts
6. Use GitHub Actions with `reuseExistingServer: true`
7. Use `await using` syntax for async disposables and auto cleanup

## Rules

### 1. Configuration Requirements

A config file at the root is required:

- `playwright.config.ts` must exist at the root
- Use `bun add -D @playwright/test` for installation
- Run `bunx playwright install` to install browsers
- Set `testDir` explicitly
- Set `fullyParallel` for parallel execution
- Set `trace: 'on-first-retry'` for debugging
- Set `screenshot: 'only-on-failure'` for failure artifacts
- Use the `reporter` appropriate for the environment (`html` local, `blob` CI)

### 2. Test Organization

Organize test files:

- Arrange test files by features or pages
- Use `test.describe` for grouping related tests
- Use clear, descriptive test names
- Use `test.beforeEach`, `test.afterEach` for isolated tests
- Use the Page Object Model for reusable code

### 3. Selectors Strategy

Use selectors properly:

- Use `getByRole()` as the preferred locator
- Use `getByText()`, `getByLabel()` for user-facing attributes
- Use `getByTestId()` only when role/text is not enough
- Avoid fragile CSS selectors
- Use `codegen` to generate locators

### 4. Best Practices

Follow best practices:

- Use Playwright's auto-waiting (don't use `page.waitForTimeout()`)
- Use auto-waiting web-first assertions
- Use the Page Object Model for maintainability
- Use fixtures for shared setup
- Use `fullyParallel` for performance
- Use the `request` fixture to seed data via API, not UI
- Use `storageState` for authentication reuse
- Avoid conditional logic (`if`, `try/catch`) in tests
- Always keep the Playwright version up to date

### 5. CI/CD

- Use `--shard=x/y` to split tests across CI machines
- Use the `blob` reporter for sharding and `merge-reports` to combine
- Set `forbidOnly: !!process.env.CI` to prevent `test.only`
- Use `reuseExistingServer: true` for local iteration speed
- Install only the necessary browsers in CI

- Use /use-agent-browser if needed
- Use /use-chrome-devtools if needed
- Use /use-astgrep if needed
- Use /follow-tool-aube if needed
- Use /follow-tool-usage if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /deep-test e2e if needed

## References

- [CLI reference](references/cli.md)
- Use /run-test if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Playwright installed and working
- Config supports browsers, parallelism, and monorepo
- All E2E tests run
- Compliant with best practices from the Playwright 2026 official documentation

