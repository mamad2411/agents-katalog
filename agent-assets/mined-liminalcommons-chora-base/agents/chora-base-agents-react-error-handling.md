# SAP-036: React Error Handling - Agent Awareness

**SAP ID**: SAP-036
**Agent Compatibility**: All AI agents with command execution and file operations
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

This AGENTS.md provides: Agent-specific patterns for implementing SAP-036.
s.

---

## Quick Start for Agents

This SAP provides workflows for **React error handling** using the three-layer architecture:

1. **Error Boundaries** → Next.js 15 error.tsx + react-error-boundary (prevent crashes)
2. **Monitoring** → Sentry (production visibility, <1% overhead)
3. **Recovery** → Retry patterns + toast notifications (95%+ user recovery)

### First-Time Session

1. **Identify error type**: Transient (network), Permanent (validation), Fatal (code bug), or 404
2. **Choose appropriate handling**: Retry, error message, error boundary, or not-found page
3. **Install dependencies**: Sentry, react-error-boundary, react-hot-toast
4. **Copy templates**: error.tsx, global-error.tsx, not-found.tsx

### Key Principle

**All errors must be caught, logged, and provide user recovery options**. No white screens of death.

---

## User Signal Pattern Tables

### Table 1: Error Handling Setup Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Setup error boundaries** | "Add error handling", "Setup error boundaries", "Prevent app crashes" | Execute Workflow 1: Set Up Error Boundaries | error.tsx, global-error.tsx, not-found.tsx created |
| **Setup Sentry** | "Add Sentry", "Monitor production errors", "Track errors" | Execute Workflow 2: Install Sentry | Sentry configured with PII scrubbing |
| **Setup toast notifications** | "Add toast notifications", "Show error messages", "Non-blocking errors" | Execute Workflow 3: Add Toast Notifications | react-hot-toast configured |
| **Add retry logic** | "Retry failed requests", "Exponential backoff", "Handle network errors" | Execute Workflow 4: Implement Retry Logic | TanStack Query retry configured |
| **Handle errors** | "Catch errors", "Error handling for API", "Handle exceptions" | Execute Workflow 5: Add Error Handling | Error handling patterns implemented |

### Table 2: Error Handling Operation Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Catch error** | "Catch this error", "Handle exception", "Error boundary" | Add ErrorBoundary wrapper | Error caught by boundary |
| **Log to Sentry** | "Log to Sentry", "Track error", "Capture exception" | Add Sentry.captureException() | Error logged to Sentry |
| **Show toast** | "Show error toast", "Notify user", "Error message" | Add toast.error() | Toast notification shown |
| **Retry operation** | "Retry this", "Try again", "Exponential backoff" | Add retry logic | Operation retried with backoff |
| **Scrub PII** | "Remove PII", "Scrub sensitive data", "GDPR compliance" | Add beforeSend hook | PII removed from Sentry events |

---

## Workflow 1: Set Up Error Boundaries (10 minutes)

**When to use**: Adding error handling to Next.js 15 App Router app

**Prerequisites**:
- Next.js 15.1+ (App Router)
- React 19+
- TypeScript 5.7+

**Steps**:

1. **Create route-level error boundary** (`app/error.tsx`):
   ```typescript
   'use client'

   import { useEffect } from 'react'

   export default function Error({
     error,
     reset,
   }: {
     error: Error & { digest?: string }
     reset: () => void
   }) {
     useEffect(() => {
       // Log error to console (Sentry added in Workflow 2)
       console.error('Error caught by boundary:', error)
     }, [error])

     return (
       <div className="min-h-screen flex items-center justify-center">
         <div className="max-w-md p-8 bg-red-50 rounded-lg">
           <h2 className="text-2xl font-bold text-red-900 mb-4">
             Something went wrong
           </h2>
           <p className="text-red-700 mb-4">
             {error.message || 'An unexpected error occurred'}
           </p>
           <button
             onClick={reset}
             className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
           >
             Try again
           </button>
         </div>
       </div>
     )
   }
   ```

