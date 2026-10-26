---
name: lime-design
description: Use this skill to generate well-branded interfaces and assets for LIME 萊姆輸入法 (LimeIME) — a free, open-source Traditional-Chinese input method / soft keyboard for Android & iOS — either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and the iOS Settings UI kit components for prototyping.
user-invocable: true
---

Read the `VISUAL_DESIGN.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Where things are
- `VISUAL_DESIGN.md` — the full design guide: Content Fundamentals, Visual Foundations, Iconography, and a file index. **Read this first.**
- `styles.css` — link this one file to inherit every token (colors, type, spacing). It `@import`s `tokens/*.css`.
- `components/` — React UI primitives (Button, Switch, SegmentedControl, Stepper, ListGroup, ListRow, StatusBanner, TabBar). Each has a `.d.ts` contract and `.prompt.md` usage note.
- `foundations/*.card.html` — visual specimens of color, type, spacing, brand.
- `ui_kits/lime-settings/` — the interactive 4-tab iOS Settings app recreation (設定 / 輸入法 / 喜好設定 / 資料庫). Start here to see the components composed into real screens.
- `assets/` — the lime logo / app icon (PNG).

## Brand in one breath
Lime-fruit wordmark on a diagonal green gradient (`#B2D234`→`#00833E`). Product chrome is clean iOS-HIG light: white pages, `#F2F2F7` grouped cards, 34px bold left-aligned titles, brand green `#009444` for actions, lime green `#4CAF50` for toggles. Copy is plain instructional Traditional Chinese (Taiwan), privacy-forward, no emoji in chrome, no hype.

## Caveats
- Fonts (SF Pro / PingFang TC) are system-only — not bundled; Noto Sans TC is the web fallback.
- Icons substitute SF Symbols with Lucide-style SVGs — swap back if you have the licensed sets.
