---
name: mage-video-editor
description: |
  Edit an existing video with a prompt using Mage: describe the change and it
  is applied across the clip while the motion, camera, timing, and composition
  stay, with optional reference images or characters for a specific subject,
  object, or look. The Video Editor app as a skill, on Cherry 2 Pro by
  default. Use when: "edit this video", "change her jacket to red in this
  clip", "make this video look like anime", "replace the background of this
  clip", "turn day into night in this video", "add snow to this footage",
  "restyle this clip", "put this product in the video". NOT for: swapping a
  face or a whole person in a video (mage-video-face-swap,
  mage-video-character-swap), making a video from nothing or from a still
  (mage-generate), lip sync (mage-lipsync), or cutting, trimming, and timeline
  work.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Video Editor

Change what a video shows without re-shooting it: one instruction, applied across the whole clip, with the original motion and framing kept. This is the [Video Editor app](https://www.mage.space/apps/video-editor) as a skill: the same models, prompts, and defaults, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link. A page that plays a video (YouTube, Instagram, a Drive preview) is not a file.
3. **The clip's length matters.** Each model accepts a range of clip lengths, and the price depends on the clip's length. Measure it when you can run commands (`ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp4`); otherwise ask the user how long it is. `estimate_cost` measures a clip that is a `create_upload` URL or an earlier Mage result, and answers `requires_media_measurement` for a clip on another host: upload it with `create_upload` to price it.
4. **Rights.** The user needs permission for the footage and for anyone recognizable in it.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always quote the model and the price in Gems and wait for a yes before generating.
4. The user's instruction is the change. Don't expand or restyle it; it goes inside the app's wrapper, unchanged.
5. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **The video:** one clip, MP4, MOV, or WebM. 4–30 seconds on the default model; other models differ (`references/models.md`).
2. **The change,** in the user's words: their instruction as a sentence of its own, without the link or the request around it ("In this clip <link>, change her jacket to red" is sent as "Change her jacket to red."). Don't add to it. If it is vague ("make it better"), ask what should change.
3. **References (optional, up to 2):** images of a specific subject, object, or look the change involves, or saved characters by `@handle`. Mention each `@handle` in the instruction where it belongs ("replace the dog with @rex"), and call a reference image "the reference image" ("make her wear the jacket from the reference image").

## Settings

- Model: Cherry 2 Pro (`cherry`, `model_id: "cherry-2-pro"`), Mage's default for video. When the user asks for another model, use it.
- `resolution`: `480p`, the cheapest. Offer `720p` or `1080p` with the price when the user wants a final.
- Leave `duration` and `aspect_ratio` out: on Cherry 2 Pro the output follows the clip's length and shape.
- `use_character_voices: false`.
- The clip must be 4 to 30 seconds long. For a shorter clip, say so and offer Lemon, which takes 1 to 15 seconds.

Other models the app offers (Lemon, the other Cherry models, Plum, Plum Max, Berry, Grok Video), with their clip limits, fields, and settings: `references/models.md`. Read it before using any model but Cherry 2 Pro.

## Run

On a Cherry model the app wraps the instruction before sending it. Send exactly this, with the instruction in the slot:

```
Use the provided reference video as the source of truth. Recreate its visual content as closely and faithfully as possible from beginning to end.

Preserve the shot sequence, timing, camera angle, camera movement, framing, composition, subject identity, poses, actions, body movement, facial expressions, environment, background, lighting, color grading, and visual style of the reference video.

Apply only the following requested change:
<the change>

Make the minimum changes necessary to fulfill the request. Everything not explicitly mentioned in the requested change must remain consistent with the reference video. Do not restage the scene, reinterpret the action, alter the camera or motion, add or remove unrelated subjects or objects, or introduce unrelated visual changes unless the request explicitly requires it.
```

Models outside the Cherry line get the instruction alone.

```json
{
  "model_id": "cherry-2-pro",
  "resolution": "480p",
  "videos": [
    "<the clip>"
  ],
  "image": "<optional first reference>",
  "additional_images": [
    "<optional second reference>"
  ],
  "use_character_voices": false,
  "prompt": "<the wrapped prompt>"
}
```

Leave `image` and `additional_images` out when there are no reference images.

1. `get_model` for the architecture, once per conversation, to confirm its fields, options, and rules.
2. `estimate_cost` with the exact config. Tell the user the model, resolution, length, and price in Gems, and **wait for a yes**. Video is expensive and the price climbs with resolution and length.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120`, repeated quietly until the status is `completed`, `failed`, or `cancelled`. Video takes minutes.

`duration` and `resolution` are strings, written exactly as `get_model` lists them (`"4"`, `"480p"`, and on Plum `"768P"`).

## Check and deliver

Deliver the link with the model, resolution, length, and Gems. Tell the user to watch the whole clip, not one frame: an edit that looks right in a still can break during motion. If the change didn't take or the motion drifted, offer one retry.

Prompt editing is not a timeline: it can't make an exact cut or change a specific frame range.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |
| `requires_media_measurement` | The clip is on a host `estimate_cost` can't measure. Upload it with `create_upload` and price again. |

## References

- `references/models.md`: every model the app offers for editing, with clip limits, fields, settings, the Cherry wrapper prompt, and audio.
