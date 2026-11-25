---
name: streamdeck-publishing
description: 'Packaging and shipping a Stream Deck plugin to the Elgato Marketplace: streamdeck pack to produce .streamDeckPlugin, .sdignore exclusions, DRM (SDKVersion 3 + Software 6.9+: file encryption + integrity), Maker Console submission (https://maker.elgato.com), Maker Agreement, review process, supported product types, country/Stripe limitations, 70/30 payout split, IP ownership, multi-listing, marketplace UX guidelines for icons, side-loading via .streamDeckPlugin double-click, version bumps. USE FOR: publishing a Stream Deck plugin, enabling DRM, packaging a plugin, submitting to Maker Console, becoming a maker, marketplace review, plugin updates / version bumps, icon UX guidelines, distributing outside the marketplace.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "marketplace", "packaging", "drm", "publishing"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck Plugin — Packaging & Marketplace Publishing

> **Prerequisite:** `streamdeck-general` (project layout),
> `streamdeck-cli` (the `pack` / `validate` commands),
> `streamdeck-manifest` (`SDKVersion`, `Version`, `Software.MinimumVersion`).

## Purpose

You've built a plugin and want to ship it. This skill covers the entire
path from `.sdPlugin/` source folder to a published Marketplace listing
that updates automatically on users' machines:

1. Pre-flight checklist
2. Choosing `SDKVersion: 2` vs `3` (DRM)
3. `.sdignore` — what to strip
4. Building the `.streamDeckPlugin` installer
5. Side-loading vs. Marketplace distribution
6. Maker Console: account, agreement, submission, review
7. Marketplace UX guidelines (icons, listing copy)
8. Version bumps / updates
9. Payouts and IP

---

## 1. Pre-flight checklist

Before you even run `pack`, verify:

| ✔ | Item |
|---|---|
| `manifest.UUID` is reverse-DNS and **permanent**. Once published, it can't change. |
| `manifest.Version` is the four-component `MAJOR.MINOR.PATCH.BUILD` (e.g. `1.0.0.0`). |
| `manifest.Author`, `Description`, `Icon`, `Category`, `CategoryIcon` are set. |
| `manifest.OS` lists every platform you've actually tested on. |
| `manifest.Software.MinimumVersion` is the lowest Stream Deck app you tested with. |
| Every action's `UUID`, `Name`, `Tooltip`, `Icon`, `States[].Image` is set. |
| Every PI page renders cleanly in the Stream Deck app on both light and dark mode. |
| No `console.log` of secrets; logger level is `INFO` or `WARN` in production. |
| No hard-coded API keys / OAuth client secrets in the source. (PKCE — see `streamdeck-oauth`.) |
| All icons use one of: SVG, PNG, JPG, WEBP. **No GIF, no APNG.** |
| `streamdeck validate` exits clean. |
| Plugin works on a freshly-installed Stream Deck app (no leftover state). |

---

## 2. `SDKVersion`: 2 vs. 3 (DRM)

| | `SDKVersion: 2` | `SDKVersion: 3` |
|---|---|---|
| Minimum Stream Deck | `"6.4"` (per `Software.MinimumVersion`) | **`"6.9"`** required |
| Minimum `@elgato/streamdeck` | v1 | **v2+** |
| File encryption | none | yes (applied at Maker Console upload) |
| Integrity checking | none | yes |
| Side-loadable for users? | yes | yes, but uploaded `.streamDeckPlugin` from Maker Console is the encrypted version |
| Side-loadable for **you** during dev? | yes | yes — DRM is applied only on Maker upload, not by `streamdeck pack` locally |
| Eligible for Marketplace? | yes | yes |

> Use `SDKVersion: 3` if your plugin contains anything you want to make
> hard to copy (custom artwork, novel logic, paid features). It costs
> you nothing in dev experience.
>
> Use `SDKVersion: 2` if you're side-loading only (e.g. internal tools)
> or want to keep the option open to support older Stream Deck app
> installs.

Changing later is fine — just bump `Version` and the user upgrade flow
takes care of it.

---

## 3. `.sdignore` — strip dev-only files

Same syntax as `.gitignore`. Lives in the **project root** (not inside
`*.sdPlugin/`). Default exclusions: `.git/`, `/.env*`, `*.log`,
`*.js.map`.

Recommended additions:

```gitignore
# Source — only ship compiled bin/
src/
tsconfig.json
rollup.config.mjs
*.test.*
__tests__/

# Dev-only docs / configs
README.md
CONTRIBUTING.md
.editorconfig
.eslintrc*
eslint.config.*
prettier.config.*
.vscode/
.github/
node_modules/

# OS junk
.DS_Store
Thumbs.db
```

> Do NOT exclude `bin/`, `imgs/`, `ui/`, `manifest.json`, `layouts/`,
> `profiles/`, language files (`*.json` at the root of `*.sdPlugin/`).

Verify your `.sdignore` is doing the right thing:

```pwsh
streamdeck pack <UUID>.sdPlugin/ --dry-run
```

The dry-run prints the file list that would go into the
`.streamDeckPlugin`.

---

## 4. Building the installer

```pwsh
# Clean build + validate + pack
npm run build
streamdeck validate <UUID>.sdPlugin/
streamdeck pack    <UUID>.sdPlugin/ --output dist/ --force
```

The result is `dist/<plugin-name>.streamDeckPlugin` — a ZIP archive in
disguise. Double-click installs it for the local user.

Useful flags:

| Flag | When to use |
|---|---|
| `--dry-run` | Inspect the file list without writing. |
| `-f`, `--force` | Overwrite an existing `.streamDeckPlugin`. |
| `-o`, `--output <dir>` | Where to write the file. |
| `--version 0.2.0.0` | Override `manifest.Version` for this build. Handy for CI release tags. |
| `--no-update-check` | Skip schema-update HTTP call. **Always set in CI.** |

A reproducible release script:

```json
{
  "scripts": {
    "release": "npm run lint && npm run build && streamdeck validate <UUID>.sdPlugin/ --no-update-check && streamdeck pack <UUID>.sdPlugin/ --output dist --force --no-update-check"
  }
}
```

---

## 5. Distribution paths

### 5a. Side-loading (no Marketplace)

Hand someone the `.streamDeckPlugin` file (email, GitHub release page,
intranet share). They double-click — Stream Deck prompts to install.

Pros: no review, no fees, instant publish.
Cons: no auto-update; user gets a "this plugin isn't from Marketplace"
warning the first time; not searchable.

Good fit for: internal company plugins, beta-tester builds, niche tools.

### 5b. Elgato Marketplace

Goes through review; benefits from auto-update, discoverability,
optional paid distribution.

Pros: auto-update on every install; appears in the in-app store;
optional paid tier (70/30 split).
Cons: review wait (days to a couple of weeks); must follow UX
guidelines; payouts require Stripe Connect (country-limited).

---

## 6. Marketplace submission flow

### 6.1 Create a Maker account

1. Sign in at <https://maker.elgato.com> with your Elgato account
   (or create one).
2. Set up your **organization** (display name, contact email, optional
   logo). This is who Marketplace shows as the publisher.
3. Sign the **Maker Agreement**. One-time.

### 6.2 Submit the plugin

For each plugin:

1. **New Submission → Plugin**.
2. Upload your `<plugin>.streamDeckPlugin` from `dist/`.
3. Fill in the listing:
   - Display name (matches `manifest.Name`).
   - Short description (matches `manifest.Description` — fine to expand).
   - Long description (Markdown).
   - Category.
   - Marketplace tile icon (high-res; see UX guidelines).
   - Screenshots (PNG, recommended 1920×1080).
   - Pricing (Free / Paid). Paid requires Stripe Connect.
   - Supported devices / OS.
4. Submit for review.

### 6.3 Review

Elgato reviews:

| What | Common rejections |
|---|---|
| Plugin runs cleanly on macOS and Windows | Crashes on launch, native module incompatible |
| Manifest is valid + schema-correct | Missing `Icon`, wrong file paths |
| Icons follow UX guidelines | Off-grid, low-contrast, photo-realistic |
| No misleading branding | Using an Elgato logo, impersonating another vendor |
| No malicious / harmful content | Crypto miners, surveillance tools |
| Reasonable resource use | Tight polling loops, runaway memory |

Turnaround: typically a few business days. You can iterate — fix,
re-pack, re-upload. The UUID stays the same; bump `Version`.

### 6.4 Updates

To ship a new version:

1. Bump `manifest.Version` (`1.0.0.0` → `1.0.0.1`, `1.1.0.0`, etc.). Use
   the four-component format always.
2. Repackage: `streamdeck pack ... --version 1.0.0.1`.
3. Upload the new `.streamDeckPlugin` to the existing Marketplace
   listing.
4. Submit for review. Users get the update silently the next time their
   Stream Deck app checks in.

> **The UUID must NOT change between versions.** If you change it, it's
> a brand-new plugin from the user's POV — existing buttons break.

---

## 7. UX guidelines — icons that pass review

Elgato has a fairly opinionated icon style. Plugins that violate it
generally get rejected for the listing tile.

| Rule | Why |
|---|---|
| Use the official Elgato icon grid (download from <https://docs.elgato.com/resources/icons>) | Consistent visual weight across the Marketplace |
| Solid, flat, monochrome glyph on a colored circular background | Stream Deck's house style |
| Glyph must be legible at 72×72 (the actual key size) | Anything tiny disappears |
| Background color: one solid color OR a subtle gradient | No photos, no busy patterns |
| No text in the **listing tile** icon (action key icons can include short text) | Tiles are small in the store |

Generate icons in multiple resolutions:

```
imgs/plugin/marketplace.png    # 72×72 — used in actions list
imgs/plugin/marketplace@2x.png # 144×144 — hi-DPI displays
imgs/plugin/category.png       # 72×72 — category header
imgs/plugin/category@2x.png    # 144×144
```

For action icons:

```
imgs/actions/<slug>/icon.png       # actions list
imgs/actions/<slug>/icon@2x.png
imgs/actions/<slug>/key.png        # rendered on the Stream Deck key (state)
imgs/actions/<slug>/key@2x.png
```

The manifest references all of these **without extensions** — the SDK
picks `@2x` automatically on hi-DPI displays.

---

## 8. Payouts and country limitations

| | Free plugin | Paid plugin |
|---|---|---|
| Available worldwide | ✓ | only countries supported by Stripe Connect |
| Stripe Connect required | ✗ | ✓ |
| Revenue split | n/a | 70% Maker / 30% Elgato |
| Payouts | n/a | via Stripe Connect monthly |

> If Stripe Connect doesn't support your country, you can still publish
> free plugins; paid is gated by Stripe support.

---

## 9. IP and multi-listing

- You retain **all intellectual property** in your plugin. Elgato gets a
  license to distribute via Marketplace.
- You can also list the same plugin elsewhere (Etsy, your own site,
  GitHub releases) — multi-listing is allowed.
- You're responsible for any third-party IP (icons, libraries, API
  clients). Don't ship art you don't have rights to.

---

## 10. Practical checklist — going from "works locally" to "live"

```
[ ] manifest UUID locked in (forever)
[ ] manifest Version bumped to 1.0.0.0
[ ] manifest Author, Description, Icon, Category set
[ ] manifest Software.MinimumVersion matches your testing
[ ] manifest OS array lists tested platforms
[ ] SDKVersion 2 or 3 chosen (3 if you want DRM)
[ ] .sdignore strips src/, configs, README, .vscode
[ ] @2x.png variants present alongside .png
[ ] No hard-coded secrets in source or PI
[ ] OAuth (if any) uses PKCE + proxy URL (see streamdeck-oauth)
[ ] streamdeck validate exits clean
[ ] Plugin loads on a fresh Stream Deck install (no leftover settings)
[ ] streamdeck pack ... --no-update-check produces .streamDeckPlugin
[ ] Double-click install on macOS works
[ ] Double-click install on Windows works
[ ] Maker Console listing copy + screenshots prepared
[ ] Submitted for review
[ ] (After approval) Test the Marketplace install flow as a user
```

---

## See Also

- Distribution guide: <https://docs.elgato.com/streamdeck/sdk/introduction/distribution>
- Become a Maker: <https://docs.elgato.com/marketplace/become-a-maker>
- Plugin UX guidelines (icons): <https://docs.elgato.com/guidelines/stream-deck/plugins>
- Elgato icons download: <https://docs.elgato.com/resources/icons>
- Maker Console: <https://maker.elgato.com>
- Marketplace Makers Discord: <https://discord.gg/GehBUcu627>
- Sibling skills: `streamdeck-general`, `streamdeck-cli`,
  `streamdeck-manifest`, `streamdeck-oauth`
