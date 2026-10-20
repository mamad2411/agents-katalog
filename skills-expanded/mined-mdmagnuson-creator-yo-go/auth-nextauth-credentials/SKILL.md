---
name: auth-nextauth-credentials
description: "Authenticate with NextAuth.js credentials provider for testing. Use when project.json has authentication.provider: nextauth and authentication.method: email-password. Triggers on: nextauth login, next-auth credentials, nextauth password."
---

# NextAuth.js Credentials Authentication

Authenticate with a NextAuth.js-powered application using the credentials provider for testing purposes.

---

## Prerequisites

1. **Project configuration** in `docs/project.json`:
   ```json
   {
     "authentication": {
       "method": "email-password",
       "provider": "nextauth",
       "testUser": {
         "mode": "fixed",
         "emailVar": "TEST_EMAIL",
         "emailDefault": "test@example.com",
         "passwordVar": "TEST_PASSWORD"
       },
       "routes": {
         "login": "/auth/signin",
         "authenticated": "/dashboard"
       }
     }
   }
   ```

2. **Environment variables** in `.env.local`:
   ```
   TEST_EMAIL=test@example.com
   TEST_PASSWORD=your-test-password
   ```

3. **Test user exists** in your database with hashed password

---

## NextAuth Configuration Requirements

Your NextAuth configuration should include a credentials provider:

```typescript
// pages/api/auth/[...nextauth].ts or app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        // Your authentication logic
        const user = await validateUser(credentials.email, credentials.password);
        if (user) return user;
        return null;
      }
    })
  ],
  pages: {
    signIn: '/auth/signin'  // Custom sign-in page (optional)
  }
});
```

---

## The Job

1. Read authentication config from `project.json`
2. Navigate to NextAuth sign-in page
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
    csrfEndpoint?: string;
  };
  selectors?: {
    emailInput?: string;
    passwordInput?: string;
    submitButton?: string;
    credentialsForm?: string;
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
    password = process.env[config.testUser.passwordVar || 'TEST_PASSWORD'] 
      || config.testUser.passwordDefault 
      || 'Test123!@#';
  } else {
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

### Step 3: Authenticate with Playwright

```typescript
import { Page } from 'playwright';

interface AuthResult {
  success: boolean;
  email: string;
  error?: string;
}

async function authenticateWithNextAuth(
  page: Page,
  baseUrl: string,
  projectRoot: string
): Promise<AuthResult> {
  loadEnv(projectRoot);
  const config = loadAuthConfig(projectRoot);
  const { email, password } = getTestCredentials(config);
  
  try {
    // Navigate to login page
    const loginUrl = `${baseUrl}${config.routes.login}`;
    await page.goto(loginUrl);
    
    // Get selectors
    const selectors = config.selectors || {};
    
    // NextAuth default sign-in page has provider buttons
    // If using custom page, skip this step
    const credentialsFormSelector = selectors.credentialsForm || 
      'form[action*="credentials"], form[action*="callback/credentials"]';
    
    // Check if we need to click a "Sign in with Credentials" button first
    const credentialsButton = page.locator('button:has-text("Credentials"), button:has-text("Sign in with Email")');
    if (await credentialsButton.count() > 0) {
      await credentialsButton.first().click();
      await page.waitForTimeout(500);
    }
    
    // Fill credentials
    const emailSelector = selectors.emailInput || 
      'input[name="email"], input[type="email"], input#email';
    const passwordSelector = selectors.passwordInput || 
      'input[name="password"], input[type="password"], input#password';
    const submitSelector = selectors.submitButton || 
      'button[type="submit"], button:has-text("Sign in"), button:has-text("Log in")';
    
    await page.waitForSelector(emailSelector);
    await page.fill(emailSelector, email);
    await page.fill(passwordSelector, password);
    
    // Submit form
    await page.click(submitSelector);
    
    // Wait for redirect to authenticated page
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

```typescript
import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

const PROJECT_ROOT = process.cwd();
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000';

// (Include helper functions from above)

async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();
  
  try {
    const result = await authenticateWithNextAuth(page, BASE_URL, PROJECT_ROOT);
    
    if (!result.success) {
      console.error('Authentication failed:', result.error);
      process.exit(1);
    }
    
    console.log(`Logged in as ${result.email}`);
    
    // Navigate to authenticated pages
    // await page.goto(`${BASE_URL}/dashboard`);
    
  } finally {
    await browser.close();
  }
}

