---
name: sorrycode-image2
description: Generate or edit and save images through the unified SorryCode Images API. Use when the user asks to generate covers, posters, illustrations, product visuals, article images, avatars, game sprites, or edit/restyle an existing image with SorryCode image models such as gpt-image-2 or Gemini image models. The skill must check for a SorryCode API key before making requests, guide the user to create or set the key if missing, call /v1/images/generations or /v1/images/edits, and save outputs into a local folder with prompt and response diagnostics.
---

# SorryCode Image2

Use this skill when the user wants to create image assets through the unified SorryCode Images API.

## Default Path

1. Clarify whether the user wants to generate a new image or edit an existing one.
2. Check whether `SORRYCODE_API_KEY` exists before writing or running any request.
3. If the key is missing, stop and help the user set it up. Do not invent a key and do not continue with a fake request.
4. Use `gpt-image-2` by default. If the user asks for Gemini, Nano Banana, or a Gemini image model, use `gemini-3-pro-image-preview` unless they specify another model.
5. Use `1024x1024` by default. If the user asks for aspect ratio, high resolution, 2K / 4K, or `size`, load `references/size-guide.md` before choosing the parameter.
6. Use the bundled Node script `scripts/sorrycode-image2.mjs` for actual requests. Do not hand-write inline JSON for shell one-offs.
7. For first-run Gemini image checks, use `--no-stream` so the request is plain OpenAI-compatible JSON with `response_format: b64_json`.
8. For slow OpenAI image requests or large images, use the default streaming mode with `stream: true` and `partial_images: 2`.
9. For editing, require a local input image path, then run the script with `--mode edit --image <path>`.
10. Save outputs under `outputs/images/<short-slug>/` unless the user asks for another folder. The script writes `prompt.txt`, `request.json`, `headers.txt`, `response.json`, `summary.json`, and `events.ndjson` when streaming.

## Execution Path

Resolve `SKILL_DIR` to the directory that contains this `SKILL.md`; when editing this repository directly, `SKILL_DIR` is the repository root.

Default OpenAI image generation:

```bash
node "$SKILL_DIR/scripts/sorrycode-image2.mjs" \
  --prompt "a cute cat sleeping in sunlight" \
  --out outputs/images/cat
```

Gemini image generation through the same Images API:

```bash
node "$SKILL_DIR/scripts/sorrycode-image2.mjs" \
  --model gemini-3-pro-image-preview \
  --no-stream \
  --prompt "a clean product-style image of a cute orange cat astronaut sticker" \
  --out outputs/images/gemini-cat
```

Edit mode:

```bash
node "$SKILL_DIR/scripts/sorrycode-image2.mjs" \
  --mode edit \
  --image ./input/product.png \
  --prompt "make this product screenshot cleaner" \
  --out outputs/images/product-hero
```

Do not ask the user to set `SKILL_DIR`; derive it from the loaded skill path before running the command.

## API Settings

Default generation endpoint:

```text
https://www.sorrycode.com/v1/images/generations
```

Default edit endpoint:

```text
https://www.sorrycode.com/v1/images/edits
```

If the user or project provides `SORRYCODE_BASE_URL`, use that value and append `/images/generations` or `/images/edits` after removing any trailing `/v1` or `/` ambiguity carefully.

Default `gpt-image-2` generation request body:

```json
{
  "model": "gpt-image-2",
  "prompt": "...",
  "size": "1024x1024",
  "n": 1,
  "stream": true,
  "partial_images": 2,
  "response_format": "b64_json"
}
```

Gemini first-run request body (non-streaming):

```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "...",
  "size": "1024x1024",
  "n": 1,
  "response_format": "b64_json"
}
```

Do not use Gemini native `/v1beta/models/{model}:generateContent` in this skill. SorryCode image generation is consolidated on OpenAI-compatible Images endpoints.

## API Key Gate

Before making a request, check:

- macOS / Linux: `process.env.SORRYCODE_API_KEY` or `$SORRYCODE_API_KEY`
- Windows PowerShell: `$env:SORRYCODE_API_KEY`

If missing, say:

```text
I need your SorryCode image API key before I can generate or edit images. Create one from Platform / Create API Key, then I can help your computer remember it. The setting name is SORRYCODE_API_KEY, and it will not change your Codex model configuration.
```

## Progressive Disclosure References

Load references only when they are needed:

- `references/prompt-patterns.md`: when the user wants examples, styles, or help shaping the prompt
- `references/size-guide.md`: when the user asks for aspect ratio, high resolution, 2K / 4K, or how to set `size`

## Prompt Shaping

Ask for only the missing fields that matter:

- task type: generate a new image, or edit an existing image
- source image path, only for edit tasks
- model family: OpenAI image or Gemini image, only if the user cares
- purpose: cover, poster, illustration, character, product visual, article image
- subject
- style
- mood or color
- whether text is needed

Do not over-optimize the first prompt. The first run should produce one usable image quickly.

## Script Rules

Use the bundled script instead of generating a new ad-hoc request script. The bundled script is dependency-free, uses built-in `fetch`, reads `SORRYCODE_API_KEY`, writes UTF-8 diagnostics, and parses JSON or SSE responses.

Do not hardcode secrets. Do not print the API key.

## Error Handling

- `401`: API key is missing, invalid, or not sent as `Authorization: Bearer ...`
- `400`: request body is malformed; check `model`, `prompt`, `size`, and `n`
- `400 images endpoint requires an image model`: model is not enabled as an image model
- `503 No available compatible accounts`: the current group has no compatible image account available, or compatible accounts are temporarily unavailable
- `524`: request exceeded Cloudflare's response window. Retry later, simplify the prompt, reduce size, or try `--no-stream` for first-run Gemini checks.

When a request fails, point to the diagnostics folder and mention the exact saved files. Do not claim the image was generated unless the script saved an image file.
