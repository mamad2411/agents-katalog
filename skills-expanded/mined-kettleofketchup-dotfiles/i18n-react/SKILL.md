---
name: i18n-react
description: react-i18next + remix-i18next for SSR React (React Router 7 / Remix). Use for SSR locale detection (cookie/?lang/Accept-Language), i18next-parser extraction, eslint-plugin-i18next enforcement, and typed t() module augmentation.
---

# i18n for SSR React (react-i18next + remix-i18next)

## Overview

Add localization to a React Router 7 (or Remix) SSR app using `react-i18next` for runtime, `remix-i18next` for server-side detection, `i18next-parser` for key extraction, and `eslint-plugin-i18next` for "no untranslated strings" enforcement. Translation files are bundled at build time — no async loader on first paint.

## When to use this skill

Trigger when:
- User asks to add i18n / localization / translation to a React app.
- App is React Router 7 or Remix (has `entry.server.tsx`, loaders, `ssr: true`).
- Need typed translation keys, key-extraction tooling, or lint-level enforcement against hardcoded JSX literals.

Skip when: app is a pure SPA (no SSR) — drop `remix-i18next` and use plain `i18next-browser-languagedetector`. The other patterns still apply.

## Quick start

1. Install deps: `i18next react-i18next remix-i18next` (runtime), `i18next-parser eslint-plugin-i18next` (dev). See `references/setup.md`.
2. Scaffold `app/i18n/{config.ts, server.ts, client.ts, types.ts, locales/<lng>/<ns>.json}`. See `references/setup.md`.
3. Wire `root.tsx` loader to return `{ locale }`, call `useChangeLanguage(locale)` in `Layout`, set `<html lang={locale}>`. See `references/detection.md`.
4. Wrap SSR render in `<I18nextProvider>` in `entry.server.tsx`. See `references/setup.md`.
5. Configure `i18next-parser.config.ts` with scoped input glob; add `i18n:extract` and `i18n:check` scripts. See `references/enforcement.md`.
6. Add `eslint-plugin-i18next` to flat config with an `overrides` block scoped to translated directories. See `references/enforcement.md`.

## Architecture summary

**Two i18n instances:**
- **Server**: `createInstance()` per request (no cross-request state leak). Initialized with locale from `i18nServer.getLocale(request)`.
- **Client**: singleton in `entry.client.tsx`. Synced to server-decided locale via `useChangeLanguage(locale)` hook — prevents hydration mismatch.

**Detection priority (server-side):** `?lang=` query → cookie (e.g. `app-locale`) → `Accept-Language` header → `fallbackLng`. Configured via `remix-i18next`'s `RemixI18Next` constructor.

**Resources** bundled at build time (no HTTP fetch on first paint). One `<lng>/<ns>.json` per (language, namespace) under `app/i18n/locales/`.

## Common pitfalls (read `references/pitfalls.md` before debugging)

- **Prerendered routes flicker.** Any route in `react-router.config.ts`'s `prerender` list ships static HTML at build time and cannot honor `Accept-Language` — those routes flash the fallback language until client-side hydration.
- **Prop-based visible text is not lint-caught.** `eslint-plugin-i18next`'s `no-literal-string` with `markupOnly: true` only flags JSX text nodes. Strings in `title="..."`, `subtitle="..."`, `label="..."` need manual translation. Turning `markupOnly` off floods warnings on legitimate enum-like props (`variant="primary"`).
- **Hydration mismatch on `<html lang>`.** If client and server pick different locales, React errors. Always set `<html lang={locale}>` from loader data and call `useChangeLanguage(locale)` before render.
- **`supportedLngs` strictness.** A locale not in `supportedLngs` (e.g. `fr` when only `['en', 'es']`) falls through to `fallbackLng`. Add new languages to `supportedLngs` AND ship the JSON files together.

## References

| File | Topic |
|---|---|
| `references/setup.md` | Dependencies, file layout, `config.ts` / `server.ts` / `client.ts` / `types.ts` code |
| `references/wiring.md` | `root.tsx` loader, `entry.server.tsx` provider, `entry.client.tsx`, using `t()` (interpolation, plurals, outside components) |
| `references/detection.md` | Detection priority chain, cookie semantics, `useChangeLanguage` hook, `?lang=` override behavior |
| `references/enforcement.md` | `i18next-parser` config, `eslint-plugin-i18next` overrides block, typed `t()` via module augmentation, CI workflow |
| `references/pitfalls.md` | Prerender flicker, prop-string blind spots, hydration mismatch, `supportedLngs` vs `fallbackLng` |

## Workflow for adding a new translated string

1. Add `t('ns.key')` in a component covered by the parser's `input` glob.
2. Run `npx i18next-parser --config i18next-parser.config.ts` → writes/updates JSON keys with placeholder values across all locales.
3. Fill in real translations in each locale file.
4. Run validation (`tsc` + `eslint` + parser in `--fail-on-update` mode) — CI fails if any locale is missing keys.
5. Commit JSON files alongside the component change.

## Workflow for expanding translation coverage

To add another directory under enforcement:
1. Append the path to `i18next-parser.config.ts`'s `input` array.
2. Append the same path to `eslint.config.js`'s `i18next` `overrides` block.
3. Re-run extract + fill translations.
