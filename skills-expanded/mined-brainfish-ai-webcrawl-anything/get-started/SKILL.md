---
name: get-started
description: Use Webcrawl to search the web, read pages and documents with sources, map or crawl a site, extract fields, and set up page monitors.
---

# Getting started with Webcrawl

Use these tools when the user needs live information from public web pages or documents.

## Pick the tool

- **web_search**: find pages. Set `category` for structured results: `news`, `shopping`, `flights`, `hotels`, `real-estate`, `business`, `security` (CVEs), `academic` or `tech`. Call `search_categories` if unsure which filters exist.
- **web_read**: read one URL as Markdown.
- **web_parse**: read a PDF, Word, Excel, PowerPoint, image, YouTube or audio/video URL. For long files set `background: true`, then poll `web_parse_status` with the returned id.
- **web_map**: list a site's URLs before choosing what to read.
- **web_crawl**: read up to 25 pages of one site.
- **web_extract**: return structured JSON from a URL using a prompt or JSON Schema.
- **web_rerank**: order a set of documents by relevance to a query.
- **web_monitor**: create, list, check, pause, resume or delete scheduled monitors on the user's account.

## Good habits

1. Cite the source URL for every fact taken from a result.
2. Prefer `web_map` then a few `web_read` calls over a large crawl.
3. Only read public pages. Do not attempt to sign in to sites, solve challenges or read pages that need the user's credentials.
4. Before deleting a monitor, confirm with the user which monitor and that they want it removed.
5. When a page cannot be read, say so and offer a search for another source instead of guessing its content.

## First prompts to try

- "Read https://modelcontextprotocol.io/specification and summarize it with links."
- "Find recent critical CVEs for OpenSSL and list the fixed versions."
- "Watch this pricing page daily and email me when a plan price changes."
