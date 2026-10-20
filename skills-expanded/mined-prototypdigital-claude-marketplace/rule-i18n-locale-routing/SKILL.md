---
name: i18n-locale-routing
description: Configure next-intl routing in one place — an explicit locales list, a single fallback locale, a deliberate localePrefix strategy, and a typed pathnames map. Never detect locales ad hoc.
---

# next-intl locale routing

Locale routing scattered across middleware, layouts, and link helpers drifts: a locale added in one place but not another produces 404s, untranslated pages, or links that drop the prefix. Define it once and import it everywhere.

## Rules

- Declare the supported `locales` array and the single `defaultLocale` in **one** shared routing config (e.g. `src/i18n/routing.ts`) and import it into the middleware, navigation helpers, and layout — never re-list locales inline.
- Derive a `Locale` union type from that array (`(typeof locales)[number]`) and use it everywhere a locale is typed — never `string`.
- Choose `localePrefix` deliberately (`'always'` | `'as-needed'` | `'never'`) and document why; switching it later changes every URL and breaks existing links.
- Use next-intl's typed `pathnames` map for any localized/translated path segments instead of hand-building locale-prefixed strings.
- Build internal links and redirects through next-intl's navigation APIs (`Link`, `redirect`, `usePathname`, `getPathname` from `createNavigation`), so the active locale prefix is always preserved.

## Examples

```ts
// BAD — locales hardcoded inline in the middleware, separate from the rest of the app;
// links hand-build the prefix, so a dropped/extra prefix silently 404s
export default createMiddleware({ locales: ['en-GB', 'de-DE'], defaultLocale: 'en-GB' })
<a href={`/${locale}/about`}>About</a>

// GOOD — one routing source of truth, a Locale union, navigation via next-intl
// src/i18n/routing.ts
export const locales = ['en-GB', 'de-DE', 'fr-FR', 'nl-NL', 'pl-PL'] as const
export type Locale = (typeof locales)[number]
export const routing = defineRouting({ locales, defaultLocale: 'en-GB', localePrefix: 'always' })
export const { Link, redirect, usePathname } = createNavigation(routing)

// src/middleware.ts
import { routing } from '@/i18n/routing'
export default createMiddleware(routing)

// usage — prefix is always preserved
<Link href="/about">About</Link>
```

## Gotchas

- The middleware `matcher` must exclude `/api`, `/_next`, and static assets, or it will rewrite asset/API requests and break them.
- `defaultLocale` with `localePrefix: 'as-needed'` means the default locale has no prefix — make sure route guards and canonical URLs account for both the prefixed and unprefixed form.
