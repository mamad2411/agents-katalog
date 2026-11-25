---
name: presstronic-academy-design-system
description: Design system for Presstronic Academy — a branching, story-driven learning platform. Muted cyberpunk: graphite blacks, signal cyan, reserve volt yellow. Square corners, one notched-corner signature motif, Archivo + IBM Plex Mono, shadcn/ui CSS-variable contract with dark default + light mode. Use when designing or building any Presstronic Academy screen or component.
---

# Presstronic Academy Design System

Read `readme.md` first — it holds the full art direction, content voice, and
visual rules. This file is the working recipe.

## Non-negotiables

1. **Square corners. Radius 0 on everything.** No pills, no rounded cards.
2. The only corner treatment allowed is the **signature notch**
   (`clip-path: var(--notch)`, 12px top-right) — on at most ONE element class
   per screen (the primary CTA, the hero card, or the active dialog).
3. **Primary accent: signal cyan** (`--cyan-500 #22c3d6`). **Volt yellow**
   (`--volt-500 #d4b52e`) is reserved for story decisions and caution only.
   **Synth magenta** (`--mag-500 #cf3f9a`) is a third, thinner signal — REC/LIVE
   indicators, code keywords, HUD corner accents, one gradient word per hero
   (`.ink-signal`). Red = destructive, green = success. Never invent hues, and
   never use magenta as the dominant color of a surface.
   No language glyphs/katakana or other decorative script — use `.sig-dash`
   (small cyan/magenta rule) instead.
4. **Dark is default.** `:root` is the dark theme; light mode is
   `[data-theme='light']` or `.light` on an ancestor.
5. Type: **Archivo** (display 700/800 at `-0.025em`; body 400–600, 15px base).
   **IBM Plex Mono** for all labels, data, numbers, and code.
6. Mono labels are UPPERCASE with `0.1–0.12em` tracking; eyebrows are prefixed
   `// LIKE THIS`. Sentence case everywhere else. **No emoji.**
7. Selection/active state = **2px left edge** (cyan for nav/selection, volt for
   story choices) + matching tint background. Hover = stronger border +
   one-step lighter fill. Nothing lifts or scales on hover.
8. Backgrounds are flat graphite. Only permitted decoration: the faint 48px
   grid + single cyan radial glow (see `.grid-bg` / `.hero-glow` in
   `ui_kits/academy/academy.css`) on hero/auth surfaces.
9. Icons: Lucide 0.460.0, outline, `currentColor`. No hand-drawn SVGs.
10. Motion: 120–320ms, `--ease-out`, color/border changes only. Story narration
    may type on. Respect `prefers-reduced-motion`.

## Files

- `styles.css` — import this one file; it pulls all tokens.
- `tokens/colors.css` — ramps + **shadcn/ui variable contract**
  (`--background`, `--primary`, `--ring`, …), dark `:root` + light override.
- `tokens/typography.css`, `tokens/spacing.css` (notch, glows, motion, z-index),
  `tokens/fonts.css` (Google Fonts; swap for licensed binaries later).
- `components/` — reference implementations (`.jsx` + `.d.ts` + `.prompt.md`):
  Button, Badge, Card, Tabs, Progress · Input, Select, Checkbox, Switch ·
  Dialog, Tooltip. Runtime bundle: `_ds_bundle.js` →
  `window.PresstronicAcademyDS`.
- `ui_kits/academy/` — the full click-through app (`index.html`): landing →
  auth → dashboard → story (flagship) → challenge → progression → profile.
  `academy.css` holds screen-level patterns (app shell, choice rows, branch
  map nodes, code pane). `data.jsx` holds demo content and copy tone examples.

## Using in the repo (shadcn/ui port)

1. Copy `tokens/*.css` into `apps/frontend/src/styles/` and import from the
   global stylesheet. The variables already match shadcn's contract; set
   `--radius: 0` (already in tokens).
2. `components.json`: `"cssVariables": true`. Theme toggling flips
   `data-theme` on `<html>`.
3. When generating shadcn components, restyle to match `components/*.jsx`
   exactly: mono uppercase button labels, square checkbox/switch, 2px-edge
   tabs, inset input wells with cyan focus ring.
4. Screen layouts, spacing, and copy voice: mirror `ui_kits/academy/`.

## Copy voice (quick reference)

Narrative SaaS — a mission briefing, not a classroom. Learner = "operative".
Vocabulary: paths, branches, objectives, checkpoints, clearance, mission log.
One flavor word per surface. Numbers always mono. No exclamation marks in
chrome. Examples live in `ui_kits/academy/data.jsx`.