2. **Create root error boundary** (`app/global-error.tsx`):
   ```typescript
   'use client'

   import { useEffect } from 'react'

   export default function GlobalError({
     error,
     reset,
   }: {
     error: Error & { digest?: string }
     reset: () => void
   }) {
     useEffect(() => {
       console.error('Global error:', error)
     }, [error])

     return (
       <html>
         <body>
           <div className="min-h-screen flex items-center justify-center p-4">
             <div className="max-w-md text-center">
               <h1 className="text-4xl font-bold mb-4">Application Error</h1>
               <p className="text-gray-700 mb-6">
                 Something went wrong. Please try refreshing the page.
               </p>
               <button
                 onClick={reset}
                 className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
               >
                 Reload Application
               </button>
             </div>
           </div>
         </body>
       </html>
     )
   }
   ```

3. **Create 404 page** (`app/not-found.tsx`):
   ```typescript
   import Link from 'next/link'

   export default function NotFound() {
     return (
       <div className="min-h-screen flex items-center justify-center">
         <div className="max-w-md text-center">
           <h1 className="text-6xl font-bold text-gray-900">404</h1>
           <h2 className="text-2xl font-semibold text-gray-700 mt-4">
             Page Not Found
           </h2>
           <p className="text-gray-600 mt-2">
             The page you're looking for doesn't exist.
           </p>
           <Link
             href="/"
             className="mt-6 inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
           >
             Go Home
           </Link>
         </div>
       </div>
     )
   }
   ```

4. **Test error boundaries**:
   ```bash
   npm run dev
   # Create test route that throws error
   # Verify error.tsx shows fallback UI
   # Verify reset() button works
   ```

**Expected outcome**:
- error.tsx catches component errors (no app crash)
- global-error.tsx catches root layout errors
- not-found.tsx shows custom 404 page
- Users can retry failed operations

**Time saved**: 45 minutes (manual setup) → 10 minutes (template-based)

---

## Workflow 2: Install Sentry for Production Monitoring (15 minutes)

**When to use**: Adding production error tracking to React app

**Prerequisites**:
- Next.js 15+ project
- Sentry account (free tier: 5k events/month)

**Steps**:

1. **Install Sentry with wizard**:
   ```bash
   npx @sentry/wizard@latest -i nextjs
   ```

   This creates:
   - `sentry.client.config.ts` (client-side configuration)
   - `sentry.server.config.ts` (server-side configuration)
   - Updates `next.config.js` with Sentry webpack plugin
   - Creates `.env.local` with `NEXT_PUBLIC_SENTRY_DSN`

2. **Add PII scrubbing** (client: `sentry.client.config.ts`):
   ```typescript
   import * as Sentry from '@sentry/nextjs'

   Sentry.init({
     dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

     // Performance Monitoring (10% sampling for <1% overhead)
     tracesSampleRate: 0.1,

     // Environment
     environment: process.env.NODE_ENV,

     // PII Scrubbing
     beforeSend(event, hint) {
       // Remove cookies and headers
       if (event.request) {
         delete event.request.cookies
         delete event.request.headers
       }

       // Remove email addresses from error messages
       if (event.message) {
         event.message = event.message.replace(
           /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi,
           '[EMAIL]'
         )
       }

       return event
     },
   })
   ```

3. **Add PII scrubbing** (server: `sentry.server.config.ts`):
   ```typescript
   import * as Sentry from '@sentry/nextjs'

   Sentry.init({
     dsn: process.env.SENTRY_DSN,

     tracesSampleRate: 0.1,

     beforeSend(event, hint) {
       // Remove server-side PII
       if (event.request) {
         delete event.request.cookies
         delete event.request.headers
         delete event.request.data // Remove POST body
       }

       // Remove user email and IP
       if (event.contexts?.user) {
         delete event.contexts.user.email
         delete event.contexts.user.ip_address
       }

       return event
     },
   })
   ```

