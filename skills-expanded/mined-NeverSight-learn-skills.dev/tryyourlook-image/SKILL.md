---
name: tryyourlook-image
description: Generate images from text prompts or edit one image through the TryYourLook API. Use when the user asks for image generation, text-to-image, image-to-image, image editing, product photography, concept art, social graphics, or a downloadable generated image.
---

# TryYourLook Image

Use the bundled script to generate an image and save it into the current workspace.

## Requirements

- Require Node.js 18 or newer. Prefer Node.js 22.21 or newer when the machine uses `HTTP_PROXY` or `HTTPS_PROXY`.
- Read the API key from `TRY_YOUR_LOOK_API_KEY`.
- Never print, store, or pass the key as a command-line argument.
- Use `TRY_YOUR_LOOK_API_BASE` only when the user explicitly needs a different API host.

If the key is missing, ask the user to create one in the TryYourLook API Keys page and set the environment variable. Do not ask the user to paste the key into chat.

## Generate from text

Run:

```bash
node <skill-folder>/scripts/generate-image.mjs \
  --prompt "A clean product photo of a glass perfume bottle" \
  --size 1024x1024 \
  --output generated-image.png
```

Allowed sizes are `1024x768`, `1024x1024`, and `768x1024`.

## Edit one image

The input must be a directly accessible HTTP(S) image URL. Local paths cannot be sent directly.

```bash
node <skill-folder>/scripts/generate-image.mjs \
  --prompt "Replace the background with a night city; preserve the face and outfit" \
  --image-url "https://example.com/input.png" \
  --size 1024x768 \
  --output edited-image.png
```

## Workflow

1. Convert the user's request into a specific visual prompt. Include subject, scene, style, lighting, composition, and quality.
2. For editing, state both what must change and what must remain unchanged.
3. Choose the closest supported size unless the user already specified one.
4. Run the script once. It creates a unique idempotency key automatically.
5. Return the saved file path, result URL, credits used, and remaining credits.
6. If generation fails, report the public error and request ID without exposing credentials.

One successful image costs 20 credits. Authentication, validation, and rate-limit failures are not charged; a charged generation failure is refunded once.

Read [references/api.md](references/api.md) only when exact request or response fields are needed.
