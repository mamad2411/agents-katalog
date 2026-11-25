---
name: api-security
description: Focused API security auditor for REST, GraphQL, and webhook endpoints in any stack. Use when the user is building or reviewing an API layer, mentions rate limiting, API keys, webhooks, CORS, or specifically wants "API security" checked — as opposed to a full-project audit.
---

# API Security — API Layer Auditor

A specialized skill for auditing the security of the API surface (REST/GraphQL/Webhooks) independent of the rest of the project.

## When to use this
- Reviewing API routes/controllers in any framework (Express, FastAPI, NestJS, Next.js API routes, Django REST Framework, Spring, etc.)
- Reviewing incoming/outgoing webhook design
- Reviewing API key issuance for external clients or partners

## Core Checks

### Authorization at Every Endpoint
- For each route: who is allowed to access it? Is there actual enforcement, or just a `// TODO: add auth` comment?
- GraphQL: check that introspection isn't exposed in production, and that query depth/complexity limiting exists to prevent nested-query denial-of-service.

### Rate Limiting
- Is every sensitive endpoint (login, OTP, search, checkout, password reset) protected by a rate limiter (Redis-backed or equivalent)?
- Is the limit keyed on IP alone (easy to bypass) or combined with user/device identity?

### CORS
- Is `Access-Control-Allow-Origin: *` combined with `credentials: true`? (Always Critical.)
- Explicit allow-list of origins instead of accepting everything.

### Input Validation at API Boundaries
- Strict schema validation (zod/joi/pydantic/class-validator) on every body/query/params
- Rejects unexpected extra fields (mass-assignment protection)

### Webhooks
- Incoming webhook signature (HMAC) verified before processing — never trust an unsigned webhook payload
- Nonce/timestamp used to prevent replay attacks

### Error Handling & Responses
- Correct HTTP status codes (401 vs 403 vs 404) without leaking information through inconsistency (e.g., returning 404 for an existing-but-unauthorized resource vs. 403 may be an intentional anti-enumeration choice — call out the tradeoff for the given context)
- No stack traces or internal details returned in production responses

### API Keys for External Clients
- Keys hashed/stored securely in the database (never plaintext)
- Revocation and rotation supported
- Scoped permissions per key instead of always granting full access

## Report Format
```
Endpoint: METHOD /path
Issue: [name]
Severity: Critical/High/Medium/Low
Evidence: [code or observed behavior]
Impact: [impact]
Fix: [suggested remediation]
```

## Rules
- Stay focused on the API boundary; hand off database-layer issues to `database-security`.
- Don't produce ready-to-use attack payloads — describe the issue and impact scenario briefly instead.
