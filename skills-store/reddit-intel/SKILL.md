---
name: reddit-intel
description: |
  Reddit competitive intelligence for any product. Discovers keywords, finds relevant
  communities, searches for posts with pain points, and analyzes comments to extract
  competitor mentions, real user language, and unmet needs.
  Runs 4 incremental steps: expand-keywords / expand-subreddits / find-posts /
  analyze-comments. Also: init (first-time setup).
  Each run: read JSONL → search → dedup-append → re-render Markdown.
  Requires: Exa MCP server for Reddit search.
  Usage: /reddit-intel step-name
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - mcp__exa__web_search_exa
  - AskUserQuestion
metadata:
  trigger: When user asks to search Reddit posts, analyze comments, expand keywords, discover communities, or do Reddit competitive intelligence
---

# Reddit Competitive Intelligence (reddit-intel)

Incremental intelligence gathering: each step runs independently, idempotently. Each execution reads existing JSONL data, searches for new entries, dedup-appends, and re-renders display Markdown. Data only grows, never deletes. Accumulates over time.

**Bilingual**: Set `"language": "en"` or `"zh"` in config. All rendered Markdown labels and stats output adapt automatically. The `init` command picks the matching product-context template.

---

## Prerequisites

- **Exa MCP Server**: Required for Reddit search. Add Exa MCP to your Claude Code config.
- **Config File**: Run `/reddit-intel init` to create `.reddit-intel.json` in your project root.
- **Product Context**: Fill in `product-context.md` with your product info after init.

---

## Tool Selection Rules (must follow)

