---
name: competitor-content-audit
description: Audit one or more competitors' public social content on Instagram, TikTok, YouTube and X with the Scrape Everything API. Finds their top-performing posts, posting cadence and best days, format mix (reels vs photos vs carousels, shorts vs long-form), recurring themes, hooks and calls to action, then turns it into gaps and recommendations for the user's own brand. Use when the user asks to "audit", "benchmark" or "spy on" competitor content, compare brands' social performance, or asks what is working for a competitor.
---

# Competitor content audit

Benchmarks 1-5 competitor accounts and outputs a comparison report with concrete content recommendations.

## Inputs

- **Competitors**: handles or profile URLs, per platform. Up to 5 brands per run.
- **Own brand** (optional): the user's handles, to benchmark against.
- **Platforms**: default Instagram + TikTok + YouTube; add X if the brands are active there.
- **Depth**: posts per account (default Instagram 60, TikTok 12, YouTube 30, X 60).

## Credit estimate (per brand)

| Platform | Calls | Credits |
| --- | --- | ---: |
| Instagram | `instagram.photos` (limit 60) + `instagram.reels` (limit 30) | 4 |
| TikTok | `tiktok.posts` + `tiktok.video` on the top 3 by plays | 4 |
| YouTube | `youtube.videos` (limit 30) + `youtube.video` on the top 3 | 4 |
| X | `x.posts` (limit 60) | 2 |

About 12-14 credits per brand on three or four platforms; 3 competitors plus own brand is roughly 50 credits. Confirm with the user before running. Use `"cache_days": 7`.

## How to call the API

Use the `scrapeeverything-api` skill if installed (MCP tools such as `instagram_photos`, the `scrapeeverything` CLI, or `node <skills-dir>/scrapeeverything-api/scripts/se.mjs`). Otherwise `POST https://api.scrapeeverything.com/v1/<platform>/<action>` with `Authorization: Bearer $SCRAPEEVERYTHING_API_KEY` and a JSON body. Save each response as `{brand}_{endpoint}.json`.

## Method

1. Run the profile + list endpoints for every brand and platform. Note followers for normalisation.
2. **Per brand, per platform compute** (the scrapeeverything-api skill's `post-metrics.mjs` does most of this):
   - Posts per week and median gap; weekday distribution (`taken_at`, `published_text`, `created_at`).
   - Format mix: Instagram `posts[].type` (photo / video / album) plus reels count; YouTube shorts vs long-form from `duration_seconds` (<= 60 s is a short); X original vs reply vs repost vs media posts.
   - Median engagement rate and median views, so brands of different size compare fairly.
   - Top 5 posts by interactions (or views). For TikTok, enrich the top 3 by `play_count` with `tiktok.video` for likes/shares/saves; for YouTube use `youtube.video` for exact views and likes.
3. **Qualitative pass on the top posts** (captions, titles, descriptions):
   - Theme buckets (product, education, behind the scenes, UGC, memes/trends, promos, community).
   - Hook pattern of the first line or title (question, number, bold claim, "POV", tutorial).
   - CTA used (link in bio, comment keyword, discount code, none).
   - Hashtag usage: count and the recurring ones.
4. **Compare**: rank brands on cadence, ER and views; show which formats over-index for each (format median vs brand median).
5. **Gaps and recommendations**: themes or formats competitors win with that the own brand does not use, best posting days, 5 concrete post ideas modelled on the top posts (adapted, not copied).

## Output template

```markdown
# Competitor content audit: {brands}
_Date: {YYYY-MM-DD} · Platforms: {list} · Window: last {n} posts · Credits used: {n}_

## Key takeaways
1. ...
2. ...
3. ...

## Benchmark
| Brand | Platform | Followers | Posts/week | Median ER | Median views | Top format |
| --- | --- | ---: | ---: | ---: | ---: | --- |

## Format mix
| Brand | Platform | Reels/Video | Photo | Carousel | Shorts | Long-form | Text |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |

## Top posts
### {Brand}
| # | Post | Date | Format | Interactions | Views | Theme | Hook |
| --- | --- | --- | --- | ---: | ---: | --- | --- |

## Themes and hooks that work
- {theme}: {evidence across brands}

## Cadence
- {brand}: {n}/week, best days {days}, longest gap {n} days

## Gaps and opportunities for {own brand}
- ...

## 5 post ideas
1. {format} · {hook} · {why, referencing which competitor post}

_Method: public data via Scrape Everything ({endpoints}). Counts as of the scrape date._
```

## Guardrails

- Public brand accounts only; this is market research, not monitoring of individuals.
- Recommend adapting what works, never copying competitors' creative, captions or assets.
- Say when counts are missing (hidden likes, `null` counts) instead of guessing.
- Respect the agreed credit budget and plan rate limits; do not loop over every single post with detail calls.
