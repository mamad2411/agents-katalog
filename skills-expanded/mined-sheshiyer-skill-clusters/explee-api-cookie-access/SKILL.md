---
name: explee-api-cookie-access
description: "Use Explee session cookies to authenticate and call Explee public API endpoints safely and consistently. USE WHEN a task matches the Craft workspace workflow for explee-api-cookie-access."
cluster: explee-master
version: 1.0.0
origin: "craft-agent workspace"
---

# Explee API Cookie Access

Use this skill when the user asks to work with Explee APIs that require browser/session cookies.

## Goal

Authenticate API calls to Explee using user-provided cookie headers and execute requests against Explee API endpoints.

## Base URLs

- Documentation UI: https://api.explee.com/public/api/docs
- API host: https://api.explee.com

## Operating Rules

1. **Never hardcode cookies in files.**
   - Ask the user to provide cookies for the current task/session.
   - Treat cookies as sensitive credentials.

2. **Use Cookie header authentication.**
   - Include the cookie string exactly as provided by the user.
   - Preferred header form:
   - `Cookie: session=<...>; token=<...>; other_cookie=<...>`

3. **Do not confuse URL tracking params with cookies.**
   - Query params like `_gl` and `_gcl_au` are URL analytics parameters.
   - They are **not** valid as HTTP Cookie header values by themselves.
   - Only use browser cookie key/value pairs from the `Cookie` request header.

4. **Discover endpoints from docs first.**
   - Start from the docs page and identify exact endpoint paths, methods, and payload schemas.
   - Confirm assumptions before mutating requests (POST/PUT/PATCH/DELETE).

5. **Safe request progression.**
   - Test auth with a read-only endpoint first.
   - Then perform the requested API operation.

6. **Be explicit in outputs.**
   - Report method, endpoint, status code, and summarized response.
   - If unauthorized, ask for refreshed cookies.

## Request Templates

### 1) Generic authenticated request

```bash
curl 'https://api.explee.com/<endpoint>' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: <cookie_string>'
```

### 2) Safer local terminal workflow (env var)

```bash
export EXPLEE_COOKIE='session=<...>; token=<...>; other_cookie=<...>'

curl 'https://api.explee.com/<endpoint>' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Cookie: ${EXPLEE_COOKIE}"
```

### 3) GET with query params

```bash
curl 'https://api.explee.com/<endpoint>?page=1&limit=20' \
  -H 'Accept: application/json' \
  -H "Cookie: ${EXPLEE_COOKIE}"
```

### 4) POST with JSON body

```bash
curl 'https://api.explee.com/<endpoint>' \
  -X POST \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H "Cookie: ${EXPLEE_COOKIE}" \
  --data '{"key":"value"}'
```

## Troubleshooting

- **401/403**: Cookie expired or incomplete. Ask user for a fresh cookie string.
- **404**: Endpoint path likely differs from docs guess; re-check docs.
- **415/422**: Payload format mismatch; re-validate schema from docs.
- **CORS confusion**: Browser CORS errors do not apply to server-side `curl`/agent HTTP calls.
- **Cookie missing keys**: If session cookie exists but auth still fails, ask for the full cookie set from an authenticated request.
## What to Avoid

- Do not store cookies in repository files or plans.
- Do not print full cookie values in final user-visible summaries.
- Do not run destructive endpoints without confirming intent.
