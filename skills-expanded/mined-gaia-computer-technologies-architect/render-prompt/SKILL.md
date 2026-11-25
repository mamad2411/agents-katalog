---
name: render-prompt
description: Craft a structured, optimised prompt for AI architectural image tools — subject, style, materials, lighting, camera, atmosphere, plus a targeted negative prompt and cross-view consistency notes. Use when an architect wants a "render prompt", to visualise a concept, or to translate loose design intent into precise image-model instructions. Recommends Midjourney (concept mood) and Google Nano Banana (editing a specific design), teaches cross-tool prompting. Feeds from material-palette and space-feel.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Render Prompt

Craft an optimised architectural render prompt from a design description.

## When to use

When an architect, designer, or homeowner needs an AI image render and wants the prompt to actually produce what they intend. This skill translates loose design intent into a precise, structured prompt that works across image models. It crafts the prompt; it does not generate the image.

The single biggest quality lever is **material specificity** — a named material and finish beats any adjective. The second is describing **light behaviour** (raking, diffused, grazing) rather than mood words. Structure and negatives matter, but those two dominate.

## Input

The user provides a design description. This can be:
- A single sentence: "minimalist concrete house, golden hour"
- A detailed brief: room type, style, materials, mood, time of day
- A reference to a style movement: "Tadao Ando meets Scandinavian warmth"
- An existing render they want to iterate on

## Process

1. **Parse the intent.** Identify: building/room type, style, dominant materials, lighting condition, camera perspective, mood.

2. **Fill gaps with informed defaults.** If the user says "modern kitchen" but doesn't specify lighting, default to soft north-facing daylight — the most flattering for kitchens. Always choose the option that an experienced architectural photographer would choose.

3. **Structure the prompt** using this hierarchy (most to least important for image models):
   - **Subject**: what is being rendered (room type, building type, scale)
   - **Style**: architectural movement or aesthetic direction
   - **Materials**: specific materials, not generic ("white-washed Douglas fir ceiling" not "wood ceiling")
   - **Lighting**: time of day, direction, quality (diffused, raking, golden)
   - **Camera**: eye level, bird's eye, worm's eye, focal length equivalent
   - **Atmosphere**: mood, season, weather, human presence
   - **Technical**: resolution, aspect ratio, rendering style (photorealistic, watercolour, section)

4. **Output the prompt** in two formats:
   - **Full prompt**: detailed, comma-separated, ready to paste
   - **Negative prompt**: what to exclude (distortion, oversaturation, unrealistic scale)

5. **Point them at the right tool.** Recommend Midjourney to explore, Nano Banana to edit and hold a specific design, or a geometry-locked route (ControlNet, an in-CAD renderer) when the render must stay true to a real space or model (see Recommended tools below).

## Domain knowledge

### Lighting conditions by space type
- **Living rooms**: late afternoon west light, warm, long shadows. Or: overcast north light for Scandinavian interiors.
- **Kitchens**: morning east light or soft north light. Avoid direct overhead — it kills material texture.
- **Bathrooms**: soft diffused light, steam atmosphere. Dawn or dusk.
- **Exteriors**: golden hour (low sun, warm) or blue hour (dusk, moody). Midday flattens facades.
- **Bedrooms**: early morning, curtains filtering light. Intimate, not staged.

### Camera perspectives
- **Eye level (1.2m)**: most natural, residential feel. Default for interiors.
- **Seated level (0.9m)**: living rooms, restaurants. Creates intimacy.
- **Elevated (2.5m)**: shows spatial layout. Good for open plans.
- **Worm's eye (0.3m)**: dramatic, emphasises ceiling and volume. Use for double-height spaces.
- **Bird's eye**: aerial exterior views. Requires explicit request.

### Material specificity
Never use generic material names. Translate:
- "wood" → "white oak with matte finish" or "charred Yakisugi cedar" or "reclaimed Douglas fir"
- "stone" → "honed Ceppo di Gré limestone" or "bush-hammered Vals quartzite"
- "concrete" → "board-formed concrete with vertical grain" or "polished microcement in warm grey"
- "metal" → "patinated brass hardware" or "blackened steel window frames" or "brushed stainless"
- "tile" → "Moroccan zellige in sea foam" or "matte white subway with dark grout"

### Style shorthands
When the user references a style, expand it:
- **Japandi**: low furniture, natural materials (oak, linen, stone), muted earth palette, negative space, handmade ceramics
- **Brutalist**: raw concrete, dramatic volumes, angular geometry, raking light, minimal furniture
- **Warm Minimalism**: travertine, bouclé, matte plaster, coffee/mocha palette, soft curves
- **Scandinavian Modern**: light wood (ash, birch), white walls, wool textiles, functional furniture, north light
- **Mediterranean Modern**: lime wash walls, terracotta, olive wood, linen, outdoor-indoor continuity
- **Mid-Century Modern**: walnut, brass, terrazzo, statement lighting, low-slung furniture, warm tones

### Holding the same building across views

