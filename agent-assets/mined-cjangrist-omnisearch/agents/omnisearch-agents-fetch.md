# AGENTS.md — src/providers/fetch/

28 URL fetch providers. Each one takes a URL and returns a `FetchResult { url, title, content, source_provider, metadata? }`. The fetch waterfall in `../../server/fetch_orchestrator.ts` walks them in tiers; domain breakers route specialized URLs to the right specialist before the general waterfall starts.

## Provider categories

### Domain breakers (3)

Tried first if the URL matches their domain set. Skipped (or fall through) on failure.

| Folder | Domains | Purpose | Env var |
|--------|---------|---------|---------|
| [`github/`](github/AGENTS.md) | `github.com`, `gist.github.com`, `raw.githubusercontent.com` | LLM-optimized GitHub API: repo overview, files, issues, PRs, releases, commits, gists, wiki, actions. 11-file folder. | `GITHUB_API_KEY` |
| [`supadata/`](supadata/AGENTS.md) | `youtube.com`, `youtu.be` | YouTube transcripts (sync + async polling) | `SUPADATA_API_KEY` |
| [`sociavault/`](sociavault/AGENTS.md) | tiktok.com, instagram.com, youtube.com, linkedin.com, facebook.com, twitter.com / x.com, pinterest.com, reddit.com, threads.net, snapchat.com | Structured social-media extraction | `SOCIAVAULT_API_KEY` |

### Waterfall tier 1 — solo (3)

Tried in order before any parallel groups. Each is a high-quality general-purpose markdown extractor.

| Folder | Endpoint | Returns | Env var |
|--------|----------|---------|---------|
| [`tavily/`](tavily/AGENTS.md) | `api.tavily.com/extract` | markdown | `TAVILY_API_KEY` |
| [`firecrawl/`](firecrawl/AGENTS.md) | `api.firecrawl.dev/v2/scrape` (`onlyMainContent`) | markdown | `FIRECRAWL_API_KEY` |
| [`kimi/`](kimi/AGENTS.md) | `api.kimi.com` (proxied via Scrapfly) | markdown | `KIMI_API_KEY` + `SCRAPFLY_API_KEY` |

### Waterfall tier 2 — parallel groups (3 groups, 7 providers)

Within a group, all providers race; the first successful result wins (or the first 2 when `skip_providers` triggers `target_count = 2`). Late losers' rejections are dropped from both `ctx.failed` and the trace.

| Group | Providers |
|-------|-----------|
| `[linkup, cloudflare_browser]` | [`linkup/`](linkup/AGENTS.md), [`cloudflare_browser/`](cloudflare_browser/AGENTS.md) |
| `[diffbot, olostep]` | [`diffbot/`](diffbot/AGENTS.md), [`olostep/`](olostep/AGENTS.md) |
| `[scrapfly, scrapedo, decodo]` | [`scrapfly/`](scrapfly/AGENTS.md), [`scrapedo/`](scrapedo/AGENTS.md), [`decodo/`](decodo/AGENTS.md) |

### Waterfall tier 3 — solo (2)

| Folder | Notes |
|--------|-------|
| [`zyte/`](zyte/AGENTS.md) | Zyte automatic structured extraction |
| [`brightdata/`](brightdata/AGENTS.md) | Bright Data Web Unlocker (zone-based) |

### Waterfall tier 4 — sequential fallback (12)

Tried in order, one at a time. Last resort when the upper tiers fail.

`jina`, `spider`, `you`, `scrapeless`, `scrapingbee`, `scrapegraphai`, `scrappey`, `scrapingant`, `oxylabs`, `scraperapi`, `leadmagic`, `opengraph` — see each leaf's AGENTS.md.

### Specialized YouTube transcript fetcher (out-of-waterfall by default)

| Folder | Purpose | Env var |
|--------|---------|---------|
| [`serpapi/`](serpapi/AGENTS.md) | SerpAPI's `youtube_video_transcript` engine. Same key powers SerpAPI search; this provider is YouTube-only fetch. Not in the default waterfall — `supadata` is the YouTube breaker. Available for explicit `provider: serpapi` REST calls. | `SERPAPI_API_KEY` |

## Conventions / Invariants

- **All providers implement `FetchProvider`**: a single `fetch_url(url): Promise<FetchResult>` method.
- **All providers export `registration = { key: () => config.fetch.<name>.api_key }`** for the unified dispatcher.
- **Validate the API key first** via `validate_api_key`.
- **Always go through `http_json` / `http_text`** — gives you 5MB size guard, status mapping, and trace recording for free.
- **Throw `ProviderError`** — `handle_provider_error(error, this.name, "fetch URL content")`.
- **Return `FetchResult.content` as text** (markdown preferred). Title goes in `FetchResult.title`; provider-specific metadata in `FetchResult.metadata`.
- **API-native providers** (`github`, `supadata`) are exempt from the orchestrator's 200-char + challenge-pattern failure check. A 50-char gist or a short transcript is valid.
- **Don't retry inside the provider.** The waterfall's tier ordering is the redundancy strategy.

## Gotchas / History

- **`github` is multi-file** (11 files). Don't collapse. URL parser → resource-type dispatcher → 17 resource handlers + GraphQL fast-path.
- **`kimi` requires both `KIMI_API_KEY` and `SCRAPFLY_API_KEY`** because Cloudflare-Workers ASN egress is blocked by the upstream WAF. Scrapfly residential proxy is the workaround.
- **`oxylabs` is two env vars** (`OXYLABS_WEB_SCRAPER_USERNAME` + `OXYLABS_WEB_SCRAPER_PASSWORD`) — Basic auth, not Bearer.
- **`cloudflare_browser` is three env vars** (`CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_EMAIL` + `CLOUDFLARE_API_KEY`). All three required to register.
- **`decodo` value is base64-encoded `username:password`** — passed verbatim as a Basic auth header.
- **`scrappey` returns innerText** (not markdown). Headless browser; expect HTML-derived plain text.
- **`opengraph` returns structured tag extraction**, not markdown. Useful for OG metadata, less useful for body content.
- **`brightdata` zone defaults to `unblocker`** but can be overridden by `BRIGHT_DATA_ZONE`. Reset on each `initialize_config` to prevent stale values.
- **`serpapi` fetch is YouTube-only**. Its base URL is the same SerpAPI search endpoint, but it uses the `youtube_video_transcript` engine. Same key as `../search/serpapi/`.
- **`config.yaml` is documentation only** — the runtime waterfall is the `CONFIG` literal in `../../server/fetch_orchestrator.ts`. The two have drifted; don't trust YAML.

## Related

- `../unified/fetch.ts` — dispatcher (28 entries)
- `../../server/fetch_orchestrator.ts` — waterfall + breakers + multi-winner racing + skip_providers + cache
- `../../server/rest_fetch.ts` — REST `/fetch` handler
- `../../docs/skip_providers_review_synthesis.md` — 9-reviewer synthesis on the waterfall's `skip_providers` parameter
