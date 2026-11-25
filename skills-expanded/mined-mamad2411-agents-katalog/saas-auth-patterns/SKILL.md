---
name: saas-auth-patterns
description: SaaS authentication and authorization patterns including JWT vs session strategies, multi-tenant isolation, RBAC, API key management, passwordless flows, MFA, and secure session handling.
---

# SaaS Auth Patterns

Authentication and authorization patterns for multi-tenant SaaS applications.

## Auth Strategy Decision Matrix

| Strategy | Stateless | Scalable | Revocable | Best For |
|----------|-----------|----------|-----------|----------|
| JWT + Refresh | Yes | High | Hard (needs blocklist) | API-first, mobile clients |
| Session (server) | No | Medium (sticky/shared store) | Instant | Traditional web apps |
| OAuth 2.0 + PKCE | Yes | High | Via provider | Third-party login, SSO |

Pick JWT when you control both client and server and need horizontal scaling.
Pick sessions when you need instant revocation and serve server-rendered pages.
Pick OAuth when users expect "Sign in with Google/GitHub" or you federate identity.

## Multi-Tenant Auth

### Tenant Isolation Middleware

```typescript
interface TenantContext {
  tenantId: string
  userId: string
  role: string
}

// Extract tenant from JWT claims or subdomain
function resolveTenant(req: Request): TenantContext {
  const token = req.headers.get('authorization')?.replace('Bearer ', '')
  if (!token) throw new AuthError('Missing token')

  const payload = verifyJwt(token)
  return {
    tenantId: payload.tenantId,
    userId: payload.sub,
    role: payload.role,
  }
}

// Every DB query scoped to tenant - no cross-tenant leakage
async function getTenantUsers(ctx: TenantContext): Promise<User[]> {
  return db.users.findMany({
    where: { tenantId: ctx.tenantId },
  })
}
```

### Shared DB vs Isolated DB

```typescript
// Shared DB (row-level isolation) - simpler ops, lower cost
// Every table has tenant_id column + RLS policy
// SQL: CREATE POLICY tenant_isolation ON users
//        USING (tenant_id = current_setting('app.tenant_id'))

async function withTenantScope<T>(tenantId: string, fn: () => Promise<T>): Promise<T> {
  await db.$executeRaw`SELECT set_config('app.tenant_id', ${tenantId}, true)`
  return fn()
}

// Isolated DB (schema-per-tenant) - stronger isolation, harder ops
// Use when: compliance requires it, tenants have wildly different data volumes
function getTenantConnection(tenantId: string): PrismaClient {
  // SECURITY: Validate tenantId to prevent schema injection
  if (!/^[a-zA-Z0-9_-]+$/.test(tenantId)) {
    throw new Error('Invalid tenant ID format')
  }
  const schema = `tenant_${tenantId}`
  // Note: Cache PrismaClient instances per tenant to avoid connection leaks
  return new PrismaClient({ datasources: { db: { url: `${DB_URL}?schema=${schema}` } } })
}
```

## Account Linking (Email + Social Merge)

```typescript
async function linkOrCreateAccount(provider: string, profile: OAuthProfile): Promise<User> {
  // Step 1: Check if social account already linked
  const existing = await db.socialAccounts.findUnique({
    where: { provider_providerAccountId: { provider, providerAccountId: profile.id } },
    include: { user: true },
  })
  if (existing) return existing.user

  // Step 2: Check if email matches an existing user
  // SECURITY: Only auto-link if provider verified the email
  if (!profile.email_verified) {
    return db.users.create({
      data: {
        email: null, name: profile.name,
        socialAccounts: { create: { provider, providerAccountId: profile.id } },
      },
    })
  }

  const emailUser = await db.users.findUnique({
    where: { email: profile.email },
  })

  if (emailUser) {
    // Link social account to existing user (merge)
    await db.socialAccounts.create({
      data: { userId: emailUser.id, provider, providerAccountId: profile.id },
    })
    return emailUser
  }

  // Step 3: Brand new user - create both records
  return db.users.create({
    data: {
      email: profile.email,
      name: profile.name,
      socialAccounts: {
        create: { provider, providerAccountId: profile.id },
      },
    },
  })
}
```

## Role-Based Access Control (RBAC)

