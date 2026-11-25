---
name: brand-canon-ingest
description: Consume a brand repo emitted by the brand-system-skills builder (interchange contract 0.6.0) into an Astro plus Tailwind v4 site on Cloudflare — run the brand's own gate board first, copy its pre-emitted tokens/web string projection verbatim as the Style Dictionary source, serialize its color schemes into role-level CSS override blocks (light default, never auto-switch), wire exact-file logos, currentColor icons, woff2 font faces, favicon and raster OG image, load canon.json plus both keystones for on-brand copy, and register the site in the brand's projection registry. Trigger on consume this brand repo into my site, apply my brand canon to the website, ingest the brand system, or wire the brand repo into Astro. Consumes an existing canon — to build, edit, or scope one use brand-canon-builder or brand-canon-scoper. Delegates the token pipeline to astro-css-tokens; setting up design tokens from a plain tokens.json with no brand repo is that skill, not this one.
---

# brand-canon-ingest

## Verdict

Use when a site on this stack must look, speak, and behave as a brand whose canonical source is a repo emitted by the brand-system-skills builder. The brand repo is the single source of truth; the site is a registered projection that consumes it — never a second source. This skill is the crossing discipline: what to copy verbatim, what to generate with the vendored serializer, what to load for copywriting, and what to register back. It makes no design decisions and duplicates no sister pipeline.

```
brand repo (contract 0.6.0)                        site (this stack)
  tools/run-gates.mjs ── run FIRST, must be green
  tokens/web/{base,semantic,component}.json ──copy verbatim──▶ tokens/  ▶ astro-css-tokens pipeline (SD v5)
  tokens/schemes/*.tokens.json ──vendored C-1 serializer──▶ src/styles/schemes.css (role vars + bridge)
  assets/logos · icons · fonts ──exact-file copy──▶ public/ and src/assets/
  canon/canon.json + brand-keystone.md + brand-visual-keystone.md ──load together──▶ copy and design calls
  satellites/projections.md ◀──register the site as a projection──
```

A brand without a builder-emitted repo has nothing to ingest: build the canon first (brand-canon-builder), or fall back to hand-authored tokens with astro-css-tokens alone.

## Contract pin

| What | Pin | Note |
|---|---|---|
| brand-system-skills (emitter) | plugin `0.6.0`, tool-repo commit `abcc31fe7eaceba182de767c20c6ed965430c8bb` | the contract this skill consumes by |
| Node | ≥ 22.12 | serializer + the brand repo's own tools |
| Token pipeline | delegated to `astro-css-tokens` | its pins (SD 5.5.1, tailwind 4.3.3, astro 7.2.2) apply unchanged |

Emitted brand repos carry NO version stamp — the contract is auto-enforced by the gate suite the builder copies into every repo (`tools/run-gates.mjs`). Review-gate: on a brand-system-skills release newer than 0.6.0, re-verify the four surfaces this skill consumes before ingesting a repo emitted by the newer builder — (1) `tokens/web/` string projection plus `tools/tokens-project.mjs`, (2) `tokens/schemes/*.tokens.json` shape (`scheme.<id>.color.<role>` with structured-OKLCH `$value`), (3) the resident set naming (`<brand>-keystone.md`, `<brand>-visual-keystone.md`, `satellites/asset-index.md`), (4) the `satellites/projections.md` machine row format.

## Precondition — run the brand's gates (step 0, non-negotiable)

Never consume a red or unverified board. The gates ARE the contract check — they prove the repo still honors everything this skill assumes (token drift, custody, keystone structure, asset index).

```bash
cd <brand-repo> && node tools/run-gates.mjs
```

Proceed only on a green verdict. NOT-RUN rows are honest deferrals, not failures. Any FAIL stops the ingest; fixing the brand repo is brand-canon-builder territory, not this skill's.

## Consumption recipe — in order

### 1. Gates

Run the precondition above. Record the verdict in the site's decision log.

### 2. Tokens — copy the string projection verbatim

Copy `tokens/web/{base,semantic,component}.json` from the brand repo into the site's `tokens/` directory, same filenames, byte-identical. These files are the brand's pre-emitted, SD-v5-ready string projection — every color `$value` already serialized to a plain `oklch()` string, provenance stripped, hex fallbacks dropped. Then run the astro-css-tokens pipeline unchanged, plus one registered transform for cubicBezier arrays (see `references/brand-repo-map.md`).

Never point Style Dictionary at the spine (`tokens/*.tokens.json`): its structured-OKLCH `$value` objects split into `-value`/`-unit` sub-vars. If `tokens/web/` is missing or stale, regenerate it in the BRAND repo (`node tools/tokens-project.mjs`) — never fabricate it site-side.

### 3. Schemes — generate the override layer

The schemes (dark mode, register variants) live in the spine as structured-OKLCH role sets and have no string projection — serialize them with the vendored zero-dep script into `src/styles/schemes.css`: role-level custom properties, `:root` = the default light scheme, `[data-theme="dark"]` = the dark scheme, variants as opt-in classes. Then bridge the semantic-tier vars once so Tailwind utilities become scheme-reactive. Full script, selector adapter, and bridge in `references/scheme-serializer.md`.

The default is light and the site NEVER auto-switches (canon rule G-UX-02) — the no-flash script defaults to light, not to `prefers-color-scheme`. This deliberately diverges from the astro-css-tokens reference script.

### 4. Assets — logos, icons, fonts, favicon, OG

Logos are exact-file (G-LOGO-01): copy the shipped SVG, never redraw, recolor, or distort; the `-fc` full-color variants are off-system (G-LOGO-02). Icons are single-stroke currentColor — inline them and they re-ink with the active scheme for free. Fonts: `@font-face` only for the woff2 weights the repo actually ships, family names matching the token stacks. Favicon derives from the mono isotype; the OG image must be raster (G-IMG-03). Recipes in `references/assets-fonts-og.md`.

### 5. Voice — load the resident set for all copy

Every copywriting or design-judgment task loads `canon/canon.json` plus BOTH keystones together (`<brand>-keystone.md` + `<brand>-visual-keystone.md`). Cite rules by their `G-*`/`ALGO-*` IDs; never restate them into the site repo. Discipline in `references/voice-and-copy.md`.

### 6. Data pointers — volatile values never freeze into the site

Prices, plans, coverage, contact data live in the source the brand's `satellites/data-map.md` names (a catalog JSON or a database) — the site reads them from there, never hardcodes them into components. See `references/governance-projections.md`.

### 7. Register the projection

Add the site as a row in the brand repo's `satellites/projections.md` registry. The row format is machine-checked by the brand's own gates — exact format and a worked row in `references/governance-projections.md`.

## Gotchas

- The scheme spine carries a `hex` field next to each OKLCH object — the serializer drops it. The stack's no-fallback OKLCH policy holds (see astro-css-tokens `references/color-oklch.md`).
- Scheme selector blocks tie on specificity — source order decides the cascade. Emit `:root` (light default) FIRST; a dark block emitted before `:root` silently loses. The vendored script encodes this order.
- cubicBezier tokens are DTCG arrays (`[0.22, 0.61, 0.36, 1]`); emitted raw they are invalid CSS. Register the one-transform wrap to `cubic-bezier()` — snippet in `references/brand-repo-map.md`.
- The copied token files use group-level `$type` (DTCG inheritance). That is valid and SD v5 resolves it — do not "fix" the files to per-leaf `$type`; they stay byte-identical to the brand repo.
- Motion vocabulary tokens like `press-scale 0.98`, `reveal-threshold 0.12`, or `78px/s` marquee speeds are JS vocabulary — consume them by importing the token JSON in script, not as CSS vars.
- Legacy shipped consumers may carry compat aliases (`--t1`, `--text`, raw brand-named vars). Those are sanctioned bridges for OLD consumers only — a new site uses the role names.
- `@font-face` family names must byte-match the first entry of the token font stacks, or every text node silently falls back.
- Never edit the copied tokens, the schemes output, or any canon file site-side. A needed change goes to the brand repo's root (builder discipline), passes its gates, and re-ingests.

## Boundaries — what this skill is not

- Building, extending, or fixing the canon — brand-canon-builder (brand-system-skills plugin).
- Scoping a brand in conversation — brand-canon-scoper.
- Palette, type, or identity decisions — the canon already made them; a deviation is an owner-ratified canon change, not a site-side patch.
- Visual rendering and page design — how a page looks and composes is design work governed by the canon's grammar and delivered by the stack's visual-layer skills; this skill only wires brand truth in.
- The token pipeline mechanics (SD config, `@theme` bridge, dark-mode seam plumbing) — astro-css-tokens owns them; this skill layers on top.
- Composing the full site build — stack-integration-playbook (deferred).
- Brands with no builder-emitted repo — nothing to ingest.

## Limitations

- Verified against one reference brand repo (furever-brand, contract 0.6.0, 2026-08-17); a second brand exercise is pending and may surface brand-specific role vocabularies.
- Favicon and OG are command recipes, not scripts — outputs need a visual check.
- Font licensing is owner-supplied; shipping webfonts publicly needs the owner's license confirmation, which this skill cannot verify.
- Scheme serialization covers color roles; if a future contract version adds non-color scheme categories, extend the serializer deliberately.

## References (load when relevant)

- `references/scheme-serializer.md` — the vendored C-1 serializer script, selector adapter, semantic bridge, light-default no-flash script, verification
- `references/brand-repo-map.md` — anatomy of a contract-0.6.0 brand repo, what to copy vs generate vs load vs never touch, cubicBezier transform, JS-vocabulary import
- `references/assets-fonts-og.md` — logo and icon rules, `@font-face` recipe, favicon derivation, raster OG recipe
- `references/voice-and-copy.md` — resident-set loading discipline, truth-gating, citing rules by ID
- `references/governance-projections.md` — projection registration row, data pointers, update protocol and re-ingest cadence
