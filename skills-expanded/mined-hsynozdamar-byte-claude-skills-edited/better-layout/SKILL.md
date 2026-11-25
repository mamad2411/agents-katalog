---
name: better-layout
description: "Layout structure: grouping, alignment, reading order, spacing, safe areas, breakpoints, RTL. Use when building or reviewing layout, or when a screen feels cluttered, misaligned or breaks on resize."
---

# Layout

Position, spacing and alignment carry hierarchy before a word is read. Build that structure, then stress-test it: resize it, translate it, mirror it for RTL.

Write fixes in the project's styling system. The numbers below are starting points for projects with no density or spacing system, and compact professional tools can go tighter as long as the stress tests still pass.

Hit areas and focus belong to `better-accessibility`, radius and motion to `better-ui`, measure and text spacing to `better-typography`.

## Grouping and hierarchy

- **Space first, shapes second, lines last.** Gap between groups at least 2x the gap within one (`8px` inside, `16px`+ between). A separator is for dense data (tables, long settings) and stays quiet; never stack one on a gap that already did the job.
- **Controls look like controls.** Every interactive element gets a fill, border, underline or a consistent control zone. The reverse too: a static badge shaped like a button collects dead clicks.
- **Shared edges.** Few alignment edges, everything on them. One spacing step per level of nesting (`16px` is a good default). Numbers in tables align trailing, text leading.
- **Order by importance.** Key fact near the top and leading edge; within a row, identity leads, metadata and actions trail. Don't bury the one number the user came for under secondary detail.
- **Light entry point.** One primary action per view. Past two or three secondary actions, move them into a menu. A short view linking deeper beats a long one showing everything.

## Spacing and edges

- **Between targets.** `12px` between bordered or filled controls, `24px` around borderless text or icon buttons (the space is their only boundary), `24px`+ between unrelated groups. Keep an existing usable density instead of inflating it.
- **Inset buttons.** Full-width buttons in content stay inside the layout margins (start near `16px` on mobile) with a visible radius. Edge-to-edge is fine when it's deliberate platform chrome that respects safe areas.
- **Content bleeds, controls float.** Backgrounds, media and scroll lists may reach the viewport edges; text and controls stay inside margins and `env(safe-area-inset-*)`. Sticky chrome floats above content.
- **Hint at hidden content.** Collapsed or off-screen content needs a cue: the next card peeking `16` to `32px` past the edge, or a disclosure labelled with what it hides ("Show 12 more results", not "More"). A row that ends exactly at the edge looks complete, so nobody scrolls.

## Adaptivity

- **Logical properties** for anything direction-dependent (`ms-4 pe-6 text-start`, `inset-inline-end`). Physical sides only for physical geometry such as a notch. Sequences (steps, ratings, progress) mirror in RTL; digits never reverse.
- **Breakpoints come from content.** Break where the layout stops fitting, not at 768/1024 by default. Collapse late. Prefer container queries for components so a card adapts to its column, not the viewport. Test the smallest and largest sizes first.
- **Plan for growth.** Translations grow, and short labels grow the most. No fixed width or height on text containers (`max-width`, `min-height`, wrapping instead); buttons size from padding, not a fixed width. Test with pseudo-localization.
- **Never clip the critical action.** Keep primary actions out of places resizing, a fixed-height modal or the keyboard can cut off. A modal's content scrolls; its action row doesn't.

CSS for the peeking scroller, full-bleed grid, safe-area FAB, container query and the logical property map: [references/recipes.md](references/recipes.md).

## Reporting (standalone)

`HIGH`: content or an action blocked at a supported viewport. `MEDIUM`: hurts hierarchy, reading order or adaptability. `LOW`: isolated alignment or spacing. One row per root cause: Severity, Location (`path:line`), Before, After, Why. Check every supported width, 200% zoom and the RTL mirror; mark what you couldn't run `Not verified`. End with `Block` if any `HIGH`, else `Approve`.
