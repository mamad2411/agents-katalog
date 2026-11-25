---
name: vercel-deployment
description: Use when deploying to Vercel - covers Fluid Compute (timeout issues, 60s bug), vercel.json configuration, maxDuration settings, cron jobs, environment variables (printf gotcha), monorepo setup, Next.js issues, and common build errors
---

# Vercel Deployment

## When to Use This Skill

- Configuring `vercel.json` for deployments
- Setting environment variables via CLI
- Deploying monorepos
- Troubleshooting build failures
- Understanding preview vs production deployments

---

## vercel.json Configuration

### Minimal Configuration

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json"
}
```

Most projects don't need `vercel.json` - Vercel auto-detects frameworks.

### Common Configuration

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  }
}
```

### Redirects and Rewrites

```json
{
  "redirects": [
    { "source": "/old-page", "destination": "/new-page", "permanent": true }
  ],
  "rewrites": [
    { "source": "/api/:path*", "destination": "https://api.example.com/:path*" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

---

## Environment Variables

### Critical Gotcha: Trailing Newlines

<EXTREMELY-IMPORTANT>
When piping values to `vercel env add`, use `printf`, NEVER `echo`.

`echo` adds a trailing newline that becomes part of the value, breaking API keys and secrets.
</EXTREMELY-IMPORTANT>

```bash
# ❌ WRONG - echo adds trailing newline
echo "sk-abc123" | vercel env add SECRET_KEY production

# ✅ CORRECT - printf has no trailing newline
printf "sk-abc123" | vercel env add SECRET_KEY production

# ✅ ALSO CORRECT - interactive prompt
vercel env add SECRET_KEY production
# Then paste value when prompted
```

**Symptoms of trailing newline bug:**
- API calls fail with "invalid key"
- Authentication errors despite correct credentials
- Value looks correct in dashboard but doesn't work

**Diagnosis:**
```bash
# Check for trailing newline
vercel env pull .env.local
cat -A .env.local | grep SECRET_KEY
# If you see SECRET_KEY=sk-abc123$ - no newline (good)
# If you see SECRET_KEY=sk-abc123\n$ - has newline (bad)
```

### Environment Types

| Type | When Used | Example |
|------|-----------|---------|
| `production` | Production deployments only | API keys, database URLs |
| `preview` | Preview deployments (PRs, branches) | Staging API keys |
| `development` | Local dev via `vercel dev` | Local overrides |

```bash
# Add to production only
vercel env add API_KEY production

# Add to all environments
vercel env add API_KEY production preview development

# Pull to local .env
vercel env pull .env.local
```

### Framework-Specific Prefixes

| Framework | Public Prefix | Private (server-only) |
|-----------|--------------|----------------------|
| Next.js | `NEXT_PUBLIC_*` | No prefix |
| Vite | `VITE_*` | No prefix |
| Create React App | `REACT_APP_*` | No prefix |

```bash
# Client-accessible (bundled into JS)
vercel env add NEXT_PUBLIC_API_URL production

# Server-only (API routes, SSR)
vercel env add DATABASE_URL production
```

---

## Monorepo Deployment

### Root Configuration

```json
// vercel.json at repo root
{
  "buildCommand": "cd apps/web && npm run build",
  "outputDirectory": "apps/web/dist",
  "installCommand": "npm install",
  "rootDirectory": "apps/web"
}
```

### Multiple Apps from One Repo

Create separate Vercel projects, each with different `rootDirectory`:

**Project 1 (Web App):**
```json
{
  "rootDirectory": "apps/web"
}
```

**Project 2 (API):**
```json
{
  "rootDirectory": "apps/api"
}
```

### Turborepo / pnpm Workspaces

```json
{
  "buildCommand": "cd ../.. && pnpm turbo build --filter=web",
  "outputDirectory": ".next",
  "rootDirectory": "apps/web"
}
```

**Common issue:** Build fails because dependencies aren't installed.

**Fix:** Set install command at root level:
```json
{
  "installCommand": "cd ../.. && pnpm install",
  "buildCommand": "cd ../.. && pnpm turbo build --filter=web",
  "rootDirectory": "apps/web"
}
```

---

## Next.js Specific

### Common Build Errors

**Error: `useX must be used within Provider`**

```
Error: useAuth must be used within an AuthProvider
Error occurred prerendering page "/dashboard"
```

**Cause:** Next.js tries to statically prerender pages that use React Context.

**Fix:** Wrap providers in `layout.tsx`:

```tsx
// src/components/Providers.tsx
'use client'

export default function Providers({ children }) {
  return <AuthProvider>{children}</AuthProvider>
}

// src/app/layout.tsx
import Providers from '../components/Providers'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

---

**Error: `NEXT_PUBLIC_* undefined at build time`**

**Cause:** Environment variable not set in Vercel project settings.

**Fix:**
1. Add variable in Vercel dashboard → Settings → Environment Variables
2. Or use `vercel env add NEXT_PUBLIC_API_URL production`
3. Redeploy (env vars are baked in at build time for `NEXT_PUBLIC_*`)

---

**Error: `Dynamic server usage` / `opted out of static rendering`**

```
Error: Dynamic server usage: cookies
Route /dashboard couldn't be rendered statically
```

**Cause:** Using dynamic functions (`cookies()`, `headers()`) in pages Vercel tries to statically generate.

**Fix:** Export dynamic route config:

```tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic'

// Or force static
export const dynamic = 'force-static'
```

---

### Output Modes

```js
// next.config.js
module.exports = {
  output: 'standalone',  // For Docker/self-hosting
  // output: 'export',   // Static HTML export (no server features)
}
```

**Vercel auto-detects** - usually don't need to set this.

---

## Preview Deployments

### Automatic Previews

Every push to a non-production branch creates a preview deployment:
- `feature-branch` → `project-feature-branch-xxx.vercel.app`
- PR comments show preview URL automatically

### Preview Environment Variables

Preview deployments use `preview` environment variables:

```bash
# Production database
vercel env add DATABASE_URL production
# Value: postgres://prod-db...

# Preview/staging database
vercel env add DATABASE_URL preview
# Value: postgres://staging-db...
```

### Disable Previews

```json
// vercel.json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "feature/*": false
    }
  }
}
```

---

## CLI Commands

### Installation & Auth

```bash
npm install -g vercel
vercel login
vercel whoami
```

### Deployment

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Deploy without prompts
vercel --prod --yes

# Deploy specific directory
vercel ./dist --prod
```

### Project Management

```bash
# Link local project to Vercel
vercel link

# List deployments
vercel list

# View deployment logs
vercel logs <deployment-url>

# Inspect deployment
vercel inspect <deployment-url>

# Promote deployment to production
vercel promote <deployment-url>
```

### Environment Variables

```bash
# List env vars
vercel env ls

# Add env var
vercel env add VAR_NAME production

# Remove env var
vercel env rm VAR_NAME production

# Pull env vars to local file
vercel env pull .env.local
```

### Rollback

```bash
# List recent deployments
vercel list

# Promote previous deployment to production
vercel promote <previous-deployment-url>

# Or instant rollback in dashboard
# Deployments → ... → Promote to Production
```

---

## Serverless Functions

### API Routes (Next.js)

```typescript
// app/api/hello/route.ts (App Router)
export async function GET(request: Request) {
  return Response.json({ message: 'Hello' })
}

// pages/api/hello.ts (Pages Router)
export default function handler(req, res) {
  res.status(200).json({ message: 'Hello' })
}
```

### Standalone Functions

```typescript
// api/hello.ts
import type { VercelRequest, VercelResponse } from '@vercel/node'

export default function handler(req: VercelRequest, res: VercelResponse) {
  res.status(200).json({ message: 'Hello' })
}
```

### Function Configuration

```json
// vercel.json
{
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,      // MB (128-3008)
      "maxDuration": 30    // seconds (max 300 on Pro)
    }
  }
}
```

### Edge Functions

```typescript
// app/api/edge/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  return new Response('Hello from the edge!')
}
```

**Edge vs Serverless:**
| Feature | Edge | Serverless |
|---------|------|------------|
| Cold start | ~0ms | 250-500ms |
| Memory | 128MB | Up to 3GB |
| Duration | 30s | Up to 300s |
| Node.js APIs | Limited | Full |
| Location | All regions | Selected region |

---

## Async Operations & Background Tasks

### Critical: Vercel Kills Background Tasks

<EXTREMELY-IMPORTANT>
Vercel terminates serverless functions as soon as the response is sent. Any background async tasks (IIFE, `.then()`, `.catch()`) may not complete.
</EXTREMELY-IMPORTANT>

```typescript
// ❌ BROKEN - Vercel may kill this before completion
;(async () => {
  const email = await lookupEmail(phone)  // Takes 500ms
  await sendEmail(email, content)          // Never runs!
})().catch(err => console.error(err))

return NextResponse.json({ success: true }) // Response sent, function dies
```

```typescript
// ✅ WORKING - Everything completes before response
const email = await lookupEmail(phone)
try {
  await sendEmail(email, content)
} catch (err) {
  console.error('Email failed:', err)
}
return NextResponse.json({ success: true })
```

**Trade-off:** Response is slower (adds ~1-2s) but async operations are guaranteed to complete.

### External API Timeouts

Fetch requests to external APIs can hang indefinitely on Vercel, causing the function to timeout without completing.

```typescript
// Add AbortController with explicit timeout
const controller = new AbortController()
const timeoutId = setTimeout(() => controller.abort(), 8000) // 8s timeout

const response = await fetch(url, {
  headers: { 'Referer': 'https://example.com/' },
  signal: controller.signal,
})
clearTimeout(timeoutId)
```

### Recommended Pattern for Notifications

```typescript
export async function POST(req: NextRequest) {
  // ... validation and business logic ...

  // Do email lookup in main request flow (not background)
  const email = phoneNumber ? await lookupEmailByPhone(phoneNumber) : null

  // Send notification synchronously (await ensures completion)
  if (phoneNumber) {
    try {
      if (email) {
        await sendEmail({ to: email, ...params })
      } else {
        await sendSMS({ to: phoneNumber, ...params })
      }
    } catch (err) {
      console.error('[Notification] Failed:', err)
      // Don't fail the request if notification fails
    }
  }

  return NextResponse.json({ success: true })
}
```

### Debugging Serverless Functions

1. **Create debug endpoints** to isolate components:
   - `/api/debug-email-lookup?phone=X` - Test email lookup
   - `/api/debug-email-send?to=X` - Test email sending

2. **Add logging at each step:**
   ```typescript
   console.log(`[Notification] Starting for ${ref}, phone=${phone}`)
   const email = await lookupEmail(phone)
   console.log(`[Notification] Lookup returned: ${email || 'null'}`)
   console.log(`[Notification] SENDING EMAIL to ${email}`)
   const result = await sendEmail(...)
   console.log(`[Notification] Result:`, result)
   ```

3. **Test locally first** - Local dev shows full logs, Vercel logs are delayed/incomplete

4. **Check Vercel logs** (but they're unreliable):
   ```bash
   vercel logs https://your-app.vercel.app | grep -E "(Notification|Email|SMS)"
   ```

### Key Takeaways

1. **Never trust background tasks on Vercel** - Always await
2. **Trim API keys** - Env vars can have hidden newlines (see Environment Variables section)
3. **Add timeouts to external API calls** - Prevent indefinite hangs
4. **Test locally first** - Full visibility into logs
5. **Debug endpoints are invaluable** - Isolate components for testing

---

## Vercel AI Gateway

### Overview

Vercel AI Gateway provides a unified interface for calling AI models (OpenAI, Anthropic, etc.) with automatic OIDC authentication on Vercel deployments.

### Installation

```bash
npm install ai
```

### Correct Usage Pattern

<EXTREMELY-IMPORTANT>
Use `import { generateText } from 'ai'` with a model string. Do NOT use `@ai-sdk/anthropic` or custom providers for Vercel AI Gateway.
</EXTREMELY-IMPORTANT>

```typescript
// ✅ CORRECT - Simple pattern from docs
import { generateText } from 'ai'

const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4',  // provider/model format
  system: 'You are a helpful assistant.',
  prompt: 'What is 2+2?',
})
```

```typescript
// ❌ WRONG - Over-complicated patterns that break
import { anthropic } from '@ai-sdk/anthropic'
import { gateway } from '@vercel/ai-sdk-gateway'

// These cause FUNCTION_INVOCATION_FAILED errors
```

### Model String Format

Use `provider/model-name` format:

| Provider | Model String |
|----------|-------------|
| Anthropic | `anthropic/claude-sonnet-4` |
| Anthropic | `anthropic/claude-opus-4` |
| OpenAI | `openai/gpt-4o` |
| OpenAI | `openai/gpt-4-turbo` |

### Authentication

#### On Vercel (Production/Preview)

OIDC authentication is **automatic** - no configuration needed. The AI SDK detects it's running on Vercel and uses OIDC tokens.

#### Local Development

Use `vercel dev` to proxy through Vercel and get the same OIDC auth:

```bash
vercel dev
```

<EXTREMELY-IMPORTANT>
You do NOT need individual provider API keys (like `ANTHROPIC_API_KEY`) when using Vercel AI Gateway. The gateway handles authentication via OIDC.
</EXTREMELY-IMPORTANT>

**Note:** Regular `npm run dev` won't work for AI features - you must use `vercel dev` locally.

### Error Handling with Fallback

```typescript
import { generateText } from 'ai'

async function askAI(question: string) {
  try {
    const { text } = await generateText({
      model: 'anthropic/claude-sonnet-4',
      prompt: question,
    })
    return text
  } catch (error) {
    console.error('[AI Gateway] Error:', error)
    // Fallback to non-AI behavior
    return generateFallbackResponse(question)
  }
}
```

### Common Errors

**Error: `FUNCTION_INVOCATION_FAILED`**

- **Cause:** Using wrong import patterns or deprecated packages
- **Fix:** Use simple `import { generateText } from 'ai'` pattern

**Error: `AI analysis is temporarily unavailable`**

- **Cause:** AI Gateway call failing, falling back to error handler
- **Debug:** Check Vercel logs for the actual error
- **Common fixes:**
  - Ensure `AI_GATEWAY_API_KEY` is set for local dev
  - Use correct model string format
  - Check network connectivity to AI provider

**Error: `Timeout waiting for AI response`**

- **Cause:** Model taking too long to respond
- **Fix:** Add maxDuration to function config:
  ```json
  {
    "functions": {
      "api/**/*.ts": {
        "maxDuration": 60
      }
    }
  }
  ```

### Streaming Responses

```typescript
import { streamText } from 'ai'

export async function POST(req: Request) {
  const { prompt } = await req.json()

  const result = await streamText({
    model: 'anthropic/claude-sonnet-4',
    prompt,
  })

  return result.toDataStreamResponse()
}
```

### Best Practices

1. **Always handle errors** - AI calls can fail; have fallback behavior
2. **Don't over-engineer** - The simple pattern works; avoid custom providers
3. **Test locally first** - Use `AI_GATEWAY_API_KEY` or `vercel dev`
4. **Log errors** - Include `[AI Gateway]` prefix for easy filtering
5. **Mock in tests** - Avoid real API calls in unit tests:
   ```typescript
   vi.mock('ai', () => ({
     generateText: vi.fn().mockRejectedValue(new Error('Mocked')),
   }))
   ```

---

## Build Caching

### Turborepo Remote Cache

```bash
# Link to Vercel remote cache
npx turbo login
npx turbo link
```

```json
// turbo.json
{
  "remoteCache": {
    "signature": true
  }
}
```

### Clear Build Cache

If builds are stale or broken:

1. **Dashboard:** Settings → General → Build Cache → Purge
2. **CLI:** Redeploy with `vercel --force`

---

## E2E Testing with Turso/Cloud Databases

When running Playwright E2E tests against a Next.js app that supports both local SQLite and Turso, **force local database mode** to avoid socket timeouts and flaky tests.

```typescript
// playwright.config.ts
webServer: {
  // Unset Turso env vars to force local SQLite mode
  command: 'TURSO_DATABASE_URL= TURSO_AUTH_TOKEN= npm run dev -- --port 3001',
  url: 'http://localhost:3001',
  timeout: 120000,
},
```

**Why:** Long-running E2E tests (e.g., processing 280K+ records) can timeout waiting for Turso cloud responses. Local SQLite is faster and more reliable for testing.

**See also:** `nextjs-e2e-testing.md` skill for complete E2E testing patterns.

---

## Common Issues

### Build Timeout

**Error:** `Build exceeded maximum duration`

**Fixes:**
- Upgrade plan (Hobby: 45min, Pro: 45min)
- Optimize build (parallel builds, caching)
- Use `turbo prune` for monorepos

### Memory Exceeded

**Error:** `FATAL ERROR: JavaScript heap out of memory`

**Fix:** Increase Node memory in build command:
```json
{
  "buildCommand": "NODE_OPTIONS='--max-old-space-size=4096' npm run build"
}
```

### Module Not Found

**Error:** `Cannot find module 'x'`

**Causes:**
- Dependency in `devDependencies` but needed at runtime
- Case sensitivity (works on Mac, fails on Linux)
- Missing from `package.json`

**Fix:** Move to `dependencies` or check case sensitivity.

---

## OAuth Integration

### Callback URL Must Match Final Domain

If your domain redirects (e.g., `example.com` → `www.example.com`), the OAuth callback URL must use the **final destination domain**:

```
https://www.example.com/api/auth/callback  ✓
https://example.com/api/auth/callback      ✗ (if it redirects to www)
```

### Debugging OAuth Issues

```bash
# Check redirect URL for corruption
curl -s -I "https://your-app.com/api/auth/github" | grep location
```

Look for `%0A` (newline) or unexpected characters in `client_id` - indicates env var has trailing newline.

**Common errors:**
- `client_id and/or client_secret passed are incorrect` → Check for newlines in env vars
- `404 on callback` → Callback URL mismatch in OAuth app settings

---

## GCP Workload Identity Federation (WIF)

### Audience Mismatch

Vercel OIDC tokens have `aud: "https://vercel.com/{team-slug}"` but GCP providers often default to expecting `https://oidc.vercel.com/{team-slug}`.

