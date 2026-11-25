---
name: material-color-system
description: >-
  use this when a UI color must be chosen, generated, fixed, or judged: a
  palette, a theme from a brand color or an image, dark mode, a contrast
  failure. Generates the whole system from one source in HCT and measures
  every designed pair.
license: MIT
---

# Material Color System

Use this skill whenever color has to be chosen, generated, fixed, or judged for a UI: a new palette, a theme from a brand color or an image, a UI that "looks off", a contrast failure, dark mode, or a request to balance color in an existing screen. It captures the whole Material color lineage (2014 fixed swatches, 2017 Color Tool, 2021 Material You / dynamic color) as one executable system, not taste advice.

The core promise, in one line: **pick one source color, never a palette. The algorithm builds the palette, and the relationships between colors are guaranteed by tone arithmetic, not by your eye.**

## The pipeline (never skip a stage, never hand-pick downstream)

```
source color -> HCT -> 5+1 key colors -> tonal palettes (13 tones each)
-> color roles (light + dark + contrast levels) -> tokens -> UI elements
```

1. **Source.** One color only. Three legal origins: hand-picked (brand), extracted from an image (wallpaper, photo, logo, product shot), or inherited (an existing UI's dominant accent). If the user gives many colors, treat the first as source and harmonize the rest (see Harmonization).
2. **HCT.** Convert to Hue (CAM16, 0 to 360), Chroma (colorfulness, not HSL saturation), Tone (CIELAB L*, 0 black to 100 white). Tone is perceptual: tone 40 looks equally light in every hue. This is why the system works and HSL/RGB shading does not. Full theory: `references/core-theory.md`.
3. **Key colors.** Primary (source hue, capped chroma per variant), Secondary (same hue, low chroma ~16), Tertiary (hue rotated, ~+60 degrees in tonal-spot), Neutral (same hue, chroma ~4 to 6), Neutral Variant (~8), Error (fixed hue 25, chroma 84, never derived from source).
4. **Tonal palettes.** Each key color held at constant hue and chroma, solved at tones 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100. Where a hue cannot reach its chroma at a tone, the solver returns the most colorful in-gamut color. That fading at the extremes is correct, not a bug.
5. **Roles.** Fixed tone assignments per role, different for light and dark. The table is in `references/roles-and-tokens.md`. Roles are the paint-by-number numbers: UI elements are assigned roles once, and a new source re-skins everything without touching the elements.
6. **Tokens.** Three tiers, never mix them: reference (`primary-40`), system (`--md-sys-color-primary`), component (`button-container`). Components consume system roles only. Raw hex in a component is a defect.

## Run it, do not approximate it

The engine is Google's Material Color Utilities (MCU), bundled in `scripts/`:

```bash
cd ~/workspace/custom-skills/material-color-system/scripts
node color-kit.mjs --source '#6750A4'                    # full kit JSON: palettes, light+dark roles, verified contrast pairs
node color-kit.mjs --source '#6750A4' --format css       # CSS variables, light + [data-theme=dark]
node color-kit.mjs --source '#6750A4' --format tokens    # W3C design tokens JSON
node color-kit.mjs --image photo.jpg                     # Celebi quantization + Score ranking, then a content kit
node color-kit.mjs --source '#B3261E' --variant vibrant --contrast 0.5
```

Rules for the run:

- The script's output is the palette. Never adjust a role hex by eye afterward. If a color looks wrong, change the source, the variant, or the contrast level, then re-run.
- The seed usually does **not** appear verbatim in the scheme: tonal-spot caps primary chroma (a strong red seed yields a calmer primary). That is the system working. When the exact brand color must appear, use `fidelity` or `content` (they place the source in `primaryContainer`), or add the brand color as a harmonized custom color, never as a replacement for `primary`.
- Every kit ships with measured WCAG ratios for its on/container pairs. Report the minimum pair ratio with the kit. Tone arithmetic (delta 40 ~ 3:1, delta 50 ~ 4.5:1) is for placing colors; the measured ratio is for accepting them.

## Choose the variant by intent

| Variant | What it does | Use when |
|---|---|---|
| `tonal-spot` (default) | Calm, chroma-capped, tertiary hue +60 | General product UI, the Android Material You default |
| `content` | Fidelity to the image/source appearance | Kit from a photo, album art, product image |
| `fidelity` | Source kept as-is in primaryContainer | Brand color is non-negotiable |
| `vibrant` | Max chroma at every palette position | Marketing, playful, color-forward surfaces |
| `expressive` | Source hue deliberately absent, playful offsets | Creative tools, kids, entertainment |
| `fruit-salad` | Vibrant with rotated secondary/tertiary | Playful, multi-color feel |
| `rainbow` | Wide hue spread across palettes | Same as above, stronger |
| `neutral` | Near-achromatic, very low chroma | Pro tools, finance, quiet institutional UI |
| `monochrome` | Zero chroma everywhere | E-ink, print-like, extreme restraint |

## Mode A: image to kit

1. Run `color-kit.mjs --image <file>`. It downsamples, runs QuantizerCelebi (Wu-seeded weighted k-means in Lab), then Score: unsuitable colors are filtered (too dark, too light, low chroma), the rest ranked by population proportion, chroma against a target, and hue desirability. Skin-tone and muddy ranges are downweighted by the scorer, not by you.
2. Present the ranked candidates, not just the winner: the top scored color is the algorithmic pick, but a lower candidate is sometimes the brand-right one. Show source candidates + the generated light/dark roles for the pick.
3. Default variant for images is `content`. Offer `tonal-spot` as the calmer alternative when the image is loud.
4. Deliver: kit JSON, CSS, and a one-screen visual swatch (palettes as tone ladders, roles as labeled chips) so the user judges the whole picture at once. Never deliver hex lists alone.

## Mode B: audit and direct an existing UI

Look at the screenshot or live page and diagnose in role terms, in this order. Each finding names the role, the current fault, and the directional fix with exact tones/hexes from a generated kit. No vague advice ("more contrast", "less saturated") without the replacement value.

1. **Surface discipline.** Most of the screen must be neutral palette: `surface`, the five `surfaceContainer` steps (lowest to highest for nesting and elevation, instead of shadows), `onSurface` for body text, `onSurfaceVariant` for secondary text. If chromatic color covers large areas, that is finding #1.
2. **Accent budget.** Primary is for the highest-emphasis actions only (filled button, FAB, active state). Secondary for less prominent fills and selected states. Tertiary sparingly, for the one contrasting accent or badge. A useful check is roughly 60 neutral / 30 secondary-container and surface variation / 10 primary accent by area. Everything screaming primary means nothing is primary.
3. **Pairing integrity.** Every fill must carry its own `on-` color: `primary` with `onPrimary`, `primaryContainer` with `onPrimaryContainer`, and so on. Text in `onSurface` on a `primaryContainer` fill is the classic break. Check every pair's measured ratio: 4.5:1 body text, 3:1 large text and UI components.
4. **One source check.** Sample the UI's chromatic colors. If their hues scatter with no shared source, the UI has no system: propose the dominant accent as source, regenerate, and map each stray color to its nearest role. If hues cluster but tones are random (same hue button darker than its own hover, borders lighter than backgrounds inconsistently), keep the source and fix only the tone assignments.
5. **Dark mode is not an invert.** Dark roles come from the same palettes at dark tones (primary 80, container 30, surface 6, containers stepping 4 to 22). Never ship a dark theme made by flipping light hexes.
6. **States come from the palette.** Hover, pressed, selected, disabled are tone steps and `surfaceContainer` steps of the same palettes (or state-layer opacities of the on-color), never new colors.

Output shape for an audit: findings ranked by visual damage, each with before hex, role, after hex, and the ratio after. Then the regenerated kit for the UI's source. Apply changes only on the user's go, unless the task already authorized the build.

## Harmonization and custom colors

Brand, semantic, or chart colors that must coexist with a scheme get harmonized, not dropped in raw: rotate the custom color's hue toward the source hue by half the difference, capped at 15 degrees, chroma and tone untouched (MCU `Blend.harmonize`). Success, warning, and data-viz colors each get their own tonal palette built the same way (fixed hue/chroma, 13 tones), so their containers and on-colors exist too. Fixed colors that must not move between light and dark use the `*Fixed` roles (primaryFixed, etc.).

## Known traps the old tooling solved, check for each

- **Disliked colors.** Dark yellow-green (roughly hue 90 to 115, low tone, high chroma) reads as bile/sickly to most viewers. MCU `DislikeAnalyzer` detects and fixes it by lightening. Run the check on any yellow-green source.
- **Yellow lies.** Yellow reaches max chroma only at high tones, so a yellow primary at tone 40 is muddy brown-olive. Yellow brands belong at container tones or as tertiary, with dark on-colors.
- **Skin tones as source.** Image scoring downweights them for a reason. A portrait's best theme color is rarely the face.
- **Pure gray neutrals.** Neutral palettes keep a trace of the source hue (chroma 4 to 8). Swapping in #808080-family grays kills the cohesion that makes the scheme feel designed.
- **Elevation by shadow.** On colored surfaces, hierarchy is tonal (surface container steps), not shadow darkness.
- **Contrast levels.** Standard, medium (+), high (7:1 target on essential pairs) are scheme parameters (`--contrast -1..1`), regenerated, not hand-tweaked pairs.

## The modern stack (how this runs in 2026)

Full detail in `references/modern-stack.md`. The short form:

- Generate once in HCT, transport everywhere as **W3C design tokens** (the `--format tokens` output). A color in a component that is not in tokens is a bug. Roles map onto Tailwind v4 `@theme inline` vars or the shadcn/shadcss variable names once, in the theme file, never per component.
- State layers in one line of modern CSS: `color-mix(in srgb, var(--color-on-primary) 8%, var(--color-primary))`, hover 8, focus/pressed 10, dragged 16. Gradients interpolate `in oklch`, never HSL.
- `prefers-contrast: more` swaps in the +0.5/+1.0 contrast kit (generate it, do not approximate it). `forced-colors: active` must lose zero information. P3 wide gamut is an enhancement layer only, never the sole carrier of meaning.
- Verification is a four-check stack, in order: WCAG ratio measured (the gate), APCA Lc as second signal (draft standard, report do not gate), CVD simulation on categorical colors, forced-colors plus dark pass.
- When users can theme (per-community, per-user), ship the generator, not just the palette: one photo or one color in, the whole role system follows, accessibility survives because roles touch text, not raw picks.
- **MCP server is built**: `mcp/server.mjs` (stdio, tools: color_kit_from_source, color_kit_from_image, tonal_palette, harmonize, fix_contrast, audit_palette). Any MCP client can call it; in this agent flow the scripts remain the default path.

## The legacy rule sets (the generators before M3)

Full capture in `references/legacy-rule-sets.md`, executable versions in `scripts/legacy-rules.mjs`. The sets that still govern audits of non-Material UIs:

- **M2 dark theme:** base #121212, white text floor 15.8:1, elevation by white overlay (0% at 0dp to 16% at 24dp, never on primary/secondary surfaces), accents from the 200 to 50 range desaturated, full-saturation brand on at most 1 to 2 small elements, text emphasis 87/60/38%.
- **Android Palette targets:** image colors scored into Vibrant/Muted x Light/Normal/Dark by HSL bands (hard exclusions) with weights luma 0.52, saturation 0.24, population 0.24. A category may return nothing: always plan the fallback chain.
- **State layers:** states are the content color at fixed opacity (M3: hover 8, focus 10, pressed 10, dragged 16; disabled content 38, container 12, no state layer when disabled), never new colors.
- **Emphasis alphas:** black/white text at 87/60/38 and dividers at 12% collapse most accidental gray sprawl.
- **Leonardo's rule:** define colors by target contrast ratio against a named background and solve for them, the contrast-first alternative to tone arithmetic, best for multi-brand and data-viz work.
- **M2 application tests:** hierarchical, legible, expressive, in that order.

## The 2014 layer (use only when asked for classic Material)

The original system was fixed, not generative: 19 hand-built families (Red to Blue Grey), shades 50 to 900 plus accents A100 to A700, 500 as the primary baseline, 700 the darker variant, an accent A200/A400 for secondary actions. The 2017 Color Tool added primary/secondary variant generation and WCAG legibility checks on sample UI. Those swatches are a compatibility palette for legacy Material work, not a starting point for new UI: new work always starts from a source and HCT.

## MCP form

The same operations are specified as an MCP server in `mcp/SPEC.md` (`color_kit_from_source`, `color_kit_from_image`, `audit_palette`, `harmonize`, `fix_contrast`, `tonal_palette`). Build or connect that server when a project needs these calls repeatedly from code or another agent; for one-off work in chat, the bundled script is the same engine and is faster to run.

## Sources

Primary: m3.material.io/styles/color/system/how-the-system-works, /styles/color/roles, Material Color Utilities (github.com/material-foundation/material-color-utilities). Theory: Material's "Science of color design" (HCT/CAM16). Lineage: 2014 Material palette, 2017 Color Tool (developers.googleblog.com, April 6 2017). Full synthesis with the three-pass notes: `references/core-theory.md`.
