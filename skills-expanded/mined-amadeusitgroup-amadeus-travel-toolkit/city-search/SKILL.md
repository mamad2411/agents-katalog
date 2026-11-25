---
name: city-search
description: Write application code that calls the Amadeus Travel Builder APIs to match a typed city keyword (optionally scoped to a country) to cities with their coordinates, their IATA city code when they have one, and, on request, the airports that serve each city - including cities that have no airport of their own (e.g. Antibes, resort/rural towns). Use when building a city autocomplete or country-scoped city lookup for destination guides, hotels or activities, code that resolves a typed city name like "Paris" or "Lyon" into its coordinates for a location-based search, or a two-step city → airport picker where the user chooses a city and then one of the airports serving it. When the app needs cities regardless of airport coverage, this is the skill. Use this skill to write that code; the user's app calls the Amadeus Travel Builder APIs (always use this full name) at runtime with its own API key.
---

# City Search

Build city search by keyword into an app. A user types part of a city name - optionally scoped to a country - and your app gets back matching cities with their coordinates and, when they have one, their IATA city code. Ask for `include=AIRPORTS` and each city with airports also links to the airports that serve it.

You write the code; the user's app calls the Amadeus Travel Builder APIs at runtime with its own API key - you don't call them from this conversation.

## Gateway and authentication

