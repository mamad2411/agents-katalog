---
name: privacy-data-privacy-by-design-review
description: "Shift privacy questions into design docs so answers shape architecture, not patches."
---
# Run privacy reviews inside feature development

> Shift privacy questions into design docs so answers shape architecture, not patches.

**Track:** ⚖️ Legal & Compliance · **Domain:** Privacy & Data Protection · **Level:** advanced · **~30 min**

**Who this is for:** Legal Ops, Privacy Officers, Compliance Teams, Founders, Engineers

## When to Use This Skill

Shift privacy questions into design docs so answers shape architecture, not patches.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Add privacy section to PRD template: data collected, purpose, retention
2. Trigger full assessment when new data categories or sharing emerge
3. Prefer client-side computation when feasible over collecting raw data
4. Minimize: collect only fields a defined purpose consumes
5. Wire consent flags into actual code paths, not just UI copy
6. Re-assess when vendors change subprocessor chains

## Common Pitfalls

- Consent banners lying about actual SDK behavior
- Analytics collecting more than documented

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill privacy-data-privacy-by-design-review
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill privacy-data-privacy-by-design-review -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills