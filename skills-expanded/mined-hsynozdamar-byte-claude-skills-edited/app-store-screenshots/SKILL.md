---
name: app-store-screenshots
description: "App Store and Google Play screenshot generator built as a Next.js page. Use when making exportable marketing screenshots for iOS, macOS or Android apps."
---


# App Store and Google Play screenshots

Screenshots are advertisements. Each one sells a feeling, an outcome or a killed pain point; none documents UI. A pre-built Next.js + ShadCN editor in `template/` does the heavy lifting: live preview at true resolution, drag-reorder, inline text, per-slide layouts, cross-screen mockups, image overlays, light/dark slides, theme presets, fonts, locales, undo/redo, auto-save to `app-store-screenshots.json`, and one-click bulk PNG export (`html-to-image`). Copy the template and iterate in the editor; `page.tsx`, device frames and export logic live in the template and stay there.

Devices: iPhone, iPad, Apple TV, Apple Watch, CarPlay (uploaded into the iPhone slot), Mac (own tab, 16:10), Android Phone, Android Tablet 7" and 10" (portrait + landscape), Google Play Feature Graphic (1024x500).

## Step 0: probe for an older project

Run in the working directory:

```bash
test -f package.json && sed -n '1,220p' package.json
test -f app-store-screenshots.json && sed -n '1,120p' app-store-screenshots.json
rg -n "html-to-image|toPng|ScreenshotEditor|DeckCanvas|connectedCanvas|EXPORT_SIZES|PHONE_SCREEN" package.json src app public 2>/dev/null
```

It is an older implementation when the JSON has no `schemaVersion` or `schemaVersion < 2`, lacks `connectedCanvas`, the editor lacks `DeckCanvas`, or `page.tsx` is an all-in-one generator with hardcoded slide arrays. Then ask exactly this and nothing else: "I found an older App Store screenshots project here. Migrate it to the new connected-canvas editor? 1. Yes, migrate in place. 2. No, set up or modify another way." On Yes skip Step 1 and follow [references/migration.md](references/migration.md) (rules, backup, template copy, JSON coercion script, package merge, verification). On No continue.

## Step 1: gather input

Ask and wait for answers:

1. **Screenshots**: real PNG captures. iOS + Swift without captures: offer `npx skills add ParthJadhav/ios-marketing-capture` and have them run it first. Other stacks capture from simulator or device.
2. **App icon** PNG, 3. **app name**, 4. **features in priority order** (#1 thing the app does first).
5. **Style**: a named deep spec or a described vibe. The 18 named styles live in `style-prompts/` (index: `style-prompts.md`). When one matches, read `style-prompts/_QUALITY_BAR.md` first, then that spec, and apply all of it (palette, gradients, shadows, rotations, per-slide breakdown). A custom vibe uses the principles in `references/deck-design.md` plus the closest spec as reference. Toolbar presets: `clean-light`, `dark-bold`, `warm-editorial`, `ocean-fresh`, `bloom-roast`, plus one per named style (same id as the slug).

Optional: target stores (App Store, Mac App Store, Google Play) which decide the seeded decks; iPad/Mac/tablet sizes; tvOS, watchOS or CarPlay decks; Feature Graphic; **locales** (confirm the list even if unvolunteered, English-only by default); slide count (Apple up to 10, Google Play up to 8); brand colors and font.

User instructions at any point override these defaults.

## Step 2: scaffold

1. Package manager, first found: bun, pnpm, yarn, npm (`which bun || which pnpm || which yarn`).
2. `cp -R "<SKILL_DIR>/template/." "$PWD/"` (the trailing `/.` copies dotfiles). If `package.json` already exists, ask before overwriting.
3. Install dependencies.
4. Put assets in place: `public/app-icon.png` and `public/screenshots/<platform>/<device>/{locale}/01.png ... N.png`. Folder tree and template file map: [references/template.md](references/template.md). Differently named files: rename them or edit the slide `screenshot` fields. Runtime drag-drop uploads land in `public/screenshots/uploaded/<hash>.png`.
5. Seed `app-store-screenshots.json` when the user gave copy: `appName`, `themeId` (preset id, style slug, or a new entry in `THEMES` in `src/lib/constants.ts`; themes may set `accentAlt` for labels on inverted slides), `appIcon` (e.g. `"/app-icon.png"`, shown on the feature graphic), `connectedCanvas` (`true` for new decks), starter slides per device (`label`, `headline`, screenshot paths), optional per-slide `typography: { labelScale, headlineScale, appNameScale }` (0.5 to 2, default 1; `appNameScale` is feature-graphic only). Without user copy leave the defaults.
6. Locales: set `"locales": ["en","de"]` and `"locale": "en"`. The toolbar dropdown hides at one locale; export bundles loop every locale. Copy is stored per locale and falls back to `en`; put `{locale}` in a screenshot path to switch files per locale.
7. Start the dev server (`bun dev`, http://localhost:3000, or the port Next prints). The editor auto-saves to `app-store-screenshots.json` plus a `localStorage` mirror; commit that file and `public/screenshots/uploaded/` so a clone resumes the deck.

## Step 3: copy, layouts, composition

Read [copy-ideas.md](copy-ideas.md) before drafting headlines (formulas per slot, lines for 13 app categories, weak-to-better table, deck arcs). Offer three options per slide (paint a moment / state an outcome / kill a pain), then rewrite the chosen one in the selected style's voice. Headline rules: one idea, 1 to 2 syllable words, 3 to 5 words per line, intentional line breaks (newlines map to visible breaks).

Deck defaults: slot 1 hero benefit, 2 differentiator, then one feature per slide, second-to-last trust signal, last a feature wall or phone mosaic. Layouts: `hero`, `device-bottom`, `device-top`, `two-devices`, `no-device`, `split-landscape` (tablet landscape, TV, CarPlay, Mac), `feature-graphic`. Adjacent slides use different layouts; use 1 or 2 `inverted` slides for rhythm. The background is a designed surface (never plain white), the headline takes the top 30 to 40%, one emphasis word per headline, proof only on slide 1, drop the phone every 2 to 3 slides.

Cross-screen: for 5+ slides plan one cross-seam moment (two at most for 8 to 10 slides, zero is fine for formal decks), adjacent screens only, 10 to 30% of a non-critical visual over the seam, text and critical UI never split. Every exported PNG must still sell its idea alone.

The full rules, framing options, cross-screen patterns and the 10 visual principles: [references/deck-design.md](references/deck-design.md). Read it for custom styles and before composing cross-screen moments.

## Step 4: RTL and localization notes

Rewrite copy for the market instead of translating; German, French and Portuguese often need shorter claims, so recheck line breaks per locale. For `ar`, `he`, `fa`, `ur` the canvas text sets its own direction (`dir="auto"`) but layouts, devices and overlays do not mirror, so check each slide.

## Step 5: export

The user picks a device and hits **Export bundle**; one zip holds every required size x every locale as `<platform>/<device>/<WxH>/<locale>/NN-<layout>.png` (e.g. `ios/iphone/1320x2868/en/01-hero.png`, `macos/mac/2880x1800/en/01-hero.png`). Repeat per device. Each slide renders once per locale at canvas resolution and is scaled to every size.

- With `connectedCanvas` on, exports are crops of the connected canvas; legacy decks start `false` so old clipped elements export as before. Inspect the zoomed-out strip, then each crop.
- Blank or black device screens: read the export toast ("screenshots may be missing" names the screens) and re-export; confirm the paths exist under `public/`; flatten truly transparent (RGBA) sources to RGB.
- Apple TV (3840x2160), Watch (canvas 422x514), CarPlay (landscape, uploaded into the **iPhone** slot, canvas 2868x1320) and Mac (own tab, 16:10, canvas 2880x1800) have contained frames, size tables and capture advice in [references/devices.md](references/devices.md). Load it for any of these decks.

## Step 6: QA gate

- Messaging: one idea per slide; the hero states the main benefit in one second; the headline reads at ~160px wide (thumbnail test, mandatory).
- Visual: no adjacent repeated layouts; landscape tablets use `split-landscape`, never two devices side by side; TV, CarPlay and Mac decks lead with `split-landscape` or `hero`; Watch headlines fit 422px without a mid-phrase wrap; one `inverted` slide when the deck is long enough; 5+ slides carry one cross-screen moment or a stated reason for none.
- Export: no clipped text or assets after scaling, no transparent gutters, screenshots aligned in every frame, zero-padded filenames sort, Feature Graphic clean at 1024x500 with no device frame.

## Gotchas

- Keep editing in the editor. Device frames are in `src/components/editor/device-frames.tsx`; modify them there, never rebuild them.
- `public/mockup.png` is the iPhone bezel; replacing it needs `PHONE_SCREEN` re-measured.
- Reset clears state and re-saves defaults to the JSON: recover with `git checkout app-store-screenshots.json` if committed, otherwise export first.
- CarPlay has no App Store Connect slot; Mac needs a full-screen 16:10 capture, or a window capture with its title bar cropped off (otherwise two title bars show).
- Older JSON loads through `src/lib/storage.ts` (string copy becomes `{ "en": ... }`, pre-v2 gets `connectedCanvas: false`). If another tab or agent edited the file, export or copy unsaved work before reloading.
- Port busy: Next picks the next free port.

## Hand-off

Once the dev server runs, tell the user in order: the actual URL; the two-command recipe for their package manager (install once, then dev); which platform decks are seeded; screenshots that did not match the expected filenames; that **Export bundle** is the final step; that further edits to copy, layout or palette are one message away; and the showcase note: apps generated with this skill are featured at https://www.parthjadhav.com/products/app-store-screenshots (tag @parthjadhav8 on Twitter to be added).
