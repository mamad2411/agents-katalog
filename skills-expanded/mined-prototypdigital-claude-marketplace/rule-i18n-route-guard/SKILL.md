---
name: i18n-route-guard
description: In [locale] route segments, validate the locale param against the Locale union and call notFound() for unknown locales — never render with the fallback silently. Type the param, don't accept string.
---

# Locale route guard

An unvalidated `[locale]` param lets `/xx/anything` render the page in the fallback locale with a 200 status. That ships duplicate, wrong-locale content to crawlers and hides broken links. Reject unknown locales explicitly.

## Rules

- In every `[locale]` segment (layout or page), check the incoming `locale` against the shared `locales` list **before** rendering; call `notFound()` if it isn't a known locale.
- Type the param as the `Locale` union, not `string` — `params: { locale: Locale }` — so an unhandled locale is a type error, not a runtime surprise.
- Call next-intl's `setRequestLocale(locale)` (after the guard) in the layout/page so server components render in the right locale and static rendering works.
- Generate `generateStaticParams` from the same `locales` source of truth so only valid locales are pre-rendered.
- Do the guard once at the highest `[locale]` boundary (the locale layout), not duplicated in every leaf page.

## Examples

```tsx
// BAD — param typed as string, no validation: /zz/about renders in the fallback locale with a 200
export default async function LocaleLayout({ params }: { params: { locale: string } }) {
  return <html lang={params.locale}>{/* ... */}</html>
}

// GOOD — typed param, explicit guard, then setRequestLocale
import { notFound } from 'next/navigation'
import { setRequestLocale } from 'next-intl/server'
import { locales, type Locale } from '@/i18n/routing'

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }))
}

export default async function LocaleLayout({
  params,
}: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params
  if (!locales.includes(locale)) notFound()   // unknown locale → 404, not silent fallback
  setRequestLocale(locale)
  return <html lang={locale}>{/* ... */}</html>
}
```

## Gotchas

- In Next.js 15 `params` is a Promise — `await` it before the guard; a synchronous `.locale` access is a type/runtime error.
- `setRequestLocale` must come **after** the guard — calling it with an invalid locale defeats the point.
