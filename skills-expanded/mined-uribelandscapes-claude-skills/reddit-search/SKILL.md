---
name: reddit-search
description: Finds Reddit discussions via Brave Search (titles, links, subreddits, snippets; not full comment threads). Use when the user wants Reddit opinions or experiences, or when normal web search lacks Reddit results.
allowed-tools: Bash(python3 ~/.claude/skills/reddit-search/scripts/search.py *)
---

# reddit-search

Searches Reddit through the Brave Search API only. No Reddit API, no scraping.

## Usage

```
python3 ~/.claude/skills/reddit-search/scripts/search.py "best mechanical keyboard"
python3 ~/.claude/skills/reddit-search/scripts/search.py "rust vs go" 15 en us --freshness pm
python3 ~/.claude/skills/reddit-search/scripts/search.py "query" --json
```

Args: `"<query>" [count 1-20, default 10] [lang, default en] [country, default us] [--freshness pd|pw|pm|py] [--json]`.
Output per result: Title, Link, Subreddit, Age, Snippet.

## One-time setup

1. Create a Brave Search API account. A card is required even for the free $5 credit (about 1,000 requests per month).
2. Store the key in the macOS Keychain (it prompts, so the key never enters shell history):
   `security add-generic-password -s brave-search -a api-key -w`
   Alternative: export `BRAVE_SEARCH_API_KEY`.

## Monthly cap

Overage is billed to the card, so the script counts requests in `~/.cache/reddit-search/usage-YYYY-MM.json` and refuses at 900 per month. Change with `BRAVE_MONTHLY_CAP=<number>`. A corrupt counter file blocks searching until fixed.

## Limits

- Snippets only. Reddit pages cannot be fetched: Reddit blocks automated fetching, and its verification must not be bypassed.
- Tell the user to open the links for full threads and comments.
