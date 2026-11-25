---
name: icon-system-skill
description: >-
  Icon library selection, sizing system, optical alignment, stroke vs fill decisions,
  color inheritance, icon weight matching to typography, and animated icon patterns
  for UI and branding. Use when choosing an icon set, sizing icons in a layout,
  matching icons to a font, adding icon animation, or deciding between stroke and
  fill icon styles. Works alongside color-combo-skill, design-effects-skill, and
  font-pairing-skill. Activate on: "what icon library", "icon size", "icon weight",
  "icon animation", "icon system", "stroke icons", "fill icons", "/icon-system-skill".
trigger_keywords:
  - icon
  - icon library
  - icon set
  - icon size
  - icon weight
  - icon animation
  - stroke icon
  - fill icon
  - Lucide
  - Phosphor
  - Heroicons
  - Radix Icons
  - SVG icon
  - animated icon
  - /icon-system-skill
author: bilioveloso
version: "1.1"
---

# Icon System Skill

## Purpose
This skill teaches an agent to make deliberate, system-level icon decisions — from choosing a library to sizing, weighting, coloring, and animating icons consistently. For any project requiring an icon system, the agent should:

1. Identify the brand tier, UI density, and typeface in use.
2. Check the Archetype Recipes section first — if it matches, use that stack directly.
3. Use the Library Guide and Sizing System to customize if needed.
4. Cross-reference [font-pairing-skill](https://github.com/bilioveloso/font-pairing-skill) to match icon stroke weight to the body typeface weight.
5. Cross-reference [color-combo-skill](https://github.com/bilioveloso/color-combo-skill) to apply icon color from the active palette using `currentColor`.
6. Cross-reference [design-effects-skill](https://github.com/bilioveloso/design-effects-skill) for animated icon patterns (SVG stroke draw, bounce, spin, Lottie).

## Core Rules
- **One library per project.** Never mix Lucide and Phosphor in the same interface. Visual inconsistency destroys system trust.
- **Icons inherit color — always use `currentColor`.** Never hardcode a hex into an SVG icon used in UI.
- **Icon weight must match type weight.** Light body font → light/regular icons. Bold display font does not dictate icon weight — the body does.
- **Size icons optically, not mathematically.** A 20px icon next to 16px text will feel heavy. A 18px icon next to 16px text feels right.
- **Stroke icons for UI, fill icons for emphasis or solid state.** Mixing both in the same context requires a clear rule.
- **Never use icons as decoration without semantic meaning.** Icons that add no information should be removed.
- **Animated icons are for state change and delight — not constant loops.** A spinning icon that never stops becomes visual noise.

---

## Icon Library Guide

### Lucide
- **Style:** Stroke, consistent 2px stroke width, rounded line caps.
- **Mood:** Clean, neutral, modern, UI-native.
- **Best for:** SaaS dashboards, enterprise tools, developer products, any UI where icons should be invisible as a system.
- **Weight options:** One weight only (2px stroke).
- **React:** `lucide-react` — tree-shakeable.
- **Site:** [lucide.dev](https://lucide.dev)

### Phosphor Icons
- **Style:** Stroke and fill variants, 6 weights (Thin, Light, Regular, Bold, Fill, Duotone).
- **Mood:** Versatile, expressive, can be premium or playful depending on weight.
- **Best for:** Consumer apps, SaaS, portfolios, wellness, any project where icon personality matters.
- **Weight options:** Thin → Light → Regular → Bold → Fill → Duotone.
- **React:** `@phosphor-icons/react` — tree-shakeable.
- **Site:** [phosphoricons.com](https://phosphoricons.com)

### Heroicons
- **Style:** Stroke (outline) and solid (fill) variants, designed for Tailwind CSS.
- **Mood:** Clean, structured, Tailwind-adjacent, trustworthy.
- **Best for:** Tailwind-based projects, corporate UI, internal tools.
- **Weight options:** Outline (1.5px) and Solid.
- **React:** `@heroicons/react` — tree-shakeable.
- **Site:** [heroicons.com](https://heroicons.com)

### Radix Icons
- **Style:** 15px grid, minimal stroke, designed for Radix UI / shadcn contexts.
- **Mood:** Ultra-minimal, developer-adjacent, invisible system.
- **Best for:** shadcn/ui projects, Radix-based design systems, minimal admin UI.
- **Weight options:** One weight only.
- **React:** `@radix-ui/react-icons`.
- **Site:** [radix-ui.com/icons](https://www.radix-ui.com/icons)

### React Icons
- **Style:** Aggregator — includes Feather, Font Awesome, Material, Bootstrap, and more.
- **Mood:** Depends entirely on the sub-library chosen.
- **Best for:** Rapid prototyping, projects that need icons from multiple sets.
- **Warning:** Do not mix sub-libraries in the same project — it defeats visual consistency.
- **React:** `react-icons`.
- **Site:** [react-icons.github.io](https://react-icons.github.io/react-icons/)

### Custom SVG
- **Best for:** Brand icons, logo marks, social icons, highly specific UI moments.
- **Rule:** Always optimize with SVGO before inlining. Never inline raw Illustrator exports.

---

## Library Selection by Archetype

| Archetype | Recommended library | Weight/style |
|---|---|---|
| Premium AI / SaaS | Phosphor or Lucide | Regular (Phosphor) or 2px (Lucide) |
| Gaming / Esports | Phosphor Bold or custom SVG | Bold or Fill — matches aggressive type |
| Wellness / Healthcare | Phosphor Light or Regular | Light or Regular — matches gentle type |
| Developer Tool / OSS | Lucide or Heroicons | 2px stroke or Outline |
| Creative Portfolio / Agency | Minimal or custom only | Never a full library — competes with type |
| Consumer Lifestyle App | Phosphor Regular | Regular or Duotone for playful moments |
| Dark Editorial / Magazine | Minimal — custom or none | Editorial contexts rarely need icon libraries |
| Enterprise Dashboard | Lucide or Heroicons Outline | Consistent 1.5–2px stroke, 16–20px |

---

## Sizing System

Icons must be sized relative to the text they accompany, not set to a fixed global size.

| Context | Icon size | Notes |
|---|---|---|
| Inline with body text (16px) | 16–18px | Never 20px — feels heavy |
| Inline with large text (20–24px) | 20–22px | Match text cap-height optically |
| Navigation item | 20px | Consistent across all nav icons |
| Button with label | 16–18px | Optically even with button label size |
| Icon-only button / action | 20–24px | Larger target, still compact |
| Feature card hero icon | 32–48px | Statement icon — increase stroke weight |
| Empty state / onboarding illustration | 48–64px | Use Duotone (Phosphor) or a Lottie here |
| Touch target minimum | 44×44px (wrapper) | Icon can be 20–24px — wrapper provides the target |

```css
/* Icon sizing token system */
:root {
  --icon-xs:  14px;
  --icon-sm:  16px;
  --icon-md:  20px;  /* default UI icon */
  --icon-lg:  24px;
  --icon-xl:  32px;
  --icon-2xl: 48px;
}

.icon {
  width: var(--icon-md);
  height: var(--icon-md);
  flex-shrink: 0; /* prevent squishing in flex rows */
}
```

---

## Stroke vs Fill

| Rule | When to apply |
|---|---|
| **Stroke** as default | All UI icons in resting/inactive state |
| **Fill** for active/selected state | Active nav item, selected tab, toggled-on state |
| **Fill** for emphasis | Hero feature icon, primary CTA icon, brand moment |
| **Duotone** (Phosphor) | Empty states, onboarding, delight moments |
| **Never** mix stroke and fill randomly | Every fill must mean something (active, selected, brand) |

```tsx
// Phosphor — stroke default, fill on active
import { House, HouseFill } from '@phosphor-icons/react'

<NavItem icon={isActive ? <HouseFill /> : <House />} />
```

---

## Color Inheritance

Icons must always use `currentColor`. Never hardcode hex values into icon color in UI contexts.

```css
/* SVG icon — inherits text color automatically */
.icon {
  color: inherit;         /* or set explicitly from palette */
  fill: currentColor;     /* for fill-style icons */
  stroke: currentColor;   /* for stroke-style icons */
}

/* Contextual color from palette — always from color-combo-skill tokens */
.icon-accent  { color: var(--color-accent); }
.icon-muted   { color: var(--color-supporting-1); }
.icon-danger  { color: #D7202D; } /* reserved for error/destructive state only */
.icon-success { color: #1A8A40; } /* reserved for success state only */
```

**Cross-reference:** Source all palette tokens from [color-combo-skill](https://github.com/bilioveloso/color-combo-skill). Never invent colors for icon states — use the active palette's accent, supporting, or error tokens.

---

## Weight Matching to Typography

Icon visual weight must match the body typeface, not the display typeface. The body face is what users read alongside icons.

| Body typeface | Icon weight |
|---|---|
| Inter 400 (thin neutral) | Lucide 2px or Phosphor Regular |
| DM Sans 400 (friendly) | Phosphor Regular |
| Nunito 400 (rounded warm) | Phosphor Regular or Duotone |
| Manrope 400 (geometric) | Lucide or Phosphor Regular |
| Geist 400 (developer) | Lucide or Geist-adjacent minimal |
| Inter 600 (medium UI labels) | Phosphor Bold or Heroicons Solid |

For **bold display contexts** (feature cards, hero sections), you can step up one weight:
- Regular body → Regular icon in body, Bold icon in hero feature card.

---

## Animated Icon Patterns

Animated icons are a motion decision. These patterns live here for reference, but the full code and rules are in [design-effects-skill](https://github.com/bilioveloso/design-effects-skill).

### SVG Stroke Draw (success/confirmation)
```css
.path-draw {
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
  animation: draw 0.8s ease forwards;
}
@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```
**Use for:** Checkmark on form success, circle on step completion, underline on badge.

### Bounce on interaction (spring physics)
```css
@keyframes icon-bounce {
  0%   { transform: scale(1); }
  40%  { transform: scale(0.88); }
  70%  { transform: scale(1.12); }
  85%  { transform: scale(0.96); }
  100% { transform: scale(1); }
}
.icon-bounce:active {
  animation: icon-bounce 0.35s ease;
}
```
**Use for:** Like button, reaction, cart add, playful CTA.

### Spin for loading state
```css
.icon-spin {
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
```
**Use for:** Loading spinner replacement, sync-in-progress indicator. **Never** use on decorative icons.

### Lottie for onboarding and empty states
```tsx
import Lottie from 'lottie-react'
import emptyAnimation from './empty-state.json'

<Lottie animationData={emptyAnimation} loop={true} style={{ width: 120, height: 120 }} />
```
**Use for:** Empty states, onboarding step illustrations, success screens.

---

## Optical Alignment

Icons rarely align perfectly on the mathematical center. Adjust optically.

```css
/* Icon in flex row with text — always vertically center */
.icon-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Nudge icon down by 1px if it reads as floating above text */
.icon-optical {
  position: relative;
  top: 1px;
}

/* Icon-only button — center in padded touch target */
.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px; /* WCAG minimum touch target */
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
  border-radius: 8px;
}
.icon-btn:hover { background: rgba(0, 0, 0, 0.06); }
.icon-btn:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
```

---

## Archetype Recipes

Complete icon stacks per project type. These mirror the Page-Type Recipes in [design-effects-skill](https://github.com/bilioveloso/design-effects-skill) and font recommendations in [font-pairing-skill](https://github.com/bilioveloso/font-pairing-skill).

### Recipe 1 — Premium AI / SaaS
- **Library:** Phosphor (Regular) or Lucide
- **Size:** 20px nav and labels, 32px feature cards
- **Style:** Stroke default, Fill for active states
- **Animation:** SVG stroke draw on success states
- **Color source:** Accent token from Otherworldly or Dreamy Periwinkle palette
- **Body font pair:** Inter — 2px Lucide or Phosphor Regular matches Inter 400

### Recipe 2 — Gaming / Esports
- **Library:** Phosphor Bold or custom SVG
- **Size:** 24px nav, 40–48px hero feature
- **Style:** Fill for primary, Stroke Bold for secondary
- **Animation:** Bounce on kill/achievement interaction, Lottie for rank-up
- **Color source:** Accent token from Midnight Frag, Ember Clan, or Toxic Ranked
- **Body font pair:** Inter 400 → Phosphor Regular for body; Phosphor Bold for hero only

### Recipe 3 — Wellness / Healthcare
- **Library:** Phosphor Light or Regular
- **Size:** 18px inline, 24px nav, 48px empty states
- **Style:** Stroke only — no Fill except Lottie moments
- **Animation:** SVG stroke draw on form success; Lottie for empty states (calm loop)
- **Color source:** Soft Gradients, Healthcare, or Nature / Organic palette tokens
- **Body font pair:** DM Sans 400 → Phosphor Light matches the calm, open type

### Recipe 4 — Developer Tool / Open Source
- **Library:** Lucide or Heroicons Outline
- **Size:** 16px inline code, 20px UI, 24px feature
- **Style:** Stroke only — consistent 1.5–2px
- **Animation:** SVG stroke draw on copy-to-clipboard, spin on sync
- **Color source:** Acid Contemporary or Minimalist palette tokens
- **Body font pair:** Geist or Inter — Lucide matches both perfectly

### Recipe 5 — Creative Portfolio / Agency
- **Library:** None, or custom SVG only
- **Size:** Fluid — icons should feel designed, not systemic
- **Style:** Minimal — icons compete with expressive type
- **Animation:** Custom SVG animation only — never generic spin/bounce
- **Color source:** Whichever palette is committed — one accent only
- **Body font pair:** Clash Display / Syne — no icon library needed; type carries the personality

### Recipe 6 — Consumer Lifestyle App
- **Library:** Phosphor Regular or Duotone
- **Size:** 20px nav, 24px feature cards, 48px empty states
- **Style:** Regular default, Duotone for onboarding and empty state delight
- **Animation:** Bounce on like/save/reaction; Lottie for onboarding steps
- **Color source:** Warm Tropical / Resort or Soft Gradients palette tokens
- **Body font pair:** Nunito 400 → Phosphor Regular matches the rounded warmth

### Recipe 7 — Dark Editorial / Magazine
- **Library:** Minimal or none
- **Size:** 16–20px only if navigation requires it
- **Style:** Stroke only — fill competes with editorial photography
- **Animation:** None for standard UI; custom SVG stroke for special branded moments
- **Color source:** Gothic / Dark Romance or Luxury palette tokens
- **Body font pair:** Lora / Source Serif 4 — editorial type needs no icon distraction

### Recipe 8 — Enterprise Dashboard / B2B SaaS
- **Library:** Lucide or Heroicons Outline
- **Size:** 16px data rows, 20px nav and labels, 24px section headings
- **Style:** Stroke only, consistent 1.5–2px across all contexts
- **Animation:** SVG stroke draw on save/confirm; spin on sync loading
- **Color source:** Corporate / Enterprise palette tokens (Steel Authority, Slate Trust)
- **Body font pair:** Inter 400 / Manrope 400 → Lucide 2px is the natural pair

---

## Accessibility

- **Decorative icons:** `aria-hidden="true"` — always.
- **Semantic icons:** `role="img"` + `aria-label` or an adjacent visually-hidden label.
- **Icon-only buttons:** Must have `aria-label` on the `<button>` element.
- **Touch targets:** Never smaller than 44×44px wrapper, regardless of visual icon size.
- **Color alone:** Never use color as the only differentiator between icon states — pair with shape or weight change.

```tsx
// Decorative — hidden from screen readers
<CheckIcon aria-hidden="true" />

// Semantic — icon carries meaning
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>
```

---

## Skill Network

This skill is part of a four-skill design system. Each skill cross-references the others:

| Skill | What it covers | Repo |
|---|---|---|
| **color-combo-skill** | Named palettes, contrast tiers, CSS usage | [github.com/bilioveloso/color-combo-skill](https://github.com/bilioveloso/color-combo-skill) |
| **design-effects-skill** | Animations, morphisms, motion patterns, page recipes | [github.com/bilioveloso/design-effects-skill](https://github.com/bilioveloso/design-effects-skill) |
| **font-pairing-skill** | Typeface selection, pairing rules, type scale | [github.com/bilioveloso/font-pairing-skill](https://github.com/bilioveloso/font-pairing-skill) |
| **icon-system-skill** | Icon library selection, sizing, weight, animated icons | *This skill* |

> **Need pre-built UI components?** [React Bits](https://www.reactbits.dev/get-started/index) has ready-to-use animated and interactive components that pair well with these icon systems. Install only the specific component you need and credit the source when adapting their work.
