---
name: social-api
description: Debug and extend social media platform integrations in ettametta. Use when working with OAuth flows, content publishing, trend scanning, CloakBrowser stealth scraping, or platform-specific API issues. Covers 8 platforms: YouTube, TikTok, Instagram, Facebook, X, LinkedIn, Snapchat, Twitch.
---

# Social Media API Integration

Skill for working with ettametta's multi-platform social media integrations — OAuth, publishing, discovery/scraping, and the CloakBrowser stealth engine.

## Platform Status Matrix

| Platform | Discovery | Publishing | OAuth | CloakBrowser | Status |
|----------|-----------|------------|-------|--------------|--------|
| YouTube | API v3 | API (resumable) | Full | Yes | **Full** |
| TikTok | Scraping | Video Kit API (chunked) | Full | Yes | **Full** |
| Instagram | Scraping | Graph API v18.0 | Full | Yes | **Full** |
| Facebook | Scraping | Graph API v20.0 | Via Meta/IG | Yes | **Full** |
| X/Twitter | Scraping | API v1.1 upload + v2 tweet | Full (PKCE) | Yes | **Full** |
| LinkedIn | Scraping | Marketing API v2 | Full | Yes | **Full** |
| Snapchat | Scraping | Marketing API | Full | No | **Full** |
| Twitch | Scraping | Helix (clips only) | Full | No | **Full** |

## Quick Diagnostics

### Check OAuth token status
```bash
# Tokens are stored encrypted in the SocialAccount DB table
# Check via API (requires auth)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/publish/accounts
```

### Test a scanner
```python
from src.services.discovery.cloak_tiktok_scanner import CloakTikTokScanner
scanner = CloakTikTokScanner()
results = await scanner.scan_trends(niche="AI technology", limit=10)
```

### Test a publisher
```python
from src.services.optimization.tiktok_publisher import TikTokPublisher
pub = TikTokPublisher()
result = await pub.upload_video(video_path, title="Test", description="Test")
```

## Key Files

### OAuth
| File | Purpose |
|------|---------|
| `src/api/routes/publish/oauth.py` | OAuth initiate + callback routes for all 7 platforms (746 lines) |
| `src/services/optimization/auth.py` | `TokenManager` singleton — Fernet encryption, DB storage, auto-refresh |
| `src/services/optimization/cookie_manager.py` | Cookie fallback (TikTok, YouTube, X, LinkedIn only) |

### Discovery (Scanners)
| File | Purpose |
|------|---------|
| `src/services/discovery/scanner_base.py` | `DiscoveryScannerBase` abstract class, viral scoring |
| `src/services/discovery/scanner_service.py` | `ScannerService` — parallel multi-platform scan with circuit breakers |
| `src/services/discovery/cloak_scanner.py` | `CloakBrowserScanner` — stealth engine (451 lines) |
| `src/services/discovery/cloak_platform_config.py` | Platform configs for CloakBrowser (6 platforms) |
| `src/services/discovery/youtube_scanner.py` | YouTube Data API v3 (only scanner using official API) |
| `src/services/discovery/cloak_*_scanner.py` | Per-platform CloakBrowser wrappers with httpx fallback |

### Publishing
| File | Purpose |
|------|---------|
| `src/services/optimization/publisher_base.py` | `SocialPublisher` abstract — retry, rate limits, file validation |
| `src/services/optimization/youtube_publisher.py` | YouTube resumable upload |
| `src/services/optimization/tiktok_publisher.py` | TikTok chunked upload (10MB chunks) |
| `src/services/optimization/instagram_publisher.py` | Meta Graph API 3-step flow |
| `src/services/optimization/facebook_publisher.py` | Meta Graph API 4-step flow |
| `src/services/optimization/x_publisher.py` | Hybrid v1.1 upload + v2 tweet |
| `src/services/optimization/linkedin_publisher.py` | LinkedIn Marketing API 3-step flow |
| `src/services/optimization/snapchat_publisher.py` | Snapchat Marketing API |
| `src/services/optimization/twitch_publisher.py` | Twitch Helix (clip creation only) |

