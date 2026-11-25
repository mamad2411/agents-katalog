---
name: social-fetch
description: "Use when the user supplies a social post URL to read or another task needs its content. Applies to X, LinkedIn, Instagram, TikTok, Bluesky, Reddit, Mastodon, Threads, and Hacker News. Skip video hosts such as YouTube, Loom, and Vimeo; use reddit for signed-in Reddit tasks."
metadata:
  version: 0.1.1
  source: coreyhaines31/makerskills
---

# social-fetch

Pull a social post by URL. Detect the platform, try the strategy chain
in `references/strategies.md`, and return the same JSON shape every
time. See `references/output-schema.md` for the full spec.

Adapted from Corey Haines's Maker Skills `social-fetch`
(https://github.com/coreyhaines31/makerskills). License notice:
`references/attribution.md`.

Do not use this skill for YouTube, Loom, Vimeo, or other video hosts.
Those need a transcript or watch workflow, not a social-post fetch.

For Reddit *actions* on the shared signed-in Chrome (inbox, vote,
comment), use the `reddit` machine skill. This skill only fetches
structured data from a URL.

## 1. Detect platform

| URL pattern | Platform |
|---|---|
| `x.com/*/status/*` or `twitter.com/*/status/*` | x |
| `linkedin.com/posts/*` or `linkedin.com/feed/update/urn:li:activity:*` | linkedin |
| `linkedin.com/in/*` (profile, recent activity) | linkedin-profile |
| `instagram.com/p/*` or `instagram.com/reel/*` | instagram |
| `tiktok.com/@*/video/*` | tiktok |
| `bsky.app/profile/*/post/*` | bluesky |
| `reddit.com/r/*/comments/*` | reddit |
| `https://<instance>/@<user>/<id>` (Mastodon) | mastodon |
| `threads.net/@*/post/*` | threads |
| `news.ycombinator.com/item?id=` | hn |

If the URL matches none of these, inspect its public destination to identify
the platform. Ask only if the destination remains ambiguous or inaccessible.

## 2. Pick the strategy chain

Read `references/strategies.md`. Each platform has a free-first chain.

- Bluesky, Mastodon, HN, and Reddit have public APIs. Use those.
- X, LinkedIn, Instagram, TikTok, and Threads need a preview, archive,
  or paid fallback for full data.
- Paid strategies (ScrapeCreators, Apify) run only when the env key is
  set and the user has authorized that paid service for this task. Ask before
  an unapproved paid fallback; do not repeat an approval already given.
  See `references/auth-keys.md`.

Prefer a direct fetch over a headed browser. When a login wall requires
a rendered preview, use Codex's built-in computer use and browser tools.

## 3. Execute

For each strategy in order:

1. Try it.
2. On success, parse, normalize, return.
3. On failure (404, 402, auth wall, empty body), record why and try
   the next one.

After the chain is exhausted, say which strategies ran, why each
failed, and what would unlock the next step (usually
`$SCRAPECREATORS_API_KEY` or `$APIFY_API_TOKEN`).

## 4. Normalize

Return this shape on every platform. Fields with no equivalent are
`null`, not `0`. Missing is not zero.

```json
{
  "platform": "x",
  "url": "https://x.com/example/status/1234567890",
  "fetched_at": "2026-08-17T00:00:00Z",
  "raw_source": "fxtwitter",
  "author": {
    "handle": "@example",
    "name": "Example",
    "verified": true
  },
  "posted_at": "2026-08-16T16:32:04Z",
  "text": "...",
  "media": [],
  "engagement": {
    "likes": 0,
    "reposts": 0,
    "replies": 0,
    "bookmarks": 0,
    "views": 0
  },
  "is_thread": false,
  "thread": [],
  "replies": []
}
```

## 5. Optional flags

| Flag | Behavior |
|---|---|
| `--with-replies` | Top-level replies, one hop. Extra quota on paid paths. |
| `--thread` | Same-author thread, when the platform exposes it. |
| `--raw` | Include the raw API or scrape payload. |
| `--media` | Download images/videos to `~/Documents/social-fetches/<platform>-<id>/`. |
| `--save` | Write JSON to `~/Documents/social-fetches/<platform>-<id>.json`. |
| `--no-cache` | Skip the 24h cache. |

Default: the post itself. No replies, no media download (URLs only).

## 6. Cache

If `~/Documents/social-fetches/_cache/` exists, cache successes as
`<platform>-<id>.json` for 24 hours.

Skip cache on `--no-cache`, `--with-replies`, and `--thread`.

## Limits

- **X:** free strategies often return text, author, and basic
  engagement. Full thread + replies need a paid key.
- **LinkedIn:** a browser can see profile recent-activity after
  dismissing the signup modal. Specific `linkedin.com/posts/...` URLs
  usually need paid fallback.
- **Instagram / TikTok / Threads:** anti-bot is heavy. Paid fallback
  is the reliable path.
- **Bluesky / Mastodon / HN / Reddit:** free and reliable.
- **Private or deleted:** stop. Wayback is the only extra try for
  deleted public posts.

If the same paid-gated platform fails three times in one session, ask
once whether to set up a key. Do not nag.

## What to return

1. One line: `<platform> · <handle> · <posted_at> · "<short text>"`
2. The JSON, or the `--save` path if that flag was set.
3. If the result is partial, say so and name the key that would fill
   the gaps.
