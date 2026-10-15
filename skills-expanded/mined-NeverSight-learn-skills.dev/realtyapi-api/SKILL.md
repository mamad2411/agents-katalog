---
name: realtyapi-api
description: >-
  Fetch real estate data from 30+ property portals worldwide using the RealtyAPI
  REST API. Covers Redfin, Realtor.com, Zillow, Trulia, Homes.com, Apartments.com,
  HotPads, Auction.com, StreetEasy (US), Centris (Canada), Rightmove, Zoopla (UK),
  Idealista, SeLoger, Immobiliare, Immowelt, ImmoScout24, Funda, Otodom, Cian
  (Europe), Bayut, Dubizzle, Property Finder (Middle East), 99.co (Asia),
  Domain, Flatmates (Australia), and Airbnb, Vrbo, Agoda, Trip.com, Tripadvisor
  (short-term/vacation). Use when the user asks to look up, search, fetch, or
  extract property listings, home/rental details, price or tax history,
  valuations and estimates, comparables, market and rent trends, agents,
  foreclosures/auctions, or any real estate data for an address, area, or portal.
  Also use when the user mentions RealtyAPI, a real estate API, MLS data, or a
  specific property portal.
allowed-tools: Bash, Read, Write, WebFetch
homepage: https://www.realtyapi.io
repository: https://github.com/realtyapi/realtyapi-skills
license: MIT
metadata:
  openclaw:
    emoji: "🏠"
    requires:
      env:
        - REALTYAPI_API_KEY
    primaryEnv: REALTYAPI_API_KEY
    homepage: https://www.realtyapi.io
    tags:
      - real-estate
      - property
      - listings
      - rentals
      - redfin
      - realtor
      - zillow
      - rightmove
      - zoopla
      - airbnb
      - market-data
      - valuations
      - comps
      - agents
      - realtyapi
---

# RealtyAPI

Fetch real estate data from **30+ property portals worldwide** through one REST API
and one API key — listings, property and rental details, price/tax history,
valuations, comparables, market trends, and agents, across the US, Canada, UK,
Europe, the Middle East, Asia, and Australia (~400 endpoints).

**Get an API key:** https://www.realtyapi.io — pass it in the `x-realtyapi-key` header.

## How to Call

Every provider has its own subdomain. The base URL is `https://<provider>.realtyapi.io`
and you append the endpoint path. All endpoints are JSON; most are `GET`.

```bash
curl -s "https://redfin.realtyapi.io/detailsbyaddress" \
  -H "x-realtyapi-key: $REALTYAPI_API_KEY" \
  --data-urlencode "property_address=166 W 22nd St Unit 1D, New York, NY 10011" -G
```

Or with `fetch`:

```javascript
const url = new URL("https://redfin.realtyapi.io/detailsbyaddress");
url.searchParams.set("property_address", "166 W 22nd St Unit 1D, New York, NY 10011");
const res = await fetch(url, {
  headers: { "x-realtyapi-key": process.env.REALTYAPI_API_KEY },
});
const data = await res.json();
```

Without a valid key every data endpoint returns `401`.

## Endpoint Discovery (do this first)

**Do not guess endpoint paths or parameters.** There are ~400 endpoints, so route
in two cheap, keyless steps before spending a request credit:

1. **Find the endpoint** — fetch the full machine-readable index and search it for
   the provider + capability you need:

   ```
   https://www.realtyapi.io/llms.txt
   ```

   It lists every provider, its base URL, and every endpoint as
   `- [Name](docpage): `METHOD /path``. Pick the provider and endpoint that match
   the user's intent (use the **Provider Catalog** and **Intent Routing** below to
   narrow down).

2. **Get the exact parameters** — fetch that provider's OpenAPI 3.1 spec (public,
   **no key required**) for parameter names, types, requiredness, and an example
   response:

   ```
   https://<provider>.realtyapi.io/openapi.json
   ```

   e.g. `https://redfin.realtyapi.io/openapi.json`. Read the spec for the chosen
   path, then make the real call. This avoids 400s from wrong/misspelled params.

Both `llms.txt` and `openapi.json` are free to fetch and do not consume credits.

## Provider Catalog

Pick by **region** and **data type**. Sale + rental unless noted.

| Region | Providers (subdomain) | Notes |
|--------|----------------------|-------|
| 🇺🇸 US | `redfin`, `realtor`, `zillow`, `trulia`, `homes` | Listings, full property details, price/tax history, valuations, market trends, agents |
| 🇺🇸 US rentals | `apartments`, `hotpads` | Apartment & rental listings |
| 🇺🇸 US niche | `streeteasy` (NYC), `auction` (foreclosures/auctions) | |
| 🇨🇦 Canada | `centris` | Quebec/Canada listings |
| 🇬🇧 UK | `rightmove`, `zoopla` | Listings, sold prices, estimates, market data |
| 🇪🇺 Europe | `idealista` (ES/IT/PT), `seloger` (FR), `immobiliare` (IT), `immowelt` (DE), `immoscout` (DE), `funda` (NL), `otodom` (PL), `cian` (RU) | |
| 🕌 Middle East | `bayut`, `dubizzle`, `propertyfinder` (UAE/GCC) | |
| 🌏 Asia | `99co` (Singapore) | |
| 🇦🇺 Australia | `domain`, `flatmates` (shared housing) | |
| 🏖️ Short-term / vacation | `airbnb`, `vrbo`, `agoda`, `trip`, `tripadvisor` | Stays, hotels, travel |

> The catalog changes as portals are added. `llms.txt` is the source of truth — if a
> provider or endpoint isn't there, it isn't live.

## Intent Routing

Map the user's goal to the right kind of endpoint, then confirm the exact path/params
via `llms.txt` + the provider `openapi.json`.

| User wants… | Endpoint pattern (typical names) | Notes |
|-------------|----------------------------------|-------|
| Full details for one property | `…byaddress` / `…byurl` / `…detailsbyaddress` / `…by-zpid` | Pass the street address or the portal listing URL |
| Search listings in an area | `search/byaddress`, `search/bycoordinates`, `search/bypolygon`, `search/bymapbounds` | Supports filters: price, beds, baths, home type, status (for-sale/sold/rent) |
| Autocomplete / resolve a place or address | `autocomplete`, `locations` | Use first to get IDs/slugs other endpoints need |
| Price / tax / sold history | `pricehistory`, `taxinfo*`, `sold-prices` | |
| Valuation / estimate | `zestimate*`, `estimates`, graph/chart endpoints | "How much is it worth" |
| Comparables (comps) | `comparable_homes`, `similar*`, `nearby*` | Pair with valuation for a CMA |
| Market / rent trends | `housing_market`, `rental_market*`, `market*`, `housingMarketTrends` | Area-level analytics |
| Schools / climate / walkability | `schools`, `climate`, `walk_transit_bike` | Context for a listing |
| Find / evaluate an agent | `agent/search`, `agentInfo`, `agentdetails`, `agentreviews` | |
| Rentals (long-term) | `apartments`, `hotpads`, `zillow` rentals, regional portals | |
| Short-term / vacation stays | `airbnb`, `vrbo`, `agoda`, `trip` search + details | |
| Foreclosures / auctions | `auction` search + details | Investment use cases |

## Credit Costs

- **Most endpoints cost 1 request credit** per successful call.
- A small number of heavier endpoints cost more (e.g. 2× or 6×). The exact cost is
  shown per endpoint in the dashboard playground and on each endpoint's doc page.
  **Warn the user before calling an endpoint that costs more than 1 credit**, and
  before running a loop that makes many calls.
- See https://www.realtyapi.io/docs/api-credits for how credits work.

## Pagination

Search and list endpoints are paginated. The convention varies by endpoint —
**check the `openapi.json` parameters**:

| Param | Meaning |
|-------|---------|
| `page` | Most common — 1-based page number (often with `pageSize` / `resultCount` / `hitsPerPage`) |
| `nextPageCursor` | Cursor returned in the response; pass it back for the next page |
| `offset` / `limit` | Offset-based windows on some endpoints |

To gather many results, increment `page` (or follow `nextPageCursor`) until the
results run out — and respect credit cost, since each page is a separate request.

## Conventions & Tips

- **Two ways to identify a property:** a street address (e.g. `property_address`,
  `address`, `propertyaddress`) or the portal's listing URL (`url`). Prefer the URL
  when the user pastes one; otherwise use the address.
- **Resolve first when needed:** some endpoints need an internal id (ZPID, listing id,
  location slug). Use the provider's `autocomplete` / `locations` endpoint to get it.
- **Match the portal to the country.** A UK address won't resolve on a US portal —
  route Spain to `idealista`, France to `seloger`, UAE to `propertyfinder`, etc.
- **Status filters** distinguish for-sale vs sold vs for-rent — set them explicitly
  when the user's intent is specific.
- **Handle errors:** `401` = missing/invalid key; `400` = bad/missing params (re-read
  the `openapi.json`); `404` = property/listing not found or not yet indexed.
- **Cite sources.** Include the portal listing URL (and the RealtyAPI doc page) in
  outputs so results are verifiable.

## Known Limitations

- Coverage is per-portal and public-data only — a field present on one portal may be
  absent on another. Cross-reference portals when a value is critical.
- A portal indexes its own market; there is no single global search. To compare
  across portals, query each relevant portal and merge results yourself.
- Newly listed or off-market properties may not be indexed yet (`404`).
- `llms.txt` and the per-provider `openapi.json` always reflect the live endpoint set;
  trust them over any hardcoded list, including this one.