**Diagnosis:**
```bash
gcloud iam workload-identity-pools providers describe {provider} \
  --location=global \
  --workload-identity-pool={pool} \
  --project={project} \
  --format="value(oidc.allowedAudiences)"
```

**Fix:** Update allowed audience to match Vercel's token:
```bash
gcloud iam workload-identity-pools providers update-oidc {provider} \
  --location=global \
  --workload-identity-pool={pool} \
  --project={project} \
  --allowed-audiences="https://vercel.com/{team-slug}"
```

### OIDC Package

Use `@vercel/functions/oidc`, NOT the deprecated `@vercel/oidc`:

```typescript
// ❌ Old (deprecated, causes "getToken is not a function")
import { getToken } from '@vercel/oidc'

// ✅ New
import { getVercelOidcToken } from '@vercel/functions/oidc'
```

### Newlines Break WIF

If env vars have trailing newlines, the STS audience string becomes corrupted:
```
"//iam.googleapis.com/projects/123456\n/locations/global..."
```

**Symptoms:**
- Debug endpoint shows `\n` in the `stsAudience` field
- STS exchange fails with "Invalid value for audience"

**Fix:** Re-add each WIF env var using `printf` (not dashboard copy-paste):
```bash
printf "value" | vercel env add GCP_PROJECT_NUMBER production --force
printf "value" | vercel env add GCP_WORKLOAD_IDENTITY_POOL_ID production --force
printf "value" | vercel env add GCP_WORKLOAD_IDENTITY_PROVIDER_ID production --force
printf "value" | vercel env add GCP_SERVICE_ACCOUNT_EMAIL production --force
```

---

## Domains

### Add Custom Domain

```bash
vercel domains add example.com
```

### DNS Configuration

| Type | Name | Value |
|------|------|-------|
| A | @ | 76.76.21.21 |
| CNAME | www | cname.vercel-dns.com |

### SSL

Automatic via Let's Encrypt. No configuration needed.

---

## Quick Reference

```bash
# Deploy to production
vercel --prod

# Add env var (use printf!)
printf "value" | vercel env add KEY production

# Pull env vars locally
vercel env pull .env.local

# View logs
vercel logs <url>

# Rollback
vercel promote <previous-url>

# Clear cache and redeploy
vercel --force --prod
```

---

## Fluid Compute & Function Duration

### Overview

Fluid Compute is Vercel's enhanced serverless model providing longer timeouts, optimized concurrency, and better cold start performance.

### Duration Limits

| Plan | Without Fluid Compute | With Fluid Compute |
|------|----------------------|-------------------|
| **Hobby** | 10s default, 60s max | 300s default, 300s max |
| **Pro** | 15s default, 300s max | 300s default, 800s max |
| **Enterprise** | 15s default, 300s max | 300s default, 800s max |

<EXTREMELY-IMPORTANT>
If your function times out at exactly 60 seconds despite Pro plan and Fluid Compute settings, Fluid Compute is NOT actually active. This is a known issue affecting multiple users.
</EXTREMELY-IMPORTANT>

### Enabling Fluid Compute

**Two independent settings must BOTH be configured:**

