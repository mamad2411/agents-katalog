---
name: http-status-codes
description: |
  Use when writing API endpoints, HTTP handlers, controllers, or any code that
  returns HTTP responses. Guides selection of the correct status code and required
  headers. Trigger on ambiguous pairs: 200/201/202, 400/422, 401/403, 404/405/410,
  429/503, and when multiple error conditions are simultaneously true.
  Also use when reviewing response-returning code for correctness.
  DO NOT skip this skill because "the code is simple" — wrong status codes silently
  break clients.
---

# HTTP Response Codes & Headers

## Sources

- **RFC 9110** (IETF, 2022) — authoritative semantics for each status code. Section 15 covers all codes.
- **IANA HTTP Status Code Registry** — official list of all registered codes.
- **OWASP WSTG v4.2** — security guidance including enumeration prevention.
- **Note on precedence**: RFC 9110 Section 2.4 explicitly does NOT define an ordering when multiple error conditions apply — it delegates to implementations. The precedence in this skill reflects conventional middleware pipeline order and OWASP security guidance, not an RFC-mandated standard.

---

## When Multiple Conditions Are True

RFC 9110 does not specify which code wins when multiple errors are true. Use the conventional middleware check order — **return the code for the first failing check**:

| Priority | Check | Code |
|----------|-------|------|
| 1 | Request body is unparseable / structurally malformed | 400 |
| 2 | HTTP method not supported on this path | 405 |
| 3 | User is not authenticated | 401 |
| 4 | User lacks permission for this resource | 403 |
| 5 | Resource does not exist | 404 / 410 |
| 6 | Semantic validation fails | 422 |
| 7 | State conflict (duplicate, version mismatch) | 409 |

**Common examples:**

| Conditions true simultaneously | Return | Reason |
|---|---|---|
| Unauthenticated + resource missing | 401 | Auth check (3) before resource check (5) |
| Bad JSON body + unauthenticated | 400 | Parse check (1) before auth check (3) |
| Wrong HTTP method + unauthenticated | 405 | Method check (2) before auth check (3) |
| Unauthenticated + rate limited | 401 | Auth check before rate limiting in most stacks |
| Authorized + resource permanently deleted | 410 | Auth passes, resource check reveals gone |

### Security Exception: Prevent Resource Enumeration (OWASP WSTG v4.2)

Returning 401 or 403 reveals that a resource exists. For private or sensitive resources, this leaks information to unauthenticated attackers (they can probe IDs to find valid ones).

```
Is this resource's existence itself private/sensitive?
  YES → Always return 404 — for unauthenticated, unauthorized, AND missing cases
        Do NOT return 401 or 403; that confirms the resource path is valid
  NO  → Follow the priority table above
```

This is a deliberate architectural choice — comment it in code when applied. Note that timing differences can still leak existence; consistent response times are also required for full protection.

---

## Decision Flows

Work through these flows to pick the right code for common ambiguous pairs.

### Success (2xx)

```
Did the request create a new resource?
  YES → 201 Created  (+ Location header required)
  NO  → Is the work queued/async (result not ready yet)?
          YES → 202 Accepted
          NO  → Did the request have a body to return?
                  YES → 200 OK
                  NO  → 204 No Content
```

### 400 vs 422

```
Is the request body unparseable / structurally malformed (bad JSON, wrong content-type)?
  YES → 400 Bad Request
  NO  → Does it parse fine but fail validation (missing field, value out of range, business rule)?
          YES → 422 Unprocessable Content
```

### 401 vs 403

```
Does the request have valid authentication credentials (token present and valid)?
  NO  → 401 Unauthorized  (+ WWW-Authenticate header required)
  YES → Does the authenticated user have permission for this resource/action?
          NO  → 403 Forbidden
          YES → proceed
```

### 404 vs 405 vs 410

```
Does this URL path exist in the router at all?
  NO  → 404 Not Found
  YES → Does the HTTP method match a handler for this path?
          NO  → 405 Method Not Allowed  (+ Allow header required)
          YES → Was this specific resource permanently deleted (will never exist again)?
                  YES → 410 Gone
                  NO  → 404 Not Found
```

