---
name: grid-margin-safe-zone-alignment
description: Restores a consistent grid, even margins, and a respected safe zone so elements stop drifting past the template's edges.
---

# Grid, Margin and Safe-Zone Alignment

## When to use

Use this skill when elements drift past the template's margins or ignore the layout grid. Symptoms include titles that start at a different x position on every slide, content that runs to the slide edge on some slides and stops short on others, and objects nudged a few pixels off the placeholder so nothing lines up across the deck. Run this after placeholders are in order, so you are aligning real placeholders rather than rogue boxes.

## What it does

It re-establishes the template's grid and margins across the deck: a single left margin, a single right margin, a consistent top position for titles, a consistent content top, and a safe zone that nothing important crosses. The output is a deck where, if you flipped through it, the title and content blocks would hold their position from slide to slide.

## Method

A template defines an implicit grid: the margins, the column structure, and the safe zone that keeps content away from the trim and away from any footer band. The job is to make every slide honor it.

1. **Recover the template's margins.** Read the placeholder positions on the master and layouts. The title placeholder's left edge defines the left margin. Its right edge (or the content placeholder's) defines the right margin. The content placeholder's top defines the content top. Record these as the canonical values.

2. **Set guides to the margins.** Turn on guides (Alt then F9) and place vertical guides at the left and right margins and horizontal guides at the title top and content top. Place a safe-zone guide a small inset from each slide edge. These guides become the alignment reference for the whole deck.

3. **Snap placeholders back to the layout.** For any slide where the title or content placeholder has been nudged, use Home then Reset to return placeholders to the layout position, or align them to the guides by hand. Titles and content should share the same left edge across the deck.

4. **Build on a column grid.** For multi-element slides, divide the content area into a consistent number of columns (commonly two, three, or four) with even gutters. Align cards, charts, and images to column edges rather than eyeballing. Use Align (Arrange then Align) to distribute evenly: Align Left, Align Top, Distribute Horizontally.

5. **Enforce the safe zone.** Move any element that crosses the safe-zone inset back inside it, unless the layout is a deliberate full-bleed image layout. Nothing structural (text, logos, page numbers) should sit in the trim margin.

6. **Even the spacing.** Make the gap between stacked elements consistent (for example a single vertical rhythm value), and make the gutter between columns consistent. Uneven gaps read as sloppy even when alignment is correct.

7. **Check across slides, not just within one.** Step through the deck in slide sorter or a flip-through and watch the title and content blocks. They should not jump. Fix the outliers.

## Inputs

- A deck with content in real placeholders.
- The template's margin and placeholder positions, or access to the template so they can be read.

## Output format

A short alignment spec plus a fix list:

- The canonical values: left margin, right margin, title top, content top, safe-zone inset, column count and gutter.
- A per-slide list of elements that violate the grid, margins, or safe zone, and the corrective move (reset, align to guide, distribute).

Close with a confirmation that titles and content share one left edge and nothing crosses the safe zone.

## Example

Input: a deck where slide titles start at three different x positions and a chart on slide 6 runs into the right trim.

Output:

- Canonical values: left margin 0.5 in, right margin 0.5 in, title top 0.3 in, content top 1.4 in, safe-zone inset 0.3 in, three columns with 0.25 in gutters.
- Slide 2, 4, 7: title left edge off by a few points. Reset placeholders.
- Slide 6: chart crosses the right safe zone. Resize to the right margin guide.
- Result: titles share one left edge and no element crosses the safe zone.
