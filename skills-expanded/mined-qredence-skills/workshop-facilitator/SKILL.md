---
name: workshop-facilitator
description: "Designs a workshop structure with sections, prompts, timing, and facilitator guidance. Use for brainstorms, retrospectives, kickoffs, or design studios when the result should be created in Figma Design or delivered as a board specification."
---

# Workshop Facilitator

## Capability Mode

`Create in Figma Design when supported; otherwise specify`. Do not assume the current agent session can create or edit FigJam boards.

## Inputs

- Workshop goal and format
- Participant count and session duration
- Live or asynchronous mode
- Existing template or design-system constraints, when available

## Workflow

1. Define the desired decision or outcome.
2. Choose the minimum set of activities needed to reach it.
3. Allocate realistic timeboxes, including instructions, discussion, and synthesis.
4. Specify each section's title, prompt, participant action, and expected output.
5. Add facilitator notes for transitions, voting, conflict, and incomplete participation.
6. Include an opening context area and a closing decisions/actions area.
7. Create the structure on the current Figma Design canvas when requested and supported; otherwise return a complete board specification.

## Guardrails

- Do not claim FigJam editing unless that surface is explicitly available.
- Avoid decorative complexity that competes with participation.
- Do not invent organizational decisions, attendees, or research inputs.
- Keep edits scoped and reversible.

## Output Contract

Return the ordered workshop sections, prompts, timeboxes, facilitator notes, expected outputs, assumptions, and whether the artifact was created or proposed.
