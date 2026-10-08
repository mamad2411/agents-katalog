---
name: learn-visual
description: >
  Make a teaching diagram (usually SVG) for one idea, look at it, and fix
  it until the picture actually shows the claim. Use when the user runs
  /learn-visual or /skill:learn-visual, or asks for a figure, diagram,
  SVG, sketch, visualization, or picture of a concept being taught.
license: MIT
metadata:
  author: vasanthsreeram
  version: "1.0"
  source: "Eero Alvar — How I Use AI to Learn Things https://youtu.be/kzcI5F4tGiU"
---

# Learn visual

One idea, one picture. The picture exists so the learner can accept the step — not as decoration.

## Output

Write `.alvar/visuals/<slug>-<n>.svg` (create the folder). Embed or link it in the session file.

Prefer SVG. Use another format only if the harness cannot preview SVG.

## Loop (do not skip)

1. State the claim the picture must make, in one sentence.
2. Draw the smallest picture that makes that claim.
3. **Look at the file** (image/read tool). If you cannot view it, say so and keep the SVG simple enough to audit as text.
4. Fix labels, overlap, wrong arrows, missing units, or a picture that does not match the claim.
5. Look again. Stop after a clean pass, not after the first draft.

## Design

- One claim. No collage of the whole course.
- Large labels. High contrast. No tiny legend the learner needs a second lesson to read.
- If the idea is algebraic, show the objects (arrows, planes, machines), not a screenshot of the equation.
- Do not add decorative gradients, watermarks, or "AI art" backgrounds.

## Failures to catch on the look pass

- Arrow direction disagrees with the prose
- Two symbols for the same object
- 3D that hides the relation
- Cropped text
- A picture of a *different* special case than the one just taught

## After

Tell the learner what to look at first ("the two arrows, then the pairing number"). Do not re-teach the whole node unless they ask.
