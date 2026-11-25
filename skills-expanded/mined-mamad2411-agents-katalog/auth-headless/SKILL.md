---
name: auth-headless
description: "Authenticate via direct API calls and cookie injection for faster E2E tests. Use when project.json has authentication.headless enabled. Triggers on: headless auth, api login, fast auth, cookie injection, session injection."
---

# Headless Authentication

Authenticate via direct API calls and inject auth cookies/tokens into the browser context, bypassing the login UI for faster tests.

---

## Overview

Instead of clicking through the login UI for every test:

1. **One UI test** exercises the actual login flow (for coverage)
2. **All other tests** use headless auth (direct API + cookie injection)

This can reduce test suite time by 80%+ when you have many authenticated tests.

---

## Prerequisites

1. **Project configuration** in `docs/project.json`:
   ```json
   {
     "authentication": {
       "method": "passwordless-otp",
       "provider": "supabase",
       "headless": {
         "enabled": true,
         "method": "supabase-admin",
         "sessionStorage": "cookies"
       },
       "testUser": {
         "mode": "fixed",
         "emailVar": "TEST_EMAIL"
       }
     }
   }
   ```

2. **Environment variables** in `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJ...
   TEST_EMAIL=test@example.com
   ```

---

## Headless Methods

### Supabase Admin (`"method": "supabase-admin"`)

Use Supabase Admin API to generate a session directly:

```typescript
import { createClient } from '@supabase/supabase-js';
import { BrowserContext } from 'playwright';

interface HeadlessAuthResult {
  success: boolean;
  email: string;
  accessToken?: string;
  refreshToken?: string;
  error?: string;
}

async function authenticateHeadlessSupabase(
  context: BrowserContext,
  baseUrl: string,
  projectRoot: string
): Promise<HeadlessAuthResult> {
  loadEnv(projectRoot);
  const config = loadAuthConfig(projectRoot);
  const email = getTestEmail(config);
  
  const supabase = getSupabaseServiceClient();
  
  try {
    // Generate a magic link token for the user
    const { data: linkData, error: linkError } = await supabase.auth.admin
      .generateLink({
        type: 'magiclink',
        email,
        options: {
          redirectTo: `${baseUrl}${config.routes?.authenticated || '/'}`,
        }
      });
    
    if (linkError || !linkData?.properties?.hashed_token) {
      throw new Error(`Failed to generate link: ${linkError?.message || 'No token'}`);
    }
    
    // Verify the OTP to get a session
    const { data: sessionData, error: verifyError } = await supabase.auth
      .verifyOtp({
        token_hash: linkData.properties.hashed_token,
        type: 'magiclink',
      });
    
    if (verifyError || !sessionData.session) {
      throw new Error(`Failed to verify: ${verifyError?.message || 'No session'}`);
    }
    
    const session = sessionData.session;
    
    // Inject cookies into browser context
    await injectSupabaseSession(context, baseUrl, session);
    
    console.log(`Headless auth successful for ${email}`);
    
    return {
      success: true,
      email,
      accessToken: session.access_token,
      refreshToken: session.refresh_token,
    };
    
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Headless auth failed: ${message}`);
    return { success: false, email, error: message };
  }
}

async function injectSupabaseSession(
  context: BrowserContext,
  baseUrl: string,
  session: { access_token: string; refresh_token: string; expires_at?: number }
): Promise<void> {
  const url = new URL(baseUrl);
  const domain = url.hostname;
  
  // Supabase stores session in localStorage, but we can also set cookies
  // The exact storage depends on your Supabase client configuration
  
  // Option 1: Set cookies (if using cookie-based storage)
  await context.addCookies([
    {
      name: 'sb-access-token',
      value: session.access_token,
      domain,
      path: '/',
      httpOnly: true,
      secure: url.protocol === 'https:',
      sameSite: 'Lax',
      expires: session.expires_at || (Date.now() / 1000 + 3600),
    },
    {
      name: 'sb-refresh-token',
      value: session.refresh_token,
      domain,
      path: '/',
      httpOnly: true,
      secure: url.protocol === 'https:',
      sameSite: 'Lax',
      expires: Date.now() / 1000 + 86400 * 7,
    },
  ]);
  
  // Option 2: Inject into localStorage (if using localStorage-based storage)
  // This requires navigating to the page first
  const page = await context.newPage();
  await page.goto(baseUrl);
  await page.evaluate((sessionData) => {
    const key = `sb-${new URL(window.location.origin).hostname.split('.')[0]}-auth-token`;
    localStorage.setItem(key, JSON.stringify(sessionData));
  }, {
    access_token: session.access_token,
    refresh_token: session.refresh_token,
    expires_at: session.expires_at,
    token_type: 'bearer',
    user: null, // Will be populated when the page loads
  });
  await page.close();
}
```

### NextAuth Direct (`"method": "nextauth-direct"`)

Create a NextAuth session directly:

```typescript
import { BrowserContext } from 'playwright';
import crypto from 'crypto';

