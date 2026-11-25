---
name: nestjs-guards-auth
description: NestJS guards, authentication, and authorization best practices. Use when implementing or reviewing auth in NestJS — guards, JWT/Passport strategies, RBAC, route protection. Triggers on CanActivate, AuthGuard, JwtStrategy, @Roles, @Public, or Reflector.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Guards, Auth & Authorization

Best practices for securing NestJS applications with guards, Passport-based JWT
authentication, and role-based authorization. Verified against the current
NestJS v10/v11 documentation (guards, authentication, authorization, and the
Passport recipe).

The core mental model: **authentication** (authn) answers "who are you?" and
runs as a guard that validates a credential and attaches a typed `user` to the
request. **Authorization** (authz) answers "are you allowed?" and runs as a
separate guard that reads route metadata via `Reflector` and compares it against
that user. Keep these two concerns in distinct guards, declare a strong JWT
config from the environment, and never leak whether a credential was valid.

## When to Apply

Reference these rules when:

- Implementing login / token issuance or protecting routes in NestJS
- Writing or reviewing a `CanActivate` guard, `AuthGuard`, or `JwtStrategy`
- Setting up Passport (`@nestjs/passport` + `passport-jwt`)
- Adding role-based access control (`@Roles`, `RolesGuard`)
- Registering a global auth guard with per-route opt-out (`@Public`)
- Reviewing how `req.user` is typed, how secrets are configured, or how auth
  failures are surfaced to clients

## Rules

| Rule | Impact | Summary |
|------|--------|---------|
| [separate-authn-from-authz](rules/separate-authn-from-authz.md) | HIGH | Keep identity verification and permission checks in distinct guards |
| [passport-jwt-strategy](rules/passport-jwt-strategy.md) | HIGH | Use `@nestjs/passport` + a `passport-jwt` strategy class for JWT auth |
| [global-auth-guard-with-public](rules/global-auth-guard-with-public.md) | HIGH | Register a global auth guard and opt out via `@Public()` metadata |
| [roles-guard-rbac](rules/roles-guard-rbac.md) | HIGH | Drive RBAC with `@Roles()` metadata read by a `RolesGuard` via `Reflector` |
| [hash-passwords](rules/hash-passwords.md) | CRITICAL | Never store plaintext; hash with bcrypt/argon2 + salt |
| [type-the-request-user](rules/type-the-request-user.md) | MEDIUM | Strongly type `req.user`; never trust an unvalidated payload |
| [dont-leak-auth-details](rules/dont-leak-auth-details.md) | HIGH | Return generic 401/403; don't reveal whether a user exists |
| [validate-jwt-config](rules/validate-jwt-config.md) | CRITICAL | Load a strong secret from config/env with sane expiry; verify signature and expiration |

## How to Use

Read individual rule files for the rationale and incorrect/correct code:

```
rules/passport-jwt-strategy.md
rules/roles-guard-rbac.md
```

Each rule file contains a short explanation of why it matters, followed by an
**Incorrect** and a **Correct** TypeScript example. Apply CRITICAL and HIGH
impact rules first when reviewing existing auth code.
