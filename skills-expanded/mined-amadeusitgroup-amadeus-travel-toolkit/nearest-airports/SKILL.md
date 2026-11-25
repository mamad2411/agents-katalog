---
name: nearest-airports
description: Write application code that calls the Amadeus Travel Builder APIs to turn a geographic coordinate (latitude/longitude) into airports within a configurable radius (up to 500 km), ranked by relevance, distance, or traffic. Use when building a "nearest airport to me" feature, an "airports within 100 km of this hotel" lookup, a map-based airport finder, geo-aware defaults for a flight-search origin, or alternative-airport suggestions around a destination region (LHR/LGW/STN/LTN, etc.) - any app feature that starts from coordinates and needs airports, even if the user doesn't say the word "nearest". Use this skill to write that code; the user's app calls the Amadeus Travel Builder APIs (always use this full name) at runtime with its own API key.
---

# Nearest airports

Build a nearest-airports lookup from a `latitude`/`longitude`. Results are sorted by *relevance* (a blend of distance and traffic) by default, with alternative sorts for pure distance or pure traffic.

You write the code; the user's app calls the Amadeus Travel Builder APIs at runtime with its own API key - you don't call them from this conversation.

## Gateway and authentication

Base URL: `https://api.amadeus.com`; default to env vars `AMADEUS_GATEWAY_URL` and `AMADEUS_API_KEY` in generated code, unless the user's app loads them differently - either way, treat the key as a secret, keeping it out of client code and publicly served files. Authentication: send `X-API-Key: <key>` as a request header. When handing over the code, tell the user where to put their API key; if they don't have one yet, write out the [Request API access form](https://eu1.ironcladapp.com/public-launch/6aaa463f6f95614fe0f6db9d) URL in your reply (requires accepting the terms).

## Endpoint

```
GET https://api.amadeus.com/v1/reference-data/locations/airports?latitude=51.5074&longitude=-0.1278&radius=100
```

The coordinates and radius are illustrations of runtime input.

## Parameters

| Parameter | Required | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `latitude` | yes | number, -90 to 90 | - | Search centre in decimal degrees, with a dot as the decimal separator. |
| `longitude` | yes | number, -180 to 180 | - | Search centre in decimal degrees. The search doesn't wrap at ±180°: airports across the antimeridian are missing. |
| `radius` | no | integer, 0 to 500 | `500` | Search radius in km; `0` returns no airports. It filters on the exact distance while `distance.value` is rounded down, so an airport shown at N km can need `radius` N+1. |
| `page[limit]` | no | integer, 1 to 32767 | `10` | Maximum number of airports in the page. |
| `page[offset]` | no | integer, 0 to 50 | `0` | Zero-based index of the first airport in the page; at most 50 and at most `meta.count`, even when `meta.links` point further. Raise `page[limit]` to read more airports. |
| `sort` | no | `relevance` \| `distance` \| `analytics.flights.score` \| `analytics.travelers.score` | `relevance` | Sort order; one value, case-sensitive. |

### Sort modes

| Sort | Orders by | Use for |
| --- | --- | --- |
| `relevance` *(default)* | A score that grows with the airport's traffic and shrinks with its distance from the query point, highest first | An "airports to consider" list |
| `distance` | Straight-line distance from the query point, nearest first | A closest-airport feature |
| `analytics.flights.score` | Flight volume, busiest first | Ranking by flight volume |
| `analytics.travelers.score` | Traveler volume, busiest first | Ranking by traveler numbers; a region's main airports |

## Response shape

```json
{
  "meta": {
    "count": 7,
    "links": {
      "self": "https://api.amadeus.com/v1/reference-data/locations/airports?latitude=51.5074&longitude=-0.1278&radius=100&page%5Blimit%5D=5",
      "next": "https://api.amadeus.com/v1/reference-data/locations/airports?latitude=51.5074&longitude=-0.1278&radius=100&page%5Boffset%5D=5&page%5Blimit%5D=5",
      "last": "https://api.amadeus.com/v1/reference-data/locations/airports?latitude=51.5074&longitude=-0.1278&radius=100&page%5Boffset%5D=2&page%5Blimit%5D=5"
    }
  },
  "data": [
    {
      "type": "location",
      "subType": "AIRPORT",
      "name": "HEATHROW",
      "detailedName": "LONDON/GB:HEATHROW",
      "timeZoneOffset": "+00:00",
      "iataCode": "LHR",
      "geoCode": { "latitude": 51.4775, "longitude": -0.46138 },
      "address": {
        "cityName": "LONDON",
        "cityCode": "LON",
        "countryName": "UNITED KINGDOM",
        "countryCode": "GB",
        "regionCode": "EUROP"
      },
      "distance": { "value": 23, "unit": "KM" },
      "analytics": {
        "flights":   { "score": 39 },
        "travelers": { "score": 45 }
      },
      "relevance": 167.25014
    }
  ]
}
```
First result of Example 2's request with `page[limit]=5` (central London, 100 km, relevance order); scores, `relevance` and `timeZoneOffset` (with daylight saving time) vary over time.

| Field | Type | Notes |
| --- | --- | --- |
| `meta.count` | integer | Total number of airports matching the query, across all pages. |
| `meta.links.self` | string | The request URL. |
| `meta.links.next` | string, optional | Next page; present when airports remain. Its offset can exceed 50. |
| `meta.links.previous` | string, optional | Previous page; present when the offset is at least the limit. |
| `meta.links.last` | string, optional | Page at offset `count - limit`; present when `count` exceeds the limit. Its offset can exceed 50. |
| `meta.links.first` | string, optional | First page; present when the offset is above 0. |
| `data` | object[] | The page of airports, in `sort` order. Empty when no airport is in range. Each item follows [Airport](#airport). |

### Airport

| Field | Type | Notes |
| --- | --- | --- |
| `type` | `"location"` | Resource type. |
| `name` | string | Short name, uppercase, at most 30 characters; longer names are cut or abbreviated (`GREATER ROCHESTER INTL`), and some airports are named just `AIRPORT` (`LGG`). |
| `detailedName` | string | City, optional state code, country code and airport name (`LONDON/GB:HEATHROW`), cut at 30 characters; some airports have no `:airport` part (`BERU/KI`). |
| `timeZoneOffset` | string | UTC offset of the airport on the day of the call, including daylight saving time. |
| `iataCode` | string | IATA airport code. |
| `geoCode.latitude` | number | Airport latitude in decimal degrees. |
| `geoCode.longitude` | number | Airport longitude in decimal degrees. |
| `address.cityName` | string | Name of the city the airport serves, uppercase. |
| `address.cityCode` | string | IATA code of the city the airport serves. |
| `address.countryName` | string | Country name, uppercase. |
| `address.countryCode` | string | ISO 3166-1 alpha-2 country code, e.g. `GB` for the United Kingdom. |
| `address.stateCode` | string, optional | State or province code, present only in some countries (e.g. `NY` in the US). |
| `address.regionCode` | string | Amadeus world-region code, e.g. `EUROP`, `NAMER`, `ASIA`. |
| `distance.value` | integer | Great-circle distance from the search centre in whole km, rounded down - not a travel distance. |
| `distance.unit` | `"KM"` | Distance unit. |
| `analytics.flights.score` | integer | Flight-volume score; higher is busier, and small airports can score 0. |
| `analytics.travelers.score` | integer | Traveler-volume score; higher is busier, and small airports can score 0. |
| `relevance` | number | Higher is more relevant; grows with the airport's traffic and shrinks with its distance. Present whatever the `sort`, and specific to the query point. |
| `subType` | `"AIRPORT"` | Always `AIRPORT`; cities are never returned. |

## Examples

### Example 1: Nearest-airport-to-me feature

Developer asks: *"Add a feature that lists the 5 airports nearest the user's current location."*
Implementation:
1. Capture the user's lat/lon from the browser geolocation API.
2. Call `GET ${AMADEUS_GATEWAY_URL}/v1/reference-data/locations/airports?latitude=51.5074&longitude=-0.1278&radius=100&sort=distance&page%5Blimit%5D=5` - the coordinates stand for the captured position.
3. Render `name` with `address.cityName`, `iataCode` and `distance.value` km in the order returned (`sort=distance` ranks the closest airport first; the default relevance order can put a farther, busier airport ahead).

Result: a nearby-airports list in the UI, closest first.

### Example 2: Alternative-airport suggestions for a region

Developer asks: *"Add alternative-arrival-airport suggestions to my trip planner."*
Implementation:
1. For a worked example, London: call with `latitude=51.5074&longitude=-0.1278&radius=100`. By relevance it returns Heathrow (`LHR`), then Gatwick (`LGW`), City (`LCY`), Stansted (`STN`) and Luton (`LTN`).
2. Show the first as the primary airport and the rest as alternatives.

Result: a suggestions panel grouping a primary airport and its alternatives.

### Example 3: Pure-proximity sort

Developer asks: *"Add a 'closest airport' option that ignores airport size."*
Implementation:
1. Call with `sort=distance`. From central London (`latitude=51.5074&longitude=-0.1278`) the first result is London City (`LCY`) at 12 km, ahead of Heathrow at 23 km.
2. Take the first result.

Result: a closest-airport option showing straight-line distance in km.

## Things to get right

- **This endpoint returns airports only, never cities.** For a unified city + airport result set, use the [airport-city-search](../airport-city-search/SKILL.md) skill - filtering this one won't surface cities.
- **Display `name` with `address.cityName`, not `detailedName`.** Some airports' `name` is just `AIRPORT` (for example, Liège's `LGG`), so show it next to the city, or the city alone. `detailedName` is cut at 30 characters and can lack the airport part (for example, `BERU/KI`).
- **`distance` is straight-line, not driving distance.** Label it "X km away", not as a drive or travel time.
- **Pass a `radius` for a "nearby" feature.** It defaults to 500 km, which reaches airports hours away; 50-100 km suits most nearby lists.
- **For a region's main airports, sort by `analytics.travelers.score` and raise `page[limit]` when filtering results** - there is no server-side filter, so client-side filtering sees only the returned page, which can leave too few matches. Cover a country beyond the 500 km radius with several points merged by `iataCode`.
- **A radius search has no country boundary.** When the user requests airports within a particular country, retain only records whose `address.countryCode` equals that country's ISO code. Excluding named neighbouring countries is insufficient because the radius may reach others.
- **`countryCode` is the ISO 3166-1 alpha-2 code, which can differ from the everyday abbreviation** - e.g. `GB` for the United Kingdom, not `UK`, so a filter on `UK` matches nothing.
- **Don't follow `meta.links` past offset 50.** `page[offset]` above 50 returns 400 `4926`, yet `links.next` and `links.last` can point further (`next` sits at offset + limit, so at offset 50 with `page[limit]=1` it points at 51). Raise `page[limit]` instead (up to 32767); follow pagination links only while their offset is at most 50.
- **The search doesn't wrap at ±180° longitude.** Near the antimeridian (e.g. Fiji), airports just across it are missing - query a point on each side and merge by `iataCode`.
- **Closed airports can still be listed**, such as Berlin `TXL`.

## Errors

| HTTP | Code | Title | Cause |
| --- | --- | --- | --- |
| 400 | `477` | INVALID FORMAT | A value that isn't a number (`abc`, `51,5074`), a decimal for an integer parameter, a negative `page[limit]` or `page[offset]`, or an integer above 32767. |
| 400 | `572` | INVALID OPTION | Unknown query parameter; names are case-sensitive. |
| 400 | `703` | Size of URI parameters exceeds 2048 bytes. | URL-encoded query string over 2048 bytes. |
| 400 | `4926` | INVALID DATA RECEIVED | `latitude`, `longitude` or `radius` out of range, `sort` not one of its values, `page[limit]=0`, or `page[offset]` above 50 or above `meta.count`. |
| 400 | `32171` | MANDATORY DATA MISSING | `latitude` or `longitude` missing; `source.parameter` names it. |
| 400 | `38187` | Invalid parameters | Invalid API key. |
| 401 | `38191` | Invalid HTTP header | Missing X-API-Key header. |
| 429 | - | - | Rate limit for the API key exceeded. |
| 500 | `141` | SYSTEM ERROR HAS OCCURRED | Upstream failure. |

Error bodies are `{ "errors": [{ "status", "code", "title", "detail"?, "source"? }] }`.

## Troubleshooting

### Empty result set
**Cause:** `radius=0`; no airports within range of the coordinates; `page[offset]` equal to `meta.count`; or coordinates that aren't valid numbers - `latitude=NaN` returns 200 with no airports instead of an error.
**Solution:** Never pass `radius=0`, page only while `page[offset]` is below `meta.count`, and validate coordinates (finite, within ±90 / ±180) before calling.

## Related skills

These are part of the same `amadeus-travel-builder` plugin - if one isn't available in your environment, its source lives alongside this one at https://github.com/AmadeusITGroup/amadeus-travel-toolkit/tree/main/plugins/amadeus-travel-builder/skills.

- [airport-city-search](../airport-city-search/SKILL.md) - when you only have a place name (a hotel's city, an attraction), resolve it to coordinates first (its `geoCode`, returned with `view=FULL`), then call this.
- [flight-search](../flight-search/SKILL.md) - pass a picked airport's `iataCode` as a search origin or destination, with `+` to keep the search on that airport.
