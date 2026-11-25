---
name: accessibility-semantic-first-markup
description: "Native elements carry behavior and semantics for free; ARIA is the fallback, not the default."
---
# Write semantic markup before reaching for ARIA

> Native elements carry behavior and semantics for free; ARIA is the fallback, not the default.

**Track:** 🎨 Frontend Engineering · **Domain:** Accessibility · **Level:** foundation · **~25 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Native elements carry behavior and semantics for free; ARIA is the fallback, not the default.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Choose native elements: button not clickable-div, real headings in order
2. Use landmarks (nav, main, aside) so screen readers can jump regions
3. Label every input visibly; placeholder is not a label
4. Reserve ARIA for composite widgets you truly build custom
5. Test heading outline reads like the page's table of contents
6. Keep interactive targets 24px minimum with adequate spacing

## Common Pitfalls

- aria-label duplicating visible text, read twice
- Skip-links pointing to containers lacking tabindex

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill accessibility-semantic-first-markup
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill accessibility-semantic-first-markup -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills