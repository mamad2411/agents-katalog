# SAP-036: React Error Handling - Claude Agent Awareness

**SAP**: SAP-036 (react-error-handling)
**Version**: 1.0.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-036?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Quick setup with production-ready configuration
- 📚 **Time Savings** - 5% time savings
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020 (Foundation)

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-036.
s.

---

## Quick Start for Claude

**When User Says**:
- "Add error handling" → Read AGENTS.md (Quick reference, Error Decision Tree)
- "Set up Sentry" → Read adoption-blueprint.md (Step 2-3: Sentry setup)
- "Handle errors in app" → Read protocol-spec.md (How-to: Error boundaries)
- "Add error tracking" → Read adoption-blueprint.md (Full 30-min guide)
- "Fix error boundary" → Read protocol-spec.md (Reference: Error boundary API)

**Progressive Context Loading**:
- **Phase 1** (Quick reference): Read AGENTS.md only (5 min, ~10k tokens)
- **Phase 2** (Implementation): Read adoption-blueprint.md + protocol-spec.md (20 min, ~130k tokens)
- **Phase 3** (Design rationale): Read capability-charter.md (10 min, ~145k tokens total)

---

## Progressive Context Loading Strategy

### Phase 1: Orientation (AGENTS.md)

**Read when**:
- User asks "how do I handle errors?"
- User wants quick reference
- User needs error decision tree
- User wants copy-paste examples

**Key sections**:
- Quick Reference (30-second overview)
- Error Decision Tree (categorize error → choose pattern)
- Common Workflows (4 workflows with code examples)
- Troubleshooting Guide (common issues + fixes)

**Token cost**: ~10k tokens

**Output**: Know which error pattern to use, copy-paste working code

**Example**:
```markdown
User: "How do I catch errors in my app?"

Claude (Phase 1):
1. Read AGENTS.md (5 min)
2. Identify error type using decision tree:
   - Fatal error (code bug) → Error boundary (error.tsx)
3. Copy error.tsx template from Workflow 1
4. Provide to user with explanation
```

---

### Phase 2: Implementation (adoption-blueprint.md + protocol-spec.md)

**Read adoption-blueprint.md when**:
- User says "set up error handling from scratch"
- User wants step-by-step guide
- User needs working installation

**Read protocol-spec.md when**:
- User needs complete API reference
- User asks "how do I do X with Sentry?"
- User building complex error recovery (retry, backoff, custom boundaries)

**Key sections**:
- **adoption-blueprint.md**:
  - Prerequisites (Next.js 15+, React 19+)
  - Installation (7 steps, 30 minutes)
  - Validation Checklist
- **protocol-spec.md**:
  - Reference (complete API for error boundaries, Sentry, retry)
  - How-to guides (10+ common tasks)
  - Tutorials (3 end-to-end examples)

**Token cost**: ~30k (adoption-blueprint) + ~100k (protocol-spec) = ~130k tokens total

**Output**: SAP-036 successfully adopted, error handling operational

**Example**:
```markdown
User: "Set up error tracking for production"

Claude (Phase 2):
1. Read adoption-blueprint.md (15 min)
2. Execute Step 1: Install dependencies
   - npm install @sentry/nextjs react-error-boundary react-hot-toast
3. Execute Step 2: Run Sentry wizard
   - npx @sentry/wizard@latest -i nextjs
4. Execute Step 3: Configure PII scrubbing
   - Update sentry.client.config.ts with beforeSend hook
5. Execute Step 4-7: Create error boundaries, toast, test
6. Run validation checklist
7. Report success to user
```

---

### Phase 3: Deep Understanding (capability-charter.md)

**Read when**:
- User asks "why Sentry over other tools?"
- User needs design rationale
- User wants evidence for time savings
- User evaluating alternatives (GlitchTip, Highlight.io)

**Key sections**:
- Problem Statement (why error handling matters)
- Solution Design (why these technologies)
- Success Criteria (metrics, benchmarks)
- Business Value (time savings, ROI)

**Token cost**: ~15k tokens

**Output**: Complete understanding of SAP-036 design decisions

**Example**:
```markdown
User: "Why should I use Sentry instead of self-hosting?"

Claude (Phase 3):
1. Read capability-charter.md (10 min)
2. Extract evidence:
   - Sentry: 3M+ devs, $0 (dev) + $26/month (prod)
   - Self-hosted: GlitchTip (free, but requires server maintenance)
   - Trade-off: Sentry easier ($26/month) vs self-hosted cheaper (but ops overhead)
3. Provide recommendation based on user's context
```

---

## Claude Code Workflows

### Workflow 1: Set Up Error Boundaries (10 min)

**User**: "Add error boundaries to my app"

**Claude Steps**:

1. **Read AGENTS.md** (Workflow: Set up error boundaries)

2. **Create error.tsx** (route-level):
   ```bash
   # Use Write tool
   Write app/error.tsx
   ```

3. **Create global-error.tsx** (root-level):
   ```bash
   # Use Write tool
   Write app/global-error.tsx
   ```

4. **Create not-found.tsx** (404 page):
   ```bash
   # Use Write tool
   Write app/not-found.tsx
   ```

5. **Verify**:
   ```bash
   # Use Bash tool
   ls app/error.tsx app/global-error.tsx app/not-found.tsx
   ```

6. **Test**:
   - Create test page: `app/test-error/page.tsx`
   - Navigate to `/test-error`
   - Trigger error → Verify error.tsx shows

**Token usage**: ~10k (read AGENTS.md)

**Time**: 10 minutes

---

### Workflow 2: Add Sentry Tracking (10 min)

**User**: "Add error tracking to production"

**Claude Steps**:

1. **Read adoption-blueprint.md** (Step 2-3: Sentry setup)

2. **Install Sentry**:
   ```bash
   # Use Bash tool
   npm install @sentry/nextjs
   ```

3. **Run wizard**:
   ```bash
   # Use Bash tool
   npx @sentry/wizard@latest -i nextjs
   ```

4. **Add PII scrubbing**:
   ```bash
   # Use Edit tool to update sentry.client.config.ts
   Edit sentry.client.config.ts
   # Add beforeSend hook to remove cookies, headers, emails
   ```

5. **Verify**:
   ```bash
   # Use Bash tool
   grep "beforeSend" sentry.client.config.ts
   # Expected: beforeSend hook present
   ```

6. **Test**:
   - Trigger error at `/test-error`
   - Check Sentry dashboard → Verify error logged
   - Check PII scrubbing → Verify `[EMAIL_REDACTED]`

**Token usage**: ~30k (read adoption-blueprint.md)

**Time**: 10 minutes

---

### Workflow 3: Implement Error Recovery (10 min)

**User**: "Add retry logic for network errors"

**Claude Steps**:

1. **Read protocol-spec.md** (How-to: Retry with exponential backoff)

2. **Create retry utility**:
   ```bash
   # Use Write tool
   Write utils/retry.ts
   ```
   ```typescript
   export async function retryWithBackoff<T>(
     fn: () => Promise<T>,
     maxRetries: number = 3
   ): Promise<T> {
     let lastError: Error

     for (let i = 0; i < maxRetries; i++) {
       try {
         return await fn()
       } catch (error) {
         lastError = error as Error
         const delay = Math.min(1000 * Math.pow(2, i), 10000)
         await new Promise(resolve => setTimeout(resolve, delay))
       }
     }

     throw lastError!
   }
   ```

3. **Use in API calls**:
   ```bash
   # Use Edit tool to update existing API call
   Edit app/dashboard/page.tsx
   ```
   ```typescript
   import { retryWithBackoff } from '@/utils/retry'

   const data = await retryWithBackoff(() => fetch('/api/data'))
   ```

4. **Add toast notifications**:
   ```typescript
   import toast from 'react-hot-toast'

   try {
     await retryWithBackoff(() => fetch('/api/data'))
   } catch (error) {
     toast.error('Failed to load data. Please try again.')
   }
   ```

5. **Verify**:
   - Simulate network error (disconnect WiFi)
   - Retry should happen 3x with exponential backoff
   - Toast should show after final failure

**Token usage**: ~100k (read protocol-spec.md How-to section)

**Time**: 10 minutes

---

### Workflow 4: Integrate with TanStack Query (5 min)

**User**: "Add error handling to TanStack Query"

**Claude Steps**:

1. **Read adoption-blueprint.md** (Next Steps: Integrate with TanStack Query)

2. **Create QueryClient with error handling**:
   ```bash
   # Use Write tool
   Write app/providers.tsx
   ```
   ```typescript
   'use client'

   import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
   import * as Sentry from '@sentry/nextjs'
   import toast from 'react-hot-toast'

   const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         retry: 3,
         retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
         onError: (error) => {
           Sentry.captureException(error)
           toast.error('Failed to load data. Please try again.')
         },
       },
       mutations: {
         onError: (error) => {
           Sentry.captureException(error)
           toast.error('Operation failed. Please try again.')
         },
       },
     },
   })

   export function Providers({ children }: { children: React.ReactNode }) {
     return (
       <QueryClientProvider client={queryClient}>
         {children}
       </QueryClientProvider>
     )
   }
   ```

3. **Update layout.tsx**:
   ```bash
   # Use Edit tool
   Edit app/layout.tsx
   ```
   ```typescript
   import { Providers } from './providers'

   export default function RootLayout({ children }) {
     return (
       <html>
         <body>
           <Providers>
             {children}
           </Providers>
         </body>
       </html>
     )
   }
   ```

4. **Verify**:
   - Trigger query error → Should retry 3x
   - After 3rd failure → Should show toast + log to Sentry

**Token usage**: ~30k (read adoption-blueprint.md)

**Time**: 5 minutes

---

## Error Decision Prompts

**When User Says**: "Handle this error"

**Claude Decision Tree**:

```
User encounters error → What type?
│
├─ **Transient** (network timeout, rate limit, server 503)
│  └─ Pattern: Retry with exponential backoff + toast
│     - Use retryWithBackoff() utility
│     - Show toast.error() after final failure
│     - Log to Sentry after 3 retries
│
├─ **Permanent** (validation, auth, not found)
│  └─ Pattern: Show error message
│     - Display validation errors inline
│     - Show toast.error() for auth errors
│     - Redirect to login for 401 errors
│
├─ **Fatal** (unhandled exception, code bug)
│  └─ Pattern: Error boundary
│     - Catch with error.tsx
│     - Log to Sentry (with stack trace)
│     - Show reset button (may not work, needs code fix)
│
└─ **404** (page not found)
   └─ Pattern: Custom not-found page
      - Display helpful 404 with navigation
      - Log to analytics (not Sentry, not an error)
      - Provide search or sitemap
```

**Claude Implementation**:

1. **Identify error type** (ask user or inspect code)
2. **Choose pattern** (from decision tree)
3. **Read relevant section**:
   - Transient → protocol-spec.md (How-to: Retry with backoff)
   - Permanent → protocol-spec.md (How-to: Show error messages)
   - Fatal → AGENTS.md (Workflow 1: Set up error boundaries)
   - 404 → AGENTS.md (Workflow 1: Create not-found.tsx)
4. **Implement pattern** (copy-paste + customize)
5. **Verify** (test error scenario)

---

## Code Generation Patterns

### Pattern 1: Always Include Error Boundaries

**When generating app routes**, always create error boundaries:

**Generate** (correct):
```typescript
// app/dashboard/page.tsx
export default function DashboardPage() {
  return <div>Dashboard</div>
}

// app/dashboard/error.tsx
'use client'

export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Dashboard Error</h2>
      <button onClick={reset}>Retry</button>
    </div>
  )
}
```

**Don't generate** (incorrect):
```typescript
// ❌ Missing error boundary
// app/dashboard/page.tsx
export default function DashboardPage() {
  return <div>Dashboard</div>
}
```

**Why**: Error boundaries prevent app crashes. Without error.tsx, errors crash entire app.

---

### Pattern 2: Always Add PII Scrubbing to Sentry

**When configuring Sentry**, always include PII scrubbing:

**Generate** (correct):
```typescript
// ✅ With PII scrubbing
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  beforeSend(event) {
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers
    }
    return event
  }
})
```

**Don't generate** (incorrect):
```typescript
// ❌ No PII scrubbing (GDPR violation)
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN
})
```

**Why**: PII scrubbing required for GDPR/CCPA compliance. Without it, sensitive data sent to Sentry.

---

### Pattern 3: Always Show User-Friendly Error Messages

**When displaying errors**, never show stack traces to users:

**Generate** (correct):
```typescript
// ✅ User-friendly
<div>
  <h2>Something went wrong</h2>
  <p>We've been notified and are working on a fix.</p>
  <button onClick={reset}>Try again</button>
</div>
```

**Don't generate** (incorrect):
```typescript
// ❌ Exposes stack trace (security risk)
<div>
  <h2>Error</h2>
  <pre>{error.stack}</pre>
</div>
```

**Why**: Stack traces expose code structure, file paths, dependencies (security risk). User-friendly messages better UX.

---

### Pattern 4: Always Use Exponential Backoff for Retry

**When implementing retry**, use exponential backoff (not fixed delay):

**Generate** (correct):
```typescript
// ✅ Exponential backoff (1s, 2s, 4s, 8s, ...)
const delay = Math.min(1000 * Math.pow(2, attemptIndex), 10000)
await new Promise(resolve => setTimeout(resolve, delay))
```

**Don't generate** (incorrect):
```typescript
// ❌ Fixed delay (hammers server)
await new Promise(resolve => setTimeout(resolve, 1000))
```

**Why**: Exponential backoff prevents thundering herd (all clients retrying simultaneously). Fixed delay hammers server.

---

### Pattern 5: Always Log to Sentry Before Throwing

**When throwing errors**, log to Sentry first:

**Generate** (correct):
```typescript
// ✅ Log to Sentry, then throw
try {
  await fetchData()
} catch (error) {
  Sentry.captureException(error)
  toast.error('Failed to load data')
  throw error // Re-throw for caller
}
```

**Don't generate** (incorrect):
```typescript
// ❌ Throw without logging (error lost)
try {
  await fetchData()
} catch (error) {
  throw error
}
```

**Why**: If error caught by parent, Sentry never sees it. Always log before re-throwing.

---

## Integration Patterns with Other SAPs

### SAP-020 (react-foundation)

**When generating error boundaries**:

1. **Always use Next.js 15 App Router error.tsx pattern** (not Pages Router _error.tsx)
   ```typescript
   // ✅ App Router (Next.js 15)
   // app/error.tsx
   'use client'

   export default function Error({ error, reset }) { ... }
   ```

   ```typescript
   // ❌ Pages Router (Next.js 12-13, deprecated)
   // pages/_error.tsx
   function Error({ statusCode }) { ... }
   ```

2. **Use `'use client'` directive** (error boundaries are client components)
   ```typescript
   'use client' // Required for error boundaries

   export default function Error({ error, reset }) { ... }
   ```

3. **Return structured error pages** (not plain HTML)
   ```typescript
   export default function Error({ error, reset }: {
     error: Error & { digest?: string }
     reset: () => void
   }) {
     return <div>...</div>
   }
   ```

**Evidence**: Next.js 15 error handling docs, SAP-020 protocol-spec.md

---

### SAP-025 (react-performance)

**When integrating Sentry with performance monitoring**:

1. **Use sampling to minimize overhead**:
   ```typescript
   Sentry.init({
     tracesSampleRate: 0.1, // 10% sampling (<1% overhead)
   })
   ```

2. **Monitor Core Web Vitals** (LCP, FID, CLS):
   ```typescript
   Sentry.init({
     integrations: [
       new Sentry.BrowserTracing({
         // Monitor all routes
         routingInstrumentation: Sentry.nextRouterInstrumentation(router),
       }),
     ],
   })
   ```

3. **Correlate errors with performance metrics**:
   - Slow errors → Performance problem (e.g., timeout due to slow API)
   - Fast errors → Code bug (e.g., null pointer)

**Evidence**: Sentry performance docs, RT-019 research (Section 6: Performance Monitoring)

---

### SAP-023 (react-state-management)

**When handling TanStack Query errors**:

1. **Use global error handling** (instead of per-query):
   ```typescript
   const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         retry: 3,
         onError: (error) => {
           Sentry.captureException(error)
           toast.error('Failed to load data')
         },
       },
     },
   })
   ```

2. **Differentiate query vs mutation errors**:
   - Query errors → Auto-retry (transient)
   - Mutation errors → No retry (permanent)

3. **Use error boundaries for critical queries**:
   ```typescript
   import { ErrorBoundary } from '@/components/ErrorBoundary'

   function DashboardPage() {
     return (
       <ErrorBoundary>
         <Suspense fallback={<Loading />}>
           <DashboardData />
         </Suspense>
       </ErrorBoundary>
     )
   }
   ```

**Evidence**: TanStack Query error handling docs, RT-019 research (Section 7: State Management Errors)

---

## Common Claude Pitfalls

### Pitfall 1: Not Catching Errors in Server Components

**Problem**: Claude generates Server Component without error boundary

**Symptom**: App crashes on error, no error.tsx shown

**Diagnosis**:
```bash
# Check if page.tsx is Server Component (no 'use client')
grep "'use client'" app/dashboard/page.tsx
# If no output → Server Component

# Check if error.tsx exists
ls app/dashboard/error.tsx
# If "No such file" → Missing error boundary
```

**Fix**: Always create error.tsx for routes with Server Components:
```typescript
// app/dashboard/page.tsx (Server Component)
export default async function DashboardPage() {
  const data = await fetchData() // Can throw
  return <div>{data}</div>
}

// app/dashboard/error.tsx (Client Component)
'use client'

export default function Error({ error, reset }) {
  return <div>Error loading dashboard</div>
}
```

**Why**: Server Components can't have error boundaries inline (must be separate error.tsx file).

---

### Pitfall 2: Missing PII Scrubbing

**Problem**: Claude configures Sentry without PII scrubbing

**Symptom**: Sensitive data (cookies, emails) appears in Sentry events

**Diagnosis**:
```bash
# Check PII scrubbing configured
grep "beforeSend" sentry.client.config.ts
# If no output → Missing PII scrubbing
```

**Fix**: Always include beforeSend hook:
```typescript
// ✅ Correct
Sentry.init({
  beforeSend(event) {
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers
    }
    return event
  }
})
```

**Why**: GDPR/CCPA requires PII scrubbing. Without it, legal compliance violated.

---

### Pitfall 3: Showing Technical Error Messages to Users

**Problem**: Claude displays error.message directly to users

**Symptom**: Users see "TypeError: Cannot read property 'foo' of undefined"

**Diagnosis**:
```bash
# Check error.tsx for error.message
grep "error.message" app/error.tsx
# If found → Technical message exposed
```

**Fix**: Always show user-friendly messages:
```typescript
// ❌ Technical message
<p>{error.message}</p>

// ✅ User-friendly
<p>We encountered an issue. Please try again.</p>
```

**Why**: Technical messages confuse users, expose code details (security risk).

---

### Pitfall 4: Not Using Exponential Backoff for Retry

**Problem**: Claude implements retry with fixed delay

**Symptom**: Server hammered with requests (thundering herd problem)

**Diagnosis**:
```bash
# Check retry logic
grep "setTimeout" utils/retry.ts
# If "setTimeout(resolve, 1000)" → Fixed delay
```

**Fix**: Use exponential backoff:
```typescript
// ❌ Fixed delay
await new Promise(resolve => setTimeout(resolve, 1000))

// ✅ Exponential backoff
const delay = Math.min(1000 * Math.pow(2, attemptIndex), 10000)
await new Promise(resolve => setTimeout(resolve, delay))
```

**Why**: Fixed delay causes all clients to retry simultaneously (thundering herd). Exponential backoff spreads retries over time.

---

### Pitfall 5: Not Testing Error Boundaries in Production Mode

**Problem**: Claude tests error boundaries in dev mode only

**Symptom**: Error boundaries work in dev, but not in production

**Diagnosis**:
```bash
# Check if tested in production mode
npm run build
npm run start
# Navigate to /test-error, trigger error
# If error.tsx not shown → Hydration issue
```

**Fix**: Always test in production mode:
```bash
# Build production bundle
npm run build

# Start production server
npm run start

# Test error boundaries
# Navigate to /test-error, trigger error
# Verify error.tsx shows
```

**Why**: Next.js dev mode has different error handling than production. Must test both.

---

## Troubleshooting for Claude

**When User Reports**:

### Issue: "Errors not showing in Sentry"

**Diagnosis**:
```bash
# Check DSN configured
grep "NEXT_PUBLIC_SENTRY_DSN" .env.local
# Expected: DSN present

# Check Sentry initialized
grep "Sentry.init" sentry.client.config.ts
# Expected: Sentry.init() called
```

**Fix**:
1. Verify `NEXT_PUBLIC_SENTRY_DSN` in `.env.local`
2. Restart dev server: `npm run dev`
3. Trigger test error at `/test-error`
4. Check Sentry dashboard (may take 1-2 minutes)

---

### Issue: "App crashes on error"

**Diagnosis**:
```bash
# Check error.tsx exists
ls app/error.tsx
# Expected: file exists

# Check 'use client' directive
head -n 1 app/error.tsx
# Expected: 'use client'
```

**Fix**:
1. Create error.tsx if missing
2. Add `'use client'` at top of file
3. Restart dev server

---

### Issue: "Sensitive data in Sentry"

**Diagnosis**:
```bash
# Check beforeSend hook
grep "beforeSend" sentry.client.config.ts
# Expected: PII scrubbing code present
```

**Fix**:
1. Add beforeSend hook to `sentry.client.config.ts`
2. Restart dev server
3. Trigger test error with email in message
4. Verify `[EMAIL_REDACTED]` in Sentry

---

### Issue: "Toast notifications not showing"

**Diagnosis**:
```bash
# Check Toaster in layout.tsx
grep "Toaster" app/layout.tsx
# Expected: <Toaster /> component present
```

**Fix**:
1. Import `Toaster` from `react-hot-toast` in layout.tsx
2. Add `<Toaster />` component to layout
3. Restart dev server

---

### Issue: "High Sentry overhead (>1%)"

**Diagnosis**:
```bash
# Check sampling rate
grep "tracesSampleRate" sentry.client.config.ts
# Expected: 0.1 (10%) or lower
```

**Fix**:
1. Reduce `tracesSampleRate` to 0.05 (5%) or 0.01 (1%)
2. Reduce `replaysSessionSampleRate` to 0.005 (0.5%)
3. Redeploy to production

---

## Next Steps for Claude

After setting up error handling, suggest:

### 1. Test Error Handling (2 min)

```bash
# Navigate to test page
http://localhost:3000/test-error

# Test error boundary
# Click "Trigger Error Boundary" → Should show error.tsx

# Test toast notifications
# Click toast buttons → Should show toast

# Test 404 page
# Visit /non-existent-page → Should show not-found.tsx
```

### 2. Integrate with Other SAPs (5-10 min)

- **SAP-025 (react-performance)**: Add Sentry performance monitoring
- **SAP-023 (react-state-management)**: Add TanStack Query error handling
- **SAP-038 (react-i18n)**: Translate error messages (if multilingual app)

### 3. Customize Error Pages (10 min)

- Add company branding to error.tsx
- Add support contact link
- Add error code lookup

### 4. Set Up Sentry Alerts (5 min)

- Configure email alerts for critical errors
- Set threshold (e.g., >10 errors in 1 hour)
- Add Slack integration (optional)

---

## Progressive Loading Summary

| Phase | Read | Token Cost | Time | Use When |
|-------|------|-----------|------|----------|
| **Phase 1** | AGENTS.md | ~10k | 5 min | Quick lookup, copy-paste examples |
| **Phase 2** | adoption-blueprint.md + protocol-spec.md | ~130k | 20 min | Full setup, complex patterns |
| **Phase 3** | capability-charter.md | ~15k | 10 min | Design rationale, evidence, alternatives |

**Total**: ~145k tokens for complete understanding (but start with Phase 1)

**Optimization**:
- Quick task → Phase 1 only (10k tokens)
- Implementation → Phase 1 + Phase 2 (140k tokens)
- Deep understanding → All phases (145k tokens)

---

## Key Takeaways for Claude

1. **Always start with AGENTS.md** (Phase 1) - Quick reference, decision trees, copy-paste examples
2. **Use error decision tree** - Categorize error (transient/permanent/fatal/404) → Choose pattern
3. **Always add PII scrubbing** - GDPR/CCPA compliance required, check beforeSend hook
4. **Never show stack traces to users** - Security risk, poor UX
5. **Use exponential backoff for retry** - Prevents thundering herd
6. **Test in production mode** - Next.js dev mode ≠ production error handling
7. **Read adoption-blueprint.md for setup** (Phase 2) - 30-minute guided installation
8. **Read protocol-spec.md for complex tasks** (Phase 2) - Complete API reference

---

**Version**: 1.0.0
**Status**: Pilot (pending SAP-027 validation)
**Created**: 2025-11-09
**Part of**: React SAP Excellence Initiative (Week 7-8)
