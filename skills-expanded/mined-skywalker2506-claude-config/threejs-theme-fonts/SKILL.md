---
name: threejs-theme-fonts
description: Analyze a Three.js game's visual theme/style, optionally use Playwright screenshots, research current free/open-source theme-appropriate fonts, select multilingual fonts before falling back to Noto, scaffold HUD typography that supports all threejs-localize Steam languages, and QA translated text overflow/clipping from real screens. Use when Codex is asked to improve game fonts, match typography to game theme, choose open-source fonts, make centered HUD popup/toast text, verify multilingual font coverage, catch localized UI text growth, or prepare typography that remains compatible with localization and Steam shipping.
---

# Three.js Theme Fonts

## Goal

Make typography fit the game's theme while staying safe for localization and real layouts. Research current free/open-source fonts for the actual game style before choosing. Use Noto as the final fallback safety net, not the default first choice, unless no better theme-appropriate multilingual option is available.

## Default Strategy

Prefer a theme-appropriate free font that covers the required locale/script buckets. Research current sources such as Google Fonts metadata, Fontsource, foundry/GitHub repositories, and license files before selecting the UI font. Score candidates by:

- theme fit for the game's actual screenshots/HUD,
- license clarity for bundling in a game,
- coverage for `$threejs-localize` locale/script buckets,
- readability at HUD/menu sizes,
- availability as self-hosted files or Fontsource packages.

Use Noto only as fallback coverage:

- fallback/default: `Noto Sans`
- Arabic fallback: `Noto Sans Arabic`
- Simplified Chinese fallback: `Noto Sans SC`
- Traditional Chinese fallback: `Noto Sans TC`
- Japanese fallback: `Noto Sans JP`
- Korean fallback: `Noto Sans KR`
- Thai fallback: `Noto Sans Thai`

Use theme/display fonts only for short, non-critical titles if their glyph coverage is limited. Never apply a narrow Latin-only display font to translated body text, buttons, dialogue, achievements, or center-screen HUD alerts.

This skill works standalone. If `$threejs-localize` is used, align locale/script buckets with its locale files. If `$threejs-steam-shipper` is used, self-host fonts under `public/fonts/` so the packaged build works offline.

Do not scaffold final font choices before the research gate unless the user explicitly asks for offline/no-internet work. In offline mode, generate only a provisional theme-candidate stack and mark Noto as fallback in `font-plan.json`.

## Workflow

1. **Analyze theme and current fonts.**

   ```bash
   node <skill>/scripts/analyze-theme-fonts.mjs <target-project>
   ```

   Read `buildable/typography/theme-font-analysis.md`. If the visual style is unclear, use Playwright or browser screenshots and infer the theme from actual HUD/gameplay, not only filenames.

2. **Research and choose font roles.** Load `references/font-selection-theory.md` and `references/font-sources-and-coverage.md`.
   - Search current free/open-source font sources for the detected theme and required scripts before accepting defaults. Use current internet sources when network is available.
   - Check Google Fonts API/metadata for subsets/scripts and variants, Fontsource for self-hostable packages, and upstream repository/license files for game bundling.
   - Pick one theme-appropriate multilingual UI stack when possible, with Noto only as fallback.
   - Pick at most one optional display/accent font.
   - Define HUD popup style separately: strong, readable, centered, short-lived, and not layout-breaking.
   - Record at least 3 candidates when available, including rejected candidates and why, in `buildable/typography/theme-font-analysis.md` or `font-plan.json`.

3. **Scaffold typography tokens and HUD classes.**

   ```bash
   node <skill>/scripts/scaffold-typography-system.mjs <target-project> --theme sci-fi
   ```

   This creates `src/theme/typography.css`, `src/theme/font-plan.json`, and `buildable/typography/FONT_NOTICES.md` without overwriting existing files. Pass `--ui-font` and `--display-font` when research finds better current fonts; otherwise the scaffold writes provisional theme candidates with Noto fallback and marks research as still required.

4. **Preview multilingual samples and stress text.**

   ```bash
   node <skill>/scripts/create-font-preview.mjs <target-project>
   ```

   Open `buildable/typography/font-preview.html` and inspect Latin, Cyrillic, Greek, Arabic, Thai, CJK, Korean, Turkish, and Vietnamese samples. Check the constrained button, dialogue, and HUD popup stress samples for wrapping, clipping, text growth, and awkward line breaks. Use this preview before shipping or after changing fonts.

5. **Integrate lightly.**
   - Import `src/theme/typography.css` from the app's main CSS/JS entry.
   - Apply `.hud-popup` to center-screen "level up", "wave clear", damage, reward, or tutorial burst text.
   - Use `data-locale="<locale>"` on the app root when available so CSS can switch script-specific font stacks.
   - Keep text containers constrained and responsive.

6. **Run visual overflow QA on actual screens.**
   - Use Playwright/browser screenshots when the project can run locally. Capture representative states: main menu, settings/options, pause, gameplay HUD, dialogue/tutorial, inventory/shop if present, and the centered HUD popup.
   - Test the default locale plus long or script-sensitive locales from the project's JSON catalogs when available. Include German or Turkish for expansion, Arabic for RTL, Thai/Vietnamese for marks, and CJK/Korean for dense glyph metrics.
   - Look for text leaving containers, buttons growing unexpectedly, clipped diacritics, overlapping HUD, popup text escaping the viewport, scrollbars appearing in fixed panels, or layout shifts between locales.
   - Save notes in `buildable/typography/visual-overflow-qa.md` and keep any screenshots under `buildable/typography/screenshots/`, not under `public/`.
   - Fix issues in this order: shorten or rephrase the translation/key copy first; then allow wrap/flex/min-width changes; then adjust line-height, padding, or font weight; then reduce font size with bounded `clamp()` or container-specific CSS; finally add locale-specific overrides only when the script truly needs it.
   - Coordinate with `$threejs-localize` when present so shortened translations stay in locale JSON instead of becoming hardcoded UI patches.

7. **Validate with localization.**
   - If `$threejs-localize` exists, use its locale files and long-language QA.
   - Test the centered popup with long German/Turkish text, Arabic, Thai, Japanese, Korean, Simplified Chinese, and Vietnamese.
   - Check that font files are in `public/fonts/` or a reliable local path before Steam packaging.

## Output Shape

```text
target-project/
  buildable/
    typography/
      theme-font-analysis.md
      theme-font-analysis.json
      font-preview.html
      FONT_NOTICES.md
  src/
    theme/
      typography.css
      font-plan.json
  public/
    fonts/
```

Do not put analysis reports or raw screenshots under `public/`.

## References

- Read `references/font-selection-theory.md` before choosing or changing fonts.
- Read `references/font-sources-and-coverage.md` before downloading, self-hosting, or licensing fonts.
