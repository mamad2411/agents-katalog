---
name: css-design-systems-design-tokens-tailwind
description: "Encode brand decisions as named tokens (CSS variables) consumed by utilities so themes change in one place."
---
# Set up design tokens for color, space, type (Tailwind setup)

> Encode brand decisions as named tokens (CSS variables) consumed by utilities so themes change in one place.

**Track:** 🎨 Frontend Engineering · **Domain:** CSS & Design Systems · **Level:** intermediate · **~35 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Encode brand decisions as named tokens (CSS variables) consumed by utilities so themes change in one place.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define scales: one neutral ramp plus accent ramps, 8px spacing ladder, modular type scale
2. Name by role (bg-surface, text-muted), never by value (gray-3)
3. Expose as CSS variables; map Tailwind colors to var() references
4. Add dark mode by swapping variable values under a media or class hook
5. Lint for raw hex values outside the token file
6. Ship a living style page rendering every token with its name
7. Reference variables in tailwind.config so utilities emit them
8. Use opacity modifiers carefully; they require rgb/hsl channel variables

## Common Pitfalls

- Role names that encode light mode assumptions breaking dark theme
- Token sprawl: 40 grays nobody can choose between

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill css-design-systems-design-tokens-tailwind
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill css-design-systems-design-tokens-tailwind -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills