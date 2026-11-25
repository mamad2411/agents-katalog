---
name: grand-bazaar
description: >-
  Create Etsy listings as DRAFTS on the user's own shop from a folder of product
  photos, in one shot: read the photos, infer style/price/category from the shop's
  existing active listings, write SEO titles + descriptions + tags, optional
  multilingual translations and variations, then create the draft via the Etsy
  Open API v3 (OAuth2/PKCE, auto token refresh). Use when the user wants to upload,
  create, or publish a product / listing / annuncio on Etsy, turn a photo folder
  into an Etsy listing, or "carica questo prodotto su Etsy". Generic and shop-agnostic:
  tone, languages, and copy rules come from a personal shop-profile file.
allowed-tools: Bash(python3 *), Bash(python *), Bash(py *)
---

# Etsy Upload

Standing guidance for turning a folder of product photos into a **draft** Etsy
listing on the user's own shop, in a single confirmation step. The skill is
**generic** — every shop-specific decision (brand voice, target languages,
price band, materials policy) is read from a personal **shop profile** file, not
hardcoded here.

## Operating principles (read first)

1. **Drafts only, never publish.** Every listing is created with `state=draft`.
   The user publishes manually from Etsy after review. Never set `state=active`.
2. **One-shot when you can infer, guided when you can't.** With existing active
   listings to learn from, do it all in one pass: look at the photos, read a few
   of the shop's listings to infer style/price/category, build the whole payload,
   show **one** compact summary, wait for a plain yes/no. Don't use
   `AskUserQuestion` for minor decisions (price, dimensions, material, `who_made`,
   `when_made`, taxonomy, cover image, image order) — pick sensible defaults. But
   the **first listing of an empty shop** has nothing to infer from: in that case
   switch to guided mode (see step 3a) instead of inventing everything.
3. **Confirm before the irreversible call.** Show the summary and get a yes
   before running `create_listing.py`. Approval for one listing is not approval
   for the next — confirm each.
4. **Never expose secrets.** Never print `client_secret` or tokens in a reply.
5. **Report Etsy's errors verbatim.** On API error, show Etsy's textual message
   (it usually names the exact bad field) — don't invent diagnostics.

## Setup (run this FIRST, before any other step)
This skill needs the items below. On invocation, verify each and guide the user
to fix anything missing **before** doing real work. Secrets and per-shop data
live **outside this repo** in a data dir (default `~/.claude/etsy-tools/`,
override with the `ETSY_TOOLS_DIR` env var) so nothing is ever committed.

