---
name: API
description: Consume, debug, and integrate REST APIs with best practices.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---

# API Integration Rules

## Request Gotchas
- Include `Content-Type: application/json` on POST/PUT/PATCH — omitting it causes silent 415 errors on many APIs
- Add `Accept: application/json` unless the API specifies a different format — some default to XML without it
- API keys in query params get logged in server access logs — prefer header-based auth when supported
- Tokens can expire mid-flight between request and response — handle 401 with single retry + refresh

## Silent Failures
- Some APIs return HTTP 200 with error in response body — validate response schema, not just status code
- Watch for empty arrays vs null vs missing keys — each means something different per API
- Paginated endpoints may return 200 with empty page when offset exceeds total — check total count first

## Retry and Resilience
- Use jittered exponential backoff: `delay = min(base * 2^attempt * (1 + random(0, 0.3)), max_delay)` with base=1s, max=30s
- Generally only retry on 429, 500, 502, 503, 504 — avoid retrying 400, 401, 403, 404 unless the API documents otherwise
- Read `Retry-After` header on 429 — it overrides your calculated backoff
- After 5+ consecutive failures to the same endpoint, back off entirely for 60s before retrying (circuit breaker)

## Pagination Traps
- Cursor-based pagination can return duplicate items if data changes between pages — deduplicate by ID
- Some APIs change `total_count` between requests — snapshot it on first page
- If page returns fewer items than `per_page` but includes a `next` cursor, keep paginating — it's not necessarily the last page

## Rate Limiting
- Track quota via `X-RateLimit-Remaining` header — throttle proactively before hitting 0, don't wait for 429
- Some APIs have hidden per-endpoint rate limits, not just global — monitor 429s per path
- Distribute requests evenly across the rate window instead of bursting at the start

## Webhooks
- Implement idempotent handlers with event ID dedup — providers retry on timeout and you'll get duplicates
- Return 200 immediately, process asynchronously — webhook providers timeout at 5-30s
- Verify webhook signatures when the provider supports them — don't trust payload origin without cryptographic proof
- Log the raw webhook body before parsing — invaluable when the provider changes their schema without notice

## Debugging Production Issues
- Log: method, URL, status code, response time, and `X-Request-Id` header for every API call
- APIs that work in dev but fail in prod: check IP allowlists, TLS version, SNI, and egress proxy settings
- When response data looks wrong, compare against the OpenAPI/Swagger spec — the spec is often more current than human-written docs
