---
name: get-started
description: Set up Octocrawl after installing it and learn which tool fits a web task. Use when the person asks how to start with Octocrawl, connect their account, or read a web page with it.
---

# Get started with Octocrawl

Octocrawl turns public web pages into clean Markdown, tables, links and JSON, each with an Evidence Record that says where and when the page was read.

## Connect

The plugin connects to `https://mcp.octocrawl.dev/mcp-oauth`. The first time a tool runs, the person signs in to their Octocrawl account (with Google, GitHub or an emailed link at octocrawl.dev) and chooses Authorize. Every account gets 500 free credits a month. The connection is listed under MCP connections at https://octocrawl.dev/dashboard/keys/, where it can be disconnected.

## Choose the tool

- One known page: `scrape`. Ask for `formats: ["markdown"]` for the text, `["tables"]` for a page's tables, `["links"]` for its links.
- The pages of a site without reading each one: `map`.
- A section of a site, page by page (up to 500 pages): `crawl`, then `wait_crawl`, then `get_crawl_pages`.
- A known list of URLs (up to 1,000): `batch_scrape`, then `wait_batch`, then `get_batch_items`.
- One Amazon.sg product page (`https://www.amazon.sg/dp/<ASIN>`) as checked JSON: `scrape_product`.

## Read the result

- `status` says whether the page was read: `success`, or a failure such as `failed` with `failureReason` `http_error` for a missing page. Report a failed or blocked page as such; do not present an error page as the content that was asked for.
- To cite a page, use `evidenceRecord.finalUrl` and `evidenceRecord.fetchedAt`.
- `agentHints`, when present, say what to change on the next call.

## What it does not do

It reads public pages only. It obeys robots.txt, refuses private network addresses, and does not sign in to sites, solve CAPTCHAs or use proxies. Monitoring, saved logins and larger crawls or batches run with the open-source Octocrawl on the person's own computer (https://octocrawl.dev/docs/connect-mcp/).
