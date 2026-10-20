---
name: security-standards
description: Security rules for AWS/Cognito/Express stacks — JWT auth middleware, Cognito group-based authorisation, Zod input validation, helmet, rate-limit, CORS, IAM least-privilege, and no-PII logging. Load when writing auth logic, API endpoints, or security-sensitive code in the Cognito stack.
user-invocable: false
stack: auth/cognito
paths:
  - "**/auth/**"
  - "**/middleware/**"
  - "**/cognito*"
  - "**/*.controller.*"
  - "**/*.route.*"
---

> **Scope — applies only if this project uses cognito.** This layer shares `**/auth/**` with `auth0`, `azure-ad` in `layers/auth/`, so more than one may load at once and their rules conflict. If the project is not using cognito, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

## Authentication & Authorization
- All protected routes use `authMiddleware` — Cognito JWT cryptographically verified with `CognitoJwtVerifier` from `aws-jwt-verify`: `await verifier.verify(token)` — never decoded-only
- Authorization by Cognito `groups` claim via `requireGroup('Admin')` — never by username or email
- Frontend tokens stored in memory or `HttpOnly` cookies — never `localStorage`
- Token refresh-and-retry on 401: attempt one refresh, redirect to login on failure
- Full `signOut()` on logout — never just deleting the cookie

## Input Validation
- ALL inputs validated with Zod at system boundaries: always call `Schema.parse(req.body)` — never access `req.body` fields directly
- Never use raw `req.body`, `req.params`, or `req.query` without Zod parse
- Validate type, format, length, and range — not just presence
- Return 400 with field-level error details on validation failure

## Secrets & Config
- Secrets in AWS Secrets Manager or SSM Parameter Store — never in source code
- `.env` only for local dev; always in `.gitignore`; never committed
- No API keys, tokens, or credentials in frontend bundles (`VITE_` vars are public)
- Environment variables validated with Zod at startup — fail fast if missing

## API Security
- `helmet()` on every Express app (sets secure HTTP headers)
- `express-rate-limit` on all public and auth endpoints
- No sensitive data in error responses returned to clients
- CORS configured with explicit `origin:` allowlist — never wildcard origins in production
- HTTPS only — no HTTP in staging or production

## Logging (what NOT to log)
- No `Authorization` headers or JWT tokens
- No passwords, secret keys, or credentials
- No PII unless required and explicitly scrubbed in the log pipeline
- No full request/response bodies on auth endpoints

## AWS IAM
- Least-privilege always — no `"Action": "*"` or `"Resource": "*"` in production policies
- Use IAM roles for service-to-service — never long-lived access keys for services
- Rotate any long-lived access keys (CI/CD) every 90 days
- Enable CloudTrail for all AWS accounts

## Dependency Security
- `npm audit` must pass with no high/critical vulnerabilities before any release
- Pin major dependency versions in `package.json`
- Review new dependencies before adding — check download count, maintainers, last publish

## Review checklist (every PR)
- [ ] No hardcoded secrets, tokens, or credentials
- [ ] All endpoints that need auth have `authMiddleware`
- [ ] Admin operations have `requireGroup('Admin')`
- [ ] All user inputs validated with Zod
- [ ] No sensitive data logged
- [ ] CORS configured correctly
- [ ] `npm audit` passes
