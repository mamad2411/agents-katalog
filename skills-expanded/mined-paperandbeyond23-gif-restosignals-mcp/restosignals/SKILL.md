---
name: restosignals
description: Find restaurants, bars and cafés 1–6 months BEFORE they open, as a scored lead list. Use whenever the user wants new/upcoming/soon-to-open food & beverage venues, restaurant opening leads, pre-opening prospects for a city or state, or to watch an area for new openings. RestoSignals fuses government open-data (liquor licenses, food permits, new-business filings) into one deduped venue with an opening_score (0–100). US only; live states are returned by the `coverage` call. Not for already-open restaurant listings, reviews, or menus.
---

# RestoSignals — opening-restaurant leads for agents

RestoSignals turns raw government open-data into a clean, scored list of venues that are **about to open**. Each lead is one deduped venue with an `opening_score` (0–100) built by fusing up to three signal types: `liquor` (a liquor-license application/issuance), `food_permit` (a new food/health permit), and `business` (a new LLC/corp filing). More independent signals → higher score; a lone signal scores low, a 3-signal fused venue scores near 100.

**Base URL:** `https://api.restosignals.com`  ·  **MCP:** `https://api.restosignals.com/mcp`  ·  **Metering:** 1 credit = 1 returned lead (empty results are free).

## Authenticate
Every call needs an API key. Get one free (100 lead credits, no card) at https://restosignals.com/signup, or mint a smaller trial key:
```bash
curl -s -X POST https://api.restosignals.com/v1/register   # -> {"api_key":"pk_...","credits":15}
```
Send it as `X-API-Key: pk_...` (REST) or in the MCP client's auth header.

## Golden rule: check coverage first
Data exists only for some states. **Always discover live inventory before querying**, so you don't query an empty state:
```bash
curl -s "https://api.restosignals.com/v1/openings?state=NY&limit=5" -H "X-API-Key: pk_..."
```
Via MCP, call the free `coverage` tool. Live states with hot leads today: **NY, TX, IL, CA, OR**. CO and WA have venues but no hot leads yet. NY and IL have the most fully fused, high-score leads; TX is mostly single-signal (issued liquor).

## REST endpoints (all metered per returned lead unless noted)
- `GET /v1/openings?state=NY&min_opening_score=40&limit=10` — the core call (default limit 10; each lead costs 1 credit, so keep it small while testing). Returns scored, fused venues.
- `GET /v1/openings/latest?limit=10` — venues with a signal in the last 7 days.
- `GET /v1/signals?state=NY&limit=10` — the raw underlying signals (pre-fusion), for transparency.
- `GET /v1/export?state=NY&format=csv` — bulk CSV to a signed URL (1 credit/row).
- `POST /v1/webhooks` — register `{url, criteria:{state,city,signal_type,min_opening_score}}` to be POSTed new matches (free).
- `GET /v1/account`, `GET /v1/usage` — wallet balance and usage. Free.

### Response shape (`/v1/openings`)
```json
{
  "count": 2,
  "credits_used": 2,
  "credits_remaining": 48,
  "openings": [
    { "business_name": "DINER 24 BROADWAY NYC LLC.", "city": "New York", "state": "NY",
      "opening_score": 100, "signal_types": ["business", "food_permit", "liquor"], "status": "opening" },
    { "business_name": "MEDUSA ART STUDIOS & EVENTS", "city": "Astoria", "state": "NY",
      "opening_score": 90, "signal_types": ["food_permit", "liquor"], "status": "opening" }
  ]
}
```
`signal_types` values are exactly `liquor`, `food_permit`, `business` — nothing else.

## MCP tools (same key + wallet)
Connect the hosted server, then these tools are available:
- `coverage` — states + venue/hot-lead counts. **Free. Call first.**
- `new_openings` — `{state, min_score=30, limit=10}` → scored leads.
- `venue_signals` — `{venue_id}` → the raw signals fused into that venue.
- `watch_area` — `{url, criteria}` → webhook on new matches. Free.

MCP client config (Claude Desktop / Code, Cursor, etc.):
```json
{ "mcpServers": { "restosignals": {
  "url": "https://api.restosignals.com/mcp",
  "headers": { "Authorization": "Bearer pk_YOUR_KEY" }
} } }
```

## Recipes
- **"Find restaurants opening soon in New York, best first."** → `coverage` → `new_openings(state=NY, min_score=40)` → present name, city, score, signal_types.
- **"Only the strongest (multi-signal) leads."** → `min_score=80` (a fused venue always outranks any single-signal one).
- **"Alert me when a new bar files in Brooklyn."** → `watch_area(url=<your endpoint>, criteria={state:NY, city:Brooklyn, signal_type:liquor})`.
- **"Why is this venue scored 100?"** → `venue_signals(venue_id=…)` to show the underlying liquor/permit/filing rows.

## Honest limits (state these; don't overclaim)
- Live states are only what `coverage` returns (NY, TX, IL, CA, OR with hot leads today; CO/WA thin) — do not promise other states until they appear.
- Owner contact details are subscriber-only: free keys see `contact.locked`/`available` on each lead. Subscribers get the owner name from the filing, plus phone (NYC) and owner mailing address (TX, NY) where public records carry them.
- Signals are derived from public government open-data; RestoSignals is not affiliated with any government agency.
