---
name: py-django-cors-headers-4-9-debug
description: Diagnoses django-cors-headers 4.9.x ordinary requests and preflight failures across origin matching, middleware ordering, URL scope, redirects, headers, credentials, CSRF, and browser policy.
---

# django-cors-headers 4.9 Debug

Use this skill when a browser reports a CORS error, an `OPTIONS` request fails, or expected CORS response headers are missing.

## Operating rules

- Reproduce the exact origin, method, URL, and request headers.
- Inspect the network request and response before changing settings.
- Separate CORS failure from authentication, authorization, CSRF, proxy, TLS, redirect, and application errors.
- Do not fix unknown failures by enabling allow-all or credentials.
- Compare an allowed origin with a deliberately rejected near miss.

## Workflow

Use `workflows/debug-cors-request-workflow.md` for systematic diagnosis.

## Resource

Use `resources/preflight-troubleshooting.md` to map browser symptoms to server-side checks.

## Completion criteria

- Root cause is identified at the correct layer.
- Policy remains least privilege.
- A regression test reproduces the failure and the fix.
- No broad wildcard or unnecessary trusted origin was introduced.
