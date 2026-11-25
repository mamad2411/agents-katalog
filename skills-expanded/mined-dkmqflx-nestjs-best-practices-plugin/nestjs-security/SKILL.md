---
name: nestjs-security
description: NestJS security hardening best practices. Use when securing a NestJS app — security headers, rate limiting, CORS, secrets, and input hardening. Triggers on helmet, ThrottlerModule, enableCors, CSRF, rate limiting, or production security review.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Security

Hardening rules for production NestJS apps (v10/v11). These cover the gaps the framework leaves open by default — headers, rate limiting, CORS, secrets, and input validation — for both the Express and Fastify platforms.

## When to Apply

- Preparing a NestJS service for production or running a security review.
- Exposing an API to the public internet or to browser clients.
- Adding security headers (helmet), rate limiting (ThrottlerModule), or CORS (enableCors).
- Handling auth: cookie-based sessions, CSRF, or password storage.
- Mitigating DoS via payload-size limits.

## Rules

- [helmet-security-headers](rules/helmet-security-headers.md) — apply helmet for secure HTTP response headers (Express vs Fastify).
- [rate-limiting-throttler](rules/rate-limiting-throttler.md) — limit abuse with @nestjs/throttler + a global ThrottlerGuard.
- [explicit-cors-origins](rules/explicit-cors-origins.md) — allowlist explicit origins; never wildcard with credentials.
- [validation-as-defense](rules/validation-as-defense.md) — global ValidationPipe with whitelist to reject unexpected input.
- [secrets-from-env](rules/secrets-from-env.md) — load secrets from env/secret manager; keep them out of git.
- [csrf-for-cookie-auth](rules/csrf-for-cookie-auth.md) — CSRF protection for cookie-based sessions.
- [limit-payload-size](rules/limit-payload-size.md) — cap request body size to mitigate DoS.
- [hash-passwords-and-disable-x-powered-by](rules/hash-passwords-and-disable-x-powered-by.md) — bcrypt/argon2 for passwords; drop the x-powered-by header.

## How to Use

Read the rule whose topic matches the change you are making, then apply the **Correct** pattern. When doing a full production review, walk every rule top to bottom as a checklist. Each rule notes Express vs Fastify differences where they matter — confirm which platform adapter the app uses before copying code.