- **Tools:** a Python 3 interpreter, stdlib only (no pip installs). Detect the
  command — try `python3`, else `python`, else (Windows) `py` — with
  `command -v python3 || command -v python || command -v py`. Use whichever exists
  in place of `python3` in the commands below (on Windows it's usually `python`/`py`).
- **Data dir + config:** `${ETSY_TOOLS_DIR:-~/.claude/etsy-tools}/config.json`
  must exist with `client_id` and `client_secret` (Etsy app keys from
  <https://www.etsy.com/developers/your-apps>). Copy the template:
  `cp "${CLAUDE_SKILL_DIR}/scripts/config.example.json" ~/.claude/etsy-tools/config.json`
  and fill `client_secret`. On the Etsy app, register the callback
  `http://localhost:3003/oauth/callback`.
- **OAuth tokens:** `${ETSY_TOOLS_DIR}/.auth.json` must exist. If missing, run
  the one-time browser flow:
  `python3 "${CLAUDE_SKILL_DIR}/scripts/auth.py"`
- **Shop discovery:** `config.json` needs `shop_id`. If `null`, run
  `python3 "${CLAUDE_SKILL_DIR}/scripts/get_shop_info.py"` — it saves `shop_id`
  and prints shipping profiles / sections / return policies. The user pastes the
  chosen `default_shipping_profile_id` (required to later publish) and, if the
  shop has return policies, `default_return_policy_id` into `config.json`.
- **Shop profile (personalization):** optional but recommended. If
  `${ETSY_TOOLS_DIR}/shop-profile.md` exists, **read it first** and follow it for
  brand voice, target languages, terminology, price band, and materials policy.
  If absent, infer everything from the shop's existing listings and offer to
  create one from
  [references/shop-profile.example.md](references/shop-profile.example.md).

If any step is missing, stop and ask the user to complete it — do not proceed
ignoring the error.

## When to use
The user says things like "carica questo prodotto su Etsy", "crea una listing /
annuncio Etsy da queste foto", "upload this to my Etsy shop", "make an Etsy
draft from this folder". Hands you a folder of photos (± a price).

## Workflow (create a draft listing)

1. **Read the shop profile** (`${ETSY_TOOLS_DIR}/shop-profile.md`) if present —
   it overrides the generic defaults below.
2. **Look at the photos** (Read tool on each image in the folder).
3. **Sample 1–3 similar active listings** to infer style, price band,
   `taxonomy_id`, typical tags, `when_made` — via `GET /shops/{shop_id}/listings/active`
   using the `etsy.api` helper.
3a. **If there are no (or no similar) active listings** — e.g. a brand-new shop's
   first product — you have nothing to infer from. **Do not invent** price/category
   silently. Switch to **guided mode**: ask the user a few targeted questions in
   chat (or one `AskUserQuestion`) for the things you cannot derive — category /
   `taxonomy_id`, price (band), target languages, tone/voice. Then **offer to save
   their answers as `shop-profile.md`** (see Setup) so every following product is
   one-shot again. Photos still drive the description; only the un-inferrable
   fields are asked.
4. **Build the full payload** in memory (title ≤140 char SEO, description, tags
   ≤13 each ≤20 char, materials, estimated dimensions, price aligned to similar
   items, translations + variations if the profile asks for them). The payload
   **schema** (every field create_listing.py accepts) is documented in
   [references/listing.example.json](references/listing.example.json) — it is a
   field reference, NOT example copy to imitate; voice/content come from the
   photos, the shop's real listings, and `shop-profile.md`.
5. **Save** it to `/tmp/listing.json`.
6. **Show one compact summary** (titles per language, tags, price, attached
   files) — not the full JSON inline. Wait for a textual yes/no.
7. On yes → run `python3 "${CLAUDE_SKILL_DIR}/scripts/create_listing.py" /tmp/listing.json`
   (or pipe JSON via stdin with `… create_listing.py -`). On no → ask what to change.
8. **Report**: `listing_id`, admin URL
   (`https://www.etsy.com/your/shops/me/tools/listings/{id}`), and whether images
   uploaded.

### Fields
| Field | Required | How to get it |
|---|---|---|
| `title` | yes | ≤140 char, SEO-optimized |
| `description` | yes | propose a draft for approval |
| `price` | yes | shop currency; infer from similar listings or ask one line |
| `quantity` | no (default 1) | — |
| `taxonomy_id` | yes | see below |
| `tags` | recommended | max 13, each ≤20 char |
| `materials` | recommended | max 13 (profile may say leave empty) |
| `who_made` | no (`i_did`) | `i_did` / `someone_else` / `collective` |
| `when_made` | no (`made_to_order`) | e.g. `made_to_order`, `2020_2026` |
| `is_supply` | no (false) | true for supplies |
| `image_paths` | recommended | absolute paths; first = cover |
| `video_path` | optional | max 1, ~100MB / ~15s, uploaded after images |
| `translations` | per profile | `{lang: {title, description, tags}}` |
| `variations` | optional | single listing with variants, not duplicates |

### Translations
Target languages come from the **shop profile** (e.g. `en`, `fr`, `es`, `de`).
Each needs `title` (≤140), `description`, `tags` (≤13, each ≤20 char), in the
same voice as the primary language.

### Variations (when the product has configurations)
One listing with `variations`, not duplicate listings:
```json
"variations": {
  "property_name": "Size",
  "options": [
    {"name": "S", "price": 165.00, "quantity": 1, "sku": "..."},
    {"name": "M", "price": 165.00, "quantity": 1, "sku": "..."}
  ]
}
```
**Etsy API v3 limit:** there is no public endpoint to translate variation
*names* into other languages reliably, so use **cross-language universal**
option names (`Size` → `S`/`M`/`L`, `Length` → `40cm`/`50cm`). Explain what each
means in the per-language description. `set_inventory()` adds the required
`readiness_state_id` automatically for physical listings.

### Finding `taxonomy_id`
Common handmade-jewelry nodes: `1216` Rings, `1183` Necklaces, `1184` Bracelets,
`1209` Earrings. If unsure, list seller taxonomies:
```bash
python3 -c "import sys; sys.path.insert(0,'$CLAUDE_SKILL_DIR/scripts'); \
from etsy import api; import json; print(json.dumps(api('GET','/seller-taxonomy/nodes'),indent=2)[:5000])"
```

### Recovery
If `create_listing.py` fails mid-way (e.g. on `set_inventory`), the listing
already exists with images. Resume the missing steps:
`python3 "${CLAUDE_SKILL_DIR}/scripts/finish_listing.py" <listing_id> /tmp/listing.json`

## Files
- `scripts/etsy.py` — Etsy API v3 client (stdlib only, auto token refresh)
- `scripts/auth.py` — one-time OAuth2/PKCE flow → `.auth.json`
- `scripts/get_shop_info.py` — discover shop_id / profiles / sections / policies
- `scripts/create_listing.py` — create draft + upload images/video + translations
- `scripts/finish_listing.py` — resume a half-created listing
- `scripts/config.example.json` — config template (NO secrets)
- `references/listing.example.json` — payload schema
- `references/shop-profile.example.md` — personalization template

Secrets (`config.json`, `.auth.json`) and the personal `shop-profile.md` live in
`${ETSY_TOOLS_DIR:-~/.claude/etsy-tools}/`, never in this repo.
