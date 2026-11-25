---
name: auth-config-check
description: "Check for authentication configuration before auth-dependent tasks like E2E tests, screenshots, or QA browser testing. Triggers on: auth config check, authentication check, pre-auth validation, auth prerequisite."
---

# Authentication Configuration Check Skill

> ⛔ **CRITICAL: Check for authentication config BEFORE any auth-dependent task.**
>
> **Failure behavior:** If config is missing/invalid, run inline auth setup (below). Do not proceed without valid configuration.
>
> **Auth-dependent tasks:** E2E tests, screenshot capture, QA browser testing, any Playwright/browser automation requiring login.

## Triggers

- Starting E2E tests that require login
- Capturing screenshots of authenticated pages
- Running QA tests on authenticated features
- Any sub-agent (ui-tester-playwright, qa-browser-tester, screenshot) needs to authenticate
- "auth config", "authentication check", "login required"

## Applicable Agents

- **builder** — before delegating auth-dependent tasks
- **ui-tester-playwright** — before writing authenticated tests
- **qa-explorer** — before testing protected features
- **qa-browser-tester** — before automating protected flows
- **screenshot** — before capturing authenticated pages

---

## Check Flow

### Step 1: Read Authentication Config

```bash
jq '.authentication' docs/project.json
```

### Step 2a: If Valid Config Exists

If `authentication` exists and is valid:
- Proceed with the auth-dependent task
- Load the appropriate auth skill (derived from `method` + `provider`)
- Pass auth config to sub-agents

### Step 2b: If Config Missing or Invalid

> ⛔ **DO NOT stop and ask the user.** Resolve auth autonomously first.
> Builder has `setup-auth` and detection patterns — use them before involving the user.

**Step A: Attempt autonomous resolution via `setup-auth` skill**

Load the `setup-auth` skill and run its detection + configuration flow:
- It scans `package.json` for auth dependencies
- It scans code for auth patterns (signInWithOtp, signInWithPassword, useSession, etc.)
- It checks for existing env vars (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, etc.)
- It derives the auth provider and method automatically
- It writes `authentication` config to `project.json`

If `setup-auth` succeeds → loop back to **Step 2a** with the new config.

**Step B: If autonomous resolution fails (no auth infrastructure detectable)**

Only THEN involve the user, with a specific diagnostic report:

```
═══════════════════════════════════════════════════════════════════════
            ⚠️ AUTHENTICATION CONFIGURATION REQUIRED
═══════════════════════════════════════════════════════════════════════

I attempted to configure authentication automatically but could not
detect your auth setup.

What I tried:
  • Scanned package.json — no known auth dependencies found
  • Scanned src/ for auth patterns — no matches
  • Checked environment variables — none detected

I cannot proceed with auth-dependent tasks without configuration.

Please add auth config to docs/project.json:

   {
     "authentication": {
       "method": "passwordless-otp",
       "provider": "supabase",
       "testUser": {
         "type": "fixed",
         "email": "test@example.com"
       },
       "routes": {
         "login": "/login",
         "verify": "/verify",
         "authenticated": "/dashboard"
       }
     }
   }

After configuration, retry the task.

> _
═══════════════════════════════════════════════════════════════════════
```

**Step C: Wait only after autonomous resolution has failed**

- Do NOT proceed with auth-dependent tasks
- Do NOT attempt to guess or hardcode auth configuration
- Do NOT offer to "try anyway"

---

## Detection Patterns

| Dependency | Provider | Likely Method |
|------------|----------|---------------|
| `@supabase/supabase-js` | supabase | Check for OTP vs password |
| `@supabase/ssr` | supabase | Check for OTP vs password |
| `next-auth` | nextauth | credentials or oauth |
| `@auth/core` | nextauth | credentials or oauth |
| `@clerk/nextjs` | clerk | oauth |
| `@auth0/auth0-react` | auth0 | oauth |

---

## Auth Skill Selection

Based on `authentication.provider` and `authentication.method`:

| Provider | Method | Auth Skill |
|----------|--------|------------|
| supabase | passwordless-otp | `auth-supabase-otp` |
| supabase | email-password | `auth-supabase-password` |
| nextauth | email-password | `auth-nextauth-credentials` |
| custom | * | `auth-generic` |

If `authentication.headless.enabled` is `true`, prefer `auth-headless` for speed.

### Acquisition Validation

When `authentication.acquisition` is present, validate:

| Field | Required | Check |
|-------|----------|-------|
| `description` | Yes | Must be a non-empty string |
| `steps` | Yes | Must be a non-empty array of strings |
| `fallbackToUI` | No | Boolean, defaults to `true` |
| `notes` | No | Optional string |

If `acquisition` exists but is invalid (empty `steps` or missing `description`), warn:

```
⚠️ ACQUISITION CONFIG INCOMPLETE

authentication.acquisition exists but is missing required fields:
  - description: [present/missing]
  - steps: [N items / empty / missing]

Fix: Ensure both description and steps are populated.
Agents use acquisition.steps as fallback when headless auth fails.
```

### Headless CLI Validation

When `authentication.headless.method` is `"cli"`, additionally validate:

| Field | Required | Check |
|-------|----------|-------|
| `command` | Yes | Must be a non-empty string |
| `responseFormat` | No | Must be `json`, `text`, or `env` if present |
| `tokenPath` | No | Must be a non-empty string if present |
| `sessionStorage` | No | Must be `cookies`, `localStorage`, or `both` if present |

If `method: "cli"` but `command` is missing:

```
⚠️ CLI AUTH CONFIG INCOMPLETE

headless.method is "cli" but command is missing.

Fix: Add headless.command with the CLI command to generate auth tokens.
Example: "pnpm cli auth:test-token --email $TEST_EMAIL"
```

---

## Sub-Agent Delegation with Auth

When delegating to auth-dependent sub-agents, include auth config in context:

```yaml
<context>
version: 1
project:
  path: {path}
  stack: {stack}
authentication:
  method: {method}
  provider: {provider}
  skill: {skill name}
  testUserEmail: {email}
  routes:
    login: {login path}
    authenticated: {authenticated path}
</context>
```

---

## Related Skills

- `setup-auth` — Interactive auth configuration wizard
- `auth-supabase-otp` — Supabase OTP login
- `auth-supabase-password` — Supabase password login
- `auth-nextauth-credentials` — NextAuth credentials login
- `auth-generic` — Generic/custom auth
- `auth-headless` — Headless auth session injection
