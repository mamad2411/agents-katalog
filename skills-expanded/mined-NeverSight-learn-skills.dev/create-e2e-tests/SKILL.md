---
name: create_e2e_tests
description: "Spec-driven E2E test creation: plan what to test through structured discovery phases, then scaffold a local Shiplight test project and write YAML tests by walking through the app in a browser."
---

# Create Local YAML Tests

A spec-driven workflow that front-loads testing expertise through structured planning before any tests are written. Tests run with `npx shiplight test --headed` — no cloud infrastructure required.

## When to use

Use `/create_e2e_tests` when the user wants to:
- Create a new local test project from scratch
- Add YAML tests for a web application
- Set up authentication for a test project
- Plan what to test before writing tests

## Principles

1. **Always produce artifacts.** Every phase writes a markdown file. Artifacts clarify your own thinking, give the user something to review, and guide later phases. When the user provides detailed requirements, use them as source material — skip questions already answered, but still produce the artifact.

2. **Confirm before implementing.** Present the spec (Phase 2 checkpoint) for user confirmation before spending time on browser-walking and test writing. Echo back your understanding as structured scenarios to catch mismatches early.

3. **Each phase reads the previous phase's artifact.** Discover feeds Specify, Specify feeds Plan, Plan feeds Implement, Implement feeds Verify. If an artifact exists from a prior run, offer to reuse it.

4. **Escalate, don't loop.** When something fails or is ambiguous, report it and ask the user rather than retrying silently.

## Phase Overview

```
Phase 1: Discover  → test-strategy.md    (understand the app & user goals)
Phase 2: Specify   → test-spec.md        (define what to test in Given/When/Then)
Phase 3: Plan      → test-plan.md        (prioritize, structure, per-test guidance)
Phase 4: Implement → *.test.yaml files   (setup project, write tests, run them)
Phase 5: Verify    → updated spec files  (coverage check, reconcile spec ↔ tests)
```

## Fast-Track

Check for existing artifacts before starting. The only way to skip artifact generation is if the user **explicitly** says so.

| Situation | Behavior |
|-----------|----------|
| User explicitly says "skip to implement" or "just write the tests" | Phase 4 only |
| Existing `test-specs/test-strategy.md` | Offer to reuse, skip Phase 1 |
| Existing `test-specs/test-spec.md` | Offer to reuse, skip Phases 1-2 |
| Existing `test-specs/test-plan.md` | Offer to reuse, skip to Phase 4 |

---

## Phase 1: Discover

**Goal:** Understand the application, the user's role, and what matters most to test.

**Output:** `<project>/test-specs/test-strategy.md`

### Steps

1. **Get project path** — ask where to create the test project (e.g., `./my-tests`). All artifacts and tests will live here. Create the `test-specs/` directory.

   If cloud MCP tools are available (`SHIPLIGHT_API_TOKEN` is set), use the `/cloud` skill to fetch environments and test accounts — this can pre-fill the target URL and credentials.