```typescript
type Permission = 'read' | 'write' | 'delete' | 'manage_users' | 'billing'

const ROLE_PERMISSIONS: Record<string, Permission[]> = {
  owner:  ['read', 'write', 'delete', 'manage_users', 'billing'],
  admin:  ['read', 'write', 'delete', 'manage_users'],
  member: ['read', 'write'],
  viewer: ['read'],
}

function authorize(role: string, required: Permission): boolean {
  const permissions = ROLE_PERMISSIONS[role]
  if (!permissions) return false
  return permissions.includes(required)
}

// Middleware factory - attach to any route
function requirePermission(permission: Permission) {
  return async (req: Request): Promise<void> => {
    const ctx = resolveTenant(req)
    if (!authorize(ctx.role, permission)) {
      throw new AuthError('Insufficient permissions')
    }
  }
}

// Usage
// await requirePermission('manage_users')(req)
// await requirePermission('billing')(req)
```

## API Key Management

```typescript
import { randomBytes, createHash } from 'crypto'

// Generate: show full key once, store only the hash
function generateApiKey(): { fullKey: string; hashedKey: string; prefix: string } {
  const raw = randomBytes(32).toString('base64url')
  const prefix = raw.slice(0, 8)
  const fullKey = `sk_live_${raw}`
  const hashedKey = createHash('sha256').update(fullKey).digest('hex')
  return { fullKey, hashedKey, prefix }
}

// Store key with scopes and expiry
async function createApiKey(tenantId: string, name: string, scopes: string[]): Promise<string> {
  const { fullKey, hashedKey, prefix } = generateApiKey()
  await db.apiKeys.create({
    data: { tenantId, name, hashedKey, prefix, scopes, expiresAt: addDays(new Date(), 90) },
  })
  return fullKey  // Return ONCE - never stored in plaintext
}

// Validate incoming API key
async function validateApiKey(key: string): Promise<{ tenantId: string; scopes: string[] }> {
  const hashedKey = createHash('sha256').update(key).digest('hex')
  const record = await db.apiKeys.findUnique({ where: { hashedKey } })

  if (!record) throw new AuthError('Invalid API key')
  if (record.expiresAt < new Date()) throw new AuthError('API key expired')
  if (record.revokedAt) throw new AuthError('API key revoked')

  await db.apiKeys.update({ where: { id: record.id }, data: { lastUsedAt: new Date() } })
  return { tenantId: record.tenantId, scopes: record.scopes }
}

// Rotation: create new key, mark old as deprecated, revoke after grace period
async function rotateApiKey(oldKeyId: string, tenantId: string): Promise<string> {
  const oldKey = await db.apiKeys.findUnique({ where: { id: oldKeyId } })
  if (!oldKey) throw new Error('Key not found')

  const newFullKey = await createApiKey(tenantId, `${oldKey.name} (rotated)`, oldKey.scopes)
  await db.apiKeys.update({ where: { id: oldKeyId }, data: { revokedAt: addDays(new Date(), 7) } })
  return newFullKey
}
```

## Magic Link / Passwordless Flow

```typescript
async function sendMagicLink(email: string): Promise<void> {
  const token = randomBytes(32).toString('base64url')
  const hashedToken = createHash('sha256').update(token).digest('hex')

  await db.magicLinks.create({
    data: { email, hashedToken, expiresAt: new Date(Date.now() + 15 * 60 * 1000) },  // 15 min
  })

  const link = `${process.env.APP_URL}/auth/verify?token=${token}`
  await sendEmail(email, 'Sign in', `Click to sign in: ${link}`)
}

async function verifyMagicLink(token: string): Promise<{ userId: string; sessionToken: string }> {
  const hashedToken = createHash('sha256').update(token).digest('hex')

  // Atomic: mark as used only if not already used (prevents TOCTOU race)
  const result = await db.magicLinks.updateMany({
    where: { hashedToken, usedAt: null, expiresAt: { gt: new Date() } },
    data: { usedAt: new Date() },
  })
  if (result.count === 0) throw new AuthError('Invalid, expired, or already used link')

  const record = await db.magicLinks.findUnique({ where: { hashedToken } })

  const user = await findOrCreateUser(record.email)
  const sessionToken = await createSession(user.id)
  return { userId: user.id, sessionToken }
}
```

## MFA Integration

