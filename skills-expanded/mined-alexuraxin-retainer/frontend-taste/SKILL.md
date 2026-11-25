---
name: frontend-taste
description: "Call BEFORE the first line of markup when creating or redesigning any HTML interface, page, report or layout. Trigger words (RU+EN): макет, набросаем, вёрстка, страница, экран, дизайн, редизайн, CSS, шаблон, лендинг, отчёт-страница / mockup, layout, page, screen, design, redesign, CSS, template, landing, report page. Audit against generic-AI patterns: typography, font weight, color and surfaces, layout, states. Do not skip because «the change is small» or «I'll take the style from the project» — the observed failure is exactly that. Complements dataviz with a layout pass."
---

# Taste in markup

Turn dull generated output into a considered design. Works with any CSS (Tailwind, vanilla,
styled-components). **Do not rewrite from scratch — improve what exists.** Order: Scan (stack,
styling method) → Diagnose (by the audit below) → Fix (surgically, within the existing stack).

Complements `dataviz` (charts/palette/KPI) with a **layout and typography** layer — they are about
different things and do not conflict.

## Typography

- Default fonts / Inter everywhere → a font with character (Geist, Outfit, Satoshi; for editorial —
  a serif heading + sans body).
- Headings with no weight → larger display, tighter tracking (negative), smaller line-height.
- Too-wide text → ~65 characters per line, more line-height.
- Only 400/700 → add 500/600 for fine hierarchy.
- Numbers in a proportional font → `font-variant-numeric: tabular-nums` for data.
- Orphans (one word on the last line) → `text-wrap: balance`/`pretty`.

## Color and surfaces

- Pure `#000000` background → off-black (`#0a0a0a`, `#121212`, a dark navy).
- Oversaturated accents → saturation < 80%, desaturate. **One** accent, not several.
- A mix of warm and cool grays → one gray family, a single hue.
- The "AI gradient" purple-blue → a neutral base + one considered accent.
- A flat `box-shadow` → tint it to the background, a single light direction.
- Empty flat sections → a background image/pattern/low-opacity ambient gradient.
- A sudden dark section on a light page (or vice versa) → hold a single tone, do not jump to `#111`.

## Layout

- Everything centered/symmetric → break it: offset margins, left alignment, asymmetry.
- Three equal feature columns → a 2-column zigzag, an asymmetric grid, masonry.
- `height: 100vh` → `min-height: 100dvh` (iOS Safari).
- No max-width → a container ~1200–1440px with auto margins.
- The same border-radius on everything → vary it (inner ones tighter).
- Buttons not aligned to the bottom of cards → pin to the bottom (a shared horizontal).
- Feature lists start at different heights → align the baselines.
- Too little air → double the spacing (for marketing; data dashboards are denser).

## States and interaction

- No hover → a background shift/slight scale/translate.
- No active/pressed → `scale(0.98)`/`translateY(1px)`.
- Instant transitions → 200–300ms on interactive elements.
- No focus ring → a visible focus (accessibility, not optional).
- Spinners → skeleton loaders in the shape of the layout.
- An empty state → a composed "getting started", not emptiness.

## Banlist: clichés, placeholders, generic defaults

The audit above is about form; here are concrete bans on content and defaults by which markup reads
as "AI-generated".

**AI clichés in UI text:** Elevate, Seamless, Unleash, Next-Gen, Game-changer, Delve, "supercharge
your workflow", "take it to the next level" → flat concrete language for what the feature REALLY
does. The same "no neuroslop" rule applied to interface copy, not to the answer's prose.

**Filler placeholders:** John Doe / Jane Smith / Acme Corp / Lorem Ipsum / user@example.com / "Your
Company Here" → realistic contextual content for the domain (names, companies, amounts, dates that
could be real). Filler betrays unfinished work.

**Generic defaults (by default — NOT these):**
- Fonts: Inter / Roboto / Open Sans / the system sans → a font with character (see Typography).
- Icons: thin single-line libraries (Lucide, Feather, Heroicons) by default → match the weight and
  tone of the layout, not the first library at hand.
- Shadows: heavy default `shadow-md/lg/xl` → lighten and tint them (see Color and surfaces).
- Emoji in markup / alt / as placeholder icons → a real icon or nothing.
- Effects: gradient / neon / 3D glassmorphism by default → extends the "AI gradient" ban to neon and
  glassmorphism (see Color and surfaces).

## When NOT to apply

Only HTML/UI markup and visual artifacts. Backend/CLI/data/logic — not here (that is
gate/code-reviewer/graph).

Related: [[task-cycle]].
