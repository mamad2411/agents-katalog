---
name: keyframes
description: Use when writing image-generation prompts (ChatGPT / GPT Image, Midjourney, Flux, Gemini, Seedream) for film stills - a cinematic cold open, storyboard frames, a cast line-up or character sheet, start and end frames for video models - where the same characters, style and object must hold shot after shot. Also use when stills look like generic AI illustration instead of a film frame, characters drift between shots, hands or anatomy go wrong, heights are off, or a real product object has to appear in the shots.
---

# keyframes

The stills are the film. Image-to-video models mostly animate their first frame, so look, faces, light and
composition are decided here. Work in one chat with the image model, one message at a time, references attached.
Model notes: `references/models/` (gpt-image, midjourney, flux, nano-banana, seedream). Style blocks:
`references/styles.md`. A full master prompt to copy: `references/master-prompt.md`.

## The master prompt (one per chat)

1. **What this is**: "Stills for a short film. I animate them afterwards."
2. **STYLE (every image)**: a style block from `references/styles.md`. Name real reference works and what each one
   brings, then the rules that make it read as a frame from that medium (for photoreal: real optics, natural light
   sources, deep blacks, film grain, nothing illustrated).
3. **THE CAST**, numbered, each tied to its reference images, with role, hair, face, outfit, colours, prop and a
   **height relative to the others**. "Redraw every reference into the one style so they belong in the same film."
4. **THE OBJECT**: the real product render attached. In wide shots small and glowing, text not drawn; in close shots
   colours, border and art matched, lettering soft or hidden by light. Never invented writing.
5. **STEP 1: the line-up.** Everyone side by side, full body, plain background, correct heights. "Generate it, then
   stop and wait for me." Every later shot copies this image, so fix the style here.
6. **STEP 2: the shots**, one per message when asked, under **COMPOSITION RULES**: film frames, not group
   portraits; nobody lined up, nobody looking at camera, no neutral poses; different depths and heights, overlapping,
   most partly cropped; one focal point lit hardest, the rest in shadow or blur; 2.39:1 letterbox inside 16:9.

## A shot

Camera first (lens, height, angle), then **foreground / midground / background**, each with who, pose, action and
light; atmosphere and mood in one line. Write what is seen, not what it means.

## Frames that video models need

- **The move in three frames.** For a clip that must end somewhere exact (the object flat to camera), ask for the
  same moment three times: start (edge-on), middle (half turned), end (flat). They become first, intermediate and
  last frames in `clip-prompts`.
- **Cut frames.** A reaction close-up and a lunge toward camera let a film cut from a wide to an overhead without
  asking a video model to invent the move.
- **Same camera, two moments** for any first and last frame pair. A big angle change between them causes morphs.

## Working the chat

- **Three versions of each shot**, so the person picks instead of re-rolling.
- **Fixes are short, named and local**: "her right hand is backwards: palm toward the card, thumb inside";
  "buttons on the front of the coat only"; "two white stripes down each sleeve". Never re-describe the whole shot.
- **Drift** after several shots: start a fresh chat with the master prompt and the approved line-up and the best
  shot attached, and continue there.
- **Rejected style** ("looks like an AI illustration, not a film"): fix the line-up with a style correction, not the shots.
