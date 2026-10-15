---
name: social-content-parser
description: Parse public short-video and social share URLs through platform-specific APIs plus an aggregated fallback that covers 20+ platforms including Douyin, Kuaishou, Xiaohongshu, Bilibili, X/Twitter, YouTube, TikTok, Xigua, Haokan, Weishi, Pear Video, AcFun, Zhihu, Oasis, Meipai, Quanmin, Huya, Instagram, Doubao, Jimeng AI, and WeChat Channels. Use when a user wants to extract or archive public social links into local files, including cases where tracking parameters appear, X/Twitter posts need FXTwitter, or the primary parser needs a fallback route.
---

# Social Content Parser

Use this skill to turn a public short-video or social share URL into a local content package. Treat the aggregated fallback as the broad coverage layer; use the platform-specific routes when the link clearly belongs to Xiaohongshu, Douyin, Bilibili, or X/Twitter.

Supported platforms:

- Xiaohongshu via `https://api.bugpk.com/api/xhsjx`
- Douyin works via `https://api.bugpk.com/api/douyin`
- Douyin profiles via `https://api.bugpk.com/api/dyzy`
- Bilibili via `https://api.bugpk.com/api/bilibili`
- X/Twitter via `https://api.fxtwitter.com/:screen_name/status/:id`
- Aggregated fallback via `https://api.bugpk.com/api/short_videos` for 20+ platforms

Fallback order:

1. Platform-specific parser.
2. Platform-specific backup parser when available.
3. Aggregated short-video fallback.

## Workflow

1. Use `scripts/parse_social.mjs` as the primary entrypoint.
2. Pass a public share URL with `--url`.
3. Let the script auto-detect the platform from the URL.
4. For Douyin, let the script choose profile or work parsing:
   - `/user/...` links or `--kind profile` use the profile API and return `items`.
   - video, image, and live-photo share links use the work API and return `type=video|image|live`.
5. Strip tracking query parameters from share URLs before parsing.
6. If the primary parser fails or returns an empty payload, try the platform backup parser when available.
7. If both platform parsers fail, fall back to the aggregated short-video parser.
8. Preserve the raw API response in `raw.json`.
9. Normalize shared fields into `normalized.json`.
10. Write a human-readable `report.md`.
11. Download avatar, cover, images, live-photo media, and optional videos into `media/` unless disabled.

## Output Contract

Default output root:

- `./social-notes/`

Each parsed item creates one subfolder:

- `<platform>-<title>-<YYYY-MM-DD>-<id>/`

Files:

- `report.md`
- `normalized.json`
- `raw.json`
- `media/`

Normalized fields:

- `platform`
- `kind`
- `canonicalUrl`
- `fallbackUsed`
- `sourceUrl`
- `code`
- `msg`
- `type`
- `title`
- `desc`
- `author.name`
- `author.id`
- `author.avatar`
- `cover`
- `primaryVideo`
- `videoBackups`
- `images`
- `livePhoto`
- `music`
- `statistics`
- `parts`
- `items`
- `pagination`

## Commands

```bash
node scripts/parse_social.mjs --url "https://v.douyin.com/..."
node scripts/parse_social.mjs --url "https://www.douyin.com/user/..." --count 10
node scripts/parse_social.mjs --url "https://b23.tv/..."
node scripts/parse_social.mjs --url "https://www.xiaohongshu.com/explore/..."
```

Useful options:

```bash
node scripts/parse_social.mjs --url "<share-url>" --out-dir ./social-notes
node scripts/parse_social.mjs --url "<share-url>" --no-download
node scripts/parse_social.mjs --url "<share-url>" --download-video
node scripts/parse_social.mjs --platform douyin --kind profile --id "<sec_uid>" --count 10
node scripts/parse_social.mjs --from-file raw.json --platform douyin
```

## Platform Notes

- Xiaohongshu: `desc` is the正文. `video_backup` may be a string or list.
- Douyin profile: `/user/...` homepage links use `dyzy`; normalized output has `kind=profile`, `type=profile`, and an `items` list.
- Douyin work: video, image, and live-photo share links use `douyin`; normalized output has `kind=post` and `type=video|image|live`. `live_photo` includes paired image/video values.
- X/Twitter: the parser uses FXTwitter first, keeps tweet text, author info, media, metrics, and long-form article content when available, then falls back to the aggregated parser if needed.
- Share links often contain tracking parameters; the parser keeps the content path and drops those extras before calling the API.
- Do not assume every fallback wants the same cleaned URL; some fallback parsers prefer the original share link.
- When the primary parser misses content, the skill can fall back to the aggregated short-video parser to recover a usable result.
- Bilibili: supports short videos and collections. Use `videos` as parts when present. Direct video URLs may expire.
- Fallback parser: `short_videos` covers 20+ short-video platforms and is useful when the platform-specific parser misses a share link.

## Rules

- Do not use the official `key=value` sample as a real parameter.
- Do not invent engagement metrics. Keep unsupported fields empty or absent.
- Do not assume every platform returns the same schema.
- Do not download videos unless the user asks or `--download-video` is provided.
- Preserve `raw.json` exactly for debugging and future schema changes.
