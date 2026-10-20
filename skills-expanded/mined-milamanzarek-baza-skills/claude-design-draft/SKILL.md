---
name: kamilla-gafurzianova-design
description: Use this skill to generate well-branded interfaces and assets for Kamilla Gafurzianova (AI Implementation Consultant & Olympic Silver Medalist), for production or throwaway prototypes/mocks. Contains the neural design language, colors, type, fonts, the signature neural-field canvas, the PPPP framework, assets, and UI kit components.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

Key files:
- `README.md` — brand context, the PPPP framework, content fundamentals, visual foundations, iconography, manifest.
- `colors_and_type.css` — themes + type/spacing/radius/depth tokens. Import it and set a theme
  class (default `theme-neural`).
- `assets/neural-field.js` — the signature brand motif: a live, on-brand neural-network canvas
  (nodes + firing synapses + one warm-peach ignition node). Drop a `<canvas class="neural-field">`
  behind heroes/sections and include the script.
- `assets/README.md` — brand-mark notes + asset URLs.
- `preview/` — specimen cards for every foundation + component.
- `ui_kits/` — `_shared.css` component classes + two surfaces (`portfolio-site/`, `pppp-framework/`).
  Copy components from here as starting points.

Core rules to honor (Kamilla's hard NO's):
- **No pill shapes.** Rounded corners OK; fully-round capsules banned. There is no `--radius-pill`.
- **No flat / dull surfaces.** Depth is mandatory — glow, glass, layered shadow, luminance.
- **No low contrast.** Accessibility first; text/surface pairs hit WCAG AA (4.5:1)+.

More rules:
- **Default to the Neural (dark) theme.** Document (light) is for long-form reading; Print is for PDF.
- **Type:** Space Grotesk headings/wordmark/numbers, Source Sans 3 body, JetBrains Mono labels/data/code.
- **Color:** deep purple void; pale-pink ink; orchid-magenta + lilac + muted-violet accent
  family; one rare warm-peach ignition node per composition.
- **Voice:** first-person, integrative, disciplined (Olympic rigor → AI implementation). Uppercase
  mono kickers/labels; sentence-case headings; left-aligned body. No emoji.
- **PPPP:** Past · Present · Possible · Practice, bound by a hidden 5th P (Protocol/Process). Render
  as connected nodes / `.pbadge--*` badges; Protocol is the warm-peach synapse layer.
- **Icons:** Lucide (pin `lucide@0.288.0`). Brand mark = neural node-cluster glyph (circles + lines).

If creating visual artifacts (slides, mocks, throwaway prototypes), copy assets out and create
static HTML files for the user to view. If working on production code, copy assets and read the
rules here to become an expert in designing with this brand.

If the user invokes this skill without other guidance, ask what they want to build, ask a few
questions, and act as an expert designer who outputs HTML artifacts _or_ production code.
