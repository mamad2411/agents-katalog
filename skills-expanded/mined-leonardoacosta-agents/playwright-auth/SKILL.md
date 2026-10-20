---
name: playwright-auth
description: "Auth flow contract for Playwright E2E tests. Covers credential-based login, storage state persistence, POM vs fixture patterns, and multi-role auth across T3 Turbo projects. Triggers on: storageState, loginAs, auth fixture, multi-role login, e2e login."
allowed-tools: Bash
paths: ["packages/e2e/**"]
---


# Playwright Auth Flows

> Shared auth contract for Playwright E2E tests. Scope is strictly authentication --
> defer all other Playwright patterns to the `webapp-testing` skill.

## Auth Flow Contract

Every Playwright auth flow follows the same core sequence regardless of integration style:

**Inputs:**
- Credentials (email + password)
- Login URL (e.g. `/login`, `/sign-in`)
- Form selectors (email input, password input, submit button)

**Outputs:**
- Authenticated `Page` object (post-redirect)
- Optional: saved storage state file for reuse across tests

**Core steps:**
1. Navigate to login URL
2. Wait for form visibility
3. Fill email and password fields
4. Click submit
5. Wait for post-login redirect (URL no longer contains login path)
6. Optionally save `storageState` for subsequent tests

## Integration Styles: Which One and Why

The two styles solve different problems — picking by "which repo already does this" instead of
by what the suite actually needs is how you end up importing POM boilerplate into a suite that
never asserts on the login page, or bolting a fixture factory onto a suite that needs to test
login itself.

**The signal that decides it: is the login flow itself part of what you're testing, or is it
pure setup to get past?**

- **The login page is a test subject** (OAuth buttons, remember-me, rate limiting, error states
  on bad credentials) → **Page Object Model**. A POM gives you an addressable object to assert
  against (`loginPage.errorMessage`, `loginPage.rateLimitBanner`) — a fixture that just hands you
  an authenticated `Page` has nowhere to hang those assertions.
- **Login is scaffolding for everything downstream** (multi-role app, tests only care about
  post-login behavior) → **Fixture (`test.extend()`)**. A fixture bakes auth into test setup so
  test bodies never see a login call — the whole point is zero boilerplate, which a POM instance
  constructed per-test does not give you.

**Cost of choosing wrong:** POM-for-a-fixture-shaped-problem means every test file that needs
`agentPage` and `platformAdminPage` re-instantiates and re-drives a login page object per role,
multiplying boilerplate exactly where the fixture style eliminates it. Fixture-for-a-POM-shaped-
problem means you lose the addressable object entirely — a test asserting "shows rate-limit
banner after 5 failed attempts" has no natural home once login is hidden behind a fixture that
only returns an already-authenticated page.

Full class shapes, reference file paths, and key characteristics for each style:
`references/integration-styles.md`.

## Single-User vs Multi-Role Auth

**Single-user:** One set of credentials, one authenticated page. Use when the app has
no role differentiation or tests only exercise one role.

```typescript
// Single-user: just export one fixture or one POM instance
const authenticatedPage = await loginAs(page, DEFAULT_USER);
```

**Multi-role:** Multiple credential sets, one authenticated page per role. Define personas in the
canonical typed persona catalog and expose each as a named fixture or POM factory.

```typescript
const PERSONAS = {
  platformAdmin: { role: "platform-admin", storageStatePath: ".auth/platform-admin.json" },
  agent: { role: "agency-agent", storageStatePath: ".auth/agent.json" },
};
// Each becomes a separate fixture: platformAdminPage, agentPage, etc.
```

## Persona Catalog + Setup Project State

Playwright auth state is owned by one typed canonical persona catalog. The catalog drives seed
identity, semantic role, credential env keys or deterministic fallbacks, and the `.auth/<persona>.json`
path consumed by fixtures and config.

```typescript
type Persona = {
  key: "admin" | "agent" | "attendee";
  role: "platform-admin" | "agency-agent" | "event-attendee";
  emailEnv: string;
  passwordEnv: string;
  defaultEmail: string;
  defaultPassword: string;
  storageStatePath: `.auth/${string}.json`;
};
```

Create auth state in the serial Playwright `setup` project, not a browser-launching `globalSetup`
or per-test login loop:

