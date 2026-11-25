---
name: canon-depth
description: Use when designing or auditing shadows, elevation, layering, z-index, borders, dividers, or any visual depth in an interface. Covers shadow construction, elevation systems, when to use shadows vs borders, and the most common depth anti-patterns. Trigger when the user mentions shadow, elevation, depth, layer, z-index, border, divider, or visual hierarchy via depth.
---

# CANON · Depth and Elevation

Depth communicates layering and importance. Most AI-generated UIs either flatten everything (no hierarchy) or shadow everything (visual noise). The rules below produce restrained, intentional depth.

## Quantified Rules

### Shadow Construction

A real shadow has multiple layers. Single-shadow elements look CSS-generated.

```css
/* Wrong: flat, single-layer */
.card { box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }

/* Right: layered, soft */
.card {
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 4px 8px rgba(0, 0, 0, 0.06),
    0 16px 32px rgba(0, 0, 0, 0.08);
}
```

| Layer | Purpose |
|---|---|
| Tight (0 1px 2px) | Defines edge contact |
| Medium (0 4px 8px) | Hints at lift |
| Wide (0 16px 32px) | Carries the perceived height |

**Shadow color is never pure black.** Use a tinted color from the same hue as your primary, with very low opacity.

### Elevation Tokens

```css
:root {
  --elevation-0: none;
  --elevation-1:
    0 1px 2px rgba(0, 0, 0, 0.04);
  --elevation-2:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.04);
  --elevation-3:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 4px 8px rgba(0, 0, 0, 0.06),
    0 8px 16px rgba(0, 0, 0, 0.04);
  --elevation-4:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 4px 8px rgba(0, 0, 0, 0.06),
    0 16px 32px rgba(0, 0, 0, 0.08);
  --elevation-5:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 4px 8px rgba(0, 0, 0, 0.06),
    0 16px 32px rgba(0, 0, 0, 0.08),
    0 32px 64px rgba(0, 0, 0, 0.10);
}
```

| Elevation | Use case |
|---|---|
| 0 | Page background, flush content |
| 1 | Resting card, input |
| 2 | Hovered card |
| 3 | Dropdown, popover |
| 4 | Modal |
| 5 | Notification, toast (above modal) |

**Maximum 5 elevation levels.** More than that is noise.

### Z-Index Scale

```css
:root {
  --z-base:        0;
  --z-dropdown:    100;
  --z-sticky:      200;
  --z-fixed:       300;
  --z-modal-bg:    400;
  --z-modal:       410;
  --z-popover:     500;
  --z-tooltip:     600;
  --z-toast:       700;
  --z-notification: 800;
}
```

**Rule: never use raw z-index values in components.** Always reference the scale. Random `z-index: 99999` is the universal sign of an unmanaged stack.

### Borders vs Shadows for Separation

| Situation | Use |
|---|---|
| Containers on a colored or off-white surface | Border (or no separation, just whitespace) |
| Containers on a pure white page | Border, very subtle shadow, or whitespace |
| Cards lifted above the page | Shadow |
| Modal above content | Shadow + dimmer overlay |
| Popover anchored to element | Shadow + small arrow |
| Sticky header | Bottom border, shadow on scroll |
| Inputs | Border (focus = border + ring) |
| Dividers between list items | Border |

**Default: prefer whitespace over a border. Prefer a border over a shadow.** Add depth only when the layering is meaningful.

### Border Specs

| Context | Width | Color |
|---|---|---|
| Card border | 1px | `--color-border` (8% L darker than surface) |
| Input border (default) | 1px | `--color-border` |
| Input border (focused) | 1–2px + 2px ring | `--color-accent` |
| Input border (error) | 1–2px | `--color-error` |
| Section divider | 1px | `--color-border` |
| Heavy emphasis (rare) | 2px | `--color-accent` or `--color-text` |

**Never use `border: 1px solid black`.** Pure black borders are too heavy. Use a tinted neutral.

### Border Radius

| Element | Radius | Source |
|---|---|---|
| Tags, pills, status badges | 999px (full pill) | Common practice |
| Avatar (circular) | 50% | |
| Inputs | 4–8px | Material 3 (4px), HIG (10–12px) |
| Buttons | 4–10px (match inputs) | |
| Cards | 8–16px | Material 3 (12px) |
| Modals | 12–24px | |
| Image thumbnails | 4–8px | |
| Hard / brutalist | 0px | Intentional choice |

**Rule: pick a radius scale and stick to it.** 4 / 8 / 12 / 16 is a clean four-step scale. Don't use 7px next to 11px.

### Radius Consistency

Inputs and buttons in the same form should share radius. Cards and modals can use a larger radius. Avatars are full-round. Pills are full-round. That's it.

## Layering Rules

### Single Source of Elevation

Each layer of the UI has one elevation. Don't elevate elements within an elevated container — that's russian doll.

| Layer | Has elevation |
|---|---|
| Page (background) | 0 |
| Cards on page | 1 |
| Things inside cards | 0 (use border or whitespace, not shadow) |
| Modal | 4 |
| Buttons inside modal | 0 (just color, no shadow) |

### Modal Overlay

Modals need a dimmer behind them:

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);  /* optional, modern browsers */
}
```

| Property | Value |
|---|---|
| Backdrop opacity | 30–50% |
| Backdrop color | Black tinted, not pure |
| Blur (optional) | 4–12px |

Backdrop separates modal from page; modal shadow lifts modal off backdrop.

### Hover Elevation Change

Cards and buttons can rise on hover:

```css
.card {
  box-shadow: var(--elevation-1);
  transition: box-shadow 200ms var(--ease-out), transform 200ms var(--ease-out);
}
.card:hover {
  box-shadow: var(--elevation-2);
  transform: translateY(-2px);
}
```

**Subtle is the goal.** A 2px lift + one elevation step = enough. Lifting cards 8px and adding glow looks tacky.

## Dark Mode Depth

Light mode uses shadows for elevation. Dark mode primarily uses **surface lightness**:

| Layer | Light mode | Dark mode |
|---|---|---|
| Page bg | white (100% L) | 15% L |
| Card | white + shadow | 20% L (no shadow needed) |
| Modal | white + larger shadow | 24% L + subtle shadow |
| Popover | white + shadow | 28% L + subtle shadow |

**In dark mode, shadows are weaker.** Surfaces get lighter to convey elevation. Some shadow can still help separate from the dimmer beneath.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Single-layer shadow `0 4px 8px black` | Flat, harsh | Multi-layer with low opacity |
| Pure black shadow color | Too saturated | Tinted with primary hue |
| `box-shadow: 0 0 20px purple` | Glow effect, dated/AI-slop | Use proper elevation |
| Nested shadows (card in card with shadow) | Visual noise | Inner uses border or whitespace |
| `z-index: 99999` | Unmanaged stack | Use z-index scale |
| Random radius (3px, 7px, 11px) | No system | Pick a 3–4 step scale |
| Pill-shaped buttons next to square cards | Inconsistent | Match radius family |
| Pure black 1px border on white | Too heavy | Tinted, low contrast |
| Border AND shadow on same element | Belt and suspenders | Pick one |
| Border on every section | Visual clutter | Use whitespace |
| Modal without backdrop | No focus | Add semi-transparent backdrop |
| Shadow on dark mode card | Doesn't work, looks muddy | Use lighter surface instead |
| Tilted shadow (e.g., `-4px 0 8px`) | Wrong light direction | Light from top, shadow below |
| Inset shadow imitating physical engraving | Skeuomorphic, dated | Use border + lower elevation |

## Decision Tree

```
Need to separate two areas?
├─ Try whitespace first
├─ Whitespace not enough? Try a border.
├─ Border not enough? Add subtle shadow (elevation-1).
├─ Element should appear lifted? Use elevation-2 or higher.
├─ Element is overlay (modal, popover)? Use elevation-3+ AND backdrop.
└─ Inside dark mode? Lighten surface instead of shadowing.
```

## Audit Checklist

1. Count distinct elevation values. More than 5? Consolidate.
2. Search for `z-index: \d+`. Each one a token reference?
3. Search for `box-shadow:`. Single-layer? Pure black? Replace.
4. Check border colors. Any `#000` or pure black? Replace with tinted.
5. Count distinct border radii. More than 4? Consolidate.
6. Check radius consistency. Same family in inputs/buttons? Cards/modals?
7. Check nested shadows. Cards inside cards both shadowed? Flatten.
8. Check modals have backdrop. Backdrop opacity 30–50%?
9. Check dark mode. Surfaces lighten with elevation? Shadows reduced?
10. Check glow effects. Any `box-shadow: 0 0 X color`? Likely AI-slop, replace.

## Citations

- Material Design 3 Elevation: https://m3.material.io/styles/elevation/overview
- Apple HIG Materials: https://developer.apple.com/design/human-interface-guidelines/materials
- Refactoring UI, Chapter 9 (Depth)
- Tailwind Shadow Scale: https://tailwindcss.com/docs/box-shadow
- Smooth Shadow Generator (proper layering): https://shadows.brumm.af
