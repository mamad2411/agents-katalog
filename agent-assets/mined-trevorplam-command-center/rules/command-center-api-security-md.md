---
description: Run API Security and Rate Limiting Standards Check
globs: ['**/api/**/*.ts', '**/middleware.ts', '**/lib/rate-limit/**/*.ts']
---

# Security: API Security & Rate Limiting

<audit_rules>

- You MUST implement API rate limiting with user-specific and endpoint-specific limits.
- You MUST configure API key authentication with proper rotation and revocation mechanisms.
- You MUST implement request validation using schemas to prevent malformed or malicious requests.
- You MUST configure CORS policies with specific allowed origins, methods, and headers.
- You MUST implement API versioning strategies to maintain backward compatibility.
- You MUST configure request/response logging for security monitoring and audit trails.
- You MUST implement proper error handling that doesn't leak sensitive information.
- You MUST configure web application firewall (WAF) rules for common attack patterns.
- You MUST implement API discovery and documentation with OpenAPI/Swagger specifications.
  </audit_rules>

**How to check**: Confirm rate limiting is applied to API routes; verify API key validation and CORS config; ensure request validation and error responses do not leak internals.

<example_good>

```typescript
import { z } from 'zod'
import { rateLimit } from '@/lib/rate-limit'
import { validateApiKey } from '@/lib/api-keys'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).default('user'),
})

export async function POST(req: Request) {
  // Rate limiting
  const clientIP = req.headers.get('x-forwarded-for') ?? 'unknown'
  await rateLimit(clientIP, { max: 100, window: '1h' })

  // API key validation
  const apiKey = req.headers.get('x-api-key')
  if (!apiKey || !(await validateApiKey(apiKey))) {
    return new Response('Unauthorized', { status: 401 })
  }

  try {
    const body = await req.json()

    // Request validation
    const validated = CreateUserSchema.parse(body)

    // Business logic
    const user = await createUser(validated)

    // Response with proper headers
    return new Response(JSON.stringify({ data: user }), {
      status: 201,
      headers: {
        'Content-Type': 'application/json',
        'X-Rate-Limit-Remaining': '99',
      },
    })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return new Response(
        JSON.stringify({ error: 'Invalid request data', details: error.errors }),
        { status: 400 }
      )
    }

    // Generic error that doesn't leak internal details
    return new Response(JSON.stringify({ error: 'Internal server error' }), { status: 500 })
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No rate limiting, no validation, no proper error handling
export async function POST(req: Request) {
  const body = await req.json() // BAD: No validation

  // BAD: Direct database access without checks
  const user = await db.user.create({ data: body })

  // BAD: Leaking internal error details
  try {
    return NextResponse.json({ user })
  } catch (error) {
    return NextResponse.json(
      {
        error: error.message,
        stack: error.stack, // BAD: Exposing stack trace
      },
      { status: 500 }
    )
  }
}
```

</example_bad>

**Related rules**: api-standards, auth-standards, input-validation, security-headers.
