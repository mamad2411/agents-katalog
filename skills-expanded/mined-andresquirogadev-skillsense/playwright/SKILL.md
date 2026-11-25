# Playwright Skill

You are writing end-to-end tests with Playwright. Apply these conventions.

## Test Structure

- Each test file covers a user-facing feature or flow, not a single component.
- Use `test.describe` for grouping related flows.
- Use `test.beforeEach` to navigate to the starting URL rather than duplicating `page.goto()` in every test.
- Use Page Object Model (POM) for complex flows — create classes in `tests/pages/` that encapsulate selectors and actions.

## Selectors

- Prefer user-visible locators in priority order:
  1. `getByRole('button', { name: 'Submit' })` — semantic and accessible
  2. `getByLabel('Email')` — form inputs
  3. `getByTestId('submit-btn')` — use `data-testid` as a last resort for dynamic content
- Avoid CSS selectors and XPath — they couple tests to implementation details.
- Use `locator.filter({ hasText: '…' })` to narrow a locator.

## Assertions

- Use `expect(locator).toBeVisible()`, `toHaveText()`, `toHaveValue()` — these auto-retry until the condition passes or timeout.
- Avoid `waitForSelector` — `expect()` assertions include built-in waiting.
- Use `expect(page).toHaveURL('/dashboard')` after navigation.

## Network

- Mock API calls for unit-level e2e tests: `page.route('**/api/users', route => route.fulfill({ json: mockUsers }))`.
- Use `page.waitForResponse('**/api/submit')` to wait for network requests triggered by actions.

## Performance & Reliability

- Run tests in parallel by default (Playwright's default); use `test.describe.serial` only for tests with hard ordering dependencies.
- Always run tests against a local dev server; configure `webServer` in `playwright.config.ts`.
- Use `test.slow()` to extend the timeout for known slow tests instead of setting global timeouts high.
- Capture screenshots on failure: `use: { screenshot: 'only-on-failure' }` in config.

## playwright.config.ts

```ts
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  use: { baseURL: 'http://localhost:3000', trace: 'on-first-retry' },
  webServer: { command: 'npm run dev', url: 'http://localhost:3000', reuseExistingServer: !process.env.CI },
});
```