async function authenticateHeadlessNextAuth(
  context: BrowserContext,
  baseUrl: string,
  projectRoot: string
): Promise<HeadlessAuthResult> {
  loadEnv(projectRoot);
  const config = loadAuthConfig(projectRoot);
  const { email } = getTestCredentials(config);
  
  try {
    // Get CSRF token first
    const page = await context.newPage();
    await page.goto(`${baseUrl}/api/auth/csrf`);
    const csrfResponse = await page.content();
    const csrfToken = JSON.parse(csrfResponse.match(/{.*}/)?.[0] || '{}').csrfToken;
    await page.close();
    
    // Create session via credentials endpoint
    const response = await fetch(`${baseUrl}/api/auth/callback/credentials`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        csrfToken,
        email,
        password: process.env.TEST_PASSWORD || '',
        json: 'true',
      }),
      redirect: 'manual',
    });
    
    // Extract session cookie from response
    const setCookieHeader = response.headers.get('set-cookie');
    if (!setCookieHeader) {
      throw new Error('No session cookie in response');
    }
    
    // Parse and inject cookies
    const cookies = parseSetCookieHeader(setCookieHeader, new URL(baseUrl).hostname);
    await context.addCookies(cookies);
    
    return { success: true, email };
    
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { success: false, email, error: message };
  }
}

