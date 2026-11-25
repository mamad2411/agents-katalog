---
name: rendering-strategy-rendering-mode-selection
description: "Static/ISR/SSR/streaming/client mapped to freshness needs, personalization, and TTFB budgets."
---
# Select rendering modes per route deliberately

> Static/ISR/SSR/streaming/client mapped to freshness needs, personalization, and TTFB budgets.

**Track:** 🎨 Frontend Engineering · **Domain:** Rendering Strategy · **Level:** advanced · **~40 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Static/ISR/SSR/streaming/client mapped to freshness needs, personalization, and TTFB budgets.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Classify routes: content volatility × personalization × interactivity
2. Default static/ISR for public volatile-slow content with tag revalidation
3. Reserve SSR for truly per-request data; stream shells for perceived speed
4. Never client-fetch server-known data out of habit — that's a waterfall
5. Document choice per route table; mixed strategies confuse debugging
6. Measure TTFB+LCP per mode on real routes after each framework upgrade

## Common Pitfalls

- Whole-app SPA conversion losing SEO overnight
- ISR windows serving stale prices beyond business tolerance

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill rendering-strategy-rendering-mode-selection
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill rendering-strategy-rendering-mode-selection -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills