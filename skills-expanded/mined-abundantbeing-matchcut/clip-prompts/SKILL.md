---
name: clip-prompts
description: Use when writing image-to-video or text-to-video prompts for MiniMax Hailuo, Grok Imagine, Seedance, Veo, Kling, Wan, Runway, Luma Ray or LTX - animating film stills into clips, using first, intermediate and last frames, keeping named characters and a product object consistent, or planning clip lengths for an edit. Also use when clips grow extra arms or limbs, duplicate a character, melt between angles, make an object follow a character, warp text, ignore the story, or run the wrong length.
---

# clip-prompts

Video models remember nothing between clips and know nothing about your characters. Each generation sees one
image (or a first and last frame, or references) and one prompt. So every prompt carries the whole story, ties
every name to what that character looks like, and says exactly what moves.

Per-model notes (modes, lengths, syntax, failure modes, sources): `references/models/` for minimax, grok,
seedance, veo, kling, wan, runway, luma and ltx. Read the one for the model in use before writing. A full
three-clip example: `references/templates.md`.

## The prompt block

```
STORY: One shot from a short [cinematic] film. [Who they are, what just happened, what happens next.] Mood: [one word].
Style: [medium], cinematic 2.39:1 letterbox, [palette]. Keep every character exactly as drawn in the first frame.
THIS SHOT (n of N), [shot name and angle]. [NAME], [role]: [hair, face, outfit, colours, prop], at [left/centre/right].
ACTION: [what moves, in order, with time in words: "for the first half...", "in the last second..."]
LOCKED: [counts and constraints: exactly three characters, each appears once; the glove keeps five fingers;
the card keeps its shape]
CAMERA: [one move]. One continuous shot, no cuts, no text.
```

Names alone do nothing. "KAI, spiky green hair, red angular visor, dark green jacket, at centre" does. Some models
want a different shape (Seedance: labelled shots and `@Image 1` tags; Veo: a paragraph with audio cues); the model
file says so.

## Lengths

- Generate at the model's shortest length that holds the action (often 5 or 6 s) and **trim in the edit**. Plan the
  film in kept seconds.
- Problems often appear late in a clip. Check whether a flaw is inside the seconds you keep before regenerating.
- Speed-ramp in the editor rather than regenerating for timing.

## Frames

| Mode | Use it for | Avoid |
|---|---|---|
| Single image | Most shots. The model moves a little from the still | Asking for a big camera change |
| First + last frame | One move between two frames from the same camera angle | A wide to an overhead: the model invents the move and morphs |
| First + middle + last | One continuous move with a known path (an object turning to camera) | Mixing different moments |
| Reference images | Keeping a character or object across shots (models that support it) | Too many references at once |

One generation, one move. End a generation where the next one's first frame begins.

## Fixes that work

| Problem | Fix |
|---|---|
| An extra arm or hand appears | The model is inventing a limb the still never showed. Crop it out in the edit (scale 115 to 120%, keyframed in), trim before it appears, or crop the last frame so that character leaves the shot. Add "his other arm is never shown; no hand ever appears at the bottom of the frame" |
| A character appears twice | "exactly N characters, each appears once"; drop a wide last frame that forces the model to re-place everyone |
| An object follows a character | "the card stays above his hand and never moves sideways or follows him"; never interpolate between angles |
| Bodies melt between angles | Two single-image clips and a cut on motion, on a hand filling the lens, or on a flash of light |
| Text on an object warps | "keep the design, lettering and proportions exactly as in the first frame"; end on a held still of the real object; a match cut covers the last frames |
| The model ignores a long prompt | Keep ACTION, LOCKED and CAMERA only; the image carries the rest |
| Everything moves at once | One action per clip; list secondary motion (hair, embers) as background |

## Cutting

- Cut on a flash, on something filling the lens, or on fast motion: each hides an angle change.
- The last cold-open clip ends on the hero object flat and still for half a second: that frame is the match cut.
- Run the same still and prompt on two models and pick per shot, not per model.
