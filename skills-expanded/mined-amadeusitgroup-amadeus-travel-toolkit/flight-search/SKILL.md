---
name: flight-search
description: Write application code that calls the Amadeus Travel Builder APIs to search flights, returning priced offers from multiple airlines in a single call - one-way, return, and complex multi-city / open-jaw itineraries - with booking deep links that redirect to each airline's site. Use when building a flight comparison feature, fare aggregation tooling, multi-city trip planners, a cheapest-flight search, any application that needs flight pricing aggregated across carriers, or any feature that shows flight departure/arrival times, layovers, or trip duration from a real search rather than mocked or precomputed data. Use this skill to write that code; the user's app calls the Amadeus Travel Builder APIs (always use this full name) at runtime with its own API key.
---

# Flight search

Build flight search across multiple airline merchants with a single API call. Each result includes pricing and full itinerary detail, usually with a deep link that redirects to the merchant's site.

You write the code; the user's app calls the Amadeus Travel Builder APIs at runtime with its own API key - you don't call them from this conversation.

## Gateway and authentication

Base URL: `https://api.amadeus.com`; default to env vars `AMADEUS_GATEWAY_URL` and `AMADEUS_API_KEY` in generated code, unless the user's app loads them differently - either way, treat the key as a secret, keeping it out of client code and publicly served files. Authentication: send `X-API-Key: <key>` as a request header. When handing over the code, tell the user where to put their API key; if they don't have one yet, write out the [Request API access form](https://eu1.ironcladapp.com/public-launch/6aaa463f6f95614fe0f6db9d) URL in your reply (requires accepting the terms).

## Endpoint

```
GET https://api.amadeus.com/api/v3/search/
```

One call covers one-way, return, multi-city and open-jaw searches.

## Quick start

Paths, parameter names, `flow=NETWORK` and enum values are literal. Locations, dates, counts, locale and currency illustrate runtime input, never defaults.

```
GET ${AMADEUS_GATEWAY_URL}/api/v3/search/?origins=LON,PAR&destinations=PAR,LON&dates=<outbound YYYY-MM-DD>,<return YYYY-MM-DD>&locale=en-GB&flow=NETWORK&adults=1&travel_class=ECONOMY&currency=GBP
X-API-Key: <key>
```

The lists are **positional**: `origins[i]`, `destinations[i]` and `dates[i]` define leg i.

| Shape | `origins` | `destinations` | `dates` |
| --- | --- | --- | --- |
| One-way `BOS → AMS` | `BOS` | `AMS` | `D1` |
| Return `BOS ↔ AMS` | `BOS,AMS` | `AMS,BOS` | `D1,D2` |
| Multi-city `BOS → AMS → CDG → BOS` | `BOS,AMS,CDG` | `AMS,CDG,BOS` | `D1,D2,D3` |
| Open-jaw `BOS → AMS, CDG → BOS` | `BOS,CDG` | `AMS,BOS` | `D1,D2` |

`D1` ≤ `D2` ≤ `D3` are dates in `YYYY-MM-DD`, today or later.

## Parameters

### Required parameters

| Parameter | Required | Type | Notes |
| --- | --- | --- | --- |
| `origins` | yes | CSV of string `[A-Za-z]{3}\+?`, 1-6 items | Departure city or airport IATA code per bound, case-insensitive. A city code covers all its airports; `+` after an airport code restricts to that airport. |
| `destinations` | yes | CSV of string `[A-Za-z]{3}\+?`, 1-6 items | Arrival code per bound, same format; must differ from the bound's origin. |
| `dates` | yes | CSV of string, 1-6 items | Departure date per bound, `YYYY-MM-DD`: today or later, each on or after the previous one. Beyond a merchant's booking window (BA: about 354 days ahead), that merchant returns no results and error `931`. |
| `locale` | yes | string `[A-Za-z]{2,3}([-_][A-Za-z0-9]{2,8}){0,3}` | BCP 47 (e.g. `en-US`). Doesn't change which merchants answer or their offers. A malformed value is rejected as `This parameter is required.` |
| `flow` | yes | `"NETWORK"` | Always `NETWORK`; no default. |

### Passenger composition

| Parameter | Required | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `adults` | no | integer, 0 to 9 | `1` | Age 12+. `adults` + `children` ≥ 1; `adults` + `children` + `infants_with_seat` ≤ 9. |
| `children` | no | integer, 0 to 9 | `0` | Ages 2-11, each with a seat. |
| `infants` | no | integer, 0 to 9 | `0` | Under 2, on an adult's lap. `infants` + `infants_with_seat` ≤ `adults`. |
| `infants_with_seat` | no | integer, 0 to 9 | `0` | Under 2, with a seat. Priced under `fare.price_per_ptc.INS`. |
| `pax_ages` | no | CSV of integer, ≥ 2 | - | Age of each adult and child, at most `adults` + `children` values in any order; prices them in `fare.price_per_ptc` by age-based code (`B35`, `C08`). Ages must fit the passenger counts - 12+ for adults, 2-11 for children - or those merchants return no results and no `errors` entry. |

### Cabin and price

| Parameter | Required | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `travel_class` | no | `FIRST` \| `BUSINESS` \| `ECONOMY` \| `PREMIUM_ECONOMY` | `ECONOMY` | Preferred cabin, not a filter. |
| `currency` | no | string `([A-Za-z]{3}\|AUTO\|MERCHANT)` | `EUR` | ISO 4217 code. `AUTO`: the origin country's. `MERCHANT`: each merchant's choice, so currencies can mix. |

### Merchant filtering

Use merchant codes (airline IATA codes), not airline names.

| Parameter | Required | Type | Notes |
| --- | --- | --- | --- |
| `include_merchants` | no | CSV of string | Codes to search, upper-case, no spaces; omit for every merchant. |
| `exclude_merchants` | no | CSV of string | Codes to leave out; combinable with `include_merchants`, but not on the same code. |

### Result shaping

| Parameter | Required | Type | Default | Notes |
| --- | --- | --- | --- | --- |
| `number_of_results` | no | integer, 1 to 1000 | - | Maximum results per merchant; default is each merchant's own limit. |
| `nonstop` | no | boolean | `false` | `true` asks for non-stop flights; each merchant decides whether to apply it. |
| `disable_deep_links` | no | `FALSE` \| `TRUE` \| `KEEP_NETWORK` | `FALSE` | `TRUE` removes every `deep_link` (smaller response); `KEEP_NETWORK` acts as `FALSE`. |
| `preferred_landing_page` | no | `passenger_details` \| `search_results` \| `home_page` | `search_results` | Where deep links land. |
| `platform` | no | `mobile` \| `web` | `web` | Deep-link target platform. |
| `tfl_id` | no | string | - | End-user query ID for tracking. |

## Response shape

```json
{
  "request_id": "<request-id>",
  "results": [
    {
      "bounds": [
        { "duration": "01:15", "flights": [
          { "marketing_airline": "BA", "flight_number": "322", "origin": { "airport": "LHR", "terminal": "5" }, "destination": { "airport": "CDG", "terminal": "2C" },
            "departs_at": "2027-01-03T21:00:00Z", "arrives_at": "2027-01-03T23:15:00+01:00", "duration": "01:15",
            "booking_infos": [ { "ptc": "ADT", "priced_ptc": "ADT", "travel_class": "ECONOMY", "cabin_code": "M", "booking_code": "N", "fare_basis": "NZ0R", "fare_breakpoint": true } ] } ] },
        { "duration": "01:10", "flights": [
          { "marketing_airline": "BA", "flight_number": "315", "origin": { "airport": "CDG", "terminal": "2C" }, "destination": { "airport": "LHR", "terminal": "5" },
            "departs_at": "2027-01-10T18:50:00+01:00", "arrives_at": "2027-01-10T19:00:00Z", "duration": "01:10",
            "booking_infos": [ { "ptc": "ADT", "priced_ptc": "ADT", "travel_class": "ECONOMY", "cabin_code": "M", "booking_code": "N", "fare_basis": "NZ0R", "fare_breakpoint": true } ] } ] }
      ],
      "fare": { "currency": "GBP", "itinerary_price": { "total_fare": 186.51, "tax": 93.51 }, "price_per_adult": { "total_fare": 186.51, "tax": 93.51 } },
      "merchant": "BA",
      "deep_link": "https://..."
    }
  ],
  "errors": { "TU": "120 - No flight found on this route for merchant TU" },
  "meta": { "carriers": { "BA": { "name": "British Airways", "debug_info": ["<debug-info>"] } } }
}
```

A London-Paris round trip with `include_merchants=BA,TU`, trimmed; prices vary per search. The trip total is `fare.itinerary_price.total_fare` in `fare.currency` - there is no flat `fare.total`.

Read [`references/response-schema.md`](references/response-schema.md) if the app uses a field beyond the example - baggage, stops, fare families, per-passenger-type prices, itemised taxes, `pax_ages` mappings - or needs to know which fields are optional. For a specific field, search that file by its exact name.

## Examples

### Example 1: Round-trip search

Developer asks: *"Build a round-trip flight search function for my application."*
Implementation:
1. For London to Paris and back, one adult: `origins=LON,PAR`, `destinations=PAR,LON`, `dates=<outbound>,<return>`, as in the quick start.
2. For each result, show `fare.itinerary_price.total_fare` and `fare.currency`, then each bound's flights (carrier, flight number, times, layovers).
3. Link each offer to its `deep_link` when it has one.

Result: a search function returning priced offers and their deep links, sorted client-side.

### Example 2: Multi-city itinerary

Developer asks: *"Support multi-city flight search in my app."*
Implementation:
1. For Boston → Amsterdam → Paris → Boston, 2 adults: `origins=BOS,AMS,CDG`, `destinations=AMS,CDG,BOS`, `dates=D1,D2,D3`, `adults=2`.
2. Render each result's three `bounds` in itinerary order.
3. Treat `deep_link` as optional: some merchants' multi-city offers have none.

Result: a multi-city search whose results carry one bound per leg.

### Example 3: Force airport interpretation

Developer asks: *"Let users search from one specific airport rather than every airport in its city."*
Implementation:
1. For a worked example, London City rather than every London airport: send `origins=LCY+`, setting the `+` through the query encoder.

Result: a search scoped to the chosen airport.

## Things to get right

- **Show `departs_at` / `arrives_at` as returned, with no timezone conversion.** Each is the airport's local time; a formatter in the viewer's timezone shifts it, even after rebuilding a timestamp from the parts. BA 322 above leaves Heathrow at 21:00 (`...T21:00:00Z`) and lands at 23:15 (`...T23:15:00+01:00`); `Z` is offset zero, not "convert me".
- **Compute a bound's total time from its first `departs_at` to its last `arrives_at`, keeping the offsets.** `bound.duration` can be 60 minutes off when a layover spans a clock change; flight `duration` is right (BA 322: `01:15`). EY from LHR on 2027-03-27 leaves at 18:00Z and lands at `2027-03-29T09:40:00+08:00`: 31h40m elapsed, `bound.duration` says `32:40`, and ignoring the offsets gives 39h40m.
- **Build the three lists leg by leg.** Equal-length lists that pair the wrong cities are valid and silently search a different itinerary.
- **Use `+` only on airport codes, and pass it raw to a query encoder.** `LCY+` searches London City only and `LON+` finds nothing; a bare `NYC` returns JFK, LGA and EWR departures, a bare `LAX` can return `ONT`. The `+` must arrive as `%2B`: concatenated it decodes as a space, pre-encoded it is encoded twice - both return 400 `must match "[a-zA-Z]{3}"`.
- **Spell parameter names exactly.** Unknown query parameters are ignored, so a typo (`adult=2`) silently searches with the default instead of failing.
- **Sort results yourself** (e.g. by `fare.itinerary_price.total_fare`); they come back grouped by merchant.
- **Omit `include_merchants` to search every merchant.** An explicit `*` adds an `errors["*"]` entry, and codes are case-sensitive and untrimmed: `ba` or ` AZ` gets `Unknown or unauthorized merchant` and no results.
- **Get airline names for flights from airline-code-lookup, not `meta.carriers`.** `meta.carriers` names only the merchants, while a merchant's offers often include partner airlines' flights: BA's London-Sydney offers include Qantas (`QF`) flights, and `meta.carriers` has no `QF`. Resolve every `marketing_airline` and IATA `operating_airline` code in one batched lookup.
- **Read each flight's cabin from `booking_infos[].travel_class`.** `travel_class=FIRST` on London-Paris, a route with no first cabin, returns economy offers.
- **Use `deep_link` as returned; re-search rather than store results.** It redirects to the merchant's site, so don't parse, rewrite or domain-check it; prices are live. Depending on the merchant, multi-city and open-jaw offers can come without one, so show the offer without a link rather than dropping it.

## Errors

| HTTP | Code | Title | Cause |
| --- | --- | --- | --- |
| 400 | - | - | Validation failure: `message` names every invalid parameter - e.g. missing or unequal lists, past or unordered dates, an origin equal to its destination, over 6 bounds, passenger limits, invalid values. |
| 400 | `38187` | Invalid parameters | Invalid API key. |
| 401 | `38191` | Invalid HTTP header | Missing `X-API-Key` header. |
| 429 | - | - | Rate limit for the API key exceeded; retry later with exponential backoff. |
| 500 | - | - | Server error; retry once. |

A merchant with no offers doesn't fail the search: the response is 200, with an `errors` entry for it.

| Code | Meaning | Retry? |
| --- | --- | --- |
| `120` | No flight on this route for the merchant. | No |
| `931` | No itinerary found. | No |
| `866` | No fares for this itinerary from the merchant. | No |
| `977` | Flight not available from the merchant. | No |
| `920` | Past date/time not allowed - also sent for a date decades ahead (2099); a date just past the booking window gets `931`. | No |
| `987` / `995` | No content; the message gives no reason. | No |
| `117` / `118` | Open-jaw / multi-city not enabled for the merchant. | No |
| `871` | Too many segments for the merchant. | No |
| `123` / `126` | Rate limit reached - `123` for that merchant; `126` for the whole search, under the `*` key. | Later, with backoff |
| `865` | Invalid `currency`; other merchants may price in a currency of their choice. | No |
| `99` / `-1` | Technical error. | At most once |
| `Unknown or unauthorized merchant` | Code unknown, not upper-case, space-padded, or not authorized for this key. | No - fix or drop the code |

Other codes come from the merchant's system; the message doesn't always say why, so treat them as no offers from that merchant.

## Troubleshooting

### Parsing a 400
**Cause:** `message` is a JSON string mapping each invalid parameter (or a check such as `input_consistent`) to its reason, all at once: `"{\"adults\":\"must be between 0 and 9\"}"`. A malformed date or age gives `path` and `problem` keys instead; gateway errors (`38187`) are `{ errors: [{ code, title, status, detail }] }`.
**Solution:** Branch on the body shape: parse `message` a second time, and fall back to `errors[0].detail` when there's no `message`.

### Unknown location code returns 200 with no results
**Cause:** A well-formed unknown code (`ZZZ`) isn't a 400: `results` is empty and every merchant has an `errors` entry.
**Solution:** Validate codes client-side, e.g. from an airport picker.

### Mixed currencies in one result list
**Cause:** `currency=MERCHANT`, or an unsupported code: it returns 200, with `865` from some merchants while others price in a currency of their choice.
**Solution:** Use `currency=AUTO` or a valid ISO 4217 code, checked client-side.

### Hundreds of results
**Cause:** A search across every merchant can return hundreds of offers.
**Solution:** Cap them per merchant with `number_of_results`.

### One merchant missing, response is still `200`
**Cause:** That merchant failed and is listed in `errors` as `"<code> - <message>"`; the other merchants' results are unaffected.
**Solution:** Handle `errors` per merchant rather than failing the whole search; retry only the codes the Errors table marks as retryable.

## Related skills

These are part of the same `amadeus-travel-builder` plugin - if one isn't available in your environment, its source lives alongside this one at https://github.com/AmadeusITGroup/amadeus-travel-toolkit/tree/main/plugins/amadeus-travel-builder/skills.

- [airline-code-lookup](../airline-code-lookup/SKILL.md) - airline names for each flight's `marketing_airline` and `operating_airline` codes, which `meta.carriers` doesn't cover.
- [airport-city-search](../airport-city-search/SKILL.md) - origin / destination pickers: pass the picked `iataCode`, with `+` for an `AIRPORT` pick.
- [nearest-airports](../nearest-airports/SKILL.md) - airports near the user, as a default origin.
