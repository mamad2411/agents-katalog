---
name: ebay-seller
description: Guides the complete eBay.de selling process per item as a state machine. Use when the user wants to sell an item on eBay, attaches a photo of something to sell, or asks to research prices, draft a listing, or check on a running eBay listing. Triggers (EN) - "sell on eBay", "list this item", "create eBay listing". Triggers (DE) - "auf eBay stellen", "Artikel verkaufen", "eBay Anzeige", Foto eines Verkaufsobjekts.
---

# eBay-Seller

Guides each item through fixed phases. Per-item state lives in `<workspace>/ebay/items/<YYYY-MM-DD-slug>/state.json`. Seller defaults in `<workspace>/ebay/config.json`. Usually one new item per day; several items can run in parallel across different phases.

The listing text and item content are produced **in German** (target marketplace eBay.de), even though this guide is written in English.

`<workspace>` = the user's current project directory (fallback: ask). On Windows the `.claude` directory is under `%USERPROFILE%\.claude\`. References and templates live relative to this SKILL.md under `references/` and `templates/`.

## Requirements
- **Required:** Claude Code + the "Claude in Chrome" extension, and a Chrome where the user is **logged in to eBay.de**. Nothing else — runs on macOS and Windows.
- **Optional (convenience only):** Python 3 + `Pillow` for automatic photo enhancement (`scripts/enhance_photo.py`). **Without Python/Pillow the skill still works** — photos are used unedited (the user uploads them manually anyway).
- No installation needed: manage `state.json` directly (read/write JSON), no Python helper required.

## Safety gates (non-negotiable)
- **Never publish without explicit approval.** Fill the listing, then stop before the final click.
- Live price changes and counter-offers only after approval.
- Never retouch defects out of photos (see `references/compliance.md`).

## First run
If `<workspace>/ebay/config.json` does not exist, this is the first run: **first show a short quick-start** (3 sentences: drag in a photo + "sell on eBay"; you upload the photos yourself; nothing is published without your approval). Then create it from `templates/config-template.json` and ask the user for the fields (location/ZIP, shipping method+cost, returns, handling time, default sale format, tone). `ebay_benutzername` is optional. **Login is manual:** the user logs in to eBay in Chrome themselves — no password in chat, no Keychain setup needed.

## Every run
1. Scan `<workspace>/ebay/items/`. Show an overview: item × phase × today's task.
2. **New photo(s) on the message?** (one or more) — derive a rough name from the first photo, then search `items/` for an item with a similar name (dedupe). Match → ask whether it is the same item; if yes, add the new photos to the existing item. Otherwise create a new item (phase `neu`).
3. For items in `beobachten` and `live`: daily update — but only if `letzter_lauf` ≠ today (idempotency). Otherwise skip and report "already captured today".
4. The user drives the phase transitions.

**State handling:** read/write `state.json` directly. Save once at the end of a step; for daily updates set `letzter_lauf` to today's date in the same save. Never save mid browser step. (Optional, if Python is present: the helpers in `scripts/state.py` do the same.)

Note: phase values (`neu`, `beobachten`, `fertig_machen`, `einstellen`, `live`, `abgeschlossen`) and the JSON field names (`fotos`, `kategorie`, `artikelmerkmale`, `preis_history`, `preisvorschlag`, `letzter_lauf`, `listing_url`, `live_history`, …) are literal identifiers used by the templates and helpers — keep them exactly as written.

## Phases

### `neu` → identify
- See `references/item-identification.md`.
- Save all submitted photos under `photos/original-N.jpg` (1..n) and record them in `fotos[]` as `{original}` (first = main image).
- Fill `artikel`, `kategorie`, `artikelmerkmale` (as far as possible).
- First sold-price research (see `references/price-research.md`), write the first `preis_history` entry — only if `letzter_lauf` ≠ today (no double scraping).
- Phase → `beobachten`.

### `beobachten` → build price sense
- Daily (idempotent) capture sold prices + competition, append to `preis_history`.
- Show the trend (median/range over the days).
- User says "ready" → phase `fertig_machen`.

### `fertig_machen` → photos + price + text
- **Photo enhancement (optional):** if Python 3 + Pillow are present, enhance all photos — run from the skill folder:
  `cd "<skill-folder>" && python3 -c "from scripts import enhance_photo; print(enhance_photo.enhance_all('<absolute-item-path>/photos'))"`
  and write the returned `enhanced` names back into `fotos[]`. **Without Python/Pillow, skip this step** and use the original photos.
- Price suggestion from `preis_history` (median/range) with rationale → `preisvorschlag`. Range = fixed price resp. auction start price.
- Write the listing text from `templates/listing-template.md` → `listing.md` (see `references/listing-guide.md`). Write it in German.
- **Optimization** (see `references/optimization.md`): 80-character title with synonyms, main image = product, complete item specifics, format/best-offer strategy, optional free shipping, timing — present as suggestions to the user.
- User approval → phase `einstellen`.

### `einstellen` → fill the listing
- Browser: check tab context, open a new tab. **Make sure the user is logged in to eBay in Chrome** — if not, ask them to log in (see `references/login.md`). Then the eBay listing form.
- Fields from `state.json`/`config.json`: title, description, **category**, **item specifics**, condition, images (existing `fotos`, first = main image), price/format, shipping profile, location/ZIP.
- **The user uploads photos themselves** (programmatic file upload is blocked for automation): drag the enhanced or original photos into the photo area.
- Ask the user for any missing required fields.
- **STOP before the final publish.** After approval, publish, save `listing_url`, phase → `live`.

### `live` → monitor
- Daily (idempotent) read views/watchers/offers → `live_history` entry `{ datum, aufrufe, beobachter, angebote }`.
- Anomalies (few views, many watchers without purchase) → SUGGEST a price/text adjustment, change only after approval.
- Sold/ended → phase `abgeschlossen`.

### `abgeschlossen`
End state, folder kept for history.

## Browser notes
- The eBay tools (Claude in Chrome) are deferred → load via ToolSearch before use (`select:mcp__claude-in-chrome__...`).
- Before any eBay action make sure the user is logged in; on 2FA/captcha, stop and ask the user.
- Work throttled (see `references/price-research.md`).
