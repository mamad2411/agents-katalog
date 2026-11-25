---
name: goodreads-book-author-and-listopia-list-scraper
description: "Look up Goodreads books by URL, search query, or ISBN, or pull every book by an author, in a series, on a Listopia list, shelf, or genre page. Filter by rating, ratings count, publish year, language, genre, or author. Output fields: title, primaryAuthor, averageRating, ratingsCount, publishedYear and more, as JSON rows. Use it for requests like \"Goodreads book, author scraper\", or a CSV/JSON export of public Goodreads data."
---

# Goodreads Book, Author & Listopia List Scraper

Look up Goodreads books by URL, search query, or ISBN, or pull every book by an author, in a series, on a Listopia list, shelf, or genre page. Filter by rating, ratings count, publish year, language, genre, or author.

- Actor: https://apify.com/dataspryva/goodreads-book-author-and-listopia-list-scraper (ID `dataspryva~goodreads-book-author-and-listopia-list-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/goodreads-book-author-and-listopia-list-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Goodreads book, author scraper
- a repeatable export of public Goodreads data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `primaryAuthor`: Author
- `averageRating`: Rating
- `ratingsCount`: # Ratings
- `publishedYear`: Year
- `url`: URL

All 13 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | auto | What to scrape. Auto runs every non-empty input you provide. |
| `bookUrls` | array | no | [] | Goodreads book URLs, bare book IDs, or ISBNs. Used by books, reviews, editions, similar, and bookLists. (mode=books, reviews, editions, similar, bookLists, auto) |
| `searchQueries` | array | no | [] | Titles, authors, or keywords to search for. (mode=search, auto) |
| `isbns` | array | no | [] | ISBN-10 or ISBN-13 values. Hyphens and spaces are accepted. (mode=isbns, auto) |
| `authorUrls` | array | no | [] | Goodreads author URLs or bare author IDs. (mode=authors, auto) |
| `seriesUrls` | array | no | [] | Goodreads series URLs or bare series IDs. (mode=series, auto) |
| `listUrls` | array | no | [] | Listopia /list/show/ URLs or bare list IDs. (mode=lists, auto) |
| `shelfNames` | array | no | [] | Popular shelf names such as mystery, fantasy, or historical-fiction. (mode=shelves, auto) |
| `genreNames` | array | no | [] | Genre slugs such as fantasy, romance, or science-fiction. (mode=genres, auto) |
| `maxItems` | integer | no | 50 | Hard cap on every record emitted in the run, including review, edition, quote, list, and summary records. |
| `detailLevel` | string | no | full | Full returns complete book records. Listing returns lighter row records for search, author, series, list, shelf, and genre results. |
| `includeMetadata` | boolean | no | false | Also emit one author, series, or Listopia summary record alongside the books. |
| `includeRelated` | boolean | no | false | In auto mode, also collect reviews, editions, similar books, and lists for each book URL. |
| `minRating` | number | no |  | Drop books rated below this value. Decimals such as 4.5 are supported. |

21 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "mode": "isbns",
  "bookUrls": [
    "https://www.goodreads.com/book/show/4671.The_Great_Gatsby"
  ],
  "isbns": [
    "9780743273565"
  ],
  "maxItems": 25,
  "maxReviewsPerBook": 3,
  "maxEditionsPerBook": 3,
  "quoteTags": [
    "love"
  ],
  "maxQuotesPerSource": 3,
  "maxSimilarPerBook": 5,
  "maxListsPerBook": 5
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~goodreads-book-author-and-listopia-list-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~goodreads-book-author-and-listopia-list-scraper/runs" \
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
