---
name: google-scholar-paper-and-citation-search-scraper
description: "Search Google Scholar by keyword and get structured records for papers and citations, with author, venue, year, citation counts, and links to PDFs and related work. Filter by year range, document format, and article type. Output fields: title, name, authors, year, publication and more, as JSON rows. Use it for requests like \"Google Scholar paper scraper\", or a CSV/JSON export of public Google Scholar data."
---

# Google Scholar Paper & Citation Search Scraper

Search Google Scholar by keyword and get structured records for papers and citations, with author, venue, year, citation counts, and links to PDFs and related work. Filter by year range, document format, and article type.

- Actor: https://apify.com/dataspryva/google-scholar-paper-and-citation-search-scraper (ID `dataspryva~google-scholar-paper-and-citation-search-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/google-scholar-paper-and-citation-search-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Google Scholar paper scraper
- a repeatable export of public Google Scholar data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `name`: Author
- `authors`: Authors
- `year`: Year
- `publication`: Publication
- `citations`: Citations
- `documentType`: Type
- `documentLink`: PDF/HTML
- `link`: Link
- `clusterId`: Cluster
- `scholarUrl`: Scholar URL

All 13 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | no | search | What to fetch: paper search, citing papers, or public author profiles. |
| `queries` | array | no |  | Keywords or paper titles to search on Google Scholar (mode=search). Each query runs separately. |
| `clusterIds` | array | no |  | Paper cluster IDs or Google Scholar 'cites=' URLs to list citing papers for (mode=citations). |
| `authorIds` | array | no |  | Google Scholar author IDs or profile URLs to export (mode=authorProfile). |
| `maxItems` | integer | no | 100 | Maximum papers per query or cluster, or papers per author. Google Scholar serves about 10 search results per page. |
| `sortBy` | string | no | relevance | Sort search results by relevance or date (mode=search). |
| `filter` | string | no | all | Keep only PDF or HTML results; applied to returned rows (mode=search). |
| `articleType` | string | no | any | Return all articles or review articles only (mode=search). |
| `newerThan` | integer | no |  | Only include papers published in this year or later (mode=search). |
| `olderThan` | integer | no |  | Only include papers published in this year or earlier (mode=search). |
| `author` | string | no |  | Return papers written by this author, e.g. 'Geoffrey Hinton' (mode=search). |
| `publication` | string | no |  | Return papers from this journal or venue, e.g. 'Nature' (mode=search). |
| `titleOnly` | boolean | no | false | Match the query against paper titles instead of the full text (mode=search). |
| `includeCitationFormats` | boolean | no | false | Also return MLA, APA, Chicago, Harvard, and Vancouver citations for returned rows, within a bounded budget (mode=search or citations). |

1 more optional field on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "queries": [
    "attention is all you need"
  ],
  "maxItems": 25
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~google-scholar-paper-and-citation-search-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~google-scholar-paper-and-citation-search-scraper/runs" \
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
