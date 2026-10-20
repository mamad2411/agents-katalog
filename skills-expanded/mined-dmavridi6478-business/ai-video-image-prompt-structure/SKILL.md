---
name: ai-video-image-prompt-structure
description: A 6-part structural pattern for writing a detailed AI image/video generation prompt (subject, action, setting, camera/shot direction, style/VFX, closing beat) — the shape that makes the difference between a vague one-liner and a prompt that reliably produces a specific, cinematic result. Use when writing a prompt for an AI video/image generator (Midjourney, Sora, Seedance, Veo, GPT Image, etc.), when a generated result comes back generic or unpredictable, or when adapting an example prompt found on a prompt-discovery site into a new one.
---

# AI Video/Image Prompt Structure

Source: reviewed from an uploaded screen-recording (@simplydigital,
"3 Websites for unlimited FREE PROMPTS": Meigen.ai, Yesand.ai,
YouMind.com/prompts — see `design-dev-resources` for those). The
recording's actual example prompts belong to named individual creators on
those platforms, so none are reproduced verbatim here — this skill is a
structural pattern written fresh, abstracted from what those examples
had in common, not a copy of any one of them.

## The pattern

A prompt that reliably produces a specific result — not a generic,
unpredictable one — tends to stack these six parts, roughly in this
order. Not every generator needs every part (a still-image prompt can
skip the camera-movement and closing-beat parts entirely), but skipping
a part is a choice, not an oversight:

1. **Subject** — who or what is in frame, described with enough concrete
   visual detail that two different readers would picture the same
   thing: build, clothing, distinguishing features, expression. "A
   teenager" is not a subject; "a teenage swordsman with wild black hair
   and glowing electric-blue eyes, wearing a torn combat jacket" is.

2. **Action** — what the subject is actually doing, as a specific verb
   phrase, not a vague state. "Fighting" is a state; "charging through a
   collapsing city while cutting down pursuers mid-sprint" is an action
   with its own internal sequence.

3. **Setting** — where and when, with enough environmental detail to
   anchor lighting and mood: time of day, location type, weather,
   background activity. The setting should be doing work — creating
   contrast, urgency, or atmosphere — not just naming a location.

4. **Camera / shot direction** — for video specifically: how the camera
   moves and cuts (static, handheld, orbit, whip-pan, crash-zoom), and
   the shot types used (wide establishing, close-up, POV). This is the
   part most one-line prompts skip entirely, and it's usually the
   difference between a generic clip and a deliberate one.

5. **Style / VFX** — the visual treatment: art style, color grading,
   render style (photoreal, anime, painterly), and any specific effects
   (particle FX, motion blur, lighting rigs). Name the reference
   register precisely ("anime-style smear frames," "documentary-style
   handheld") rather than a vague adjective like "cool" or "epic."

6. **Closing beat** — for video: how the shot resolves — the final frame
   or moment the sequence lands on. A prompt that specifies where the
   action *ends* produces a far more coherent generated clip than one
   that only describes the middle.

## Worked example (original, not from any source site)

*Subject:* A weathered lighthouse keeper in a yellow oilskin coat, grey
beard soaked with spray.
*Action:* Climbing the spiral stairs two at a time toward a flashing
warning light.
*Setting:* A storm-lashed cliff-top lighthouse at night, waves crashing
below, lightning intermittently lighting the scene.
*Camera:* Handheld, following close behind at stair height, cutting to a
wide exterior shot as lightning strikes.
*Style:* Photoreal, desaturated blue-grey grading, heavy rain particle
effects, practical-looking lighting flicker.
*Closing beat:* Ends on the keeper reaching the lamp room and turning to
face the storm, lit only by the rotating beam.

## Adapting an example from a prompt-discovery library

When starting from someone else's posted prompt (Meigen.ai, Yesand.ai,
YouMind, or similar), map it onto the six parts above before changing
anything — it makes clear which part is doing the work you actually want
to borrow (usually camera direction or style) versus the parts that are
specific to their original subject and should be swapped out entirely,
not lightly edited.

## Related skills in this repo

- **design-dev-resources**: the three prompt-discovery sites this
  pattern was abstracted from, plus the design-inspiration galleries for
  visual (not prompt) reference.
- **hyperframes**: once a prompt produces the footage, this is the
  skill for actually composing it into a finished video.
- **canvas-design**, **frontend-design**: for static-image generation
  specifically, the subject/setting/style parts of this pattern still
  apply; camera direction and closing beat don't.
