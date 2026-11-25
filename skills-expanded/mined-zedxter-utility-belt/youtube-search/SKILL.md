---
name: youtube-search
description: Search YouTube without an API key and get results with publish date, view count, duration, channel and URL, sortable and filterable by date, views, duration and channel. Use when the user asks to find YouTube videos on a topic, the newest or most-watched videos about something, a talk/tutorial/interview/review on YouTube, videos from a particular channel, or needs a video to transcribe or summarise but has no link yet ("найди на YouTube"). Not for a video the user already linked (youtube-transcript for what is said, youtube-audio for the sound), podcasts (podcast-search) or general web search (web-search).
license: MIT
compatibility: Python 3.12+ with uv (preferred) or pip; macOS, Linux, Windows. Needs network access to youtube.com. Works from most IPs; the optional --details mode is blocked on cloud/datacenter IPs.
metadata:
  author: zedxter
  version: "1.1.0"
  source: https://github.com/zedxter/utility-belt
---

# YouTube Search

Find videos on YouTube from the command line, free and key-less, with the data
you need to judge them: **publish date, view count, duration**, channel and URL.
The script uses `yt-dlp` as a library to call YouTube's own search endpoint.

## When to use

- "Find a video about…", "what are the best/most popular videos on…"
- "Latest videos about…", "anything new this week on…"
- "Is there a talk/tutorial/review of X on YouTube?"
- "Find <channel>'s video about Y"
- The user wants a summary or transcript of a video but has not given a link —
  search first, then hand the chosen URL to the `youtube-transcript` skill.

Not for: video comments, channel statistics, downloading media, or anything
requiring a signed-in account.

## Quick start

The script is `scripts/search.py` relative to this skill. Run with `uv`
(cross-platform; installs `yt-dlp` into a cached environment automatically):

```bash
uv run scripts/search.py python asyncio tutorial
uv run scripts/search.py "LLM agents" --sort date --period month -n 15
uv run scripts/search.py rust borrow checker --sort views --duration long
uv run scripts/search.py asyncio --channel @TechWithTim
```

Without `uv`: `pip install yt-dlp`, then `python scripts/search.py …`.

Default output is a readable list (10 results):

```
 1. Asyncio in Python - Full Tutorial
    https://www.youtube.com/watch?v=Qb9s3UiMSTA  |  Tech With Tim · 24:59 · 393K views · ~2024
```

`~` before a date means approximate: YouTube only shows "1 year ago", and the
date is printed with the same granularity as that text — `~2024` for "N years
ago", `~2026-08` for "N months ago", `~2026-10-20` for "N weeks/days ago",
today's date for "N hours/minutes ago". `--details` replaces it with the exact
upload date (`2024-10-29`, no `~`).

## Options

| Flag | Meaning |
|------|---------|
| `-n, --limit N` | Number of results (default 10, max 100). |
| `--sort relevance\|date\|views\|rating` | Order. `date` = newest first (sorted locally over a larger fetch, see notes). |
| `--period hour\|today\|week\|month\|year` | Only videos uploaded within that window (server-side). |
| `--duration short\|medium\|long` | <4 min / 4–20 min / >20 min (server-side). |
| `--min-minutes F`, `--max-minutes F` | Exact duration bounds (client-side). |
| `--min-views N` | Drop results with fewer views. |
| `--after YYYY-MM-DD` | Drop results published before that date. |
| `--type video\|channel\|playlist\|movie` | Result type (default: videos only). |
| `--channel @handle\|URL\|UC…` | Search within one channel. |
| `--details` | One extra request per result: exact upload date, likes, description, available caption languages (manual and auto). |
| `-f table\|json\|urls\|ids` | Output format. `json` carries every field (shape below); `urls`/`ids` are for piping into other tools. |
| `--proxy URL` | HTTP(S)/SOCKS proxy if YouTube blocks the IP. |

## JSON output

`-f json` prints one object, not a bare list:

```json
{
  "query": "python asyncio tutorial",
  "results": [
    {
      "kind": "video",
      "id": "Qb9s3UiMSTA",
      "url": "https://www.youtube.com/watch?v=Qb9s3UiMSTA",
      "title": "Asyncio in Python - Full Tutorial",
      "channel": "Tech With Tim",
      "channel_url": "https://www.youtube.com/@TechWithTim",
      "duration": 1499,
      "view_count": 393000,
      "published": "2024",
      "published_exact": false,
      "published_precision": "year",
      "live": false
    }
  ]
}
```

Top-level keys: `query` (string, the search terms as sent) and `results`
(array, in output order). Each result has exactly these keys:

| Key | Type | Meaning |
|-----|------|---------|
| `kind` | `"video"\|"channel"\|"playlist"` | Non-video results only appear with `--type` or `--channel`. |
| `id`, `url`, `title`, `channel` | string | `channel` may be `""`. |
| `channel_url` | string \| null | |
| `duration` | number \| null | Seconds; `null` for live streams. |
| `view_count` | number \| null | |
| `published` | string \| null | `YYYY`, `YYYY-MM` or `YYYY-MM-DD` — never more precise than YouTube's relative date (see `published_precision`). No `~` here; that is table decoration. |
| `published_exact` | boolean | `true` only with `--details`, when the real upload date was fetched. |
| `published_precision` | `"year"\|"month"\|"day"\|null` | Granularity of `published`; `null` when no date is known. |
| `live` | boolean | Live or upcoming stream. |

With `--details` a video result additionally gets `like_count`,
`comment_count`, `channel_follower_count`, `categories`, `tags`, `chapters`
(each only when YouTube returned it), `description` (first 1500 chars),
`captions_manual` and `captions_auto` (lists of language codes), or
`details_error` (string) if that video's extra request failed.

## How to pick and present results

Always weigh the three numbers the script gives you — do not just take the
first hit:

- **Date.** For fast-moving topics (software versions, AI, news, prices) prefer
  recent uploads: add `--period year` or `--sort date --period month`. For
  timeless topics (maths, history, classic talks) age does not matter; say so.
  **Caution with `--period` (and `--sort date`) on broad queries:** YouTube
  relaxes relevance when a date filter is on, so a long query such as
  `smartphone zombies society addiction --sort date --period year` returns
  unrelated uploads (gaming VODs, news clips). With `--period` use short,
  precise queries — 2–3 words or a quoted phrase — and add `--min-views`. If
  the results still look unrelated, drop `--period`, search without it and
  filter locally with `--after YYYY-MM-DD`.
- **Views.** A proxy for quality and relevance, but biased toward old and
  clickbait videos. Use `--min-views` to cut noise (e.g. 10 000 for mainstream
  topics, 1 000 for niche ones), not as the sole ranking.
- **Duration.** Match the user's need: `--duration short` for a quick answer or
  demo, `long` for a full course/talk/interview. Mention the length when
  recommending, so the user knows what they are committing to. Tip:
  `--min-minutes 4` (or `--duration medium`) removes the kids' songs and music
  clips that flood queries like "phone zombies".
- **Channel.** Recognisable official or expert channels beat anonymous
  re-uploads with the same title. The `--channel` flag is the fastest way to
  find one creator's video on a subject.

When presenting, give for each recommended video: title, channel, duration,
views, date and the URL — one line per video, in the user's language. Say which
one you would start with and why (newest, most watched, most relevant length).
If the user asks for "the best" video, show 3–5 candidates with those numbers
rather than one.

Use `-f json` when you need to post-process; use `-f urls -n 1` to pipe straight
into the transcript skill.

**Before recommending or transcribing, run `--details` on your shortlist (≤5
videos).** It is the only way to get the exact upload date (the plain search
only shows `~2024`) and to see whether captions exist at all: its
`captions_manual`/`captions_auto` fields tell you whether `youtube-transcript`
will succeed before you call it. Keep it to a shortlist — it costs one extra
request per video and is blocked on cloud IPs (the result then carries a
`details_error` and keeps its approximate date).

## Chaining with youtube-transcript

Typical flow for "summarise the latest talk on X":

1. `uv run scripts/search.py X talk --sort date --period year -n 5`
2. Re-run the 2–3 best candidates with `--details` to get exact dates and
   caption availability, pick one (or ask the user if several are plausible),
   then run the `youtube-transcript` skill's script on its URL.
3. Summarise from the transcript, citing the video's title, channel and date.

## Errors and exit codes

| Exit | Meaning | What to do |
|------|---------|------------|
| 1 | No results after filters | Loosen `--min-views`, `--after`, `--period`, or broaden the query. |
| 2 | Bad input (empty query, unparsable channel) or `yt-dlp` missing | Fix the argument; or `pip install yt-dlp` / use `uv run`. |
| 4 | Blocked by YouTube (bot check, 429) | Rare for plain search; common for `--details` on cloud IPs. Retry without `--details`, wait a minute, or pass `--proxy`. Don't retry in a tight loop. |
| 6 | Network failure | Check connectivity, retry. |
| 7 | Other yt-dlp error, or an unexpected error in the script (the message says `unexpected`) | Usually a YouTube-side change; `uv` fetches the newest `yt-dlp` on a fresh cache, otherwise `pip install -U yt-dlp`. Report an `unexpected` error with the command line. |
| 130 | Interrupted | — |

With `--details`, a per-video failure does not abort: the result keeps its
basic fields and gains a `details_error` line.

## Notes and limitations

- YouTube's search endpoint ignores sort-by-date, so `--sort date` fetches up
  to 3× `-n` (min 30) results and sorts them locally. Combine with `--period`
  to make "newest" meaningful; without it you get the newest among the most
  relevant, not the newest overall.
- Dates without `--details` are approximate and printed only as precisely as
  YouTube's relative text allows: "8 years ago" → `~2018`, "3 months ago" →
  `~2026-07`, "3 weeks ago" → `~2026-10-07` (±a few days). `--after` compares
  against YouTube's estimate, so it is equally fuzzy for old videos.
- A date filter (`--period`) loosens YouTube's relevance ranking; see the
  caution under "How to pick and present results".
- Live streams and premieres show `LIVE` instead of a duration and may lack a
  view count.
- Results depend on YouTube's region/language heuristics for the requesting IP.
