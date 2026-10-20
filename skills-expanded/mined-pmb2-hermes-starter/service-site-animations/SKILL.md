---
name: service-site-animations
version: 1.0.0
description: "CSS scroll-driven animation and 3D effect patterns for local service business websites — pure CSS transforms + IntersectionObserver, no JS libraries."
metadata:
  hermes:
    tags: [css-animations, scroll-effects, 3d-flythrough, glassmorphism, service-sites]
    triggers:
      - scroll animation
      - CSS flythrough
      - glassmorphism effect
      - service site animation
      - scroll-driven animation
    related_skills: [gsap-animations, service-site-design, service-website-design]
---

# Service Site Animations

Scroll-driven animation and 3D effect patterns for local service business
websites (plumber, landscaper, electrician, painter, roofer, contractor,
cleaning, handyman, HVAC). All patterns use pure CSS transforms with
IntersectionObserver orchestration — no Three.js, GSAP, or library CDN.

## Core Techniques

### 3D Camera Flythrough (scroll-world style)

Creates a "camera flying through a 3D world" effect as the user scrolls.
Uses CSS perspective + translate3d to position elements in Z-space.

**Container:** `perspective: 1000px; transform-style: preserve-3d;`

**Element positioning:** Each object gets a Z depth (-200 to -1500px).
Scroll drives cameraZ = -scrollProgress × 800 through the layer stack.

**Perspective scaling:** `scale = 1000 / (1000 + relDepth)`
Objects closer to camera appear larger, farther ones appear smaller and drift
laterally (parallax). Objects rotate slowly for depth perception.

**Scene labels:** 4 scenes with overlapping scroll keyframes (0-25%, 20-45%,
40-65%, 60-100%). Each cross-fades as the camera passes through.

**Progress indicator:** Thin 20px bar at bottom-right, width tracks scroll %.

**DOM structure:**
```
<div style="perspective:1000px;transform-style:preserve-3d">
  <!-- each object: -->
  <div style="transform:translate3d(x, y, Zdepth)">...</div>
</div>
```

### Pill-Nav Glassmorphism

Floating rounded navbar that sits above all content. Works on any background.

**CSS:** backdrop-filter blur(16px) saturate(180%), bg rgba(255,255,255,0.85),
border-radius 9999px, box-shadow 0 2px 8px rgba(0,0,0,0.06)

Must position the header `fixed top-0 z-50` so it overlays the 3D canvas.

### Button Text Roll

On hover, the button text scrolls upward to reveal a duplicate underneath.
The text is duplicated in a flex-column container with overflow:hidden.
On group-hover, the inner container translates -50% vertically.

Duration: 0.5s. Easing: cubic-bezier(0.25,0.1,0.25,1) — the motionsites
standard curve used throughout.

The arrow icon rotates -45deg on hover using the same timing.

## Design Rules (from the operator, July 2026)

These are hard rules for every template. Zero tolerance.

1. **NO badge/pill/chip elements.** Never render "Niche — City" pills,
   "★ rated · N clients" tags, or any decorative pill/badge/chip in the hero
   or anywhere visible. These are dead AI-slop giveaways.
2. **NO star ratings (★).** No `★` characters anywhere in templates, data,
   or generator output. Remove the `stars()` helper. No star display in
   review cards or hero sections.
3. **NO em dashes (—) in rendered content.** Replace every em dash in template
   copy, meta descriptions, section headers, and copy text with commas,
   periods, spaces, or nothing. Em dashes in JSDoc/comments are fine.
4. **NO middle dots (·) as badge separators.** The `niche · city` pattern
   is a badge. Remove it completely.
5. **Per-site uniqueness.** Every generated site must look different — use
   different templates, color palettes, stats (yearsInBusiness, reviewCount,
   jobsCompleted). Never produce two near-identical sites.

## Template Architecture Pitfalls

### Critical: Stray `</div>` closes the wrapper early

When adding a `pill-nav` to an existing template, the inner `<nav>` tag
had its closing tag accidentally changed from `</nav>` to `</div>`.

**Symptom:** A full-viewport-height blank gap appears between the header and
hero section on ALL sites using that template.

**Root cause:** The stray `</div>` closes the OUTER wrapper div (the one with
`bg-color` and `min-h-screen`) right after the header, instead of after the
hero. The `min-h-screen` makes the near-empty wrapper fill the viewport with
empty background.

**Fix:** Verify every template's nav closing tag:
```
<nav class="pill-nav...">          ← opens correctly
  ...
  </div>                           ← BUG: closes the outer wrapper!
</header>
```

Should be:
```
<nav class="pill-nav...">          ← opens correctly
  ...
  </nav>                           ← correctly closes the nav
</header>
```

### Header Position Dictates Hero Padding

This table governs how much `pt-` the hero section needs:

| Header type | In flow? | Hero padding | Why |
|------------|----------|-------------|-----|
| `fixed`    | No       | `pt-28` (112px) | Nav overlays content; need padding to clear fixed height |
| `absolute` | No       | `pt-16` (64px) | Same as fixed, nav is out of flow |
| `sticky`   | Yes      | `pt-4` (16px)  | Header pushes hero down naturally; minimal breathing room |
| `relative` | Yes      | `pt-4` (16px)  | Same as sticky |

If you set `pt-24` (96px) on a sticky-header template, you create a visible
blank gap because the sticky header is already in flow pushing content down.
The pt-24 adds 96px of empty space BELOW the header's own height.

## scroll-world Pipeline Architecture

Three implementation tiers for the 3D camera flythrough:

| Tier | Technology | Cost | Visual Quality |
|------|-----------|------|---------------|
| Free | CSS 3D transforms (no deps) | $0 | Abstract geometric |
| Low | ComfyUI + Seedance 2.0 node | ~$0.50/site (electricity) | Real AI dioramas |
| Production | Higgsfield AI full pipeline | ~$14-22/site | Original scroll-world |

Full cost breakdown: `docs/scroll-world-cost-breakdown.md` (in website-landlord repo)

## Applying to Sites

These patterns are pre-built into the Astro template system:
- scroll-world/Page.astro — full 3D camera flythrough template
- Layout.astro — pill-nav, fade-in-up, glass-nav CSS utilities
- Each template's hero section uses the scroll-driven reveal

The variant engine (variants.py) seeds scroll-world as the PRIMARY template
choice for all niches. ~25% of new sites will use it automatically.
