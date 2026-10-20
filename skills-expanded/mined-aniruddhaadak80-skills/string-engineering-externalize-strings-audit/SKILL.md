---
name: string-engineering-externalize-strings-audit
description: "Systematic extraction, key naming, and context comments making translation safe."
---
# Externalize strings without breaking the app

> Systematic extraction, key naming, and context comments making translation safe.

**Track:** 🌐 Localization & i18n · **Domain:** String Engineering · **Level:** foundation · **~30 min**

**Who this is for:** Localization Engineers, i18n Developers, Localization Managers, Transcreators

## When to Use This Skill

Systematic extraction, key naming, and context comments making translation safe.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Extract all user-visible strings; ban literals in components via lint rule
2. Name keys by semantic meaning (checkout.payment.decline), never by English text
3. Attach translator context comments: where shown, character limits, tone
4. Handle interpolation with ICU MessageFormat; never concatenate translated fragments
5. Add pseudo-localization build mode surfacing hardcoded strings visually
6. Test longest locale (usually de) for layout breakage before shipping

## Common Pitfalls

- Concatenated sentences untranslatable in any other grammar
- Keys named after current English copy, shattering on rewording

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill string-engineering-externalize-strings-audit
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill string-engineering-externalize-strings-audit -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills