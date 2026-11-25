---
name: i18n-localization-setup
description: Externalizes user-facing text into message catalogs keyed by stable IDs and wires locale-correct rendering — ICU MessageFormat plurals/gender/select, named-placeholder interpolation, Intl/CLDR number/date/list/relative-time formatting, RTL/bidi via logical CSS, and an extract→translate→compile pipeline with pseudo-localization.
when_to_use: Making a product support multiple languages/locales, or auditing existing i18n — hardcoded UI strings, sentence concatenation, English-only `if(n===1)` plurals, missing RTL, locale-blind number/date formatting, or wiring i18next/react-intl/gettext/Rails i18n/Fluent. Distinct from style-responsive-tailwind (visual layout) and audit-accessibility-wcag (a11y conformance — i18n only owns translatable a11y *attribute text*).
---

## When to Use

Reach for this when text must render correctly in **more than one language/locale**, not just look right:

- "Add Spanish/Arabic/Japanese — what's the right way to externalize strings?"
- "Our plurals break in Polish/Russian" or "we do `count === 1 ? 'item' : 'items'` everywhere"
- "Dates show as `6/15/2026` for everyone" / numbers use `.` for thousands in `de-DE`
- "Arabic/Hebrew layout is broken — everything's still left-to-right"
- "Translators can't reorder words — we concatenate `'Deleted ' + n + ' files'`"
- "Set up the extraction pipeline: extract → PO/XLIFF/JSON → translate → compile" + catch missing keys before ship
- Auditing an app that's "already i18n'd" for the traps below

