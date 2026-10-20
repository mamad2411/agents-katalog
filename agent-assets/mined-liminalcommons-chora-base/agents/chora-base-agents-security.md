# SAP-033: React Authentication - Security Patterns

**SAP**: SAP-033 (react-authentication)
**Domain**: Security
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **security best practices** for authentication in Next.js 15+ projects.

**Topics Covered**:
1. Session Security
2. Password Security
3. CSRF Protection
4. Rate Limiting
5. Security Headers

**For provider setup**, see [../providers/AGENTS.md](../providers/AGENTS.md)

**For workflows**, see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## 1. Session Security

### Secure Session Configuration

**NextAuth v5 - JWT Sessions**:
```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // 24 hours (refresh daily)
  },

  jwt: {
    maxAge: 30 * 24 * 60 * 60,
  },

  cookies: {
    sessionToken: {
      name: `__Secure-next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        secure: process.env.NODE_ENV === "production",
      },
    },
  },
});
```

**Key Security Features**:
- `httpOnly: true` - Prevents JavaScript access (XSS protection)
- `sameSite: "lax"` - CSRF protection
- `secure: true` - HTTPS-only in production
- `maxAge` - Automatic session expiration

---

### Session Refresh Pattern

**Automatic session refresh**:
```typescript
// middleware.ts
import { auth } from "@/auth";

export default auth((req) => {
  const session = req.auth;

  if (session) {
    // Update session activity timestamp
    session.lastActivity = Date.now();
  }

  return NextResponse.next();
});
```

---

## 2. Password Security

### Password Hashing

**Use bcrypt** (recommended):
```typescript
import bcrypt from "bcryptjs";

// Hash password
const hashedPassword = await bcrypt.hash(password, 10);

// Verify password
const isValid = await bcrypt.compare(password, hashedPassword);
```

**Never**:
- ❌ Store passwords in plaintext
- ❌ Use MD5 or SHA1 (not secure)
- ❌ Roll your own crypto

---

### Password Requirements

**Strong password policy**:
```typescript
const passwordSchema = z.string()
  .min(8, "Password must be at least 8 characters")
  .regex(/[A-Z]/, "Must include uppercase letter")
  .regex(/[a-z]/, "Must include lowercase letter")
  .regex(/[0-9]/, "Must include number")
  .regex(/[^A-Za-z0-9]/, "Must include special character");
```

**Display password strength**:
```typescript
function calculatePasswordStrength(password: string): number {
  let strength = 0;

  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[^A-Za-z0-9]/.test(password)) strength++;

  return strength; // 0-5
}
```

---

## 3. CSRF Protection

### Built-in CSRF Protection

**NextAuth v5** - Automatic CSRF protection:
```typescript
// Enabled by default
// Uses double-submit cookie pattern
// No additional configuration needed
```

**Clerk** - Built-in protection

**Supabase** - Built-in protection

---

### Custom CSRF Protection

**Using next-csrf**:
```bash
npm install next-csrf
```

```typescript
// middleware.ts
import { createCsrfMiddleware } from "next-csrf";

const csrfMiddleware = createCsrfMiddleware({
  secret: process.env.CSRF_SECRET!,
});

export default csrfMiddleware;
```

---

## 4. Rate Limiting

### Prevent Brute Force Attacks

**Using Upstash Rate Limit**:
```bash
npm install @upstash/ratelimit @upstash/redis
```

```typescript
// lib/rate-limit.ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

export const loginRateLimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, "15 m"), // 5 attempts per 15 minutes
  analytics: true,
});

export const magicLinkRateLimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(3, "1 h"), // 3 requests per hour
});
```

**Usage in Server Action**:
```typescript
"use server";

import { loginRateLimit } from "@/lib/rate-limit";

export async function login(formData: FormData) {
  const email = formData.get("email") as string;

  // Check rate limit
  const { success } = await loginRateLimit.limit(email);

  if (!success) {
    return { error: "Too many login attempts. Please try again later." };
  }

  // Proceed with login...
}
```

---

## 5. Security Headers

### Configure Next.js Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  {
    key: "X-Frame-Options",
    value: "SAMEORIGIN",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "X-XSS-Protection",
    value: "1; mode=block",
  },
  {
    key: "Referrer-Policy",
    value: "origin-when-cross-origin",
  },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=()",
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};
```

---

## Security Checklist

### ✅ Authentication Security

- [ ] Passwords hashed with bcrypt (salt rounds ≥10)
- [ ] Session cookies are `httpOnly`, `secure`, `sameSite`
- [ ] JWT tokens have expiration (`maxAge`)
- [ ] Session refresh implemented
- [ ] CSRF protection enabled
- [ ] Rate limiting on login endpoints
- [ ] Account lockout after failed attempts
- [ ] Password reset requires email verification
- [ ] Magic links expire after 5-15 minutes
- [ ] OAuth state parameter validated

---

### ✅ Authorization Security

- [ ] Role-based access control (RBAC) implemented
- [ ] Protected routes enforce authentication
- [ ] Server Actions validate session
- [ ] API routes check permissions
- [ ] Database queries scoped to authenticated user
- [ ] Admin actions require additional verification

---

### ✅ Infrastructure Security

- [ ] HTTPS enforced in production
- [ ] Security headers configured
- [ ] Environment variables not exposed to client
- [ ] Secrets rotated regularly
- [ ] Database credentials secured
- [ ] OAuth secrets not committed to git
- [ ] CORS configured correctly
- [ ] Content Security Policy (CSP) configured

---

## Common Security Vulnerabilities

### ❌ Vulnerability 1: Session Fixation

**Problem**: Attacker sets session ID before authentication

**Fix**: Regenerate session after login

```typescript
// NextAuth v5 handles this automatically
// Manual implementation:
async function login(email: string, password: string) {
  // Verify credentials...

  // Destroy old session
  await destroySession();

  // Create new session
  const newSession = await createSession(userId);

  return newSession;
}
```

---

### ❌ Vulnerability 2: Insecure Password Reset

**Problem**: Password reset tokens don't expire or are predictable

**Fix**: Use cryptographically secure tokens with expiration

```typescript
import crypto from "crypto";

async function createPasswordResetToken(userId: string) {
  // Generate secure token
  const token = crypto.randomBytes(32).toString("hex");
  const expires = new Date(Date.now() + 15 * 60 * 1000); // 15 minutes

  // Store in database
  await prisma.passwordResetToken.create({
    data: {
      userId,
      token,
      expires,
    },
  });

  return token;
}

async function verifyPasswordResetToken(token: string) {
  const resetToken = await prisma.passwordResetToken.findUnique({
    where: { token },
  });

  if (!resetToken || resetToken.expires < new Date()) {
    throw new Error("Invalid or expired token");
  }

  return resetToken.userId;
}
```

---

### ❌ Vulnerability 3: Missing Rate Limiting

**Problem**: Attackers can brute force credentials or spam endpoints

**Fix**: Implement rate limiting (see section 4 above)

---

### ❌ Vulnerability 4: XSS via User Data

**Problem**: User-provided data rendered without escaping

**Fix**: React escapes by default, but be careful with `dangerouslySetInnerHTML`

```typescript
// ✅ Safe (React escapes automatically)
<p>{user.name}</p>

// ❌ Dangerous (no escaping)
<p dangerouslySetInnerHTML={{ __html: user.bio }} />

// ✅ Safe alternative
import DOMPurify from "isomorphic-dompurify";

<p dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(user.bio) }} />
```

---

## Version History

**1.0.0 (2025-11-10)** - Initial security patterns extraction from awareness-guide.md
- Session security best practices
- Password hashing and requirements
- CSRF protection patterns
- Rate limiting implementation
- Security headers configuration
- Security checklist
- Common vulnerabilities and fixes
