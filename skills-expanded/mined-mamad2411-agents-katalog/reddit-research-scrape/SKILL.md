---
name: reddit-research-scrape
version: 3.0.0
description: |
  Scrape state — runs the Reddit JSON API scraper for correct data (upvotes,
  comment counts, full comment trees, exact selftext), then generates a viral
  video script per post from the post content + top comments via the backend
  API. Saves structured markdown files + index.json.

allowed-tools:
  - Bash
  - Read
  - Write
  - ChromeDevTools
---

# Reddit Research — Scrape State (v3)

Scrapes top posts from a subreddit with **correct** upvotes/comment counts using Reddit's JSON API, then generates a viral video script per post.

## Before running

Ensure the Flask backend is running on port 8080 (for script generation): `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/models`

## Run

```bash
node "$CLAUDE_SKILL_ROOT/scripts/scrape.js" <subreddit> [limit] [sort] [lang] [--session <id>] [--data-root <path>]
# fallback: node ./skills/reddit-research/scripts/scrape.js <subreddit> ...
```

Defaults: `limit=10`, `sort=hot`, `lang=es` (Spanish).

## What the script does

1. Fetches the subreddit listing JSON: `https://www.reddit.com/r/<sub>/<sort>.json?limit=<n>`
2. For each post, fetches `<permalink>.json` for **correct data**:
   - Accurate upvotes (not the HTML bug showing `1`)
   - Accurate comment counts, full comment trees with correct scores
   - Exact `selftext`, video URL (`media.reddit_video.fallback_url`), linked URL
3. Extracts the top 10 comments (depth ≤ 2)
4. Generates a **viral video script** via the backend API (title + content + top comments), ~30-60s
5. Writes `.reddit-research/<YYYY-MM-DD_HHMMSS>/<post-slug>.md` (dated session) with:
   - `# Title`, author, upvotes, comments, source, scraped date
   - `## Content`, `## Viral Video Script (Spanish)`, `## Videos`, `## Sourced Videos` (placeholder), `## Top Comments`
6. Writes `index.json` (`posts[]` with index/title/file/url/upvotes/comments)

## Manual fallback (Chrome DevTools CLI)

If the JSON API is blocked, scrape the listing page manually:

1. `chrome-devtools navigate_page --url "https://www.reddit.com/r/<subreddit>/<sort>/"` — scroll to load more posts
2. Extract post URLs from `a[href*="/comments/"]`
3. Fetch each post's data via `fetch("<post_url>.json")` in `evaluate_script`
4. Write the same markdown + index.json structure

## Key points

| Issue | HTML scrape | JSON API |
|-------|-------------|----------|
| Upvotes | Often `1` | Correct count |
| Comment count | Missing | Correct count |
| Comments | Author/score missing | All fields present |

## Errors

If a post's JSON API errors (deleted/private/NSFW), log it, skip to the next post, and note the failure in `index.json`.