function parseSetCookieHeader(header: string, domain: string): Cookie[] {
  return header.split(',').map(cookie => {
    const [nameValue, ...attrs] = cookie.split(';');
    const [name, value] = nameValue.split('=');
    
    return {
      name: name.trim(),
      value: value?.trim() || '',
      domain,
      path: '/',
      httpOnly: attrs.some(a => a.trim().toLowerCase() === 'httponly'),
      secure: attrs.some(a => a.trim().toLowerCase() === 'secure'),
      sameSite: 'Lax' as const,
    };
  });
}
```

### Custom API (`"method": "custom-api"`)

For custom auth systems, call your own API:

```json
{
  "authentication": {
    "headless": {
      "enabled": true,
      "method": "custom-api",
      "endpoint": "/api/auth/test-login",
      "requestBody": {
        "email": "{{email}}",
        "password": "{{password}}",
        "testMode": true
      },
      "responseTokenPath": "data.session.token",
      "cookieName": "auth-token"
    }
  }
}
```

```typescript
async function authenticateHeadlessCustom(
  context: BrowserContext,
  baseUrl: string,
  config: AuthConfig,
  credentials: { email: string; password?: string }
): Promise<HeadlessAuthResult> {
  const headless = config.headless!;
  
  // Build request body
  const body = JSON.parse(
    JSON.stringify(headless.requestBody)
      .replace('{{email}}', credentials.email)
      .replace('{{password}}', credentials.password || '')
  );
  
  const response = await fetch(`${baseUrl}${headless.endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  
  const data = await response.json();
  
  // Extract token from response using path
  const token = getNestedValue(data, headless.responseTokenPath!);
  
  if (!token) {
    throw new Error('No token in response');
  }
  
  // Set cookie
  await context.addCookies([{
    name: headless.cookieName!,
    value: token,
    domain: new URL(baseUrl).hostname,
    path: '/',
    httpOnly: true,
    secure: baseUrl.startsWith('https'),
    sameSite: 'Lax',
  }]);
  
  return { success: true, email: credentials.email };
}

function getNestedValue(obj: any, path: string): any {
  return path.split('.').reduce((acc, key) => acc?.[key], obj);
}
```

### CLI (`"method": "cli"`)

For projects with CLI tools that generate auth tokens (admin APIs, custom scripts):

```json
{
  "authentication": {
    "headless": {
      "enabled": true,
      "method": "cli",
      "command": "pnpm cli auth:test-token --email $TEST_EMAIL",
      "responseFormat": "json",
      "tokenPath": "accessToken",
      "refreshTokenPath": "refreshToken",
      "sessionStorage": "localStorage"
    }
  }
}
```

**Configuration fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Shell command to run. Supports `$ENV_VAR` and `${ENV_VAR}` expansion. |
| `responseFormat` | No | Format of CLI output: `json` (default), `text`, or `env` (KEY=VALUE lines) |
| `tokenPath` | No | Dot-path to access token in JSON response (default: `accessToken`) |
| `refreshTokenPath` | No | Dot-path to refresh token in JSON response (optional) |
| `sessionStorage` | No | Where to inject: `cookies`, `localStorage`, or `both` (default: `cookies`) |

```typescript
async function authenticateHeadlessCLI(
  context: BrowserContext,
  baseUrl: string,
  projectRoot: string
): Promise<HeadlessAuthResult> {
  const config = loadAuthConfig(projectRoot);
  const headless = config.headless!;
  const email = getTestEmail(config);

  // Expand env vars in command
  const command = headless.command
    .replace(/\$TEST_EMAIL|\${TEST_EMAIL}/g, email)
    .replace(/\$([A-Z_]+)|\${([A-Z_]+)}/g, (_, a, b) => process.env[a || b] || '');

  // Execute CLI command from project root
  const { stdout, stderr, exitCode } = await exec(command, { cwd: projectRoot });

  if (exitCode !== 0) {
    return { success: false, email, error: `CLI failed (exit ${exitCode}): ${stderr}` };
  }

  // Parse response based on format
  let tokens: Record<string, string>;
  switch (headless.responseFormat || 'json') {
    case 'json':
      tokens = JSON.parse(stdout);
      break;
    case 'text':
      tokens = { accessToken: stdout.trim() };
      break;
    case 'env':
      tokens = {};
      stdout.split('\n').forEach(line => {
        const [k, ...rest] = line.split('=');
        if (k && rest.length) tokens[k.trim()] = rest.join('=').trim();
      });
      break;
    default:
      throw new Error(`Unknown responseFormat: ${headless.responseFormat}`);
  }

  // Extract tokens using configured paths
  const accessToken = getNestedValue(tokens, headless.tokenPath || 'accessToken');
  const refreshToken = headless.refreshTokenPath
    ? getNestedValue(tokens, headless.refreshTokenPath)
    : undefined;

  if (!accessToken) {
    return {
      success: false,
      email,
      error: `No token found at path "${headless.tokenPath || 'accessToken'}" in CLI output`,
    };
  }

  // Inject into browser context
  await injectSession(context, baseUrl, config, accessToken, refreshToken);

  return { success: true, email, accessToken };
}

async function injectSession(
  context: BrowserContext,
  baseUrl: string,
  config: AuthConfig,
  accessToken: string,
  refreshToken?: string
): Promise<void> {
  const url = new URL(baseUrl);
  const domain = url.hostname;
  const storage = config.headless?.sessionStorage || 'cookies';

  if (storage === 'cookies' || storage === 'both') {
    const cookies = [
      {
        name: 'access-token',
        value: accessToken,
        domain,
        path: '/',
        httpOnly: true,
        secure: url.protocol === 'https:',
        sameSite: 'Lax' as const,
        expires: Date.now() / 1000 + 3600,
      },
    ];
    if (refreshToken) {
      cookies.push({
        name: 'refresh-token',
        value: refreshToken,
        domain,
        path: '/',
        httpOnly: true,
        secure: url.protocol === 'https:',
        sameSite: 'Lax' as const,
        expires: Date.now() / 1000 + 86400 * 7,
      });
    }
    await context.addCookies(cookies);
  }

  if (storage === 'localStorage' || storage === 'both') {
    const page = await context.newPage();
    await page.goto(baseUrl);
    await page.evaluate(({ accessToken, refreshToken }) => {
      localStorage.setItem('access-token', accessToken);
      if (refreshToken) localStorage.setItem('refresh-token', refreshToken);
    }, { accessToken, refreshToken });
    await page.close();
  }
}
```

**Fallback behavior:** If the CLI command fails, agents should check `authentication.acquisition.steps` for manual fallback instructions. If `acquisition.fallbackToUI` is `true`, fall back to the UI-based auth flow using the appropriate auth skill.

---

## Complete Script Template

```typescript
import { chromium, BrowserContext } from 'playwright';
import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

const PROJECT_ROOT = process.cwd();
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5001';

// (Include helper functions from above)

async function getAuthenticatedContext(): Promise<BrowserContext> {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  
  const config = loadAuthConfig(PROJECT_ROOT);
  
  if (config.headless?.enabled) {
    // Use headless auth
    const result = await authenticateHeadless(context, BASE_URL, PROJECT_ROOT);
    if (!result.success) {
      throw new Error(`Headless auth failed: ${result.error}`);
    }
  } else {
    // Fall back to UI auth
    const page = await context.newPage();
    await authenticateViaUI(page, BASE_URL, PROJECT_ROOT);
  }
  
  return context;
}

async function authenticateHeadless(
  context: BrowserContext,
  baseUrl: string,
  projectRoot: string
): Promise<HeadlessAuthResult> {
  const config = loadAuthConfig(projectRoot);
  
  switch (config.headless?.method) {
    case 'supabase-admin':
      return authenticateHeadlessSupabase(context, baseUrl, projectRoot);
    case 'nextauth-direct':
      return authenticateHeadlessNextAuth(context, baseUrl, projectRoot);
    case 'custom-api':
      return authenticateHeadlessCustom(context, baseUrl, config, getTestCredentials(config));
    case 'cli':
      return authenticateHeadlessCLI(context, baseUrl, projectRoot);
    default:
      throw new Error(`Unknown headless method: ${config.headless?.method}`);
  }
}

// Usage
async function main() {
  const context = await getAuthenticatedContext();
  const page = await context.newPage();
  
  // Navigate directly to authenticated page
  await page.goto(`${BASE_URL}/dashboard`);
  
  // Take screenshot or run tests
  await page.screenshot({ path: 'dashboard.png' });
  
  await context.close();
}

main().catch(console.error);
```

---

## Playwright Fixture Pattern

Use a custom fixture for authenticated tests:

```typescript
// tests/fixtures.ts
import { test as base, BrowserContext } from '@playwright/test';

type AuthFixtures = {
  authenticatedContext: BrowserContext;
};

export const test = base.extend<AuthFixtures>({
  authenticatedContext: async ({ browser }, use) => {
    const context = await browser.newContext();
    
    // Use headless auth
    await authenticateHeadless(context, BASE_URL, PROJECT_ROOT);
    
    await use(context);
    await context.close();
  },
});

// tests/dashboard.spec.ts
import { test } from './fixtures';

test('dashboard loads correctly', async ({ authenticatedContext }) => {
  const page = await authenticatedContext.newPage();
  await page.goto('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

---

## Which Test Should NOT Use Headless?

Keep **one test** that exercises the actual login UI:

```typescript
// tests/auth/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  // This test uses real UI auth - DO NOT use headless fixture
  test('user can log in via UI', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="email"]', process.env.TEST_EMAIL!);
    await page.fill('input[type="password"]', process.env.TEST_PASSWORD!);
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
});

