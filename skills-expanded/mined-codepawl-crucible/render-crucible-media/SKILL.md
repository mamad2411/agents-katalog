---
name: render-crucible-media
description: Export a Crucible scene to PNG stills, render passes or an MP4 through the MCP render job tools (scene_render_submit, scene_render_status, scene_render_result) of the npm package @codepawlhq/crucible. Use when an agent must render an image or video of a scene, play a camera or light animation to video, cut shots with a timeline, add a score, write depth or object-ID passes, make a transparent frame sequence, path trace a still, pick a quality tier, choose GPU or CPU and an encoder, or stay inside memory limits. Also for "render ảnh 3D", "render video 3D", "xuất mp4", "export Crucible", "render bị lỗi bộ nhớ", "chất lượng MSAA". Scene building is the build-crucible-scene skill.
license: MIT
---

# Export images and video from Crucible over MCP

A render job is an immutable snapshot of one scene (`sessionId`, else the last used) and stays tied to it. Edits made while it runs do not change it, and it does not
change the scene's revision, pose or checkpoints. The MCP server must have been started with `--jobs <abs private dir>`;
MP4 also needs `ffmpeg` on PATH or `--ffmpeg <abs path>`, and sound needs `--audio <abs dir>`. Without `--jobs` the
submit call fails: tell the user which launch option is missing.

## Steps

1. `scene_look` first. Never submit a job for a scene you have not looked at.
2. `scene_inspect` for the current `revision`.
3. `scene_render_submit` with `expectedRevision` and `settings`. Start small and fast: one image at 960x540 with
   `quality: "draft"`. The reply carries `estimate` (`seconds`, `peakMemoryMiB`) and, with `quality`, which tier will run.
4. `scene_render_status` with the `jobId` alone (a `sessionId` is refused) until the state is terminal (`completed`,
   `failed`, `cancelled`, `interrupted`). Wait about the estimated seconds, then poll every 5 to 10 seconds and read the
   durable frame progress. Never loop tightly. Status and result answer in a short `concise` form by default; pass
   `response_format: "detailed"` for the full record.
5. `scene_render_result`: output paths, sizes and metrics. Report the actual `width` and `height`, the backend
   and the seconds; memory limits can lower the size. `detailed` adds SHA-256 hashes and resource counters. The answer attaches the PNGs of a job of up to 8 files; pass `images: false` when the paths are enough, or `images: [0, 95]` (artifact indexes) to see chosen frames of a larger job.
   `metrics.report.fallbacks` lists everything that ran differently from the request: read it.
6. Keep what you need, then `scene_render_release` to remove the job's files.
7. `scene_render_cancel` stops a job; poll `scene_render_status` until it is `cancelled` before editing again.

## Settings by task

| Task | Read |
|---|---|
| Image, stills, transparent sequences, video, motion clock, shots, audio, encoder, passes, path tracer, quality tiers, grid volumes and texture sequences | `${CLAUDE_SKILL_DIR}/references/jobs.md` |
| Size, memory, GPU or CPU, time limits, verifying the file | `${CLAUDE_SKILL_DIR}/references/limits-and-checks.md` |
| A job failed or the result looks wrong | `${CLAUDE_SKILL_DIR}/references/errors-and-recovery.md` |
| Rendering in a source checkout with `scripts/render-media.mjs` (contributors only) | `${CLAUDE_SKILL_DIR}/references/rendering.md` |

## Rules

- Smallest output that meets the need: a `draft` still before a video, a 2 second slice before the full film.
  Every film round starts as a small, low-quality preview with sound; full quality (`final`, or a larger size) only
  after sign-off. Never submit the final render first.
- Time is deterministic. A frame depends on its time only, so a seek gives the same pixels as the frame in a video.
  Never record the screen.
- Use `settings.motion: { "start": 0 }` to play recipe tracks (camera, nodes, lights, sun, sky, effects). Without it the
  job holds the first pose, which is the usual reason a video is a still frame. A recipe with a `timeline` uses
  `settings.timeline` and rejects `motion` and `animation`.
- A recipe whose only motion is `physics` (or `cloth`, `particles`), a grid volume sequence or a texture sequence is
  filmed with `motion: { "start": 0 }`; the job plays the bake on the scene clock, so do not `bake-motion` first. Physics,
  cloth and particles start at 0 when `motion` is left out; sequences need it set. Video `duration` defaults to the bake length.
- Imported clips use `settings.animation`; the two clocks are independent.
- For compositing, `settings.transparent`, `settings.format` (`png16`, `exr`) and `settings.region` are off by default; a
  transparent frame sequence is one `stills` job with `stillCount`; video runs up to 60 fps (`references/jobs.md`).
- Path tracing (`settings.renderer`, or `quality: "final"`) is offline and slow: judge a still first. A video job takes
  it too, one trace per frame; passes, `transparent`, `format` and `region` need the rasterizer.
- Do not stop another session's process. Heavy local exports run at below-normal priority, one job at a time.
- A GLB for Blender is `scene_export_glb`, not a render job.
- A preview that shows a look change (shaders, lighting, materials, default render, post steps) goes through
  `node scripts/check-preview.mjs <still or clip> [--reference <Cook or Cycles still>]` before you send it for review. It
  reports exposure, shimmer and the camera inside a wall, and exits 1 on a fail (`docs/check-preview.md`).

## Deliver

The file path, its JSON metrics, the settings you sent and one frame you looked at. Say what was measured (frames,
duration, seconds, dimensions) and what was judged by eye. Say whether anyone listened to the audio; a score
needs provenance and measured loudness.
