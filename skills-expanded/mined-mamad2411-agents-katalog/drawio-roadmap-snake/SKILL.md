---
name: drawio-roadmap-snake
description: Create or redesign editable Draw.io snake-style roadmaps with continuous U-turn tracks, paired color lanes, category bands, knowledge columns, priority markers, and smooth stage transitions. Use for learning paths, curriculum maps, skill trees, product capability maps, certification routes, career roadmaps, and .drawio diagrams that should read as a colorful winding route.
---

# Draw.io Snake Roadmap

Build dense learning maps around a continuous S-shaped route while keeping every label, track, and category editable in Draw.io.

## Related skills (routing)

| Need | Skill |
|------|--------|
| Dense poster / S-shaped dual-color track knowledge map | **this skill (snake)** |
| Presentation stage cards, 3–7 nodes, talk-through slides | `drawio-roadmap-ppt` |
| Strict learning order, unit title + subtitle, swimlanes | `drawio-roadmap-swimlane` |

If unsure, ask which style they want, or offer ppt for presentation, swimlane for course order, and snake for poster density.

## Workflow

 1. Define the route order and group the content into 3–6 major stages.
 2. Limit each horizontal run to 3–5 equal columns.
 3. Alternate reading direction at every U-turn.
 4. Read references/snake-style.md before creating or restyling the route.
 5. Reuse assets/python-learning-snake.drawio as a reference for layout, band stacking, and arc construction.
 6. Replace headings and items before changing track geometry.
 7. Add or remove entire column modules on the straight segments.
 8. Build turns from native `mxgraph.basic.arc` vertices, never from automatic curved edges, embedded images, stacked rounded rectangles, or white masks.
 9. Open the `.drawio` file in Draw.io/diagrams.net and inspect every tangent, color boundary, and turn; do not rely only on a separate SVG preview.
10. Run `python3 scripts/validate_snake_roadmap.py <file.drawio>`.

## Content Structure

- Use one major-stage label on the outer lane.
- Use category labels on the adjacent inner lane.
- Place knowledge items in the white corridor between route runs.
- Keep each item to one line.
- Use consistent priority markers, such as `A` for required and `B` for awareness.
- Keep 2–5 items per category; split overloaded categories.
- Add a compact legend only when marker meanings are not obvious.

## Required Geometry

- Keep all straight bands at one lane thickness.
- Keep adjacent lane centerlines one lane thickness minus 1–2 px apart.
- Use the same turn center for paired lanes.
- Make the inner radius equal to the outer radius minus the lane separation.
- Join straight runs tangentially; do not create visible corners at entry or exit.
- Overlap adjacent color lanes by 1–2 px to prevent antialiasing seams.
- Keep straight band rectangles over the arc cells in the stacking order so endpoints meet cleanly.
- Use paired native `mxgraph.basic.arc` vertices with identical vertical centers and tangent lines.
- Use `startAngle=0;endAngle=0.5` for a right U-turn and `startAngle=0.5;endAngle=1` for a left U-turn.
- Do not use `curved=1` Draw.io edges for thick U-turns. Draw.io recalculates their splines and can create slopes, flat spots, and mismatched tangents.

## Visual Rules

- Use a white canvas and saturated route colors.
- Pair every major color with a lighter or neighboring inner-lane color.
- Use dark text on route bands and black or near-black text in the corridor.
- Use 24–30 px type for route headings and 18–22 px type for items.
- Align all column starts and repeated item baselines.
- Keep the route as the strongest visual element; avoid card borders and decorative shadows.
- Use simple native symbols or text glyphs when icon assets are unavailable.

## QA

Verify at normal viewing size:

- Follow the route without guessing where it continues.
- See no step, notch, white gap, or thickness change at a turn.
- Keep paired lanes parallel through the full curve.
- Keep entry and exit segments horizontal before they meet content columns.
- Prevent text from entering the colored turn area.
- Preserve at least 24 px between item rows.
- Keep the diagram readable at 50% zoom.

Deliver the editable `.drawio` source and an inline preview. If the preview differs from the Draw.io source, correct the source rather than treating the preview as authoritative.