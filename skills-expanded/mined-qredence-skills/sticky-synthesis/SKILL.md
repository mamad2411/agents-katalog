---
name: sticky-synthesis
description: "Synthesizes provided sticky-note content into evidence-based themes, counts, takeaways, and outliers. Use after a brainstorm, retro, or research session when sticky content is visible in the current Figma Design file or supplied as text."
---

# Sticky Synthesis

## Capability Mode

`Review and structure`. Work from visible or supplied sticky content. Do not assume the Figma Agent can read or edit a FigJam board unless that surface is explicitly available in the current session.

## Scope

- Default to the current selection or named section.
- Use author, color, or spatial grouping only when their meaning is documented or clearly intentional.
- Ask only when missing source content prevents a credible synthesis.

## Workflow

1. Inventory every in-scope sticky or supplied note without silently dropping duplicates or outliers.
2. Group notes by underlying meaning, not keyword overlap alone.
3. Name 3-8 actionable themes and count the notes assigned to each.
4. Write a one- or two-sentence synthesized takeaway per theme.
5. Preserve important outliers and contradictory evidence.
6. Order themes by strength of evidence or by the workshop's documented structure.
7. When editing is supported and requested, create reversible grouping and labels in the current Figma Design canvas. Otherwise return the proposed structure.

## Guardrails

- Do not fabricate missing notes, participant intent, or research evidence.
- Do not claim direct FigJam access from a Figma Design session.
- Do not treat color or proximity as semantic evidence without confirmation.
- For report-only requests, do not alter the file.

## Output Contract

Return:

1. `Theme — count — synthesized takeaway`
2. Supporting notes or identifiers per theme
3. Outliers and contradictions
4. Assumptions and whether changes were applied or only proposed
