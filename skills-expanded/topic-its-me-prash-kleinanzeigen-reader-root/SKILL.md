---
name: kleinanzeigen-reader
version: 1.2.0
description: >
  Read, scrape, and analyze ANY listing from kleinanzeigen.de — cars, electronics,
  furniture, real estate, clothing, or any other category. Use this skill whenever
  the user shares a kleinanzeigen.de URL, asks to "check this listing", wants to
  compare multiple ads, needs to detect if a seller is a dealer or private person,
  wants to find duplicate listings, or asks "is this a good deal?" for any German
  classifieds ad. Works without Playwright or external APIs.
---

# Kleinanzeigen Reader — Universal Listing Analyzer

Extracts structured data from any kleinanzeigen.de listing using three built-in
HTML data sources. No browser automation, no paid APIs, no external dependencies.

---

## Quick Start

When a user shares a `kleinanzeigen.de/s-anzeige/...` URL:

1. **Fetch** the page → `scripts/fetch.sh [URL]` or inline curl (Step 1)
2. **Extract** all data → `python3 scripts/extract.py listing.html`
3. **Identify category** → auto-detect from `ad_attributes` or title
4. **Apply category rules** → load the relevant reference file
5. **Output** structured result with flags and recommendation

For multiple URLs → use compare mode (Step 5).

---

## Step 1 — Fetch the Listing

```bash
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1" \
  -H "Accept-Language: de-DE,de;q=0.9" \
  -H "Referer: https://www.kleinanzeigen.de/" \
  --compressed \
  "[URL]" > /tmp/listing.html
```

**Why iPhone UA:** Kleinanzeigen blocks headless/server requests but allows
mobile Safari — this is a well-documented characteristic of their bot filter.

---

## Step 2 — Three Data Sources (Always Present)

### Source A — Schema.org JSON-LD
SEO requirement. Always in `<script type="application/ld+json">`.
Contains: title, description, asking price, main image URL.

### Source B — `ad_attributes` GTM String
All structured attributes packed into a pipe-separated string for Google Tag Manager:
```
km:95000|aussenfarbe:schwarz|schaden:t|power:150|tuevdate:2026-08|...
```
→ See `references/ad-attributes-fields.md` for complete field list.

### Source C — DFP Bidder Block
A second JS block with cleaner values for key fields:
`ExactPreis`, `Kilometerstand`, `Erstzulassung`, `HU_bis`, `Marke`, `Getriebe`

### Source D — Seller Type
- `"li":"0"` in GTM = **Privater Anbieter**
- `"li":"1"` in GTM = **Gewerblicher Händler**
- Confirmed by text badge: "Privater Nutzer" vs "Gewerblicher Anbieter"
- `"lsc":["0"]` = additional private/commercial signal

---

## Step 3 — Dealer Detection

Extract and evaluate **four dealer signals** — combine for confidence score:

| Signal | Where | Private | Dealer |
|---|---|---|---|
| `li` field | GTM JS | `"0"` | `"1"` |
| `lsc` field | GTM JS | `["0"]` | `["1"]` or higher |
| Badge text | HTML | "Privater Nutzer" | "Gewerblicher Anbieter" / "Händler" |
| Ad volume | Other ads URL | Low | High (fetch counter if needed) |

**Output format:**
```
Verkäufertyp: ✅ Privat  /  ⚠️ Gewerblich (Händler)
```

**Why this matters:**
- Dealers must provide 2-year statutory warranty (§ 475 BGB) — negotiating room is different
- Private sellers can exclude warranty entirely
- Dealer listings often have inflated prices vs. identical private listings
- Some "private" listings are actually undeclared commercial sellers (grey zone)

**Undeclared dealer heuristics** (flag if 2+ match):
- Title uses commercial language ("sofort verfügbar", "Händler", "Bestand")  
- Multiple identical or very similar listings from same seller
- Price is at or above market rate with no personal story in description
- Description is structured/template-like (no typos, no personal details)
- Generic stock photos (no personal garage / street background)

---

## Step 4 — Universal Category System

Auto-detect category from `ad_attributes` fields or listing title, then load
the matching reference file for category-specific analysis.

| Category | Detection | Reference File |
|---|---|---|
| **Fahrzeuge** | `marke`, `km`, `fuel`, `power` present | `references/categories/fahrzeuge.md` |
| **Immobilien** | `zimmer`, `wohnflaeche`, `mietpreis` present | `references/categories/immobilien.md` |
| **Elektronik** | `zustand` + known brands (Apple, Samsung...) | `references/categories/elektronik.md` |
| **Möbel & Haushalt** | No vehicle/immo fields, physical object | `references/categories/moebelhaushalt.md` |
| **Allgemein** | No category match | Apply generic output only |

If category is unclear → use generic output (Step 4b) without loading a reference file.

---

## Step 4a — Category-Specific Flags

### Fahrzeuge (see `references/categories/fahrzeuge.md`)
- `schaden:t` = declared damage → always highlight
- `tuevdate` expired = HU fällig → cost ~€80–150
- KM > 300k = high mileage note
- Motor identification from PS + build year (BMW N47/M47, VW TDI etc.)
- Duplicate detection: same car listed twice at different prices

### Immobilien
- `zimmer` count vs. `wohnflaeche` ratio → abnormal if < 15m² per room
- `kaltmiete` vs. area median (flag if > 30% above)
- Missing fields: no floor plan, no energy certificate mentioned

