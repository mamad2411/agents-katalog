---
name: airline-code-lookup
description: Write application code that calls the Amadeus Travel Builder APIs to resolve IATA or ICAO airline codes to airline business and common names, one at a time or in batches. Use when building an app that displays carrier names in flight results, an airline picker or filter, decoding of carrier codes from search responses, fare lookups, airline-code validation in a form, or batch resolution of a list of codes in one call. Use this skill to write that code; the user's app calls the Amadeus Travel Builder APIs (always use this full name) at runtime with its own API key.
---

# Airline Code Lookup

Build airline-code lookups into an app, resolving IATA or ICAO codes to airline names. One endpoint, one call.

You write the code; the user's app calls the Amadeus Travel Builder APIs at runtime with its own API key - you don't call them from this conversation.

## Gateway and authentication

Base URL: `https://api.amadeus.com`; default to env vars `AMADEUS_GATEWAY_URL` and `AMADEUS_API_KEY` in generated code, unless the user's app loads them differently - either way, treat the key as a secret, keeping it out of client code and publicly served files. Authentication: send `X-API-Key: <key>` as a request header. When handing over the code, tell the user where to put their API key; if they don't have one yet, write out the [Request API access form](https://eu1.ironcladapp.com/public-launch/6aaa463f6f95614fe0f6db9d) URL in your reply (requires accepting the terms).

## Endpoint

```
GET https://api.amadeus.com/v1/reference-data/airlines?airlineCodes=BA,AFR,LH
```

The codes are illustrations of runtime input.

## Parameters

| Parameter | Required | Notes |
| --- | --- | --- |
| `airlineCodes` | no | Comma-separated IATA (2 characters) and/or ICAO (3 characters) airline codes, mixed freely and case-insensitive. No spaces: a code with a space next to it is dropped. Duplicates and empty items are ignored; an IATA and an ICAO code of the same airline return one record. An empty value returns no airlines; omitting the parameter returns every airline that has an IATA code. The query string is limited to 2048 bytes as sent: an encoded comma (`%2C`) counts 3, a raw one 1. |

## Response shape

```json
{
  "meta": { "count": 3, "links": { "self": "https://api.amadeus.com/v1/reference-data/airlines?airlineCodes=BA,AFR,LH" } },
  "data": [
    { "type": "airline", "iataCode": "AF", "icaoCode": "AFR", "businessName": "AIR FRANCE", "commonName": "AIR FRANCE" },
    { "type": "airline", "iataCode": "BA", "icaoCode": "BAW", "businessName": "BRITISH AIRWAYS", "commonName": "BRITISH A/W" },
    { "type": "airline", "iataCode": "LH", "icaoCode": "DLH", "businessName": "LUFTHANSA", "commonName": "LUFTHANSA" }
  ]
}
```
The response to the request above.

| Field | Type | Notes |
| --- | --- | --- |
| `meta.count` | integer | Number of records in `data`. |
| `meta.links.self` | string | The request URL, with the codes uppercased. |
| `data` | object[] | One record per matched airline, sorted by IATA code when codes are requested (ICAO-only airlines last); the full list isn't fully sorted, so sort it yourself. Each item follows [Airline](#airline). |

### Airline

| Field | Type | Notes |
| --- | --- | --- |
| `type` | `"airline"` | Resource type. |
| `iataCode` | string, optional | IATA code (2 characters, letters or digits). Absent on airlines with no IATA code. |
| `icaoCode` | string, optional | ICAO code (3 characters, usually letters). Absent on many airlines, including every placeholder record. |
| `businessName` | string | Business name, usually uppercase. `UNDEFINED` on placeholder records (e.g. `XX`, `9W`). |
| `commonName` | string, optional | Common name, sometimes abbreviated (`BRITISH A/W`) and usually uppercase. Absent on most placeholder records. |

## Examples

### Example 1: Decode carrier codes from a flight result

Developer asks: *"Add a helper that turns carrier codes into airline names for my flight results UI."*
Implementation:
1. Call `GET ${AMADEUS_GATEWAY_URL}/v1/reference-data/airlines?airlineCodes=BA,AF,LH`.
2. Read `data[].businessName` for each entry; a record whose `businessName` is `UNDEFINED` is a placeholder, so treat that code as unknown.

Result: a code → display-name map the results list renders from.

### Example 2: Resolve a mix of IATA and ICAO codes

Developer asks: *"Build me an airline lookup that accepts both 2-letter and 3-letter codes."*
Implementation:
1. Split the user input on commas and whitespace, drop empty items, upper-case each code and join them with commas for `airlineCodes` - mixed standards (`BA,BAW,AF`) are accepted in one call, but a code with a space next to it is silently dropped (`BA, AF` returns only BA) and codes joined without a comma match nothing (`BAAF`).
2. Index the response by both `iataCode` and `icaoCode`, which come back upper-case.

Result: a single map keyed by whichever code the caller provided, looked up in upper case.

## Things to get right

- **Always send `airlineCodes`, and split long lists across requests** - a few hundred codes reach the query-string limit.
- **Send `airlineCodes` once, as one comma-joined value.** Repeated, only the first is used: `airlineCodes=BA&airlineCodes=AF` returns only BA. A query builder given an array (Python `requests` with a list) repeats the parameter - join the codes yourself.
- **Validate codes by length, not by letters.** Digits appear in both standards - IATA `2K`, ICAO `5AH` - so a letters-only pattern such as `[A-Z]{2}` rejects real airlines.

## Errors

| HTTP | Code | Title | Cause |
| --- | --- | --- | --- |
| 400 | `572` | INVALID OPTION | Unknown query parameter; names are case-sensitive. |
| 400 | `703` | Size of URI parameters exceeds 2048 bytes. | Query string over 2048 bytes as sent. |
| 400 | `38187` | Invalid parameters | Invalid API key. |
| 401 | `38191` | Invalid HTTP header | Missing X-API-Key header. |
| 429 | - | - | Rate limit for the API key exceeded. |
| 500 | `38189` | Internal error | Server error. |

## Troubleshooting

### Unknown code returns nothing
**Cause:** Unknown and malformed codes don't error - they're silently absent from `data`.
**Solution:** Diff the requested codes against `data[].iataCode` / `data[].icaoCode` to find misses:

```ts
const found = new Set(response.data.filter(a => a.businessName !== 'UNDEFINED').flatMap(a => [a.iataCode, a.icaoCode].filter(Boolean)))
const missing = requested.filter(code => !found.has(code.toUpperCase()))
```

### Response order doesn't match request order
**Cause:** Results are sorted by IATA code (ICAO-only airlines last), not in request order.
**Solution:** Build a lookup map keyed by `iataCode` / `icaoCode`; don't index by position.

## Related skills

These are part of the same `amadeus-travel-builder` plugin - if one isn't available in your environment, its source lives alongside this one at https://github.com/AmadeusITGroup/amadeus-travel-toolkit/tree/main/plugins/amadeus-travel-builder/skills.

- [flight-search](../flight-search/SKILL.md) - searches for flights; pair its `merchant`/carrier codes with this skill to show airline names instead of raw codes.
