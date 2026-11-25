---
name: auth-patterns
description: >-
  This skill should be used when the user asks to "implement authentication",
  "set up JWT auth", "configure OAuth2", "implement RBAC", "add MFA/two-factor",
  "secure session management", or mentions "authentication", "authorization",
  "JWT", "OAuth", "login", "session management", "password hashing", "RBAC",
  "role-based access", "MFA", "two-factor", "API keys", "token refresh", "CSRF",
  "CORS with auth". Provides authentication and authorization patterns including
  JWT, OAuth2, session management, RBAC, MFA, and password security.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Authentication & Authorization Patterns

## JWT Authentication

### Token Structure
```
Header.Payload.Signature

Header:  { "alg": "RS256", "typ": "JWT" }
Payload: { "sub": "user-123", "iss": "myapp", "aud": "myapp-api", "exp": 1700000000, "iat": 1699999000 }
Signature: RS256(header + "." + payload, privateKey)
```

### Access + Refresh Token Pattern

```
Login → Access Token (15 min) + Refresh Token (30 days)
         │                        │
         ├── Use for API calls    ├── Use to get new access token
         ├── Short-lived          ├── Long-lived
         ├── Stateless            ├── Stored in DB (revocable)
         └── In httpOnly cookie   └── In httpOnly cookie (separate)
```

### Implementation Checklist

| Check | Details |
|-------|---------|
| Algorithm | Use RS256 for multi-service, HS256 for single service |
| Secret/Key | ≥256 bits, stored in env var, rotatable |
| Expiration | Access: 15-60 min. Refresh: 7-30 days |
| Storage | httpOnly + secure + sameSite cookies |
| Validation | Verify signature, exp, iss, aud on every request |
| Refresh | Rotate refresh token on use (invalidate old one) |
| Revocation | Store revoked tokens or use token version in DB |
| Logout | Invalidate refresh token, clear cookies |

### Token Storage Comparison

| Method | XSS Safe | CSRF Safe | Recommendation |
|--------|----------|-----------|----------------|
| httpOnly cookie | Yes | Need SameSite/token | **Recommended** |
| localStorage | No | Yes | Never for auth tokens |
| sessionStorage | No | Yes | Never for auth tokens |
| Memory (variable) | Yes | Yes | OK for SPAs (lost on refresh) |

## Password Security

### Hashing

```javascript
// CORRECT — bcrypt with sufficient rounds
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.compare(password, hash);

// CORRECT — argon2 (preferred for new projects)
import argon2 from 'argon2';
const hash = await argon2.hash(password);
const valid = await argon2.verify(hash, password);

// NEVER — these are NOT for password hashing
// MD5, SHA-1, SHA-256 (even with salt)
```

### Password Policy

| Rule | Minimum |
|------|---------|
| Length | 8 characters (NIST recommends up to 64) |
| Complexity | Don't require special chars (NIST 2024). Check against breached password lists instead. |
| History | Prevent reuse of last 5 passwords |
| Rotation | Don't force periodic changes (NIST) |
| Breach check | Check against HaveIBeenPwned API |

## OAuth 2.0

### Flow Selection

| Client Type | Flow | Use Case |
|-------------|------|----------|
| Server-side web app | Authorization Code | Traditional web apps |
| SPA / Mobile | Authorization Code + PKCE | Public clients |
| Server-to-server | Client Credentials | Backend services |
| CLI / IoT | Device Code | No browser available |

### Authorization Code + PKCE (SPA)

```
1. Generate code_verifier (random 43-128 chars)
2. Generate code_challenge = SHA256(code_verifier)
3. Redirect to auth server with code_challenge
4. User authenticates, gets authorization code
5. Exchange code + code_verifier for tokens
6. Auth server verifies SHA256(code_verifier) == code_challenge
```

## Session Management

### Secure Session Configuration

```javascript
app.use(session({
  secret: process.env.SESSION_SECRET,  // Strong random secret
  name: '__session',                    // Custom name (not 'connect.sid')
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,     // Not accessible via JavaScript
    secure: true,       // HTTPS only
    sameSite: 'lax',    // CSRF protection
    maxAge: 3600000,    // 1 hour
    domain: '.example.com'
  }
}));
```

### Session Lifecycle

| Event | Action |
|-------|--------|
| Login | Regenerate session ID |
| Privilege change | Regenerate session ID |
| Logout | Destroy session |
| Idle timeout | Expire after 30 min inactivity |
| Absolute timeout | Expire after 8 hours regardless |

## RBAC (Role-Based Access Control)

### Simple Roles

```javascript
const ROLES = {
  admin:  ['read', 'write', 'delete', 'manage_users'],
  editor: ['read', 'write'],
  viewer: ['read'],
};

function authorize(...requiredPermissions) {
  return (req, res, next) => {
    const userPerms = ROLES[req.user.role] || [];
    const hasAll = requiredPermissions.every(p => userPerms.includes(p));
    if (!hasAll) return res.status(403).json({ error: 'Forbidden' });
    next();
  };
}

// Usage
app.delete('/api/users/:id', authorize('delete', 'manage_users'), deleteUser);
```

### Resource-Level Authorization

```javascript
// Always verify ownership
app.get('/api/posts/:id', async (req, res) => {
  const post = await db.posts.findById(req.params.id);
  if (!post) return res.status(404).json({ error: 'Not found' });

  // Check ownership OR admin role
  if (post.authorId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.json(post);
});
```

## MFA (Multi-Factor Authentication)

### TOTP (Time-based One-Time Password)

```
1. Generate secret: base32-encoded random bytes
2. Create QR code with otpauth:// URI
3. User scans with authenticator app
4. On login: verify 6-digit code against secret + time
5. Store backup codes (hashed) for recovery
```

### Implementation Notes

- Generate 8-10 backup codes on MFA setup
- Hash backup codes in DB (like passwords)
- Mark backup codes as used (single-use)
- Allow MFA recovery via email verification
- Rate limit TOTP verification (prevent brute-force)

## Rate Limiting

### Auth-Specific Limits

| Endpoint | Limit | Window | Action on Exceed |
|----------|-------|--------|-----------------|
| POST /login | 10 | 15 min | Lock account 15 min |
| POST /register | 5 | 1 hour | Block IP |
| POST /forgot-password | 3 | 1 hour | Silently ignore |
| POST /verify-mfa | 5 | 5 min | Lock account |

## CSRF Protection

### SameSite Cookies (Primary)
```
Set-Cookie: session=abc; SameSite=Lax; Secure; HttpOnly
```

### CSRF Tokens (Additional Layer)
```
1. Server generates random token, stores in session
2. Token included in form as hidden field or meta tag
3. Server validates token matches session on POST/PUT/DELETE
```

### Double Submit Cookie Pattern
```
1. Set CSRF token in a regular cookie (readable by JS)
2. Client reads cookie, sends as X-CSRF-Token header
3. Server compares cookie value with header value
```