### Elektronik
- `zustand` field: `neu`, `wie_neu`, `gut`, `akzeptabel`, `defekt`
- `defekt:t` equivalent = listed under "Defekt / Bastlerware"
- Price vs. idealo/Amazon median (mention to check externally)
- Serial number fraud risk for high-value items (MacBooks, iPhones)

### Möbel & Haushalt
- No structural red flags — focus on description quality and seller type
- Note if price > 60% of new price (rarely worth it for furniture)

---

## Step 4b — Universal Output Format

Use this format for **all categories**:

```
## [Title]

**Kategorie:** [detected category]
**Verkäufertyp:** ✅ Privat  /  ⚠️ Gewerblich

| Feld          | Wert                          |
|---------------|-------------------------------|
| Preis         | X.XXX € [VB / Festpreis]      |
| Standort      | [PLZ City]                    |
| Datum         | [listing date]                |
| Zustand       | [if present]                  |
| [cat fields]  | [category-specific rows]      |

**Beschreibung:** [original text]

**⚠️ Flags:**
- [flag 1]
- [flag 2]

**Bilder:** [N] Fotos verfügbar
[image URLs listed]

**Gesamtbewertung:** ★★★☆☆  [short reasoning]
```

---

## Step 5 — Comparison Mode

When 2+ URLs are given, fetch all listings then produce:

```
| Merkmal        | Inserat 1   | Inserat 2   | Inserat 3   |
|----------------|-------------|-------------|-------------|
| Preis          | ...         | ...         | ...         |
| Verkäufertyp   | Privat ✅   | Händler ⚠️  | ...         |
| [cat fields]   | ...         | ...         | ...         |
| Flags          | ...         | ...         | ...         |
| Bewertung      | ★★★☆☆      | ★★☆☆☆      | ...         |
```

**Duplicate detection:** If ≥5 fields match across listings AND location matches
→ flag as probable same item listed twice (common seller tactic to test prices).

---

## Step 6 — Images

Download with:
```bash
curl -s -L \
  -H "Referer: https://www.kleinanzeigen.de/" \
  "[IMAGE_URL]" -o image.jpg
```

URL format: `https://img.kleinanzeigen.de/api/v1/prod-ads/images/[2ch]/[UUID]?rule=X`

Image rules (empirically verified 2026-08-01 — `$_57` is the **largest**, not a thumbnail):

| Rule | Size | Use |
|---|---|---|
| `$_57.JPG` | **1600 × 1096** | **Default — maximum resolution** |
| `$_45.JPG` | 1200 × 822 | Medium |
| `$_59.JPG` | 960 × 658 | Small |
| `$_2.JPG` | original | Full / damage inspection |

Suffix: `.JPG` = JPEG (readable everywhere), `.AUTO` = AVIF (smaller, needs AVIF viewer).

---

## Step 7 — Signals (demand · seller · price)

Beyond the static page, `kl_reader.signals` adds read-only signals (all public or
your-own-account):

```python
from kl_reader.signals import view_counter, seller_other_ads, price_reduction, detect_status, PriceTracker

view_counter(url)              # numVisits — high views + old ad = overpriced/stale
detect_status(html)            # active | reserved | sold | deleted
price_reduction(html)          # native "was X, now Y" if the ad was discounted
seller_other_ads(html)         # the seller's other active ads (private sellers too)
PriceTracker().record(id, p)   # snapshot price over time → build a real price history
```

Full CAPI map, auth scheme, and hidden ad fields (exact lat/long, member-since,
timestamps, price type): **`references/mobile-api.md`**.

---

## Step 8 — Authenticated mode (optional, bring your own session)

With your **own** kleinanzeigen.de session you get what the platform serves to any
logged-in user (same as the official app). Grab a Bearer from DevTools → Network →
`api.kleinanzeigen.de` → `Authorization` header; pass via `KA_BEARER` or `Session(bearer=…)`.

```python
from kl_reader import Session
s = Session(bearer="eyJ…")
s.visitors(adId)   # 👀 views for ANY ad (no starring)   ·  s.watchers(adId)  # ⭐
s.ad(adId)         # full ad JSON                          ·  s.my_ad(id, "paused")  # your own
```

Login does **not** expose other users' paused/deleted/draft ads (owner-scoped → 403).
Details: `references/mobile-api.md` §8.

---

## Scope & Ethics

- Read-only, public data or **your own** account only.
- **Reserved** ads are public → detect and report them.
- **Deleted / expired** ads: recover from the Wayback Machine / search cache, or (for
  your own ads) via your logged-in account — never by probing other users' private IDs.
- Do **not** read other users' paused/deactivated/draft ads, and do **not** edit/delete
  listings that aren't yours — those endpoints are bound to the owner's login (see
  `references/mobile-api.md` §7).

---

## Limitations

- `kleinanzeigen.de` web URLs only — convert app share links first
- `ezdate` / `tuevdate` = current month if seller left field blank
- Personal data in listing descriptions (phone numbers, names) — do not store or repeat
- Rate limit: add `sleep 1` between requests for batch operations
- For research/personal use only — respect kleinanzeigen.de ToS

---

## Reference Files

- `references/mobile-api.md` — **Mobile CAPI map, auth scheme, hidden fields (RE)**
- `references/ad-attributes-fields.md` — All GTM field names + values
- `references/categories/fahrzeuge.md` — Vehicle-specific analysis rules
- `references/categories/elektronik.md` — Electronics flags + fraud indicators
- `references/categories/immobilien.md` — Real estate checks
- `references/categories/moebelhaushalt.md` — Furniture/household rules
