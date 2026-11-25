---
name: google-flights-fare-and-itinerary-filter-scraper
description: "Search Google Flights for one-way or round-trip fares across any cabin class, then narrow results by stops, total duration, airline, and price range, with an optional price-alert flag. Output fields: price, airline, departureAirport, departureTime, arrivalAirport and more, as JSON rows. Use it for requests like \"Google Flights fare scraper\", or a CSV/JSON export of public Google Flights data."
---

# Google Flights Fare & Itinerary Filter Scraper

Search Google Flights for one-way or round-trip fares across any cabin class, then narrow results by stops, total duration, airline, and price range, with an optional price-alert flag.

- Actor: https://apify.com/vexaloom-labs/google-flights-fare-and-itinerary-filter-scraper (ID `vexaloom-labs~google-flights-fare-and-itinerary-filter-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/google-flights-fare-and-itinerary-filter-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Compare flight fares before Monday's booking brief](https://www.youtube.com/shorts/ntNLhXTe4VE)

## When to use

Use this skill when the user wants:

- Google Flights fare scraper
- a repeatable export of public Google Flights data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `price`: Price
- `currency`: Currency
- `airline`: Airline
- `departureAirport`: Departure Airport
- `departureTime`: Departure Time
- `arrivalAirport`: Arrival Airport
- `arrivalTime`: Arrival Time
- `durationMinutes`: Duration Minutes
- `stops`: Stops
- `emissionsGrams`: Emissions Grams
- `bookingUrl`: Booking Url

All 12 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | Search flights, or collect the cheapest fare for each date around your departure date. |
| `originAirport` | string | no | JFK | Three-letter IATA airport or city code, e.g. JFK, LHR, NYC. One code per search; use `searches` for alternate airports. |
| `destinationAirport` | string | no | LHR | Three-letter IATA airport or city code, e.g. LHR, HND, LON. One code per search; use `searches` for alternate airports. |
| `outboundDate` | string | no |  | Departure date in YYYY-MM-DD format. Leave empty to use 30 days from today (UTC); the chosen date is logged. |
| `returnDate` | string | no |  | Return date in YYYY-MM-DD format. Leave empty for a one-way search. |
| `adults` | integer | no | 1 | Travellers aged 12 and over (1-9). |
| `children` | integer | no | 0 | Travellers aged 2-11 (0-8). |
| `infants` | integer | no | 0 | Infants under 2 travelling on an adult lap (0-8). Cannot exceed the number of adults. |
| `infantsInSeat` | integer | no | 0 | Infants under 2 travelling in their own seat (0-8). |
| `cabinClass` | string | no | economy | Cabin to search. |
| `currency` | string | no | USD | Currency for every price. |
| `language` | string | no | en | Language Google Flights uses for airport and airline names. |
| `country` | string | no | US | Country whose fares and availability Google should show. |
| `maxStops` | string | no | any | Largest number of stops allowed on any leg. |

16 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "outboundDate": "2026-12-10",
  "maxResults": 25,
  "includePriceInsights": false,
  "priceGraphDays": 1,
  "mode": "search"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxResults` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~google-flights-fare-and-itinerary-filter-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~google-flights-fare-and-itinerary-filter-scraper/runs" \
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
