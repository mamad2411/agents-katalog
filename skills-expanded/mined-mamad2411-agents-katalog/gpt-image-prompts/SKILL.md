---
name: gpt-image-prompts
disable-model-invocation: true
description: Turn a visual idea into a production-ready prompt and API settings for OpenAI GPT Image models (gpt-image-2).
---

# GPT Image Prompt Generator

Generate prompts for OpenAI GPT Image models, with `gpt-image-2` as the default target. Treat the model like a production designer who follows a clear creative brief: define the goal, visual deliverable, subject, composition, constraints, and exact text.

Primary reference: OpenAI's GPT Image Generation Models Prompting Guide: <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>

## Output

Unless the user asks for another format, return:

1. **Ready-to-use prompt** in a fenced code block.
2. **Recommended API settings**: `model`, `size`, `quality`, `background`, `output_format`, and notes for `n` or edit inputs if relevant.
3. **Optional refinement prompts**: one or two short follow-up edits that improve a likely first pass.

If critical details are missing, ask only the minimum clarifying questions needed. Otherwise, make tasteful assumptions and state them briefly.

## Model defaults and constraints

- **Default model:** `gpt-image-2`.
- **Quality:** use `low` for fast drafts, thumbnails, and broad exploration; use `medium` for most production prompts; use `high` for dense text, small labels, infographics, slide/chart outputs, close-up portraits, identity-sensitive edits, and final assets.
- **Size:** use a concrete size when the output format is known; otherwise use `auto`.
  - Common sizes: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`.
  - `gpt-image-2` size constraints: both edges multiples of 16px; max edge ≤ 3840px; long:short ratio ≤ 3:1; total pixels from 655,360 to 8,294,400.
  - Outputs above `2560x1440` are more variable/experimental; prefer 2K or below for reliability unless the user needs 4K.
- **Background:** `gpt-image-2` does **not** support transparent backgrounds. Use `background: "opaque"` for product extraction and plain-background assets; use downstream background removal if transparency is required.
- **Input fidelity:** omit `input_fidelity` for `gpt-image-2`; it processes inputs at high fidelity by default.
- **Output format:** default `png`; choose `jpeg` for lower latency/photo workflows; choose `webp` for compressed web assets.
- **Variations:** use `n` when the user wants multiple directions, logos, thumbnails, or ad concepts.

## Golden rules

1. **Write a creative brief, not tag soup.** Natural language and labeled sections are better than keyword piles.
2. **Lead with purpose.** Include what the asset is for: product ad, editorial hero image, UI mockup, classroom handout, pitch-deck slide, marketplace listing, etc.
3. **Use a stable prompt order.** Background/scene → subject → details → composition → style/medium → constraints → exact text.
4. **Name the visual medium explicitly.** Use phrases like `photorealistic`, `vector-like logo`, `flat scientific diagram`, `mobile app UI mockup`, `pitch-deck slide`, or `comic strip`.
5. **Specify composition.** Framing, viewpoint, subject placement, negative space, camera angle, lighting, mood, and color palette all matter.
6. **Preserve invariants in edits.** Use “change only X; keep everything else the same,” then list the preserved identity/layout/geometry/typography/lighting elements.
7. **Quote exact text.** Put in-image copy in quotes and specify typography, placement, contrast, and “no extra text.” For hard spellings, spell words letter by letter.
8. **Iterate surgically.** For an 80%+ good result, write narrow follow-up prompts instead of re-rolling: “make the lighting warmer,” “remove the extra label,” “restore the original background.”

## Prompt structure template

Use labeled sections for complex or production prompts:

```text
Create [DELIVERABLE] for [PURPOSE/AUDIENCE].

Scene / background:
[Environment, era, mood, context, world details]

Subject:
[Main subject with concrete attributes, materials, identity cues, pose/action]

Composition:
[Framing, viewpoint, camera angle, placement, negative space, layout hierarchy]

Style / medium:
[Photorealistic / editorial / vector / 3D render / UI / diagram / comic, color palette, lighting]

Text, if any:
Render exactly: "..."
[Typography, size, placement, contrast]

Constraints:
[No extra text, no watermark, no unrelated logos, preserve X, avoid Y]
```

For simple requests, a polished paragraph is enough. For production work, labeled sections are easier to debug and reuse.

## Capability patterns

For guidance specific to the deliverable — photorealism, people and pose, text and infographics, ads, logos, UI mockups, slides and charts, product shots, edits and localization, multi-image compositing, comics — load [`PATTERNS.md`](PATTERNS.md) and apply the sections that match the request.
