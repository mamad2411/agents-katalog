---
name: domain-scoped-site-crawler-for-markdown-datasets
description: "Crawl a website from one or more start URLs, staying on the same domain, and get back clean Markdown, text, or HTML per page with title, description, and crawl depth. Built for feeding LLM, RAG, or knowledge-base pipelines. Output fields: url, title, depth, wordCount, httpStatusCode and more, as JSON rows. Use it for requests like \"Domain-Scoped site scraper\", or a CSV/JSON export of public Domain-Scoped data."
---

# Domain-Scoped Site Crawler for Markdown Datasets

Crawl a website from one or more start URLs, staying on the same domain, and get back clean Markdown, text, or HTML per page with title, description, and crawl depth. Built for feeding LLM, RAG, or knowledge-base pipelines.

- Actor: https://apify.com/vexaloom-labs/domain-scoped-site-crawler-for-markdown-datasets (ID `vexaloom-labs~domain-scoped-site-crawler-for-markdown-datasets`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/domain-scoped-site-crawler-for-markdown-datasets.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Domain-Scoped site scraper
- a repeatable export of public Domain-Scoped data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `url`: URL
- `title`: Title
- `depth`: Depth
- `wordCount`: Words
- `httpStatusCode`: Status

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `startUrls` | array | yes |  | One or more URLs to start crawling from. The crawler follows links found on these pages and stays on the domain of the first start URL. |
| `maxCrawlDepth` | integer | no | 10 | How many links deep to follow from the start URLs. 0 means only the start URLs are crawled. |
| `maxCrawlPages` | integer | no | 20 | Maximum number of pages (and files) to store. The crawl stops when this limit is reached. |
| `useSitemaps` | boolean | no | false | Look for sitemaps (from robots.txt and /sitemap.xml) and enqueue the URLs they list. Finds pages that are not linked from the start URLs. |
| `useLlmsTxt` | boolean | no | false | Look for /llms.txt at the start URL domains and enqueue the files listed there (common on documentation sites). |
| `respectRobotsTxtFile` | boolean | no | true | Skip discovered pages that the site's robots.txt disallows. Start URLs are always crawled. |
| `crawlOnlyPagesChangedSince` | string | no |  | Optional date (YYYY-MM-DD or full ISO date-time). Crawls only pages that may have changed since then and outputs a delta. Leave empty to crawl everything. |
| `includeUrlGlobs` | array | no | [] | Only crawl discovered URLs matching these glob patterns (e.g. `https://example.com/docs/*`). Leave empty to allow everything on the domain. |
| `excludeUrlGlobs` | array | no | [] | Skip discovered URLs matching any of these glob patterns (e.g. *login*, *.pdf). |
| `includeUrlRegexps` | array | no | [] | Only crawl discovered URLs matching at least one of these regular expressions. Combined with glob patterns (both must pass when both are set). |
| `excludeUrlRegexps` | array | no | [] | Skip discovered URLs matching any of these regular expressions. |
| `keepUrlFragments` | boolean | no | false | Treat URLs that differ only in #fragment as different pages. Enable for single-page sites that use fragments as routes. |
| `ignoreCanonicalUrl` | boolean | no | false | When disabled, pages whose canonical URL points to a page that was already crawled are skipped as duplicates. |
| `outputFormat` | string | no | markdown | How page content is returned. Markdown keeps headings, lists, tables, and links — best for LLMs and RAG. |

12 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "startUrls": [
    {
      "url": "https://docs.apify.com"
    }
  ],
  "maxCrawlDepth": 1,
  "maxCrawlPages": 3
}
```

The input passes the Actor's input schema (checked at every publish). The run size follows the number of inputs you pass.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~domain-scoped-site-crawler-for-markdown-datasets/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~domain-scoped-site-crawler-for-markdown-datasets/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d @references/example-input.json)
RUN_ID=$(echo "$RUN" | jq -r '.data.id'); DATASET=$(echo "$RUN" | jq -r '.data.defaultDatasetId')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" -H "Authorization: Bearer $APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/datasets/$DATASET/items?format=json" -H "Authorization: Bearer $APIFY_TOKEN" > output.json
```

## Cost and limits

- Apify bills the Actor's usage on your account; the Actor's Pricing tab shows the current price.
- Keep the limit in the input small for a first run.

## Guardrails

- Public data only. Do not pass cookies, sessions or private account data.
- Do not use the output for spam, harassment or unlawful discrimination.
- Check the target site's terms and local law before running at scale.
