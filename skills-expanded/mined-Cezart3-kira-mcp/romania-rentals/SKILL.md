---
name: romania-rentals
description: Search live apartment rentals (chirii) anywhere in Romania — any city, town or commune — across storia.ro, publi24.ro and lajumate.ro, with heating type, parking and walking distance extracted from the ad text. Use when the user wants to rent a flat or a parking spot in Romania, compare rents, or check an ad.
---

# Romanian rentals (kira)

Live search of rental listings in Romania. Covers all 3,100+ localities
(municipii, orașe, comune), not only the big cities.

## How to call it

**If the `kira` MCP tools are available** (`search_rentals`,
`get_listing_details`, `search_parking`, `find_locality`), use them.

**Otherwise use the CLI** (needs `uv`; no install step):

```bash
uvx --from kira-rentals-mcp kira --json search "Cluj-Napoca" --rooms 2 --max-price 500
uvx --from kira-rentals-mcp kira --json listing "<ad url>"
uvx --from kira-rentals-mcp kira --json parking "Brasov" --max-price 80
uvx --from kira-rentals-mcp kira --json find "Floresti"
```

## Search options

| Option | Meaning |
|---|---|
| `city` (+ `--county`) | Any Romanian locality. Diacritics optional. Ambiguous names (there are 6 Floreștis) pick the largest unless a county is given: `"Floresti, Prahova"`. |
| `--min-price` / `--max-price` | Monthly rent in **EUR** (RON ads converted at ~5 RON/EUR). |
| `--rooms 1 2` | 1 = garsonieră/studio; 4 means 4+. |
| `--heating` | `centrala_proprie` (own gas boiler) or `termoficare` (district or shared building heating — not the flat's own boiler). |
| `--parking` | Any of `included`, `likely_included`, `area_possible`, `none`, `unknown`. |
| `--owner-only` | Private owners only (no agency fee) — only where the site states it. |
| `--keywords` | Words that must **all** appear in the ad (e.g. `"balcon mobilat"`, `"Zorilor"`). |
| `--near "UMF"` + `--max-walk 20` | Walking distance from a place (via OpenStreetMap); combine with `--sort distance`. |
| `--sort` | `newest` (default), `price_asc`, `price_desc`, `distance`. |

## Working well with it

1. A search takes 5–20 s (live, polite request rate). Ask for the user's
   must-haves first and run **one well-filtered search**, not many broad ones.
2. Heating and parking come from the ad text. When `parking` or `heating` is
   `unknown`, say so — don't guess. `get_listing_details` reads the full ad.
3. `distance.precision` is `street` or `district`; treat `district` distances as
   rough. Listings without a `distance` could not be placed (the ad gives no
   street or neighbourhood) — they are listed after the located ones; mention
   them rather than silently dropping them.
4. Always give the ad link. Contact details are deliberately not returned —
   the user contacts the owner on the site.
5. OLX and imobiliare.ro are not searched (they block automated access). If
   the user wants maximum coverage, tell them to check those sites too.
6. Ads are in Romanian; answer in the user's language and translate what
   matters (e.g. "centrală proprie" = own boiler, "fără comision" = no agency fee).
