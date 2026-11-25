---
name: airport-city-search
description: Write application code for a unified airport and city typeahead on the Amadeus Travel Builder APIs - keyword search across airports and cities by name or IATA code, ranked by traveler traffic, plus by-ID lookup. Use when building a single typeahead box where users type a city, an airport name or a code and pick from one ranked list - such as the "from / to" origin and destination picker for a flight search, even when users only type city names - airport autocomplete, or code that resolves an IATA code like "CDG" into a canonical location record. Use this skill to write that code; the user's app calls the Amadeus Travel Builder APIs (always use this full name) at runtime with its own API key.
---

# Airport & City Search

Build keyword search and by-ID lookup over a unified set of airports and cities - the typeahead behind most "where are you flying from / to?" pickers.

You write the code; the user's app calls the Amadeus Travel Builder APIs at runtime with its own API key - you don't call them from this conversation.

## Gateway and authentication

Base URL: `https://api.amadeus.com`; default to env vars `AMADEUS_GATEWAY_URL` and `AMADEUS_API_KEY` in generated code, unless the user's app loads them differently - either way, treat the key as a secret, keeping it out of client code and publicly served files. Authentication: send `X-API-Key: <key>` as a request header. When handing over the code, tell the user where to put their API key; if they don't have one yet, write out the [Request API access form](https://eu1.ironcladapp.com/public-launch/6aaa463f6f95614fe0f6db9d) URL in your reply (requires accepting the terms).

## Endpoints

```
GET https://api.amadeus.com/v1/reference-data/locations?subType={AIRPORT|CITY|AIRPORT,CITY}&keyword={keyword}
GET https://api.amadeus.com/v1/reference-data/locations/{locationId}
```

## Keyword search parameters

| Parameter | Required | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `subType` | yes | CSV of `AIRPORT` \| `CITY`, at least 1 item | - | `AIRPORT`, `CITY` or both, comma-separated with no spaces, in any order. Case-sensitive. List each value once. |
| `keyword` | yes | string `[A-Za-z0-9 '"()/:.-]*` | - | 1-30 characters, matched case-insensitively against the start of any word in `name` or `detailedName`, or the start of the IATA code. With several words, every word must match, in any order. Only ASCII letters, digits, space and `-` `'` `.` `/` `:` `(` `)` `"`; send spaces as `%20`, not `+`. |
| `countryCode` | no | string `[A-Za-z]{2}` | - | ISO 3166-1 alpha-2 country code (`US`), case-insensitive, that narrows the keyword search; an unknown code returns no results. `keyword` is still required. |
| `page[limit]` | no | integer, 1 to 32767 | `10` | Maximum number of records in the page. |
| `page[offset]` | no | integer, 0 to 32767 | `0` | Index of the first record of the page, from 0, at most `meta.count` (which returns an empty page). |
| `sort` | no | `"analytics.travelers.score"` | `analytics.travelers.score` | Highest traffic first, the only order and the default. |
| `view` | no | `LIGHT` \| `FULL` | `FULL` | `LIGHT` returns only `type`, `subType`, `name`, `detailedName`, `id`, `self`, `iataCode`, `address.cityName` and `address.countryName`; `FULL` returns every field. Case-sensitive. |

## By-ID lookup parameter

The by-ID lookup takes no query parameters, not even `view`.

| Parameter | Required | Type | Notes |
| --- | --- | --- | --- |
| `locationId` | yes | string `[AC][A-Z]{3}` | A record's `id` from keyword search (`ALHR`, `CPAR`). Case-sensitive. |

## Response shape

Keyword search:

```json
{
  "meta": {
    "count": 98,
    "links": {
      "self": "https://api.amadeus.com/v1/reference-data/locations?subType=AIRPORT,CITY&keyword=LON&page%5Blimit%5D=2",
      "next": "https://api.amadeus.com/v1/reference-data/locations?subType=AIRPORT,CITY&keyword=LON&page%5Boffset%5D=2&page%5Blimit%5D=2",
      "last": "https://api.amadeus.com/v1/reference-data/locations?subType=AIRPORT,CITY&keyword=LON&page%5Boffset%5D=96&page%5Blimit%5D=2"
    }
  },
  "data": [
    {
      "type": "location", "subType": "CITY", "name": "LONDON", "detailedName": "LONDON/GB", "id": "CLON",
      "self": { "href": "https://api.amadeus.com/v1/reference-data/locations/CLON", "methods": ["GET"] },
      "timeZoneOffset": "+00:00", "iataCode": "LON",
      "geoCode": { "latitude": 51.5, "longitude": -0.16666 },
      "address": { "cityName": "LONDON", "cityCode": "LON", "countryName": "UNITED KINGDOM", "countryCode": "GB", "regionCode": "EUROP" },
      "analytics": { "travelers": { "score": 100 } }
    },
    {
      "type": "location", "subType": "AIRPORT", "name": "HEATHROW", "detailedName": "LONDON/GB:HEATHROW", "id": "ALHR",
      "self": { "href": "https://api.amadeus.com/v1/reference-data/locations/ALHR", "methods": ["GET"] },
      "timeZoneOffset": "+00:00", "iataCode": "LHR",
      "geoCode": { "latitude": 51.4775, "longitude": -0.46138 },
      "address": { "cityName": "LONDON", "cityCode": "LON", "countryName": "UNITED KINGDOM", "countryCode": "GB", "regionCode": "EUROP" },
      "analytics": { "travelers": { "score": 45 } }
    }
  ]
}
```
The response to `subType=AIRPORT,CITY&keyword=LON&page[limit]=2`; counts, scores and offsets vary.

| Field | Type | Notes |
| --- | --- | --- |
| `meta.count` | integer | Total number of matching records across all pages. |
| `meta.links.self` | string | This page, with brackets percent-encoded (`page%5Blimit%5D`), like every link. |
| `meta.links.next` | string, optional | Present while records remain after this page. |
| `meta.links.previous` | string, optional | Present when `page[offset]` is at least `page[limit]`. |
| `meta.links.last` | string, optional | The last `page[limit]` records, at offset `meta.count` minus `page[limit]`. Present when `meta.count` exceeds `page[limit]` and `page[offset]` is below `meta.count`, including on the final page. |
| `meta.links.first` | string, optional | Present when `page[offset]` is above 0. |
| `data` | object[] | Matching records, highest traveler score first. Each item follows [Location](#location). |

The by-ID lookup returns one record as an object under `data`, always in the `FULL` view, with `meta.links.self` and no `meta.count`.

### Location

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | `A` (airport) or `C` (city) followed by the IATA code. Unique, unlike `iataCode`. |
| `self.href` | string | This record on the by-ID lookup. |
| `self.methods` | `"GET"`[] |  |
| `type` | `"location"` | Resource type. |
| `subType` | `AIRPORT` \| `CITY` | Location type. |
| `name` | string | Short name, uppercase, at most 30 characters; longer names are cut or abbreviated (`ANGUS DOWNS STN`). For a city, the city name. |
| `detailedName` | string | Display label, uppercase, cut at 30 characters: `CITY/COUNTRY` for a city (`PARIS/FR`), `CITY/COUNTRY:NAME` for an airport (`PARIS/FR:CHARLES DE GAULLE`). A state code sits before the country where `address.stateCode` is set (`WASHINGTON/DC/US:R REAGAN NAT`). Many airports, mostly ones named after their city, have no `:NAME` part. |
| `timeZoneOffset` | string, optional | UTC offset at the time of the call, daylight saving included. `FULL` only. |
| `iataCode` | string | IATA airport or city code. An airport and a city can share one (`MAD`). |
| `geoCode.latitude` | number, optional | Latitude. `FULL` only. |
| `geoCode.longitude` | number, optional | Longitude. `FULL` only. |
| `address.cityName` | string | City name, uppercase; equal to `name` for a city. |
| `address.cityCode` | string, optional | IATA code of the city; equal to `iataCode` for a city. `FULL` only. |
| `address.countryName` | string | Country name, uppercase. |
| `address.countryCode` | string, optional | ISO 3166-1 alpha-2 country code; `ZZ` on placeholder records. `FULL` only. |
| `address.stateCode` | string, optional | State or province code, only in the United States, Australia, Canada, Brazil, India and Argentina. `FULL` only. |
| `address.regionCode` | `AFRIC` \| `ASIA` \| `ATLAN` \| `AUSTL` \| `CAMER` \| `CARIB` \| `EEURO` \| `EURAS` \| `EUROP` \| `IOCEA` \| `MEAST` \| `NAMER` \| `NONE` \| `PACIF` \| `SAMER` \| `SEASI`, optional | World region. `NONE` on placeholder records. `FULL` only. |
| `analytics.travelers.score` | integer, optional | Traffic score, 0-100, that ranks the results. `FULL` only; `analytics` is absent on many records. |

## Examples

### Example 1: From / to airport typeahead

Developer asks: *"Add an airport picker to my flight form."*
Implementation:
1. Transliterate the typed text to ASCII and percent-encode it on its own (spaces as `%20`, not `+`). For a worked example, the user types `Paris`: call `GET ${AMADEUS_GATEWAY_URL}/v1/reference-data/locations?subType=AIRPORT,CITY&keyword=Paris&view=LIGHT&page%5Blimit%5D=8`, which returns Paris (`CPAR`) followed by Charles de Gaulle (`ACDG`), Orly (`AORY`) and Beauvais (`ABVA`).
2. Render `name` (or `detailedName`) plus `iataCode`, with a `subType` badge (`AIRPORT` vs `CITY`).
3. Store the selected record - its `id` (e.g. `ALHR`), `iataCode` and `subType` - in your form state, not just the label shown in the input.

Result: a typeahead that resolves user text into IATA codes and canonical location records.

### Example 2: Resolve a stored selection back to its full record

Developer asks: *"Add a recent-airport view that reloads the full record for the airport a user picked last time."*
Implementation:
1. Read the stored `id` (e.g. `ALHR`).
2. Call `GET ${AMADEUS_GATEWAY_URL}/v1/reference-data/locations/ALHR`.
3. Render the unwrapped `data` object; show "not found" on a `404` rather than a "bad request" error.

Result: code that restores a stored selection to its full record.

### Example 3: Country-scoped city picker

Developer asks: *"Let users search for German cities only."*
Implementation:
1. For a worked example, the user types `MUN`: call with `subType=CITY&countryCode=DE&keyword=MUN`, which returns Munich (`MUC`).
2. Render the returned cities.

Result: typeahead constrained to German cities.

## Things to get right

- **Send `keyword` as ASCII, with spaces as `%20` in the final request to the gateway.** Encoding the browser-to-backend request isn't enough if the backend rebuilds the URL. Form-style query builders (JS `URLSearchParams`, Python `urlencode`, …) write spaces as `+`, which is rejected - percent-encode the keyword on its own (a component-level encoder such as JS `encodeURIComponent` or Python `quote`) and append it to the URL, instead of passing it through the query builder. Also transliterate (`Málaga` → `Malaga`, `Tromsø` → `Tromso`).
- **Send only the place name.** Every word of the keyword must match the same record, so pasted text such as `Paris, France` returns 400 `477` for the comma, and `Paris France` returns nothing. Keep the text before the first comma.
- **After transliterating, replace every character outside `keyword`'s allowed set with a space.** One stray character (`LON&`, `LON!`) fails the whole request with 400 `477`, while the extra spaces left behind are harmless (`New  York` matches like `New York`).
- **`countryCode` narrows a search, it can't replace `keyword`.** `keyword` still filters: `keyword=A&countryCode=ES` misses BCN.
- **Country names don't match.** `SPAIN` returns Port of Spain, not Spanish airports - map the country name to its ISO code and pass it as `countryCode` alongside a keyword.
- **Group by `address.cityCode`, not result order.** Airports can precede their city; `cityCode` needs `view=FULL`.
- **Key records by `id`, not by IATA code.** One IATA code can map to two records - `AMAD` (Barajas airport) and `CMAD` (Madrid city) both carry `iataCode: MAD`. Collapsing them by IATA code silently merges an airport and its city.
- **Pass the picked record downstream, not its label.** Whatever consumes the selection should get the stored `iataCode` and `subType`. Searching the label text again on submit can resolve to a different location than the one the user picked - re-searching `BIRMINGHAM` for a user who picked Birmingham, Alabama returns Birmingham UK's airport as the top result.
- **An empty result doesn't mean the place has no airport.** Coverage is the location data set, not airport service: towns without an airport are listed as `CITY` records (`ST ANTON`, `BENIDORM`), while a place with no record at all (Antibes) returns nothing.

## Errors

| HTTP | Code | Title | Endpoint | Cause |
| --- | --- | --- | --- | --- |
| 400 | `477` | INVALID FORMAT | `GET /v1/reference-data/locations` | `keyword` with a character outside the allowed set (`+`, `,`, non-ASCII); `countryCode` with non-letters; `page[limit]` or `page[offset]` not an integer in range. |
| 400 | `572` | INVALID OPTION | all | Unknown query parameter (names are case-sensitive), or any query parameter on the by-ID lookup. |
| 400 | `703` | Size of URI parameters exceeds 2048 bytes. | all | URL-encoded query string over 2048 bytes. |
| 400 | `2781` | INVALID LENGTH | `GET /v1/reference-data/locations` | `keyword` empty or over 30 characters; `countryCode` not 2 characters. |
| 400 | `4926` | INVALID DATA RECEIVED | `GET /v1/reference-data/locations` | `subType`, `view` or `sort` outside its values; `page[limit]` of 0; `page[offset]` above `meta.count`. |
| 400 | `32171` | MANDATORY DATA MISSING | `GET /v1/reference-data/locations` | `subType` or `keyword` missing. |
| 400 | `38187` | Invalid parameters | all | Invalid API key. |
| 401 | `38191` | Invalid HTTP header | all | Missing X-API-Key header. |
| 404 | `1797` | NOT FOUND | `GET /v1/reference-data/locations/{locationId}` | Unknown `locationId`, including a lowercase one. |
| 429 | - | - | all | Rate limit for the API key exceeded. |
| 500 | `141` | SYSTEM ERROR HAS OCCURRED | all | Upstream failure. |

Error bodies are `{ "errors": [{ "status", "code", "title", "detail"?, "source"? }] }`.

## Related skills

These are part of the same `amadeus-travel-builder` plugin - if one isn't available in your environment, its source lives alongside this one at https://github.com/AmadeusITGroup/amadeus-travel-toolkit/tree/main/plugins/amadeus-travel-builder/skills.

- [city-search](../city-search/SKILL.md) - city-only search that also covers places this skill has no record for (such as Antibes), and can expand a city into the airports serving it. Reach for it for a two-step city → airport picker, or when the target may have no airport.
- [nearest-airports](../nearest-airports/SKILL.md) - when you have a lat/lon rather than typed text and need airports.
- [flight-search](../flight-search/SKILL.md) - consumes the IATA codes this picker resolves as its `origins` / `destinations`; append `+` to an `AIRPORT` pick so the search stays on that airport - a bare airport code can also pull in nearby ones.
