# AGENTS.md — src/providers/fetch/sociavault/

## Purpose
SociaVault social-media extractor. Domain breaker — runs before the general waterfall for any URL whose hostname matches one of the supported social platforms. Routes the URL to a platform-specific endpoint and returns structured content.

## Vendor

- **Vendor**: SociaVault
- **Base URL**: `https://api.sociavault.com`
- **Auth**: `X-API-Key: <SOCIAVAULT_API_KEY>`
- **Env var**: `SOCIAVAULT_API_KEY`
- **Returns**: `FetchResult` with platform-specific content (post text + comments / metadata / engagement, etc.).

## Platform routing

`PLATFORM_ROUTES` in `index.ts` maps hostnames to endpoints:

| Platform | Hostnames | Endpoint |
|----------|-----------|----------|
| Reddit | reddit.com, www.reddit.com, old.reddit.com | `/v1/scrape/reddit/post/comments` |
| Twitter/X | twitter.com, www.twitter.com, x.com, www.x.com | `/v1/scrape/twitter/tweet` |
| YouTube | youtube.com, www.youtube.com, youtu.be | `/v1/scrape/youtube/video` (transcripts come from Supadata's earlier breaker) |
| Facebook | facebook.com, www.facebook.com, fb.com | `/v1/scrape/facebook/post` |
| Instagram | instagram.com, www.instagram.com | `/v1/scrape/instagram/post-info` |
| TikTok | tiktok.com, www.tiktok.com | `/v1/scrape/tiktok/video-info` |
| LinkedIn | linkedin.com, www.linkedin.com | `/v1/scrape/linkedin/post` |
| Threads | threads.net, www.threads.net | `/v1/scrape/threads/post` |
| Pinterest | pinterest.com, www.pinterest.com | `/v1/scrape/pinterest/pin` |

All requests are GET with `?url=<encoded-url>` (and `?param_name=` may vary per platform — see `PlatformRoute.param_name`).

## Conventions / Invariants

- Implements `FetchProvider`.
- `detect_route(url)` returns the matching platform route + param value, or `undefined` for non-social URLs (which causes the breaker check to fall through).
- The breaker config in `../../../server/fetch_orchestrator.ts` lists the same hostname set under `social_media`.

## Gotchas

- **YouTube hits Supadata first** (the YouTube breaker comes before social_media in the breaker order). SociaVault's YouTube endpoint runs only as a fallback if Supadata fails or is inactive.
- **Snapchat is in the breaker list but NOT in `PLATFORM_ROUTES`** — the breaker matches the domain, the provider has no route, the call falls through to general waterfall.

## Related

- Registered as `sociavault` in `../../unified/fetch.ts`.
- Domain breaker in `../../../server/fetch_orchestrator.ts CONFIG.breakers.social_media`.
