---
name: spacing
description: "Use when sizing gaps and density: the spacing scale, padding-to-gap ratios, optical alignment, section rhythm, and comfortable versus compact modes."
---


# Spacing and Density

Space is a grouping signal, not decoration — distance is how an interface says "these belong together and that one does not", and it says it before any border, background or label is read. So the default posture is: one scale for the whole project, every gap a step on it, and `gap` on the parent rather than margins on children. When a value feels wrong, the fix is almost always to change the *ratio between two gaps* rather than to nudge one of them; an interface reads as sloppy when nested gaps are similar, not when they are large. The sibling `layout` decides which regions exist and how they stack — if the open question is what goes where, that is `layout`, and this skill starts once the regions are settled. The other near-neighbour is `ui-polish`: nudging a single glyph inside its own box (a play triangle, an asymmetric caret) is theirs; balancing the space *around* a group is here.

**Find the project's scale before writing a single value.** Look for `theme.spacing` or a Tailwind `--spacing` setting, a `--space-*` token block, an SCSS `$space` map, or — most commonly — an implicit scale you can read off the existing components. Adopt it exactly, including its quirks. A `18px` gap in a codebase built on multiples of 4 is more damaging than a slightly wrong step from the real scale, because it teaches every future contributor that values are freehand. If the project has no scale, introduce the one below as tokens and convert the file you are already touching, not the whole codebase.

## Quick Reference

| Topic | File |
| --- | --- |
| You need the actual numbers — a step value, its Tailwind class, a component's padding recipe, or the comfortable/compact/dense row specs | Open [scale.md](references/scale.md) whenever a concrete value or a density table is required rather than a rule. |

## Core Principles

1. **Ship one scale and make every gap a step on it.** A closed set makes a wrong choice visible; an open set makes every choice arguable. The default is `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96` px, expressed as tokens. **Exception:** a single optical correction (`-1px`, `2px`) may sit off-scale where it fixes an alignment illusion, and it must carry a comment saying so — otherwise the next person "rounds it to the scale" and reintroduces the bug.

2. **Steps go linear near zero and geometric above it.** `4px` is a large relative jump at small sizes and an invisible one at large sizes, so a purely linear or purely geometric scale fails at one end. Below `16px` the increment is `4px`; above `16px` each step is roughly `1.5×` its predecessor. **Exception:** a project already on a strict 8px grid — keep it and do not rebase; a half-migrated scale is worse than either scale.

3. **A container's padding is one step above the gap it contains.** With `padding < gap`, items look glued to the container's edge and disconnected from each other, which inverts the grouping you were trying to express. So `gap: 16px` takes `padding: 24px`. **Exception:** full-bleed children — list rows with edge-to-edge hover states, images that must touch the card edge — take `padding: 0` on the container and supply their own inset internally.

4. **The gap between groups is at least `2×` the gap within a group.** Below 2× the eye cannot resolve which level it is looking at, and the layout reads as one undifferentiated list; at 2× or more the grouping is unmistakable without a single divider line. Rendered on the scale that is `8` within, `24` between, `48` at section level. **Exception:** uniform dense lists and tables, where every row is a peer and separators do the grouping — that is `dense-ui`'s territory.

5. **Use `gap` on the parent; never `margin-bottom` on every child.** Margin leaves a trailing gap after the last item, collapses in ways that depend on the neighbours, and bleeds past the component's own boundary so the component is no longer safely droppable anywhere. Write `display: flex; flex-direction: column; gap: 12px`. **Exception:** deliberate bleed — pulling a full-width child out of a padded parent with a negative margin (`-mx-4`) — which is a layout escape, not spacing.

6. **Derive vertical text rhythm from line-height, not from round numbers.** A `12px` paragraph gap next to a `24px` line-height creates a rhythm that breaks the moment the type scale changes. Set paragraph spacing to `1×` the element's own line-height (`margin-block-end: 1lh`), and give headings more space above than below at a `2:1` ratio, because the space belongs to the thing the heading introduces. **Exception:** the first child of a container never carries a top margin — the container's padding already did that job, and doubling it is the most common source of a lopsided card.

7. **Pick one section gap and reuse it everywhere on the page.** Sections separated by `64`, then `72`, then `80` read as accidental, and no reader can tell which variation was meaningful. The house defaults are `64px` between marketing bands on mobile and `96px` on desktop, `32px` between sections inside a product page. **Exception:** a band with its own background colour holds the space as *padding inside* the band rather than as a gap outside it — otherwise the coloured block floats with dead margins above and below.

8. **Make density a token swap, not a redesign.** A "compact mode" implemented by hand-editing padding in forty components will drift within a release. Express it as a multiplier over the same scale, applied only to container padding, row height and control height — never to type size, never to section gaps, because shrinking those makes the UI look broken rather than dense. Row heights are `48 / 40 / 32` for comfortable / compact / dense. **Exception:** the pointer-target floor, which belongs to `touch-input` and which density never overrides — a dense table on touch keeps full-size targets even when the row looks tighter.

9. **Align to the ink, not to the bounding box.** A control whose right edge holds a chevron or a trailing icon has visual mass that its box does not report, so mathematically equal padding reads as heavier on that side. Reduce the icon-side padding by `2px` (`pl-4 pr-3.5`). The same correction applies to a trailing count badge and to text set beside a circular avatar. **Exception:** anything inside a data grid, where column alignment across rows beats per-cell optics.

## Output Format

When introducing or repairing a scale, emit the tokens first and the usages second — a diff that changes values without naming them is unreviewable:

```css
:root {
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px;
  --space-4: 16px; --space-6: 24px;  --space-8: 32px;
  --space-12: 48px; --space-16: 64px; --space-24: 96px;
}
```

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| `margin-bottom` on every child of a list | `gap` on the parent |
| A value not on the scale (`18px`, `30px`) | Nearest step, or an off-scale comment saying why |
| Nested gaps within `1.5×` of each other | Push the outer one to at least `2×` the inner |
| Container padding smaller than its inner gap | Padding is one step above the gap |
| Card lopsided — more space at the top than the bottom | First child carrying a top margin on top of container padding |
| Section gaps varying band to band | One section gap, reused |
| A coloured band with margins above and below | Convert the gap to padding inside the band |
| Compact mode shrinking the type | Density touches padding and row height only |
| Trailing-icon button looking right-heavy | `2px` off the icon-side padding |
| A divider added to make a group readable | Increase the gap ratio first; keep the divider only if it still fails |

## Checklist

- [ ] Project scale detected and reused; no freehand values
- [ ] Steps linear below `16px`, geometric above
- [ ] Container padding one step above the gap it contains
- [ ] Group gap at least `2×` the within-group gap
- [ ] `gap` on parents; no per-child margins
- [ ] Paragraph spacing tied to line-height; no top margin on first children
- [ ] One section gap per page; coloured bands pad inside
- [ ] Density expressed as a token multiplier, type untouched
- [ ] Trailing-icon padding optically corrected
