---
name: dense-ui-metrics
description: >-
  Mathematical spacing, sizing, weight, line-height, letter-spacing, radius, and
  padding rules for "productive" SaaS interfaces, across density regimes: Dense
  (Linear / Doppler / Raycast / Vercel), Comfortable/roomier (Cal.com style), and
  anything in between. Use this whenever you are building OR refining any such UI —
  dashboards, data tables, sidebars, toolbars, filter bars, forms, inputs, buttons,
  badges/pills, KPI tiles, nav items, list rows, icon rails — or whenever you're
  picking font-size, weight, line-height, letter-spacing (tracking), padding, gaps,
  corner radius, or control heights, even if the user doesn't name a grid. Trigger it
  when spacing "looks off," when values are arbitrary (p-[13px], gap-18px, radius-7px,
  height: 60px), when snapping a design to an 8px grid, or when the user mentions
  tracking, density, Inter/SF Pro metrics, or wants a component to feel "tight" and
  premium. Prefer this over eyeballing numbers.
---

# Dense UI Metrics

A single source of truth for the numbers that make productive SaaS UIs feel engineered
rather than hand-placed. Every value traces to an industry spec: Inter Dynamic Metrics
(Rasmus Andersson) for tracking, IBM Carbon 2x grid + Material Design 3 8dp grid for
spacing/density, Bringhurst / Carbon Productive sets for type. The point of encoding it
is that "premium" isn't taste — it's a small set of locked relationships. Follow them
and the rhythm holds; break one and the eye notices even when the user can't say why.

**The model in one breath:** a small set of **universal laws** (this file) applied at a
chosen set of **anchors** (a *regime*). Laws never change; anchors slide with density.
Regimes are named points on a continuous axis, **not** boxes every app falls into — if a
design matches no preset, read its base font size and base padding off the reference and
apply the laws at those numbers.

## Where things live

- **This file** — the universal laws (grid, tracking, derived height, degrees of
  freedom) + the apply-loop + self-check. Read top to bottom; it's the whole method.
- **`references/regimes.md`** — the regime concept and the full property matrices
  (Dense + Comfortable): per-role font size, weight, line-height, tracking, padding,
  height. **Read this when you need concrete numbers for a component.**
- **`references/component-patterns.md`** — recipes for specific components that don't
  reduce to a single-line control: multi-line list rows, icon-only nav rails, corner-
  radius scale, row-separation strategy (zebra vs borders vs whitespace), inline code
  chips. **Read this when building lists, rails, cards, or choosing radii/separators.**

## How to apply (the loop)

1. **Pick the regime, then the component role.** Regime = density anchor set (Dense /
   Comfortable / read-your-own). Then find the role's row in `references/regimes.md` —
   it gives size, weight, line-height, tracking, and padding at once. Don't mix values
   across roles or across regimes on one screen.
2. **Snap every spacing value to the grid** (§Spatial scale). Padding, margin, gap,
   offsets. No arbitrary numbers — `13px`, `18px`, `60px` are smells. Nearest step wins.
3. **Derive height, don't set it.** `H = L + 2·Py` (Degree 4). A 36px control is
   `20px line-height + 2×8px`, not a magic `height: 36px` with mystery padding. (Multi-
   line rows are the exception — see `references/component-patterns.md`.)
4. **Apply tracking by font size** (§Tracking). Small text loosens (positive), large
   text tightens (negative). Headings left at `0` look soft; body over-tightened looks
   cramped. This is where cheap UIs give themselves away.
5. **Vary only along the degrees of freedom** (§Degrees of freedom) when a design needs
   to breathe or compress. Those axes are the *only* sanctioned ways to move off the
   defaults without breaking rhythm.

## Fonts

- **UI / data:** neutral neo-grotesque sans with a high x-height — Inter, SF Pro Text,
  IBM Plex Sans. High x-height is what keeps 12–14px text legible at density.
- **Code / tokens / IDs:** tabular monospace where every glyph is 1:1 — JetBrains Mono,
  SF Mono, Fira Code. Use for anything that aligns in columns (secrets, hashes, numbers
  in tables) and for inline code chips (see `references/component-patterns.md`).

## Tracking (dynamic letter-spacing)

Tracking is a function of size, from the Inter metrics spec:

