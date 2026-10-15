---
name: ui-polish
description: "Use when a UI works but feels unfinished and no single dimension is obviously wrong: optical corrections, hairlines, cursors, selection, and missing interaction states."
---


# The Last Ten Percent

When a UI works and still feels unfinished, assume the missing thing is a *state*, not a value. The overwhelmingly common cause is that some interactive element has a hover but no focus, a focus but no pressed state, no disabled treatment, or no answer for the second between the click and the response. Run the state sweep before you touch a single pixel value. Only once every interactive element has a complete row do you go looking for the optical nudges, the hairline greys, and the cursor that lies — and those are what this skill owns, because nobody else does.

This skill is the residue and nothing more. If you can name the dimension — shadow, radius, elevation, blur, gap, density, breakpoint — it is out by its own description, and `surfaces` owns the plane while `spacing` owns the gaps. Two more edges are worth naming, because they are the ones people reach for here first: the *construction* of a focus ring is `a11y`'s, and the colour of a text selection is `color`'s.

**Find where the project keeps its interaction states before adding one.** A `:hover` written at a call site in a codebase that has a `Button` component with variants is not polish, it is a fork. Look for the component layer, a `data-state` convention (Radix, Base UI), a `cva`/`tv` variant map, or a global stylesheet of element defaults, and put the missing state where its siblings already live. Corrections belong at the lowest layer that covers every instance.

## Quick Reference

| You need | Open |
|---|---|
| The full sweep, in order, to run over a finished component or page | `references/checklist.md` — open it when the request is "go over this" and nothing specific is named. |
| The nudge for a specific shape, glyph, or label pair | `references/optical-corrections.md` — open it when something is mathematically centred and still looks wrong. |

## Core Principles

1. **Fill the state matrix before anything else.** Every interactive element owes five states — rest, `:hover`, `:focus-visible`, `:active`, `:disabled` — plus a loading treatment wherever the action is async. Missing states are why a UI feels dead while every value in it is defensible. The exception is a link inside prose, which does not need an `:active` state distinct from its hover.

2. **Optical centring beats mathematical centring.** A glyph's bounding box is not its visual mass, so maths puts it in the wrong place. A button with a trailing icon takes `2px` less padding on the icon side — `pl-4 pr-3.5` — and a play triangle shifts `2px` toward its point. The exception is a symmetric glyph in a symmetric box: measure first, because a nudge applied to something already centred is just as visible as one that was missing.

3. **Hairlines have three values, not one per component.** Ship a three-step ladder — `#f2f2f2` for the faintest internal rules, `#ededed` for the workhorse divider, `#d9d9d9` where a line must actually be seen, the values Benji Taylor's site runs on — and render them at `0.5px` above `192dpi` through a `--border-hairline` variable that falls back to `1px`. Hand-picking a grey per divider is how a page ends up with nine of them. The exception is a hairline crossing a translucent surface, which needs alpha rather than hex or it will not composite.

4. **The cursor is a promise about what happens next.** `pointer` on everything clickable and on nothing else, `text` on the whole input wrapper rather than just the field, `grab` swapped to `grabbing` on pointerdown. During a drag or a resize, set the cursor on `body` for the duration — otherwise it flickers back to the default every time the pointer outruns the handle, which reads as the drag breaking. The exception is a disabled control: `cursor: not-allowed` only renders if the element still receives pointer events, so do not also set `pointer-events: none` when you want the cursor or the explanatory tooltip.

5. **A scrim is a multi-stop eased gradient, never two stops.** A two-stop linear fade bands visibly across its middle and leaves a soft hard line where there should be nothing at all; the fix is more stops following an easing curve, and Benji Taylor's site uses `12` so content dissolves under the viewport edge. Build it as `mask-image` rather than a gradient overlay wherever more than one background sits behind it. The exception is a flat modal overlay, which is one alpha over everything and not a fade at all. Never put a fade over scrollable content — it hides exactly what the reader is scrolling toward.

6. **Signal hover on the group, not only on the row.** Lightening the hovered row competes with every other row's background; dimming the *others* to `opacity: .3` reads instantly and needs no new colour, which is what Benji Taylor's site does on hover of a list. The exception is a list where rows carry their own status colour, since dimming would read as those items being disabled.

7. **Selection and caret are styled once, globally.** `user-select: none` on control chrome — button labels, tab strips, table headers — because a blue smear across a control reads as malfunction; then audit what select-all actually grabs, which should be content and not interface. `caret-color` is effectively the entire caret API, and replacing the caret means rebuilding text editing. The exception is a product aiming to feel installed, which inverts the default: selection off globally, re-enabled only on genuinely copyable content.

8. **The page animates in once, then holds still.** A surface that keeps moving after arrival reads as unfinished no matter how good each individual animation is. The reference implementation is an `8px` `translateY` plus a fade over `500ms`, staggered `50ms` per element with the total stagger capped at `400ms`, fired on first paint only — Benji Taylor's site. The exception is the app shell: `500ms` deliberately exceeds the `300ms` product ceiling because it is a document entrance that fires once per session, and a view the user returns to forty times a day gets no entrance at all.

## Smell / Fix

| Smell | Fix |
|---|---|
| "It works but feels dead" and nothing is nameable | Run the state matrix; find the missing rows |
| Icon looks off-centre in a button that is mathematically centred | `2px` less padding on the icon side |
| Nine slightly different divider greys | Three-step hairline ladder through one variable |
| Dividers look chunky on retina | `0.5px` above `192dpi`, `1px` fallback |
| Drag cursor flickers when the pointer moves fast | Set the cursor on `body` for the duration of the drag |
| Disabled button shows no `not-allowed` cursor | `pointer-events: none` is suppressing it — remove it |
| Visible band across a bottom fade | Two-stop gradient — go multi-stop and eased |
| Selecting text drags blue across the whole toolbar | `user-select: none` on control chrome |
| Everything on the page is subtly always moving | Entrance runs once, then the page is still |
| `cursor: pointer` on a heading | It is not clickable; remove it |

## Output Format

Report a polish pass as the state matrix, one row per interactive element, so the gaps are the finding:

| Element | Rest | Hover | Focus-visible | Active | Disabled | Loading |
|---|---|---|---|---|---|---|
| Primary button | ✓ | ✓ | — | — | ✓ | — |
| Row action | ✓ | ✓ | ✓ | ✓ | n/a | n/a |

A dash is a defect, `n/a` is a decision you can defend. Follow the matrix with the optical and hairline corrections as ordinary Before/After rows.

## Checklist

- [ ] Every interactive element has rest, hover, focus-visible, active, disabled, and loading where async
- [ ] Icons and asymmetric glyphs optically nudged, symmetric ones left alone
- [ ] One hairline ladder of three values, rendered at `0.5px` on high-DPI
- [ ] Cursors match behaviour; drag cursors set on `body` for the drag's duration
- [ ] Disabled controls still receive pointer events where a cursor or tooltip is wanted
- [ ] Fades are multi-stop and eased; no fade over a scroll area
- [ ] Hover states resolved on the group where a list is involved
- [ ] `user-select: none` on control chrome; select-all grabs content, not interface
- [ ] The page settles after its entrance and then stops moving
- [ ] Nothing in this pass belongs to `surfaces`, `spacing`, `a11y`, or `color`
