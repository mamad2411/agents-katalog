---
name: firecrawl_web
description: Hybrid Firecrawl workflow for search, scrape, interact, browser automation, map, crawl, batch scrape, parse, extract, agent jobs, account usage, queues, and webhook-aware status work through the official Firecrawl CLI with a REST fallback.
license: MIT
compatibility:
  runtimes:
    - codex
    - openclaw
    - claude_code
    - cursor
    - windsurf
metadata:
  category: research
  capability_taxonomy_ids:
    - cap.research.web_search
    - cap.research.web_scrape
    - cap.research.browser_automation
  distribution_scope: public
  invocation_strategy: explicit
  version: v0.3
  source_of_truth: github:firecrawl/firecrawl
---

# Firecrawl Web

Use this skill when a task needs Firecrawl for web search, scraping, browser-backed interaction, site discovery, crawling, local document parsing, structured extraction, agentic research, usage checks, queues, or job status/cancel/error inspection.

Firecrawl consumes paid credits. Prefer the official Firecrawl CLI and MCP where available; use the bundled REST fallback only for exact API calls that the CLI does not expose cleanly.

## Preconditions

- Preferred: `FIRECRAWL_API_KEY` is present in the environment.
- Supported fallback: `.env.local` next to the installed skill with `FIRECRAWL_API_KEY=...`.
- Official setup for agents and OpenClaw:
  - `npx -y firecrawl-cli@latest init --all --browser`
  - `firecrawl --status`
- Never print or commit the API key. Do not ask the user to paste a key into chat output.

## Tool Selection

1. Use `firecrawl` or `fcrawl` for normal work.
2. Use `search` for web/news/image search, `tbs`, location/country targeting, categories, and optionally scraping results.
3. Use `scrape` for one public URL and formats such as markdown, html, rawHtml, links, images, screenshot, summary, JSON, changeTracking, branding, audio, and attributes.
4. Use `interact` after a scrape when the task needs a form, click, login flow, pagination, dynamic extraction, prompt-driven interaction, or Playwright/agent-browser code.
5. Use `browser` for remote browser sandbox work, especially multi-step workflows where agent-browser commands are better than a single scrape.
6. Use `map` before `crawl` when URL discovery may be enough.
7. Use `crawl` only with an explicit low `--limit` unless the user clearly requested broad ingestion.
8. Use `batch scrape` for a known list of URLs.
9. Use `parse` for local or non-public documents. Use `scrape` for public document URLs.
10. Use `extract` or `agent` for multi-page structured extraction and autonomous research; prefer `agent` only with an explicit `maxCredits` budget.
11. Use `scripts/firecrawl_call.py` for status, cancel, errors, activity, usage, queue, parse multipart, or any precise `/v2/...` endpoint not covered by the CLI.

## Command Patterns

- Check setup:
  - `fcrawl --status`
- Official all-agent setup:
  - `npx -y firecrawl-cli@latest init --all --browser`
- Scrape a page:
  - `fcrawl https://example.com --only-main-content`
  - `fcrawl scrape https://example.com --format markdown,links --pretty`
- Search:
  - `fcrawl search "query" --limit 5 --pretty`
  - `fcrawl search "query" --sources web,news,images --categories research,pdf --tbs qdr:w --country US`
  - `fcrawl search "query" --scrape --scrape-formats markdown --only-main-content --pretty`
- Interact after scrape:
  - `fcrawl scrape https://example.com`
  - `fcrawl interact "Click the pricing tab and extract plan names"`
  - `fcrawl interact stop`
- Browser sandbox:
  - `fcrawl browser "open https://example.com"`
  - `fcrawl browser "snapshot"`
  - `fcrawl browser "scrape"`
  - `fcrawl browser close`
- Map and crawl:
  - `fcrawl map https://example.com --limit 20`
  - `fcrawl crawl https://example.com --limit 25 --max-depth 2 --wait --progress --pretty`
- Agent:
  - `fcrawl agent "Find and compare pricing" --urls https://example.com --max-credits 25 --wait --pretty`
- REST fallback:
  - `fcrawl api --method GET --path /v2/team/credit-usage`
  - `fcrawl api --method GET --path /v2/crawl/<job-id>`
  - `fcrawl api --method DELETE --path /v2/crawl/<job-id>`
  - `fcrawl api --method POST --path /v2/parse --file ./report.pdf --body-json '{"formats":["markdown"]}'`
- Convenience helpers:
  - `fcrawl usage`
  - `fcrawl search-web "query" --limit 5 --scrape`
  - `fcrawl scrape-url https://example.com --formats markdown,links`
  - `fcrawl map-site https://example.com --limit 50`
  - `fcrawl batch-scrape urls.txt --formats markdown`
  - `fcrawl parse-file ./report.pdf --formats markdown`
  - `fcrawl safe-crawl https://docs.example.com --limit 25 --max-depth 2`
  - `fcrawl agent-run "Find competitors" --max-credits 50`
  - `fcrawl crawl-status <job-id>`
  - `fcrawl wait crawl <job-id> --poll 5 --timeout 600`
  - `fcrawl job-errors crawl <job-id>`
  - `fcrawl queue-status`
  - `fcrawl cancel crawl <job-id>`
  - `fcrawl smoke --dry-run`

## Safety Rules

- Default to small, read-only operations: search limit <= 5, map limit <= 20, crawl limit <= 25.
- Do not run broad crawls, large batch scrapes, browser sessions, enhanced proxy, OCR, audio, JSON mode, extract, or agent jobs without a clear user goal and bounded output.
- For `crawl`, always set `limit`; the API default can be very large.
- For `agent`, always set `maxCredits`.
- Stop interact/browser sessions when done:
  - `fcrawl interact stop`
  - `fcrawl browser close`
- If a costly option is necessary, state the reason and keep the limit/budget explicit.

## References

- `references/endpoint_catalog.md` for API v2 coverage, endpoints, and examples.
- `references/method_selection.md` for choosing the narrowest method before spending credits.
- `references/jobs.md` for async status, wait, errors, cancel, active crawls, queue, and activity workflows.
- `references/output_management.md` for `--output`, `--output-dir`, and `--jsonl`.
- `references/webhooks.md` for crawl, batch, and agent webhook patterns.
- `references/cost_and_safety.md` for credit-sensitive options and confirmation rules.
- `references/use_cases.md` for detailed method-specific examples and domain workflows.
- `references/openclaw.md` for OpenClaw install and verification notes.
- `recipes/` for runnable workflow examples such as RAG ingestion, competitor pricing, ecommerce snapshots, lead enrichment, investment news, SEO audit, data migration, and browser checks.
