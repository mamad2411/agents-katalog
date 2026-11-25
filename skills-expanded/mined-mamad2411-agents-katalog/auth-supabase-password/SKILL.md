---
name: auth-supabase-password
description: "Authenticate with Supabase email/password for testing. Use when project.json has authentication.provider: supabase and authentication.method: email-password. Triggers on: supabase password login, email password auth, supabase credentials."
---

# Supabase Email/Password Authentication

Authenticate with a Supabase-powered application using email and password for testing purposes.

---

## Prerequisites

1. **Project configuration** in `docs/project.json`:
   ```json
   {
     "authentication": {
       "method": "email-password",
       "provider": "supabase",
       "testUser": {
         "mode": "fixed",
         "emailVar": "TEST_EMAIL",
         "emailDefault": "test@example.com",
         "passwordVar": "TEST_PASSWORD"
       },
       "routes": {
         "login": "/login",
         "authenticated": "/dashboard"
       }
     }
   }
   ```

2. **Environment variables** in `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJ...
   TEST_EMAIL=test@example.com
   TEST_PASSWORD=your-test-password
   ```

3. **Test user exists** in Supabase Auth with confirmed email (for fixed mode)

---

## The Job

1. Read authentication config from `project.json`
2. Navigate to login page
3. Enter test email and password
4. Submit login form
5. Wait for redirect to authenticated page
6. Return authenticated page context

---

## Authentication Flow

### Step 1: Load Configuration

```typescript
import * as fs from 'fs';
import * as path from 'path';

interface AuthConfig {
  method: string;
  provider: string;
  testUser: {
    mode: 'fixed' | 'dynamic';
    emailVar?: string;
    emailDefault?: string;
    emailPattern?: string;
    passwordVar?: string;
    passwordDefault?: string;
  };
  routes: {
    login: string;
    authenticated: string;
  };
  selectors?: {
    emailInput?: string;
    passwordInput?: string;
    submitButton?: string;
  };
}

function loadAuthConfig(projectRoot: string): AuthConfig {
  const projectJsonPath = path.join(projectRoot, 'docs', 'project.json');
  const projectJson = JSON.parse(fs.readFileSync(projectJsonPath, 'utf-8'));
  
  if (!projectJson.authentication) {
    throw new Error('No authentication config found in project.json. Run /setup-auth first.');
  }
  
  return projectJson.authentication;
}

function getTestCredentials(config: AuthConfig): { email: string; password: string } {
  let email: string;
  let password: string;
  
  if (config.testUser.mode === 'dynamic') {
    const uuid = crypto.randomUUID().slice(0, 8);
    const pattern = config.testUser.emailPattern || 'test-{uuid}@example.com';
    email = pattern.replace('{uuid}', uuid);
    // Dynamic mode uses a known password for all test users
    password = process.env[config.testUser.passwordVar || 'TEST_PASSWORD'] 
      || config.testUser.passwordDefault 
      || 'Test123!@#';
  } else {
    // Fixed mode
    const emailVar = config.testUser.emailVar || 'TEST_EMAIL';
    const passwordVar = config.testUser.passwordVar || 'TEST_PASSWORD';
    email = process.env[emailVar] || config.testUser.emailDefault || 'test@example.com';
    password = process.env[passwordVar] || config.testUser.passwordDefault || '';
    
    if (!password) {
      throw new Error(
        `Password not configured. Set ${passwordVar} in .env.local or ` +
        `testUser.passwordDefault in project.json`
      );
    }
  }
  
  return { email, password };
}
```

### Step 2: Load Environment Variables

```typescript
function loadEnv(projectRoot: string): void {
  const envPath = path.join(projectRoot, '.env.local');
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf-8');
    content.split('\n').forEach(line => {
      const match = line.trim().match(/^([^=]+)=(.*)$/);
      if (match && !process.env[match[1]]) {
        process.env[match[1]] = match[2];
      }
    });
  }
}
```

### Step 3: Create Supabase Service Client (for dynamic user creation)

```typescript
import { createClient, SupabaseClient } from '@supabase/supabase-js';

function getSupabaseServiceClient(): SupabaseClient {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  
  if (!url || !key) {
    throw new Error(
      'Missing Supabase env vars. Ensure NEXT_PUBLIC_SUPABASE_URL and ' +
      'SUPABASE_SERVICE_ROLE_KEY are set in .env.local'
    );
  }
  
  return createClient(url, key, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
}

async function createTestUser(
  supabase: SupabaseClient,
  email: string,
  password: string
): Promise<void> {
  const { error } = await supabase.auth.admin.createUser({
    email,
    password,
    email_confirm: true // Auto-confirm email for test users
  });
  
  if (error && !error.message.includes('already exists')) {
    throw new Error(`Failed to create test user: ${error.message}`);
  }
}
```

### Step 4: Authenticate with Playwright

```typescript
import { Page } from 'playwright';

interface AuthResult {
  success: boolean;
  email: string;
  error?: string;
}

async function authenticateWithSupabasePassword(
  page: Page,
  baseUrl: string,
  projectRoot: string
): Promise<AuthResult> {
  // Load config and env
  loadEnv(projectRoot);
  const config = loadAuthConfig(projectRoot);
  const { email, password } = getTestCredentials(config);
  
  try {
    // Create dynamic user if needed
    if (config.testUser.mode === 'dynamic') {
      const supabase = getSupabaseServiceClient();
      await createTestUser(supabase, email, password);
      console.log(`Created dynamic test user: ${email}`);
    }
    
    // Navigate to login
    await page.goto(`${baseUrl}${config.routes.login}`);
    
    // Get selectors (use defaults or custom from config)
    const selectors = config.selectors || {};
    const emailSelector = selectors.emailInput || 'input[type="email"], input[name="email"]';
    const passwordSelector = selectors.passwordInput || 'input[type="password"], input[name="password"]';
    const submitSelector = selectors.submitButton || 'button:has-text("Sign in"), button:has-text("Log in"), button[type="submit"]';
    
    // Wait for login form
    await page.waitForSelector(emailSelector);
    
    // Enter credentials
    await page.fill(emailSelector, email);
    await page.fill(passwordSelector, password);
    
    // Submit
    await page.click(submitSelector);
    
    // Wait for authenticated page
    await page.waitForURL(new RegExp(config.routes.authenticated), { timeout: 10000 });
    console.log(`Authentication successful, landed on ${config.routes.authenticated}`);
    
    return { success: true, email };
    
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Authentication failed: ${message}`);
    return { success: false, email, error: message };
  }
}
```

---

## Complete Script Template

Use this template for screenshot capture or E2E setup:

```typescript
import { chromium } from 'playwright';
import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

// === CONFIGURATION ===
const PROJECT_ROOT = process.cwd();
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5001';

// === HELPER FUNCTIONS ===
// (Include all functions from Steps 1-4 above)

// === MAIN ===
async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();
  
  try {
    const result = await authenticateWithSupabasePassword(page, BASE_URL, PROJECT_ROOT);
    
    if (!result.success) {
      console.error('Authentication failed:', result.error);
      process.exit(1);
    }
    
    console.log(`Logged in as ${result.email}`);
    
    // Now you can navigate to authenticated pages
    // await page.goto(`${BASE_URL}/dashboard`);
    // await page.screenshot({ path: 'dashboard.png' });
    
  } finally {
    await browser.close();
  }
}

main().catch(console.error);
```

---

## Dynamic User Mode

When `testUser.mode` is `"dynamic"`, the skill creates a new user for each test run:

```json
{
  "authentication": {
    "method": "email-password",
    "provider": "supabase",
    "testUser": {
      "mode": "dynamic",
      "emailPattern": "test-{uuid}@testmail.example.com",
      "passwordDefault": "Test123!@#"
    },
    "cleanup": {
      "enabled": true,
      "trigger": "auto",
      "pattern": "test-*@testmail.example.com"
    }
  }
}
```

For dynamic mode:
1. The skill uses Supabase Admin API to create the user
2. Email is auto-confirmed (no verification needed)
3. Consider enabling `cleanup` to remove test users after runs

---

## Configuration Options

### Custom Selectors

If your login form uses non-standard elements:

```json
{
  "authentication": {
    "selectors": {
      "emailInput": "input#login-email",
      "passwordInput": "input#login-password",
      "submitButton": "button.login-btn"
    }
  }
}
```

### Environment Variable Names

Customize which env vars hold credentials:

```json
{
  "authentication": {
    "testUser": {
      "mode": "fixed",
      "emailVar": "E2E_USER_EMAIL",
      "passwordVar": "E2E_USER_PASSWORD"
    }
  }
}
```

---

## Troubleshooting

### "No authentication config found"
Run `/setup-auth` to configure authentication, or manually add the `authentication` section to `docs/project.json`.

### "Missing Supabase env vars"
Ensure `.env.local` contains:
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### "Password not configured"
Set the password via environment variable (recommended) or in project.json:
```
TEST_PASSWORD=your-secure-password
```

### "Invalid login credentials"
- Verify the test user exists in Supabase Auth
- Check that the email is confirmed
- Verify the password is correct
- For dynamic mode, ensure service role key has admin privileges

### "Timeout waiting for authenticated page"
- Check that `routes.authenticated` matches where your app redirects after login
- Verify the dev server is running on the expected port
- Check for JavaScript errors in browser console

---

## Comparison with OTP Method

| Feature | Email/Password | Passwordless OTP |
|---------|----------------|------------------|
| Setup complexity | Lower | Higher (need OTP retrieval) |
| Test user creation | User + password | User only |
| Login speed | Single form | Two-step (email, then code) |
| Production similarity | May differ | Often identical |
| Security in tests | Password in env | Code from database |

Choose email/password when:
- Your app supports both methods
- You want simpler test setup
- Test speed is a priority

---

## Session Reuse

When `authentication.reuseSession` is `true`, save and reuse auth state across tests for faster execution.

### Configuration

```json
{
  "authentication": {
    "method": "email-password",
    "provider": "supabase",
    "reuseSession": true
  }
}
```

### Implementation

```typescript
import { BrowserContext, Browser } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

const AUTH_STATE_FILE = '.tmp/auth-state.json';

async function saveAuthState(context: BrowserContext): Promise<void> {
  const state = await context.storageState();
  fs.mkdirSync(path.dirname(AUTH_STATE_FILE), { recursive: true });
  fs.writeFileSync(AUTH_STATE_FILE, JSON.stringify(state, null, 2));
  console.log(`Auth state saved to ${AUTH_STATE_FILE}`);
}

async function loadAuthState(context: BrowserContext): Promise<boolean> {
  if (!fs.existsSync(AUTH_STATE_FILE)) {
    return false;
  }
  
  try {
    const state = JSON.parse(fs.readFileSync(AUTH_STATE_FILE, 'utf-8'));
    const now = Date.now() / 1000;
    
    // Check if auth cookies are expired
    const isExpired = state.cookies?.some((c: any) => 
      c.name.includes('auth') && c.expires && c.expires < now
    );
    
    if (isExpired) {
      console.log('Saved auth state expired');
      fs.unlinkSync(AUTH_STATE_FILE);
      return false;
    }
    
    await context.addCookies(state.cookies || []);
    console.log('Loaded cached auth state');
    return true;
  } catch {
    return false;
  }
}

async function getAuthenticatedContext(browser: Browser): Promise<BrowserContext> {
  const config = loadAuthConfig(PROJECT_ROOT);
  const context = await browser.newContext();
  
  if (config.reuseSession && await loadAuthState(context)) {
    // Verify session is still valid
    const page = await context.newPage();
    await page.goto(`${BASE_URL}${config.routes?.authenticated || '/dashboard'}`);
    
    if (!page.url().includes(config.routes?.login || '/login')) {
      await page.close();
      return context; // Session is valid
    }
    await page.close();
  }
  
  // Authenticate fresh
  const page = await context.newPage();
  await authenticateWithSupabasePassword(page, BASE_URL, PROJECT_ROOT);
  
  if (config.reuseSession) {
    await saveAuthState(context);
  }
  
  return context;
}
```

### Performance Gain

| Approach | Login time |
|----------|------------|
| Fresh login each test | ~2-3 seconds |
| Session reuse | ~0 seconds |

---

## Integration with Other Skills

This skill is used by:
- `screenshot` - for capturing authenticated page screenshots
- `ui-tester-playwright` - for E2E test authentication
- `qa-browser-tester` - for QA testing authenticated flows
- `auth-headless` - can use this skill's API auth pattern

Agents should:
1. Check if `project.json` has `authentication` config
2. Load this skill if `provider` is `supabase` and `method` is `email-password`
3. Call `authenticateWithSupabasePassword()` before accessing protected pages
