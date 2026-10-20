---
description: Run CORS and Security Headers Configuration Check
globs: ['**/middleware.ts', 'next.config.js', 'vercel.json', 'src/app/**/*.ts']
---

# Security: CORS & Security Headers Configuration

<audit_rules>

- You MUST implement a Content Security Policy (CSP) header with a strict whitelist to prevent XSS attacks.
- You MUST set X-Frame-Options to DENY or SAMEORIGIN to prevent clickjacking attacks.
- You MUST set X-Content-Type-Options to nosniff to prevent MIME-type sniffing attacks.
- You MUST implement Strict-Transport-Security (HSTS) with includeSubDomains for production HTTPS sites.
- You MUST configure CORS origins specifically and minimally. Avoid wildcard (`*`) origins for APIs that handle sensitive data.
- You MUST ensure Referrer-Policy is set appropriately (e.g., strict-origin-when-cross-origin) to prevent leaking referrer data.
  </audit_rules>

**How to check**: Inspect middleware or server config for CSP, X-Frame-Options, X-Content-Type-Options, HSTS, and CORS; ensure no permissive wildcards for sensitive APIs.

<example_good>

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Security Headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')

  // CSP Header
  const csp = [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self'",
    "connect-src 'self' https://api.example.com",
  ].join('; ')

  response.headers.set('Content-Security-Policy', csp)

  // CORS for API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const origin = request.headers.get('origin')
    if (origin === 'https://app.example.com') {
      response.headers.set('Access-Control-Allow-Origin', origin)
      response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
      response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    }
  }

  return response
}
```

</example_good>

<example_bad>

```typescript
// BAD: Missing security headers and permissive CORS
export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // No security headers set

  // BAD: Wildcard CORS origin
  if (request.nextUrl.pathname.startsWith('/api/')) {
    response.headers.set('Access-Control-Allow-Origin', '*')
  }

  return response
}
```

</example_bad>
