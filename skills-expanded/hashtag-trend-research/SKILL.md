---
name: hashtag-trend-research
description: Research a TikTok hashtag or trend with the Scrape Everything API. Gets hashtag totals (video count, view count) for a seed tag and its variants, measures saturation (views per video), tracks growth between snapshots, and samples real posts using the trend from TikTok video links, TikTok sounds, Instagram reels search and YouTube Shorts search, then summarises the formats and hooks that perform. Use when the user asks whether a hashtag or trend is worth joining, which hashtags to use, how big a TikTok tag is, or wants to track a trend over time.
---

# Hashtag and trend research

Sizes a TikTok hashtag (and its variants), shows what posts riding the trend look like, and recommends which tags and formats to use.

## Inputs

- **Seed hashtag(s)**: with or without `#`, or tiktok.com/tag/... URLs.
- **Variants** (optional): if not given, propose 5-8 (singular/plural, with niche or year suffix, the brand's language) and confirm.
- **Sample posts** (optional): TikTok video URLs or a TikTok sound URL associated with the trend.
- **Previous snapshot** (optional): a saved JSON from an earlier run, to compute growth.

## Credit estimate

| Step | Calls | Credits |
| --- | --- | ---: |
| Tag sizing | `tiktok.hashtag` per tag (seed + ~6 variants) | ~7 |
| Sound sample (if a sound URL is known) | `tiktok.music` (top 12 videos) | 2 |
| Video detail | `tiktok.video` on 5 sample videos | 5 |
| Cross-platform sample | `instagram.reels_search` (limit 10) + `youtube.search` type shorts | 3 + 1 |

Typical run: 12-18 credits. Tag sizing alone: 1 credit per tag. Use live data (no `cache_days`) for trend tracking.

## How to call the API

Use the `scrapeeverything-api` skill if installed (MCP tool `tiktok_hashtag`, the `scrapeeverything` CLI, or `node <skills-dir>/scrapeeverything-api/scripts/se.mjs tiktok.hashtag hashtag=booktok`). Otherwise:

```bash
curl -sS https://api.scrapeeverything.com/v1/tiktok/hashtag -H "Authorization: Bearer $SCRAPEEVERYTHING_API_KEY" \
  -H "Content-Type: application/json" -d '{"hashtag":"booktok"}'
```

## Method

1. **Size every tag** with `tiktok.hashtag`: record `video_count`, `view_count`, `is_commerce`, `description`. Note that this endpoint returns stats only, not the tag's videos.
2. **Derive per tag**:
   - Views per video = `view_count` / `video_count`. High = room to get views; low = saturated or long-tail.
   - Size tier: mega (>10B views), large (1-10B), mid (100M-1B), niche (<100M).
   - Growth (if a previous snapshot exists): delta and % change of videos and views per day between snapshots.
3. **Sample posts on the trend** (TikTok has no public hashtag feed in this API, so sample through these routes):
   - If the user has TikTok video URLs, call `tiktok.video` on each for likes, shares, saves, plays, `music` and caption.
   - If a trend sound is known, `tiktok.music` returns `video_count` (how many videos use it) and the top videos, then enrich 3-5 with `tiktok.video`.
   - `instagram.reels_search` with the tag as `query` (and `date_posted: last-month`) shows how the trend is crossing to Reels.
   - `youtube.search` with `type: shorts` and the tag as `query` for Shorts.
4. **Pattern the samples**: hook in the first line, length, sound (original vs trending), on-screen format (tutorial, POV, duet, list), CTA. Save rate (saves / plays) and share rate (shares / plays) signal content people value or forward.
5. **Recommend**: a tag set mixing 1 large, 2-3 mid and 2-3 niche tags; which formats to copy; whether to join now (growing, healthy views/video) or skip (flat or saturated).
6. **Save a snapshot** JSON (`{date, tags:[{tag, video_count, view_count}]}`) so the next run can compute growth. Suggest re-running weekly.

## Output template

```markdown
# Hashtag research: #{seed}
_Date: {YYYY-MM-DD} · Tags checked: {n} · Credits used: {n}_

## Verdict
{Join now | Join with a niche angle | Skip}: {one-line reason}

## Tag sizing
| Tag | Videos | Views | Views/video | Tier | Growth since {date} |
| --- | ---: | ---: | ---: | --- | ---: |

## What the trend looks like
| Post | Platform | Plays/views | Likes | Shares | Saves | Sound | Hook |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |

## Patterns
- Hooks: ...
- Formats: ...
- Length: ...
- Sound: ...

## Recommended tag set
- Large: #...
- Mid: #... #...
- Niche: #... #...

## Next check
Re-run on {date + 7d} with this snapshot: `{snapshot file}`
```

## Guardrails

- Public, aggregate trend data only. Do not compile lists of the individual users posting under a tag.
- Flag `is_commerce` tags and anything touching health, finance or minors as needing extra review.
- Search-based samples (Instagram via search engine index, YouTube search) are not exhaustive; say so.
- Keep within the agreed credit budget; growth tracking needs only `tiktok.hashtag` calls (1 credit per tag).