NOT this skill:
- Visual responsive layout, breakpoints, container sizing → **style-responsive-tailwind** (i18n owns *logical* CSS props + `dir`, not the design system)
- WCAG conformance, screen-reader semantics, contrast → **audit-accessibility-wcag** (i18n only owns making `aria-label`/`alt`/`title` *translatable*)
- `hreflang`, localized URLs, sitemap per-locale, canonical → **audit-technical-seo**
- Validating/parsing user-entered locale data (phone, postal) → **build-form-validation**
- Wrapping a single component's copy as you build it → **build-react-component** (use this skill when standing up the *catalog system*)
- UTC storage, DST, IANA conversion math behind a displayed timestamp → **datetime-timezone-correctness** (i18n only *formats* the instant per locale; it doesn't compute it)

## Steps

1. **Externalize every user-facing string into a catalog keyed by a stable ID — kill concatenation.** A string is translatable if a human ever reads it: labels, buttons, errors, emails, `alt`/`aria-label`/`title`/`placeholder`, `<title>`, push/toast text. Key by **semantic ID**, never by English source (English changes → key shouldn't). Co-locate by feature: `checkout.cart.empty`, not `string_447`.

   ```jsonc
   // en.json — one message = one full sentence with named placeholders
   { "checkout.items": "{count, plural, one {# item} other {# items}}",
     "profile.greeting": "Welcome back, {name}!" }
   ```
   Never build sentences from fragments. `t('deleted') + ' ' + n + ' ' + t('files')` is **untranslatable** — word order, plural agreement, and gender all vary by language. One key = one whole sentence.

2. **Pluralize with ICU MessageFormat / CLDR categories — never `if (n === 1)`.** English has 2 forms; Arabic has **6** (zero/one/two/few/many/other), Polish/Russian have 4. Provide every category the *target* locale's CLDR rules require; `other` is the mandatory fallback. Same mechanism for gender/choice via `select`. Use `#` for the count (auto-formatted per locale), not `{count}` re-interpolated.

   | Need | ICU construct | Anti-pattern it replaces |
   |---|---|---|
   | Count agreement | `{n, plural, one {…} few {…} many {…} other {…}}` | `n === 1 ? 'x' : 'xs'` |
   | Ordinals (1st/2nd) | `{n, selectordinal, one {#st} two {#nd} few {#rd} other {#th}}` | string-suffix hacks |
   | Gender / enum | `{g, select, female {…} male {…} other {…}}` | branching in code, concatenating |
   | Money/percent inside text | `{amt, number, ::currency/EUR}` | manual `$` + `toFixed(2)` |

   Translators supply the categories *their* language needs — don't hardcode the English set into the message shape.

3. **Interpolate with named placeholders so translators can reorder.** `"{count} {unit} remaining"` lets a translator emit `"quedan {count} {unit}"`. Positional `{0}`/`%s`/`printf` ordering is fixed and breaks under reordering — use named only. Pass an explicit values object: `t('checkout.items', { count })`. Escape literal braces per ICU (`'{'`). Auto-escape interpolated values for the sink (HTML) to avoid injection.

4. **Format numbers/dates/lists/units via `Intl` (CLDR) in the user's locale — never roll your own.** Locale decides separators (`1,234.5` vs `1.234,5`), date order, AM/PM vs 24h, RTL digit shaping, list conjunctions. Always pass the resolved locale explicitly; relying on the host default is non-deterministic.

   ```js
   new Intl.NumberFormat(locale, { style: 'currency', currency: 'JPY' }).format(1234)   // ¥1,234
   new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(d)                       // 15 de junio de 2026
   new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-1, 'day')             // "yesterday"
   new Intl.ListFormat(locale, { type: 'conjunction' }).format(['a','b','c'])             // "a, b, and c"
   ```
   `currency` is data, not locale — `de` user paying USD shows `1.234,00 $`. Never store formatted strings; format at render time from raw numbers + ISO/epoch timestamps. Default time storage to **UTC**, convert to the user's IANA timezone for display (the conversion/DST math itself lives in **datetime-timezone-correctness**).

5. **Make layout direction-agnostic: logical CSS + `dir` + bidi isolation.** Set `<html dir="rtl" lang="ar">` from the locale (RTL set: ar, he, fa, ur). Replace physical properties with logical ones so one stylesheet serves both directions:

   | Physical (breaks RTL) | Logical (correct both) |
   |---|---|
   | `margin-left` / `padding-right` | `margin-inline-start` / `padding-inline-end` |
   | `left` / `right` | `inset-inline-start` / `inset-inline-end` |
   | `text-align: left` | `text-align: start` |
   | `border-left` | `border-inline-start` |

   Wrap user/dynamic content of unknown direction in `<bdi>` or `unicode-bidi: isolate` so an Arabic username doesn't scramble surrounding LTR punctuation. Mirror directional icons (back/forward arrows) via `[dir=rtl]` or transform; don't mirror logos.

6. **Stand up the pipeline: extract → catalog → translate → compile, gated by pseudo-loc + missing-key detection.** Source code is the single source of truth for *keys*; translators own values. Pick the format by toolchain:

   | Format | Use with | Plurals |
   |---|---|---|
   | **JSON / ICU** | i18next, react-intl/FormatJS | native ICU |
   | **PO/POT** (gettext) | Rails (`gettext`), Python, PHP, C | `nplurals` header |
   | **XLIFF** | Angular, enterprise TMS handoff | ICU or `<plural>` |
   | **FTL** (Fluent) | Mozilla stack, attribute-rich UI | built-in selectors |

   Pipeline: (1) `extract` keys from source (`i18next-parser`, `formatjs extract`, `xgettext`) → POT/template; (2) merge into per-locale catalogs without dropping existing translations; (3) translate / push to TMS; (4) `compile` to runtime bundles (`formatjs compile`, `msgfmt`). Generate a **pseudo-locale** (`en-XA`: `[!!! Ŝéàŕçĥ ~~~]`) — accent + ~40% length padding + bracket markers — to surface hardcoded strings, truncation, and concatenation in CI before any human translates. Fail the build on missing keys / unknown ICU vars.

7. **Negotiate locale, fall back, and support runtime switching.** Resolve in priority order: explicit user setting → URL/cookie → `Accept-Language` → app default. Match with BCP-47 lookup (`fr-CA` → `fr` → default); never 404 on an unsupported region — fall back to base language, then to source locale. Lazy-load the active locale's bundle (don't ship all 30); switching locale re-renders messages **and** updates `lang`/`dir` on `<html>`. Use a real BCP-47 matcher — `@formatjs/intl-localematcher` (`match()`) or `accept-language-parser` for the header, canonicalized via `Intl.getCanonicalLocales` — never naive string equality (there is no `Intl.LocaleMatcher` global; locale matching is the `localeMatcher` *option* on `Intl` constructors or a library).

## Common Errors

- **`count === 1 ? x : xs`.** Breaks every language with ≠2 plural forms (Arabic, Polish, Russian, Welsh). Use ICU `plural` with CLDR categories.
- **Sentence concatenation** (`t('sent') + name + t('a_msg')`). Word order/agreement/gender vary; translators can't fix it. One key = one full sentence with named placeholders.
- **Keying by English source text.** Editing the copy silently orphans the translation. Key by stable semantic ID.
- **Hand-formatted numbers/dates** (`'$' + n.toFixed(2)`, `MM/DD/YYYY`). Wrong separators/order/currency per locale. Use `Intl.NumberFormat`/`DateTimeFormat` with an explicit locale.
- **Conflating locale with currency/timezone.** A `de` user can pay in USD in `America/New_York`. Format with the user's *locale* but the transaction's *currency* and the event's *timezone*; store UTC + ISO currency code.
- **Physical CSS** (`margin-left`, `float: right`). Layout breaks in RTL. Use logical properties + `dir`.
- **No bidi isolation.** An RTL name/number injected into LTR text reorders adjacent punctuation/brackets. Wrap unknown-direction content in `<bdi>`/`unicode-bidi: isolate`.
- **Forgetting non-`textContent` text.** `alt`, `aria-label`, `title`, `placeholder`, `<title>`, email subjects, validation messages are all translatable — and untranslated `aria-label` regresses a11y.
- **No length budget.** German/Finnish run ~35% longer than English; pseudo-loc padding exposes truncation/overflow before translators do.
- **Locale-blind sort/case.** JS `.sort()` is code-point order (`Ä` after `Z`); Turkish `i`↔`İ`/`ı` breaks `toUpperCase()`. Use `Intl.Collator(locale)` for sorting and `toLocaleUpperCase(locale)` for case.
- **Inventing `Intl.LocaleMatcher`.** No such global exists — locale matching is the `localeMatcher` option on `Intl` constructors or a library (`@formatjs/intl-localematcher`). Don't string-compare BCP-47 tags.
- **Shipping all locales eagerly / hard 404 on unknown region.** Lazy-load active locale; fall back `region → language → source`, never error.
- **Pluralizing the count with `#` but re-interpolating `{count}` raw.** `#` is locale-formatted (`1,000`); a separate `{count}` isn't. Use `#` inside `plural`.

## Verify

1. **No hardcoded strings:** lint (`eslint-plugin-formatjs`, `i18next` no-literal rule) reports zero user-facing literals outside the catalog.
2. **Pseudo-loc pass:** run UI in `en-XA` — every visible string is accented+bracketed (no bare English = no missed key), nothing truncates or overflows, no concatenated fragments appear.
3. **Plural matrix:** render the count message at `n = 0,1,2,5,11,100` in `en`, `pl` (4 forms), and `ar` (6 forms); each picks the CLDR-correct category. `if(n===1)` cannot pass this.
4. **Reordering:** a target locale that reverses placeholder order renders correctly (proves named, not positional, interpolation).
5. **Formatting:** the same number/date/currency/list renders per-locale separators/order (`1,234.5`↔`1.234,5`, `06/15`↔`15/06`, currency symbol placement) — assert against `Intl` golden strings.
6. **RTL:** load `ar`/`he` → `<html dir="rtl">`, layout mirrors via logical props, directional icons flip, bidi-isolated names don't scramble punctuation.
7. **Missing-key gate:** delete a key from a non-source catalog → CI fails (or falls back to source) — it must never render a raw key like `checkout.items` to a user.
8. **Negotiation:** `Accept-Language: fr-CA` with only `fr` available resolves to `fr` (not default/404) via a real matcher; switching locale at runtime updates messages **and** `lang`/`dir`.
9. **Sort/case:** a localized list sorts via `Intl.Collator(locale)` (e.g. Swedish `å/ä/ö` last); Turkish case round-trips with `toLocaleUpperCase('tr')`.

Done = zero hardcoded user-facing strings, pseudo-loc clean, the plural matrix passes for a 4-form and a 6-form locale, RTL renders with logical CSS + bidi isolation, all formatting goes through `Intl` with explicit locale, locale negotiation uses a real BCP-47 matcher, and CI fails on any missing key or unknown ICU variable.
