---
name: wan-text-to-image
description: Generate a brand-new image from a text prompt via the Wanxiang wan2.6-t2i model on Alibaba MaaS. Use when the user says "สร้างภาพ...", "วาดภาพ...", "generate an image of...", or otherwise asks for a new image from a description — not for modifying an image that already exists (that's wan-image-edit).
---

# Wan Text-to-Image

Generate an image from a text prompt using the Wanxiang `wan2.6-t2i` model via Alibaba MaaS.

## Steps

1. **Resolve the API key.** Follow `../_shared/wan-api-key.md` to load `WAN_API_KEY` and `WAN_BASE_URL`. Complete when `WAN_API_KEY` holds a value — never call the API without it.

2. **Determine parameters.** Pull from the user's request, asking only for what's missing:
   - `prompt` — the image description (required).
   - `size` — width*height, e.g. `1280*1280`, `1280*720`; ask if the user hasn't implied one; default `1280*1280`.
   - `n` — number of images; ask if not specified; default `1`.

   Complete when prompt, size, and n are all settled (user-given or default).

3. **Call the API.** Follow `../_shared/wan-async-call.md` to submit and poll. The request's `content` is just the prompt:
   ```json
   {"role": "user", "content": [{"text": "<resolved prompt>"}]}
   ```
   with `model: "wan2.6-t2i"` and `parameters: {"n": <resolved n>, "size": "<resolved size, as width*height e.g. 1280*1280>"}`.

   Complete when the task reaches `SUCCEEDED` (image URLs in hand) or a genuine error has been surfaced and the step has stopped.

4. **Save the output.** Download each image URL from the response to a temp file — the links expire in 24 hours. Ask the user where to save the result before writing the final file(s).

   Completion criterion: every requested image exists as a file at the location the user gave.
