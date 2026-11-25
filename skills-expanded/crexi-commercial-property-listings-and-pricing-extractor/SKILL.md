---
name: crexi-commercial-property-listings-and-pricing-extractor
description: "Collects active commercial real estate listings from Crexi across any US state and 14 property types, with asking price, square footage, location, and brokerage details. Output fields: name, transaction_type, property_type, price, net_operating_income and more, as JSON rows. Use it for requests like \"Crexi commercial property listings scraper\", or a CSV/JSON export of public Crexi data."
---

# Crexi Commercial Property Listings & Pricing Extractor

Collects active commercial real estate listings from Crexi across any US state and 14 property types, with asking price, square footage, location, and brokerage details.

- Actor: https://apify.com/dataspryva/crexi-commercial-property-listings-and-pricing (ID `dataspryva~crexi-commercial-property-listings-and-pricing`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/crexi-commercial-property-listings-and-pricing-extractor.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Crexi commercial property listings scraper
- a repeatable export of public Crexi data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `name`: Property Name
- `transaction_type`: Kind
- `property_type`: Type
- `city`: City
- `state`: State
- `price`: Price
- `cap_rate`: Cap Rate %
- `net_operating_income`: NOI
- `building_sqft`: Building SqFt
- `broker_names`: Brokers
- `property_url`: URL

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `propertyUrls` | array | no | [] | Paste Crexi property links or IDs (e.g. `https://www.crexi.com/properties/123456/name,` /lease/properties/987/name, a bare ID, or a property-record link) to fetch those exact… |
| `transactionTypes` | array | no | [] | Which Crexi marketplaces to search. Empty = for-sale listings only. |
| `searchTerms` | array | no | [] | Free-text keywords matched against listing names, descriptions and addresses (e.g. warehouse, medical office). |
| `propertyTypes` | array | no | [] | One or more commercial property categories. Empty searches every type. |
| `subtypes` | array | no | [] | Narrow to specific subtypes (e.g. Shopping Center, Medical Office, Warehouse). Note: some subtypes exist only for sale or only for lease listings. |
| `locations` | array | no | [] | US states to search, by two-letter code or full name. Each state is searched and combined. Empty searches nationwide. |
| `cities` | array | no | [] | City names to filter by (e.g. Austin). Works alongside or instead of states. |
| `counties` | array | no | [] | County names to filter by, including the word County where Crexi uses it (e.g. Travis County). |
| `zipCodes` | array | no | [] | US ZIP codes to filter by (e.g. 78701). |
| `minPrice` | integer | no |  | Only return listings asking at least this much. Sale and auction listings only. |
| `maxPrice` | integer | no |  | Only return listings asking at most this much. Sale and auction listings only. |
| `minPricePerSqft` | number | no |  | Only return sale listings priced at or above this per square foot. |
| `maxPricePerSqft` | number | no |  | Only return sale listings priced at or below this per square foot. |
| `minCapRate` | number | no |  | Only return sale listings with a published cap rate at or above this percentage. |

13 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "maxProperties": 5
}
```

The input passes the Actor's input schema (checked at every publish). The run size follows the number of inputs you pass.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~crexi-commercial-property-listings-and-pricing/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~crexi-commercial-property-listings-and-pricing/runs" \
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
