---
name: moda-video-motion
description: >-
  Vector-native motion: keyframes, animated posts/banners, logo stingers,
  shader fills, photo slideshows, timeline compositing. Free authoring;
  exports mp4/gif.
argument-hint: "[what moves + the target size/platform] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read
---

# moda-video-motion

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Sizes and defaults

| Piece | Size | `--category` | Export |
|---|---|---|---|
| Landscape motion / stinger | 1920×1080 | `animation` | `--format mp4 --page N` |
| Vertical post, story, reel | 1080×1920 | `animation` | mp4 (gif for a loop) |
| Square animated post | 1080×1080 | `animation` | mp4 or gif |
| Animated banner ad | the ad's exact size | `animation` | gif |
| Shader-fill background | any canvas | any | mp4/gif — it freezes in stills |

Four facts that decide most of the work:

- Keyframes and clip sequencing apply ONLY on `--category animation`; on any
  other canvas every motion call is dropped with a warning. Animated shader
  fills move anywhere.
- Static exports (png/jpeg/pdf/pptx) of animation and video-filled nodes render
  BLANK or frozen — deliver mp4/gif, and say so if a still is requested.
- mp4/gif REQUIRE `--page N`: one animated page per file. A page with no
  animation rejects typed `no_animation` — the honest answer is a still + the link.
- Everything in this recipe is unmetered: iteration costs nothing.

## Recipe — motion on a canvas

1. `moda canvas create --name "[Piece]" --intent "[one-line brief]" --size [WxH] --pages 1 --category animation --brand [KIT]` — send the link immediately.
2. Author the still frame FIRST — real type, brand geometry, layout: `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]` (references/markup.md). Motion on a bad frame is a bad piece that moves.
3. `moda canvas screenshot [CANVAS_REF]` — fix the frame before animating.
4. Add motion: `moda canvas edit [CANVAS_REF] --file motion.js` — a `motion.page(...)` program with tweens, effects, staggers and recipes. Read references/motion-recipes.md FIRST: its opening "motion model" section is the five rules that decide whether the motion is correct (rest state, one track per target, what `blend` makes keyframes mean, why `endMs` is not a snap-back point, how an endless loop is authored), and the named recipes — logo sting, animated stat, kinetic type, shader background — follow it. Author from that file; don't probe.
5. Draft-judge the movement: `moda export [CANVAS_REF] --format gif --page [N] -o draft.gif` and look at it. A screenshot shows one frozen frame — it cannot tell you whether the motion works.
6. Deliver: live link FIRST, then `moda export [CANVAS_REF] --format mp4 --page [N] -o [piece].mp4`. Read `warnings[]`.

## Recipe — footage under real type (timeline compositing)

1. Get the clip into team files: `moda file upload [clip.mp4]`, or reuse the durable `file_…` a generated render returned (moda-video-clip owns generation).
2. Animation canvas at the delivery size, then place the clip with `<video src="file_…" width="1920" height="1080" fit="cover"/>` via `moda canvas markup [CANVAS_REF] --file - --page [PAGE_ID]` — the clip is a fill; layer type and brand marks above it.
3. Sequence and trim in `moda canvas edit [CANVAS_REF] --file cut.js` (`t.video(node, { startMs })`; trim/rate/loop via `update()` — references/edit-code.md).
4. `moda export [CANVAS_REF] --format mp4 --page [N] -o [piece].mp4`, then read `warnings[]`: server mp4 muxes audible clip audio, and `audio_source_dropped` names anything that did not survive. Relay it — never a silent loss.

## Examples

- "an animated banner ad, 300×250" → motion recipe at the ad's exact size → gif.
- "a stinger from our logo" → motion recipe, `recipe-rise` + a shader backdrop.
- "make this post move" → import/rebuild the frame on an animation canvas, then animate.
- "cut these two clips together with our headline over them" → compositing recipe.
- "a video from these 5 photos" → compositing recipe: place, sequence, export mp4.

## Errors

Any typed error → load moda-core and read its recovery reference.
Edit programs are atomic — a failure means NOTHING applied: re-read, fix the
program, re-run. `no_animation` on export means the page has no motion yet.

## Make it recurring

The weekly animated post → moda-automate; a stinger or lower-third you will
reuse on every future piece → moda-templates.

See also: moda-video — the lane fork, generated clips, cost boundaries ·
moda-core — the contract, recovery, everything Moda can do.

## References

| Doc | Load when |
|---|---|
| references/motion-recipes.md | ALWAYS before authoring motion — the motion model, then the named deliverables (logo sting, teaser, animated ad) |
| references/edit-code.md | before writing an edit program: batches, revisions, warnings |
| references/video.md | the timeline API, canvas video placement, export rules — jump to "The motion timeline API"; the long first half is the generated-clip model roster, which this lane does not need |
