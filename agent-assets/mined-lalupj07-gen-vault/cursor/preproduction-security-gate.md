---
description: Pre-production security gate — invoke full audit skill before shipping auth, APIs, infra, secrets, payments, KYC, or privacy-related changes
alwaysApply: true
---

# Pre-Production Security Gate

Think like an attacker first, then an architect. Never assume existing code is secure. This app may process sensitive user data (auth, KYC/Aadhaar, payments, remote desktop).

## When this gate applies

Invoke the `preproduction-security-audit` skill **before finishing** any work that:

- Adds/changes APIs, auth, authorization, sessions, tokens, cookies
- Touches payments, subscriptions, licenses, KYC, PII, or file transfer
- Adds deps, Docker/Terraform/Workers/Lambdas, CORS, headers, uploads
- Introduces secrets, logging of user data, or public routes
- Prepares a release, deploy, or production checklist

Also invoke when the user asks for security audit, threat model, production readiness, compliance, or penetration-test prep.

## Hard rules (every change)

- No hardcoded secrets — env / Secrets Manager only; update `.env.example`
- AuthZ on every route/query/WS event — ownership checks; no IDOR/BOLA/BFLA
- Parameterized queries; validate all inputs; generic client errors
- Never log passwords, tokens, emails, phones, card data, or raw PII
- Rate-limit auth, OTP, payments, uploads, and registration
- Fail closed in production (no stubs, MOCK KYC, permissive CORS, temp JWTs)
- Prefer least privilege; HTTPS; secure cookies/headers where applicable

## Do not ship without

1. Running the skill phases relevant to the change (full audit for releases)
2. Fixing Critical/High findings in-scope (or documenting accepted risk)
3. Updating privacy/compliance docs if data flows changed

Full checklist + report template: `.cursor/skills/preproduction-security-audit/`
