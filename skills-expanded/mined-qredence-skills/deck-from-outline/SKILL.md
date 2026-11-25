---
name: deck-from-outline
description: "Converts an outline or document into a slide-by-slide presentation plan and, when supported, a consistent deck in the active Figma surface."
---

# Deck From Outline

## Capability Mode

Create slides only when the active surface supports slide editing. Otherwise provide a complete slide specification. Do not assume Figma Slides access from Figma Design.

## Workflow

1. Identify the audience, goal, and target length.
2. Convert the source into one main message per slide.
3. Build a clear narrative from context through evidence to recommendations and next steps.
4. Assign each slide a repeatable layout pattern.
5. Preserve supplied facts and flag unsupported claims or missing evidence.
6. Reuse the active file's theme, components, and styles when accessible.
7. Create the deck only when supported; otherwise return a production-ready slide plan.

## Guardrails

- Do not claim access to Figma Slides unless explicitly available.
- Do not invent metrics, quotes, sources, or conclusions.
- Keep visible slide text concise.
- Separate presenter guidance from visible slide content.

## Output Contract

Return a numbered slide plan with title, purpose, visible content, layout direction, presenter guidance when needed, assumptions, and whether slides were created or specified.
