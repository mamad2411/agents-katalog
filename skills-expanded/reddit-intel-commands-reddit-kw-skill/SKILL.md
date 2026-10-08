---
name: reddit-kw
description: |
  Expand Reddit marketing keywords. Discovers how users describe pain points in your product domain.
  Searches Reddit via Exa, finds synonyms, long-tail variants, and real user language.
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
  trigger: When user wants to expand Reddit keywords, find pain-point keywords, or mentions reddit-kw
---

# reddit-kw — Expand Keywords

Discover how Reddit users actually describe pain points related to your product domain.

## Tool Rules

- **DO NOT** use built-in WebSearch for Reddit (blocked by Anthropic's crawler)
- **MUST** use `mcp__exa__web_search_exa` (type="deep") for all Reddit searches
- Max 3 query attempts per search intent; skip if no results
- Target: keep total tool calls under 30

## Config

Reads `.reddit-intel.json` from project root. If not found, tell user to run `/reddit-intel-init`.

```json
{
  "data_dir": "./reddit-intel/data",
  "product_name": "MyProduct",
  "product_context": "./reddit-intel/product-context.md",
  "language": "en"
}
```

## Schema: keywords.jsonl (unique key: `keyword`)

```json
{"keyword": "context loss", "category": "pain", "reddit_usage": "AI keeps forgetting my project context", "source": "r/ClaudeAI", "added": "2026-02-06"}
```

category values: `pain` | `tool` | `scenario` | `solution`

## Flow

1. Read `{data_dir}/keywords.jsonl`, group existing keywords by category
2. Read `product-context.md` for product positioning and pain points
3. Read `SKILL_DIR/references/step-details.md` Step 1 section for detailed search strategy
4. For each category, use `mcp__exa__web_search_exa` (type="deep") to search Reddit:
   - pain: `"site:reddit.com {keyword} frustration OR problem OR broken"`
   - tool: `"site:reddit.com {tool_name} alternative OR replacement OR better"`
   - scenario: `"site:reddit.com {scenario} workflow OR setup OR tools"`
   - solution: `"site:reddit.com {concept} implementation OR framework"`
5. Generate associations: synonyms, long-tail variants, Reddit vernacular
6. Dedup by `keyword`, append new entries via:
   ```bash
   python3 SKILL_DIR/scripts/jsonl_ops.py append keywords '<json>'
   ```
7. Render: `python3 SKILL_DIR/scripts/jsonl_ops.py render keywords`
8. Report: new entries added + current total

Where `SKILL_DIR` is two levels up from this file (the reddit-intel repo root).
