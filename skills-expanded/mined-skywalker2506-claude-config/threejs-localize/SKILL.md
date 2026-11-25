---
name: threejs-localize
description: Extract, refactor, and translate hardcoded UI/game text in Three.js, WebGL, Electron, Vite, React Three Fiber, and browser game projects. Use when Codex is asked to add localization/i18n, move strings into JSON locale files, scan hardcoded text, create language packs, translate Steam-supported languages, add language selector flags/icons, choose default machine locale, or validate locale key coverage for Three.js projects.
---

# Three.js Localize

## Goal

Make a Three.js project localization-ready without heavy rewrites. Prefer JSON locale catalogs and a small translation helper unless the project already uses an i18n library. Extract the source/default language first, then generate target locale files and translation batches from that catalog. Keep outputs compatible with `$threejs-steam-shipper` when that companion skill is also being used, but do not require it.

## Default Strategy

Use existing conventions first. If the project already has `i18next`, `react-i18next`, `vue-i18n`, `svelte-i18n`, FormatJS, or custom locale files, extend that system. For plain Three.js, vanilla JS, or small Vite games, create a minimal `src/i18n/` module with flat JSON catalogs and a `t(key, vars)` helper.

Do not blindly replace every string literal. Only extract player-facing text: menus, HUD labels, prompts, errors, tutorials, settings, accessibility labels, achievement names/descriptions, store-facing text in app data, and dialogue. Leave technical strings alone: imports, URLs, selectors, asset paths, shader code, storage keys, event names, enum values, analytics IDs, CSS class names, filenames, and protocol constants.

This skill must work standalone. If no Steam packaging skill or Steam staging folder exists, stop after locale extraction, runtime integration, translation, asset setup, build, and UI QA. When used with `$threejs-steam-shipper`, run localization before the final production web build and before `buildable/steam-electron/scripts/copy-web.mjs`. Runtime locale files under `src/i18n` should be bundled by the app build; flag assets under `public/localization/flags` should be copied by Vite/static build into `dist/localization/flags` and then into `buildable/steam-electron/web/localization/flags`.

## Workflow

1. **Scan first.** Run:

   ```bash
   node <skill>/scripts/extract-hardcoded-text.mjs <target-project>
   ```

   Read `<target-project>/buildable/localization/i18n-candidates.md` and `.json`. Use the report as a review surface, not as automatic truth.

2. **Choose integration.**
   - Existing i18n library: add keys to its locale files and patch code using its API.
   - React Three Fiber: prefer `react-i18next` if already installed; otherwise a tiny context/provider is enough for small games.
   - Plain Three.js/Vite: run the scaffold script and use `t()`.
   - Electron/Steam: persist selected language in app/user settings and default from saved setting, Steam language if integrated, then `navigator.languages`/machine locale.

3. **Scaffold when needed.** For plain projects:

   ```bash
   node <skill>/scripts/scaffold-i18n-runtime.mjs <target-project> --source en
   ```

   This creates `src/i18n/` only if missing. Preserve existing files.

4. **Extract and patch carefully.**
   - Create stable semantic keys, not English-as-key, for text likely to change.
   - Group by feature: `menu.start`, `settings.audio.master`, `hud.score`, `tutorial.move`.
   - Keep interpolation placeholders explicit: `{count}`, `{playerName}`, `{key}`.
   - For text rendered to canvas or Three.js text geometry, route the source text through `t()` before creating/updating the texture or geometry.
   - Rebuild text geometry/canvas textures when locale changes.

5. **Prepare target languages.** For selected languages, run:

   ```bash
   node <skill>/scripts/sync-locale-keys.mjs <target-project> --locales tr,es,fr,de,ja,ko,zh-CN
   ```

   This copies missing keys from the source catalog with `TODO:` prefixes and writes a missing-key report.

   For Steam full platform/API languages, verify the current list from Steamworks docs if internet is available, then run:

   ```bash
   node <skill>/scripts/sync-locale-keys.mjs <target-project> --steam-full
   ```

   Steam does not require every language; full platform languages are the practical default when the user asks for "all Steam languages".

6. **Translate.** Load `references/translation-workflow.md` when translating or preparing vendor/LLM batches. Translate JSON values only, preserve keys, placeholders, markup tokens, button glyphs, and line-break intent. For many Steam languages, translate one locale file at a time and write valid JSON back to `src/i18n/locales/<locale>.json`.

7. **Add language selector assets when requested.** Load `references/language-selector-assets.md`. Use flags only as small language-choice icons, not as a claim that a language belongs to one country. Prefer open-license SVG packs such as `flag-icons` or `circle-flags`, copy assets into the project, record attribution, and style them to fit the existing UI without breaking layout.

   ```bash
   node <skill>/scripts/prepare-language-flags.mjs <target-project>
   ```

8. **Optionally verify Steam shipper compatibility.** If the project will be packaged with `$threejs-steam-shipper` or already has `buildable/steam-electron/`, run this after the production web build and after the shipper's `copy:web` step:

   ```bash
   node <skill>/scripts/verify-steam-shipper-localization.mjs <target-project> --strict-steam
   ```

   Fix missing translations, leaked build-only files, missing flag assets, or missing `buildable/steam-electron/web/index.html` before creating the Steam depot. If `$threejs-steam-shipper` is unavailable or not relevant, either skip this step or run the same script without `--strict-steam` for standalone localization validation.

9. **Validate.**
   - Run `sync-locale-keys.mjs` again to catch missing/extra keys.
   - Build the project.
   - If packaging for Steam, run packaging only after locale JSON parses cleanly and no `TODO:` translations remain in shipping locales.
   - Inspect the UI in the longest-language locale and a CJK locale.
   - Check that text does not overflow HUD panels, buttons, modals, canvas textures, or text geometry.

## Output Shape

Default generated files:

```text
target-project/
  buildable/
    localization/
      i18n-candidates.json
      i18n-candidates.md
      locale-key-report.md
      steam-shipper-localization-report.md
      translation-batch.<locale>.json
      THIRD_PARTY_NOTICES.localization.md
  src/
    i18n/
      index.js
      locale-meta.json
      locales/
        en.json
  public/
    localization/
      flags/
        <country>.svg
```

Use `public/locales/` instead of `src/i18n/locales/` only when the app already loads runtime JSON over HTTP or the catalogs are large enough to lazy-load.

Do not put `translation-batch.*.json`, candidate reports, missing-key reports, raw glossaries, or build-only QA files under `public/`; Steam packagers usually copy the production web output into the final package.

## References

- Read `references/implementation-patterns.md` before patching React, Vite, vanilla Three.js, canvas text, or text geometry.
- Read `references/translation-workflow.md` before translating many locales or preparing files for translation review.
- Read `references/language-selector-assets.md` before downloading or adding language flags/icons.