4. **Update error.tsx to log to Sentry**:
   ```typescript
   'use client'

   import { useEffect } from 'react'
   import * as Sentry from '@sentry/nextjs'

   export default function Error({ error, reset }: ErrorProps) {
     useEffect(() => {
       Sentry.captureException(error)
     }, [error])

     return (
       <div>
         <h2>Something went wrong</h2>
         <button onClick={reset}>Try again</button>
       </div>
     )
   }
   ```

5. **Test Sentry**:
   ```bash
   npm run build
   npm start

   # Trigger error in production mode
   # Check Sentry dashboard for error
   # Verify PII is scrubbed (no emails, cookies)
   ```

**Expected outcome**:
- Sentry captures all production errors
- PII scrubbed by default (GDPR/CCPA compliant)
- <1% performance overhead (10% sampling)
- Real-time error alerts (email, Slack)

**Time saved**: 1 hour (manual setup) → 15 minutes (wizard + PII scrubbing)

---

## Workflow 3: Add Toast Notifications for Errors (5 minutes)

**When to use**: Showing non-blocking error messages to users

**Prerequisites**:
- React 19+ project

**Steps**:

1. **Install react-hot-toast**:
   ```bash
   npm install react-hot-toast
   ```

2. **Add Toaster to layout** (`app/layout.tsx`):
   ```typescript
   import { Toaster } from 'react-hot-toast'

   export default function RootLayout({ children }) {
     return (
       <html lang="en">
         <body>
           {children}
           <Toaster position="top-right" />
         </body>
       </html>
     )
   }
   ```

3. **Use toast in components**:
   ```typescript
   import toast from 'react-hot-toast'

   function MyComponent() {
     const handleAction = async () => {
       try {
         await riskyOperation()
         toast.success('Operation successful!')
       } catch (error) {
         toast.error('Operation failed. Please try again.')
       }
     }

     return <button onClick={handleAction}>Do Action</button>
   }
   ```

4. **TanStack Query integration**:
   ```typescript
   import { useMutation } from '@tanstack/react-query'
   import toast from 'react-hot-toast'

   function useCreateOrder() {
     return useMutation({
       mutationFn: createOrder,
       onSuccess: () => {
         toast.success('Order placed!')
       },
       onError: (error) => {
         toast.error(`Failed: ${error.message}`)
       },
     })
   }
   ```

5. **Test toasts**:
   ```bash
   npm run dev
   # Trigger success and error actions
   # Verify toasts appear in top-right
   ```

**Expected outcome**:
- Non-blocking error messages (users can continue working)
- Success/error feedback (better UX)
- Accessible (WCAG 2.2 compliant)

**Time saved**: 30 minutes (manual setup) → 5 minutes (install + configure)

---

## Workflow 4: Implement Retry Logic with Exponential Backoff (5 minutes)

**When to use**: Retrying transient errors (network, API timeout)

**Prerequisites**:
- TanStack Query configured (SAP-023)

**Steps**:

1. **Configure retry in QueryClient** (`lib/query-client.ts`):
   ```typescript
   import { QueryClient } from '@tanstack/react-query'

   export const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         retry: 3, // Max 3 attempts
         retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
         // Attempt 1: 0s delay
         // Attempt 2: 1s delay
         // Attempt 3: 2s delay
         // Attempt 4: 4s delay (max 30s)
       },
       mutations: {
         retry: 0, // Don't retry mutations (avoid duplicates)
       },
     },
   })
   ```

2. **Use in query** (inherits retry from QueryClient):
   ```typescript
   import { useQuery } from '@tanstack/react-query'

   function useProducts() {
     return useQuery({
       queryKey: ['products'],
       queryFn: fetchProducts,
       // Automatically retries 3 times with exponential backoff
     })
   }
   ```

