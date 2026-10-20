---
name: playbook-localization-i18n-global-ready
description: "Externalized strings, RTL support, and locale-data correctness verified by smoke suites."
---
# Playbook: Make a product truly global-ready

> Externalized strings, RTL support, and locale-data correctness verified by smoke suites.

**Track:** 🗺️ Localization & i18n · **Domain:** Journey Playbooks · **Level:** journey · **~65 min**

**Who this is for:** Localization Engineers, i18n Developers, Localization Managers, Transcreators

## When to Use This Skill

Externalized strings, RTL support, and locale-data correctness verified by smoke suites.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Externalize strings without breaking the app: start with "Extract all user-visible strings; ban literals in components via lint rule"
2. Step 2 — Support RTL layouts properly: start with "Convert directional CSS to logical properties (margin-inline-start etc.)"
3. How it fits together: Pseudo-localization early beats Arabic-layout archaeology later.

### Referenced Skills

- `string-engineering-externalize-strings-audit`
- `string-engineering-rtl-layout-support`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill string-engineering-externalize-strings-audit && npx skills add aniruddhaadak80/skills --skill string-engineering-rtl-layout-support
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills