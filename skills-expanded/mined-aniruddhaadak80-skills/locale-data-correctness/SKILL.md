---
name: locale-data-correctness
description: "ICU-driven formatting, name ordering, address forms, and timezone correctness per locale."
---
# Get locale data right: dates, numbers, names

> ICU-driven formatting, name ordering, address forms, and timezone correctness per locale.

**Track:** 🌐 Localization & i18n · **Domain:** Linguistic Quality · **Level:** foundation · **~25 min**

**Who this is for:** Localization Engineers, i18n Developers, Localization Managers, Transcreators

## When to Use This Skill

ICU-driven formatting, name ordering, address forms, and timezone correctness per locale.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Format dates/numbers/currency through Intl APIs — never hand-roll patterns
2. Collect names as given/family separately OR single full-name field, per culture
3. Address forms per country via validated libraries, not one global template
4. Store timestamps UTC + IANA zone; display in user zone explicitly
5. Pluralization via CLDR rules for every supported language in tests
6. Locale smoke suite: de long text, ar RTL, ja no-spaces, es-MX currency

## Common Pitfalls

- MM/DD/YYYY assumptions shipped worldwide
- Currency symbols concatenated in wrong position per locale

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill locale-data-correctness
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill locale-data-correctness -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills