# Skill: Query declassified Pentagon UAP records (uap-pulse)

Search and map 350 official-government UAP/UFO records spanning 1944–2026: all four U.S. Pentagon PURSUE releases plus curated archives from 12 nations.

## Install (MCP server, no auth)

```
npx -y uap-pulse
```

Add to any MCP client:

```json
{ "mcpServers": { "uap-pulse": { "command": "npx", "args": ["-y", "uap-pulse"] } } }
```

## Tools

- `search_sightings(query?, release?, agency?, type?, year_start?, year_end?, location?, limit?)`
- `search_nearby(latitude, longitude, radius_km?, limit?)`
- `get_sighting(id)` — full record + war.gov source link
- `full_text_search(query, limit?)` — relevance-ranked
- `notable_cases(key?)` — curated historic cases
- `hotspots(limit?)`, `stats()`, `timeline(granularity?)`, `timeline_data(granularity?)`

## Data

- Raw JSON (CORS-open): https://uap-pulse.vercel.app/sightings.json
- Source: war.gov PURSUE Releases 1–4 — U.S. public domain (17 U.S.C. § 105) — plus official national archives
- 350 records · 334 U.S. files · 16 curated international cases · 275 geolocated · 20 off-world
- Latest tranche: `search_sightings(release=4, limit=100)` returns all 40 files published July 10, 2026

## Links

- Live map: https://uap-pulse.vercel.app
- GitHub: https://github.com/davidmosiah/uap-pulse
- npm: https://www.npmjs.com/package/uap-pulse
