---
name: reddit-ac
description: |
  Analyze Reddit comment sections for competitive intelligence. Extracts competitor mentions,
  real user language (copy material), and unmet needs from active posts.
  Part of reddit-intel. Requires .reddit-intel.json (run /reddit-intel-init first).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__exa__web_search_exa
  - WebFetch
metadata:
  trigger: When user wants to analyze Reddit comments, extract competitive intelligence, or mentions reddit-ac
---

# reddit-ac — Analyze Comments

Analyze comment sections of active posts. Extract competitor info, real user language, and unmet needs.

## Tool Rules

- **DO NOT** use built-in WebSearch for Reddit (blocked by Anthropic's crawler)
- **MUST** use `mcp__exa__web_search_exa` (type="deep") for all Reddit searches
- Use WebFetch for specific non-Reddit URLs
- Max 3 query attempts per search intent; skip if no results
- Target: keep total tool calls under 30

## Config

Reads `.reddit-intel.json` from project root. If not found, tell user to run `/reddit-intel-init`.

## Schema: comments.jsonl (unique key: `post_url` + `content[:50]`)

```json
{"post_url": "https://www.reddit.com/...", "type": "competitor", "content": "I use Cursor when I exceed the token limit", "competitor": "Cursor", "sentiment": "positive", "insight": "Cursor used as fallback", "added": "2026-02-06"}
```

type values: `competitor` | `language` | `need`

## Comment Types

| type | What to extract | Key fields |
|------|----------------|-----------|
| competitor | Mentions of competing/alternative tools | `competitor` + `sentiment` (positive/neutral/negative) |
| language | Real user language, verbatim quotes for copy | `content` (quote) + `insight` (marketing-usable phrasing) |
| need | Unmet needs users express | `content` + `insight` (whether your product can solve it) |

## Flow

1. Read `{data_dir}/posts.jsonl` — only `status=active` posts
2. Read `{data_dir}/comments.jsonl` — find unanalyzed posts (post_url not in existing set)
3. Read `SKILL_DIR/references/step-details.md` Step 4 section for detailed logic
4. For each unanalyzed post:
   - Search with `mcp__exa__web_search_exa` (type="deep") using post title + subreddit
   - Classify valuable comments as: competitor / language / need
5. Dedup by `post_url + content[:50]`, append via:
   ```bash
   python3 SKILL_DIR/scripts/jsonl_ops.py append comments '<json>'
   ```
6. Render: `python3 SKILL_DIR/scripts/jsonl_ops.py render comments`
7. Report: new insights added + current total + posts analyzed

Where `SKILL_DIR` is two levels up from this file (the reddit-intel repo root).
