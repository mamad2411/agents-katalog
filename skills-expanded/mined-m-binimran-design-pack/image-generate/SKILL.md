---
name: image-generate
description: Generate images with an AI connector (Nano Banana / Gemini, Higgsfield Soul, or Firefly) using a strong prompt framework, the right model, aspect ratio, and iteration. Use when creating original imagery, concepts, or hero art.
---

# image-generate

Pick the model, write a real prompt, generate, curate, iterate. Record the license.

## Pick the connector/model
- **Nano Banana (Gemini):** fast, multi-reference composition (up to 14), editing, up to 4K - great default.
- **Higgsfield Soul / Flux / Seedream:** photoreal, character consistency, cinematic looks.
- **Adobe Firefly:** when you need commercially-safe training + Adobe ecosystem.
(See `mcp/CONNECTORS.md`. If none is connected, say so - don't fake an image.)

## Prompt framework
Subject + action + setting + style + composition + lighting + colour + mood + camera/lens + quality.
State aspect ratio and any reference images. Be specific; vague prompts give generic output.

## Process
1. Generate a small set (2-4 variations). 2. Curate the strongest. 3. Iterate the prompt (fix hands/text/
   artifacts, adjust comp/colour). 4. Upscale / set final aspect ratio. 5. Record model + license.

## Output
- The chosen image(s) from the connector (confirm they returned), the final prompt, and the model + license note.

## Guardrails
- Don't describe an image as generated unless the connector returned it (truth-telling + `review-gate`).
- Record AI source + usage rights (the `license-guard` hook). Curate and fix - don't ship raw first output.