```typescript
await page.context().storageState({ path: ".auth/admin.json" });
const context = await browser.newContext({ storageState: ".auth/admin.json" });
```

**Rules:**
- Use a serial `setup` project to create auth state before dependent projects run
- Use `.auth/` directory (gitignored) for state files
- One file per persona: `.auth/admin.json`, `.auth/agent.json`, etc.
- Regenerate on CI every run -- never cache auth state across builds or targets
- Missing or invalid persona state fails closed (or explicitly skips with the requested persona named)
- Never silently substitute a more privileged fallback persona
- Storage state includes cookies and localStorage, not sessionStorage

## Credential Sources

| Source | When | Example |
|--------|------|---------|
| Environment variable | CI, shared test accounts | `process.env.ADMIN_EMAIL` |
| Deterministic fallback | Local dev with seeded DB | `"admin@platform.test"` |
| `.env` file | Local dev through the package-owned dotenvx boundary | `ADMIN_EMAIL=admin@test` |

**Best practice:** Env var with deterministic fallback matching the seeded persona catalog. CI sets
the env var; local dev uses the fallback.

```typescript
const ADMIN: AuthCredentials = {
  email: process.env.ADMIN_EMAIL || "admin@platform.test",
  password: process.env.ADMIN_PASSWORD || "TestPassword123!",
};
```

Never commit real credentials. Test accounts should be seeded by the dev database
setup script and use obvious test passwords.

## Anti-Patterns

| Avoid | Why It Fails | Do Instead |
|-------|--------------|------------|
| Login in every test body | Every test pays the full login round-trip even though the app under test never changes | Use fixtures or setup-generated storage state |
| Hardcoded selectors without data-testid | Selectors built from CSS classes or DOM structure break on harmless UI refactors | Add `data-testid` attributes to login form |
| `page.waitForTimeout(3000)` after login | A fixed timeout flakes under CI variance and cold caches | `page.waitForURL()` on post-login redirect |
| Sharing browser context across roles | Reusing one context across roles leaks the first role's session into the second role's requests | One context per role (fixture teardown closes it) |
| Silent privileged fallback | Loading admin/platform-owner state when the requested staff/attendee persona is missing hides real auth defects | Fail closed or explicitly skip with remediation |
| Storing `.auth/*.json` in git or reusing prior-build state | Live session files leak credentials and go stale across builds/targets | Gitignore `.auth/`, regenerate per CI run/target |

## External Effects in Auth Journeys

Auth E2E flows that send verification, invitation, magic-link, or password-reset email MUST keep
the real browser route, auth service, token persistence, and authorization behavior. Substitute
only the terminal delivery through the application's injected `EmailDelivery` interface and its
deterministic run-scoped E2E adapter. Both POM and fixture styles import the same typed persona
catalog and `.auth/<persona>.json` paths; provider substitution never changes the auth ownership
model.

- Resolve the exact safe delivery receipt from the run-owned adapter store before asserting success.
- Read test tokens/links from the deterministic mailbox contract, never from a shared Resend inbox.
- Fail before production provider contact when E2E adapter selection or run identity is invalid.
- Do not use `page.route` to fulfill the application's auth endpoint; that bypasses the server flow.
- Keep a separate production-adapter integration lane for Resend authentication and response mapping.
- Never claim deterministic mailbox success proves real email delivery.

See `t3-testing-patterns` Rule 13 for the provider-boundary contract. POM versus fixture selection
still depends only on whether the login UI itself is under test; provider substitution does not
change the auth integration style.

## Portless local auth acceptance

When a test run explicitly opts into portless, use its stable, product-named development origin
consistently for navigation and callback configuration; the backend port remains dynamically assigned
on loopback. Before claiming authenticated
coverage, prove that auth callbacks, cookie scope, and the test URL trust policy accept that origin.
Keep the normal local command as the default and do not treat portless as a deployed target. Follow
the [portless opt-in development guide](https://github.com/Priceless-Development/priceless-internal/blob/main/docs/guides/portless-opt-in-development.md#launch-and-verify)
for the canonical boundary; do not duplicate its setup procedure here.

## Related

- `webapp-testing` skill -- Playwright setup, selectors, screenshots, server lifecycle
- `qa-test-planner` skill -- Test planning and coverage strategy
