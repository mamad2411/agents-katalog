---
name: make-video-pipeline
description: >-
  Produce a complete short or long video from an idea, script, article, URL,
  music track, pull request, or raw face-cam recording. Use when an agent must
  own the full production arc: route the source into generated-voice animation
  or real-voice face-cam, lock design and narration, create or transcribe voice,
  plan and author HyperFrames visuals, render and inspect frames, run visual and
  audio gates, bake a cover, write platform copy, and deliver or publish a
  verified MP4.
---

# Make video pipeline

Produce one verified MP4 through reviewable artifacts and lane-specific gates.

## Route

Identify the source:

- idea, article, notes, script, URL, PR, or topic -> generated-voice animation
- raw talking-head recording -> real-voice face-cam
- music track with no narration -> beat-driven animation

When available, read current creator-demand data and the latest own-channel analytics synthesis. Compare creator posts with each creator's own median. Check the shipped catalog before committing to the topic. Use this evidence to pressure-test an idea, not to copy another creator's structure or wording.

Decide:

- short vertical or long horizontal
- exact script or bullet-point delivery
- one mechanism or takeaway

Create the project structure before production. Record `source.kind` and format in `project.json`.

## Lock the common contract

Write `brief.md` and `design.md`.

Require:

- one mechanism sentence
- controlling metaphor
- locked style frame and exact final frame
- palette and type
- named rhythm
- beat windows
- motion-family plan
- caption and platform keepouts
- asset plan and negative list

Do not let downstream work re-author this contract.

Read [references/artifact-contracts.md](references/artifact-contracts.md) for files and schemas.

## Choose the voice lane

For generated voice, read [references/animation-lane.md](references/animation-lane.md).

For a real recording, read [references/face-cam-lane.md](references/face-cam-lane.md).

Never run written-copy cleanup on recorded face-cam speech. Preserve selected audio as contiguous source slices.

## Author the composition

Use HyperFrames when available.

1. Build the visible held state before entrance motion.
2. Write `shot-plan.json` for animated beats.
3. Give every visible element a motion verb or deliberate stillness.
4. Use two to four compatible motion patterns per scene.
5. Use at least three broad motion families in a multi-beat short.
6. Keep any family, axis, ease shape, or duration band below about 60 percent of beat entrances.
7. Register one paused timeline and make every rendered state seekable.
8. Freeze required media into local project paths.

Non-negotiable render rules:

- no wall-clock visual state
- no unseeded randomness
- no infinite repeat
- no render-time required network fetch
- no timeline construction inside timers or promises
- no competing transform tweens on one element
- media playback belongs to the framework

## Validate before render

Run the available equivalents of:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect
```

For sub-compositions, take midpoint snapshots of the assembled composition. Static per-file checks cannot prove that mounted scenes registered and rendered.

## Render and review

Render a draft. Generate:

- entrance, hold, payoff, and seam frames
- a full contact sheet
- machine-readable findings

Open the images. Substantial animation requires at least three render, look, and repair passes.

Use human review for metaphor, hierarchy, density, repetition, and payoff. Use a rendered-browser geometry sweep for clipping, overflow, occlusion, keepouts, off-canvas subjects, and centering.

Read [references/gates-and-handoff.md](references/gates-and-handoff.md).

## Route fixes

Route a review flag by both `kind` and `source.kind`.

- generated voice error -> update one script line and regenerate one voice frame
- face-cam voice error -> select another source take
- visual/animation -> edit the scene owning the timestamp
- pacing -> adjust clip timing and later starts
- platform copy -> update that platform field

Use one commit per flag. Rerender, audit, and lint before resolution.

## Finish

Create on-screen captions from word timestamps. Create separate platform copy and run written copy through a humanization pass.

Generate several crop-safe covers. Open them, choose one, and bake it as the final MP4 frame.

Rerun the visual gate after applying the cover. Seal the current composition, acknowledgements, and final MP4 together.

## Publish or hand off

Before publishing:

1. Verify the ship seal.
2. Validate every platform caption.
3. Confirm the schedule or queue slot with the user.
4. Upload the exact sealed MP4.
5. Record returned post IDs.
6. Archive only after the posting service reports success.

If publishing is outside scope, deliver the final MP4, cover state, captions, and verification report.

## Close the feedback loop

After the published posts have usable analytics:

1. Group platform copies of the same video by posting result ID.
2. Compute each platform's median from the channel's own history.
3. Tag results as hit above 2 times median views, normal from 0.5 to 2 times, or bomb below 0.5 times.
4. Support every pattern with named posts and real numbers.
5. Record what shipped, topic saturation, audience language, cross-platform differences, and next production decisions in `analytics-synthesis.md`.

Do not infer retention, saves, watch time, or demographics when the source does not provide those fields. This feedback pass informs future work and does not block delivery of the current MP4.

## Completion

Do not finish until:

- the design contract is present
- the lane-specific voice validator passes
- visual snapshots have been opened
- rendered-frame findings are fixed or justified against current evidence
- audio audit passes
- the cover is baked
- the final seal matches the delivered MP4
