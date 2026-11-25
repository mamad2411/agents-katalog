---
name: nextjs-secure-bff
description: Use for security-sensitive Next.js backend-for-frontend work involving Route Handlers, Proxy, Server Actions, webhooks, callbacks, data access layers, server-only modules, request validation, rate limits, or public API boundaries. Prefer this skill when a Next.js task exposes HTTP endpoints or moves privileged data across server/client boundaries.
metadata:
  author: xiro
  version: "0.1.0"
  organization: local
  date: May 2026
  framework: Next.js
  frameworkVersion: "v16.2.6"
  supportedVersions:
    - "15.x.x"
    - "16.x.x"
  priority: high
  abstract: Focused real-project skill for secure Next.js backend-for-frontend surfaces. Includes Route Handler, Proxy, Server Action, webhook, DAL, DTO, environment, and header-boundary rules with concrete before/after examples.
---

# Next.js Secure BFF

Use this skill when Next.js acts as a public backend boundary, not just a rendering layer. Treat Route Handlers, Proxy, and Server Actions as externally reachable entry points that need normal backend security review.

## When to Apply

Use this skill when:
- Writing or reviewing `app/**/route.ts`, `proxy.ts`, webhook handlers, callback URLs, or BFF proxy endpoints
- Designing Server Actions that mutate data or depend on authenticated users
- Moving database, secrets, or internal API access into a Next.js app
- Auditing whether data passed to Client Components is minimized and safe
- Debugging leaks through headers, serialized action results, logs, or broad DTOs

## Load On Demand

Start with this file. Load detailed files only when the task needs them:

```
references/_sections.md
references/api-route-boundaries.md
references/security-server-action-authz.md
references/security-dal-dto.md
references/security-env-server-only.md
references/api-webhook-validation.md
references/api-proxy-headers.md
dataset/security/server-action-authz/correct.ts
sources/inventory.json
```

Each rule file includes:
- Why the pattern matters
- Incorrect and correct examples
- Dataset path with larger TypeScript/TSX examples
- Official source references

## Rule Categories by Priority

Resolve conflicts by lower priority number first. At the same priority, prefer Security, API, then Operations.

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Security & Authorization | CRITICAL | `security-` |
| 2 | Public API Boundaries | CRITICAL | `api-` |
| 3 | Operations & Runtime Controls | HIGH | `ops-` |

## Source Policy

Prefer official Next.js docs for framework semantics. For auth libraries, follow the library's official adapter docs after this skill establishes the Next.js security boundary. Do not copy community webhook, proxy, or Server Action snippets unless they validate inputs, re-authorize the caller, and filter outputs.
