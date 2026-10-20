---
name: vue-i18n
description: Vue I18n v9 standards — useI18n, t(), locale switching, lazy loading, and pluralisation. Load when working with Vue I18n.
user-invocable: false
stack: i18n/vue-i18n
paths:
  - "**/i18n/**"
  - "**/locales/**"
  - "**/vue-i18n/**"
---

Full standards in [vue-i18n.md](vue-i18n.md). Always-on summary:

> **Scope — applies only if this project uses vue-i18n.** This layer shares `**/locales/**` with `lingui` in `layers/i18n/`, so more than one may load at once and their rules conflict. If the project is not using vue-i18n, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

**Composition API:**
- Use `const { t } = useI18n(` inside `<script setup>` — destructure `{ t, locale, n, d }` as needed
- Call `t('key')` for simple strings; `t('key', { name })` for interpolation; `t('key', count)` for plurals
- For template-only components, use the `$t` global — but prefer `useI18n` for type safety

**Locale switching:**
- Change `locale.value` to switch language reactively — Vue I18n updates all bound strings immediately
- Persist the selected locale to `localStorage` and restore on app init
- Validate the locale against your supported list before applying it

**Lazy loading:**
- Do not bundle all locale files upfront — use dynamic imports per locale
- Load the default locale eagerly; load others on demand when `locale.value` changes
- Use `setLocaleMessage(locale, messages)` after the dynamic import resolves

**Pluralisation:**
- Use the built-in plural rule — `t('apples', count)` with message `apples: 'no apples | one apple | {count} apples'`
- Provide all plural forms for every locale — missing forms fall back to the last defined form

**Message files:**
- Keep messages in JSON or YAML under `src/locales/<locale>.json`
- Structure: `messages: { en: { ... }, fr: { ... } }` — one object per locale
- Nest keys by feature: `{ "orders": { "title": "…", "empty": "…" } }`
- Never concatenate translated strings to form sentences — use interpolation or `<i18n-t>` component

**Never:**
- Use `$i18n.locale` mutation directly — use the `locale` ref from `useI18n()`
- Hardcode user-visible strings outside message files
- Ship untranslated fallback strings to production without monitoring for missing keys

**Related skills:** `i18n/lingui` (React alternative), `frontend/vue` (Vue app setup), `error-handling`
