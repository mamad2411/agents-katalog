---
name: i18n
description: Internationalization and localization — message catalogs, ICU plurals/interpolation, Intl formatting, locale routing, RTL, locale-aware input validation. Use when adding or fixing translations, multi-locale UI, date/number/currency formatting, language switching, or RTL support. 日本語の依頼例:「多言語対応」「i18n入れて」「翻訳」「ロケール切り替え」「日付/通貨の表示」「RTL対応」「言語切替」。
---

# Internationalization

## No hardcoded user-facing strings

- Every user-visible string comes from a message catalog keyed by ID — never a literal in JSX. This is the one rule that, if skipped, makes everything else impossible to retrofit.
- Use the framework-idiomatic library: `next-intl` (Next.js App Router), `react-i18next` / `react-intl` (Vite SPA), Astro's i18n routing + a catalog. One per repo (dependency ask-first rule applies).
- Keys are semantic and namespaced (`checkout.payment.submit`), not the English text. Keep catalogs shallow (≤3 levels) and run a missing/orphaned-key check in CI (`i18next-parser --fail-on-update`, or the library's extractor) — wire it as a gate, don't rely on memory.
- Translator-facing context: provide a description for ambiguous keys; never concatenate sentence fragments across keys (word order differs per language).

## Plurals, gender, interpolation — ICU MessageFormat

- Never build plurals with `count === 1 ? 'item' : 'items'` — many languages have 3–6 plural categories. Use ICU `{count, plural, ...}` and let the library + locale data decide.
- Interpolate variables through the catalog (`{name}`), never via template-string concatenation around a translated fragment.
- Rich/linked text: use the library's component interpolation (`<Trans>` / `t.rich`), not `dangerouslySetInnerHTML` on a translated string (see `frontend-security`).

## Formatting — always `Intl`, never hand-rolled

- Dates/times: `Intl.DateTimeFormat` with an explicit locale and time zone. Store/transport UTC; render in a deliberately chosen zone; label it when ambiguous (consistent with `data-viz`).
- Numbers/currency/units/lists: `Intl.NumberFormat` (with `style: 'currency'` + currency code), `Intl.ListFormat`, `Intl.RelativeTimeFormat`. No manual thousands separators, decimal marks, or "3 days ago" strings — these differ per locale.
- Currency: format with the data's currency, not the UI locale's; never assume `$`.

## Routing & locale negotiation

- Locale in the URL (`/ja/...` subpath, or domain) so pages are linkable, cacheable, and indexable — not only a cookie/header. Emit `hreflang` alternates and set `<html lang>` (and `dir`) per request.
- Negotiate initial locale from the URL → stored preference → `Accept-Language`, with a sane default; let users switch explicitly and persist it.
- SSR/RSC: load only the active locale's catalog on the server and pass it down; don't ship every language's messages to the client (bundle bloat). Code-split catalogs by locale/route.

## RTL & layout

- Drive direction from data: `<html dir="rtl">` for RTL locales; never hardcode LTR assumptions.
- Use CSS logical properties (`margin-inline`, `inset-inline-start`, `text-align: start`) — mandated already by `css-modules`, and the reason it's mandated. Physical `left`/`right` breaks RTL.
- Mirror directional icons (arrows, chevrons) in RTL; don't mirror logos or media. Test one RTL locale (e.g. `ar`) as a first-class case, plus a pseudo-locale for length/encoding.

## Locale-aware input & validation

- Accept locale-formatted input (decimal comma, native digits, local date order) and parse to a canonical form before validating with zod (see `frontend-security`) — validate the parsed value, store canonical.
- Names/addresses/phone: don't assume Western structure (first/last, state/ZIP). Keep fields permissive; avoid regex that rejects valid non-Latin input.
- Sorting/search: locale-aware collation (`Intl.Collator`), not byte order.

## Testing

- Pseudo-localization (accented + padded strings) in a story/build catches truncation, clipping, and hardcoded strings early (pairs with `visual-regression` over both LTR and one RTL locale).
- Stories cover at least one non-English and one RTL locale for layout-sensitive components (see `storybook`).
