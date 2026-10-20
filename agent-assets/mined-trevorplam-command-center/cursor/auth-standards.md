---
description: Run Authentication, Access Control, and Session Security Checks
globs: ["**/auth/**/*.ts", "**/auth/**/*.tsx", "**/middleware.ts", "**/api/**/*.ts", "**/api/**/*.tsx"]
---
# Security: Authentication & Access Control Standards

<audit_rules>
- You MUST enforce Resource Ownership Checks on every API route handling user data. Verify `resource.userId === currentUser.id`.
- You MUST explicitly check roles for admin routes (e.g., `role === 'admin'`), NOT just authentication status.
- You MUST implement state parameter validation and PKCE flow for OAuth implementations to prevent CSRF and account takeover.
- You MUST configure session cookies with `HttpOnly`, `Secure`, and `SameSite=Lax` or `SameSite=Strict` flags.
- You MUST ensure JWT refresh tokens rotate on use and access tokens have a short lifespan (<15 minutes).
- You MUST verify that email-based account linking requires ownership verification before linking to existing accounts.
- You MUST verify that NO passwords or sensitive tokens are passed in URL parameters; use POST body instead.
</audit_rules>

**How to check**: Verify protected routes use auth middleware; confirm resource access checks ownership or role; validate session and token handling (no secrets in client, HttpOnly cookies where applicable).

<example_good>
```typescript
// src/app/api/orders/[id]/route.ts
export async function GET(req: Request, { params }: { params: { id: string } }) {
  const session = await getSession();
  if (!session) return new Response('Unauthorized', { status: 401 });

  const order = await db.order.findUnique({ where: { id: params.id } });
  
  // Resource ownership check
  if (order.userId !== session.user.id) {
    return new Response('Forbidden', { status: 403 });
  }
  
  return NextResponse.json(order);
}
```
</example_good>

<example_bad>
```typescript
// src/app/api/orders/[id]/route.ts
export async function GET(req: Request, { params }: { params: { id: string } }) {
  // BAD: Missing authorization/ownership check
  const order = await db.order.findUnique({ where: { id: params.id } });
  return NextResponse.json(order);
}
```
</example_bad>

**Related rules**: api-security, input-validation, security-headers.

