---
name: whiteboard-diagrams
description: Create accurate, simple, hand-drawn whiteboard diagrams from a user's process, system, architecture, learning workflow, comparison, or causal explanation. Use when the user asks for a scribbly whiteboard visual, educational workflow graphic, hand-drawn explainer, or diagram like the bundled reference; ask one focused clarification question when the subject or relationships are missing, then generate and visually verify the final image.
---

# Whiteboard Diagrams

Turn a described system into one causal picture that a new reader can follow without narration.

## Workflow

1. Read `SCALE.md` completely before composing or generating anything.
2. Extract the subject, audience, components, relationships, required labels, and output format from the request.
3. Apply the intake gate below. Do not invent a missing workflow.
4. Convert the request into a compact diagram spec. Use `references/INTAKE.md` for the schema and `references/EXAMPLES.md` when the topology is unclear.
5. Validate and compile the spec:

   ```bash
   python scripts/diagram_prompt.py validate path/to/spec.json
   python scripts/diagram_prompt.py build path/to/spec.json --output /tmp/diagram-prompt.txt
   ```

6. Generate one raster image with the available image-generation tool using the compiled prompt. For a brand-new diagram, do not pass unrelated reference images. If the user supplies a style reference, label it as a style reference, never as an edit target.
7. Inspect the actual output at full size. Check every required label, arrow, merge, lane, margin, and distinction against the source spec.
8. Make one targeted correction when text, causality, or clipping is wrong, then inspect again. Do not call an inaccurate diagram finished.
9. Return the image and, for project-bound work, its saved path.

## Intake gate

Proceed without asking when the request provides both:

- what the diagram must explain; and
- the main steps, components, or relationships.

If either is missing, ask exactly one concise question and stop generation until answered:

> What should the diagram explain, and what are the main steps or components and how do they connect?

Do not ask about style, palette, or dimensions unless the user explicitly needs a non-default treatment. Use the defaults in `SCALE.md` for those choices.

## Non-negotiable rules

- Preserve causal truth. An attractive wrong arrow is a failed output.
- Use the user's exact technical names and verbatim copy.
- Show state changes, joins, feedback loops, and frozen versus trainable parts explicitly.
- Keep the whiteboard human: loose marker strokes, imperfect arrows, terse labels, and small explanatory doodles.
- Keep the information disciplined: no fake UI, decorative cards, gradients, glows, shadows, icon tiles, background grids, or ornamental clutter.
- Assign color by meaning, not decoration. Default to black structure, blue flow, and one red emphasis for the learned or critical component.
- Keep all live content clear of the canvas edge. Nothing may be clipped.
- Never hide missing information behind generic labels such as "process," "data," or "AI magic."
- Never claim generation succeeded without inspecting the produced image.

## Output contract

The final answer must include:

- the generated diagram;
- a one-sentence description of what it explains; and
- the saved path when the image belongs to a project or repository.

Do not expose the full internal prompt unless the user requests it.