```
Tracking(z) = -0.0223 + 0.185 · e^(-0.1745·z)     # z = font size in px, result in em
```

You rarely need to compute it — this lookup covers the common sizes (the formula
evaluated):

| Size | Tracking | | Size | Tracking |
|---|---|---|---|---|
| 10px | `+0.010em` | | 18px | `-0.014em` |
| 11px | `+0.005em` | | 20px | `-0.017em` |
| 12px | `0.000em`  | | 24px | `-0.020em` |
| 13px | `-0.003em` | | 28px | `-0.021em` |
| 14px | `-0.006em` | | 32px | `-0.022em` |
| 16px | `-0.011em` | | 40px+ | `-0.022em` (asymptote) |

Rule of thumb: **≤12px loosens, ≥14px tightens, and it never goes past ≈-0.022em.** At
12–14px the delta is sub-pixel — real but subtle; at 20px+ it's clearly visible and is
the single highest-leverage fix for a heading that looks unrefined.

## Spatial scale (8px grid + 4px micro-unit)

All padding, margin, gap, and layout offsets come from here:

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64px`  (4px is the micro-unit for icon-to-text and pill internals).

Four roles, each ~1.5–2× the previous (Degree 3):

- **S1 — micro offset:** 4px (icon↔label, pill inner padding)
- **S2 — element gap:** 8–12px (between related controls, form fields)
- **S3 — container padding:** 16–24px (card/panel interior)
- **S4 — layout gap:** 32–48px (between sections/regions)

Dark-surface detail: on deep backgrounds (`#0d0d10`–`#16171a`) use translucent hairline
borders (`rgba(255,255,255,0.08)`–`0.1`) rather than solid greys — they read as one crisp
pixel instead of a muddy line.

## Degrees of freedom

The defaults aren't a straitjacket. There are exactly four mathematically-safe axes to
move along — vary these, not the raw numbers:

**1 — Axial asymmetry (Px vs Py).** Horizontal padding should run ~1.5–2× the vertical
(`Px ≈ 1.5–2 · Py`). Glyphs already carry vertical whitespace between x-height and
cap-height, so symmetric padding (`12×12`) makes a control look taller than it is wide.
This is why every *text-bearing* control has Px > Py.

> **Exception — icon-only controls are square (`Px = Py`).** The asymmetry rule is a
> *text* rule; it exists to cancel glyph whitespace. An icon has no baseline/x-height
> asymmetry, so it's optically centered as a square. Icon buttons, toolbar actions, and
> nav-rail icons get equal padding — widening them per the text rule stretches them wrong.

**2 — Density scaling (steps of ±2/±4px on Py).** To make Compact / Comfortable /
Spacious variants, step vertical padding by 2 or 4px: `Py(D) = Py0 + D·2px`,
`D ∈ {0,-1,-2,-3}`. Height follows via Degree 4, so the grid never breaks. Constraint:
keep interactive hit targets ≥ **32px** for mouse (desktop), ≥ **48px** for touch —
shrink padding for looks, but pad the *hit area* back if needed.

**3 — Proximity hierarchy (preserve the ratio, shift the values).** You can slide the
S1–S4 values as long as each tier stays ~1.5–2× its inner neighbor. Proximity is how the
eye groups things (Gestalt) — the *ratios* carry the hierarchy, not the absolute numbers,
so a denser or airier design just rescales all four together. Works on both axes (stacked
*and* inline groups).

**4 — Height is derived, never typed.** `H = L + 2·Py`. Example: 20px line-height +
2×8px padding = a 36px control. Set line-height and padding; let height fall out. If you
ever write `height: 37px`, one of L or Py is off-grid. (Exception: multi-line list rows
and square icon targets — see `references/component-patterns.md`.)

## Quick self-check

- Any spacing value not on `4/8/12/16/24/32/48/64`? Snap it.
- Any `height:` on a single-line control that isn't `L + 2·Py`? Re-derive it.
- Heading ≥20px still at tracking `0`? Tighten it.
- Symmetric `n×n` padding on a *text* button? Widen Px to ~1.5–2× Py. (Icon button? Keep it square.)
- Interactive target under 32px tall? Grow the hit area.
- Arbitrary corner radius (`7px`, `11px`)? Snap to the radius scale (`references/component-patterns.md`).
- Mixing Dense rows into a Comfortable screen? Pick one regime and hold it.
