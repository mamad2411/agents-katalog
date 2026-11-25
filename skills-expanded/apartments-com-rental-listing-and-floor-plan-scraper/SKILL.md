---
name: apartments-com-rental-listing-and-floor-plan-scraper
description: "Search Apartments.com rentals by city, bedroom count, price, property type, pet policy, and amenities, or scrape specific listing URLs directly. Returns rent ranges, per-unit floor plans, walkability scores, amenities, and leasing contact details. Output fields: name, address, priceMin, priceMax, priceCurrency and more, as JSON rows. Use it for requests like \"Apartments.com rental listing scraper\", or a CSV/JSON export of public Apartments.com data."
---

# Apartments.com Rental Listing & Floor Plan Scraper

Search Apartments.com rentals by city, bedroom count, price, property type, pet policy, and amenities, or scrape specific listing URLs directly. Returns rent ranges, per-unit floor plans, walkability scores, amenities, and leasing contact details.

- Actor: https://apify.com/dataspryva/apartments-com-rental-listing-and-floor-plan (ID `dataspryva~apartments-com-rental-listing-and-floor-plan`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/apartments-com-rental-listing-and-floor-plan-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [See the rent range before the tour](https://www.youtube.com/shorts/YvLah5jotOg)

## When to use

Use this skill when the user wants:

- Apartments.com rental listing scraper
- a repeatable export of public Apartments.com data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `name`: Name
- `address`: Address
- `city`: City
- `state`: State
- `zipCode`: Zip Code
- `priceMin`: Price Min
- `priceMax`: Price Max
- `priceCurrency`: Price Currency
- `bedsMin`: Beds Min
- `bedsMax`: Beds Max
- `propertyType`: Property Type
- `rating`: Rating
- `photoCount`: Photo Count
- `propertyManager`: Property Manager
- `url`: Url

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | no | search | How to find listings: `search` uses a city or ZIP plus filters; `urls` uses the Apartments.com URLs you paste; `listingKeys` looks up the listing keys you paste. |
| `searchLocation` | string | no |  | US city and state (`New York, NY`) or 5-digit ZIP (`10001`). Used only in search mode. |
| `bedrooms` | string | no | any | Match listings with at least one floor plan of this bedroom count. |
| `bathrooms` | string | no | any | Match listings with a floor plan at or above this bathroom count. |
| `priceMin` | integer | no |  | Lowest monthly rent to include. Leave unset for no minimum. |
| `priceMax` | integer | no |  | Highest monthly rent to include. Leave unset for no maximum. |
| `sqftMin` | integer | no |  | Smallest floor plan to include. Leave unset for no minimum. |
| `sqftMax` | integer | no |  | Largest floor plan to include. Leave unset for no maximum. |
| `propertyType` | string | no | any | Restrict results to one property type. |
| `petPolicy` | string | no | any | Require listings that allow dogs, cats, or both. |
| `amenities` | array | no | [] | Only return listings that publish every selected amenity. |
| `rentSpecials` | boolean | no | false | Only return listings advertising a current move-in deal. |
| `minRating` | string | no | any | Only return listings rated at or above this score (1–5). |
| `moveInDate` | string | no |  | Only return listings with a unit available on or before this date (YYYY-MM-DD). |

9 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "searchLocation": "New York, NY",
  "maxItems": 25,
  "maxPages": 1
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~apartments-com-rental-listing-and-floor-plan/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~apartments-com-rental-listing-and-floor-plan/runs" \
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
