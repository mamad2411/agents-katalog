---
name: css-design-systems-animation-craft
description: "Animate with purpose: entrance choreography, micro-interactions, and reduced-motion respect."
---
# Add motion that guides attention

> Animate with purpose: entrance choreography, micro-interactions, and reduced-motion respect.

**Track:** 🎨 Frontend Engineering · **Domain:** CSS & Design Systems · **Level:** intermediate · **~30 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Animate with purpose: entrance choreography, micro-interactions, and reduced-motion respect.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define durations: 150ms feedback, 250ms transitions, 400ms entrances max
2. Animate transform and opacity only; layout properties cause jank
3. Choreograph staggered lists at 40-70ms increments
4. Give interactive elements hover AND active AND focus-visible motion
5. Wrap all animation in prefers-reduced-motion guards offering static fallbacks
6. Profile long pages; drop anything causing dropped frames mid-scroll

## Common Pitfalls

- Entrance animations replaying on every tab return
- Parallax that fights scroll-linked rendering on mobile

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill css-design-systems-animation-craft
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill css-design-systems-animation-craft -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills