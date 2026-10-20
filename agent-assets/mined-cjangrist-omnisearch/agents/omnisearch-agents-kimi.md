# AGENTS.md — src/providers/fetch/kimi/

## Purpose
Kimi (Moonshot AI) coding-agent URL fetcher. Tier 1 solo (third waterfall step after Tavily and Firecrawl). Routed via Scrapfly residential proxy because `api.kimi.com`'s WAF blocks Cloudflare-Workers ASN.

## Vendor

- **Vendor**: Moonshot AI (Kimi)
- **Endpoint**: `POST https://api.kimi.com/coding/v1/fetch` (proxied through Scrapfly)
- **Auth**: `Authorization: Bearer <KIMI_API_KEY>` + Kimi-CLI identity headers
- **Env vars**: BOTH `KIMI_API_KEY` AND `SCRAPFLY_API_KEY` required
- **Returns**: `FetchResult` with markdown content from Kimi's coding-agent fetch.

## Conventions / Invariants

- Implements `FetchProvider`.
- Reuses the same Scrapfly proxy helper as `../../search/kimi/`.
- Sends Kimi-CLI identity headers so requests look identical on the wire.
- **Per-provider timeout**: 60000ms (longer than default) because the Scrapfly hop adds latency.

## Gotchas

- **Both keys required.** Setting only one leaves the provider inactive.
- **Same key as Kimi search** but a different code path. Kimi *search* (`../../search/kimi/`) is currently disabled in production per the ROI analysis; **Kimi *fetch* is still active**. They are independent.
- **Scrapfly cost**: each fetch goes through Scrapfly, which adds ~$0.00875 per residential proxy call on top of Kimi's own cost.

## Related

- Registered as `kimi` in `../../unified/fetch.ts`.
- Sister module: `../../search/kimi/` (currently disabled).
- Tier 1 solo (step 3) in `../../../server/fetch_orchestrator.ts CONFIG.waterfall`.
- `../../../docs/kimi-search-roi-analysis.md` — ROI analysis (about search, not fetch).
