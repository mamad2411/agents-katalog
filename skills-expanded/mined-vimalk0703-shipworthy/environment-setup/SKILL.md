---
name: environment-setup
description: Eliminates the number one blocker for non-technical users — environment variable configuration. Explains what .env files are, auto-generates .env.example, provides step-by-step guides for getting API keys, and validates setup at startup.
invoke_when: Use when setting up a project for the first time, adding a new service integration, encountering "missing environment variable" errors, or configuring API keys, secrets, or .env files.
---

# Environment Setup

## What Are .env Files? (Plain Language)

Your app needs secret information to work — database passwords, API keys, service credentials. You can't put these directly in your code because:

1. **Security:** If your code is on GitHub, anyone can see your secrets
2. **Flexibility:** Different environments (your laptop vs the live site) need different values
3. **Team safety:** Each developer has their own keys; you don't share secrets in code

A `.env` file is a simple text file that sits on your computer (and ONLY your computer) containing these secrets. It looks like this:

```
# Database connection
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Stripe payment processing
STRIPE_SECRET_KEY=sk_test_abc123
STRIPE_PUBLISHABLE_KEY=pk_test_xyz789
```

Your app reads these values when it starts up. The `.env` file is listed in `.gitignore` so it never gets uploaded to GitHub.

---

## The .env.example File

Every project MUST have a `.env.example` file. This is a template that shows what variables are needed WITHOUT revealing actual secret values.

### Auto-Generate Template

When setting up a project or adding a new service, always create or update `.env.example`:

```bash
# =============================================================
# Environment Variables
# Copy this file to .env and fill in your values:
#   cp .env.example .env
# =============================================================

# ----- DATABASE -----
# Your Supabase database connection string
# Get it: Supabase Dashboard > Project Settings > Database > Connection string
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# Supabase anonymous (public) key — safe to expose in the browser
# Get it: Supabase Dashboard > Project Settings > API > anon/public key
NEXT_PUBLIC_SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

# Supabase service role key — NEVER expose this in the browser
# Get it: Supabase Dashboard > Project Settings > API > service_role key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# ----- AUTHENTICATION -----
# NextAuth secret — random string for encrypting session tokens
# Generate one: openssl rand -base64 32
NEXTAUTH_SECRET=generate-a-random-string-here
NEXTAUTH_URL=http://localhost:3000

# Google OAuth (optional — for "Sign in with Google")
# Get it: https://console.cloud.google.com/apis/credentials
# Create OAuth 2.0 Client ID, set redirect URI to http://localhost:3000/api/auth/callback/google
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# ----- PAYMENTS -----
# Stripe API keys
# Get it: https://dashboard.stripe.com/test/apikeys
# Use TEST keys during development (start with sk_test_ and pk_test_)
STRIPE_SECRET_KEY=sk_test_your-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your-key-here

# Stripe webhook secret for verifying webhook signatures
# Get it: https://dashboard.stripe.com/test/webhooks — click your endpoint, reveal signing secret
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret-here

# ----- EMAIL -----
# Resend API key for sending emails
# Get it: https://resend.com/api-keys — create a new key
RESEND_API_KEY=re_your-api-key-here

# ----- APP CONFIG -----
# Your app's public URL (no trailing slash)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Rules for .env.example:**
- Every variable that the app needs MUST be listed
- Include a comment explaining what it is and where to get the value
- Use placeholder values, never real secrets
- Group related variables with section headers
- Mark which variables are safe for the browser (NEXT_PUBLIC_) vs secret

---

## Where to Get Common API Keys

### Supabase (Database + Auth)
1. Go to [supabase.com](https://supabase.com) and sign in (or create an account — it's free)
2. Click "New Project" and give it a name
3. Set a database password (save this somewhere — you'll need it)
4. Wait about 2 minutes for the project to be created
5. Go to **Project Settings** (gear icon in the left sidebar)
6. Click **API** in the settings menu
7. You'll see:
   - **Project URL** — this is your `NEXT_PUBLIC_SUPABASE_URL`
   - **anon/public key** — this is your `NEXT_PUBLIC_SUPABASE_ANON_KEY` (safe for browsers)
   - **service_role key** — this is your `SUPABASE_SERVICE_ROLE_KEY` (keep secret!)
8. Click **Database** in the settings menu for your `DATABASE_URL`

### Stripe (Payments)
1. Go to [dashboard.stripe.com](https://dashboard.stripe.com) and sign in (or create an account)
2. Make sure you're in **Test mode** (toggle in the top-right says "Test mode")
3. Go to **Developers > API keys**
4. You'll see:
   - **Publishable key** (starts with `pk_test_`) — this is your `STRIPE_PUBLISHABLE_KEY`
   - **Secret key** (starts with `sk_test_`) — click "Reveal" — this is your `STRIPE_SECRET_KEY`
5. For webhooks: Go to **Developers > Webhooks > Add endpoint**
   - URL: `https://your-domain.com/api/webhooks/stripe` (for local dev, use Stripe CLI)
   - Select events you want to listen for
   - After creating, click the endpoint and find "Signing secret" — this is your `STRIPE_WEBHOOK_SECRET`

### Resend (Email)
1. Go to [resend.com](https://resend.com) and sign in (or create an account)
2. Go to **API Keys** in the sidebar
3. Click **Create API Key**
4. Give it a name (like "my-app-dev") and choose permissions (Full access for development)
5. Copy the key (starts with `re_`) — this is your `RESEND_API_KEY`
6. Important: you can only see the key once. If you lose it, create a new one.

### Google OAuth (Sign in with Google)
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or select existing)
3. Go to **APIs & Services > Credentials**
4. Click **Create Credentials > OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Add authorized redirect URI: `http://localhost:3000/api/auth/callback/google`
7. Click **Create**
8. You'll see your **Client ID** and **Client Secret** — these are your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
9. For production, add your real domain to the redirect URIs

### NextAuth Secret
This isn't an API key — it's a random string your app uses to encrypt session data. Generate one:
```bash
openssl rand -base64 32
```
Copy the output and use it as your `NEXTAUTH_SECRET`. Any random string works, but make it long and unpredictable.

---

## NEXT_PUBLIC_ Prefix Explained

In Next.js, environment variables are SECRET by default — they only exist on the server.

To make a variable available in the browser (client-side), prefix it with `NEXT_PUBLIC_`.

### What's SAFE to Expose (Use NEXT_PUBLIC_)
- Supabase anon key (`NEXT_PUBLIC_SUPABASE_ANON_KEY`) — designed to be public, Row Level Security protects your data
- Supabase project URL (`NEXT_PUBLIC_SUPABASE_URL`) — just a URL, not a secret
- Stripe publishable key (`STRIPE_PUBLISHABLE_KEY`) — designed to be public
- Your app's URL (`NEXT_PUBLIC_APP_URL`) — obviously public
- Analytics IDs (Google Analytics, Plausible) — public tracking codes
- Feature flags that are non-sensitive

### What MUST Stay Secret (NO NEXT_PUBLIC_ Prefix)
- Database URLs (`DATABASE_URL`) — contains password
- Supabase service role key (`SUPABASE_SERVICE_ROLE_KEY`) — bypasses Row Level Security
- Stripe secret key (`STRIPE_SECRET_KEY`) — can charge cards
- Stripe webhook secret (`STRIPE_WEBHOOK_SECRET`) — verifies webhook authenticity
- Resend API key (`RESEND_API_KEY`) — can send emails as you
- NextAuth secret (`NEXTAUTH_SECRET`) — encrypts sessions
- Any password, token, or secret key

**The Rule:** If someone with this value could do something harmful (charge money, read private data, send emails, access your database), it MUST NOT have `NEXT_PUBLIC_` prefix.

---

## Development vs Production Variables

You'll have at least two sets of values:

### Development (Your Computer)
```
DATABASE_URL=postgresql://postgres:localpassword@localhost:5432/mydb
STRIPE_SECRET_KEY=sk_test_...    # Test key — no real charges
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Production (Live Site)
```
DATABASE_URL=postgresql://postgres:prodpassword@db.abc123.supabase.co:5432/postgres
STRIPE_SECRET_KEY=sk_live_...    # Live key — real charges!
NEXT_PUBLIC_APP_URL=https://myapp.com
```

**How to manage this:**
- `.env` or `.env.local` — your local development values (never committed to git)
- Production values — set in your hosting provider's dashboard (Vercel > Settings > Environment Variables)
- Never copy production secrets to your local `.env` unless you have a specific reason

---

## Startup Validation

Every project should crash immediately with a clear message if required environment variables are missing. This saves hours of debugging mysterious errors.

### Implementation

Add this to your project's startup (e.g., `lib/env.ts` or `config/env.ts`):

```typescript
// lib/env.ts — Validate environment variables at startup

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${name}\n` +
      `Check your .env file. See .env.example for setup instructions.`
    );
  }
  return value;
}

function optionalEnv(name: string, defaultValue: string = ''): string {
  return process.env[name] || defaultValue;
}

// Required — app won't start without these
export const env = {
  DATABASE_URL: requireEnv('DATABASE_URL'),
  NEXTAUTH_SECRET: requireEnv('NEXTAUTH_SECRET'),

  // Required for payments (only if payments are enabled)
  // STRIPE_SECRET_KEY: requireEnv('STRIPE_SECRET_KEY'),

  // Optional with defaults
  APP_URL: optionalEnv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000'),
};
```

Then import `env` instead of using `process.env` directly throughout your app. If any required variable is missing, the app crashes on startup with a message like:

```
Error: Missing required environment variable: DATABASE_URL
Check your .env file. See .env.example for setup instructions.
```

This is infinitely better than discovering 10 minutes into debugging that your database URL is undefined.

---

## .gitignore Check

Every time you set up or modify environment configuration, verify that `.gitignore` includes:

```
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
```

**If `.env` is NOT in `.gitignore`, add it immediately.** This is a security-critical step. If `.env` was ever committed to git history, consider all secrets in it compromised — rotate every key.

### How to Check
```bash
# Check if .env is in .gitignore
grep -q "^\.env$" .gitignore && echo "OK: .env is in .gitignore" || echo "WARNING: .env is NOT in .gitignore — add it now!"

# Check if .env was ever committed
git log --all --oneline -- .env
# If this shows any results, those secrets may be compromised
```

---

## Quick Start for New Projects

When a user starts a new project, run through this checklist:

1. Create `.env.example` with all required variables and plain-language comments
2. Create `.env` by copying `.env.example`
3. Verify `.env` is in `.gitignore`
4. Help the user get each API key (link to the service, step-by-step)
5. Add startup validation (`lib/env.ts`)
6. Test that the app starts successfully with all variables set
7. Test that the app crashes clearly when a required variable is missing
