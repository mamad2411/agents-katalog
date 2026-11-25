---
name: reddit-sub
description: |
  Discover relevant Reddit communities for your product. Finds subreddits where target users
  discuss pain points, rates them by tier (1-4), and tracks promo policies.
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
  trigger: When user wants to find Reddit communities, discover subreddits, or mentions reddit-sub
---

# reddit-sub — Discover Subreddits

Find Reddit communities where your target users live and discuss pain points.

## Tool Rules

- **DO NOT** use built-in WebSearch for Reddit (blocked by Anthropic's crawler)
- **MUST** use `mcp__exa__web_search_exa` (type="deep") for all Reddit searches
- Max 3 query attempts per search intent; skip if no results
- Target: keep total tool calls under 30

## Config

Reads `.reddit-intel.json` from project root. If not found, tell user to run `/reddit-intel-init`.

## Schema: subreddits.jsonl (unique key: `name`)

```json
{"name": "r/ClaudeAI", "tier": 1, "members": "451K", "activity": "high", "promo_policy": "discussion OK", "relevance": "primary", "strategy": "Pain-point replies, technical discussions", "added": "2026-02-06"}
```

tier values: 1 (core) / 2 (high relevance) / 3 (general/niche) / 4 (watching)

## Flow

1. Read `{data_dir}/subreddits.jsonl` for existing communities
2. Read `{data_dir}/keywords.jsonl` for search terms
3. Read `SKILL_DIR/references/step-details.md` Step 2 section for detailed logic
4. Use keywords via `mcp__exa__web_search_exa` (type="deep") to discover new communities:
   - `"site:reddit.com/r/ {keyword}"`
   - Cross-posts and comments in existing posts
5. Evaluate each: members, activity, promo_policy, relevance
6. New communities default to tier=4 (watching)
7. Dedup by `name`, append via:
   ```bash
   python3 SKILL_DIR/scripts/jsonl_ops.py append subreddits '<json>'
   ```
8. Render: `python3 SKILL_DIR/scripts/jsonl_ops.py render subreddits`
9. Report: new entries added + current total

Where `SKILL_DIR` is two levels up from this file (the reddit-intel repo root).
