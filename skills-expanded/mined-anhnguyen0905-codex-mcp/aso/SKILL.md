---
name: aso
description: App store optimization — ASO, store listing and product page, App Store and Google Play metadata, title/subtitle/short description, keyword field and long description indexing, keyword research relevance vs search volume, icon screenshots and preview video creatives, store page conversion rate and impression-to-install funnel, per-locale localisation, A/B test store listing (Product Page Optimization, Play Store Listing Experiments), ratings and reviews impact, and iteration cadence.
---

# ASO (store listing discoverability and conversion)

## The two jobs, kept separate

```
installs    = impressions × store-page CVR (impression → install)
impressions ≈ search/browse/referral traffic won by relevance and ranking
```

Metadata mostly moves **impressions** — which queries you can appear for at all. Creatives mostly
move **CVR** — whether that traffic converts. Diagnose which half moved first: installs falling with
CVR flat is a traffic problem, installs falling with impressions flat is a page problem. Paid traffic
lands on the same page, so a CVR win compounds across all UA spend.

## Metadata fields and what each affects

- **Apple App Store**: app name, subtitle and the character-limited keyword field are indexed for
  search; the description is *not*, so it is purely a conversion asset. No repetition across fields,
  no wasted comma spacing, no plural duplicates. IAP and developer names also carry indexing weight.
- **Google Play**: title, short description and long description are all indexed, so the long
  description carries real search weight — but users read it, so stuffing costs conversion; natural
  repetition of the priority term beats a keyword list.
- Both: title and the first line of subtitle/short description are the highest-leverage text — what
  a browsing user reads before deciding.

## Keyword research: relevance before volume

Build the term set from real query sources — store autosuggest, competitor listings, search-term
reports from paid app campaigns, support tickets, category vocabulary. Triage each term on relevance
to what the app actually does, estimated volume, and difficulty (who ranks now, how entrenched).
Prefer ranking well for a moderate-volume term you genuinely satisfy over placing low on a head term:
irrelevant traffic depresses CVR and the ranking signals that follow it. Track rank *and* installs
per term — rank alone hides worthless traffic.

## Creatives are the real conversion lever

The **icon** appears in every impression, so it gates result-list CTR as well as page CVR and must
read at thumbnail size. **Screenshots**: the first one or two are all most users see — lead with the
single strongest value message, text legible small, promise consistent with the product or you buy
churn instead of retention. A **preview/promo video** can lower CVR as easily as raise it depending on
its first seconds; test it, never assume.

Localise per store *locale*, not per language family: keyword sets, screenshot text and cultural
references differ between locales that nominally share a language, and machine-translated keyword
fields miss how people actually search. Prioritise locales with organic impressions but below-average
CVR — the traffic exists and the page is the constraint.

## A/B testing store listings

Google Play offers native store listing experiments; Apple offers Product Page Optimization with
limits on concurrent treatments plus its own traffic and duration rules — check current platform
constraints before designing the test, as both change. Rules that hold on either: change one element
at a time (icon *or* first screenshot, never both), pre-commit the primary metric and minimum
runtime, run whole weeks to absorb day-of-week effects, let the platform's own significance call end
the test rather than stopping on a lead, and attribute only within the split traffic.

Rating average and volume feed both ranking inputs and the user's decision on the page: prompt at
genuine success moments, reply to reviews (future readers see the reply), never reset ratings with a
version bump you did not need. Cadence — one metadata change per cycle, one creative test at a time,
cycles long enough to read weekly seasonality, and a dated change log, without which a ranking move
two months later cannot be traced to any cause.

## Failure modes

- Judging ASO on installs while paid spend, seasonality or a featuring slot moved underneath; or
  shipping metadata and creative changes in one release, then crediting one of them.
- Stuffing a Play long description and losing more CVR than the ranking gained.
- Chasing a head term the app does not satisfy, then blaming conversion; or reading third-party rank
  trackers as truth rather than as estimates.

## Reviewer checklist

- [ ] Impressions and store-page CVR reported separately before any diagnosis
- [ ] Metadata plan correct field-by-field for each store's indexing rules
- [ ] Keyword set triaged on relevance, volume and difficulty, with sources named
- [ ] One element per test, with pre-committed primary metric and minimum runtime
- [ ] Tests read at platform significance, whole weeks, no early stop, split-traffic only
- [ ] Locale plan per store locale with CVR-gap evidence, not machine-translated keywords
- [ ] Ratings/review approach stated, no unnecessary version resets, dated change log kept

## Provenance

The platform mechanics stated here (which fields each store indexes, the existence of native listing
experiments) reflect long-standing published store behaviour but change often — verify against current
Apple and Google developer documentation before acting. Field lengths, experiment limits and every
threshold are **derived, unverified**; replace any numeric target with the project's own measured
values before treating as a target. No vendor benchmark or industry statistic is cited, none verified.
