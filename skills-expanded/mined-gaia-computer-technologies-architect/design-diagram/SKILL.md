---
name: design-diagram
description: Draws architectural diagrams as clean SVG, including adjacency or bubble diagrams sized by area, programme stacking by level, zoning and circulation diagrams, from a list of spaces and their relationships, and reports which adjacencies the layout could not satisfy. Use when the architect wants a "bubble diagram", "adjacency diagram", "relationship matrix as a diagram", "stacking diagram", "zoning diagram", "circulation diagram", or a quick programme diagram for a report or pin-up. Takes its spaces from design-brief or programme-schedule; hands to dxf-drawing when the diagram needs to become a plan at scale, and to concept-parti when the diagram suggests an organising idea.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Diagram

A diagram is an argument about relationships, not a plan. This skill turns a programme into diagrams that are honest about size (bubble area follows space area) and about what doesn't fit, which is usually the useful part.

## When to use

- After a brief or schedule exists, to see the programme as relationships before drawing plans.
- To test an adjacency matrix: can these relationships coexist, or does something have to give?
- To show stacking: what goes on which level, and how big each level gets.
- For report and presentation graphics that need to be editable (SVG opens in Illustrator, Affinity, Inkscape, Figma).

## Input

- **Spaces:** name, area, and optionally zone (public / private / service / teaching) and level. Areas come from the architect or `programme-schedule`. Don't invent them. If a space has no area, ask, or draw it at a stated nominal size and label it "area TBC".
- **Relationships:** pairs marked `required` (must touch), `desired` (should be near) or `avoid` (keep apart: noise, smell, security, privacy). An adjacency matrix converts directly into this list.
- **Diagram type:** bubble (default), stacking, or a hand-built zoning/circulation diagram (see below).

## Process

1. **Build the spec** in the JSON format documented in `scripts/adjacency_diagram.py`.
2. **Run it.**
   - Bubble: `uv run scripts/adjacency_diagram.py spec.json --out bubble.svg`
   - Stacking: `uv run scripts/adjacency_diagram.py spec.json --out stack.svg --mode stack`
   - Try `--seed N` for a different arrangement. Layouts are deterministic per seed.
3. **Read the report.** It lists required pairs that ended up apart and avoid pairs that ended up close. Those conflicts are the design content: they show where the programme forces a choice (a second entrance, a split level, a buffer zone).
4. **Look at the SVG** (render it to PNG to check if you can). Confirm labels are legible, nothing overlaps and the legend is complete.
5. **Zoning and circulation diagrams** have no generic script. Write the SVG directly. Use filled zones (rectangles or blobs) over a light base, circulation as a single heavy line with arrows, and entries as triangles. Keep it to three or four tones and one accent, and label every zone.
6. **Hand over** the SVG with a short reading: the clusters it found, the conflicts, and what they suggest.

## Domain knowledge

- **Bubble size is a claim.** Area-proportional circles let people compare sizes at a glance. A diagram with equal-sized bubbles quietly lies about the programme. Radius is computed from area (r = sqrt(A / pi)), so a 180 m2 hall really reads three times the size of a 60 m2 classroom.
- **Adjacency strength is a hierarchy.** Required means a shared wall or door (kitchen to dining hall). Desired means within a short walk or a visual connection. Avoid usually comes down to acoustic, odour, security, safeguarding or privacy separation. Give the reason for each avoid; it tells the next designer what buffer would solve it.
- **The layout is a test, not an answer.** Kamada-Kawai layout tries to meet a target distance for every pair at once. When it can't, the programme probably can't either, at least not on one level without a move. Report that; don't hide it by fiddling the seed until the picture looks tidy.
- **Stacking.** Level totals show floor-plate balance. A big imbalance between levels means either an odd massing or a programme that wants a different split. Ground-floor priorities are usually public entry, servicing, heavy plant, anything with goods in, and spaces needing level access. Check accessibility requirements with the applicable standard.
- **Graphic discipline.** Monochrome base with muted zone tones, one weight for outlines, text set horizontally, no drop shadows and no 3D. A diagram that needs a paragraph of explanation has failed.

## Output format

```
## Diagram: [title]

File: bubble.svg (or stack.svg)  |  Seed: 7  |  Spaces: 8  |  Total area: 570 m2 (sum of inputs)

Reading:
- [cluster or relationship the diagram shows]
- [the conflict, e.g. "Plant wants to sit by Kitchen but away from Library; the layout can only do both if Library goes upstairs"]

Unresolved: [required pairs apart / avoid pairs close, from the script report, or "none"]
Assumed: [any nominal areas or inferred relationships, labelled as such]
```

## What you don't do

- Don't invent areas or relationships. Infer them only when asked, and label them as inferred.
- Don't present a bubble diagram as a plan. It has no scale, no walls and no circulation. Use `dxf-drawing` for plans.
- Don't tune the seed to hide a conflict. Report it.
- Don't use the diagram to imply compliance (escape distances, accessible routes, separation distances). Those need a qualified professional and the applicable standard.
