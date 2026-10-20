---
name: api-client
description: Build and maintain API client layers for desktop and web apps, including request wrappers, typed clients, authentication headers, retries, cancellation, streaming, pagination, error normalization, rate limits, and API-driven UI state.
---

# API Client

## Workflow

1. Inspect existing API wrapper, generated client, fetch/axios usage, and error handling.
2. Centralize base URL, auth headers, timeout, cancellation, and response parsing.
3. Normalize errors into a stable shape for UI and logs.
4. Handle pagination, streaming, uploads, downloads, and long-running requests explicitly.
5. Add retry only for safe or idempotent operations.
6. Add tests for request shape, error mapping, auth behavior, and cancellation when feasible.

## Required Checks

- Do not scatter raw endpoint strings across UI components.
- Do not expose secrets in client code.
- Distinguish network error, timeout, auth failure, validation error, rate limit, and server error.
- Respect abort/cancel flows for route changes, dialogs, and repeated user actions.
- Keep API model types close to the boundary and map to UI view models when useful.

## Output

Summarize client contract, error model, retry/cancel behavior, and verification.
