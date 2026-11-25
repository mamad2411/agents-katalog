---
name: gpt-images
description: "Turns a plain-language brief into a production-ready prompt for OpenAI GPT Image models (ChatGPT Images 2.5, gpt-image-2.5-flare, gpt-image-2.5-sunburst, gpt-image-2). Returns a seven-block prompt, a settings block for the chosen surface, and three concrete levers for the next iteration. Covers text inside the image, reference binding, edits that do not drift, transparent backgrounds, and the hard API limits on size, quality and input images. Triggers: 'write an image prompt', 'gpt image prompt', 'chatgpt images 2.5', 'make me a poster', 'product shot prompt', 'article cover image', 'edit this image without changing X', 'transparent background logo', 'why does my text come out garbled', 'my edits keep drifting'. Not for video models (they use different syntax) and not for typography that must be pixel-exact."
license: MIT
---

# GPT Images

Input: a brief in plain language, one sentence is enough. Output: an English prompt ready to paste, a settings block for the chosen surface, and two or three levers that actually change the result.

`v1.0.0`. Self-contained: this skill does not depend on any other skill being installed.

**Generate nothing on your own.** Image generation costs the operator money. Produce the prompt, then ask.

Hard numbers (model IDs, sizes, quality levels, prices, limits) live in `references/official-spec.md`. Never quote them from memory, read the file.

## Step 0: pick the surface

Always first. Without a surface there is no settings block.

| Surface | When | What you deliver |
|---|---|---|
| **ChatGPT app** (default when nothing else is said) | manual work, iteration, sketch input, built-in templates | the prompt in plain language, no API parameters |
| **OpenAI API** (`v1/images/generations`, `/edits`, or the Responses API tool) | scripts, pipelines, transparent backgrounds, exact pixel sizes | prompt plus `model`, `size`, `quality`, `background`, `output_format` |
| **Third-party hosted surface** | a platform that resells GPT Image models | prompt plus whatever that platform's live catalog exposes. Check the catalog, do not assume it matches the API |

## Step 1: intake, five things

1. **Purpose and channel.** This decides the size. A social post, an article cover and a print poster are three different jobs.
2. **Subject.** What is actually in the frame. If a specific person or product must be recognizable, you need a reference image.
3. **Text inside the image.** Verbatim, in quotes. Not a paraphrase.
4. **Mode.** Photorealistic photo, flat design, illustration, 3D render, UI mockup. This decides half the prompt.
5. **Exclusions.** Third-party logos, watermarks, stock-photo look, extra text.

Missing input is not a reason to stop. Fill it in, mark it `[ASSUMED]`, and keep going. An empty form handed back to the operator is a failure.

## Step 2: model and quality

- **`gpt-image-2.5-flare`** is the default. Faster, made for everyday and high-volume work.
- **`gpt-image-2.5-sunburst`** when the job is a campaign, a series in one style, or several rounds of edits on one image.
- **`quality`**: `low` while hunting for a direction, `high` for anything containing text, `xhigh` or `max` for dense typography and information panels (2.5 only).
- Above `2560x1440` behavior gets variable. For 4K deliverables, generate at 2K and upscale with a dedicated tool.

## Step 3: prompt anatomy, seven blocks

Write in English. Copy that must appear inside the image stays verbatim in quotes, in whatever language it belongs to. Short labeled blocks, not one long paragraph.

```
USE: <what it is for, one line: "LinkedIn article cover, 1920x1080">
SUBJECT: <who or what, materials, shapes, textures>
SCENE: <environment, background, atmosphere>
COMPOSITION: <framing, angle, placement of elements, negative space>
LIGHT & STYLE: <lighting, medium: photorealistic / flat vector / 3D render / editorial collage>
TEXT: "<verbatim text>" - <placement, size, type style>
AVOID: <what must not appear>
```

The rules this stands on:

- **Photorealism is requested, not assumed.** Write `photorealistic` and add real texture: pores, fine lines, fabric wear. Words implying a polished studio setup kill it.
- **In-image text goes in quotes or ALL CAPS.** Spell hard words letter by letter and demand `verbatim rendering, no extra characters`.
- **Placement is stated, not implied.** `logo top-right`, `subject centered, negative space on the left third`.
- **Quality levers only when needed.** `film grain`, `macro detail`, `textured brushstrokes`. Not all at once.
- **Specific camera bodies and lenses are read loosely.** Use them for the overall look, not as optical simulation.

Per-format templates are in `references/recipes.md`. Failure modes and their fixes are in `references/prompt-anatomy.md`.

## Step 4: references

Number every input image and give it a role:

```
Image 1: product photo - keep the bottle shape, label and colors exactly.
Image 2: style reference - take only lighting and color grading, ignore its subject.
Apply Image 2's style to Image 1. Do not copy any object from Image 2.
```

The edits endpoint accepts up to 16 input images at 50 MB each. Hosted surfaces usually allow fewer, so check before you promise it.

## Step 5: editing an existing image

A different discipline from generation. The rule: **one change per round, plus a preserve list repeated every single round.**

```
Change only: <one thing>
Keep unchanged: face, body shape, pose, hair, expression, background, framing,
camera angle, lighting, color grading, layout, all existing text.
Do not change saturation or contrast. No new elements. No watermark.
```

When results drift round after round, do not write a longer prompt. Go back to a clean base and continue with small single-step edits.

Do not use generation for pixel-preserving work. Sharpness, canvas extension, single-region retouch and cropping all have dedicated tools that keep the rest of the image untouched. Reaching for a full regeneration is how people lose a good image.

## Step 6: what you hand over

Always in this order:

1. **The prompt** in a code block, complete, one copy action.
2. **The settings block** for the chosen surface, valid values only.
3. **Three levers** for when the first result misses. Concrete ones, not "try again differently".
4. **An offer to generate.** Never generate unprompted.

After the image exists:

- **Proofread any image containing text.** Read it band by band: typos, clipped diacritics, broken alignment, wrong facts. Models render text that looks right at a glance and is wrong on the third word.
- **Label AI-generated content where disclosure applies.** In the EU, the AI Act's transparency duty for synthetic image, audio and video content applies from 2 August 2026, and it bites hardest when the output depicts a real person, place, product or event. Check what applies to the operator's jurisdiction and use case.

## Boundaries

- **Typography that must be exact does not belong in the model.** Fonts get approximated and letterforms drift. Either describe the shape (`bold condensed geometric sans, all caps`) or generate the imagery here and set the type in a real layout tool.
- **Video models are a different world.** Their reference syntax, shot structure and audio handling do not transfer. Do not mix them into an image prompt.
- **Analyzing an existing visual** is the reverse direction: image in, description out. This skill goes brief in, prompt out.
