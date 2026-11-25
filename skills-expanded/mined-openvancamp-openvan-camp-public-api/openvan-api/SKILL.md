---
name: openvan-api
description: Build websites, apps, bots and dashboards on the free OpenVan.camp travel data API (no key, CORS) or its SDKs (@openvancamp/sdk for JS/TS, openvan for Python) — fuel prices in 170+ countries, route fuel and toll cost, ferry crossings and timetables, whole-trip roadbooks, visa and vehicle-import rules, public and school holidays, travel hazards and wildfires, power plugs, customs rules, weather suitability scores, food price index, currency rates, vanlife events, news and license plate images. Use when code calls openvan.camp/api, imports @openvancamp/sdk or openvan, or the user wants fuel, toll, visa, holiday or road-trip data in their product.
license: MIT
metadata:
  author: OpenVan.camp
  homepage: https://openvan.camp/en/developers
---

# Building on the OpenVan.camp API

Base URL `https://openvan.camp`, no key, no registration, CORS enabled. The contract is the
OpenAPI file at <https://openvan.camp/docs.openapi> — read the endpoint there before writing
code against it; interactive docs at <https://openvan.camp/docs>. Endpoint list:
[references/endpoints.md](references/endpoints.md).

## Do this in every integration

1. **Show the attribution next to the data.** The data is CC BY 4.0 and the link is required.
   Every JSON response carries it in `_attribution.attribution_html`:
   `Data: <a href="https://openvan.camp/">OpenVan.camp</a> (CC BY 4.0)`. Render it visibly in
   the UI you generate (not only in a code comment or README), wherever the data appears.
2. **Identify the integration:** add `source=<site-or-app>` to every request (the SDKs take it
   as an option). It is echoed back as `_attribution.your_source`. Responses without it carry a
   reminder in `_attribution.identify`. If the server is overloaded, requests with `source` are served
   first; the others may receive `503` with `Retry-After`. A contact can go in the User-Agent:
   `MyApp/1.0 (+https://myapp.com; dev@myapp.com)`.
3. **Send `Accept: application/json`.** Without it some errors come back as HTML.
4. **Prefer the SDK** when the project is JS/TS or Python — it handles grade units, currencies
   and the source parameter:
   - `npm install @openvancamp/sdk` → `new OpenVan({ source: "myapp.com" })`
   - `pip install openvan` → `OpenVan(source="myapp.com")`

## Traps

- **Fuel unit and currency are per grade.** Read `units[grade]` and `currencies[grade]`, not the
  country's top-level `unit` / `currency`. Colombia: top-level `unit` is `liter`, but petrol and
  diesel are priced per gallon. Venezuela: top-level `currency` is `USD`, but petrol is in `VES`.
  A `null` price means no data for that grade. `is_excluded: true` marks heavily subsidised
  prices that should not be ranked against market prices. `ov.fuel.cheapest()` in the SDK
  already normalises all of this to EUR per litre.
- **Prices are in local currency.** Convert when you render, with `GET /api/currency/rates`
  (EUR-based: `amount / rates[FROM] * rates[TO]`; note this response is `{success, rates}`,
  not `{success, data}`). Do not store converted prices as if they were fresh — rates move.
- **No data is not "nothing applies".** `covered: false` with empty `items` (holidays, customs),
  an empty vehicle-import list, or a partial toll estimate means OpenVan.camp has no data. Show
  "no data — check the official source", never "no holidays" / "no restrictions" / "free road".
- **Envelopes differ between endpoints.** Most return `{success, data, meta, _attribution}`;
  some (currency rates, holidays, customs, toll route) return their fields at the top level.
  Check the response schema in the OpenAPI file instead of assuming `data`.
- **Visa and vehicle rules carry `confidence`, `source_url` and `updated_at`.** Show the source
  link and the date; label anything below `high` confidence as "check with the embassy".
- **Roadbooks are asynchronous.** `POST /api/roadbook/from-places` returns a `code` and
  `status: pending`; poll `GET /api/roadbook/{code}/status` until `ready` (long routes take up to
  a minute), then link to `https://openvan.camp` + `url`. Identical requests return the same
  roadbook.
- **Ferries are ODbL, not CC BY.** Lines and ports from `/api/ferries` are an OpenStreetMap
  derivative: credit "© OpenStreetMap contributors" as well as OpenVan.camp, and keep a database
  you build from them under ODbL. Timetables carry the license of their GTFS feed (`sources`).
  `motorcar` missing means unknown, not "no cars"; `available: false` on a schedule means no open
  timetable, not "no ferry".
- **Hazards are the situation now**, not a forecast; a new fire bbox may answer "being loaded,
  retry in a minute" the first time.
- **Locales:** `en`, `ru`, `de`, `fr`, `es`, `pt`, `tr`.

## Limits and caching

120 requests per minute per IP (`X-RateLimit-*` headers; 429 when exceeded), 10 roadbooks per
minute, 60 per minute for plate images. Cache fuel prices for at least 6 hours (poll no faster
than every 10 minutes), currency rates for at least 1 hour, events and stories for at least
15 minutes. Plate image URLs are immutable — cache them forever. In a browser widget, fetch once
per page view; on a server, cache and serve your own copy.

## Minimal example

```html
<div id="fuel"></div>
<p class="credit"></p>
<script type="module">
  const res = await fetch("https://openvan.camp/api/fuel/prices?country=de&source=example.com", {
    headers: { Accept: "application/json" },
  });
  const { data, _attribution } = await res.json();
  const de = data.DE;
  document.getElementById("fuel").textContent =
    `Diesel in Germany: ${de.prices.diesel} ${de.currencies.diesel}/${de.units.diesel}`;
  document.querySelector(".credit").innerHTML = _attribution.attribution_html;
</script>
```

## Other ways in

- MCP server for AI agents: `https://mcp.openvan.camp/mcp` (see the `openvan-travel` skill).
- Daily CSV/JSON snapshots with history: <https://github.com/openvancamp/openvan-travel-data>.
- Questions and data corrections: issues at <https://github.com/openvancamp/openvan-camp-public-api>
  or hello@openvan.camp.