### Common
| File | Purpose |
|------|---------|
| `src/api/routes/publish/common.py` | `SUPPORTED_PLATFORMS` registry (8 platforms) |
| `src/shared/enums.py` | `ContentPublishStatus`, `SystemJobStatus` |
| `src/services/discovery/models.py` | `ContentCandidate` Pydantic model |

## OAuth Flow Pattern

All platforms follow the same pattern:

1. **Initiate:** `GET /publish/auth/{platform}` → redirects to platform's auth page
2. **Callback:** `GET /publish/auth/{platform}/callback` → exchanges code for tokens
3. **Storage:** `token_manager.store_token(platform, access_token, refresh_token, expires_in)`
4. **Usage:** `token_manager.ensure_valid_token(platform, user_id)` → auto-refreshes if expired
5. **Headers:** `token_manager.get_auth_headers(platform, user_id)` → `Authorization: Bearer ...`

State parameter is base64-encoded JSON with `user_id` and CSRF token.

## CloakBrowser Architecture

The stealth scraper (`discovery-scraper` service at `http://discovery-scraper:8010`) uses headless Playwright with anti-detection.

**Platform configs** (in `cloak_platform_config.py`):
- YouTube: dedicated `/scrape/youtube` endpoint
- TikTok: generic `/scrape/web`, requires scroll, waits for `[data-e2e="search_video-item"]`
- Instagram: generic `/scrape/web`, hashtag pages, requires scroll
- Facebook: generic `/scrape/web`, Watch search, requires scroll
- X/Twitter: generic `/scrape/web`, live search, requires scroll
- LinkedIn: generic `/scrape/web`, content search, requires scroll

**Concurrency:** Semaphore limits to 3 concurrent scans.

**Fallback:** Each `cloak_*_scanner.py` wraps CloakBrowser primary + httpx fallback.

## Common Issues & Fixes

### Snapchat/Twitch OAuth — fixed

Redirect URIs for Snapchat and Twitch are now configured in `src/api/config/settings.py`. If you see `AttributeError` on these platforms, check the env vars `SNAPCHAT_REDIRECT_URI` and `TWITCH_REDIRECT_URI` are set.

### Instagram publisher rejects local files

`_resolve_video_uri()` explicitly rejects local file paths. Videos must be accessible via URL (S3, cloud storage, or a local HTTP server). Upload to storage first, then pass the URL.

### LinkedIn refresh fails (no refresh_token stored)

The LinkedIn callback stores only `access_token` and `expires_in`, not `refresh_token`. Fix the callback in `oauth.py` to also store the refresh token when available.

### Scanner returns empty results

Check circuit breaker state — if a platform has failed too many times, the breaker opens and returns empty results for 300s. Check logs for `"Circuit breaker open"`.

### Rate limiting (429 errors)

The `SocialPublisher` base class detects 429s and respects `Retry-After` headers. If persistent, the circuit breaker will open. Check if you're hitting platform-specific upload limits.

### Two YouTube publisher implementations

There are two separate `YouTubePublisher` classes:
- `src/services/optimization/youtube_publisher.py` — uses `token_manager`
- `src/services/distribution/publishing.py` — loads tokens from disk files

Use the `optimization/` one (it's the standard pattern).

## Adding a New Platform

1. Create scanner: extend `DiscoveryScannerBase` in `src/services/discovery/`
2. Create publisher: extend `SocialPublisher` in `src/services/optimization/`
3. Add OAuth routes in `src/api/routes/publish/oauth.py`
4. Add platform to `SUPPORTED_PLATFORMS` in `src/api/routes/publish/common.py`
5. Add redirect URI to settings
6. (Optional) Create CloakBrowser wrapper with httpx fallback

## References

- [OAuth Flow Details](references/oauth-flows.md)
- [CloakBrowser Platform Configs](references/cloak-configs.md)