Base URL: `https://api.amadeus.com`; default to env vars `AMADEUS_GATEWAY_URL` and `AMADEUS_API_KEY` in generated code, unless the user's app loads them differently - either way, treat the key as a secret, keeping it out of client code and publicly served files. Authentication: send `X-API-Key: <key>` as a request header. When handing over the code, tell the user where to put their API key; if they don't have one yet, write out the [Request API access form](https://eu1.ironcladapp.com/public-launch/6aaa463f6f95614fe0f6db9d) URL in your reply (requires accepting the terms).

## Endpoint

```
GET https://api.amadeus.com/v1/reference-data/locations/cities?keyword=PARIS&countryCode=FR&include=AIRPORTS
```

The keyword and country are illustrations of runtime input.

## Parameters

| Parameter | Required | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `countryCode` | no | string `[A-Za-z]{2}` | - | ISO 3166-1 alpha-2 country code, e.g. `FR`; restricts results to that country. Case-insensitive. An unknown code returns no cities. |
| `keyword` | yes | string ` *[A-Za-z][A-Za-z ]{1,48}[A-Za-z] *` | - | Case-insensitive substring of the city name, matched anywhere in it, e.g. `PARIS`, `LYO`. 3-50 characters, not counting leading and trailing spaces. Send ASCII letters and spaces: other characters return an error, except non-ASCII letters, which are accepted but match only the few names stored with them. Spaces are matched literally, leading and trailing ones included. |
| `max` | no | integer | `1000` | Maximum number of cities returned, 1-1000. An integer outside that range is ignored and the default applies. |
| `include` | no | CSV of `"AIRPORTS"`, at least 1 item | - | `AIRPORTS` adds `relationships` to each city with airports and a top-level `included.airports` map. Case-sensitive. |

## Response shape

```json
{
  "meta": { "count": 8, "links": { "self": "https://api.amadeus.com/v1/reference-data/locations/cities?countryCode=FR&include=AIRPORTS&keyword=PARIS&max=1000" } },
  "data": [
    {
      "type": "location",
      "subType": "city",
      "name": "Paris",
      "iataCode": "PAR",
      "address": { "countryCode": "FR", "stateCode": "FR-75" },
      "geoCode": { "latitude": 48.85341, "longitude": 2.3488 },
      "relationships": [
        { "id": "BVA", "type": "Airport", "href": "#/included/airports/BVA" },
        { "id": "CDG", "type": "Airport", "href": "#/included/airports/CDG" },
        { "id": "ORY", "type": "Airport", "href": "#/included/airports/ORY" },
        { "id": "XCR", "type": "Airport", "href": "#/included/airports/XCR" }
      ]
    }
  ],
  "included": {
    "airports": {
      "BVA": { "subType": "Airport", "name": "Beauvais-Tille", "iataCode": "BVA", "address": { "countryCode": "FR", "stateCode": "FR-75" }, "geoCode": { "latitude": 49.45444, "longitude": 2.11278 } },
      "CDG": { "subType": "Airport", "name": "Charles de Gaulle", "iataCode": "CDG", "address": { "countryCode": "FR", "stateCode": "FR-75" }, "geoCode": { "latitude": 49.01278, "longitude": 2.55 } },
      "ORY": { "subType": "Airport", "name": "Orly", "iataCode": "ORY", "address": { "countryCode": "FR", "stateCode": "FR-75" }, "geoCode": { "latitude": 48.72528, "longitude": 2.35944 } },
      "XCR": { "subType": "Airport", "name": "Chalons-Vatry", "iataCode": "XCR", "address": { "countryCode": "FR", "stateCode": "FR-75" }, "geoCode": { "latitude": 48.77611, "longitude": 4.18444 } }
    }
  }
}
```
The response to the request above, trimmed to the first of its 8 cities and that city's airports; the count changes as the data does.

API responses are `application/vnd.amadeus+json` whatever `Accept` you send (requesting `application/json` is fine); the gateway's authentication errors are `application/json`. Parse the body as JSON in both cases.

| Field | Type | Notes |
| --- | --- | --- |
| `warnings` | object[], optional | Non-fatal notices, sent with HTTP 200. Each item follows [Warning](#warning). |
| `meta.links.self` | string | The request URL, parameters in alphabetical order and `max` included. |
| `meta.count` | integer | Number of cities in `data`, not the total number of matches. |
| `data` | object[], optional | Matching cities, at most `max`. Absent when nothing matches. Each item follows [City](#city). |
| `included.airports` | map of string → object, optional | Only with `include=AIRPORTS`: every airport linked from a city in `data`, keyed by IATA airport code - one pool for the whole response, not per city. Each value follows [Airport](#airport). |

### City

| Field | Type | Notes |
| --- | --- | --- |
| `type` | `"location"` |  |
| `subType` | `"city"` |  |
| `name` | string | Mixed case, keeping hyphens (`Saint-Malo`). |
| `iataCode` | string, optional | IATA city code, e.g. `PAR`. Absent (not null) on most cities; a code doesn't imply an airport. A few coded records without coordinates carry a malformed code (`GN)`). |
| `address.countryCode` | string | ISO 3166-1 alpha-2 country code, uppercase. |
| `address.stateCode` | string, optional | `{countryCode}-{subdivision}`, e.g. `FR-75`, `US-IL`; `{countryCode}-ZZZ` when the subdivision is unknown. |
| `geoCode.latitude` | number, optional |  |
| `geoCode.longitude` | number, optional |  |
| `relationships` | object[], optional | Airports serving the city, only with `include=AIRPORTS`; absent when the city has none. Each item follows [Relationship](#relationship). |

### Relationship

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | IATA airport code; the airport's key in `included.airports`. |
| `type` | `"Airport"` |  |
| `href` | string | Reference into `included.airports`, e.g. `#/included/airports/CDG`. |

### Airport

| Field | Type | Notes |
| --- | --- | --- |
| `subType` | `"Airport"` |  |
| `name` | string |  |
| `iataCode` | string | IATA airport code; also the airport's key in `included.airports`. |
| `address.countryCode` | string | ISO 3166-1 alpha-2 country code, uppercase. |
| `address.stateCode` | string, optional | That of the airport's own IATA city, not its location nor the linking city's: Chalons-Vatry (`XCR`) carries Paris's `FR-75`. |
| `geoCode.latitude` | number |  |
| `geoCode.longitude` | number |  |

### Warning

| Field | Type | Notes |
| --- | --- | --- |
| `code` | integer | `1797`: no city matched. `8200`: 1000 cities returned and more match - narrow with `countryCode` or a longer keyword; sent only when `max` is omitted or ignored. `111`: `max` outside 1-1000, so the default applied. |
| `title` | string | Title of the code. |
| `detail` | string, optional | Human-readable explanation. |
| `source.parameter` | string, optional | The query parameter the warning is about. |
| `status` | `200` |  |

## Examples

### Example 1: Country-scoped city autocomplete

Developer asks: *"Let users search for French cities as they type."*
Implementation:
1. For a worked example, the user types `NIC`: trim and transliterate the input to ASCII and call `GET ${AMADEUS_GATEWAY_URL}/v1/reference-data/locations/cities?keyword=NIC&countryCode=FR&max=10`. Nice (`NCE`) comes back first, followed by towns such as Pornic and Pornichet that have no `iataCode`.
2. Render `name` plus `iataCode` (when present) for each result.
3. Store the selection's `iataCode`, or its `name` and `geoCode` when it has none.

Result: a typeahead constrained to French cities that resolves typed text into a city code or coordinates.

### Example 2: Expand a city into its airports

Developer asks: *"When someone picks a city, let them choose which of its airports to fly from."*
Implementation:
1. For a worked example, Paris: call `GET ${AMADEUS_GATEWAY_URL}/v1/reference-data/locations/cities?keyword=PARIS&countryCode=FR&include=AIRPORTS`.
2. For the chosen city, walk `relationships[]`; for each entry, look up `included.airports[relationship.id]` to get the airport's `name` and `iataCode`.
3. Render the airports - for Paris, Beauvais-Tille (`BVA`), Charles de Gaulle (`CDG`), Orly (`ORY`) and Chalons-Vatry (`XCR`) - as sub-options under the city.

Result: a city → airports drill-down for a flight-origin selector.

### Example 3: Resolve a city name to its IATA code

Developer asks: *"Write code that resolves a typed city name to its IATA city code."*
Implementation:
1. For a worked example, "Lyon": call with `keyword=LYO&countryCode=FR`. Lyon (`LYS`) comes back first, followed by towns such as Sainte-Foy-les-Lyon that have no code.
2. Pick the record whose `name` best matches the input rather than taking `data[0]`, and skip records without an `iataCode`. When several coded records share that `name` and `address.countryCode`, take the one with `geoCode` coordinates - `GRENOBLE` returns `GNO` with coordinates and `GN)` without.
3. Read `iataCode` from the chosen record.

Result: a name → city-code resolver that skips records without a code.

## Things to get right

- **Airports come back cross-referenced, not inline.** Resolve each `relationships[].id` through `included.airports` - the relationship carries only the airport's IATA code, not its `name`, `address` or `geoCode`.
- **`included.airports` is one shared pool for the whole response, not per-city.** When `data` holds several cities (which the substring match makes common), it's the union of every city's airports. Select a city's airports through *its own* `relationships[].id` - rendering the whole map under one city wrongly attributes other cities' airports to it.
- **`keyword` is a substring match.** It matches anywhere in the name, so `PARIS` with `countryCode=FR` returns not just Paris but Le Touquet-Paris-Plage, Villeparisis, Damparis, Parisot and others. Rank/filter by name yourself (prefer exact and word-start matches) rather than assuming `data[0]` is the city the user meant, and scope with `countryCode` to cut noise. IATA codes aren't searched: `CDG` finds nothing.
- **Trim and validate the keyword before sending it.** Spaces are matched literally: a leading space keeps only names with a word before the keyword (` PARIS` finds South Paris, not Paris) and `PARIS ` finds nothing. Check the 3-50-character limit after trimming, transliteration and word selection, since normalization can leave a fragment that's too short.
- **`iataCode` is often absent** - the key is missing, not `null`. If you're resolving a name to a code, skip records without one. In a picker that feeds a location-based search (activities, points of interest), keep them - key the downstream request on `geoCode` or `name` when there's no `iataCode`, since filtering them out drops exactly the airport-less towns this API exists to return.
- **`geoCode` can be an empty object `{}`** - check `geoCode?.latitude` before using coordinates.
- **The same town can come back twice, with complementary halves.** Antibes returns one record with `iataCode: XAT` but empty `geoCode`, and another with coordinates but no `iataCode`. Merge a coded record that has no coordinates into the uncoded record with the same `name` + `address.countryCode` (code from one, coordinates from the other) when there's exactly one such record, rather than listing duplicates or dropping one. When the record with coordinates has its own code, keep it and drop the coordinate-less one: Grenoble comes back as `GNO` with coordinates and `GN)` without, Villefranche-sur-Saone as `VFC` and `XVF`. Halves that spell the name differently (`Bad Homburg vor der Höhe` and `Bad Homburg vor der Hoehe`) can't be matched this way, so they stay separate.
- **No `id` on records, and `name` + `address.countryCode` isn't unique.** The US has many cities named Springfield, told apart by `address.stateCode` and `geoCode`. Key records on `name`, `address.countryCode` and the `geoCode` coordinates (+ `iataCode` when present).
- **Send `keyword` as ASCII letters and spaces.** An accented keyword (`MÁLAGA`) returns the `1797` warning at HTTP 200, not an error - transliterate (`MALAGA` finds Malaga, `AGP`) and percent-encode spaces as `%20`. Stored names keep their hyphens, which the keyword can't contain, so `SAINT MALO` finds nothing - search one word of the name (`MALO`) and match the full name client-side.
- **Cities are stored under their current names.** `BANGALORE` finds nothing; `BENGALURU` returns Bengaluru (`BLR`).
- **No match has no `data` key.** The response is HTTP 200 with `meta.count: 0` and the `1797` warning - read `data` with a default of `[]`.
- **Towns without their own airport can link to the airports serving them.** With `include=AIRPORTS`, the Antibes record with coordinates links to `NCE`; its coded twin (`XAT`) has no `relationships`. A city with no links is a normal case, not an error.

## Errors

| HTTP | Code | Title | Cause |
| --- | --- | --- | --- |
| 400 | `477` | INVALID FORMAT | `keyword` not letters and spaces, `countryCode` not letters, or `max` not an integer (`1.5`, empty, beyond int32). |
| 400 | `572` | INVALID OPTION | Unknown query parameter, or a known one in the wrong case (`Max`). |
| 400 | `703` | Size of URI parameters exceeds 2048 bytes. | URL-encoded query string over 2048 bytes. |
| 400 | `2781` | INVALID LENGTH | `keyword` outside 3-50 characters (outer spaces not counted), or `countryCode` not 2 characters. |
| 400 | `4926` | INVALID DATA RECEIVED | `include` other than `AIRPORTS`, including lowercase or empty. |
| 400 | `32171` | MANDATORY DATA MISSING | `keyword` missing. |
| 400 | `38187` | Invalid parameters | Invalid API key. |
| 401 | `38191` | Invalid HTTP header | Missing X-API-Key header. |
| 429 | - | - | Rate limit for the API key exceeded. |
| 500 | `141` | SYSTEM ERROR HAS OCCURRED | Upstream failure. |

Error bodies are `{ "errors": [...] }`; each entry has `status`, `code` and `title`, and usually `detail` and `source`. `errors` can hold several entries: `Keyword=PARIS` (wrong case) returns `32171` and `572`.

## Troubleshooting

### No results for a valid-looking city
**Cause:** The keyword isn't a substring of the stored name - an accent, a space where the name has a hyphen, an outer space or a former name - or `countryCode` excluded it.
**Solution:** Trim and transliterate the keyword, search a single word of the name, or drop `countryCode`.

## Related skills

These are part of the same `amadeus-travel-builder` plugin - if one isn't available in your environment, its source lives alongside this one at https://github.com/AmadeusITGroup/amadeus-travel-toolkit/tree/main/plugins/amadeus-travel-builder/skills.

- [airport-city-search](../airport-city-search/SKILL.md) - unified airport **and** city typeahead returning flat, sub-type-prefixed location records; use it for a single ranked typeahead where users may type a city, an airport name or a code. It returns only IATA-coded locations, so stay with city-search when you need cities without a code, such as airport-less towns.
- [nearest-airports](../nearest-airports/SKILL.md) - when you have a lat/lon rather than a typed city name and need airports.
- [flight-search](../flight-search/SKILL.md) - the IATA city codes this skill resolves feed directly into its `origins` / `destinations`.
