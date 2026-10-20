---
name: Shared Code
description: 'Use when changing the shared Axios client, hooks, utilities, constants, or context.'
applyTo: "src/api.ts, src/hooks/**, src/utils/**, src/constants/**, src/context/**"
---

# Shared Code

- Use the configured Axios instance in `src/api.ts` for network requests. Do not add a parallel HTTP client or move requests to ad hoc `fetch` calls.
- Before adding a hook or utility, search `src/` for an existing implementation to reuse or extend.
- Never hardcode or expose secrets in client code, `VITE_*` variables, or logs. Send authentication data only as required by the API contract over HTTPS, and never persist authentication tokens in browser storage.
- Preserve the API client's `withCredentials` behavior for cookie-based authentication. Session cookies must be configured by the server with appropriate `HttpOnly`, `Secure`, and `SameSite` attributes; cookie-authenticated server operations must also enforce suitable CSRF protections.
- Keep pure helper functions in `src/utils`, reusable values in `src/constants`, and follow existing hook/context conventions.
- Before adding a shared abstraction, check whether a nearby implementation already covers the use case; keep abstractions small and focused.
