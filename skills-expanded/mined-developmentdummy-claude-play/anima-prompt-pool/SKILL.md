---
name: anima-prompt-pool
description: Build external prompt pools for Anima-based source generation. Use when creating many Anima prompts for later batch generation, especially when prompts must be saved in a stable JSON-friendly format with ids, categories, notes, subject tags, and natural-language scene text.
---

# Anima Prompt Pool

## Overview

Create prompt-bank entries that are easy to append into the batch pipeline later.
Write prompts for Anima source generation, not for the Illustrious teacher pass.

## Core Rules

- Use `subject_tags + scene_prompt` as the canonical format.
- `subject_tags` holds visible anchors in tag form.
- `scene_prompt` holds the main natural-language scene description.
- Optimize for batch consistency, not literary flair.
- Keep one entry focused on one scene idea.
- If an outfit, lighting, or camera angle matters, state it explicitly.

## Output Format

Default to this JSON object format:

```json
{
  "id": "p001",
  "category": ["office", "professional", "glasses"],
  "exposure": "clothed",
  "subject_tags": "1girl, solo, dark navy hair, long hair, teal eyes, pale skin, thin silver-rim glasses, white research blouse with rolled-up sleeves, dark navy vest, black pencil skirt, black tights, sitting at desk, legs crossed, soft skin, cool blue tones, monitor glow, upper body",
  "scene_prompt": "An adult woman with long dark navy hair and teal eyes is sitting at a sleek modern office desk, wearing a white research blouse with rolled-up sleeves over a dark navy vest and black pencil skirt with black tights. She has thin silver-rimmed glasses and is focusing on a holographic display. The scene is lit by cool blue screen glow and soft ambient office lights. The image should feel professional and focused, with sharp suit textures and polished glass surfaces.",
  "negative_prompt": "multiple girls, 2girls, extra person, crowd, people in background",
  "notes": "Optional short note about intent or risk."
}
```

### exposure field

`exposure` classifies the scene's nudity level. This drives which body/exposure tags MUST appear in `subject_tags` and ensures caption–image consistency for LoRA training.

| exposure | Definition | Required tags (subject_tags) | Forbidden tags (subject_tags) |
|----------|-----------|------------------------------|-------------------------------|
| `clothed` | Fully dressed, no sexual parts visible | Explicit clothing items (`white blouse`, `black skirt`, etc.), `clothed` | `nude`, `nipples`, `pussy`, `bare_breasts`, `topless` |
| `partial` | Partially exposed — underwear visible, cleavage, sideboob, lifted skirt, see-through, etc. | Specific exposure state (`cleavage`, `black lace bra`, `unbuttoned shirt`, `sideboob`, `lifted skirt`, `panties visible`, etc.) | `nude`, `fully_clothed` |
| `nude` | Fully nude or near-nude, sexual parts directly visible | `nude` or `topless`, plus visible anatomy (`nipples`, `navel`, `bare_breasts`, `pussy`, etc. as applicable to the composition) | `clothed`, `covered_nipples`, `fully_clothed` |

**Rules:**
- Every prompt MUST have an `exposure` field. No default — force explicit classification.
- The tags in `subject_tags` MUST be consistent with the declared `exposure`. If `exposure` is `clothed`, do not include `nipples`. If `exposure` is `nude`, do not include `clothed`.
- For `partial`, specify exactly what is exposed and what remains covered. Ambiguity here causes the worst training noise.
- `exposure` value is also carried into `category` automatically for filtering (e.g., `["bedroom", "nude"]`).

### negative_prompt field

- `negative_prompt` is optional per-item. If omitted, the pipeline uses the global default from `pipeline_meta.json` (`source_default_negative` / `teacher_default_negative`).
- Use per-item negatives only when a scene needs **extra** suppression beyond the global default (e.g., a crowded street scene that tends to spawn extra characters, or a mirror scene that generates duplicates).
- Common per-item negatives:
  - Crowded environments: `multiple girls, 2girls, extra person, crowd, people in background`
  - Mirror/reflection scenes: `duplicate, clone, symmetry, reflection`
  - Indoor scenes with windows: `extra person, crowd, people in background`
- Do **not** duplicate quality negatives (`worst quality, low quality`) here — those are already in the global default.
- For multi-character scenes (2girls etc.), **remove** the anti-multi tags from negative: `"negative_prompt": ""` to override the global default.

When asked for many prompts, output a JSON array of those objects.

Legacy compatibility:

- old `prompt` single-field format may still exist
- but new pools should default to `subject_tags + scene_prompt`

## Real File Example

Use a `prompt-bank.json` file like this:

```json
[
  {
    "id": "p001",
    "category": ["office", "professional", "glasses", "clothed"],
    "exposure": "clothed",
    "subject_tags": "1girl, solo, dark navy hair, long hair, teal eyes, pale skin, thin silver-rim glasses, white research blouse with rolled-up sleeves, dark navy vest, black pencil skirt, black tights, sitting at desk, legs crossed, clothed, soft skin, cool blue tones, monitor glow, upper body",
    "scene_prompt": "An adult woman with long dark navy hair and teal eyes is sitting at a sleek modern office desk, wearing a white research blouse with rolled-up sleeves layered under a dark navy vest, paired with a black pencil skirt and black tights. She wears thin silver-rimmed glasses. She is focusing on a holographic display. The scene is lit by cool blue screen glow and soft ambient office lights. The image should feel professional and focused, with sharp suit textures and polished glass surfaces.",
    "notes": "Good for polished interior surfaces."
  },
  {
    "id": "p002",
    "category": ["nature", "forest", "ethereal", "clothed"],
    "exposure": "clothed",
    "subject_tags": "1girl, solo, dark navy hair, long hair, teal eyes, pale skin, white cotton sundress, thin shoulder straps, barefoot, walking, clothed, soft skin, warm tones, dappled sunlight, full body",
    "scene_prompt": "An adult woman with long dark navy hair and teal eyes is walking through a sun-drenched forest, wearing a white cotton sundress with thin shoulder straps. She is barefoot on the mossy ground. The scene is lit by warm dapples of sunlight filtering through the canopy of ancient mossy trees with floating pollen. The image should feel ethereal and serene, with soft fabric movement and detailed leaf textures.",
    "notes": "Good for soft natural light."
  },
  {
    "id": "p003",
    "category": ["bedroom", "intimate", "partial"],
    "exposure": "partial",
    "subject_tags": "1girl, solo, dark navy hair, long hair, teal eyes, pale skin, unbuttoned white dress shirt, black lace bra visible, cleavage, bare legs, sitting on bed edge, leaning back on hands, soft skin, warm tones, dim lamp light, full body",
    "scene_prompt": "An adult woman with long dark navy hair and teal eyes is sitting on the edge of a bed, wearing an unbuttoned white dress shirt that reveals a black lace bra underneath. Her legs are bare. She is leaning back on her hands with a relaxed expression. The scene is lit by warm dim lamp light from a bedside table. The image should feel intimate and natural, with soft fabric folds and warm skin tones.",
    "notes": "Partial exposure — bra visible through unbuttoned shirt."
  },
  {
    "id": "p004",
    "category": ["bathroom", "morning", "nude"],
    "exposure": "nude",
    "subject_tags": "1girl, solo, dark navy hair, long hair, wet hair, teal eyes, pale skin, nude, bare breasts, nipples, navel, standing, holding towel at side, wet skin, water droplets, soft skin, warm tones, soft morning light, full body",
    "scene_prompt": "An adult woman with long dark navy hair (wet and clinging to her shoulders) and teal eyes is standing nude in a steamy bathroom, holding a white towel casually at her side. Water droplets glisten on her pale skin. The scene is lit by soft warm morning light coming through a frosted window. The image should feel natural and candid, with realistic water droplet textures and steam diffusion.",
    "notes": "Full nude — all relevant anatomy tags included."
  }
]
```

Use a `review-queue.json` file like this:

```json
[
  {
    "id": "p001",
    "status": "pending",
    "source_image": "images/source/p001.png",
    "teacher_image": "images/teacher/p001.png",
    "subject_tags": "1girl, solo, long navy hair, silver-rimmed glasses, white research blouse, dark navy vest, black pleated skirt",
    "scene_prompt": "An adult woman is sitting at a sleek modern office desk, focusing on a holographic display. The scene is lit by cool blue screen glow and soft ambient office lights. The image should feel professional and focused, with sharp suit textures and polished glass surfaces.",
    "category": ["office", "professional", "glasses"],
    "notes": "Good for polished interior surfaces."
  }
]
```

Recommended status values:

- `pending` — not reviewed yet
- `yes` — approved for dataset
- `no` — rejected
- `hold` — keep for later review

## Prompt Construction Workflow

For each prompt:

1. Choose one clear scene family
   - neon city
   - luxury interior
   - futuristic stage
   - bedroom
   - bathroom
   - office
   - fantasy tavern

2. Build `subject_tags` with all six axes filled
   subject_tags is used BOTH for Anima source generation AND as the Illustrious teacher prompt (without natural language). It must be rich enough for the teacher to render the scene correctly on its own.

   **Required axes (always include all six):**

   | Axis | Examples | Why |
   |------|---------|-----|
   | **Character identity** | `1girl, solo, dark navy hair, long hair, teal eyes, pale skin` | Teacher doesn't know the character otherwise |
   | **Outfit / exposure** | `white sundress, barefoot, clothed` or `nude, bare breasts, nipples` or `unbuttoned shirt, black lace bra visible, cleavage` — **must match the `exposure` field** | Ambiguous nudity level causes rendering errors AND training noise |
   | **Pose / anatomy** | `standing, arms at sides` or `on back, lying on bed, knees up, navel` | Prevents body distortion, especially in lying/crouching poses |
   | **Skin / texture state** | `soft skin` or `sweating, wet skin` or `oiled skin, sweat droplets` | Directly affects erotic scene quality |
   | **Color / lighting tone** | `warm tones, golden light` or `cool blue tones, dim lighting` or `high contrast, neon glow` | Anchors the teacher's color grading direction |
   | **Composition** | `upper body` or `full body` or `close-up, face focus` | Prevents framing mismatch between source and teacher |

   **Example — bedroom nude (exposure: "nude"):**
   ```
   1girl, solo, dark navy hair, long hair, teal eyes, pale skin, nude, bare breasts, nipples, navel, flat stomach, on back, lying on bed, arms above head, soft skin, messy hair, warm tones, dim lighting, full body
   ```

   **Example — office clothed (exposure: "clothed"):**
   ```
   1girl, solo, dark navy hair, long hair, teal eyes, pale skin, thin silver-rim glasses, white research blouse with rolled-up sleeves, dark navy vest, black pencil skirt, black tights, clothed, sitting at desk, legs crossed, soft skin, cool blue tones, monitor glow, upper body
   ```

   **Example — bedroom partial (exposure: "partial"):**
   ```
   1girl, solo, dark navy hair, long hair, teal eyes, pale skin, oversized white t-shirt, no bra, sideboob, black panties, bare legs, sitting on bed, knees up, soft skin, warm tones, morning light, full body
   ```

3. Write `scene_prompt` as natural language with explicit visual details
   - `scene_prompt`: action, environment, lighting, mood, material richness
   - This is used by Anima only (not teacher), so it can be descriptive prose
   - **MUST explicitly describe**: hair color & style, clothing items with color/material/detail, accessories, footwear
   - The first sentence should establish the character's appearance: *"An adult woman with long dark navy hair and teal eyes is..."*
   - Clothing descriptions should be specific: not just "wearing a dress" but "wearing a white cotton sundress with thin shoulder straps"
   - If exposure is `partial` or `nude`, describe the state of dress/undress naturally in the prose
   - Accessories (glasses, jewelry, hair ties, etc.) should be mentioned if present

4. Decide if per-item negative is needed
   - Most scenes: omit `negative_prompt` (global default handles it)
   - Busy backgrounds (streets, crowds, festivals): add `"negative_prompt": "multiple girls, 2girls, extra person, crowd, people in background"`
   - Multi-character scenes: add `"negative_prompt": ""` to clear the global anti-multi default
   - Mirror/window scenes: add `"negative_prompt": "duplicate, clone, reflection"`

5. Add a short note only if needed
   - good for glossy clothing
   - strong color contrast
   - risk of cluttered background

## Writing Pattern

Use this skeleton:

```text
exposure: [clothed | partial | nude]
subject_tags: [인원], [캐릭터 외형: 머리색, 머리길이, 눈색, 피부], [의상 또는 노출 상태 — exposure와 일치], [포즈/해부학], [피부 질감], [컬러/라이팅 톤], [구도]
scene_prompt: An adult woman with [hair color & style] and [eye color] is [pose/action] in [environment], wearing [specific clothing with color/material/detail OR nude state description]. [Accessories if any]. The scene is lit by [lighting]. The image should feel [mood], with [material/color/composition details].
negative_prompt: (optional, only if scene background is busy or multi-character suppression is needed)
```

**Checklist before submitting a prompt — all seven items present?**
- [ ] `exposure` field set (clothed / partial / nude)
- [ ] Character identity (hair color & style, eyes, skin)
- [ ] Outfit or exposure tags consistent with `exposure` field
- [ ] Pose and anatomy anchors
- [ ] Skin/texture state
- [ ] Color/lighting tone
- [ ] Composition (framing)
- [ ] scene_prompt explicitly describes hair, clothing/nudity, and accessories in natural language

## Constraints

- Prefer prompts that remain readable after batch generation.
- Do not overload every prompt with too many visual ideas.
- Do not write teacher-stage trigger tags here unless explicitly requested.
- Do not convert the whole entry into tags only; keep `scene_prompt` in natural language.
- If the user wants erotic prompts, keep the same structured format and focus on scene clarity.

## If the User Requests Variations

Generate variations by changing only one or two axes:

- environment
- lighting
- outfit material
- color palette
- camera distance

Do not change every axis at once unless the user asks for maximum variety.

## Deliverables

When asked to prepare a pool, provide:

1. A JSON array
2. Optional category summary
3. Optional warnings about prompts likely to fail in batch
