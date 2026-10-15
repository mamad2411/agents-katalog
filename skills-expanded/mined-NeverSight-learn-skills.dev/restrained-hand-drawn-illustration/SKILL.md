---
name: restrained-hand-drawn-illustration
description: Create or transform a supplied photo, image, or written brief into a small, playful hand-drawn vignette with tactile variable-width black crayon, graphite, or ink linework, a pale background, generous blank space, extremely sparse low-saturation color, and optional handwritten lettering or subtle GIF animation. Use whenever a user requests a tiny humorous hand-drawn illustration, quiet doodle, expressive rough black outlines, reference-informed hand-drawn visual system, same-as-source-aspect-ratio JPG, or simple animated GIF in this visual direction.
---

# Restrained Hand-Drawn Illustration

Create an original small, playful illustration in the visual system defined in [style-system.md](references/style-system.md). Treat the supplied references as constraints, not source material to copy: never copy distinctive characters, exact compositions, logos, or readable text.

## Route the request

Classify each supplied image before making anything:

| Input role | Goal | Preserve |
| --- | --- | --- |
| Edit target | Reinterpret the actual photo/object | subject identity, decisive pose, clothing/product cues, and aspect ratio |
| Visual reference | Learn visual constraints only | no literal objects, layout, text, or distinctive character design |
| Supporting insert | Incorporate a named object or texture | only the requested recognisable detail |

Choose one route:

1. **Generate** — brief or concept to illustration.
2. **Photo/image transform** — redraw a supplied target in the system while retaining the agreed essentials.
3. **Reference analysis** — report fixed rules, variables, and a reusable prompt; do not generate unless asked.
4. **Prompt-only** — return the compiled prompt, production recipe, and output specification only.
5. **Animate** — make a short looping GIF from a generated or supplied still, selecting motion from [motion-system.md](references/motion-system.md).

Ask one concise question only if the missing information materially changes the output: whether a supplied image is a target or reference, required ratio when no source exists, exact handwritten text, or requested animation intent. Otherwise use the defaults below.

## Defaults and output contract

- Preserve the supplied target image's width:height ratio exactly. If there is no target, default to a 1:1 square.
- Render at least 1536 px on the long edge (or the user's requested dimensions); the drawing normally occupies only 20–45% of the canvas and leaves generous empty space.
- Deliver the final still as an RGB **JPG**. Convert losslessly generated PNG/WebP results with `scripts/export_raster.py` only after visual approval.
- For animation, deliver a looping **GIF** at the still's aspect ratio, normally 3–5 seconds, 8–12 fps, 12–36 frames. Use only a small, meaningful loop rather than continuous busy motion.
- If lettering is requested, keep it short (normally 1–6 words). Handwrite it as a drawn shape; do not rely on an invented font or claim exact spelling when it is not legible. For brand-critical or longer text, typeset/letter it in a separate post-processing pass and confirm the final spelling.

## Production workflow

1. **Find the tiny joke.** Reduce the brief to one small visual surprise: an object doing one unexpected thing, a tiny character reacting, or one playful exchange. Limit the cast to 1–2 subjects and 0–2 supporting marks. Do not make an establishing shot.
2. **Lock the scale.** Read [style-system.md](references/style-system.md). Place the vignette inside a compact visual footprint with 55–80% of the canvas blank. A requested large object is still drawn simply; do not turn it into a grand scene, poster, cityscape, or technical diagram unless the user explicitly overrides this rule.
3. **Select the line profile.** Read [line-profiles.md](references/line-profiles.md). Choose one profile rather than averaging the references. Default to `soft-crayon-outline` for character/object vignettes; use `fine-gesture` only when the brief calls for airy, delicate marks. State the profile explicitly in the prompt.
4. **Select the recipe.** Build the form from a few broad, tactile, intentionally open contour strokes plus a smaller number of thin gesture marks. Each visible stroke needs a natural pressure path: light start, fuller middle, eased or lifted end. Leave 1–3 meaningful breaks where an edge turns away, overlaps another form, or does not need explanation; never seal every object into a complete outline. Add one muted flat accent only when it carries the joke or makes the subject readable.
5. **Compile the prompt.** Use [prompt-compiler.md](references/prompt-compiler.md). State the required aspect ratio, compact subject footprint, selected line profile, and prohibited scene scale. For an edit target, state what must be retained and what may be simplified.
6. **Generate and inspect.** Use the image-generation capability with the actual edit target attached when applicable. Inspect at full frame: tactile line-weight hierarchy, soft but decisive contours, visual smile/curiosity, sparse color, small vignette scale, large pale negative space, no accidental lettering, and no copied reference residue. Regenerate or revise when any gate fails.
7. **Finish still output.** Convert the approved result to JPG with `scripts/export_raster.py jpg INPUT OUTPUT`. Verify the output dimensions match the intended ratio.
8. **Animate only when requested.** Define a tiny loopable motion in words, then create consistent frames or controlled layer movement. Read [motion-system.md](references/motion-system.md), inspect beginning/end continuity, and compile with `scripts/export_raster.py gif`. Do not animate every element.

## Quality gate

Reject and retry when the result has any of these: poster-scale or full-frame subject; realistic city/landscape; cinematic establishing shot; technical rendering; a single uniform line width; blunt cut-off stroke ends; fully sealed contour on every form; hairline sketch marks used for the silhouette; scratchy repeated outlines; hard geometric joins; polished vector uniformity; thick cartoon outlines with perfectly smooth edges; mechanically regular spokes/repetition; exact radial symmetry; more than two color accents; saturated/neon color; dark or busy background; realistic shading; dense scenery; decorative clutter; copied wording, logo, character, or composition; rigid symmetry without a small joke; unreadable required text; or motion that jitters, flickers, or does not loop cleanly.

Before delivery, state: input role, retained elements (when transforming), chosen palette, output dimensions/ratio, and—if applicable—the GIF loop action and duration. Attach only the requested final format(s), not intermediate explorations unless asked.
