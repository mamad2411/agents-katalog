---
name: render-67js-media
description: Export a 67js scene to PNG stills, render passes or an MP4 through the MCP render job tools (scene_render_submit, scene_render_status, scene_render_result) of the npm package @codepawlhq/67js. Use when an agent must render an image or video of a scene, play a camera or light animation to video, cut shots with a timeline, add a score, write depth or object-ID passes, path trace a still, choose GPU or CPU and an encoder, or stay inside memory limits. Also for "render ảnh 3D", "render video 3D", "xuất mp4", "export 67js", "render bị lỗi bộ nhớ", "chất lượng MSAA". Scene building is the build-67js-scene skill.
license: MIT
---

# Export images and video from 67js over MCP

A render job is an immutable snapshot of the active scene. Edits made while it runs do not change it, and it does not
change the scene's revision, pose or checkpoints. The MCP server must have been started with `--jobs <abs private dir>`;
MP4 also needs `ffmpeg` on PATH or `--ffmpeg <abs path>`, and sound needs `--audio <abs dir>`. Without `--jobs` the
submit call fails: tell the user which launch option is missing.

## Steps

1. `scene_look` first. Never submit a job for a scene you have not looked at.
2. `scene_inspect` for the current `revision`.
3. `scene_render_submit` with `expectedRevision` and `settings`. Start small: one image at 960x540.
4. `scene_render_status` with the `jobId` until the state is terminal (`completed`, `failed`, `cancelled`,
   `interrupted`). Poll about every 5 to 10 seconds, and for video read the durable frame progress. Never loop tightly.
5. `scene_render_result`: output paths, SHA-256 hashes and metrics. Report the actual `width` and `height`, the backend
   and the seconds; memory limits can lower the size.
6. Keep what you need, then `scene_render_release` to remove the job's files.
7. `scene_render_cancel` stops a job; poll `scene_render_status` until it is `cancelled` before editing again.

## Settings by task

| Task | Read |
|---|---|
| Image, stills, video, motion clock, shots, audio, encoder, passes, path tracer | `${CLAUDE_SKILL_DIR}/references/jobs.md` |
| Size, memory, GPU or CPU, time limits, verifying the file | `${CLAUDE_SKILL_DIR}/references/limits-and-checks.md` |
| A job failed or the result looks wrong | `${CLAUDE_SKILL_DIR}/references/errors-and-recovery.md` |
| Rendering in a source checkout with `scripts/render-media.mjs` (contributors only) | `${CLAUDE_SKILL_DIR}/references/rendering.md` |

## Rules

- Smallest output that meets the need: a still before a video, a 2 second slice before the full film.
  Every film round starts as a small, low-quality preview with sound; full quality only after sign-off.
- Time is deterministic. A frame depends on its time only, so a seek gives the same pixels as the frame in a video.
  Never record the screen.
- Use `settings.motion: { "start": 0 }` to play recipe tracks (camera, nodes, lights, sun, sky, effects). Without it the
  job holds the first pose, which is the usual reason a video is a still frame. A recipe with a `timeline` uses
  `settings.timeline` and rejects `motion` and `animation`.
- Imported clips use `settings.animation`; the two clocks are independent.
- For compositing, `settings.transparent`, `settings.format` (`png16`, `exr`) and `settings.region` are off by default; video runs up to 60 fps (`references/jobs.md`, Compositing output).
- Path tracing (`settings.renderer`) is offline and slow, for stills; video and passes use the rasterizer.
- Do not stop another session's process. Heavy local exports run at below-normal priority, one job at a time.
- A GLB for Blender is `scene_export_glb`, not a render job.

## Deliver

The file path, its JSON metrics, the settings you sent and one frame you looked at. Say what was measured (frames,
duration, seconds, dimensions) and what was judged by eye. Say whether anyone listened to the audio; a score
needs provenance and measured loudness.
