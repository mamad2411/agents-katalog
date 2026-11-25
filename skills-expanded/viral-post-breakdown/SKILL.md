---
name: viral-post-breakdown
description: Break down why a specific TikTok, Instagram reel or post, YouTube video or Short, or X post went viral, using the Scrape Everything API. Pulls the post's stats, transcript, sound and top comments plus the creator's recent posts as a baseline, measures how far it outperformed (views and engagement multiple vs the creator's median), and dissects hook, structure, length, audio, caption, CTA and audience reaction into a reusable template. Use when the user shares a post link and asks why it blew up, how to replicate it, what made it work, or for a teardown of a viral video.
---

# Viral post breakdown

One link in, one teardown out: how big the outlier is, why it worked, and a template to reuse.

## Inputs

- **Post URL** (required): full TikTok video URL, Instagram post/reel URL, YouTube watch/shorts URL, or X post URL.
- **User's goal** (optional): "adapt this for our brand", "learn the hook", etc.

## Calls per platform

| Platform | Post | Words | Audience | Baseline | Credits |
| --- | --- | --- | --- | --- | ---: |
| TikTok | `tiktok.video` | `tiktok.transcript` | `tiktok.comments` (limit 50) | `tiktok.posts` (12 newest, plays) | 4 |
| Instagram reel | `instagram.reel` | caption only | `instagram.comments` (15) | `instagram.reels` (limit 30, views) | 4 |
| Instagram photo/carousel | `instagram.post` | caption only | `instagram.comments` | `instagram.photos` (limit 30) | 4 |
| YouTube | `youtube.video` | `youtube.transcript` | `youtube.comments` (top, 20) | `youtube.videos` (limit 30) | 4 |
| X | `x.post` | text | quoted/reply counts | `x.posts` (limit 40) | 3 |

Optional: `tiktok.music` on the video's sound (2 credits) to see how many videos use it. Total: **3-6 credits**.

## How to call the API

Use the `scrapeeverything-api` skill if installed (MCP tools such as `tiktok_video`, `tiktok_transcript`, the `scrapeeverything` CLI, or `node <skills-dir>/scrapeeverything-api/scripts/se.mjs tiktok.video url=<url>`). Otherwise `POST https://api.scrapeeverything.com/v1/<platform>/<action>` with `Authorization: Bearer $SCRAPEEVERYTHING_API_KEY`. Short share links (vm.tiktok.com) are not supported: ask for the full URL.

## Method

1. **Detect the platform** from the URL and fetch the post. Record views/plays, likes, comments, shares, saves, duration, publish time, caption/title, sound (`music` on TikTok, `audio` on reels).
2. **Baseline**: fetch the creator's recent posts and compute the median views (and median likes where available), excluding the viral post itself.
   - Outperformance multiple = post views / baseline median views. Over 5x is a clear outlier; 2-5x is strong; under 2x means it is the creator's normal reach, so the "why" is the account, not the post.
   - Engagement profile: like rate (likes / views), comment rate, share rate, save rate. High shares = people forward it; high saves = utility; high comments = debate or a question in the post.
3. **Words**: get the transcript (TikTok/YouTube). The **hook** is roughly the first 3 seconds (segments with `start` < 3) for short-form, the first 30 seconds for long-form. Note on-screen promise, pattern interrupt, question, or bold claim.
4. **Structure**: map the beats with timestamps (hook, setup, payoff, loop/CTA). Note length vs platform norm and whether the end loops into the start.
5. **Audio**: original vs trending sound; if trending, optionally `tiktok.music` for `video_count`.
6. **Caption and CTA**: length, keywords, hashtags, question prompts, "comment X" mechanics.
7. **Audience reaction**: cluster the comments into 3-5 themes (what they quote, argue about, ask). Do not list commenters.
8. **Timing**: day/time posted, and whether it rode a trend or event at the time.
9. **Template**: write a fill-in-the-blanks version (hook line, beats, length, sound choice, CTA), and 3 adapted ideas for the user's goal.

## Output template

```markdown
# Viral breakdown: {platform} post by @{creator}
_Date: {YYYY-MM-DD} · [Post]({url}) · Credits used: {n}_

## The numbers
| Metric | This post | Creator median | Multiple |
| --- | ---: | ---: | ---: |
| Views | ... | ... | {x}x |
| Likes | ... | ... | ... |
| Comments | ... | ... | ... |
| Shares / saves | ... | ... | ... |
Like rate {..}% · Share rate {..}% · Save rate {..}% · Length {s}s · Posted {day, time UTC}

## Why it worked (ranked)
1. **Hook**: "{first line}" ({mm:ss}). {why it stops the scroll}
2. **{factor}**: {evidence}
3. **{factor}**: {evidence}

## Beat map
| Time | Beat | What happens |
| --- | --- | --- |
| 0:00-0:03 | Hook | ... |

## Audio, caption, CTA
- Sound: {original/trending, uses}
- Caption: {...}
- CTA: {...}

## What the comments say
- {theme}: {share}

## Reusable template
- Hook: "{pattern with blanks}"
- Beats: ...
- Length: ...
- Sound: ...
- CTA: ...

## 3 ideas for {user's brand/goal}
1. ...
```

## Guardrails

- Public posts only. If the post is private or age-restricted, stop and say so.
- Adapt the format and mechanics; never recommend re-uploading or copying someone else's content, audio rights aside.
- Comment analysis is aggregate; no commenter names.
- Correlation is not causation: label each "why" with the evidence behind it.