### 301 vs 302 vs 307 vs 308

```
Is the redirect permanent?
  YES → Does the method (POST etc.) need to be preserved on redirect?
          YES → 308 Permanent Redirect
          NO  → 301 Moved Permanently
  NO  → Does the method need to be preserved on redirect?
          YES → 307 Temporary Redirect
          NO  → 302 Found  (or 303 See Other to explicitly switch to GET)
```

### 429 vs 503

```
Did the CLIENT exceed a rate limit or quota?
  YES → 429 Too Many Requests  (+ Retry-After strongly recommended)
  NO  → Is the SERVER temporarily overloaded or a dependency is down?
          YES → 503 Service Unavailable  (+ Retry-After recommended)
```

---

## Required Headers by Status Code

| Code | Required Header | Example |
|------|----------------|---------|
| 201 | `Location` | `Location: /users/42` |
| 301, 302, 303, 307, 308 | `Location` | `Location: https://example.com/new-path` |
| 401 | `WWW-Authenticate` | `WWW-Authenticate: Bearer realm="api"` |
| 405 | `Allow` | `Allow: GET, POST, HEAD` |
| 429 | `Retry-After` (strongly recommended) | `Retry-After: 60` |
| 503 | `Retry-After` (recommended) | `Retry-After: 30` |
| 204 | — | No body; omit Content-Type |

---

## Universal Header Checklist

- **`Content-Type`** — required on any response with a body (`application/json`, `text/html`, etc.)
- **`Cache-Control`** — set explicitly; don't rely on defaults
  - Public cacheable: `Cache-Control: public, max-age=3600`
  - Private/user data: `Cache-Control: no-store`
  - Must revalidate: `Cache-Control: no-cache`
- **CORS headers** — if cross-origin requests are expected:
  - `Access-Control-Allow-Origin`
  - `Access-Control-Allow-Methods`
  - `Access-Control-Allow-Headers`

---

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| `200 OK` with `{"error": "not found"}` in body | Use `404 Not Found` |
| `400 Bad Request` for all validation errors | Use `422` for semantic validation failures |
| `403 Forbidden` when user isn't logged in | Use `401` — they haven't authenticated yet |
| `201 Created` without a `Location` header | Always include `Location: <url-of-created-resource>` |
| `200 OK` for async job submission | Use `202 Accepted` |
| `500 Internal Server Error` for client mistakes | 5xx = server fault; use 4xx for client errors |
| `404` for a resource that was permanently deleted | Use `410 Gone` so clients stop retrying |
| `401` for a private resource when unauthenticated | Use `404` to prevent resource enumeration |

---

## Complete Quick Reference (IANA Registry)

### 1xx — Informational

| Code | Name | Use when |
|------|------|----------|
| 100 | Continue | Server received request headers; client should send body |
| 101 | Switching Protocols | Upgrading to WebSocket or HTTP/2 |
| 102 | Processing | Server has received and is processing (WebDAV) |
| 103 | Early Hints | Send early Link headers before final response |

### 2xx — Success

| Code | Name | Use when |
|------|------|----------|
| 200 | OK | Standard success with response body |
| 201 | Created | New resource was created |
| 202 | Accepted | Request queued; result not yet available |
| 203 | Non-Authoritative Information | Transformed proxy response (metadata modified) |
| 204 | No Content | Success; no body to return |
| 205 | Reset Content | Success; client should reset the form/view |
| 206 | Partial Content | Range request fulfilled (file download resume) |
| 207 | Multi-Status | Multiple operations with individual statuses (WebDAV) |
| 208 | Already Reported | Resource already included in earlier binding (WebDAV) |
| 226 | IM Used | Delta encoding applied to response body |

### 3xx — Redirection

| Code | Name | Use when |
|------|------|----------|
| 300 | Multiple Choices | Multiple representations available |
| 301 | Moved Permanently | Resource permanently at new URL; method may change to GET |
| 302 | Found | Temporary redirect; method may change to GET |
| 303 | See Other | Redirect to GET another resource (post/redirect/get pattern) |
| 304 | Not Modified | Conditional GET; cached copy is still fresh |
| 307 | Temporary Redirect | Temporary redirect; method and body must be preserved |
| 308 | Permanent Redirect | Permanent redirect; method and body must be preserved |

### 4xx — Client Error

| Code | Name | Use when |
|------|------|----------|
| 400 | Bad Request | Request is malformed or unparseable |
| 401 | Unauthorized | Missing or invalid authentication credentials |
| 402 | Payment Required | Payment needed to access resource |
| 403 | Forbidden | Authenticated but lacks permission |
| 404 | Not Found | Resource does not exist |
| 405 | Method Not Allowed | Path exists but HTTP method is not supported |
| 406 | Not Acceptable | Server can't produce a response in the requested format (`Accept` header mismatch) |
| 407 | Proxy Authentication Required | Proxy requires authentication |
| 408 | Request Timeout | Client took too long to send the request |
| 409 | Conflict | State conflict (duplicate, version mismatch, concurrent edit) |
| 410 | Gone | Resource permanently deleted; will never return |
| 411 | Length Required | `Content-Length` header is required |
| 412 | Precondition Failed | `If-Match` or `If-Unmodified-Since` condition not met |
| 413 | Content Too Large | Request body exceeds server limit |
| 414 | URI Too Long | Request URI exceeds server limit |
| 415 | Unsupported Media Type | Server doesn't support the request `Content-Type` |
| 416 | Range Not Satisfiable | `Range` header out of bounds |
| 417 | Expectation Failed | `Expect` header condition cannot be met |
| 418 | I'm a Teapot | Reserved (RFC 2324 joke; never use in production) |
| 421 | Misdirected Request | Request sent to a server unable to handle it |
| 422 | Unprocessable Content | Parseable but fails semantic validation |
| 423 | Locked | Resource is locked (WebDAV) |
| 424 | Failed Dependency | Previous request in batch failed (WebDAV) |
| 425 | Too Early | Replayed request rejected to prevent replay attacks |
| 426 | Upgrade Required | Client must upgrade protocol (e.g. to TLS) |
| 428 | Precondition Required | Server requires conditional request (`If-Match`) |
| 429 | Too Many Requests | Client exceeded rate limit |
| 431 | Request Header Fields Too Large | Headers exceed server limit |
| 451 | Unavailable For Legal Reasons | Resource withheld due to legal demand |

### 5xx — Server Error

| Code | Name | Use when |
|------|------|----------|
| 500 | Internal Server Error | Unexpected server fault |
| 501 | Not Implemented | Server doesn't support the request method |
| 502 | Bad Gateway | Upstream server returned an invalid response |
| 503 | Service Unavailable | Server temporarily down or overloaded |
| 504 | Gateway Timeout | Upstream server timed out |
| 505 | HTTP Version Not Supported | Server doesn't support the HTTP version used |
| 506 | Variant Also Negotiates | Content negotiation configuration error |
| 507 | Insufficient Storage | Server cannot store the representation (WebDAV) |
| 508 | Loop Detected | Infinite loop detected processing request (WebDAV) |
| 511 | Network Authentication Required | Client must authenticate to access network |

---

## Non-Standard / Framework-Specific Codes

These are not in the IANA registry. Document their use in comments.

| Code | Name | Origin | Notes |
|------|------|--------|-------|
| 419 | Page Expired | Laravel | CSRF token expired or session timeout. Use `422` or `403` in non-Laravel APIs. |
| 420 | Enhance Your Calm | Twitter API v1.0 | Rate limit. Deprecated — Twitter now uses standard `429`. |
| 444 | No Response | nginx | Connection closed without response. Never transmitted to client; nginx log only. |
| 499 | Client Closed Request | nginx | Client disconnected before response. Log only; never sent. |
| 509 | Bandwidth Limit Exceeded | cPanel / Apache | Hosting bandwidth quota exceeded. Not recognized by most clients. |
