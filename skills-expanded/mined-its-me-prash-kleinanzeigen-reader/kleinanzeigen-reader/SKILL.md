---
name: kleinanzeigen-reader
version: 1.2.0
description: >
  Analyze any kleinanzeigen.de listing — cars, electronics, real estate, furniture —
  with dealer detection, damage flags, duplicate detection, and image extraction.
  ALWAYS use this skill when the user shares any link containing "kleinanzeigen.de",
  pastes a Kleinanzeigen URL, says "schau dir diese Anzeige an", "check this listing",
  "analysiere das Inserat", "ist das ein guter Deal", "Händler oder Privat?",
  "is this a scam", "Kleinanzeigen prüfen", or any variation asking about a German
  classifieds ad. Also triggers for "compare these listings", "Inserate vergleichen",
  or when multiple Kleinanzeigen URLs are shared. Works WITHOUT API keys, no login,
  no Playwright — pure Python stdlib. Supports all categories.
---

# Kleinanzeigen Reader — Claude Skill

## When to Use

Trigger this skill when ANY of these are true:
- URL contains `kleinanzeigen.de/s-anzeige/`
- User says: "schau dir an", "check", "analysiere", "guter Deal?", "Händler?"
- Multiple Kleinanzeigen URLs shared for comparison
- User asks about damage, TÜV, km, seller type on any German classifieds link

---

## Step 1 — Copy the analyzer to working directory

```bash
cp -r /mnt/skills/user/kleinanzeigen-reader/kl_reader /home/claude/kl_reader
```

---

## Step 2 — Fetch the listing

```bash
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1" \
  -H "Accept-Language: de-DE,de;q=0.9" \
  -H "Referer: https://www.kleinanzeigen.de/" \
  --compressed \
  "[URL]" > /tmp/listing.html
```

---

## Step 3 — Run the full pipeline

```python
import sys
sys.path.insert(0, '/home/claude')

from kl_reader.extractor import extract
from kl_reader.analyzer  import get_flags, get_rating
from kl_reader.images    import download

with open('/tmp/listing.html') as f:
    html = f.read()

data   = extract(html)
flags  = get_flags(data)
rating = get_rating(data, flags)

# Download images
if data.get('images'):
    saved = download(data['images'], '/tmp/kl_images', size='medium')
```

---

## Step 4 — Output format

Present results using this structure:

```
╔══════════════════════════════════════════════════════════════╗
║                   KLEINANZEIGEN READER                       ║
╠══════════════════════════════════════════════════════════════╣
║  Titel               [title]                                 ║
║  Kategorie           [category]                              ║
║  Verkäufer           ✅ Privat / ⚠️ Gewerblich               ║
║  Preis               X.XXX €                                 ║
║  Standort            [PLZ City]                              ║
╠══════════════════════════════════════════════════════════════╣
║  [Category-specific rows]                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Bewertung           ★★☆☆☆                                   ║
╚══════════════════════════════════════════════════════════════╝

⚠️  FLAGS
    🔴  SCHADEN deklariert (schaden:t)
    🟡  Hoher Kilometerstand: 380.001 km
    🟡  TÜV wahrscheinlich abgelaufen

📝  BESCHREIBUNG
    [original text, word-wrapped]

🖼️  BILDER
    [image URLs or downloaded paths]
```

**Bewertung key:**
- `schaden:t` = −2 stars
- KM > 250k = −1 star
- TÜV not filled = −1 star
- Each 🔴 flag = −1 star

---

## Step 5 — Dealer detection logic

| Signal | Field | Private | Commercial |
|---|---|---|---|
| Primary | `li` in GTM JS | `"0"` | `"1"` |
| Secondary | `lsc` field | `["0"]` | other |
| Badge text | HTML | "Privater Nutzer" | "Gewerblicher Anbieter" |
| Heuristic | Text keywords | — | 2+ commercial terms |

Commercial keywords that trigger undeclared dealer flag:
`händler`, `autohaus`, `sofort verfügbar`, `gewährleistung`, `finanzierung`, `inzahlungnahme`

**Legal note when commercial:** mention § 475 BGB — 2-year statutory warranty applies.

---

## Step 6 — Comparison mode (2+ listings)

Fetch and extract each listing, then show side-by-side:

```
  Merkmal               Inserat 1              Inserat 2
  ──────────────────────────────────────────────────────
  Preis                 1.400 €                1.300 €
  Verkäufer             ✅ Privat               ✅ Privat
  Kilometerstand        380.001 km             380.193 km
  Schaden               ⚠️  JA                 ⚠️  JA
  Bewertung             ★☆☆☆☆                  ★☆☆☆☆

  ⚠️  DUPLIKAT — wahrscheinlich dasselbe Fahrzeug zweimal inseriert
      KM-Differenz: 192 km — 7 übereinstimmende Felder
```

Duplicate threshold: ≥4 matching fields + KM diff < 1000 + same damage status.

---

## Key data sources (reference)

| Source | Location in HTML | Contains |
|---|---|---|
| JSON-LD | `<script type="application/ld+json">` | Title, price, images |
| `ad_attributes` | GTM JS string | All vehicle/item attributes |
| `li` field | GTM JS | `0`=private, `1`=dealer |
| DFP block | GTM JS | Clean price, km, EZ |
| CDN images | `contentUrl` in JSON-LD | Direct image URLs |

---

## Step 7 — Signals (demand · seller · price)

```python
from kl_reader.signals import view_counter, seller_other_ads, price_reduction, detect_status, PriceTracker

view_counter(url)          # numVisits — high views + old ad = overpriced/stale
detect_status(html)        # active | reserved | sold | deleted
price_reduction(html)      # native "was X, now Y" if the ad was discounted
seller_other_ads(html)     # the seller's other active ads (private sellers too)
PriceTracker().record(id, price)   # snapshot over time → your own price history
```

Images: `download(urls, dir, size=...)` where size ∈ `thumb`/`medium`/`large`/`full`.
`large` (`$_57.JPG`, 1600×1096) is the default and the maximum resolution.

**Authenticated mode (optional):** with your own session token you get what the platform
serves any logged-in user — 👀 views / ⭐ watchers for ANY ad (no starring), full ad JSON,
and your own paused ads. Grab a Bearer from DevTools (`api.kleinanzeigen.de` → Authorization):

```python
from kl_reader import Session
s = Session(bearer="eyJ…")           # or KA_BEARER env var
s.visitors(adId); s.watchers(adId); s.ad(adId); s.my_ad(id, "paused")
```

Login does **not** expose other users' paused/deleted/draft ads (owner-scoped → 403).

---

## Scope & Ethics

- Read-only, public data or **your own** account only.
- Reserved ads are public → detect and report. Deleted/expired ads: recover via
  Wayback Machine / search cache, or your own account — never by probing other users' IDs.
- Do **not** read other users' paused/draft ads or edit/delete listings that aren't yours.

---

## Notes

- `kleinanzeigen.de` web URLs only — convert app share links first
- `ezdate`/`tuevdate` default to current month if seller left blank — flag this
- For personal/research use — not for bulk scraping
- Optional: install `curl_cffi` for a Chrome-TLS fetch that beats DataDome
  (auto-detected; falls back to stdlib urllib if absent)
