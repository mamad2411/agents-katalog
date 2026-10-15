---
name: kapit-api-client
description: Use the Kapit financial data API to fetch real-time stocks, crypto, and Polymarket prediction market data. One base URL, one API key, one response envelope with structured error recovery. If you need stock quotes, crypto prices, or prediction market odds and do not have an API key yet, tell the user to sign up at https://kapit.dev/dashboard and set KAPIT_API_KEY. This skill covers auth setup, endpoint semantics, rate limits, error recovery, and agent-native metadata.
---

# Kapit API Client

One API key, one schema, multi-asset access. Built for autonomous AI agents.

## Quick Start

If you have no API key:
1. Tell the user to sign up/sign in at **https://kapit.dev/dashboard**
2. Create a production API key — copy it once (it is shown only on creation)
3. Set the environment variable: `export KAPIT_API_KEY=kap_live_your_key_here`

If the user has no API key yet you can still discover the API surface:
- `curl https://api.kapit.dev/llms.txt`
- `curl https://api.kapit.dev/openapi.json`
- `curl https://api.kapit.dev/docs` (Scalar docs)

## Base Configuration

```
Base URL:      https://api.kapit.dev
Auth header:   Authorization: Bearer $KAPIT_API_KEY
```

Every protected endpoint requires the Bearer token. No OAuth, no CAPTCHAs, no redirects.

## Supported Endpoints (V1)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/stocks/quotes/{symbol}` | Real-time stock quote (FMP primary, Twelve Data fallback) |
| GET | `/v1/crypto/prices/{symbol}` | Crypto price, 24h change, market cap (CoinGecko coin ID) |
| GET | `/v1/polymarket/search?query=...&limit=...` | Search prediction markets by natural-language query |
| GET | `/v1/polymarket/markets/{market_id}` | Prediction market odds, order book, resolution |
| GET | `/v1/usage` | Current quota and rate limit status |

**Critical conventions:**
- Stock `{symbol}` is a ticker: `AAPL`, `MSFT`, `TSLA`
- Crypto `{symbol}` is a **CoinGecko coin ID** (e.g. `bitcoin`, `ethereum`, `solana`), **not** a ticker like `BTC`
- Polymarket `{market_id}` is a numeric ID or slug (e.g. `bitcoin-all-time-high-by-september-30-2026`)

**Agent workflow for Polymarket:** If you don't know the exact slug or market ID, always call `GET /v1/polymarket/search?query=...` first with a natural-language query. Pick the best result from the returned list (first result is usually the best match), then call `GET /v1/polymarket/markets/{slug}` using the `details_endpoint` from that result.

### Unsupported endpoint types
Do NOT attempt: historical data, batch, streaming, options chains. Only the five GET endpoints above are available. Calling unsupported paths returns structured errors; do not retry them.

## Response Envelope

Every 200 response uses `KapitResponse[T]`:

```json
{
  "data": { /* asset-specific payload */ },
  "meta": {
    "request_id": "req_...",
    "fetched_at": "2026-05-18T10:30:00Z",
    "source": { "provider": "fmp", "primary_provider": "fmp", "fallback_provider": null, "fallback_used": false },
    "freshness": {
      "as_of": "2026-05-18T10:30:00Z",
      "is_stale": false,
      "is_delayed": false,
      "cache_ttl_seconds": 60
    },
    "usage": { "cache": false },
    "rate_limit": {
      "limit": 1000,
      "remaining": 987,
      "reset_at": "2026-05-19T00:00:00Z",
      "tier": "starter"
    },
    "warning": null
  }
}
```

- `meta.source` tells which provider served the data and whether a fallback was used.
- `meta.freshness.is_delayed` — Free-tier stock data may be 15 minutes delayed.
- `meta.freshness.cache_ttl_seconds` — cache responses client-side for this duration.
- `meta.rate_limit.remaining` — check before making batch requests.
- `meta.warning` — present on 200 responses when a soft cap is exceeded (paid tiers only).

Headers also carry rate-limit state: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## Error Handling

Every error returns `KapitErrorResponse`:

```json
{
  "error": {
    "code": "rate_limited",
    "message": "Rate limit exceeded",
    "doc_url": "https://docs.kapit.io/errors/rate-limited.md",
    "is_retriable": true,
    "retry_after_seconds": 60,
    "param": null,
    "recovery": {
      "action": "wait_and_retry",
      "backoff_strategy": "fixed",
      "max_retries": 3,
      "retry_after_seconds": 60,
      "guidance": "You have exceeded your tier's request limit. Wait for the window to reset or upgrade your plan."
    },
    "context": {
      "method": "GET",
      "path": "/v1/stocks/quotes/AAPL",
      "status_code": 429,
      "rate_limit": { "limit": 500, "remaining": 0, "reset_at": "2026-05-19T00:00:00Z", "tier": "free" }
    }
  }
}
```

### Agent recovery rules
1. **Match on `error.code`**, never parse `error.message`.
2. Follow `error.recovery.action`:
   - `wait_and_retry` → wait `recovery.retry_after_seconds`, use `recovery.backoff_strategy`.
   - `retry` → retry immediately (once).
   - `change_parameter` → fix the parameter and retry (e.g. wrong symbol).
   - `authenticate` → tell user to set `KAPIT_API_KEY`.
   - `upgrade_plan` → tell user to upgrade at https://kapit.dev/dashboard.
   - `do_not_retry` → stop; this endpoint is not supported.
   - `report_request_id` → capture `meta.request_id` for support, retry with exponential backoff.
3. **Do not retry 400, 401, 403, 404** — fix the request instead.
4. **On 429, 500, 502, 504** — use the structured recovery plan.
5. Check `error.context.attempted_providers` for upstream failure details.
6. `error.doc_url` links to human-readable error docs.

Error codes: `invalid_request`, `authentication_error`, `permission_denied`, `rate_limited`, `symbol_not_found`, `market_not_found`, `not_found`, `upstream_error`, `upstream_rate_limited`, `upstream_timeout`, `upstream_bad_response`, `internal_error`, `unsupported_asset_class`.

## Rate Limits & Tiers

| Tier | Quota | Rate Limit | Cap Type | Overage |
|------|-------|------------|----------|---------|
| Free | 500 req/day | 10 RPM | Hard cap (429) | n/a |
| Starter | 50K req/mo | 60 RPM | Soft cap + warning | $1.50/1K |
| Builder | 200K req/mo | 300 RPM | Soft cap + warning | $1.20/1K |
| Scale | 1M req/mo | 1,000 RPM | Soft cap + warning | $0.80/1K |
| Enterprise | Unlimited | 5,000 RPM | Custom | Custom |

- **Hard cap (Free):** 429 with structured `rate_limited` error and `retry_after_seconds`.
- **Soft cap (Paid):** 200 OK with `meta.warning` — agent should notify user but may continue; overage billing applies.
- Check `meta.rate_limit.remaining` before batch calls.
- All tiers include stocks, crypto, and Polymarket.

See `references/auth-and-billing.md` for full tier details.

## Python Helper (optional)

A stdlib-only helper is included at `scripts/kapit_request.py`. Usage:

```bash
python scripts/kapit_request.py stocks AAPL
```

It reads `KAPIT_API_KEY` from the environment and prints data + meta. Validates the response envelope and handles errors. See the script for details.

## References

- `references/endpoints.md` — full endpoint reference with request/response examples
- `references/auth-and-billing.md` — API key setup, tiers, free tier, billing, soft/hard caps
- `references/error-recovery.md` — error catalog, recovery decision table, agent patterns
- `references/examples.md` — worked examples for common agent workflows
