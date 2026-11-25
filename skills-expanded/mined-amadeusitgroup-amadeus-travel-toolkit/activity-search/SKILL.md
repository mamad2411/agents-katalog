---
name: activity-search
description: Write application code that calls the Amadeus Travel Builder APIs for tours and activities - top activities at a destination, smart product recommendations filtered by traveler type, interests, price range, and similar-products, plus single-product detail lookups by productId. Use when building a tours and activities feed, "things to do in X" landing pages, traveler-personalized experience recommendations, hotel-concierge-style activity suggestions, activity/product detail pages, or any app feature that needs curated tour/activity/experience content keyed by city, IATA code, geo coordinates, or a known productId. Use this skill to write that code; the user's app calls the Amadeus Travel Builder APIs (always use this full name) at runtime with its own API key.
---

# Activity search

Build a curated tours and activities feed for a destination. Three endpoints:

- **Top activities** - the best-performing activities at a destination (city / IATA / geo).
- **Recommended products** - smart, filterable recommendations driven by traveler type, interests, price range, and an optional similar-product seed.
- **Get product** - full detail for a single, already-known product by `productId`.

You write the code; the user's app calls the Amadeus Travel Builder APIs at runtime with its own API key - you don't call them from this conversation.

## Gateway and authentication

Base URL: `https://api.amadeus.com`; default to env vars `AMADEUS_GATEWAY_URL` and `AMADEUS_API_KEY` in generated code, unless the user's app loads them differently - either way, treat the key as a secret, keeping it out of client code and publicly served files. Authentication: send `X-API-Key: <key>` as a request header. When handing over the code, tell the user where to put their API key; if they don't have one yet, write out the [Request API access form](https://eu1.ironcladapp.com/public-launch/6aaa463f6f95614fe0f6db9d) URL in your reply (requires accepting the terms).

## Endpoints

| Endpoint | Use for | Reference |
| --- | --- | --- |
| `GET /recommendation/v1/top-activities` | Generic "top things to do in X" landing pages | [`references/top-activities.md`](references/top-activities.md) |
| `POST /recommendation/v1/products` | Personalized feeds (traveler type, interests, budget); "similar to this product" carousels (`title`); tabs restricted to one category (`categories`) | [`references/recommended-products.md`](references/recommended-products.md); `categories` values: [`references/categories.md`](references/categories.md) |
| `GET /api/consumer/product/{productId}` | Detail page for one known `productId` (favourite, deep link) | [`references/product-schema.md`](references/product-schema.md) for the fields |

Paths are relative to the base URL. Get product's path isn't under `/recommendation/v1` - use it exactly as shown.

## Quick start

Paths, parameter and field names, and enum values are literal - send them exactly as shown. The destination, interests, prices, currency, counts and IDs are illustrations of runtime input, never defaults.

### Top activities

```
GET ${AMADEUS_GATEWAY_URL}/recommendation/v1/top-activities?cityName=Madrid&maxRecommendations=10&currency=EUR
X-API-Key: <key>
```

Read [`references/top-activities.md`](references/top-activities.md) if the app tunes scoring weights or sets a minimum content score.

### Recommended products

```
POST ${AMADEUS_GATEWAY_URL}/recommendation/v1/products
Content-Type: application/json
X-API-Key: <key>

{
  "maxRecommendations": 10,
  "recommendationFilters": {
    "iataCode": "MAD",
    "interests": ["food", "art", "live music"],
    "travelerType": "couple",
    "minPrice": 20,
    "maxPrice": 150,
    "currency": "EUR"
  }
}
```

Read [`references/recommended-products.md`](references/recommended-products.md) if the app filters by a similar-products seed, coordinates and radius, countries or continents, trip context or scoring weights. Read [`references/categories.md`](references/categories.md) if the app filters by `categories` - it lists the only accepted values.

### Get product

```
GET ${AMADEUS_GATEWAY_URL}/api/consumer/product/57179463
X-API-Key: <key>
```

`57179463` stands for a stored `productId`. It's a path segment, not a query parameter.

| Parameter | Required | Type | Notes |
| --- | --- | --- | --- |
| `productId` | yes | integer | The product's `productId`, as returned by top activities or recommended products. |

## Response shape

Top activities and recommended products each return a **JSON array of products** directly. Get product returns a **single product object**, not wrapped in an array. One product from the top-activities quick-start call, trimmed (prices, ratings and `id` vary per call):

```jsonc
{
  "id": 17985854214047736, // Search-response identifier, not product identity.
  "productId": 57214968, // Product identity.
  "title": "Teatro Flamenco Madrid: Live the Flamenco Experience",
  "description": "<div><p>Experience authentic Spanish culture at Teatro Flamenco Madrid...",
  "galleryImages": [ { "url": "https://images.holibob.tech/...", "order": 0 } ],
  "minPrice": 44.0,
  "maxPrice": 44.0,
  "priceCurrency": "EUR",
  "bookingUrl": "https://to.discover-exp.com/...",
  "geoLocation": { "latitude": 40.4231478, "longitude": -3.7044556, "geoHash": "ezjmgwy3zu" },
  "rating": 4.7157893,
  "numberOfRatings": 475
}
```
Read [`references/product-schema.md`](references/product-schema.md) if the app needs a per-call search identifier or shows opening hours, cancellation policy, duration, languages or classification. For a specific field, search that file by its exact name, then read the containing section for related fields and constraints.

## Examples

### Example 1: "Things to do" landing page for a city

Developer asks: *"Build a 'Things to do' landing page for a city."*
Implementation:
1. Call top activities as in the quick start, with the page's city as `cityName`.
2. Render a card grid with `title`, the `galleryImages` entry with the lowest `order` as the photo, `minPrice` + `priceCurrency`, and a short excerpt of the sanitized `description`.
3. Call to action: open `bookingUrl` in a new tab, when the product has one.

Result: a generic top activities feed for the city.

### Example 2: Personalized recommendations

Developer asks: *"Add personalized experience recommendations to my app."*
Implementation:
1. For a worked example, a couple in Madrid on leisure who like food, art and live music, with a €20-€150 budget: send the recommended-products quick-start body, adding `"tripContext": "leisure"`.
2. Render the response as a card grid, sanitizing `description`.

Result: a personalized recommendation feed.

### Example 3: Similar-products carousel

Developer asks: *"Add a carousel of experiences similar to the one being viewed."*
Implementation:
1. Call recommended products with `recommendationFilters.title` set to the viewed product's title and no `interests`, plus the same destination. For a worked example, `{ "iataCode": "MAD", "title": "Teatro Flamenco Madrid: Live the Flamenco Experience" }` returns other flamenco shows, such as Corral de la Moreria and Café Ziryab, among other Madrid highlights.
2. Drop the viewed product from the results by `productId`; the seed itself can come back.

Result: a "similar to" carousel.

### Example 4: Activity detail page

Developer asks: *"Build a detail page for an activity a user favourited earlier."*
Implementation:
1. Look up the favourite's stored `productId` and call get product with it.
2. Treat a `404` (`6041`) as "no longer available", separately from other errors.
3. Render the sanitized description, gallery images and opening hours (`availabilityPeriods` - see the product schema).
4. Call to action: open `bookingUrl`, when present.

Result: a single-product detail view driven entirely by `productId`.

## Things to get right

- **Locate a search by coordinates, IATA code or city name - and the two search endpoints spell them differently.** Top activities takes query parameters `lat`+`lon`, `iataCode` and `cityName`; recommended products takes body fields `geoLocation`, `iataCode` and `city` inside `recommendationFilters`, where `countryCodes` or `continentCodes` alone also locate a search. Top activities ignores unknown query parameters, including the body names, so a call relying on them alone returns 400 `6043`. Coordinates are a complete way to locate the search, not a refinement of a city. When several locators are sent, the API picks by priority without erroring - coordinates, then `iataCode`, then city name.
- **Top activities caps `maxRecommendations` at 10** - higher values return `400`, while recommended products accepts up to 1000. A feed that needs more than 10 uses recommended products.
- **Use `productId` for product identity; `id` and `productId` are not interchangeable.** Do not read or store `id` unless the app specifically needs to reference an individual search response. For favourites, caches, links and deduplication, use only `productId`; omit products missing it, never fall back to another field.
- **Narrow results with `interests`, not `categories`, unless the user wants a strict category.** Products not filed under any `activities-*` category are silently dropped by `categories`, while free-form `interests` still returns them.
- **`title` (similar-products mode) is ignored when `interests` is set**, so send it without `interests`.
- **`Accept-Language` selects translated text on all three endpoints.** Without it, text defaults to English; an unavailable translation falls back to English. Translation can be partial, so `displayedLanguage` doesn't guarantee every text field is in that language.
- **Product fields are supplier data and can be missing or inconsistent** - e.g. `categories` can say `no_category` while `taxonomies` files the product under Culture.
- **Split list-like text on the literal two characters `/n` before display.** `experienceHighlights`, `cancellationCutOff`, `modalitiesIncluded`, `modalitiesExcluded`, `modalitiesAdditionalInfo` and `additionalInformation.unstructured_data` join their items with `/n`, not a newline, so rendering them as-is shows `fees/nTour guide`.
- **Sanitize `description` before it reaches the DOM.** It can contain supplier-authored HTML, so injecting it raw is an XSS vector.
- **Sort `galleryImages` by `order` before picking a photo.** The array comes back in a different order from call to call, so `galleryImages[0]` isn't the first image. `thumbnailImage` is a bare UUID, not a URL.
- **There is no `shortDescription`** - use a truncated, sanitized `description` for teasers.
- **Stop at `bookingUrl` for booking, and handle its absence.** Redirect the user there; the booking engine takes over. A few products have no `bookingUrl` or `travelerUrl`, so code that assumes one breaks on them.
- **Don't retry a 500 `6503` from top activities unchanged.** It's what an unsupported `currency` returns there - not transient, so the retry fails the same way (recommended products rejects the same value with 400 `6043`).

## Errors

Codes every endpoint returns. Codes specific to top activities and recommended products are in their references; get product's follow the table.

| HTTP | Code | Title | Cause |
| --- | --- | --- | --- |
| 400 | `38187` | Invalid parameters | Invalid API key. |
| 401 | `38191` | Invalid HTTP header | Missing X-API-Key header. |
| 429 | - | - | Rate limit for the API key exceeded. |

Codes only get product returns:

| HTTP | Code | Title | Cause |
| --- | --- | --- | --- |
| 400 | - | Bad Request | A `productId` that isn't an integer; `application/problem+json` body. |
| 404 | `6041` | Non existing product | Unknown `productId`, or the product is no longer available. |
| 500 | `6503` | Internal Error | Unexpected server error. |

Gateway errors (`38187`, `38191`) come as `{ "errors": [ { "status", "code", "title", "detail" } ] }`; the API's own errors as a bare `{ "status", "code", "title", "detail"? }`. Branch on the HTTP status, then read `code` from either shape; some 400s have none.

## Troubleshooting

### 400 / 404 - code 6025, 6054, 6056 or 6087, destination not found
**Cause:** The destination isn't known (`6025` on both search endpoints, also for a non-English city name such as `Wien` or `München`), the country or continent isn't known (`6054` or `6087`, recommended products), or the destination is known but not covered (`6056`, top activities).
**Solution:** Send the English city name, a valid ISO country code or one of `EU`, `AS`, `NA`, `SA`, `AF`, `OC`. `6056` means no activities for that destination, not a failure; a nearby larger city or coordinates may have results.

### 200 with an empty array
**Cause:** Both search endpoints return `[]` when the destination resolves but has no products (top activities for `iataCode=GOH` or `ULN`) or the filters match nothing.
**Solution:** Handle `[]` as an empty state, and try a nearby larger city or coordinates with a `radius`.

## Related skills

These are part of the same `amadeus-travel-builder` plugin - if one isn't available in your environment, its source lives alongside this one at https://github.com/AmadeusITGroup/amadeus-travel-toolkit/tree/main/plugins/amadeus-travel-builder/skills.

- [city-search](../city-search/SKILL.md) - to power a destination picker that feeds this search: it covers airport-less destinations (resort towns, small coastal towns) that a hotel-concierge or "things to do" feature needs just as much as airport-served cities. For such a town, pass its coordinates (`lat`/`lon` or `geoLocation`) with a small `radius` - its name returns a wider regional list.
- [airport-city-search](../airport-city-search/SKILL.md) - an alternative picker when the app already has one for flight search and you want to reuse it, though it returns only IATA-coded places, so towns without a code (such as Antibes) are missing.
