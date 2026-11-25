---
name: web-search
description: Search the web for current information, news, weather, prices, and facts.
tools: [shell, web_search]
trigger: search, google, look up, find out, what is, news, weather, price, latest, current, today, who is, where is
---

# Web Search Skill

## When to Use
- Questions about current events, news, weather, or prices
- "What is...", "Who is...", "When did..." questions about things you don't know
- Anything requiring real-time or recent information

## How to Search
Run the web search command:

```bash
/opt/kovo/scripts/web-search.sh "Al Ain weather today"
```

This returns JSON with title, url, and snippet for each result. Parse the JSON and summarize the findings for the user.

## How to Read a URL
If you need the full text of a webpage:

```bash
/opt/kovo/scripts/link-reader.sh "https://example.com/article"
```

This returns the readable text content of the page.

## Response Style
- Give the answer first, then supporting details
- Cite sources naturally: "According to [source]..."
- If results are unclear, say so honestly
- ALWAYS try searching before saying you can't find information
