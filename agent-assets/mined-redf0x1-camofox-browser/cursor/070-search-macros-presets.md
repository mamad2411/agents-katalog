---
description: "camofox-browser search macros and geo presets reference"
alwaysApply: false
---

# Search Macros and Geo Presets

## Search Macros (from `src/utils/macros.ts`)

| Macro | Destination |
|---|---|
| `@google_search` | Google search |
| `@youtube_search` | YouTube search |
| `@amazon_search` | Amazon search |
| `@reddit_search` | Reddit search JSON |
| `@reddit_subreddit` | Reddit subreddit JSON |
| `@wikipedia_search` | Wikipedia search |
| `@twitter_search` | Twitter/X search |
| `@yelp_search` | Yelp search |
| `@spotify_search` | Spotify search |
| `@netflix_search` | Netflix search |
| `@linkedin_search` | LinkedIn search |
| `@instagram_search` | Instagram tag search |
| `@tiktok_search` | TikTok search |
| `@twitch_search` | Twitch search |

Usage pattern:
```json
{ "macro": "@google_search", "query": "camofox" }
```

## Geo Presets (from `src/utils/presets.ts`)

| Preset | Locale | Timezone | Coordinates |
|---|---|---|---|
| `us-east` | `en-US` | `America/New_York` | `40.7128, -74.006` |
| `us-west` | `en-US` | `America/Los_Angeles` | `34.0522, -118.2437` |
| `japan` | `ja-JP` | `Asia/Tokyo` | `35.6895, 139.6917` |
| `uk` | `en-GB` | `Europe/London` | `51.5074, -0.1278` |
| `germany` | `de-DE` | `Europe/Berlin` | `52.52, 13.405` |
| `vietnam` | `vi-VN` | `Asia/Ho_Chi_Minh` | `10.8231, 106.6297` |
| `singapore` | `en-SG` | `Asia/Singapore` | `1.3521, 103.8198` |
| `australia` | `en-AU` | `Australia/Sydney` | `-33.8688, 151.2093` |

Preset use in tab creation:
```json
{ "userId": "agent1", "sessionKey": "task1", "preset": "japan", "url": "https://example.com" }
```

Custom presets:
- Set `CAMOFOX_PRESETS_FILE` to JSON object path.
- Built-ins + custom are merged; custom keys override same-name built-ins.
