---
name: open-source-law-license-selection-strategy
description: "Permissive vs copyleft vs source-available tradeoffs matched to project goals."
---
# Choose open-source licenses strategically

> Permissive vs copyleft vs source-available tradeoffs matched to project goals.

**Track:** ⚖️ Legal & Compliance · **Domain:** Open Source Legal · **Level:** intermediate · **~30 min**

**Who this is for:** Legal Ops, Privacy Officers, Compliance Teams, Founders, Engineers

## When to Use This Skill

Permissive vs copyleft vs source-available tradeoffs matched to project goals.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define what you want others to do/not do with your code first
2. MIT/Apache-2.0 for maximal adoption; Apache adds patent grant + NOTICE
3. Copyleft (GPL/AGPL) when protecting downstream openness matters more than spread
4. Consider dual-licensing or CLAs if commercialization is planned
5. Add LICENSE + copyright headers consistently from commit one
6. Review dependency licenses for compatibility before every release

## Common Pitfalls

- AGPL adopted casually then blocking enterprise deals unexpectedly
- License files absent while README claims MIT mysteriously

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill open-source-law-license-selection-strategy
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill open-source-law-license-selection-strategy -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills