---
name: steam-game-reviews-and-playtime-extractor
description: "Pull Steam customer reviews for any game by URL or name, with thumbs up/down verdicts, reviewer playtime, helpfulness votes, and language filters. Output fields: gameTitle, rating, reviewText, authorName, authorPlaytimeForever and more, as JSON rows. Use it for requests like \"Steam game reviews scraper\", or a CSV/JSON export of public Steam data."
---

# Steam Game Reviews & Playtime Extractor

Pull Steam customer reviews for any game by URL or name, with thumbs up/down verdicts, reviewer playtime, helpfulness votes, and language filters.

- Actor: https://apify.com/dataspryva/steam-game-reviews-and-playtime-extractor (ID `dataspryva~steam-game-reviews-and-playtime-extractor`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/steam-game-reviews-and-playtime-extractor.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Steam game reviews scraper
- a repeatable export of public Steam data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `gameTitle`: Game
- `rating`: Rating
- `reviewText`: Review
- `authorName`: Author
- `authorSteamId`: Author ID
- `authorPlaytimeForever`: Playtime (hrs)
- `votesHelpful`: Helpful Votes
- `timestampCreated`: Date
- `language`: Language
- `steamPurchase`: Steam Purchase
- `primarilySteamDeck`: Steam Deck

All 13 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | reviews | reviews = one row per review; gameSummary = one row per game with metadata and overall score. |
| `appIds` | array | no | [] | Numeric app IDs, store URLs, community review URLs, or old appreviews URLs. Example: 1174180 or `https://store.steampowered.com/app/1174180/` |
| `startUrls` | array | no |  | Steam store page URLs for the games to scrape. Merged with appIds. |
| `gameNames` | array | no | [] | Search Steam by name. An exact case-insensitive title match is preferred over the first search result. |
| `maxReviews` | integer | no | 50 | Reviews to collect per game. Use 0 for every matching review (hard safety cap 1,000,000 per game). |
| `maxGames` | integer | no | 0 | Cap the merged game list. Use 0 for no cap. |
| `reviewType` | string | no | all | Filter reviews by recommendation verdict. |
| `language` | string | no | all | Steam language code for review text. Select All Languages to include every language. |
| `sortBy` | string | no | recent | recent and updated walk the full history; helpful is a ranked sample inside the helpfulness window; funny is also ranked and not exhaustive. |
| `helpfulWithinDays` | integer | no | 30 | Only for sortBy=helpful: rank reviews from the last 1-365 days. Use recent for full history. |
| `purchaseType` | string | no | all | Whether the reviewer acquired the game through Steam, outside Steam, or either. |
| `minPlaytimeHours` | integer | no | 0 | Minimum hours played at the time of review. Use 0 for no minimum. |
| `maxPlaytimeHours` | integer | no | 0 | Maximum hours played at the time of review. Use 0 for no maximum. |
| `steamDeckOnly` | boolean | no | false | Only reviews written while playing primarily on a Steam Deck. |

5 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "startUrls": [
    {
      "url": "https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/"
    }
  ],
  "maxReviews": 25,
  "mode": "reviews"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxReviews` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~steam-game-reviews-and-playtime-extractor/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~steam-game-reviews-and-playtime-extractor/runs" \
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
