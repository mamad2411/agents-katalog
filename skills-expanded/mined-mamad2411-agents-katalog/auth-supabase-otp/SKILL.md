---
name: auth-supabase-otp
description: "Authenticate with Supabase passwordless OTP (email code) for testing. Use when project.json has authentication.provider: supabase and authentication.method: passwordless-otp. Triggers on: supabase login, otp auth, passwordless auth, email code login."
---

# Supabase Passwordless OTP Authentication

Authenticate with a Supabase-powered application using passwordless email OTP codes for testing purposes.

---

## Prerequisites

1. **Project configuration** in `docs/project.json`:
   ```json
   {
     "authentication": {
       "method": "passwordless-otp",
       "provider": "supabase",
       "testUser": {
         "mode": "fixed",
         "emailVar": "TEST_EMAIL",
         "emailDefault": "test@example.com"
       },
       "verification": {
         "source": "supabase",
         "table": "users",
         "column": "verification_code",
         "lookupBy": "email"
       },
       "routes": {
         "login": "/login",
         "verify": "/verify",
         "authenticated": "/dashboard"
       }
     }
   }
   ```

2. **Environment variables** in `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJ...
   TEST_EMAIL=test@example.com  # Optional, uses emailDefault if not set
   ```

3. **Test user exists** in the database (for fixed mode)

---

## The Job

1. Read authentication config from `project.json`
2. Navigate to login page
3. Enter test email and submit
4. Wait for redirect to verification page
5. Fetch OTP code from database using service role
6. Enter OTP code and submit
7. Wait for redirect to authenticated page
8. Return authenticated page context

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
  };
  verification: {
    source: string;
    table: string;
    column: string;
    lookupBy: string;
  };
  routes: {
    login: string;
    verify: string;
    authenticated: string;
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

function getTestEmail(config: AuthConfig): string {
  if (config.testUser.mode === 'dynamic') {
    const uuid = crypto.randomUUID().slice(0, 8);
    const pattern = config.testUser.emailPattern || 'test-{uuid}@example.com';
    return pattern.replace('{uuid}', uuid);
  }
  
  // Fixed mode
  const envVar = config.testUser.emailVar || 'TEST_EMAIL';
  return process.env[envVar] || config.testUser.emailDefault || 'test@example.com';
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

### Step 3: Create Supabase Service Client

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
```

### Step 4: Fetch Verification Code

```typescript
async function getVerificationCode(
  supabase: SupabaseClient,
  config: AuthConfig,
  email: string
): Promise<string> {
  const { table, column, lookupBy } = config.verification;
  
  const { data, error } = await supabase
    .from(table)
    .select(column)
    .eq(lookupBy, email)
    .single();
  
  if (error || !data?.[column]) {
    throw new Error(
      `Failed to get verification code from ${table}.${column} ` +
      `for ${lookupBy}=${email}: ${error?.message || 'No code found'}`
    );
  }
  
  return data[column];
}
```

### Step 5: Authenticate with Playwright

```typescript
import { Page, BrowserContext } from 'playwright';

interface AuthResult {
  success: boolean;
  email: string;
  error?: string;
}

async function authenticateWithSupabaseOTP(
  page: Page,
  baseUrl: string,
  projectRoot: string
): Promise<AuthResult> {
  // Load config and env
  loadEnv(projectRoot);
  const config = loadAuthConfig(projectRoot);
  const email = getTestEmail(config);
  const supabase = getSupabaseServiceClient();
  
  try {
    // Navigate to login
    await page.goto(`${baseUrl}${config.routes.login}`);
    await page.waitForSelector('input[type="email"]');
    
    // Enter email
    await page.fill('input[type="email"]', email);
    await page.click('button:has-text("Continue"), button:has-text("Sign in"), button[type="submit"]');
    
    // Wait for verify page
    await page.waitForURL(new RegExp(config.routes.verify));
    await page.waitForTimeout(1000); // Allow code to be stored in DB
    
    // Fetch code from database
    const code = await getVerificationCode(supabase, config, email);
    console.log(`Retrieved verification code for ${email}`);
    
    // Enter code - handle both single input and multiple input formats
    const otpInputs = page.locator('input[maxlength="1"]');
    const inputCount = await otpInputs.count();
    
    if (inputCount >= 6) {
      // Multiple single-digit inputs
      for (let i = 0; i < 6; i++) {
        await otpInputs.nth(i).fill(code[i]);
      }
    } else {
      // Single input for full code
      const singleInput = page.locator('input[type="text"], input[inputmode="numeric"]').first();
      await singleInput.fill(code);
    }
    
    // Submit verification
    await page.click('button:has-text("Verify"), button:has-text("Submit"), button[type="submit"]');
    
    // Wait for authenticated page
    await page.waitForURL(new RegExp(config.routes.authenticated));
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
// (Include all functions from Steps 1-5 above)

// === MAIN ===
async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();
  
  try {
    const result = await authenticateWithSupabaseOTP(page, BASE_URL, PROJECT_ROOT);
    
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

When `testUser.mode` is `"dynamic"`, the skill generates a unique email for each test run:

```typescript
// In project.json:
{
  "authentication": {
    "testUser": {
      "mode": "dynamic",
      "emailPattern": "test-{uuid}@testmail.example.com"
    }
  }
}
```

For dynamic mode to work:
1. The application must accept any email (not validate against existing users)
2. The verification code must be created when the email is submitted
3. Consider enabling `cleanup` to remove test users after runs

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

### "Failed to get verification code"
- Check that the test user exists in the database
- Verify the `verification.table`, `verification.column`, and `verification.lookupBy` values match your schema
- Ensure the service role key has permission to read the users table

### "Authentication successful but page not loading"
- Check that `routes.authenticated` matches where your app redirects after login
- Verify the dev server is running on the expected port

### OTP input not found
If your app uses a different OTP input pattern, configure custom selectors:
```json
{
  "authentication": {
    "selectors": {
      "otpInputs": "input.otp-digit",
      "verifyButton": "button.verify-btn"
    }
  }
}
```

---

## Session Reuse

When `authentication.reuseSession` is `true`, save and reuse auth state across tests:

### Save Auth State After Login

```typescript
import { BrowserContext } from 'playwright';
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
    // Check if state is still valid (not expired)
    // For Supabase, check cookie expiry
    const now = Date.now() / 1000;
    const isExpired = state.cookies?.some((c: any) => 
      c.name.includes('auth') && c.expires && c.expires < now
    );
    
    if (isExpired) {
      console.log('Saved auth state expired, will re-authenticate');
      fs.unlinkSync(AUTH_STATE_FILE);
      return false;
    }
    
    // Load cookies into context
    await context.addCookies(state.cookies || []);
    console.log('Loaded auth state from cache');
    return true;
  } catch (error) {
    console.warn('Failed to load auth state:', error);
    return false;
  }
}
```

### Usage in Tests

```typescript
async function getAuthenticatedContext(browser: Browser): Promise<BrowserContext> {
  const config = loadAuthConfig(PROJECT_ROOT);
  const context = await browser.newContext();
  
  // Try to load cached state first
  if (config.reuseSession) {
    const loaded = await loadAuthState(context);
    if (loaded) {
      // Verify session is still valid by checking a protected page
      const page = await context.newPage();
      await page.goto(`${BASE_URL}${config.routes?.authenticated || '/dashboard'}`);
      
      // If we're still on the authenticated page (not redirected to login), we're good
      if (!page.url().includes(config.routes?.login || '/login')) {
        await page.close();
        return context;
      }
      await page.close();
      console.log('Cached session invalid, re-authenticating');
    }
  }
  
  // Authenticate fresh
  const page = await context.newPage();
  await authenticateWithSupabaseOTP(page, BASE_URL, PROJECT_ROOT);
  
  // Save state for reuse
  if (config.reuseSession) {
    await saveAuthState(context);
  }
  
  return context;
}
```

### Clear State at Test Run Start

```typescript
// In playwright.config.ts globalSetup or test setup
function clearAuthState(): void {
  if (fs.existsSync(AUTH_STATE_FILE)) {
    fs.unlinkSync(AUTH_STATE_FILE);
    console.log('Cleared cached auth state');
  }
}
```

---

## Integration with Other Skills

This skill is used by:
- `screenshot` — for capturing authenticated page screenshots
- `ui-tester-playwright` — for E2E test authentication
- `qa-browser-tester` — for QA testing authenticated flows

Agents should:
1. Check if `project.json` has `authentication` config
2. Load this skill if `provider` is `supabase` and `method` is `passwordless-otp`
3. Call `authenticateWithSupabaseOTP()` before accessing protected pages
