---
name: asset-generator
description: Generates or ingests the source visual asset (image or video) for a single section, before video-scroll-effect or 3d-scene-effect builds with it. Handles Higgsfield generation, user-supplied clip/image validation, and delegates the actual render-polling to the frame-pipeline agent. Called by video-scroll-effect or 3d-scene-effect when a section needs a source asset — not invoked directly by users.
---

# Asset-Generator — source asset generation and ingestion

## Scope
This skill produces ONE ready-to-use asset (a video file, or a still image) for
ONE section, based on that section's `content_brief` and `motion` from the site
plan. It does not build sites, decide structure, or make creative direction calls
beyond translating a content_brief into a generation prompt.

## Step 1 — Check for a user-supplied asset first
Before generating anything, check for a source asset in this order:
1. **`section.user_asset`** — if site-planner's plan carries one (supplied by
   the user during its Step 2c review), use it explicitly. This is the preferred,
   explicit source — the plan already told you this is what the user wants here.
2. Otherwise, fall back to checking whether the user attached or referenced a file for
   this section some other way (e.g. directly in a follow-up message).
For either source:
- Video file: validate it's readable via `ffprobe`/`ffmpeg`. If valid, this IS the
  asset — skip generation entirely, return it as-is.
- Image file: validate it's a real image. Usable directly as a still, or as a
  starting keyframe if this section will still need video generation.
- If the file isn't valid for what's needed, tell the calling skill plainly and
  ask whether to fall back to generation.

## Step 2 — Generate a keyframe (Higgsfield generate_image), if needed
- Model: **`nano_banana_pro`**. Prompt from the section's `content_brief` and
  subject — strong lighting, intentional background, "ultra sharp, photorealistic,
  8k, editorial/advertising". 16:9.
- Poll `job_display` until `completed`; keep the job id.

## Step 3 — Generate video (Higgsfield generate_video), if this section needs motion
Skip this step entirely for 3d-scene-effect sections building purely procedural
geometry with no video/image input — only run it when a section genuinely needs
generated footage or an image basis.
- Model: **`seedance_2_0`**, `1080p`, `16:9`, `duration:6`,
  `medias:[{role:"start_image", value:<keyframe id>}]`.
- Motion prompt from the section's `motion` value (see video-scroll-effect's motion
  patterns for phrasing examples — orbit, fly-through, reveal/explode, abstract, plus
  the richer named set in video-scroll-effect's SKILL.md).
- Preflight cost with `get_cost:true`; confirm with the user if cumulative cost
  across sections is non-trivial (this confirmation is coordinated by
  site-planner across the whole plan, not repeated per section here).

### Identity lock for multi-beat sections
If the section declares `beats` (a chaptered video-scroll-effect sequence — e.g.
`["orbit", "transform", "macro"]`) instead of a single `motion`: generate ONE anchor
keyframe in Step 2, then reuse that SAME keyframe id as the `start_image` reference on
EVERY beat's `generate_video` call. This locks visual identity across all of that
section's clips — same product, same lighting setup, same materials — rather than
each beat's clip drifting from an independent generation. Run Step 3 once per beat,
same keyframe each time, and return one asset per beat (see "What this returns" below).

## Step 4 — Hand off to frame-pipeline for polling/download/extraction
Once a generation job is submitted, invoke the `frame-pipeline` agent with the
job ID rather than polling inline — this keeps long render waits out of the main
conversation. Wait for its structured result before proceeding. For a multi-beat
section, invoke frame-pipeline once per beat (each beat's clip extracts into its own
`frames/<section>/<beat>/` folder) — the calling skill still gets one combined result
covering all beats.

## What this returns
Single-asset sections:
{
"asset_type": "user-clip" | "generated-video" | "generated-image" | "user-image",
"path": "...", // clip or image path
"frames_folder": "...", // only if extracted (video assets)
"actual_frame_count": 179, // only if extracted — from frame-pipeline's result
"generation_failed": false,
"failure_reason": null
}

Multi-beat sections (`section.beats` present):
{
"asset_type": "generated-video-beats",
"anchor_keyframe_id": "...", // reused as start_image across every beat below
"beats": [
{ "name": "orbit", "path": "...", "frames_folder": "...", "actual_frame_count": 150 },
{ "name": "transform", "path": "...", "frames_folder": "...", "actual_frame_count": 150 },
...
],
"generation_failed": false,
"failure_reason": null
}

## `generation_failed` / `failure_reason` must be truthful
Set `generation_failed: true` with a clear `failure_reason` any time Step 3 (video)
didn't produce a usable clip for the section it was asked for — not only on an
explicit API failure/nsfw flag, but also if video generation was never attempted at
all (no Higgsfield video access, etc.). A caller receiving an image-only result when
video was what the plan called for must be able to tell, from this field alone, that
the outcome differs from what was planned — never leave a caller to infer this from
the absence of a `frames_folder` alone, since a section that never needed video (a
pure 3d-scene-effect/image-plane section) also has no `frames_folder`, and that's a
different, non-deviating case. This field is what lets video-scroll-effect's Step 4 stop
condition and site-planner's "Disclosing plan deviations" rule actually work —
a caller can't disclose a deviation it was never told about.

## What this never does
- Never decides site structure, section count, or content — receives a
  `content_brief`, doesn't originate one.
- Never builds the actual HTML/CSS/site output — that's video-scroll-effect's or
  3d-scene-effect's job, using what this skill returns.
- Never retries a failed generation more than once with the same prompt — reword
  or switch models (per video-scroll-effect's existing retry guidance) rather than
  repeating an identical failing call.
- Never silently substitutes an image-only result for a section that was planned to
  need video — return `generation_failed: true` and let the caller decide/disclose,
  rather than quietly returning as if the image was always the whole plan.