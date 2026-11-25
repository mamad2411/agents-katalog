---
name: mage-angles
description: |
  See an existing image from a new camera angle with Mage: the same subject,
  pose, light, and scene, shot by a second camera at a chosen height and side.
  The Angles app as a skill, on Mango 4 by default. Use when: "new camera
  angle", "show this from the side", "view from above", "low-angle shot of
  this image", "back view of this", "three-quarter view", "turn the camera
  around it", "more angles of this product", "coverage of this scene for a
  storyboard". NOT for: a full turnaround sheet of a character
  (mage-character-sheet), relighting (mage-relight), product photography from
  scratch (mage-product-photoshoot), or camera moves in a video
  (mage-generate).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Angles

Regenerate an image from a different camera position: same subject, pose, light, and scene, new viewpoint. This is the [Angles app](https://www.mage.space/apps/angles) as a skill: the same angle grid, prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **The image.**
2. **The angle:** where the camera goes, as a height and a side in 45° steps. If the request names no angle, ask; offer front-right three-quarter, a side profile, and a high angle as examples.

## Build the prompt

```
Regenerate this image from a new camera angle: a <angle> view of the same subject and scene. Keep the subject's identity, pose, clothing, expression, lighting, environment, props, and overall composition exactly as in the original — only the camera position and viewing perspective should change. The output should look like the same moment captured by a second camera placed at the new angle.
```

`<angle>` is the app's label for the camera position. Left and right are the subject's own, so the camera on the subject's right sees their right side:

- Directly above the subject (bird's-eye, top-down): `directly overhead, looking straight down`. Directly below: `directly below, looking straight up`. Neither takes a side.
- Otherwise, the side:

  | Camera position | Text |
  |---|---|
  | In front | `front` |
  | Front, toward the subject's right | `front-right three-quarter` |
  | The subject's right side | `right side profile` |
  | Behind, toward the right | `back-right three-quarter` |
  | Behind | `directly behind` |
  | Behind, toward the left | `back-left three-quarter` |
  | The subject's left side | `left side profile` |
  | Front, toward the left | `front-left three-quarter` |

- With the camera 45° above eye level, put `high-angle ` in front of the side (`high-angle front-right three-quarter`); 45° below, `low-angle `. At eye level, the side alone.

The sentence always reads "a <angle> view", as the app writes it, including before `directly`.

## Settings

- Model: Mango 4 (`mango`, `model_id: "mango-v4"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask.

## Run

```json
{
  "model_id": "mango-v4",
  "resolution": "2K",
  "aspect_ratio": "<closest to the image>",
  "image": "<the image>",
  "prompt": "<the filled prompt>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

For several angles, run one generation per angle from the same source image, never from an earlier result. Quote the total and wait for a yes.

## Check and deliver

If you can see the result: it is the same subject and scene, and what was hidden in the original looks plausible. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver each link with its angle as the label.

The model invents what the original didn't show. Small moves are reliable; a reverse angle or a straight overhead view usually isn't, so say so when the user asks for one.

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
