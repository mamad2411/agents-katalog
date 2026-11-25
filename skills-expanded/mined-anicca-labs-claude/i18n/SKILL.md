---
name: i18n
description: Internationalisation for Next.js — optional, adopt when the product needs a second locale. Covers the next-intl setup shape and the rules that make later adoption cheap.
---

**This skill is optional.** A B2B dashboard often ships English-only for a long time — do not add an i18n layer speculatively. Adopt it when a real second locale is on the roadmap.

## Until then — keep adoption cheap

- Keep user-visible strings in JSX/components, not buried in utils or constants shared with server logic — extraction later is then mechanical
- Never build UI strings by concatenation (`'Delete ' + name + '?'`) — word order differs across languages; use full sentences with interpolation slots
- Format dates and numbers with `date-fns` / `Intl.NumberFormat` from day one — those are the hardest strings to retrofit

## When adopting: next-intl

`next-intl` is the default choice for App Router — it supports server components, per-locale routing (`app/[locale]/…`), and typed message keys.

```bash
yarn add next-intl
```

Setup shape (follow the current next-intl App Router guide via context7 for exact file names — the API has moved across majors):

1. Messages per locale in `messages/<locale>.json`
2. A request-scoped config that resolves the locale (from the URL segment or the user's profile) and loads its messages
3. `NextIntlClientProvider` in the locale layout for client components; `getTranslations` in server components
4. Locale-prefixed routing via the next-intl middleware, composed with the existing Supabase session middleware — both must run; compose them in one `middleware.ts`, don't add a second file

```tsx
// server component
const t = await getTranslations('projects');
<h1>{t('title')}</h1>

// client component
const t = useTranslations('projects');
```

## Rules

- One source of truth for the locale (URL segment for public pages, user profile for the dashboard) — don't mix
- Never leave a key untranslated in a shipped locale file — missing keys throw in dev; fill every locale before merging
- Third-party error messages (Supabase, Stripe) arrive in English regardless of locale — map known strings to translated copy in the component; never display `error.message` raw
- Revisit `coding-standards` string rules when adopting: every user-visible string moves into the message catalog in the same PR that introduces the locale switch
