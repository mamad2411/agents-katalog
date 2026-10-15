---
name: shopify-clone-store
description: >
  Clone a public Shopify storefront (catalog + look) onto a shop the user owns
  using Shopify CLI OAuth and Admin GraphQL. Rebuild on Horizon / OS 2.0 — do
  not steal the source theme. Use when the user says clone this Shopify site,
  replica store, copy this brand onto my myshopify store, rebuild a brand on a
  test shop, or runs /shopify-clone-store. Never commit tokens.
when-to-use: clone this Shopify site, replica store, copy this brand onto my myshopify store, rebuild a brand on a test shop, /shopify-clone-store
argument-hint: "<source-url> [shop.myshopify.com]"
license: MIT
compatibility: Requires Shopify CLI (@shopify/cli), Shopify AI Toolkit (shopify-admin + shopify-use-shopify-cli), Python 3, and network access
metadata:
  author: thomasavada
  version: "1.3"
  short-description: "Clone a Shopify storefront onto a shop you own"
---

# Shopify clone store

Rebuild a **public Shopify storefront** on a **target shop** the user owns: products, collections, pages, menu, and a matching theme. Source of truth is the live site + Admin API, not memory.

This file is an **agent prompt**. Human install notes live in `README.md`.

`SKILL_DIR` = dirname of this `SKILL.md` (the skills list announces the path). Scripts and references are relative to that directory — never hardcode `~/.claude/skills/shopify-clone-store`.

Load **shopify-admin** + **shopify-use-shopify-cli** when writing or running Admin GraphQL.

Slash form: `/shopify-clone-store <source-url> [shop.myshopify.com]`

## Steps

### 0. Prerequisites

Need **Shopify CLI** and the **Shopify AI Toolkit**. If either is missing, stop and install — do not continue the clone.

1. `shopify version` — if missing: `npm install -g @shopify/cli@latest`
2. Toolkit is present when the loaded skills include **shopify-admin** and **shopify-use-shopify-cli**. If they are absent, tell the user to install then **restart the session**:

```
# Claude Code (default)
claude plugin install shopify-ai-toolkit@claude-plugins-official

# Codex
codex plugin add shopify@openai-curated

# Grok (no official plugin)
npx skills add Shopify/shopify-ai-toolkit -g -a grok -y
```

Ready when `shopify store execute --help` works **and** those two skills are loaded. Full install table: `README.md`.

### 1. Gather inputs

Ask if missing:

1. Source URL (e.g. `https://www.example.com`)
2. Target `*.myshopify.com`
3. Admin access: **OAuth** via `shopify store auth` (default). A pasted `shpat_` custom-app token is fallback only.

**No source URL:** do not pick a brand. Offer a short list from [references/clone-roster.md](references/clone-roster.md) (Chase Chappell atlas, Shopify-readable only). Probe `products.json` this run, group by beauty / apparel / supplement / beverage, 8–12 options max. They pick one or paste their own URL. Then continue.

Do not copy a merchant's paid/custom theme Liquid from their CDN. Recreate the look with OS 2.0 sections + CSS on Horizon (or a small custom theme).

### 2. Auth (OAuth default)

**Prefer OAuth. Do not ask for an API key.** `shopify store auth` opens the Admin consent screen, stores an online token in the CLI, and every later Admin call is `shopify store execute`. `shopify store auth` cannot ingest `shpat_`.

Clone scopes (`write_*` includes read):

```
write_products,write_files,write_themes,write_theme_code,write_online_store_pages,write_online_store_navigation,write_publications
```

Do not add `read_all_orders` or other gated scopes — the CLI connector app fails the handshake.

1. `shopify store auth list` — if the target shop is already listed, skip to 3.
2. If missing, run (browser; the user must click **Install / Allow**):

```
shopify store auth --store <shop>.myshopify.com --scopes write_products,write_files,write_themes,write_theme_code,write_online_store_pages,write_online_store_navigation,write_publications
```

Tell them to approve in the browser. Do not ask them to paste a token.

3. Every Admin GraphQL call:

```
shopify store execute --store <shop>.myshopify.com --query '{ shop { name myshopifyDomain } }' --json
```

Mutations **must** add `--allow-mutations`. Large variables: `--query-file` + `--variable-file` (see `scripts/import_catalog.py`).

Probe after auth:

```
shopify store execute --store <shop>.myshopify.com --query '{ shop { name myshopifyDomain } currentAppInstallation { accessScopes { handle } } publications(first: 10) { nodes { id name } } }' --json
```

Note the **Online Store** publication GID. Products/collections must be published there.

If `auth list` is empty after they say they approved, re-run step 2. If the handshake still fails, then ask for a custom-app `shpat_` as fallback.

**Fallback `shpat_`:** only if OAuth is blocked or the user already pasted one. Use `X-Shopify-Access-Token` / `SHOPIFY_ADMIN_TOKEN`. Do not echo the full token in chat, commits, or files. Warn that it is in the thread and should be rotated if shared.

### 3. Capture the source (public)

From the source origin:

- `GET /products.json?limit=250` (paginate `page=` until empty)
- `GET /collections.json?limit=250`
- For merchandising collections: `/collections/<handle>/products.json?limit=250`
- `GET /pages/<handle>.json` for about, faq, shipping, privacy, terms, contact
- Homepage HTML: nav labels + order, announcement, footer columns, hero copy
- CSS signals: `font-family`, button radius, product-card pattern (hover image, ATC+price bar)
- `Shopify.theme` in the page source (confirms it is Shopify)