// All other tests use headless auth
// tests/dashboard.spec.ts
import { test } from './fixtures';

test.describe('Dashboard', () => {
  test('shows user data', async ({ authenticatedContext }) => {
    // This test uses headless auth - no UI login needed
    const page = await authenticatedContext.newPage();
    await page.goto('/dashboard');
    // ...
  });
});
```

Mark the UI test clearly:

```typescript
// tests/auth/login.spec.ts
/**
 * @ui-auth-test
 * This test exercises the actual login UI flow.
 * DO NOT use headless authentication for this test.
 * All other auth-requiring tests should use the headless fixture.
 */
test('user can log in via UI', async ({ page }) => {
  // ...
});
```

---

## Performance Comparison

| Approach | Time per test | 100 tests |
|----------|---------------|-----------|
| UI login every test | ~3-5 seconds | 300-500s |
| Headless auth | ~0.1-0.3 seconds | 10-30s |
| Session reuse | ~0 seconds | ~0s (first test pays cost) |

Combining headless + session reuse provides the best performance.

---

## Session Storage Options

### Cookies (`"sessionStorage": "cookies"`)

Auth tokens stored in HTTP cookies. Inject via `context.addCookies()`.

### LocalStorage (`"sessionStorage": "localStorage"`)

Auth tokens stored in localStorage. Requires navigating to page first, then using `page.evaluate()`.

### Both (`"sessionStorage": "both"`)

Some apps use both. Inject cookies first, then localStorage.

---

## Combining with Session Reuse

For maximum speed, combine headless auth with session reuse:

```json
{
  "authentication": {
    "headless": {
      "enabled": true,
      "method": "supabase-admin"
    },
    "reuseSession": true
  }
}
```

### Session Reuse Implementation

```typescript
import { BrowserContext, Browser } from 'playwright';
import * as fs from 'fs';

const AUTH_STATE_FILE = '.tmp/auth-state.json';

interface AuthState {
  cookies: Array<{
    name: string;
    value: string;
    domain: string;
    path: string;
    expires?: number;
  }>;
  localStorage?: Record<string, string>;
  createdAt: number;
}