2. **Silent scan** — before asking questions, gather context from what's available:
   - Codebase: routes, components, `package.json`, framework
   - Git branch diff (what changed recently)
   - Existing tests (what's already covered)
   - PRDs, docs, README files
   - Cloud environments (if cloud MCP tools available)

3. **Understand what to test** — ask the user what they'd like to test, then ask targeted follow-up questions (one at a time, with recommendations based on your scan) to fill gaps: risk areas, user roles, authentication, data strategy, critical journeys. Skip questions the user has already answered.

4. **Write `test-strategy.md`** containing:
   - **App profile**: name, URL, framework, key pages/features
   - **Risk profile**: what matters most, what's fragile
   - **Testing scope**: what's in/out, user roles to cover
   - **Data strategy**: how test data will be created and cleaned up
   - **Environment**: target URL, auth method, any special setup

---

## Phase 2: Specify

**Goal:** Define concrete test scenarios in structured Given/When/Then format, prioritized by risk. Surface ambiguities that would cause flaky or incomplete tests.

**Input:** reads `test-specs/test-strategy.md`

**Output:** `<project>/test-specs/test-spec.md`

### Steps

1. **Read** `test-strategy.md` to understand scope and priorities.

2. **Generate user journey specs** — for each critical journey, write:
   - **Title**: descriptive name (e.g., "New user signup with email verification")
   - **Priority**: P0 (must-have), P1 (should-have), P2 (nice-to-have)
   - **Preconditions**: what must be true before the test starts (Given)
   - **Happy path**: step-by-step actions and expected outcomes (When/Then)
   - **Edge cases**: at least 2 per journey (e.g., invalid input, timeout, empty state)
   - **Data requirements**: what test data is needed

3. **Review for testing risks** — scan each journey for issues that would cause flaky or incomplete tests: data dependencies, timing/async behavior, dynamic content, auth boundaries, third-party services, state isolation, environment differences. Add a **Testing Notes** section to each journey with identified risks and mitigations. If anything is ambiguous, ask the user (one at a time, with a recommended answer and impact statement).

4. **Write `test-spec.md`** with all journey specs.

5. **Checkpoint** — present a summary table for user review:

   | # | Journey | Priority | Steps | Edge Cases | Risks |
   |---|---------|----------|-------|------------|-------|
   | 1 | User signup | P0 | 5 | 3 | Timing |
   | 2 | ... | ... | ... | ... | ... |

   Ask: "Does this look right? Any journeys to add, remove, or reprioritize?"

   **Wait for user confirmation before proceeding.**

---

## Phase 3: Plan

**Goal:** Create an actionable implementation plan with per-test guidance.

**Input:** reads `test-specs/test-spec.md`

**Output:** `<project>/test-specs/test-plan.md`

### Steps

1. **Read** `test-spec.md`.

2. **Define test file structure** — map journeys to test files:
   ```
   tests/
   ├── auth.setup.ts          (if auth needed)
   ├── signup.test.yaml        (Journey 1)
   ├── checkout.test.yaml      (Journey 2)
   └── ...
   ```

3. **Set implementation order** — ordered by:
   - Dependencies first (auth setup before authenticated tests)
   - Then by priority (P0 before P1)
   - Then by risk (highest risk first)

4. **Per-test guidance** — for each test file, specify:
   - **Data strategy**: what data to create/use, cleanup approach
   - **Wait strategy**: where to use WAIT_UNTIL vs WAIT, expected loading points
   - **Flakiness risks**: specific things to watch for in this test

5. **Write `test-plan.md`**.

6. **Checkpoint** — present summary:
   > Ready to implement **N** test files. Shall I proceed?

---

## Phase 4: Implement

**Goal:** Set up the project and write all YAML tests guided by the plan.

**Input:** reads `test-specs/test-plan.md`

### Setup

Skip any steps already done (project exists, deps installed, auth configured).

1. **Configure AI provider** — check if the test project already has a `.env` with an AI API key. If not, ask the user to choose a provider:

   > To run YAML tests, I need an AI provider for resolving test steps. Which provider would you like to use?
   >
   > A) **Google AI** — `GOOGLE_API_KEY` ([Get key](https://aistudio.google.com/app/apikey)) — default model: `gemini-3.1-flash-lite-preview`
   > B) **Anthropic** — `ANTHROPIC_API_KEY` ([Get key](https://console.anthropic.com/settings/keys)) — default model: `claude-haiku-4-5`
   > C) **OpenAI** — `OPENAI_API_KEY` ([Get key](https://platform.openai.com/api-keys)) — default model: `gpt-5.4-mini`
   > D) **Azure OpenAI** — requires `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` — set `WEB_AGENT_MODEL=azure:<deployment>`
   > E) **AWS Bedrock** — uses AWS credential chain — set `WEB_AGENT_MODEL=bedrock:<model_id>`
   > F) **Google Vertex AI** — uses GCP Application Default Credentials — set `WEB_AGENT_MODEL=vertex:<model>`
   > G) **I already have it configured**

   After the user chooses, ask for their API key and save it to the test project's `.env` file. For A/B/C, the model is auto-detected from the key. For D/E/F, also save `WEB_AGENT_MODEL` with the appropriate `provider:model` prefix. Optionally, the user can set `WEB_AGENT_MODEL` to override the default model (e.g., `WEB_AGENT_MODEL=claude-sonnet-4-6`).

