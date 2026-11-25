---
name: mcp-duckgo
description:
  Skills for web search and content scraping.
  Used when users need online searching and web scraping.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": {"bins": ["npx", "uvx"]}
      }
  }
---

# Skill
Executing Shell commands.

## Web search
- `npx -y mcporter call --stdio 'uvx duckduckgo-mcp-server' search query="{keyword}" max_results=10`

## Web fetch
- `npx -y mcporter call --stdio 'uvx duckduckgo-mcp-server' fetch_content url="https://..."`