async function saveAuthState(
  context: BrowserContext,
  baseUrl: string
): Promise<void> {
  const state: AuthState = {
    cookies: await context.cookies(),
    createdAt: Date.now(),
  };
  
  // Also save localStorage if headless injected tokens there
  const page = await context.newPage();
  await page.goto(baseUrl);
  state.localStorage = await page.evaluate(() => {
    const items: Record<string, string> = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.includes('auth')) {
        items[key] = localStorage.getItem(key) || '';
      }
    }
    return items;
  });
  await page.close();
  
  fs.mkdirSync('.tmp', { recursive: true });
  fs.writeFileSync(AUTH_STATE_FILE, JSON.stringify(state, null, 2));
  console.log('Saved headless auth state for reuse');
}

async function loadAuthState(
  context: BrowserContext,
  baseUrl: string
): Promise<boolean> {
  if (!fs.existsSync(AUTH_STATE_FILE)) {
    return false;
  }
  
  try {
    const state: AuthState = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf-8'));
    const now = Date.now();
    
    // Check if state is too old (default 1 hour)
    const maxAge = 60 * 60 * 1000;
    if (now - state.createdAt > maxAge) {
      console.log('Cached auth state expired');
      fs.unlinkSync(AUTH_STATE_FILE);
      return false;
    }
    
    // Check if cookies are expired
    const nowSec = now / 1000;
    const hasExpiredCookies = state.cookies.some(
      c => c.expires && c.expires < nowSec
    );
    if (hasExpiredCookies) {
      console.log('Auth cookies expired');
      fs.unlinkSync(AUTH_STATE_FILE);
      return false;
    }
    
    // Load cookies
    await context.addCookies(state.cookies);
    
    // Load localStorage if present
    if (state.localStorage && Object.keys(state.localStorage).length > 0) {
      const page = await context.newPage();
      await page.goto(baseUrl);
      await page.evaluate((items) => {
        for (const [key, value] of Object.entries(items)) {
          localStorage.setItem(key, value);
        }
      }, state.localStorage);
      await page.close();
    }
    
    console.log('Loaded cached headless auth state');
    return true;
  } catch (error) {
    console.warn('Failed to load auth state:', error);
    return false;
  }
}

async function getAuthenticatedContext(
  browser: Browser,
  baseUrl: string,
  projectRoot: string
): Promise<BrowserContext> {
  const config = loadAuthConfig(projectRoot);
  const context = await browser.newContext();
  
  // Try cached state first
  if (config.reuseSession) {
    const loaded = await loadAuthState(context, baseUrl);
    if (loaded) {
      // Quick validation: check we can access authenticated page
      const page = await context.newPage();
      await page.goto(`${baseUrl}${config.routes?.authenticated || '/dashboard'}`);
      
      const isAuthenticated = !page.url().includes(config.routes?.login || '/login');
      await page.close();
      
      if (isAuthenticated) {
        return context;
      }
      console.log('Cached state invalid, re-authenticating');
    }
  }
  
  // Perform headless auth
  const result = await authenticateHeadless(context, baseUrl, projectRoot);
  if (!result.success) {
    throw new Error(`Headless auth failed: ${result.error}`);
  }
  
  // Save for reuse
  if (config.reuseSession) {
    await saveAuthState(context, baseUrl);
  }
  
  return context;
}
```

### Performance Comparison with Session Reuse

| Approach | First test | Subsequent tests |
|----------|------------|------------------|
| UI auth each test | ~3-5s | ~3-5s |
| Headless each test | ~0.1-0.3s | ~0.1-0.3s |
| Headless + reuse | ~0.1-0.3s | ~0.01s |

### Clear State Between Runs

```typescript
// In globalSetup or beforeAll
function clearAuthState(): void {
  if (fs.existsSync(AUTH_STATE_FILE)) {
    fs.unlinkSync(AUTH_STATE_FILE);
  }
}
```

---

## Troubleshooting

### "Token expired" or "Invalid session"
- Check that `expires_at` is set correctly
- Ensure system clocks are synchronized
- Verify token hasn't expired between generation and use

### "401 Unauthorized" after injection
- Verify cookie domain matches exactly
- Check if app expects both cookie AND localStorage
- Some apps verify the session on the server - ensure the session is valid

### Session not persisting across pages
- Ensure cookies have correct `path: '/'`
- Check `sameSite` attribute matches your app's requirements
- Verify `secure` flag matches protocol (https vs http)

### Works locally but fails in CI
- CI may use different base URLs
- Check cookie domain handling for localhost vs CI domain
- Ensure all required env vars are set in CI

---

## Integration

This skill is used by:
- `ui-tester-playwright` - for fast authenticated tests
- `screenshot` - for capturing authenticated pages quickly
- `qa-browser-tester` - for rapid QA testing

When headless is enabled, these skills should:
1. Check `authentication.headless.enabled`
2. Use headless auth for all tests except designated UI auth tests
3. Fall back to UI auth if headless fails
4. Report performance gains in test output
