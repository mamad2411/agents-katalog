---
inclusion: always
---

# Scraping & Knowledge Graph — Quick Reference

Skills lengkap ada di `~/skills/scraping/`. Gunakan info ini sebagai referensi cepat.

## MCP Servers Scraping (siap install)

| Server | Package | Cocok untuk |
|--------|---------|-------------|
| fetch | `@modelcontextprotocol/server-fetch` | Artikel statis, gratis |
| puppeteer | `@modelcontextprotocol/server-puppeteer` | SPA/JS sites |
| playwright | `@playwright/mcp` | Full browser automation |
| markdownload | `mcp-markdownload` | HTML → Markdown bersih |
| jina | `mcp-jinaai` | Clean text, `r.jina.ai` |
| firecrawl | `@mendableai/firecrawl-mcp-server` | Batch crawl (butuh API key) |
| apify | `mcp-server-apify` | Social media (butuh API key) |

Install gratis (tanpa API key):
```bash
npm install -g @modelcontextprotocol/server-fetch @modelcontextprotocol/server-puppeteer @playwright/mcp mcp-markdownload mcp-jinaai
```

## Web Scrapers & Clippers

- **HTML2Obsidian** — CLI Python, auto [[WikiLinks]], SPA, YouTube
- **Minibase** — AI cleaning, YouTube/Twitter/Reddit, MCP built-in
- **Obsidian Web Clipper** — Official Obsidian, template per domain
- **Slurp** — OpenGraph metadata, Obsidian plugin
- **MarkDownload** — Browser extension ringan, open-source

## Knowledge Graph

- **Knowledge Brain** — Cytoscape.js graph + streaming AI chat (DeepSeek/OpenAI/Gemini/Claude)
- **MegaMem** — Neo4j/FalkorDB + MCP server (AI agent bisa query vault)
- **MOC Plugin** — Dynamic Map of Content, filter AND/OR/NOT/regex

## Decision Guide

```
Static article/docs?      → MCP Fetch atau Jina (gratis)
SPA / React site?         → Playwright MCP
Batch crawl domain?       → Firecrawl MCP
Social media?             → Apify MCP
Clip ke Obsidian cepat?   → MarkDownload extension
Vault jadi knowledge DB?  → MegaMem + MCP
Graph + AI chat vault?    → Knowledge Brain
```

Detail lengkap: `~/skills/scraping/`
