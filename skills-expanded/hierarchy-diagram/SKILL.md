---
name: hierarchy-diagram
description: "Create an editable PowerPoint hierarchy or organization diagram with a parent, child nodes, connectors, and optional rollout states. Use for organizational structure or staged adoption diagrams. 階層図、組織図、部門展開の段階表示に使用。"
license: MIT
---

# Hierarchy Diagram

1. Confirm the parent, children, labels, relationships, and target slide/card.
   Do not invent departments, customer names, adoption status, or progress.
2. Measure the available region below the heading. Use native editable shapes
   and connectors, not an image. Follow the deck's palette and font.
3. Place one parent centered above evenly spaced children. Center connectors on
   nodes, keep labels readable, and route lines behind boxes without crossing text.
   Start with navy `1E2761` for the parent and blue `0F6CBD` for active nodes
   only if the existing theme does not prescribe other colors.
4. For three children, a starting layout is a parent about 60% of inner width,
   three equal child boxes, and gaps about 4% of inner width. Scale from the
   actual slot; do not reuse absolute EMU coordinates from another deck.
   Reflow to more rows or slides rather than shrinking labels below readability.
5. When rollout states are requested, distinguish them with text as well as color:
   - Not started: pale fill, dashed outline, explicit state label.
   - Developing: pale blue fill, navy text, explicit state label.
   - Active: blue fill, white text, explicit state label.
   An optional four-step story is none started, one developing, one active,
   then all active. Use it only when these states are supplied or clearly
   labeled as a hypothetical example.
6. Preserve existing content; replace only the requested diagram. Never clear
   all non-title objects from an existing slide without approval.
7. Check connectors, spacing, labels, contrast, reading order, and editability.
   Aim for at least 14 pt labels; split the diagram if necessary.
   Report the created structure and any unsupported editing capabilities.
