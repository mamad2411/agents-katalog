---
name: drawio-roadmap-ppt
description: Use when creating or restyling editable Draw.io diagrams in a clean PPT / presentation card style — stage cards, timelines, process flows, architecture overviews, comparison grids, or mind maps that should look presentation-ready. For dense poster knowledge maps prefer drawio-roadmap-snake; for strict prerequisite course lanes prefer drawio-roadmap-swimlane.
---

# Draw.io Roadmap PPT

Create learning roadmaps and structured diagrams with Draw.io in a clean, polished PPT visual style — calm, modern, and fully editable.

## Related skills (routing)

| Need | Skill |
|------|--------|
| Presentation stage cards, 3–7 nodes, talk-through slides | **this skill (ppt)** |
| Strict learning order, unit title + subtitle, swimlanes | `drawio-roadmap-swimlane` |
| Dense poster / S-shaped dual-color track knowledge map | `drawio-roadmap-snake` |

If unsure, ask which style they want, or offer ppt for presentation and snake for poster density.

## Workflow

1. Identify the diagram's message, audience, reading direction, and final canvas.
2. Reduce the content to one title, 3–7 primary nodes, short supporting text, and explicit relationships.
3. Choose one layout:
   - Use a horizontal stage road for sequential learning plans and timelines.
   - Use a vertical flow for procedures and decision paths.
   - Use a hub-and-spoke layout for topic maps.
   - Use a grid for comparisons or independent categories.
   - Use layers for systems and ownership (for course swimlanes with forced arrows, switch to `drawio-roadmap-swimlane`).
4. Read [references/visual-system.md](references/visual-system.md) before designing or restyling.
5. Read [references/drawio-xml.md](references/drawio-xml.md) when creating or editing Draw.io XML directly.
6. Reuse [assets/python-learning-ppt.drawio](assets/python-learning-ppt.drawio) when a card-based roadmap is suitable; replace its content and adjust the number of stages rather than rebuilding it.
7. Generate an uncompressed `.drawio` file with stable, descriptive cell IDs.
8. Produce an SVG preview and, when local conversion is available, a PNG preview.
9. Run `python3 scripts/validate_drawio.py <file.drawio>`.
10. Inspect the rendered preview at normal viewing size and revise until it passes the visual checks.

## Content Rules

- Lead with one clear takeaway, not a generic diagram title.
- Limit primary stages to 3–7; group extra material into notes or sub-items.
- Keep stage titles to 4–10 Chinese characters or 2–5 English words.
- Keep descriptions to one line when possible.
- Use 2–4 actions per card and one measurable milestone.
- Express parallel items with equal visual weight.
- Express sequence with position first and arrows second.
- Remove decorative elements that do not communicate hierarchy, grouping, state, or direction.

## Draw.io Output Rules

- Deliver an editable `.drawio` source as the primary artifact.
- Use `mxfile > diagram > mxGraphModel > root` with cells under parent `1`.
- Put background and containers before their child labels so the stacking order is correct.
- Use separate cells for cards, labels, badges, and connectors when users may edit them independently.
- Use `html=1;whiteSpace=wrap;` for text-bearing shapes.
- Escape XML-reserved characters; encode line breaks as `&lt;br&gt;`.
- Avoid images for text, icons, connectors, or shapes that Draw.io can represent natively.
- Keep important content inside a 60–100 px safe area.
- Do not rely on font weights or fonts unavailable on common systems.

## Visual QA

Verify all of the following in the preview:

- Read the title and stage sequence within three seconds.
- Keep cards aligned and equally sized unless hierarchy intentionally differs.
- Keep at least 24 px between independent objects and 28–40 px internal card padding.
- Prevent text from touching edges, wrapping awkwardly, or exceeding two hierarchy levels inside a card.
- Use one saturated accent per stage and neutral colors for most surfaces.
- Keep arrows behind cards, aligned to node centers, and visually quieter than content.
- Use color consistently: the same color must represent the same stage or semantic meaning.
- Check contrast on tinted labels and dark panels.
- Ensure the layout still reads at 50% zoom.

If the preview cannot be rendered, validate the XML and state that visual inspection remains outstanding.

## Delivery

Return:

- A link to the `.drawio` source.
- An inline PNG or SVG preview when available.
- A one-sentence description of the layout and how to edit it.

Do not overwhelm the user with implementation details unless requested.
