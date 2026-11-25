---
name: auth-middleware
description: Generates authentication and authorization middleware for Express/Fastify/Hono
argument-hint: <strategy: jwt|session|api-key|oauth>
user-invocable: true
allowed-tools: Read Glob Edit
effort: medium
---

## Generate Auth Middleware

Strategy: **$1** (jwt | session | api-key | oauth)

1. Detect framework and existing auth patterns:
```bash
cat package.json | grep -E '"express"|"fastify"|"hono"|"jsonwebtoken"|"jose"|"passport"'
grep -rn "middleware\|authenticate\|authorize" src/ --include="*.ts" -l | head -5
```

2. Read existing auth code if present.

3. Generate the middleware for the requested strategy:

**JWT example:**
```ts
export async function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.split(' ')[1]
  if (!token) return res.status(401).json({ error: 'Unauthorized' })
  
  try {
    const payload = await verifyJWT(token)
    req.user = payload
    next()
  } catch {
    return res.status(401).json({ error: 'Invalid token' })
  }
}

export function authorize(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!roles.includes(req.user?.role)) return res.status(403).json({ error: 'Forbidden' })
    next()
  }
}
```

4. Include:
   - Token refresh logic (if JWT)
   - Rate limiting for auth endpoints
   - Brute force protection (lockout after N failures)
   - Proper error messages (don't leak info)

5. Generate tests for all auth scenarios.