- When searching Reddit content, **DO NOT** use built-in WebSearch (reddit.com is blocked by Anthropic's crawler, causing empty retries and wasted tokens)
- **MUST** use `mcp__exa__web_search_exa` (type="deep") for Reddit posts and comments
- Non-Reddit web pages can use built-in WebSearch or Exa
- Use WebFetch for specific URLs
- Max 3 query attempts per search intent; skip if no results
- Target: keep tool calls under 30 per step

---

## Configuration

The skill uses `.reddit-intel.json` in your project root:

```json
{
  "data_dir": "./reddit-intel/data",
  "product_name": "MyProduct",
  "product_context": "./reddit-intel/product-context.md",
  "language": "en"
}
```

Created by `init`. The script (`jsonl_ops.py`) locates this by walking up from CWD.

---

## Data Directory

```
SCRIPT = scripts/jsonl_ops.py  (relative to this skill directory)
```

| JSONL Source | Markdown Display |
|---|---|
| `{data_dir}/keywords.jsonl` | `{data_dir}/keywords.md` |
| `{data_dir}/subreddits.jsonl` | `{data_dir}/subreddits.md` |
| `{data_dir}/posts.jsonl` | `{data_dir}/posts.md` |
| `{data_dir}/comments.jsonl` | `{data_dir}/comments.md` |

---

## JSONL Schema

### keywords.jsonl (unique key: `keyword`)

```json
{"keyword": "context loss", "category": "pain", "reddit_usage": "AI keeps forgetting my project context", "source": "r/LocalLLaMA", "added": "2026-02-06"}
```

category values: `pain` | `tool` | `scenario` | `solution`

### subreddits.jsonl (unique key: `name`)

```json
{"name": "r/LocalLLaMA", "tier": 1, "members": "451K", "activity": "high", "promo_policy": "discussion OK", "relevance": "primary", "strategy": "Pain-point replies, technical discussions", "added": "2026-02-06"}
```

tier values: 1 (core) / 2 (high relevance) / 3 (general developer) / 4 (observing)

### posts.jsonl (unique key: `url`)

```json
{"url": "https://www.reddit.com/...", "title": "...", "subreddit": "r/LocalLLaMA", "upvotes": 85, "comments": 47, "post_date": "2025-06-01", "pain_category": "context_loss", "product_solution": "Auto-inject context on each session", "status": "active", "added": "2026-02-06"}
```

status values: `active` | `archived`

### comments.jsonl (unique key: `post_url` + `content[:50]`)

```json
{"post_url": "https://www.reddit.com/...", "type": "competitor", "content": "I use Cursor when I exceed the token limit", "competitor": "Cursor", "sentiment": "positive", "insight": "Cursor used as fallback", "added": "2026-02-06"}
```

type values: `competitor` | `language` | `need`

---

## Common Operation Flow

Every step follows the same 6-step pattern:

1. **Read JSONL** -- Parse the corresponding data file, extract existing unique key set for dedup
2. **Read context** -- Load relevant reference files (product-context.md, etc.)
3. **Execute search/generate** -- Use Exa to search Reddit or generate new entries from existing data
4. **Dedup-append** -- Filter out entries with existing unique keys, append only new lines to JSONL
5. **Render Markdown** -- Run `python3 SCRIPT render <type>`; if script unavailable, manually rewrite .md
6. **Output statistics** -- Report the number of new entries added and current totals

---

## Step Dispatch

Route to the corresponding step based on user arguments.

### No arguments

When no step is specified, display current data stats and show menu:

1. Use `wc -l` to count lines in each JSONL file
2. Show 4 available steps with aliases
3. Wait for user selection

Output example:
```
Current data stats:
  keywords:   45 entries
  subreddits: 53 entries
  posts:      36 entries
  comments:   31 entries

Available Steps:
  1. expand-keywords   (kw)  -- Discover pain-point keywords from Reddit
  2. expand-subreddits (sub) -- Find relevant Reddit communities
  3. find-posts        (fp)  -- Search for posts matching your product's pain points
  4. analyze-comments  (ac)  -- Extract competitors, user language, unmet needs
```

---

### init

**Goal**: First-time setup. Creates config file and data directory.

**Flow**:
1. Ask user for `data_dir` (default: `./reddit-intel/data`), `product_name`, and `lang` (en/zh)
2. Run `python3 SCRIPT init --data-dir <dir> --product-name <name> --lang <en|zh>`
   - Template auto-selected: `--lang en` → `product-context.template.md`, `--lang zh` → `product-context.template.zh.md`
3. Tell user to fill in `product-context.md` with their product details

---

### expand-keywords (aliases: keywords, kw)

**Goal**: Expand keyword library, discover how Reddit users actually describe pain points related to your product domain.

**Input**: `keywords.jsonl` + `product-context.md` (from config)

**Flow**:
1. Read existing keywords, group by category
2. Read `references/step-details.md` Step 1 section for detailed logic
3. For each category, use `mcp__exa__web_search_exa` (type="deep") to search Reddit for new trending terms
4. Generate associations from existing words: synonyms, long-tail variants, Reddit vernacular
5. Dedup by `keyword`, append new entries
6. Render `keywords.md`, display as tables grouped by category

---

### expand-subreddits (aliases: subreddits, sub)

**Goal**: Discover new relevant Reddit communities.

**Input**: `subreddits.jsonl` + `keywords.jsonl`

**Flow**:
1. Read existing subreddit list
2. Read `references/step-details.md` Step 2 section for detailed logic
3. Use new keywords via `mcp__exa__web_search_exa` (type="deep") to discover new communities
4. Newly discovered communities default to tier=4 (observing), upgrade manually later
5. Dedup by `name`, append new entries
6. Render `subreddits.md`, display grouped by tier

---

### find-posts (aliases: posts, fp)

**Goal**: Search target communities for posts containing pain points relevant to your product.

**Input**: `posts.jsonl` + `keywords.jsonl` + `subreddits.jsonl`

**Flow**:
1. Read existing post URL set
2. Read `references/step-details.md` Step 3 section for detailed logic
3. In tier 1/2 subreddits, use `mcp__exa__web_search_exa` (type="deep") + keywords to search for new posts
4. Filter criteria: within last 30 days, has engagement (upvotes > 10 or comments > 5)
5. Analyze pain category, map to product solution (user-defined pain categories from product-context.md)
6. Dedup by `url`, append new posts
7. Mark existing posts older than 30 days as `archived`
8. Render `posts.md`

---

### analyze-comments (aliases: comments, ac)

**Goal**: Analyze comment sections of active posts, extract competitor info, real user language, and unmet needs.

**Input**: `posts.jsonl` (status=active) + `comments.jsonl`

**Flow**:
1. Find unanalyzed active posts (post_url not in existing comments.jsonl list)
2. Read `references/step-details.md` Step 4 section for detailed logic
3. Use `mcp__exa__web_search_exa` (type="deep") to search post title + subreddit to fetch comment content
4. Extract three types of information: competitor (competitor mentions), language (real user expressions), need (unmet needs)
5. Dedup by `post_url + content[:50]`, append new entries
6. Render `comments.md`

---

## Reference Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `references/step-details.md` | Detailed execution logic per step | Before executing each step |
| product-context.md (from config) | Product positioning and feature summary | expand-keywords, find-posts |
