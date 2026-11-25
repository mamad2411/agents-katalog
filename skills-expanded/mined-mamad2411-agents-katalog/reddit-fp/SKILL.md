---
name: reddit-fp
description: |
  Find Reddit posts with pain points matching your product. Searches tier 1/2 subreddits
  using keywords, classifies by pain category, maps to product solutions.
  Part of reddit-intel. Requires .reddit-intel.json (run /reddit-intel-init first).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__exa__web_search_exa
metadata:
  trigger: When user wants to find Reddit posts, search for pain-point posts, or mentions reddit-fp
---

# reddit-fp — Find Posts

Search target communities for posts containing pain points relevant to your product.

## Tool Rules

- **DO NOT** use built-in WebSearch for Reddit (blocked by Anthropic's crawler)
- **MUST** use `mcp__exa__web_search_exa` (type="deep") for all Reddit searches
- Max 3 query attempts per search intent; skip if no results
- Target: keep total tool calls under 30

## Config

Reads `.reddit-intel.json` from project root. If not found, tell user to run `/reddit-intel-init`.

## Schema: posts.jsonl (unique key: `url`)

```json
{"url": "https://www.reddit.com/...", "title": "...", "subreddit": "r/ClaudeAI", "upvotes": 85, "comments": 47, "post_date": "2025-06-01", "pain_category": "context_loss", "product_solution": "Auto-inject context on each session", "status": "active", "added": "2026-02-06"}
```

status values: `active` | `archived`

## Arguments

The user may pass a topic/keyword as argument (e.g., `/reddit-fp context loss`). If provided, focus the search on that specific topic. If no argument, search across all keywords.

## Flow

1. Read `{data_dir}/posts.jsonl` for existing post URLs (dedup set)
2. Read `{data_dir}/keywords.jsonl` for search terms
3. Read `{data_dir}/subreddits.jsonl` — **only search tier 1 and tier 2**
4. Read `SKILL_DIR/references/step-details.md` Step 3 section for detailed logic
5. For each tier 1/2 subreddit:
   - Select 3-5 most relevant keywords (or use user-provided topic)
   - Query: `"site:reddit.com/r/{subreddit} {keyword}"`
   - Execute with `mcp__exa__web_search_exa` (type="deep")
6. Filter: prefer last 30 days, with engagement (comments > 0)
7. Classify each post's `pain_category` and `product_solution` using pain categories from product-context.md
8. Mark existing posts older than 30 days as `status="archived"`
9. Dedup by `url`, append via:
   ```bash
   python3 SKILL_DIR/scripts/jsonl_ops.py append posts '<json>'
   ```
10. Render: `python3 SKILL_DIR/scripts/jsonl_ops.py render posts`
11. Report: new entries added + current total

Where `SKILL_DIR` is two levels up from this file (the reddit-intel repo root).
