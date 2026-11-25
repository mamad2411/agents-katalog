---
name: influencer-vetting
description: Vet a creator or influencer before a sponsorship, collab or ambassador deal. Pulls their public Instagram, TikTok, YouTube and X profiles and recent posts via the Scrape Everything API, computes engagement rate, views-to-followers, posting cadence and consistency, flags red flags (inflated followers, engagement spikes, brand-safety issues, competitor sponsorships) and scores audience fit against a brief. Use when the user says things like "vet @handle", "is this influencer legit", "check this creator before we sponsor them", "engagement rate of", or pastes creator profile links with a campaign in mind.
---

# Influencer vetting

Produces a one-page go / no-go vetting report for one creator across the platforms they are active on.

## Inputs

Ask only for what is missing:
- **Creator**: one handle or profile URL per platform (e.g. `@nasa` on Instagram, a TikTok or YouTube link). If only one handle is given, try the same handle on the other platforms and confirm matches by name/bio/link-in-bio before using them.
- **Brief** (optional but makes the fit score real): product/category, target audience (age band, region, language), campaign format (reel, video integration, story), competitor brands to watch for.
- **Depth**: `quick` (one platform) or `full` (all platforms found). Default `full`.

## Credit estimate

| Platform | Calls | Credits |
| --- | --- | ---: |
| Instagram | `instagram.photos` (limit 30) + `instagram.reels` (limit 12) + `instagram.comments` on 2 top posts | 2 + 2 + 2 = 6 |
| TikTok | `tiktok.profile` + `tiktok.posts` + `tiktok.video` on 3 posts | 1 + 1 + 3 = 5 |
| YouTube | `youtube.profile` + `youtube.videos` (limit 15) + `youtube.video` on 2 recent | 1 + 1 + 2 = 4 |
| X | `x.posts` (limit 40) | 2 |

Quick vet: about 6 credits. Full vet on four platforms: about 17 credits. Use `"cache_days": 7` unless the user needs today's numbers.

## How to call the API

Use the `scrapeeverything-api` skill if installed (MCP tool such as `instagram_photos`, the `scrapeeverything` CLI, or `node <skills-dir>/scrapeeverything-api/scripts/se.mjs instagram.photos username=nasa limit=30 --out ig.json`). Otherwise:

```bash
curl -sS https://api.scrapeeverything.com/v1/instagram/photos -H "Authorization: Bearer $SCRAPEEVERYTHING_API_KEY" \
  -H "Content-Type: application/json" -d '{"username":"nasa","limit":30,"cache_days":7}' > ig.json
```

Save every response to a file; compute everything from the saved files.

## Method

1. **Resolve accounts.** Call the cheapest profile endpoint per platform (`instagram.profile` is unnecessary because `instagram.photos` includes it). If a profile is private, age-restricted or not found, note it and skip that platform.
2. **Instagram.** From `instagram.photos` read `follower_count`, `following_count`, `post_count`, `is_verified`, `category_name`, `biography`, `external_url` and `posts[]` (`like_count`, `comment_count`, `type`, `caption`, `taken_at`). From `instagram.reels` read `reels[].view_count`. Ignore posts where `like_and_view_counts_disabled` is true.
3. **TikTok.** `tiktok.profile` gives `follower_count`, `like_count`, `video_count`, `region`. `tiktok.posts` gives the newest 12 videos with `play_count` only. Call `tiktok.video` on the 3 most recent non-pinned videos for `like_count`, `comment_count`, `share_count`, `save_count`.
4. **YouTube.** `youtube.profile` (`subscriber_count` is rounded) and `youtube.videos` (rounded views, relative dates). Call `youtube.video` on the 2 latest long-form uploads for exact `view_count`, `like_count` and `published_at`.
5. **X.** `x.posts`: drop retweets (`is_retweet`) and replies (`is_reply`) before computing rates.
6. **Compute metrics** per platform (or run `node post-metrics.mjs <file> --markdown` from the scrapeeverything-api skill):
   - Engagement rate per post = (likes + comments [+ shares]) / followers x 100. Report the **median**, not the mean (one viral post skews the mean).
   - Views-to-followers = median views / followers x 100 (reels, TikTok, YouTube).
   - Cadence = posts per week over the window and the longest gap.
   - Consistency = coefficient of variation of engagement (std / mean). Above 1.5 means hit-driven.
7. **Red flags** (each with evidence):
   - Median ER far below the rough norms for the size tier: Instagram roughly 1-3% (lower for 1M+ accounts), TikTok likes/plays roughly 3-10%, YouTube likes/views roughly 2-5%. These are heuristics, not standards; say so.
   - High follower count with very low views-to-followers (under 3% on reels/TikTok) suggests inactive or bought followers.
   - Following count close to or above follower count on a large account.
   - Sudden follower or ER jumps with no viral post to explain them.
   - Comments on top posts that are mostly emojis, generic praise or off-topic (sample from `instagram.comments`; summarise, do not list commenters).
   - Brand safety: scan bio, captions and transcripts for profanity, controversial topics, gambling/adult content, misinformation.
   - Competitors: captions with `#ad`, `#sponsored`, "paid partnership", "use my code", or competitor brand names from the brief, plus how recent they are.
8. **Audience-fit checklist** against the brief: content topics match the category; language of captions and comments matches the target; `region` (TikTok) or location signals match; format strength (do their reels/videos outperform their photos?); posting frequency supports the campaign timeline; past sponsored posts performed at least as well as organic ones. Mark each item Pass / Watch / Fail.
9. **Verdict.** Go / Go with conditions / No-go, with the 3 reasons that matter most and suggested deliverables (format and platform where they over-index).

## Output template

```markdown
# Influencer vetting: {name} ({primary handle})
_Date: {YYYY-MM-DD} · Platforms: {list} · Credits used: {n}_

## Verdict: {Go | Go with conditions | No-go}
- {reason 1}
- {reason 2}
- {reason 3}

## Snapshot
| Platform | Handle | Followers | Median ER | Median views | Views/followers | Posts/week | Verified |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Instagram | @... | ... | ...% | ... | ...% | ... | yes/no |

## Content and performance
- Best format: {reels vs photos vs carousels, with numbers}
- Top 3 posts: {link, date, interactions, why it worked}
- Consistency: {CV and what it means}

## Red flags
| Flag | Evidence | Severity |
| --- | --- | --- |

## Audience fit ({brief summary})
| Check | Result | Note |
| --- | --- | --- |
| Topic match | Pass/Watch/Fail | ... |
| Language | ... | ... |
| Region | ... | ... |
| Format strength | ... | ... |
| Cadence vs timeline | ... | ... |
| Sponsored vs organic performance | ... | ... |

## Existing partnerships
- {brand, date, link} or "none found in the last {n} posts"

## Recommended deal shape
- Deliverables: {...}
- Watch-outs for the contract: {...}

_Method: public data via Scrape Everything ({endpoints}). Engagement norms are rough heuristics. Data window: {from} to {to}._
```

## Guardrails

- Public data only. If an account is private or age-restricted, report that rather than trying to work around it.
- Assess the creator's public, professional presence. Do not dig into family members, home location or other personal life details.
- Summarise comment quality; do not list or profile individual commenters.
- Present fake-follower signals as indicators, never as accusations.
- Stay within the confirmed credit budget and plan rate limits (3-5 calls in parallel at most).
