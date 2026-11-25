---
name: express-middleware-security
description: >
  Secure Express middleware stacks: helmet, CORS, rate limits, body limits,
  trust proxy, auth guards, and correct middleware order. Use when Express
  security, helmet, express-rate-limit, cors, cookie/session, JWT middleware,
  or hardening Node HTTP APIs with Express/Connect.
---

# Express Middleware Security

## Scope And Authorization

- **In scope:** Express/Connect apps you own or are authorized to harden.
- **Out of scope:** Attacking third-party Express apps without permission.
- Middleware order matters—auth after body parse mistakes and CORS misconfigs are common.
- Redact session secrets and tokens from configs in tickets.
- Pair with `eslint-security-plugin`, `env-config-12factor`, and `code-quality-standards`.

## When To Use

- Standing up or reviewing an Express API/web app security baseline.
- Fixing missing security headers, open CORS, or unbounded JSON bodies.
- Correcting `trust proxy` for rate limits and secure cookies behind load balancers.
- Ordering helmet → parsers → rate limit → auth → routes.
- Session cookie flags and CSRF for cookie-based browser apps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ESLint security rules | `eslint-security-plugin` |
| FastAPI patterns | fastapi-* skills |
| JWT crypto deep dive | `api-auth-and-jwt-abuse` |
| Rate limit design for OTP | `email-otp-rate-limits` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Helmet | Sensible defaults; CSP tuned per app |
| CORS | Explicit origin allowlist; no `*` with credentials |
| Body | `express.json({ limit })` |
| trust proxy | Set when behind LB; required for accurate IP |
| Rate limit | Global + stricter on auth routes |
| Auth | Fail closed; attach user on `req` after verify |

## Workflow

### 1. Confirm scope and success criteria

1. App type: JSON API vs server-rendered vs hybrid.
2. Success: headers present; CORS tight; auth routes limited; large body rejected; tests cover order.

### 2. Inventory middleware

```bash
rg -n "app\\.use|router\\.use|helmet|cors|rateLimit|trust proxy" --glob '!node_modules'
```

1. Draw ordered list of global middleware.
2. Note session store and cookie settings.

### 3. Baseline risks

| Issue | Risk |
| --- | --- |
| No helmet | Missing baseline headers |
| `origin: true` reflect | CORS reflection |
| No body limit | Memory DoS |
| trust proxy off behind LB | Rate limit bypass / wrong IP |
| Auth after route | Unprotected handlers |

### 4. Apply hardened stack (illustrative)

```js
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

const app = express();
app.set('trust proxy', 1); // hop count — tune to your LB

app.use(helmet());
app.use(cors({
  origin: ['https://app.example.com'],
  credentials: true,
}));
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: false, limit: '100kb' }));

const globalLimiter = rateLimit({ windowMs: 60_000, max: 120 });
app.use(globalLimiter);

const authLimiter = rateLimit({ windowMs: 15 * 60_000, max: 20 });
app.use('/auth', authLimiter);

app.use('/api', requireAuth, apiRouter);

app.use((err, req, res, next) => {
  // generic message to client; log detail server-side
  res.status(err.status || 500).json({ error: { code: 'INTERNAL', message: 'Unexpected error', request_id: req.id } });
});
```

1. Cookies: `httpOnly`, `secure`, `sameSite` appropriate to CSRF strategy.
2. Disable `x-powered-by` (helmet does) and avoid verbose error stacks in prod.
3. File uploads: separate limits and type checks—not only JSON limit.

### 5. Auth middleware pattern

```js
async function requireAuth(req, res, next) {
  try {
    const user = await verifyAccessToken(req); // from cookie or Bearer
    if (!user) return res.status(401).json({ error: { code: 'UNAUTHENTICATED', message: 'Sign in required' } });
    req.user = user;
    return next();
  } catch {
    return res.status(401).json({ error: { code: 'UNAUTHENTICATED', message: 'Sign in required' } });
  }
}
```

1. Authorization checks per route (ownership)—not only authentication.
2. Never trust client-supplied `userId` without binding to session.

### 6. Verify with evidence

```bash
npm test
curl -sI https://api.example.com/health | rg -i 'content-security|x-frame|strict-transport'
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://api.example.com/v1/x \
  -H 'Content-Type: application/json' --data-binary @large.json
```

1. Supertest: unauthenticated API → 401; oversized body → 413.
2. CORS: disallowed origin does not get ACAO reflect.
3. Rate limit: burst to auth returns 429.

### 7. Hand off

1. Document middleware order in README.
2. Alert on 429 spikes and error rates.
3. Review helmet CSP when frontend changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| CORS | Allowlist origins | `*` + credentials |
| Body | 100kb default API | Unlimited JSON |
| Order | helmet → parse → limit → auth → routes | auth never applied |
| Errors | Stable codes | stack in JSON prod |
| trust proxy | Explicit hop | Default off behind LB |

## Output Checklist

- [ ] Middleware order documented
- [ ] Helmet/CORS/body limit/rate limit applied
- [ ] trust proxy correct for deployment
- [ ] Auth middleware fail-closed
- [ ] Cookie flags reviewed if sessions
- [ ] Tests/curl evidence captured
- [ ] Residual risk noted

## Rules

- Owned apps only for active testing.
- Middleware order is security-critical.
- Generic errors to clients; detail in logs.
- Authn ≠ authz.
- Pair lint rules via `eslint-security-plugin`.