2. **Scaffold the project** — call `scaffold_project` with the absolute project path. This creates `package.json`, `playwright.config.ts`, `.env.example`, `.gitignore`, and `tests/`. Save the API key to `.env`.

3. **Install dependencies**:
   ```bash
   npm install
   npx playwright install chromium
   ```

4. **Set up authentication (if needed)** — follow the standard [Playwright authentication pattern](https://playwright.dev/docs/auth).

   Add credentials as variables in `playwright.config.ts`:

   ```ts
   {
     name: 'my-app',
     testDir: './tests/my-app',
     dependencies: ['my-app-setup'],
     use: {
       baseURL: 'https://app.example.com',
       storageState: 'tests/my-app/.auth/storage-state.json',
       variables: {
         username: process.env.MY_APP_EMAIL,
         password: { value: process.env.MY_APP_PASSWORD, sensitive: true },
         // otp_secret_key: { value: process.env.MY_APP_TOTP_SECRET, sensitive: true },
       },
     },
   },
   ```

   Standard variable names: `username`, `password`, `otp_secret_key`. Use `{ value, sensitive: true }` for secrets. Add values to `.env`.

   Write `auth.setup.ts` with standard Playwright login code. For TOTP, implement RFC 6238 using `node:crypto` (HMAC-SHA1 + base32 decode) — no third-party dependency needed.

   **Verify auth before proceeding.** Run `npx shiplight test --headed` to execute the auth setup and confirm it saves `storage-state.json`. If it fails, escalate to the user — auth is a prerequisite for everything else.

   If the test plan involves special auth requirements (e.g., one account per test, multiple roles), confirm the auth strategy with the user before proceeding.

### Write tests

For each test in the plan (or each test the user wants):

1. **Open a browser session** — call `new_session` with the app's `starting_url`.
2. **Walk through the flow** — use `inspect_page` to see the page, then `act` to perform each action. This captures locators from the response.
3. **Capture locators** — use `get_locators` for additional element info when needed.
4. **Build the YAML** — construct the `.test.yaml` content following the best practices below.
5. **Save and validate** — write the `.test.yaml` file, then call `validate_yaml_test` with the file path to check locator coverage (minimum 50% required).
6. **Close the session** — call `close_session` when done.

**Important:** Do NOT write YAML tests from imagination. Always walk through the app in a browser session first to capture real locators. Tests without locators are rejected by `validate_yaml_test`.

When guided by `test-plan.md`:
- Apply the specified wait strategy at loading points
- Cover the edge cases and assertions defined in the spec

### Run tests

After writing all tests, run them:

```bash
npx shiplight test --headed
```

**When a test fails:**

1. **Report** — tell the user which test failed and why (one sentence).
2. **Classify** the failure:
   - **Implementation fix** (wrong locator, missing wait, timing) → fix and retry.
   - **Spec mismatch** (app behavior differs from spec) → ask the user whether to update the spec or skip the scenario.
3. **Escalate** if a fix doesn't work — don't keep retrying the same approach.

---

## Phase 5: Verify

**Goal:** Validate test coverage against the spec and reconcile any drift.

**Input:** reads `test-specs/test-spec.md`, `test-specs/test-plan.md`, and all `.test.yaml` files

This phase only runs when spec artifacts exist.

### Coverage check

For each spec journey, confirm the test covers the happy path and all listed edge cases.

Present a coverage summary:

| Spec Journey | Priority | Scenarios Specified | Tests Written | Coverage |
|-------------|----------|--------------------:|-------------:|----------|
| User signup | P0 | 4 | 4 | ✓ |
| Checkout | P0 | 3 | 2 | ✗ — edge case "empty cart" not covered |

Flag gaps and extras (test steps not in the spec).

### Reconcile

Update spec artifacts to match what was actually implemented:

1. **Update `test-spec.md`** — mark skipped scenarios with reason, add scenarios that emerged during implementation, update edge cases to reflect what was tested
2. **Update `test-plan.md`** — correct file structure, note deviations from the original plan
3. **Show diff summary** — tell the user what changed and why

This keeps artifacts accurate for future test maintenance and expansion.

---

## YAML Format Reference

Read the MCP resource `shiplight://yaml-test-spec-v1.3.0` for the full language spec (statement types, templates, variables, suites, hooks, parameterized tests).

Read the MCP resource `shiplight://schemas/action-entity` for the full list of available actions and their parameters.

## YAML Authoring Best Practices

These best practices bridge the YAML language spec and the action catalog to help you write fast, reliable tests.

### Statement type selection

- **ACTION is the default.** Capture locators via MCP tools (`act`, `get_locators`) during browser sessions, then write ACTION statements. ACTIONs replay deterministically (~1s).
- **DRAFT is a last resort.** Only use DRAFT when the locator is genuinely unknowable at authoring time. DRAFTs are slow (~5-10s each, AI resolution at runtime). Tests with too many DRAFTs are rejected by `validate_yaml_test`.
- **VERIFY for assertions.** Use `VERIFY:` for all assertions. Do not write assertion DRAFTs like `"Check that the button is visible"`.
- **URL for navigation.** Use `URL: /path` for navigation instead of `action: go_to_url`.
- **CODE for scripting.** Use `CODE:` for network mocking, localStorage manipulation, page-level scripting. Not for clicks, assertions, or navigation.

### The `intent` field

`intent` is the **intent** of the step — it defines _what_ the step should accomplish. The `action`/`locator` or `js` fields are **caches** of _how_ to do it. When a cache fails (stale locator, changed DOM), the AI agent uses `intent` to re-inspect the page and regenerate the action from scratch.

Because `intent` drives self-healing, it must be specific enough for an agent to act on without any other context. Describe the **user goal**, not the DOM element — avoid element indices, CSS selectors, or positional references that break when the UI changes:

```yaml
# BAD: vague, agent can't re-derive the action
- intent: Click button

# BAD: tied to DOM structure that can change
- intent: Click the 3rd button in the form
- intent: Click element at index 42

# GOOD: describes the user goal, stable across UI changes
- intent: Click the Submit button to save the new project
  action: click
  locator: "getByRole('button', { name: 'Submit' })"
```

### ACTION: structured format vs `js:` shorthand

**Use structured format by default** for all supported actions. Read the MCP resource `shiplight://schemas/action-entity` for the full list of available actions and their parameters.

**Use `js:` only when the action doesn't map to a supported action** — e.g., complex multi-step interactions, custom Playwright API calls, or chained operations:

```yaml
- intent: Drag slider to 50% position
  js: "await page.getByRole('slider').first().fill('50')"

- intent: Wait for network idle after form submit
  js: "await page.waitForLoadState('networkidle')"
```

### `js:` coding rules

- Always resolve locators to a single element (e.g., `.first()`, `.nth(1)`) to avoid Playwright strict-mode errors
- Always include `{ timeout: 5000 }` on actions for predictable timing
- The `intent` is critical — it's the input for self-healing when `js` fails
- `page`, `agent`, and `expect` are available in scope

### VERIFY best practices

- Always set a short timeout (e.g., `{ timeout: 2000 }`) on `js:` assertions that have an AI fallback, so stale locators fall back to AI quickly instead of waiting the default 5s
- Always use `VERIFY:` shorthand — do not use `action: verify` directly
- **Be aware of false negatives with `js:` assertions.** The AI fallback only triggers when `js` **throws** (element not found, timeout). If `js` passes against the wrong element (stale selector matching a different element), the assertion silently succeeds — no fallback occurs. Keep `js:` assertions simple and specific to minimize this risk.

### IF/WHILE `js:` condition best practices

- **Use natural language (AI) conditions for DOM-based checks** (element visible, text present, page state). AI conditions self-heal against DOM changes; `js:` conditions are brittle and cannot auto-heal.
- **Use `js:` conditions only for counter/state logic** — e.g., `js: counter++ < 10`, `js: retryCount < 3`. Never use `js:` for DOM inspection like `js: document.querySelector('.modal') !== null`.
- If you need a JavaScript-based DOM check, use `CODE:` to evaluate it and store the result, or use `VERIFY:` with `js:` (which at least has AI fallback on failure).

### Waiting syntax

- **`WAIT_UNTIL:`** — AI checks the condition repeatedly until met or timeout. Default timeout is 60 seconds. Each AI check takes 5–10s, so set `timeout_seconds` to at least 15.
- **`WAIT:`** — fixed-duration pause. Use `seconds:` to set duration.

See [Smart waiting](#smart-waiting) in E2E Test Design for when to use each.

### General conventions

- Put `intent` first in ACTION statements for readability
- `xpath` is only needed when an ACTION has neither `locator` nor `js`.
- **Single-test vs Suite vs Parameters:**
  - **Single-test file** — one isolated test, no shared state
  - **Suite** — tests that have sequential dependencies (e.g., test A creates a file, test B consumes it). Each test in a suite still covers one journey — the suite just guarantees execution order and shares browser state. Do NOT use suites to bundle unrelated tests.
  - **Parameters** — same test structure, different data inputs

## E2E Test Design Best Practices

These principles govern *what* to test and *how to structure* tests — independent of the YAML format. Apply them during Phase 2 (Specify) and Phase 4 (Implement).

### Test isolation

Each test must run independently — never depend on another test's side effects, execution order, or leftover state. If a test needs data, it creates that data itself.

```yaml
# BAD: depends on a previous test having created "My Project"
test: Delete a project
steps:
  - URL: /projects
  - intent: Click on "My Project"
    action: click
    locator: "getByText('My Project')"
  - intent: Click the Delete button
    action: click
    locator: "getByRole('button', { name: 'Delete' })"

# GOOD: creates its own data, then tests the behavior
test: Delete a project
steps:
  - CODE:
    js: |
      const res = await page.request.post('/api/projects', {
        data: { name: 'Delete-Test-' + Date.now() }
      });
      const project = await res.json();
      save_variable('projectName', project.name);
  - URL: /projects
  - WAIT_UNTIL: The project list has loaded
  - intent: Click on the project we just created
    action: click
    js: "await page.getByText('{{projectName}}').click()"
  - intent: Click the Delete button
    action: click
    locator: "getByRole('button', { name: 'Delete' })"
  - VERIFY: The project is no longer visible in the list
```

### One journey per test

Each test should verify one logical user journey. If step 3 of 8 fails, steps 4-8 give you zero information. Split long flows into focused tests.

**Exception:** Suites allow sequential dependencies between tests (e.g., test A uploads a file, test B downloads it). Each test in a suite still covers one journey — the suite just guarantees order and shares browser state.

```yaml
# BAD: tests login, settings change, AND deletion in one test
test: Full user lifecycle
steps:
  - intent: Log in
  - intent: Navigate to settings
  - intent: Change display name
  - VERIFY: Name updated
  - intent: Navigate to account
  - intent: Delete account
  - VERIFY: Account deleted

# GOOD: separate tests, each verifiable in isolation
# File: update-display-name.test.yaml
test: Update display name from settings
steps:
  - URL: /settings
  - intent: Clear the display name field and type "New Name"
    action: fill
    locator: "getByLabel('Display name')"
    value: "New Name"
  - intent: Click Save
    action: click
    locator: "getByRole('button', { name: 'Save' })"
  - VERIFY: Success message "Settings saved" is visible

# File: delete-account.test.yaml (separate test)
test: Delete account from account page
steps:
  - URL: /account
  # ... focused on deletion only
```

### Assert what users see, not implementation details

Test visible outcomes — text, navigation, enabled/disabled states. Never assert CSS classes, data attributes, internal state, or DOM structure.

```yaml
# BAD: asserts implementation details
- VERIFY:
    js: |
      const el = await page.locator('.btn-primary');
      await expect(el).toHaveClass(/disabled/);
      await expect(el).toHaveAttribute('data-state', 'submitted');

# GOOD: asserts what a user would observe
- VERIFY: The Submit button is disabled
    js: |
      await expect(page.getByRole('button', { name: 'Submit' }))
        .toBeDisabled({ timeout: 2000 });
```

### Focused assertions

Verify the *one thing* that proves the feature works. Over-asserting makes tests brittle — they break on cosmetic changes unrelated to the behavior under test.

```yaml
# BAD: asserts every field on the page — breaks when any label changes
- VERIFY: Page title is "Dashboard"
- VERIFY: Welcome message shows username
- VERIFY: Sidebar has 5 menu items
- VERIFY: Footer shows current year
- VERIFY: Avatar image is loaded
- VERIFY: Notification bell is visible

# GOOD: asserts the one thing that proves the user landed on the dashboard
- VERIFY: Dashboard page shows the welcome message with the user's name
```

### Never test third-party services

Don't assert that Stripe's checkout, Google OAuth's consent screen, or Twilio's SMS delivery works. Mock external services at the network boundary. Test *your* integration, not their UI.

```yaml
# BAD: tests Stripe's UI (will break when Stripe updates their page)
- intent: Enter card number in Stripe iframe
- intent: Click Stripe's pay button
- VERIFY: Stripe shows success checkmark

# GOOD: mock the payment API, test your success handling
- CODE:
    js: |
      await page.route('**/api/payments', route =>
        route.fulfill({ status: 200, json: { status: 'succeeded', id: 'pi_mock' } })
      );
- intent: Click the Pay button
  action: click
  locator: "getByRole('button', { name: 'Pay' })"
- VERIFY: Order confirmation page shows "Payment successful"
```

### Deterministic test data

Use unique identifiers per test run to avoid collisions. Never rely on hardcoded data that other tests or users might modify.

```yaml
# BAD: hardcoded name — collides if tests run in parallel or data persists
- intent: Type "Test User" into the name field
  action: fill
  locator: "getByLabel('Name')"
  value: "Test User"

# GOOD: unique per run — no collisions
- CODE:
    js: "save_variable('testName', 'Test-User-' + Date.now());"
- intent: Type the generated name into the name field
  action: fill
  locator: "getByLabel('Name')"
  text: "{{testName}}"
```

### Prefer API seeding over UI setup

When a test needs preconditions (a user exists, a project is created), set them up via API calls — not by clicking through the UI. UI setup is slow, flaky, and not what you're testing.

```yaml
# BAD: 10 UI steps just to set up data before the real test
- URL: /projects/new
- intent: Type project name
- intent: Select team
- intent: Click Create
- WAIT_UNTIL: Project page loads
# ... now the actual test starts

# GOOD: API seed in one step, then test the real behavior
- CODE:
    js: |
      const res = await page.request.post('/api/projects', {
        data: { name: 'Seed-' + Date.now(), team: 'engineering' }
      });
      const { slug } = await res.json();
      save_variable('projectSlug', slug);
- URL: /projects/{{projectSlug}}/settings
- WAIT_UNTIL: Settings page has loaded
# ... test starts immediately at the point that matters
```

### Smart waiting

Use the right wait for the situation. `WAIT_UNTIL:` costs 5-10s per check (AI resolution), so it's overkill for short, predictable delays. `WAIT:` is fine when the delay is short and known. The anti-pattern is using `WAIT:` as a *substitute* for condition-based waiting when the delay is unpredictable.

```yaml
# BAD: guessing how long a data fetch takes — too short in CI, too long locally
- WAIT: Wait for data to load
  seconds: 5
- VERIFY: The table shows results

# GOOD: condition-based wait for unpredictable operations
- WAIT_UNTIL: The data table has at least one row visible
  timeout_seconds: 30

# ALSO GOOD: short WAIT for known, fast delays (animations, transitions, debounce)
- intent: Type search query
  action: fill
  locator: "getByRole('searchbox')"
  value: "test"
- WAIT: Wait for debounce to fire
  seconds: 1
- VERIFY: Search suggestions are visible
```

Rule of thumb: if the delay is **predictable and under 5s** (animation, debounce, transition), use `WAIT:`. If the delay is **unpredictable** (API call, data loading, file processing), use `WAIT_UNTIL:`.

### Test error states, not just happy paths

Real users hit errors. A test suite that only covers happy paths gives false confidence. For every critical journey, include at least one error/edge case test.

```yaml
# Covers: empty state, invalid input, network failure
test: Search handles no results gracefully
steps:
  - URL: /search
  - intent: Type a query that returns no results
    action: fill
    locator: "getByRole('searchbox')"
    value: "zzz_no_match_zzz"
  - intent: Submit the search
    action: click
    locator: "getByRole('button', { name: 'Search' })"
  - VERIFY: Empty state message "No results found" is displayed
  - VERIFY: The search box still contains the query (user can refine)
```

### Design for parallel execution

Tests that modify shared global state (e.g., site-wide settings, the only admin account) can't safely run in parallel. Design around this:

- Use unique, per-test data instead of shared fixtures
- Avoid tests that change global configuration
- If a test *must* modify shared state, document it and mark it for serial execution

### Flaky test policy

A test that passes on retry is still broken. Never add retries to mask flakiness — find and fix the root cause:

- **Timing flake?** → Add a proper `WAIT_UNTIL:` for the right condition
- **Data flake?** → Use unique test data, add proper cleanup
- **Order flake?** → The test has a hidden dependency on another test — make it self-contained
- **Environment flake?** → Mock the unstable external service

## Project Structure

```
my-tests/
├── test-specs/                   # Spec artifacts (version-controlled)
│   ├── test-strategy.md          # Phase 1: app & risk profile
│   ├── test-spec.md              # Phase 2: Given/When/Then scenarios
│   └── test-plan.md              # Phase 3: implementation plan
│
├── playwright.config.ts
├── package.json
├── .env                          # API keys + credentials (gitignored)
├── .gitignore
│
├── tests/
│   ├── public-app/               # No login needed
│   │   ├── search.test.yaml
│   │   └── filter.test.yaml
│   │
│   └── my-saas-app/              # Requires login
│       ├── auth.setup.ts         # Playwright login setup — you write this
│       ├── dashboard.test.yaml
│       └── settings.test.yaml
```

The `test-specs/` directory contains human-readable markdown artifacts that are version-controllable. Do NOT add `test-specs/` to `.gitignore`.

## Tips

- ACTION statements with locators replay ~10x faster than DRAFTs. Always prefer ACTIONs.
- Use `inspect_page` to understand page state. **Always read the DOM file first** — it provides element indices needed for `act` and consumes far fewer tokens. Only view the screenshot when you specifically need visual information (layout, colors, images), as screenshots consume significantly more tokens than DOM.
- Run a specific project's tests with: `npx shiplight test --headed my-saas-app/`
- The `.env` file is auto-discovered by `shiplightConfig()` — no manual dotenv setup needed.