Image models keep no 3D model between generations, so "the same building from the south" tends to return a *new* building. To hold a design across views:
- **Reference image / ControlNet** is the only reliable geometry lock. Condition on a massing screenshot, clay render, depth map, or line drawing so the model restyles without moving walls. This is the difference between concept mood and iterating a *specific* scheme.
- **Seed** holds broad composition and volume across small prompt changes on the same model — good for swapping materials or light on one view.
- **Style reference** (a fixed reference image, or a curated 30–60 image board of the practice's own work) holds palette and atmosphere so new views read in one visual language.
- Be honest about the ceiling: for true multi-view consistency of a specific building, you still need the 3D model. Text alone re-rolls.

### Negative prompts: target real defects
Three to five sharp exclusions beat twenty vague ones. The discipline: generate first, look at what actually broke, then exclude *that*. A reliable base for architecture: `distorted perspective, warped lines, impossible geometry, plastic-looking materials, oversaturated, blown highlights, people, cars, text, watermark`. Don't stack fears you haven't seen — every weak negative dilutes the ones doing real work.

### Masking quality problems

AI renders fail in predictable places — warped lines, plastic materials, mangled railings and furniture, impossible geometry in the middle distance. Two ways to deal with it: fix the flaw, or hide it. Reach for *fix* first; use *hide* to compose around what you can't fix.

**Fix it locally — don't re-roll the whole image.**
- **Inpaint / mask the broken region** and regenerate only that (a warped window, an extra floor, a bad reflection). Keeps the good 90%.
- **Instruction edit** (Nano Banana) — "straighten the railing," "remove the figure on the left" — same idea without a manual mask, and it holds the rest of the image.

**Hide it — compositional and photographic cover.** Build these into the prompt from the start:
- **Atmosphere** — fog, haze, dusk / blue hour, low raking sun, rain. Low light and atmosphere forgive detail flaws and swallow a messy background; volumetric light hides a bad middle distance.
- **Shallow depth of field** — an 85mm-equivalent at a wide aperture throws foreground and background soft. Put the one clean element in focus; blur is where AI weakness hides.
- **Foreground occlusion** — a branch, planting, a column, furniture across the frame covers the messy zone and adds depth.
- **Crop tight to a detail** — a material junction, a window reveal, a corner. Details render cleanly; whole buildings invite impossible geometry. Frame the problem out.
- **Night + interior glow** — dark exterior, warm lit windows. You read the glow, not the geometry; darkness masks most flaws.
- **Film treatment** — grain, halation, a film-stock look (Portra / Ektar), slight chromatic aberration. Kills the too-clean "plastic AI" tell and reads as a photograph.
- **Drop photorealism** — a watercolour, sketch, or section-collage output is judged as a concept image, not a photo, so photoreal failures stop mattering.
- **Generate small, then upscale** — a generative upscaler invents plausible micro-detail over softness.

**One integrity line:** masking makes a *concept image* convincing; it does not make the design resolved or the render real. Don't let atmosphere hide an unresolved junction from *you*, and don't pass a masked render to a client as a photograph (see the IP note below).

### Recommended tools

Two tools cover most concept-phase work — tell the architect which to reach for:

- **Midjourney** — the pick for **concept mood, atmosphere, and finding the image** when there's no model yet. Strongest aesthetic; it keeps no 3D model between generations, so it will hallucinate geometry — a moodboard tool, not a way to iterate a specific building. Prompt comma-separated; set `--ar`, add `--style raw` for a photographic (less stylised) look, `--seed N` to hold a composition while you swap materials or light, `--sref <image>` to carry a palette across images.
- **Nano Banana** (Google Gemini image) — the pick for **editing a specific design in plain English** ("swap the cladding to charred timber," "take it to dusk, warm interior light") while keeping *the same building* across views, and for handing it a floor plan or massing that it reads as a real instruction. Fast, cheap, best-in-class edit consistency. Not a replacement for physically based lighting on a final hero image.

**Rule of thumb: Midjourney to find the image, Nano Banana to hold and edit it.** For true geometry lock on your own model, drive a base model with ControlNet / a reference image, or render inside the CAD tool (Veras, D5, Enscape-style).

Everything else — Stable Diffusion + ControlNet for hard geometry lock, real-time sketch tools, in-CAD plugins, upscalers — is mapped in [references/model-notes.md](references/model-notes.md). Tool names date fast; the structure, material, and light discipline above don't.

### Worked example

Design intent: *"warm minimalist kitchen, travertine and oak, morning light."*

```
RENDER PROMPT
warm minimalist kitchen, honed travertine island and splashback, white oak
cabinetry matte finish, warm-grey microcement floor, soft morning east light
raking across the stone, eye level 35mm, quiet and unstyled, photorealistic, 3:2

NEGATIVE PROMPT
plastic materials, oversaturated, blown highlights, warped perspective, clutter, people, text, watermark

PARAMETERS
Aspect ratio: 3:2
Consistency: --seed to iterate this view; reference-image/ControlNet if it must match a real kitchen
Recommended tool: Midjourney to explore → Nano Banana to edit materials/light → ControlNet or an in-CAD renderer on the actual kitchen model to hold its geometry
```

## Output format

```
RENDER PROMPT
─────────────
[Full structured prompt, 40-80 words, comma-separated]

NEGATIVE PROMPT
───────────────
[What to exclude, 10-20 words]

PARAMETERS
──────────
Aspect ratio: [e.g. 16:9, 3:2, 4:5 — always set one; unset ratios distort proportions]
Consistency: [reference-image/ControlNet to hold a specific design; seed to iterate one view]
Recommended tool: [Midjourney to explore · Nano Banana to edit/hold · ControlNet / in-CAD for a real space — see references/model-notes.md]
```

## What you don't do

- Don't generate the image. You craft the prompt.
- Don't suggest styles the user didn't ask for unless filling a clear gap.
- Don't use "beautiful" or "stunning" — these are noise words in image prompts. Be specific.
- Don't output more than one prompt unless the user asks for variations.
- Don't imply a render is buildable. A prompt produces an image, not a design — geometry, code, and specification are not implied by a good picture.
- Flag the IP reality when it matters: under current US Copyright Office guidance (2025), a purely AI-generated image is not copyrightable without meaningful human authorship — relevant before an architect puts one on a competition board or in a proposal.