1. **Dashboard Toggle (Project-wide)**
   - Go to Project Settings → Functions
   - Find "Fluid Compute" section
   - Toggle ON
   - Click Save
   - **Redeploy** (changes only apply to new deployments)

2. **Dashboard Max Duration (Project-wide)**
   - Go to Project Settings → Functions
   - Find "Function Max Duration" section
   - Set to desired value (e.g., 300)
   - Click Save

3. **vercel.json (Per-deployment override)**
   ```json
   {
     "$schema": "https://openapi.vercel.sh/vercel.json",
     "fluid": true
   }
   ```
   Note: `"fluid": true` in vercel.json only enables Fluid Compute for that specific deployment, NOT project-wide.

### Configuring maxDuration

**Method 1: In route.ts (App Router - Recommended)**
```typescript
// src/app/api/my-function/route.ts
export const maxDuration = 300; // seconds
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  // ...
}
```

**Method 2: In vercel.json**
```json
{
  "functions": {
    "src/app/api/**/route.ts": {
      "maxDuration": 300
    }
  }
}
```

### Path Patterns for vercel.json

<EXTREMELY-IMPORTANT>
When using a `src/` directory, you MUST include `src/` in the path pattern.
</EXTREMELY-IMPORTANT>

| Project Structure | Correct Pattern | Wrong Pattern |
|-------------------|-----------------|---------------|
| `src/app/api/` | `src/app/api/**/route.ts` | `app/api/**/route.ts` |
| `app/api/` | `app/api/**/route.ts` | `src/app/api/**/route.ts` |
| Pages Router | `src/pages/api/**/*.ts` | `pages/api/**/*.ts` |

**For App Router specifically:**
- Use `**/route.ts` pattern, not `**/*.ts`
- The pattern must match the actual route handler files

### Known Issue: 60s Timeout Despite Pro Plan

**Symptoms:**
- Pro plan confirmed
- `"fluid": true` in vercel.json
- `maxDuration = 300` in route.ts
- Function still times out at exactly 60 seconds

**Root Cause:** Fluid Compute is not being applied at the platform level despite settings.

**Community Reports:**
- [Vercel timing out at 60s on Pro plan](https://community.vercel.com/t/vercel-timing-out-functions-at-60-seconds-on-pro-plan/22939) - Closed without resolution
- [Max Duration not being used](https://community.vercel.com/t/max-duration-not-being-used/7837)
- [GitHub: maxDuration not honored](https://github.com/vercel/next.js/issues/66462)

**Troubleshooting Checklist:**
1. ✅ Verify Dashboard toggle is ON (not just vercel.json)
2. ✅ Verify Dashboard "Function Max Duration" is set
3. ✅ Verify path pattern matches your file structure
4. ✅ Redeploy after any settings change
5. ✅ Check if using Node.js runtime (Edge has different limits)
6. ❌ If all above are correct → Contact Vercel Support

**Workaround: Split Long-Running Tasks**

If Fluid Compute won't activate, split work into multiple endpoints that each complete under 60s:

```json
{
  "crons": [
    {
      "path": "/api/cron/poll-nodes",
      "schedule": "*/5 * * * *"
    },
    {
      "path": "/api/cron/poll-validators",
      "schedule": "*/5 * * * *"
    }
  ]
}
```

### Cron Jobs

```json
{
  "crons": [
    {
      "path": "/api/cron/my-job",
      "schedule": "*/5 * * * *"
    }
  ]
}
```

**Cron Authentication:**
- Vercel adds `Authorization: Bearer <CRON_SECRET>` header
- Set `CRON_SECRET` env var to protect endpoint
- Verify in your handler:
  ```typescript
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  ```

### Testing Functions Locally

```bash
# Use vercel dev for full Vercel environment simulation
vercel dev

# Or use vercel curl to test deployed endpoints with auth bypass
vercel curl /api/cron/my-job -- --header "Authorization: Bearer $CRON_SECRET"
```

### Runtime Support

Fluid Compute currently supports:
- Node.js (version 20+)
- Python
- Edge (different limits apply)
- Bun
- Rust

---

## Resources

- [Vercel Docs](https://vercel.com/docs)
- [vercel.json Reference](https://vercel.com/docs/projects/project-configuration)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Fluid Compute](https://vercel.com/docs/fluid-compute)
- [Configuring Duration](https://vercel.com/docs/functions/configuring-functions/duration)