3. **Override retry per query** (if needed):
   ```typescript
   function useCriticalData() {
     return useQuery({
       queryKey: ['critical'],
       queryFn: fetchCriticalData,
       retry: 5, // More retries for critical data
       retryDelay: (attemptIndex) => Math.min(2000 * 2 ** attemptIndex, 60000),
     })
   }
   ```

4. **Test retry**:
   ```bash
   npm run dev
   # Simulate network error in DevTools (Offline mode)
   # Verify query retries 3 times
   # Check React Query Devtools for retry count
   ```

**Expected outcome**:
- Transient errors automatically retried (network, timeout)
- Exponential backoff prevents server overload
- 90% perceived performance improvement (instant retry feedback)

**Time saved**: 45 minutes (manual implementation) → 5 minutes (QueryClient config)

---

## Workflow 5: Add Error Handling to TanStack Query (10 minutes)

**When to use**: Handling errors from API calls

**Prerequisites**:
- TanStack Query configured (SAP-023)
- Sentry and toast configured (Workflows 2-3)

**Steps**:

1. **Handle query errors** (useQuery):
   ```typescript
   import { useQuery } from '@tanstack/react-query'
   import toast from 'react-hot-toast'
   import * as Sentry from '@sentry/nextjs'

   function useProducts() {
     return useQuery({
       queryKey: ['products'],
       queryFn: fetchProducts,
       onError: (error) => {
         // Log to Sentry
         Sentry.captureException(error, {
           tags: { query: 'products' },
         })

         // Show toast notification
         toast.error(`Failed to load products: ${error.message}`)
       },
     })
   }
   ```

2. **Handle mutation errors** (useMutation):
   ```typescript
   import { useMutation, useQueryClient } from '@tanstack/react-query'

   function useCreateProduct() {
     const queryClient = useQueryClient()

     return useMutation({
       mutationFn: createProduct,
       onSuccess: () => {
         toast.success('Product created!')
         queryClient.invalidateQueries({ queryKey: ['products'] })
       },
       onError: (error) => {
         Sentry.captureException(error, {
           tags: { mutation: 'createProduct' },
         })
         toast.error(`Failed to create product: ${error.message}`)
       },
     })
   }
   ```

3. **Show error in UI**:
   ```typescript
   function ProductList() {
     const { data, isLoading, error } = useProducts()

     if (isLoading) return <div>Loading...</div>

     if (error) {
       return (
         <div className="p-4 bg-red-50 rounded">
           <p className="text-red-900">Failed to load products</p>
           <p className="text-red-700 text-sm">{error.message}</p>
         </div>
       )
     }

     return (
       <ul>
         {data?.map((product) => (
           <li key={product.id}>{product.name}</li>
         ))}
       </ul>
     )
   }
   ```

4. **Test error handling**:
   ```bash
   npm run dev
   # Simulate API error (500 response)
   # Verify toast appears
   # Verify error logged to Sentry
   # Verify UI shows error state
   ```

**Expected outcome**:
- TanStack Query errors automatically retried (3 attempts)
- Errors logged to Sentry with context
- Users notified via toast (non-blocking)
- UI shows error state (graceful degradation)

**Time saved**: 1 hour (manual implementation) → 10 minutes (onError callbacks)

---

## Error Decision Tree

### Decision 1: What Type of Error?

```
Error occurred
├─ Transient error (network, timeout, API 5xx)?
│  ├─ YES → Retry with exponential backoff
│  │  ├─ Use TanStack Query retry (3 attempts, 1s/2s/4s delays)
│  │  ├─ Show toast notification ("Retrying...")
│  │  ├─ Log final failure to Sentry
│  │  └─ Show error boundary if all retries fail
│  │
│  └─ NO → Permanent error (validation, API 4xx)?
│     ├─ YES → Show error message
│     │  ├─ Inline error (form fields with React Hook Form)
│     │  ├─ Toast notification (non-blocking)
│     │  ├─ Don't retry (won't succeed)
│     │  ├─ Don't log to Sentry (expected error)
│     │  └─ Suggest recovery action (edit form, contact support)
│     │
│     └─ NO → Fatal error (code bug, exception)?
│        ├─ YES → Error boundary
│        │  ├─ Catch with error.tsx
│        │  ├─ Show fallback UI
│        │  ├─ Provide reset() button
│        │  ├─ Log to Sentry with full context
│        │  └─ Capture user ID, route, stack trace
│        │
│        └─ NO → 404 error (route not found)?
│           └─ YES → Custom not-found page
│              ├─ Show friendly "404 Page Not Found"
│              ├─ Provide navigation (go home, go back)
│              └─ Don't log to Sentry (expected)
```

