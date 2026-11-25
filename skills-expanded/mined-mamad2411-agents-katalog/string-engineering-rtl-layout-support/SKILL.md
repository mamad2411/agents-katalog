---
name: string-engineering-rtl-layout-support
description: "Logical properties, mirrored iconography decisions, and bidi text handling done right."
---
# Support RTL layouts properly

> Logical properties, mirrored iconography decisions, and bidi text handling done right.

**Track:** 🌐 Localization & i18n · **Domain:** String Engineering · **Level:** intermediate · **~35 min**

**Who this is for:** Localization Engineers, i18n Developers, Localization Managers, Transcreators

## When to Use This Skill

Logical properties, mirrored iconography decisions, and bidi text handling done right.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Convert directional CSS to logical properties (margin-inline-start etc.)
2. Decide per-icon mirroring: directionals mirror, brand/symbols don't
3. Handle mixed-direction text with unicode-bidi isolation, not manual flips
4. Test carousels/drawers/progress flows in RTL — they invert subtly
5. Numbers/phone formats stay LTR within RTL paragraphs deliberately
6. Screenshot-snapshot both directions in CI for every component

## Common Pitfalls

- position:absolute left/right hardcodes exploding in Arabic
- Mirrored brand logos looking like counterfeits

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill string-engineering-rtl-layout-support
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill string-engineering-rtl-layout-support -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills