---
name: tryyourlook-video
description: Generate and download videos through the TryYourLook API using text, one start image, or two keyframes. Use when the user asks for text-to-video, image-to-video, photo animation, first-frame/last-frame interpolation, keyframe animation, short AI video generation, task polling, or a downloadable MP4.
---

# TryYourLook Video

Use the bundled script to create a video task, poll it to completion, and save the MP4 in the current workspace.

## Requirements

- Require Node.js 18 or newer. Prefer Node.js 22.21 or newer when the machine uses `HTTP_PROXY` or `HTTPS_PROXY`.
- Read the API key from `TRY_YOUR_LOOK_API_KEY`.
- Never print, store, or pass the key as a command-line argument.
- Use `TRY_YOUR_LOOK_API_BASE` only when the user explicitly needs a different API host.

If the key is missing, ask the user to create one in the TryYourLook API Keys page and set the environment variable. Do not ask the user to paste the key into chat.

## Choose a mode

- Text-to-video: provide only `--prompt`.
- Image-to-video: add `--image-url` with one public HTTP(S) image.
- Keyframes: add both `--first-frame-url` and `--last-frame-url`.

Local image paths cannot be sent directly. Upload them to public object storage first.

## Examples

Text-to-video:

```bash
node <skill-folder>/scripts/generate-video.mjs \
  --prompt "A slow tracking shot through a neon city in the rain" \
  --duration 5 \
  --output generated-video.mp4
```

Image-to-video:

```bash
node <skill-folder>/scripts/generate-video.mjs \
  --prompt "Subtle breathing and hair movement; preserve the face and outfit" \
  --image-url "https://example.com/start.png" \
  --duration 5 \
  --output animated-image.mp4
```

Two keyframes:

```bash
node <skill-folder>/scripts/generate-video.mjs \
  --prompt "Create a smooth transition while preserving character identity" \
  --first-frame-url "https://example.com/first.png" \
  --last-frame-url "https://example.com/last.png" \
  --duration 5 \
  --output keyframes-video.mp4
```

## Workflow

1. Build a prompt containing subject, action, scene, camera movement, lighting, and style.
2. For image modes, specify what moves and what must stay visually consistent.
3. Select 3, 5, 10, or 18 seconds. Use 5 seconds when the user gives no duration.
4. For 10 or 18 seconds, state the credit cost before generating if the user has not explicitly requested that duration.
5. Run the script once. It creates a unique idempotency key, polls every 10 seconds, and downloads the result.
6. Return the saved MP4 path, platform task ID, result URL, credits used, and remaining credits.
7. If the task fails, report the public error and request ID without exposing credentials.

Credit costs are 30, 50, 100, and 180 for 3, 5, 10, and 18 seconds. Failed tasks are refunded once.

Read [references/api.md](references/api.md) only when exact request, status, or response fields are needed.
