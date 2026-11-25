---
name: recording-studio-brutalist
description: Brutalist, Swiss-print or terminal direction for Recording Studio host themes. Use when a host wants raw grids, extreme type contrast, and utilitarian color. Execution is a named Flatpack theme with ViewComponents and tokens, not custom CSS.
---

# Recording Studio brutalist

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/brutalist-skill` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

This is a direction pack. Critique: `recording-studio-taste`. Audit: `recording-studio-redesign`. Completeness: `recording-studio-output`. Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack`. Other packs: `recording-studio-soft`, `recording-studio-minimalist`. Brand: `recording-studio-brandkit`.

## When to use

- A host surface should feel like a declassified blueprint, Swiss industrial print, or a tactical terminal
- The brief says brutalist, raw, mechanical, telemetry, or "make it harsh"
- Brutalist is opted in. Dummy, gem, and Admin stay rounded unless this chat says otherwise

Do not spray scanlines, CRT overlays, or custom dither CSS onto kit screens. If analog grain is required, it is a Flatpack theme token.

## Pick one archetype

Commit to one. Do not mix light newsprint and CRT terminal on the same surface.

### Swiss industrial print

Newsprint or off-white substrate (`#F4F4F0` / `#EAE8E3` as theme canvas). Carbon ink text. One hazard-red accent for rules and vital highlights. Heavy grotesk at huge scale, tight tracking, compressed leading, uppercase for structural titles. Visible grid lines. Asymmetric voids next to oversized numerals.

### Tactical telemetry

Dark CRT (`#0A0A0A` / `#121212`, not pure `#000`). Phosphor-like off-white text. Same hazard red, same "only one accent" rule. Optional terminal green on a single status token, never as body text. Mono for metadata, IDs, and numbers. High density tables through Flatpack table components.

## Type

Type is structure.

- Macro: heavy sans at fluid scale, tracking `-0.03em` to `-0.06em`, leading under 1, uppercase
- Micro: mono, 10-14px feel, wider tracking, uppercase metadata
- Serif: rare, and only if the theme degrades or contrasts it on purpose

Inter Extra Bold is acceptable here when the theme chooses it as the industrial face. That exception does not leak into Soft or dummy rounded.

## Color and geometry

No gradients, no soft drop shadows, no glass. Corners are 90 degrees (radius token `0`). Borders are solid 1-2px rules. Layout is CSS grid through Flatpack, elements anchored to tracks, not floating cards.

Bimodal density: tight mono clusters next to large empty zones that frame the display type.

## Components

Utilitarian, not consumer chrome.

- ASCII framing and registration marks only when they are theme-provided ornaments or real metadata, not decoration spam on every row
- Crosshairs, barcodes, and `REV 2.6` stamps are easy AI tells. Use at most one structural motif, or skip them
- Data uses semantic Flatpack: tables, definition lists, `kbd` / status tokens
- Buttons are rectangular, high contrast, one accent for the true primary

## What would look better

Four-part Taste critique is required. Useful notes:

- "The title would look better if it used the theme's fluid display clamp and negative tracking, not the kit section title."
- "The groups would look better if they sat on a 1px grid token, not rounded cards."
- "The accent would look better if hazard red were only on the primary rule and the live status, not on every link."

## Execution

1. Declare the design read and the archetype (print or telemetry).
2. Add or use a named theme. Map paper/CRT, ink, hazard red, radius 0, and type ramps to Flatpack tokens.
3. Compose Flatpack. Do not hand-roll scanline overlays or SVG dither.
4. Leave dummy / gem / Admin on rounded unless opted in.

Motion stays low. Brutalism is still, then sharp. Flatpack press states only.
