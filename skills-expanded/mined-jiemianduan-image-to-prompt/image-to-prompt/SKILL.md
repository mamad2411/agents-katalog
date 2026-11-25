---
name: image-to-prompt
description: Analyze one or more reference images and reconstruct faithful, reusable image-generation prompts in Chinese and English. Use when users want to reverse-engineer, infer, restore, imitate, or write prompts from visual references.
license: MIT
compatibility: Works with Codex and Agent Skills-compatible runtimes. Requires image viewing to analyze local reference images.
metadata:
  author: jiemianduan
  version: "0.1.0"
---

# Image to Prompt

Reconstruct prompts from visible evidence. Describe what can be reproduced, distinguish observation from inference, and never pretend to know the original prompt, seed, model, lens, or generation settings.

## Workflow

1. Confirm that at least one usable image is available. If not, ask the user to upload it.
2. Inspect the image at the highest available detail. For a local file, use the image-viewing tool before analyzing it.
3. Identify the image category: photograph, illustration, anime, 3D render, product image, poster/editorial graphic, UI, architecture/interior, or mixed media.
4. Decompose the image using the analysis order below.
5. Resolve the user's target:
   - Default: produce a model-neutral reconstruction prompt.
   - If a model is named, adapt syntax and parameter suggestions to that model.
   - If the user wants only the prompt, keep analysis brief but still perform it internally.
   - For every image, also produce a complete editable version of the prompt. Keep the standard Chinese and English prompts concrete so they remain usable without editing.
6. Produce the output in the prescribed format.
7. State material uncertainty only when it affects reproducibility.

## Analysis Order

Prioritize high-impact visual facts:

1. **Subject and action** — identity category, count, pose, expression, interaction, clothing, props.
2. **Composition** — orientation, crop, subject placement, symmetry, foreground/midground/background, negative space, viewpoint.
3. **Environment** — location, background elements, weather, time-of-day cues, atmosphere.
4. **Lighting** — direction, softness, contrast, key/fill/rim behavior, practical lights, shadow character.
5. **Color** — dominant palette, accent colors, saturation, temperature, tonal range.
6. **Surface and detail** — materials, texture, depth of field, grain, bloom, motion, reflections.
7. **Visual language** — photographic, cinematic, editorial, commercial, painterly, vector, cel-shaded, clay, CGI, collage, and other observable traits.
8. **Capture/render cues** — plausible shot scale, perspective, focal-length range, rendering method, or post-processing. Mark these as estimates when not directly verifiable.
9. **Text and layout** — transcribe only legible text; describe uncertain text as layout blocks rather than inventing wording.

Use spatially explicit phrases such as “subject in the lower-right third” or “soft backlight from frame left.” Prefer concrete visual properties over vague quality words.

## Fidelity Rules

- Preserve the reference's subject count, spatial relationships, camera angle, crop, lighting direction, palette, and major background geometry.
- Do not add narrative, symbolism, props, logos, text, anatomy, or scenery that is not visible.
- Do not identify a real person from appearance alone. Describe observable physical and styling traits.
- Do not assert an artist, brand, camera, lens, model, LoRA, checkpoint, seed, or parameter unless supplied by the user or visibly documented.
- If style attribution is uncertain, describe the visual characteristics instead of guessing a creator's name.
- Treat focal length, aperture, film stock, render engine, and generation parameters as reproduction suggestions, not recovered facts.
- For unreadable text, write `[unreadable text]` or describe its placement and typographic character.
- For multiple references, identify which traits come from each image and flag contradictions instead of silently blending them.
- Keep the prompt internally consistent. Remove terms that fight the observed image, even if they are fashionable prompt keywords.

## Prompt Construction

Build the main prompt in this order:

`subject → action/pose → environment → composition/viewpoint → lighting → color → materials/detail → medium/style → finish`

Write natural, information-dense phrases. Avoid keyword spam, duplicated adjectives, unsupported “8K/masterpiece” language, and excessive camera jargon.

For model-specific output:

- **Midjourney:** place the natural-language prompt first; add only useful aspect ratio, stylize, chaos, or image-weight suggestions. Never claim exact original values.
- **Stable Diffusion / SDXL / FLUX:** separate positive and negative prompts; suggest dimensions or aspect ratio and optional guidance/steps only when useful. Treat values as starting points.
- **DALL-E or model-neutral:** use coherent natural language with explicit composition and constraints; do not add unsupported command syntax.

## Default Output

Respond in the user's language. Unless the user asks for another format, return:

### 画面拆解

A compact factual summary covering subject, composition, lighting, color, medium/style, and key textures. Mark important estimates with `推测`.

### 中文 Prompt

One polished, copy-ready reconstruction prompt.

### English Prompt

One polished, copy-ready English prompt. Optimize it independently rather than translating word-for-word.

### Negative Prompt

Include only defects and unwanted deviations relevant to this image. Omit this section when the target model does not benefit from negative prompts.

### 建议参数

Give aspect ratio first, then a small number of model-appropriate starting suggestions. Label all inferred settings as recommendations.

### 可编辑变量

Always provide one complete, copy-ready editable prompt rather than a separate list of variable names. Base it on the Chinese prompt and preserve all fixed visual anchors as normal prose.

Choose the number of editable spans according to the image and likely reuse needs; there is no fixed minimum or maximum. Expose meaningful, high-impact elements such as the subject, clothing, action, environment, lighting, palette, material, style, or aspect ratio, while leaving structural details fixed when changing them would destroy the reference's defining composition.

Wrap each editable value directly in full-width brackets `【】`. Put a useful current value inside each bracket so the prompt works immediately without editing, and so the user can replace only the bracketed text. Do not use empty brackets, abstract variable labels, numbered placeholders, or a detached variable list.

Example:

`一位【穿深红色长外套的年轻女性】站在【雨夜的城市街道】上，柔和的【蓝紫色霓虹侧光】从画面左侧照入，保持人物居中的中景构图与潮湿路面反光。`

## Special Cases

- **Poster or graphic design:** separate visual prompt from exact copy. Preserve hierarchy, grid, spacing, typography category, and text placement.
- **UI screenshot:** describe information architecture, layout, component styling, density, color tokens, and interaction states. Do not treat it as a photographic scene.
- **Product image:** prioritize product geometry, material, camera angle, grounding shadow, reflections, backdrop, and commercial lighting.
- **Portrait:** prioritize pose, gaze, crop, facial expression, hair, wardrobe, background separation, and skin-light interaction without inferring identity.
- **Highly stylized image:** describe line quality, shape language, shading method, texture, palette, and composition before using genre labels.
- **Poor-quality or obstructed image:** state the limiting issue and provide a best-effort prompt without inventing hidden details.

## Quality Check

Before responding, verify that:

- The main prompt preserves the reference's dominant visual structure.
- Observations and reproduction suggestions are not presented as the same thing.
- The Chinese and English prompts are both directly usable.
- Every image has a complete editable prompt whose bracketed values are immediately usable defaults.
- The editable prompt uses `【】` only around replaceable values and does not reduce the output to a variable list.
- The negative prompt does not accidentally remove a defining feature.
- The output contains no invented text or falsely precise settings.
