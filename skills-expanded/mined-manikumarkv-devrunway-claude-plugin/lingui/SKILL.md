---
name: lingui
description: LinguiJS standards — t`` macro, Trans component, locale extraction, and React setup. Load when working with LinguiJS.
user-invocable: false
stack: i18n/lingui
paths:
  - "**/lingui/**"
  - "**/locales/**"
  - "**/*.po"
  - "**/*.pot"
  - "**/lingui.config.*"
---

Full standards in [lingui.md](lingui.md). Always-on summary:

> **Scope — applies only if this project uses lingui.** This layer shares `**/locales/**` with `vue-i18n` in `layers/i18n/`, so more than one may load at once and their rules conflict. If the project is not using lingui, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

**Macros:**
- Import macros: `import { t } from '@lingui/macro'` and `import { Trans } from '@lingui/react'`
- Use `t` macro for plain strings: `` t`Hello, ${name}` `` — never interpolate into translated strings manually
- Use `<Trans>` component for JSX with embedded elements: `<Trans>Click <a href="…">here</a></Trans>`
- Use `plural` macro for pluralisation: `plural(count, { one: '# item', other: '# items' })`
- `msg` macro marks strings for extraction without immediately translating — use for constants

**Extraction and compilation:**
- Run `lingui extract` after every new string — commit `.po` files alongside code changes
- Run `lingui compile` before production build to compile `.po` files to JS message catalogs
- CI should fail if `lingui extract` produces a diff (use `--clean` flag and check exit code)
- Translators work directly in `.po` files — do not edit `.po` files in generated `messages.js`

**React setup:**
- Wrap app in `<I18nProvider i18n={i18n}>` at the root
- Call `i18n.activate(locale)` when the user switches language
- Lazy-load locale catalogs: `import('@/locales/{locale}/messages')` — do not bundle all locales upfront

**Locale detection:**
- Detect from `navigator.language`, URL segment, or user preference stored in DB
- Fall back to the default locale gracefully — never crash on missing translation

**Never:**
- Hardcode strings outside of macros — they will not be extracted
- Call `t` outside a component or function that has access to the active `i18n` instance
- Commit compiled `messages.js` without the source `.po` — `.po` is the source of truth

**Related skills:** `i18n/vue-i18n` (Vue alternative), `frontend/react` (React app setup), `frontend/nextjs`
