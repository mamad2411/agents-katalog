---
name: crawlee-python-docs
description: >-
  Reference the bundled Crawlee for Python documentation exported from
  https://crawlee.dev/python/llms-full.txt. Use when answering Crawlee Python
  questions, writing or reviewing Crawlee Python crawler code, choosing between
  BeautifulSoupCrawler, ParselCrawler, HttpCrawler, PlaywrightCrawler, or
  AdaptivePlaywrightCrawler, working with Crawlee request routing, request
  loaders, storages, datasets, key-value stores, request queues, proxies,
  sessions, scaling, deployment, HTTP clients, Playwright browser options, or
  Crawlee Python API classes and methods.
---

# Crawlee Python Docs

Use the bundled references as the authoritative source for Crawlee for Python. The reference files are contiguous chunks from `https://crawlee.dev/python/llms-full.txt`; concatenating `references/*.md` in lexical order reconstructs the export.

## Lookup Workflow

1. Start with `references/00-docs-index.md` to find the relevant docs page or API page.
2. For API symbols, read `references/01-api-index.md`, then search the API chunks for the symbol heading.
3. For task guidance, read the relevant narrative docs file first, then load API chunks only for exact constructor, method, or option details.
4. Prefer `rg -n "term" references/*.md` before loading large files.

## References

- `references/00-docs-index.md`: export title and page index.
- `references/01-api-index.md`: API package index and category list.
- `references/02-api-private-through-crawlerinstrumentor.md`: API reference from `_AsyncSession` through `CrawlerInstrumentor`.
- `references/03-api-curlimpersonate-through-jsonfield.md`: API reference from `CurlImpersonateHttpClient` through `JsonField`.
- `references/04-api-keyvaluestore-through-playwrightprenav.md`: API reference from `KeyValueStore` through `PlaywrightPreNavCrawlingContext`.
- `references/05-api-processedrequest-through-robotstxtfile.md`: API reference from `ProcessedRequest` through `RobotsTxtFile`.
- `references/06-api-router-through-systemstatus.md`: API reference from `Router` through `SystemStatus`.
- `references/07-api-systeminfo-through-event.md`: API reference from `SystemInfo` through `Event`.
- `references/08-changelog.md`: changelog.
- `references/09-deployment.md`: Apify platform, AWS Lambda, Cloud Run, and Cloud Run functions.
- `references/10-examples.md`: example crawlers and recipes.
- `references/11-guides.md`: guides for adaptive Playwright, architecture, blocking avoidance, archives, error handling, HTTP clients and crawlers, login, Playwright, proxies, request loaders, routers, web servers, scaling, service locator, sessions, storage clients, storages, and tracing.
- `references/12-introduction.md`: introductory tutorial sequence.
- `references/13-quick-start.md`: quick start.
- `references/14-upgrading.md`: upgrading notes.

## Search Patterns

- API class or type: `rg -n "^# .*ClassName|ClassName\\b" references/0*-api-*.md`
- Constructor option: `rg -n "option_name|ClassName" references/0*-api-*.md`
- Crawler guidance: `rg -n "BeautifulSoupCrawler|ParselCrawler|HttpCrawler|PlaywrightCrawler|AdaptivePlaywrightCrawler" references/*.md`
- Request routing: `rg -n "Router|request router|label|default handler|error handler" references/*.md`
- Request loading and queues: `rg -n "RequestLoader|RequestList|RequestQueue|SitemapRequestLoader|enqueue_links" references/*.md`
- Storage: `rg -n "Dataset|KeyValueStore|RequestQueue|StorageClient|push_data" references/*.md`
- Proxy and sessions: `rg -n "ProxyConfiguration|ProxyInfo|Session|SessionPool|use_session_pool" references/*.md`
- Playwright hooks and browser options: `rg -n "pre_navigation_hooks|post_navigation_hooks|browser_launch_options|browser_new_context_options|headless|browser_type" references/*.md`
