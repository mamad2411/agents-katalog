---
name: twitter-research-scrape
version: 3.0.0
description: |
  Scrape state — runs the Twitter/X topic scraper via Chrome DevTools
  Protocol. Searches X by topic, collects 10+ posts across many accounts,
  extracts engagement metrics (likes, retweets, replies, views), ranks them.
  Optionally augments with seed account profiles. No API key needed.

allowed-tools:
  - Bash
  - Read
  - Write
  - ChromeDevTools
---

# Twitter/X Research — Scrape State (v3)

Scrapes topic posts from X/Twitter. Requires Chrome running with `--remote-debugging-port=9222` and user logged into X.

## Before running

Ensure:
1. Chrome is open with `--remote-debugging-port=9222` flag
2. X/Twitter is logged in (tab stays open)
3. Config exists at `.twitter-research/<timestamp>/config.json` (from setup)

## Run

```bash
node "$CLAUDE_SKILL_ROOT/scripts/scrape.js" <timestamp> [--data-root <path>]
# fallback: node ./skills/twitter-research/scripts/scrape.js <timestamp>
```

**Important**: Keep the X tab in the foreground (visible, not minimized) while this runs. Chrome throttles background tabs.

## What the script does

1. Searches X by topic (`Top` tab, then `Latest` if needed) using `config.topic` + `config.topicKeywords`
2. Scrolls to load many posts from **different accounts**
3. Extracts per post: handle, author, text, timestamp, URL, likes/retweets/replies, media
4. Visits seed accounts (`config.accounts` with `isSeed: true`) and keeps only topic-relevant tweets
5. Deduplicates by URL, ranks by engagement, keeps top `minPosts` (min 10)
6. Saves `raw-posts.json` with `posts[]`, `distinctAccounts`, `accountsSummary`

## Manual fallback (Chrome DevTools CLI)

If the script hits an X login wall or returns too few results, do it manually:

1. Navigate: `chrome-devtools navigate_page --url "https://x.com/search?q=<topic>&src=typed_query&f=top"`
2. Scroll: `chrome-devtools evaluate_script --function "async () => { for (let i=0;i<12;i++){ window.scrollTo(0, document.body.scrollHeight); await new Promise(r=>setTimeout(r,1800)); } return 'ok'; }"`
3. Extract tweets using `[data-testid="tweet"]` selectors (`tweetText`, `User-Name`, `reply`/`retweet`/`like` aria-labels)
4. Merge results into `raw-posts.json` with the same schema

## Output

```
.twitter-research/<timestamp>/
├── raw-posts.json        # Ranked posts with engagement metrics
└── screenshots/          # Optional screenshots
```