main().catch(console.error);
```

---

## Dynamic User Mode

For dynamic test users with NextAuth, you need a way to create users in your database:

```json
{
  "authentication": {
    "method": "email-password",
    "provider": "nextauth",
    "testUser": {
      "mode": "dynamic",
      "emailPattern": "test-{uuid}@testmail.example.com",
      "passwordDefault": "Test123!@#"
    },
    "dynamicUserCreation": {
      "type": "prisma",
      "model": "User",
      "passwordHashField": "hashedPassword"
    }
  }
}
```

### Prisma User Creation Helper

```typescript
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

async function createTestUser(email: string, password: string): Promise<void> {
  const prisma = new PrismaClient();
  
  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    
    await prisma.user.upsert({
      where: { email },
      update: { hashedPassword },
      create: {
        email,
        hashedPassword,
        emailVerified: new Date()
      }
    });
  } finally {
    await prisma.$disconnect();
  }
}
```

---

## Default vs Custom Sign-in Pages

### Using NextAuth Default Sign-in Page

If you use NextAuth's built-in sign-in page (`/api/auth/signin`):

```json
{
  "authentication": {
    "routes": {
      "login": "/api/auth/signin"
    }
  }
}
```

The skill will:
1. Navigate to `/api/auth/signin`
2. Click the "Sign in with Credentials" button if multiple providers exist
3. Fill and submit the credentials form

### Using Custom Sign-in Page

If you have a custom sign-in page:

```json
{
  "authentication": {
    "routes": {
      "login": "/auth/signin"
    },
    "selectors": {
      "emailInput": "input#email",
      "passwordInput": "input#password",
      "submitButton": "button#signin-btn"
    }
  }
}
```

---

## Handling CSRF Tokens

NextAuth uses CSRF protection. The skill handles this automatically when submitting through the UI. For headless authentication, see the `auth-headless` skill.

---

## Troubleshooting

### "CredentialsSignin" error
- Verify the test user exists in your database
- Check password hash algorithm matches your authorize function
- Verify email is verified (if your app requires it)

### "No authentication config found"
Run `/setup-auth` to configure authentication.

### Form not found
NextAuth default sign-in page structure may vary. Configure custom selectors:
```json
{
  "authentication": {
    "selectors": {
      "credentialsForm": "form[action*='credentials']",
      "emailInput": "input[name='email']",
      "passwordInput": "input[name='password']"
    }
  }
}
```

### Multiple providers on sign-in page
The skill will click the Credentials button first. If your button has different text:
```json
{
  "authentication": {
    "selectors": {
      "providerButton": "button:has-text('Email and Password')"
    }
  }
}
```

### Redirect loop after login
Check your NextAuth `callbacks` configuration and ensure the `redirect` callback allows your authenticated route.

---

## Database Adapter Considerations

NextAuth works with various database adapters. Test user setup varies:

| Adapter | User Creation |
|---------|---------------|
| Prisma | Use Prisma client directly |
| Drizzle | Use Drizzle query |
| MongoDB | Use MongoDB client |
| TypeORM | Use TypeORM repository |

Ensure your test user has:
- Valid email
- Properly hashed password (matching your authorize logic)
- Email verified (if required)
- Any required relations (accounts, sessions)

---

## Integration with Other Skills

This skill is used by:
- `screenshot` - for capturing authenticated page screenshots
- `ui-tester-playwright` - for E2E test authentication
- `qa-browser-tester` - for QA testing authenticated flows

Agents should:
1. Check if `project.json` has `authentication` config
2. Load this skill if `provider` is `nextauth` and `method` is `email-password`
3. Call `authenticateWithNextAuth()` before accessing protected pages