Skip source products that are not catalog: gift cards, shipping-protection, store-service SKUs.

Save JSON under `${TMPDIR:-/tmp}/<brand>-clone/` — not the skill repo.

### 4. Catalog → target

Delete demo snowboard / Hydrogen products on the target.

Import with `productSet` (`scripts/import_catalog.py` relative to `SKILL_DIR`, or equivalent). Default transport is OAuth (`shopify store execute`). Set `SHOPIFY_ADMIN_TOKEN` only for the `shpat_` fallback. Rules:

- `status: ACTIVE`
- `inventoryPolicy: CONTINUE`, `inventoryItem.tracked: false` so items are buyable
- Unique option values; default `Title` / `Default Title` if none
- Image `filename` **must keep the real extension**. Do not slice the basename — long Shopify filenames truncated at 80 chars drop `.jpg` and fail with `Provided filename extension must match original source`
- Prefix `https:` on `//cdn...` URLs
- After create, `publishablePublish` to the Online Store publication
- `productSet` with many files/variants: `synchronous: false` and poll `productOperation`

Then:

- `collectionCreate` for the merchandising set the **live nav** uses (not every internal collection)
- `collectionAddProducts` by handle map
- Publish collections
- `menuUpdate` **main-menu** to match the live header link order (usually 4–6 items, not 9+)
- `pageCreate` / `pageUpdate` for captured pages (`isPublished: true`)

### 5. Theme (rebuild, don't steal)

Duplicate or restyle **Horizon** on the target. Add custom sections; prefix with a short brand slug.

Minimum overlay:

- `sections/<slug>-header.liquid` + `header-group.json`
- `sections/<slug>-footer.liquid` + `footer-group.json`
- Homepage sections: announcement, hero, featured product grid, collections, founder/quote, values
- `sections/<slug>-product.liquid` + `templates/product.json`
- `sections/<slug>-collection.liquid` + `templates/collection.json`
- `assets/<slug>.css` + `assets/<slug>.js` linked from `layout/theme.liquid`

**Header:** copy the live top-nav labels and count. Centered wordmark. Right: shade/search/cart. Too many links collide with the logo.

**Product cards:** square media, hover second image, condensed uppercase title, black bar `Shop now` + price.

**PDP (beauty/shade products):** two columns (inline `grid-template-columns` **cannot** be overridden by a `<style>` media query — put layout in the CSS file). Shade **chips**, not a `<select>`. ATC button with price on the right. Accordions for description / how-to. Variant click must set `input[name=id]` **and** swap the main image from `variant.featured_image`.

**Hero gotchas:**

- `image_picker` values like `shopify://shop_images/file.webp` often stay blank if Shopify transcoded to `.png`
- `file_url` / `file_img_url` can render an empty `src` and Shopify drops the `<img>`
- Hardcode a same-origin Files CDN URL that `curl -I` returns 200: `https://<shop>.myshopify.com/cdn/shop/files/<file>.png?width=2400`
- Match `aspect-ratio` to the asset (a 3:1 still in a 16:9 box + white type on white crop = “hero missing”)
- Light stills need **dark type**, `object-position: right center` if the product sits on one side

Upload logos/section images with `fileCreate`. Wait until `fileStatus: READY`.

`themeFilesUpsert` then `themePublish` the theme you edited.

### 6. Checklist

Every run inventories against [references/checklist.md](references/checklist.md). Capture the source first so N/A is evidence-based, not skipped.

Work in this order: **C** catalog → **N** chrome → **H** home → **T** templates. Do not restyle the PDP until C1–C3 pass. Do not call the run done while any **required** row is FAIL.

### 7. Eval loop

Max **4** cycles. Each cycle: score → fix only FAILs → re-score in the browser. Stop when required = all PASS, or the cap is hit.

Scoreboard (print every cycle):

```
Eval <n>/4
C1 products  PASS  89/91 handles (skipped gift-card, package-protection)
N1 nav       FAIL  live Face,Eyes,Lips,Bestsellers,Shop All · target has 9 links
H1 hero      FAIL  img naturalWidth=0
T4 drawer    FAIL  ATC navigates to /cart
required FAIL: N1 H1 T4
```

One evidence line per FAIL (live vs target). No prose scoreboard.

Password gate: use the password the user gives (common `1`). Then, against the **live tab and the target tab**:

1. Home — N1, N2, N3, H1, H2, H3 (+ H4–H6 if not N/A)
2. One merchandising collection — T1, C4
3. One PDP that has variants on live — T2, T3, C2, C3
4. Add to cart from that PDP — T4 (must stay on the PDP; drawer opens with the line)

If Liquid/CSS looks stale: cache-bust `?v=` **and** re-read the theme file via Admin to confirm `themeFilesUpsert` wrote what you think.

Only patch FAIL rows from the last scoreboard. Re-eval those rows plus anything the patch could have broken (header change → recheck H1 overlap; ATC change → recheck T4).

If cycle 4 still has required FAILs, stop. Print the scoreboard and the remaining FAILs. Do not claim complete.

## Hard stops

- Do not unzip or rehost the source shop's theme assets as a theme
- Do not ask for a `shpat_` / Admin API key when `shopify store auth` can run
- Do not commit `shpat_`, `.env`, or `/tmp` dumps
- Do not request gated scopes on `shopify store auth`
- Do not claim pixel-perfect if licensed fonts / apps (reviews, quiz, Klaviyo) were not installed
