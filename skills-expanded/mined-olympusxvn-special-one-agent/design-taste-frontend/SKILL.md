---
name: design-taste-frontend
description: Anti-slop frontend taste engine. Reads the brief, sets three dials (VARIANCE / MOTION / DENSITY), and ships interfaces that do not look templated. This repo vendors a RUNTIME port of the skill as `lib/skills/taste/` so product UI consumes the same taste decisions via a typed hook.
source: https://github.com/Leonxlnx/taste-skill (MIT, © 2026 Leonxlnx)
---

# taste-skill (vendored runtime port)

The upstream [`taste-skill`](https://github.com/Leonxlnx/taste-skill) is a
portable **agent skill** — Markdown instructions an AI agent loads to build
anti-slop frontends. It is not a runtime SDK.

This folder is a faithful, decoupled **runtime port** of its core decision
model so the same taste rules drive real components at runtime, not just at
generation time.

## The three dials (core configuration)

Every layout, motion, and density decision is gated by three 1–10 dials:

| Dial | 1 | 10 |
|---|---|---|
| `DESIGN_VARIANCE` | perfect symmetry | artsy chaos |
| `MOTION_INTENSITY` | static | cinematic / physics |
| `VISUAL_DENSITY` | art gallery / airy | cockpit / packed |

Baseline is `8 / 6 / 4`. Use a preset (`premiumConsumer`, `landingSaaS`,
`landingAgency`, `editorial`, `trustFirst`, …) then override conversationally.

## Anti-slop discipline (carried over from upstream)

- No AI-purple gradient + centered hero over dark mesh as a reflex.
- No three equal feature cards by default.
- Glassmorphism is honest: `backdrop-filter` + layered borders + a solid-fill
  fallback for `prefers-reduced-transparency`. There is no official
  "liquid glass" package; web versions are approximations — label them so.
- `min-h-[100dvh]` for hero (never `h-screen`). CSS Grid over flex %-math.
- Respect `prefers-reduced-motion` (the hook does this automatically).

## Runtime usage

```ts
import { useTasteSkill, LUXURY_WC_TASTE } from "@/lib/skills/taste";

const taste = useTasteSkill(LUXURY_WC_TASTE);
// taste.dials   → resolved 1–10 dials
// taste.tokens  → spacing / motion timing / variance hints
// taste.motion  → framer-motion-compatible variants (fadeRise, scaleIn, …)
```

## Reinstall the upstream agent skill

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

See `README.md` in this folder for detach/plug instructions.
