---
description: Auth and security guardrails for server actions and API routes.
globs: "actions/**/*.ts, app/api/**/*.ts, middleware.ts"
alwaysApply: false
---

## Authentication (Clerk)
- In server actions that require auth, call `const userId = await checkAuth();` from `@/actions/auth/authCheck`.
- In API routes, verify auth server-side (never rely on client checks).
- Handle auth errors gracefully without leaking sensitive details.

## Security
- Sanitize/validate user inputs (Zod at boundaries).
- Handle sensitive data properly (never log secrets).
- Implement Content Security Policy where applicable.
- Implement proper CORS handling for API routes when cross-origin is expected.
