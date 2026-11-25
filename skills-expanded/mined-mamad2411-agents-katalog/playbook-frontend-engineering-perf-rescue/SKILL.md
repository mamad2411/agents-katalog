---
name: playbook-frontend-engineering-perf-rescue
description: "Move a lagging app's Core Web Vitals into green without a rewrite."
---
# Playbook: Rescue a slow frontend

> Move a lagging app's Core Web Vitals into green without a rewrite.

**Track:** 🗺️ Frontend Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~105 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Move a lagging app's Core Web Vitals into green without a rewrite.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Fix Core Web Vitals regressions systematically: start with "Pull field data (RUM) first; lab scores only reproduce what field data flags"
2. Step 2 — Ship images that cost almost nothing: start with "Serve AVIF/WebP with automatic fallbacks via an image component or CDN"
3. Step 3 — Put JavaScript bundles on a diet: start with "Generate a bundle report; list the ten largest modules per route"
4. How it fits together: Field data first, always. Fix LCP before INP before CLS — perceived speed compounds.

### Referenced Skills

- `web-performance-core-web-vitals`
- `web-performance-image-pipeline`
- `web-performance-js-bundle-diet`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill web-performance-core-web-vitals && npx skills add aniruddhaadak80/skills --skill web-performance-image-pipeline && npx skills add aniruddhaadak80/skills --skill web-performance-js-bundle-diet
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills