---
name: google-news-keyword-and-full-text-article-scraper
description: "Search Google News by keyword with real resolved article links, headlines, sources, and dates, plus optional full article text and image extraction, filterable by date, language, and publisher. Output fields: title, source, domain, publishedAt, url and more, as JSON rows. Use it for requests like \"Google News keyword scraper\", or a CSV/JSON export of public Google News data."
---

# Google News Keyword & Full-Text Article Scraper

Search Google News by keyword with real resolved article links, headlines, sources, and dates, plus optional full article text and image extraction, filterable by date, language, and publisher.

- Actor: https://apify.com/nimbryxo-studio/google-news-keyword-and-full-text-article-scraper (ID `nimbryxo-studio~google-news-keyword-and-full-text-article-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/google-news-keyword-and-full-text-article-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Google News keyword scraper
- a repeatable export of public Google News data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `source`: Source
- `domain`: Domain
- `publishedAt`: Published
- `url`: URL
- `fullTextStatus`: Status

All 11 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | keyword | What to scrape. Each mode reads its own list field below. |
| `queries` | array | no | [] | One or more keyword queries. Google operators such as site:, intitle: and OR are supported. Results are deduplicated across queries. |
| `topics` | array | no | [] | Topic names (WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE, HEALTH), TOP for top stories, Google News topic hashes/section URLs, or topic URLs. |
| `newsUrls` | array | no | [] | Google News search URLs, topic URLs, RSS search/topic URLs, or RSS/Atom feed URLs to convert into a feed. |
| `rssUrls` | array | no | [] | Any public RSS or Atom feed. Google News links inside the feed are resolved to publisher URLs automatically. |
| `articleUrls` | array | no | [] | Publisher article URLs or Google News article URLs. Every page is fetched and full text is extracted, with a per-record status when a publisher blocks or paywalls it. |
| `language` | string | no | en | Language of the Google News edition. Combined with country in the edition token (for example US:en, DE:de, JP:ja). |
| `country` | string | no | US | Country edition for Google News. The actor always pins the edition so results do not change with the machine's IP. |
| `dateRange` | string | no | any | Recency window. Every item is post-filtered by its real publication time, so items newer than the window never leak. 'custom' uses startDate/endDate. |
| `startDate` | string | no |  | Custom range start (YYYY-MM-DD, inclusive). Also used when dateRange=custom. |
| `endDate` | string | no |  | Custom range end (YYYY-MM-DD, inclusive). Items published after the end are dropped client-side. |
| `maxResultsPerQuery` | integer | no | 20 | Maximum records taken from each Google News feed request (1-100, Google's own cap is about 100). |
| `maxItems` | integer | no | 500 | Hard cap on unique records emitted by the run (1-5000). |
| `extractFullText` | boolean | no | false | Fetch each publisher page and extract its article body, description, author, and image. Default off for fast metadata-only runs. The articleUrls mode always extracts. |

2 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "queries": [
    "artificial intelligence"
  ],
  "maxResultsPerQuery": 3,
  "maxItems": 25,
  "mode": "keyword"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~google-news-keyword-and-full-text-article-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~google-news-keyword-and-full-text-article-scraper/runs" \
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
