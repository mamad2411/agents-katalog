---
name: surfaces
description: "Use when defining the visual plane: elevation, shadow recipes, borders versus hairlines, corner radii, blur and translucency, and background layering."
---


# The Visual Plane

Every boundary between two surfaces gets exactly one separation device: a hairline, a shadow, or a step in background lightness. Never two. Default to the hairline — it is the cheapest, it survives every background behind it, and it is what most "flat" UI actually needed. Promote to a shadow only when the element is meant to read as lifted and has to travel across mixed or image backgrounds. Promote to translucency only when content genuinely passes underneath. Interfaces that look cheap are rarely under-decorated; they are decorated twice, with a border and a shadow and a background tint all arguing the same point.

This skill owns the elevation ladder *within one theme*. Expressing that ladder as lightness when shadows stop reading against dark backgrounds belongs to `dark-mode`, which never picks a shadow recipe; this skill never derives a second theme. The choice between a border and a hairline is here; the hairline's exact grey and its device-pixel rendering are `ui-polish`'s.

**Read the project's depth system before adding to it.** Find where shadows and radii already live — a Tailwind `@theme` block, `:root` custom properties, a generated token file, a styled-components theme object — and add a step to that ladder rather than writing a one-off `box-shadow` at the call site. A codebase with four hand-written shadows has no elevation system; a codebase with four named tokens does. Never introduce a second mechanism to fix one card.

## Quick Reference

| You need | Open |
|---|---|
| The exact token values for a tier, or which tier a component gets | `references/shadow-recipes.md` — load it whenever you are about to write a literal `box-shadow` or assign elevation to a specific component. |
| Blur, translucency, noise, sheen, and the reduced-transparency fallbacks | `references/materials.md` — load it the moment `backdrop-filter` enters the diff, or when a surface is meant to read as a physical material. |

## Core Principles

1. **One separation device per boundary.** A card with a `1px` border *and* a drop shadow *and* a lighter background states the same thing three times, and the three disagree at every zoom level. Pick one and delete the others. The single exception is a translucent surface, where the blur and the `1px` top-edge sheen are one material, not two devices.

2. **Three background planes, maximum.** Base, raised, overlay — that is the whole set, and a fourth tint means you needed elevation rather than another background. Keep the steps to one rung of the grey ramp apart, enough to read as separate and not enough to read as a different component: `--surface-base`, `--surface-raised`, `--surface-overlay`, with the naming convention itself left to `design-tokens`. The exception is a deliberately full-bleed marketing band, which is a section break rather than a plane and sits outside the set.

3. **Derive nested radii, never copy them.** `innerRadius = outerRadius − padding`. A rounded child repeating its parent's radius pinches the corner gap, and that pinch is the single most frequent giveaway of unpolished UI. A `16px` container with `6px` of padding gets a `10px` child. The exception is a gap wider than `24px`: at that distance the surfaces read as independent, the derivation stops describing anything the eye can see, and each radius is chosen on its own merits.

4. **A shadow lifts, a border separates.** Anything meant to read as raised — cards, menus, popovers, dialogs, anything crossing an image — gets the translucent shadow stack, because transparency composites with whatever sits underneath and one token then works everywhere. Anything doing layout work — row dividers, table gridlines, sticky-header rules — keeps a real line. The exception is form fields, where a visible edge is an accessibility feature and converting it to a shadow costs more than it buys.

5. **The elevation ladder is named and closed.** Four steps: `flat / soft / regular / strong` — Benji Taylor's depth ladder from `/drawesome`, where one prop drives shadow, face light, and top-edge sheen together, so a surface cannot be half-raised. `flat` is hairline-only and is the default for content; `regular` is the base three-layer stack `0 0 0 1px rgb(0 0 0 / 0.05), 0 1px 3px rgb(0 0 0 / 0.05), 0 4px 10px -4px rgb(0 0 0 / 0.05)`. Components pick a rung, never a literal. The exception is a full-bleed background section, which sits outside the ladder entirely.

6. **Translucency must have something moving under it.** `backdrop-filter` repaints its whole backdrop on every scroll frame, so it earns that cost only on chrome that content scrolls beneath — a floating toolbar, a sticky header, a sheet over a list. A static panel that never has anything behind it gets an opaque fill. Two hard rules follow: never stack one light translucent surface on another, and never put brand colour on the translucent layer — put it on a solid one behind. The exception is `prefers-reduced-transparency: reduce`, where you raise the background opacity and drop the blur outright.

7. **Skeuomorphic material earns its keep only when the metaphor carries information.** "Pens in a tray beat a row of icons" — Benji Taylor, `/drawesome`, crediting Craft's tray system as the precedent. A tray tells you the tools are a set, that one is currently held, and roughly what each will do before you touch it; a row of identical glyphs tells you none of that. The exception, and it is most cases: if the real-world object has no affordance your users need, the material is decoration and costs a repaint, an asset, and a dark-mode variant for nothing.

## Smell / Fix

| Smell | Fix |
|---|---|
| Corner gap pinches where a rounded child meets its parent | Derive the child radius: outer minus padding |
| Card looks stamped onto the page instead of raised | Solid depth border; swap in the shadow token |
| Cards vanish in dark mode | Light stack still active — collapse to `0 0 0 1px rgb(255 255 255 / 0.09)`, then hand the theme to `dark-mode` |
| Shadow hover feels laggy or heavy | Element transitions `all`; scope to `box-shadow` at `150ms ease-out` |
| Four different `box-shadow` literals across the codebase | No ladder — define `flat / soft / regular / strong` and replace every literal |
| Visible stripes across a large gradient | Banding — use an eased multi-stop gradient, see `references/materials.md` |
| Blurred toolbar over an area nothing scrolls under | Translucency with no payoff; make it opaque |
| Text on glass reads muddy | Vibrancy problem — raise contrast and weight, move colour to a solid layer |
| Two translucent layers stacked | Legibility collapse; make the lower one opaque |

## Output Format

Emit the ladder as tokens, then reference them — never inline a stack at a call site:

```css
:root {
  --elevation-flat: none;
  --elevation-regular:
    0 0 0 1px rgb(0 0 0 / 0.05),
    0 1px 3px rgb(0 0 0 / 0.05),
    0 4px 10px -4px rgb(0 0 0 / 0.05);
  --elevation-regular-hover:
    0 0 0 1px rgb(0 0 0 / 0.07),
    0 1px 3px rgb(0 0 0 / 0.07),
    0 4px 10px -4px rgb(0 0 0 / 0.08);
}

.panel {
  box-shadow: var(--elevation-regular);
  transition: box-shadow 150ms ease-out;
}
.panel:hover { box-shadow: var(--elevation-regular-hover); }
```

When proposing a change, name the rung and the reason: "`soft`, because it sits on the base plane and never crosses an image" — not "add a subtle shadow."

## Checklist

- [ ] Exactly one separation device on every boundary — no border plus shadow plus tint
- [ ] No more than three background planes in the whole theme
- [ ] Every nested radius derived (outer − padding) where the gap is under `24px`
- [ ] Raised elements use shadow tokens; dividers, gridlines, and field edges keep real borders
- [ ] Every `box-shadow` in the diff is a token from the four-rung ladder, not a literal
- [ ] Shadow transitions are scoped to `box-shadow`, `150ms ease-out`, and nothing else
- [ ] Every translucent surface has content that actually passes beneath it
- [ ] No translucent surface stacked on another; no brand colour on a translucent layer
- [ ] `prefers-reduced-transparency` and `prefers-contrast` fallbacks present wherever blur is used
- [ ] Any skeuomorphic material can be defended by naming the information the metaphor carries