### Decision 2: Where to Handle Error?

```
Where did error occur?
├─ Client Component (render error)?
│  └─ Caught by error.tsx (route-level error boundary)
│     ├─ Shows fallback UI
│     ├─ Logs to Sentry
│     └─ Provides reset() to retry
│
├─ Server Component (data fetching error)?
│  └─ Try/catch in component
│     ├─ Log to Sentry (Sentry.captureException)
│     ├─ Re-throw to trigger error.tsx
│     └─ Or return error state to render error UI
│
├─ API Route (server error)?
│  └─ Try/catch in route handler
│     ├─ Log to Sentry
│     ├─ Return 5xx response
│     └─ Client handles via TanStack Query onError
│
├─ TanStack Query (network error)?
│  └─ Handled by TanStack Query
│     ├─ Automatic retry (3 attempts)
│     ├─ onError callback → toast + Sentry
│     └─ Show error in UI (error state from useQuery)
│
├─ Form Validation (user input error)?
│  └─ React Hook Form + Zod
│     ├─ Show inline error next to field
│     ├─ Don't log to Sentry (expected error)
│     └─ Suggest correction (e.g., "Email is required")
│
└─ Root Layout Error (rare)?
   └─ Caught by global-error.tsx
      ├─ Last resort boundary
      ├─ Shows full-page error
      ├─ Logs to Sentry
      └─ Provides reload button
```

### Decision 3: What to Show Users?

```
Error message strategy?
├─ Network error (fetch failed, timeout)?
│  └─ "Unable to connect. Please check your internet connection."
│
├─ API 5xx (server error)?
│  └─ "We're having trouble loading this page. Please try again."
│
├─ API 4xx (client error)?
│  ├─ 400 → "Invalid request. Please check your input."
│  ├─ 401 → "Please log in to continue."
│  ├─ 403 → "You don't have permission to access this."
│  ├─ 404 → "The requested content was not found."
│  └─ 429 → "Too many requests. Please try again later."
│
├─ Validation error (form)?
│  └─ Specific field error (e.g., "Email is required", "Password too short")
│
└─ Code error (unexpected)?
   └─ "Something went wrong. Please try again."
      (Don't show stack trace to users)
```

---

## Best Practices

### 1. Always Use Error Boundaries

**Pattern**:
```typescript
// ✅ GOOD: error.tsx in every major route
// app/dashboard/error.tsx
// app/settings/error.tsx
// app/profile/error.tsx

// ❌ BAD: No error boundaries (app crashes on error)
```

**Why**: Error boundaries prevent entire app crashes. One component error shouldn't break the whole app.

---

### 2. Scrub PII Before Sending to Sentry

**Pattern**:
```typescript
// ✅ GOOD: beforeSend hook removes PII
Sentry.init({
  beforeSend(event, hint) {
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers
    }
    if (event.message) {
      event.message = event.message.replace(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi, '[EMAIL]')
    }
    return event
  },
})

// ❌ BAD: No PII scrubbing (GDPR/CCPA violations)
Sentry.init({ dsn: '...' })
```

**Why**: GDPR/CCPA require explicit consent before sending user data to third parties. Scrubbing prevents violations.

---

### 3. Retry Transient Errors, Don't Retry Permanent Errors

**Pattern**:
```typescript
// ✅ GOOD: Retry network errors, not validation errors
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  retry: (failureCount, error) => {
    // Don't retry 4xx errors (client errors)
    if (error.status >= 400 && error.status < 500) return false
    // Retry network/server errors
    return failureCount < 3
  },
})

// ❌ BAD: Retry all errors (wastes time on validation errors)
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  retry: 3, // Retries even 400 validation errors
})
```

**Why**: Validation errors (400, 422) won't succeed on retry. Retrying wastes time and annoys users.

---

### 4. Show User-Friendly Error Messages

**Pattern**:
```typescript
// ✅ GOOD: Friendly, actionable messages
function friendlyErrorMessage(error: Error): string {
  if (error.message.includes('fetch')) {
    return 'Unable to connect. Please check your internet connection.'
  }
  if (error.message.includes('timeout')) {
    return 'This is taking longer than expected. Please try again.'
  }
  return 'Something went wrong. Please try again.'
}

// ❌ BAD: Technical error messages
<p>{error.message}</p> // "TypeError: Cannot read property 'map' of undefined"
```

**Why**: Technical errors confuse users. Friendly messages explain what happened and how to recover.

---

### 5. Provide Recovery Actions for Every Error

**Pattern**:
```typescript
// ✅ GOOD: Every error has recovery action
function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <p>{friendlyErrorMessage(error)}</p>
      <button onClick={resetErrorBoundary}>Try Again</button>
      <Link href="/">Go Home</Link>
    </div>
  )
}

// ❌ BAD: No recovery action (user stuck)
function ErrorFallback({ error }) {
  return <div>Error: {error.message}</div>
}
```

**Why**: Users need a way to recover (retry, go home, contact support). Dead-end errors cause abandonment.

---

## Common Pitfalls

### Pitfall 1: Not Using Error Boundaries

**Problem**: App crashes on uncaught errors (white screen of death)

**Symptom**: Users report "blank page" after error

**Fix**: Add error.tsx to all major routes
```typescript
// ❌ BAD: No error.tsx
app/
├─ page.tsx
└─ dashboard/
   └─ page.tsx

// ✅ GOOD: error.tsx in every route
app/
├─ page.tsx
├─ error.tsx
└─ dashboard/
   ├─ page.tsx
   └─ error.tsx
```

**Why**: Error boundaries prevent full app crashes. One component error shouldn't break the whole app.

---

### Pitfall 2: Not Scrubbing PII from Sentry

**Problem**: Sending user emails, cookies, IP addresses to Sentry (GDPR/CCPA violations)

**Symptom**: PII visible in Sentry dashboard

**Fix**: Add beforeSend hook
```typescript
// ❌ BAD: No PII scrubbing
Sentry.init({ dsn: '...' })

// ✅ GOOD: beforeSend removes PII
Sentry.init({
  beforeSend(event) {
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers
    }
    return event
  },
})
```

**Why**: GDPR/CCPA require explicit consent before sending user data to third parties. Fines up to €20M.

---

### Pitfall 3: Retrying Permanent Errors

**Problem**: Retry validation errors (400, 422) that won't succeed

**Symptom**: Slow error handling, wasted retries

**Fix**: Only retry transient errors
```typescript
// ❌ BAD: Retry all errors
retry: 3

// ✅ GOOD: Only retry network/server errors
retry: (failureCount, error) => {
  if (error.status >= 400 && error.status < 500) return false
  return failureCount < 3
}
```

**Why**: Validation errors won't succeed on retry. Wastes time and annoys users.

---

### Pitfall 4: Showing Technical Errors to Users

**Problem**: Display stack traces, technical error messages to users

**Symptom**: Users confused by "TypeError: Cannot read property 'map' of undefined"

**Fix**: Show friendly error messages
```typescript
// ❌ BAD: Technical error
<p>{error.message}</p>

// ✅ GOOD: Friendly error
<p>{friendlyErrorMessage(error)}</p>
// "Unable to connect. Please check your internet connection."
```

