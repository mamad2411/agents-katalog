# Playwright UI Testing

## Purpose
Automate user-visible web workflows with resilient semantic selectors, isolated fixtures, and cross-browser coverage: end-to-end checkout, auth, and CRUD flows that stay green through refactors and run in sharded CI with trace evidence on every failure.

## Use when
- Covering login, signup, checkout, onboarding, or settings flows that real users click through.
- Building a regression suite over critical paths with Chromium, Firefox, and WebKit parity.
- Stabilizing flaky suites via semantic locators, deterministic fixtures, and network control.
- Debugging CI-only failures with traces, videos, and step-level screenshots.

## Do not use when
- Testing game-engine UI outside a browser DOM (use `game-ui-testing`).
- Contract-testing APIs without rendering pages (use `api-contract-testing`).
- Writing unit or component tests that never launch a browser (use `testing-quality`).

## Required context
- Application base URL per environment (e.g., preview deploys, staging at `staging.shopdemo.internal`) and seeded test accounts.
- Playwright version and runner config (e.g., Playwright 1.49, `playwright.config.ts` with 3 projects, 4 shards).
- Fixture strategy: API-seeded database state vs UI-created state, and test-data cleanup policy.
- Flake budget and quarantine policy (e.g., under 2% flake rate, quarantine after 3 consecutive failures).

## Procedure
1. **Locate semantically**: Prefer `getByRole('button', { name: 'Place order' })`, then `getByLabel`, then `data-testid`; assert the strict-mode violation detector stays silent (exactly one match). XPath and CSS positional selectors (`.row > div:nth-child(3)`) are forbidden in new tests.
2. **Isolate with fixtures**: Seed orders, carts, and users via API fixtures in `test.beforeEach` (`api.createOrder({ sku: 'SKU-8842', qty: 2 })`); each test owns its data and deletes it in `afterEach`. Shared mutable staging data is prohibited.
3. **Synchronize deterministically**: Replace fixed sleeps with `expect(locator).toBeVisible()`, `page.waitForResponse(/\/api\/orders/)`, or `toHaveURL(/confirmation/)`; any `waitForTimeout` above 500 ms requires a code comment naming the external dependency.
4. **Cover the matrix**: Run the suite on Chromium, Firefox, and WebKit projects; shard 4 ways in CI (`--shard=1/4`) with automatic retries capped at 2 for network-identified flakes only, and record per-project pass rates.
5. **Capture failure evidence**: Enable trace-on-first-retry, screenshot-on-failure, and video-on-retry; upload `trace.zip` artifacts keyed by test title and shard so any red CI run opens directly in Trace Viewer.
6. **Gate and verify**: Enforce the flake budget (under 2% across 50 runs of the nightly stability job), quarantine chronic failures with owner and expiry date, and run `scripts/verify.sh` to confirm artifact completeness.

## Decision rules
- **Semantic selectors first**: Role, label, placeholder, text, test-id — in that order; positional CSS and XPath need written justification.
- **No shared mutable state**: Tests that depend on another test's leftovers fail review regardless of green runs.
- **Retries never exceed 2**: A test needing more retries is quarantined and fixed, not retried harder.
- **Flake budget is a release gate**: Suites above 2% flake block promotion to the release branch.
- **Every failure opens in Trace Viewer**: A red run without trace, screenshot, or video evidence is an incomplete report.

## Evidence required
- Full suite report across Chromium, Firefox, and WebKit with per-project pass rates and durations.
- Nightly 50-run stability report proving flake rate under 2%.
- Trace/screenshot/video artifacts linked for every failure in the verification window.
- Completed `templates/playwright-ui-spec.md` with flow inventory and verdicts.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Playwright suite with semantic locators, API fixtures, and sharded CI configuration.
- Flow specification document with coverage matrix and stability verdicts.
- Failure-evidence bundle (traces, screenshots, videos) retained per the artifact policy.

## Stop conditions
- All inventoried critical flows pass on all three browsers with flake rate under budget.
- Zero unquarantined failures; quarantined items carry owner and expiry date.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to frontend owners when missing roles, labels, or test-ids force brittle selectors across many tests (accessibility remediation needed).
- Escalate to backend owners when API fixtures cannot seed required states (missing test endpoints or data constraints).
- Escalate immediately on auth-session leaks between tests or PII appearing in trace artifacts.
