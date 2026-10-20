---
description: "Conventions for developing camofox-browser REST API routes"
globs: "src/routes/**"
alwaysApply: false
---

# Route Development Conventions

## Route Files
- Keep core API in `src/routes/core.ts` and OpenClaw compatibility in `src/routes/openclaw.ts`.
- Preserve endpoint compatibility unless a versioned migration is planned.

## Request Validation
- Validate required fields early and return `400` on malformed input.
- Keep user-scoped tab lookup consistent (`findTabById(tabId, userId)`).
- Enforce request body limits for evaluation endpoints.

## Concurrency and Timeouts
- Use `withUserLimit` and `withTimeout` for heavy tab operations.
- Use `withTabLock` for tab-mutating actions.
- Respect config-driven limits from `loadConfig()`.

## Auth and Security
- Apply conditional API-key checks where currently defined.
- Apply admin-key checks for destructive server controls (`/stop`).
- Sanitize cookie payloads and enforce bounds.

## Response Shape
- Keep responses stable for CLI and OpenClaw clients.
- Include `ok` and useful context fields when practical.
- Avoid returning raw internal errors; use safe error wrappers.

## Download/Resource Routes
- Keep user ownership checks on download lookup/content/delete.
- Enforce limits on blob resolution arrays and payload sizes.

## Logging
- Use structured `log()` calls with req context when available.
- Log operation failures with concise, non-sensitive details.
