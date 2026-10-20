# AGENTS.md — src/providers/fetch/cloudflare_browser/

## Purpose
Cloudflare Browser Rendering. Renders JavaScript before extraction — ideal for SPAs and dynamic pages. Tier 2 parallel race (with `linkup`).

## Vendor

- **Vendor**: Cloudflare
- **Endpoint**: `POST https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/markdown`
- **Auth**: `X-Auth-Email: <email>` + `X-Auth-Key: <api_key>` headers (the legacy auth flow — both required)
- **Env vars** (ALL THREE required):
  - `CLOUDFLARE_ACCOUNT_ID`
  - `CLOUDFLARE_EMAIL`
  - `CLOUDFLARE_API_KEY`
- **Returns**: `FetchResult` with markdown content. Title via `extract_markdown_title`.

## Conventions / Invariants

- Implements `FetchProvider`.
- All three env vars are validated at the top of `fetch_url` via `validate_api_key`. Missing any one throws `ProviderError(API_ERROR)`.
- The endpoint URL contains the account ID — interpolated, not configured separately.
- Per-provider timeout is `45000ms` (longer than the 30s default) because browser rendering can take a while.
- Response: `{ success: boolean, result?: <markdown>, errors?: [{ code, message }] }`.

## Gotchas

- **Three env vars** to register — easy to miss one.
- The endpoint uses CF's **legacy auth** style (X-Auth-Email + X-Auth-Key), NOT a Bearer token. Make sure the `CLOUDFLARE_API_KEY` is the legacy global API key, not an API token.

## Related

- Registered as `cloudflare_browser` in `../../unified/fetch.ts`.
- Tier 2 parallel race in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
