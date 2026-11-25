---
name: mage-refine
description: |
  Make one focused improvement to an existing image with Mage, keeping the
  subject, pose, light, and composition: the Refine app as a skill, with its
  three presets (fix eyes, fix hands, add detail) or the user's own
  instruction, on Mango 4 by default. Use when: "refine this image", "fix the
  eyes", "fix the hands", "fix the fingers", "add more detail", "sharpen the
  texture", "clean this up without changing it", "small improvement to this
  image". NOT for: changing one masked area only (mage-inpaint), new lighting
  (mage-relight), a new camera angle (mage-angles), a new composition or
  subject (mage-generate), or swaps (mage-face-swap, mage-outfit-swap).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Refine

Improve an image without recomposing it: fix eyes, fix hands, add detail, or follow one instruction of the user's. This is the [Refine app](https://www.mage.space/apps/refine) as a skill: the same presets and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **The image** to refine.
2. **What to improve:** one of the presets, or the user's own instruction. If the request doesn't say, ask which.

## Settings

- Model: Mango 4 (`mango`, `model_id: "mango-v4"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask.

## Prompt

Pick the preset that matches the request and send its prompt exactly:

| Preset | Prompt |
|---|---|
| Fix Eyes | Fix the eyes so they look natural, aligned, expressive, and detailed. Preserve the subject identity, face, pose, lighting, style, clothing, background, and overall composition. |
| Fix Hands | Fix the hands and fingers so they look anatomically correct, natural, and detailed. Preserve the subject identity, pose, lighting, style, clothing, background, and overall composition. |
| Add Detail | Add crisp natural detail and improve texture clarity throughout the image. Preserve the subject identity, pose, lighting, style, clothing, background, and overall composition. |

For anything else, send the user's instruction as the app does: their own sentence, without the link or the request around it, and with nothing added. A change to one object ("Make the coffee cup blue.") runs here too. If it is vague ("make it better"), ask what should improve.

## Run

```json
{
  "model_id": "mango-v4",
  "resolution": "2K",
  "aspect_ratio": "<closest to the image>",
  "image": "<the image>",
  "prompt": "<preset prompt or the user's instruction>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

## Check and deliver

If you can see the result, compare it with the original: the named flaw is fixed and nothing else moved. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver the link.

Refine works across the whole image and improves execution only. When everything outside one area must stay untouched, use `mage-inpaint`; for a subject that came out wrong or a new framing, generate again with `mage-generate`. Each accepted result can be the image for the next refinement.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

## References

- `references/models.md`: every model the app offers for this, with ids and resolutions.
