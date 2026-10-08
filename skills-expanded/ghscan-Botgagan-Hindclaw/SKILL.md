---
name: openrouter-image
description: Generate images through OpenRouter (Google Gemini image models) from approved prompts. Use when the workflow reaches image generation and you must use OPENROUTER_API_KEY instead of native OpenClaw image providers.
---

# OpenRouter Image

Generate images from approved prompts using OpenRouter-compatible Gemini image models.

## Use this workflow

1. Confirm the prompt is approved.
2. Run:

```bash
node skills/openrouter-image/scripts/generate_openrouter_image.mjs --prompt "<APPROVED_PROMPT>" --aspect-ratio "1:1"
```

3. Read the JSON output and capture:
   - `image_path`
   - `model`
4. Reply with a short user-facing confirmation only (for example: "Image generated successfully and ready for review.").
5. Do not expose `image_path`, `absolute_path`, raw JSON, or command/debug details in user-facing chat.

## Optional parameters

- `--model "google/gemini-2.5-flash-image"` (default)
- `--aspect-ratio "1:1"` (or `9:16`, `16:9`, etc.)
- `--image-size "1K"` (or `2K`, `4K`)
- `--output-dir "generated/images"`

## Notes

- The script reads API key in this order:
  1. `OPENROUTER_API_KEY` env var
  2. `~/.openclaw/agents/social-media/agent/auth-profiles.json` (`openrouter:default`)
- Do not print API keys in chat.