**Why**: Technical errors confuse users. Friendly messages explain what happened and how to recover.

---

### Pitfall 5: Not Providing Recovery Actions

**Problem**: Error fallback has no buttons or links (user stuck)

**Symptom**: Users can't recover from error, must hard refresh

**Fix**: Always provide recovery action
```typescript
// ❌ BAD: No recovery action
function ErrorFallback({ error }) {
  return <div>Error: {error.message}</div>
}

// ✅ GOOD: Retry + go home buttons
function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div>
      <p>{error.message}</p>
      <button onClick={resetErrorBoundary}>Try Again</button>
      <Link href="/">Go Home</Link>
    </div>
  )
}
```

**Why**: Users need a way to recover. Dead-end errors cause abandonment (40-60% bounce rate).

---

## Integration with Other SAPs

### SAP-020 (react-foundation)

**Integration**: Next.js 15 error.tsx requires App Router

**Pattern**: SAP-020 scaffolds Next.js 15 project, SAP-036 adds error boundaries

---

### SAP-023 (react-state-management)

**Integration**: TanStack Query error handling (onError, retry)

**Pattern**:
```typescript
// SAP-023: TanStack Query
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  // SAP-036: Retry + error handling
  retry: 3,
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  onError: (error) => {
    toast.error(`Failed: ${error.message}`)
    Sentry.captureException(error)
  },
})
```

---

### SAP-025 (react-performance)

**Integration**: Sentry performance monitoring (10% sampling for <1% overhead)

**Pattern**:
```typescript
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1, // SAP-025 + SAP-036: 10% sampling
})
```

---

### SAP-021 (react-testing)

**Integration**: Test error boundaries with Vitest

**Pattern**:
```typescript
test('error.tsx shows error message', () => {
  const error = new Error('Test error')
  render(<Error error={error} reset={vi.fn()} />)
  expect(screen.getByText('Something went wrong')).toBeInTheDocument()
})
```

---

## Support & Resources

**SAP-036 Documentation**:
- [capability-charter.md](capability-charter.md) - Problem statement and business value
- [protocol-spec.md](protocol-spec.md) - Complete technical reference
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step installation
- [CLAUDE.md](CLAUDE.md) - Claude-specific patterns
- [ledger.md](ledger.md) - Adoption tracking

**External Resources**:
- [Next.js Error Handling](https://nextjs.org/docs/app/building-your-application/routing/error-handling)
- [Sentry Next.js Integration](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [react-error-boundary](https://github.com/bvaughn/react-error-boundary)
- [react-hot-toast](https://react-hot-toast.com/)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - Next.js 15 project setup
- [SAP-023 (react-state-management)](../react-state-management/) - TanStack Query error handling
- [SAP-025 (react-performance)](../react-performance/) - Sentry performance monitoring
- [SAP-021 (react-testing)](../react-testing/) - Test error boundaries

---

## Version History

- **1.0.0** (2025-11-09): Initial AGENTS.md for SAP-036
  - 5 workflows: Set Up Error Boundaries, Install Sentry, Add Toast Notifications, Implement Retry Logic, Add Error Handling to TanStack Query
  - 2 user signal pattern tables: Error Handling Setup Signals, Error Handling Operation Signals
  - 3-level error decision tree: Error type, handling location, user messaging
  - 5 best practices: Error boundaries, PII scrubbing, retry logic, friendly messages, recovery actions
  - 5 common pitfalls: No error boundaries, no PII scrubbing, retrying permanent errors, technical messages, no recovery actions
  - Focus on three-layer architecture (boundaries, monitoring, recovery)

---

**Next Steps**:
1. Review [protocol-spec.md](protocol-spec.md) for complete technical reference
2. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
3. Install: `npx @sentry/wizard@latest -i nextjs && npm install react-hot-toast`
4. Copy error.tsx, global-error.tsx, not-found.tsx templates
5. Configure Sentry PII scrubbing, add toast notifications