```typescript
import { authenticator } from 'otplib'

// Enrollment: generate secret, user scans QR code
async function enrollMfa(userId: string): Promise<{ secret: string; qrUri: string }> {
  const secret = authenticator.generateSecret()
  // SECURITY: Encrypt secret at rest in production (AES-256-GCM)
  await db.mfaSecrets.create({ data: { userId, secret, verified: false } })

  const qrUri = authenticator.keyuri(userId, process.env.APP_NAME ?? 'My App', secret)
  return { secret, qrUri }
}

// Verify first code to activate MFA
async function activateMfa(userId: string, code: string): Promise<void> {
  const record = await db.mfaSecrets.findUnique({ where: { userId } })
  if (!record) throw new AuthError('MFA not enrolled')

  if (!authenticator.check(code, record.secret)) {
    throw new AuthError('Invalid MFA code')
  }

  await db.mfaSecrets.update({ where: { userId }, data: { verified: true } })
}

// Login: after password check, require MFA if enabled
async function loginWithMfa(email: string, password: string, mfaCode?: string): Promise<string> {
  const user = await verifyPassword(email, password)

  const mfa = await db.mfaSecrets.findUnique({ where: { userId: user.id, verified: true } })
  if (mfa) {
    if (!mfaCode) throw new MfaRequiredError('MFA code required')
    if (!authenticator.check(mfaCode, mfa.secret)) throw new AuthError('Invalid MFA code')
  }

  return createSession(user.id)
}
```

## Session Management

```typescript
// Session with refresh token rotation
async function createSession(userId: string): Promise<{ accessToken: string; refreshToken: string }> {
  const accessToken = signJwt({ sub: userId }, { expiresIn: '15m' })
  const refreshToken = randomBytes(32).toString('base64url')
  const hashedRefresh = createHash('sha256').update(refreshToken).digest('hex')

  await db.sessions.create({
    data: { userId, hashedRefreshToken: hashedRefresh, expiresAt: addDays(new Date(), 30) },
  })

  return { accessToken, refreshToken }
}

// Refresh: issue new pair, invalidate old refresh token (rotation)
async function refreshSession(oldRefreshToken: string): Promise<{ accessToken: string; refreshToken: string }> {
  const hashed = createHash('sha256').update(oldRefreshToken).digest('hex')
  const session = await db.sessions.findUnique({ where: { hashedRefreshToken: hashed } })

  if (!session || session.expiresAt < new Date()) throw new AuthError('Session expired')
  if (session.revokedAt) {
    // Refresh token reuse detected - revoke ALL sessions for this user
    await db.sessions.updateMany({ where: { userId: session.userId }, data: { revokedAt: new Date() } })
    throw new AuthError('Token reuse detected, all sessions revoked')
  }

  // Revoke old, issue new
  await db.sessions.update({ where: { id: session.id }, data: { revokedAt: new Date() } })
  return createSession(session.userId)
}

// Concurrent session limit
async function enforceSessionLimit(userId: string, maxSessions: number): Promise<void> {
  const activeSessions = await db.sessions.findMany({
    where: { userId, revokedAt: null, expiresAt: { gt: new Date() } },
    orderBy: { createdAt: 'asc' },
  })

  if (activeSessions.length >= maxSessions) {
    const oldest = activeSessions[0]
    await db.sessions.update({ where: { id: oldest.id }, data: { revokedAt: new Date() } })
  }
}
```

## Token Storage: GOOD vs BAD

```typescript
// BAD: localStorage is accessible to any JS on the page (XSS = full account takeover)
localStorage.setItem('token', accessToken)
fetch('/api/data', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })

// GOOD: httpOnly cookie - JS cannot read it, browser sends it automatically
// Server sets the cookie on login response:
function setAuthCookie(res: Response, accessToken: string): void {
  res.headers.set('Set-Cookie', [
    `access_token=${accessToken}`,
    'HttpOnly',        // JS cannot access
    'Secure',          // HTTPS only
    'SameSite=Lax',    // CSRF protection
    'Path=/',
    'Max-Age=900',     // 15 minutes
  ].join('; '))
}

// Server reads from cookie, not from Authorization header:
function getTokenFromCookie(req: Request): string {
  const cookies = req.headers.get('cookie') || ''
  const match = cookies.match(/access_token=([^;]+)/)
  if (!match) throw new AuthError('No session cookie')
  return match[1]
}
```

**Core rule**: Store tokens in httpOnly cookies, hash secrets before persisting, rotate keys on a schedule, and treat refresh token reuse as a breach signal. Auth is the one system where "good enough" is never good enough.
