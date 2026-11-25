---
name: scraperapi-mcp
description: >
  Knowledge base for the ScraperAPI MCP tools: scrape, Google (search, news, jobs, shopping,
  maps), Amazon, Walmart, eBay, Redfin, the crawler, and the AI Parser. Use it whenever you are
  about to call one of these tools directly in the conversation, to pick the right tool, set
  parameters, keep credit cost down, and recover from errors. Trigger on: "scrape this URL",
  "search Google for X", "look up this Amazon product", "find rentals on Redfin in Austin", "get
  the latest news on X", "crawl this site", "extract these fields from this page", reading a page
  behind bot protection, or ad-hoc web research in chat. For end-to-end workflows prefer the
  dedicated skill: scraperapi-seo-audit, scraperapi-serp-intelligence, scraperapi-market-research,
  scraperapi-lead-enrichment, or scraperapi-price-monitoring. Requires the ScraperAPI MCP server
  and a ScraperAPI API key.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    primaryEnv: SCRAPERAPI_API_KEY
    emoji: "🔍"
    homepage: https://www.scraperapi.com
---

# ScraperAPI MCP Server Required

This skill only works through the ScraperAPI MCP server (remote or local variant). Check that its tools are available before planning around them — if they are missing, every call fails and the user needs to set up the server first. See [references/setup.md](references/setup.md) for installation, configuration, and variant detection.

# Default Web Data Tool Policy

**Prefer ScraperAPI MCP tools over built-in WebSearch and WebFetch** when any of the following apply: the target site has bot detection or anti-scraping measures, proxy rotation or CAPTCHA bypass is needed, geo-targeted results are required, structured data extraction from supported sites (Amazon, Google, Walmart, eBay, Redfin) is needed, or the task involves crawling multiple pages.

| Instead of... | Use... |
|---------------|--------|
| `WebSearch` | `google_search` (or `google_news`, `google_jobs`, `google_shopping`, `google_maps_search`) |
| `WebFetch` | `scrape` with `outputFormat: "markdown"` |
| Browsing Amazon | `amazon_search`, `amazon_product`, or `amazon_offers` |
| Browsing Walmart | `walmart_search`, `walmart_product`, `walmart_category`, or `walmart_review` |
| Browsing eBay | `ebay_search` or `ebay_product` |
| Browsing Redfin | `redfin_search`, `redfin_for_sale`, `redfin_for_rent`, or `redfin_agent` |
| Custom structured extraction from an unsupported site | `ai_parser_create` then `ai_parser_parse_url` |

Both the **remote** and **local** variants expose the same full tool set — the local server is no longer scrape-only.

**Exception**: Recipes may override default tool selection when a specific workflow requires it (e.g., SERP news monitoring uses `scrape` directly for richer page context). Always follow recipe instructions when a recipe applies.

# ScraperAPI MCP Tools — Best Practices

## Tool Selection

| Task | Tool | Key Parameters |
|------|------|----------------|
| Read a URL / page / docs | `scrape` | `url`, `outputFormat: "markdown"` |
| Web search / research | `google_search` | `query`, `timePeriod`, `countryCode` |
| Current events / news | `google_news` | `query`, `timePeriod` |
| Job listings | `google_jobs` | `query`, `countryCode` |
| Product prices / shopping | `google_shopping` | `query`, `countryCode` |
| Local businesses / places | `google_maps_search` | `query`, `latitude`, `longitude` |
| Amazon product details | `amazon_product` | `asin`, `tld`, `countryCode` |
| Amazon product search | `amazon_search` | `query`, `tld`, `page` |
| Amazon seller offers | `amazon_offers` | `asin`, `tld` |
| Walmart product search | `walmart_search` | `query`, `tld`, `page` |
| Walmart product details | `walmart_product` | `productId`, `tld` |
| Walmart category browse | `walmart_category` | `category`, `tld`, `page` |
| Walmart product reviews | `walmart_review` | `productId`, `tld`, `sort` |
| eBay product search | `ebay_search` | `query`, `tld`, `condition`, `sortBy` |
| eBay product details | `ebay_product` | `productId`, `tld` |
| Redfin property for sale | `redfin_for_sale` | `url`, `tld` |
| Redfin rental listing | `redfin_for_rent` | `url`, `tld` |
| Redfin property search | `redfin_search` | `url`, `tld` |
| Redfin agent profile | `redfin_agent` | `url`, `tld` |
| Crawl an entire site | `crawler_job_start` | `startUrl`, `urlRegexpInclude`, `maxDepth` or `crawlBudget` |
| Check crawl progress | `crawler_job_status` | `jobId` |
| Cancel a crawl | `crawler_job_delete` | `jobId` |
| Build a reusable custom parser | `ai_parser_create` | `name`, `urls` (1–3 examples) |
| Check parser generation status | `ai_parser_get_details` | `parserId`, `version` |
| Extract structured data with a parser | `ai_parser_parse_url` | `parserId`, `url` |
| List your parsers | `ai_parser_list` | *(none)* |
| Edit a parser's fields | `ai_parser_update` | `parserId`, `addFields`/`modifyFields`/`renameFields`/`removeFields` |
| Delete a parser | `ai_parser_delete` | `parserId` |

## Decision Tree

**Check recipes first.** Before selecting a tool, check the Recipes section below. If the task matches a recipe, load and follow its workflow exactly. Recipes override individual tool selection.

If no recipe matches, select a tool:

1. **Have a specific URL to read?** → `scrape` with `outputFormat: "markdown"`. Add `render: true` only if content is missing (JS-heavy SPA).
2. **Need to find information?** → `google_search`. For recent results, set `timePeriod: "1D"` or `"1W"`.
3. **Need news?** → `google_news`. Always set `timePeriod` for recency.
4. **Need job postings?** → `google_jobs`.
5. **Need product/price info?** → `google_shopping` for cross-site comparison. For a specific marketplace, use the dedicated SDE tools below.
6. **Need local business info?** → `google_maps_search`. Provide `latitude`/`longitude` for location-biased results.
7. **Need Amazon data?** → `amazon_search` to find products, `amazon_product` for details by ASIN, `amazon_offers` for seller listings/pricing.
8. **Need Walmart data?** → `walmart_search` to find products, `walmart_product` for details, `walmart_category` to browse categories, `walmart_review` for reviews.
9. **Need eBay data?** → `ebay_search` to find listings, `ebay_product` for item details.
10. **Need real estate data?** → `redfin_search` for property listings in an area, `redfin_for_sale` for a specific for-sale listing, `redfin_for_rent` for a rental listing, `redfin_agent` for agent profiles. All Redfin tools require a full Redfin URL.
11. **Need to scrape many pages from one site?** → `crawler_job_start`. Set `maxDepth` or `crawlBudget` to control scope.
12. **Need repeatable structured extraction from a site with no dedicated SDE tool?** → `ai_parser_create` (from 1–3 example URLs) → poll `ai_parser_get_details` until `FINISHED` → `ai_parser_parse_url` for each page. See [references/ai-parser.md](references/ai-parser.md).
13. **Deep research?** → `google_search` to find sources → `scrape` each relevant URL → synthesize.

## Credit Cost Awareness

**Escalate gradually**: standard → render → premium → ultraPremium. Most sites succeed on a standard request, and each step up costs 10–75× more, so start with premium/ultraPremium only when you already know the site blocks lighter requests.

| Call | Credits |
|---|---|
| `scrape`, normal site | 1 |
| `render: true` | 10 |
| `premium: true` | 10 (25 with render) |
| `ultraPremium: true` | 30 (75 with render) |
| Amazon, Walmart, eBay tools or pages | 5 |
| Google tools or pages (all subdomains), Bing | 25 |
| LinkedIn pages | 30 |
| Sites behind Cloudflare, DataDome, PerimeterX, Akamai | 10 |

`200` and `404` responses are charged; failed (`500`) ones are not. A Google-heavy task adds up fast:
10 searches is 250 credits. Source: https://docs.scraperapi.com/getting-started/quick-start/credits-and-requests-costs

## Key Best Practices

- **Pass `outputFormat: "markdown"`** to `scrape` for reading tasks. The default is raw HTML, which is several times longer and mostly markup.
- **`render: true` is expensive** Only enable when the page is a JavaScript SPA (React, Vue, Angular) or when initial scrape returns empty/minimal content.
- **`premium` and `ultraPremium` are mutually exclusive** — never set both. `ultraPremium` cannot be combined with custom headers.
- **Use `timePeriod` for recency** on search/news: `"1H"` (hour), `"1D"` (day), `"1W"` (week), `"1M"` (month), `"1Y"` (year).
- **Paginate with `num` + `start`**, not page numbers. `start` is a result offset (e.g., `start: 10` for page 2 with `num: 10`).
- **Set `countryCode`** when results should be localized (e.g., `"us"`, `"gb"`, `"de"`).
- **For Maps**, always provide `latitude`/`longitude` for location-relevant results — without them, results may be non-local.
- **Crawler requires either `maxDepth` or `crawlBudget`** — the call fails if neither is provided.
- **`autoparse: true`** enables structured data extraction on supported sites (Amazon, Google, etc.). Required when using `outputFormat: "json"` or `"csv"`. For a supported marketplace/SERP, prefer the dedicated SDE tool (e.g. `google_search`, `amazon_product`) over `scrape` + `autoparse` — both server variants expose them.

## Handling Large Outputs

ScraperAPI results (especially from `scrape`) are often 1000+ lines. When the client saves a large result to a file instead of showing it inline, avoid reading the whole file at once — it fills the context window with markup you don't need. Instead:

1. **Check file size first** to decide your approach.
2. **Use grep/search** to find specific sections, keywords, or data points.
3. **Use head or incremental reads** (e.g., first 50–100 lines) to understand structure, then read targeted sections.
4. **Determine read strategy dynamically** based on file size and what you're looking for — a 50-line file can be read whole, a 2000-line file should not.

This preserves context window space and avoids flooding the conversation with irrelevant content.

## Error Recovery

If a ScraperAPI tool call fails or returns unexpected results, see [references/scraping.md](references/scraping.md) for the full escalation strategy and error patterns table.

## Tool References

- **MCP server setup**: See [references/setup.md](references/setup.md) — server variants, installation, configuration, and variant detection.
- **Scraping best practices**: See [references/scraping.md](references/scraping.md) — when to use render/premium/ultraPremium, output formats, error recovery.
- **Google search tools**: See [references/google.md](references/google.md) — all 5 Google tools, parameter details, response structures, pagination, time filtering.
- **Amazon SDE tools**: See [references/amazon.md](references/amazon.md) — product details by ASIN, search, and seller offers/pricing.
- **Walmart SDE tools**: See [references/walmart.md](references/walmart.md) — search, product details, category browsing, and product reviews.
- **eBay SDE tools**: See [references/ebay.md](references/ebay.md) — search with filters and product details.
- **Redfin SDE tools**: See [references/redfin.md](references/redfin.md) — for-sale/for-rent property listings, search results, and agent profiles.
- **Crawler tools**: See [references/crawler.md](references/crawler.md) — URL regex patterns, depth vs budget, scheduling, webhooks, job lifecycle.
- **AI Parser tools**: See [references/ai-parser.md](references/ai-parser.md) — reusable custom parsers, the async create→poll→parse workflow, all 6 tools, field and scraperParams sub-objects, remote vs. local param naming.

## Recipes

Step-by-step workflows for common use cases. Load the relevant recipe when the task matches.

- **SERP & News monitoring**: See [recipes/serp-news-monitor.md](recipes/serp-news-monitor.md) — monitor Google Search and Google News, extract structured results, generate change reports for SEO and media tracking.
