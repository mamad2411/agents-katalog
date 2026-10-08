---
name: facebook-research-scrape
version: 3.0.0
description: |
  Scrape state — runs the Facebook scraper via Chrome DevTools Protocol.
  Extracts page-level analytics (followers, engagement), top video posts,
  engagement metrics, and hook screenshots. Also scrapes competitor pages,
  computes engagement ratios, and saves a historical snapshot for trend
  comparison across analysis rounds.

allowed-tools:
  - Bash
  - Read
  - Write
  - ChromeDevTools
---

# Facebook Research — Scrape State (v3)

Scrapes a Facebook page and its competitors. Requires Chrome running with `--remote-debugging-port=9222` and Facebook logged in.

## Before running

Ensure:
1. Chrome is open with `--remote-debugging-port=9222` flag
2. Facebook is logged in (tab stays open)
3. Config exists at `.fb-research/projects/<project-name>/config.json` (from setup)

## Run

```bash
# via global skill (Muse ~/.claude/skills/, also read by Opencode):
node "$CLAUDE_SKILL_ROOT/scripts/scrape.js" <project-name> [sessionId] --session $SESSION
# local dev fallback:
node ./skills/facebook-research/scripts/scrape.js <project-name> --session $SESSION
# dataRoot auto-resolved from CWD walk-up; override: --data-root /path/to/.fb-research
```

**Important**: Keep the Facebook tab in the foreground (visible, not minimized) while this runs. Chrome throttles background tabs and screenshots will fail.

## What the script does

1. Navigates to the page (`config.pageUrl`), extracts page stats (followers, likes, category, description)
2. Opens the Videos tab, scrolls to load posts, collects video post URLs + estimated views
3. Visits each top post and extracts: views, likes, comments, shares, caption, og:title
4. Computes engagement ratios + composite score and ranks the top 5
5. Scrapes each competitor (config.competitors) the same way → `competitors/<name>/raw-posts.json`
6. Saves `page-analytics.json`, `raw-posts.json`, and appends a snapshot to `page-analytics-history.json`
7. Computes the trend vs the previous snapshot (up/down/stable per metric)

## Important note on Facebook's DOM

Facebook uses randomized class names. The script always uses `aria-label`, `role`, text
matching, and `[href*="..."]` partial URL selectors — **never hardcode class names**.

## Manual fallback (Chrome DevTools CLI)

If the script gets insufficient data, scrape manually:

1. `chrome-devtools navigate_page --url "https://www.facebook.com/<page_name>/"`
2. Scroll + extract page stats / video links via `evaluate_script`
3. Navigate into each post for metrics + take hook screenshots
4. Save `page-analytics.json` / `raw-posts.json` with the same schema

Or use WebSearch fallback: `websearch "site:facebook.com <page_name> best performing videos 2026"` and note data came from search.

## Output

```
.fb-research/projects/<project-name>/
├── page-analytics-history.json          # Global history (appended each run)
├── latest.json                            # -> <YYYY-MM-DD_HHMMSS>
└── <YYYY-MM-DD_HHMMSS>/                  # This run (dated)
    ├── page-analytics.json                # This run stats + top5
    ├── raw-posts.json                     # Full scanned posts
    └── competitors/<name>/raw-posts.json
# plus legacy copies at project root for back-compat
```

## Next step: `skill facebook-research-analyze`
