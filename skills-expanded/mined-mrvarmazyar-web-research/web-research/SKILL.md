---
name: web-research
description: Use for all web searches and URL fetching — unified CLI combining tinyfish search + Groq summarization. Replaces both native WebSearch and native WebFetch. Triggers on: research tasks, finding docs, "search for X", "look up X", fetching any public URL. Skip for GitHub repos/issues (use gh CLI), Jira/Confluence (use MCP tools), internal/authenticated URLs.
---

# Web Research (`wr`)

Unified web research CLI. Tinyfish for search, Groq for summarization, local cache for speed.

## Auto-Setup Check

```bash
which wr || { echo "Install: cd ~/web-research && go build -o ~/.local/bin/wr ./cmd/wr"; }
wr setup
```

## Commands

```bash
wr search "<query>"              # search only → URLs + snippets
wr fetch "<url>" "<prompt>"      # fetch URL → Groq summary
wr research "<query>"            # search + fetch top 3 + summarize
wr setup                         # check TINYFISH_API_KEY + GROQ_API_KEY
```

## Optimal Usage Pattern

```
1. wr research "query"           → full pipeline, best for research tasks
2. wr search "query"             → when you just need URLs first
   wr fetch "<url>" "<prompt>"   → then fetch specific result
```

## When to Skip

- GitHub issues/PRs/repos → `gh` CLI
- Jira/Confluence → Atlassian MCP tools  
- Internal/authenticated URLs → native WebFetch
- Already have exact answer → no need to search

## Env Vars

```bash
export TINYFISH_API_KEY="..."   # https://agent.tinyfish.ai → API Keys
export GROQ_API_KEY="..."       # https://console.groq.com → API Keys (free)
export WR_CACHE_DAYS=7          # optional, default 7
```

## Fallback

If `wr` not installed or `wr setup` shows missing keys:
- Search → fall back to native WebSearch
- Fetch → fall back to `~/.claude/skills/web-fetch-local/fetch.sh`
