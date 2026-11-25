---
name: janction-render
description: Render Blender scenes, bpy scripts, 3D files (GLB, glTF, FBX, USD, OBJ) and animations on remote NVIDIA GPUs through the JANCTION Render MCP server, with no local Blender or GPU. Use when the user wants a rendered image or video of 3D content - preview a Blender scene, render a bpy script, turn a GLB/FBX/USD model into product shots or a 360-degree turntable MP4, render a Blender animation to MP4, or render on a machine without an NVIDIA GPU or where Cycles is slow. Flow - preview, fix, estimate the cost, ask, render, download.
---

# JANCTION Render

<!-- terms:skill_terms_en -->
The `janction-render` MCP server (`https://render.janction.jp/mcp`) renders Blender scenes with Cycles or EEVEE on JANCTION's
NVIDIA GPUs. A new key gets 100 JPY of free GPU time (14 days; one per network every 30 days, further keys on the same
network share what is left), and 400 JPY more, once per card, when the user saves a card on a Stripe page that charges
nothing (the service offers it as `card_offer` once the 100 JPY is used up; tell the user it costs nothing). When a reply
carries `autocharge_offer` (the credit is about to run out), ask the user once whether to turn on auto top-up and share its
link only if they say yes; after that, previews are free up to 2 GPU-minutes a day and other renders cost 0.1 JPY per
GPU-second from prepaid credit (top-ups from 100 JPY). Up to 3,000 frames per instruction (run as parts of 240 under one job id):
1920x1080 on free time, up to 3840x2160 on prepaid credit. Inputs and results are deleted 24 hours after last use
(7 days, normally, for keys that have paid 500 JPY or more in total). Every estimate carries `decision` (`can_execute`,
`blocking_reasons`, `required_actions`): when it says the job cannot run, say so and offer the listed actions; do not promise
that a top-up alone makes it run.
<!-- /terms:skill_terms_en -->

Do not use it to edit a scene open in the user's own Blender (a local Blender MCP does that), for one still image on a machine
with its own NVIDIA GPU, or for non-Blender video or general GPU compute.

## Is it connected?

Look for the tools `render_preview`, `render_estimate`, `render_final`. If they are missing, the server is not
authenticated yet. Say so plainly and give the step for the user's app; never say a render ran when no tool was called.

- Claude Code: run `/mcp`, choose janction-render, press Authenticate, then Connect in the browser (creates a free key).
- Codex: `codex mcp login janction-render`. Gemini CLI: `/mcp auth janction-render`.
- ChatGPT and Claude.ai: open the connector settings and connect again.
- A cloud sandbox (Claude Code on the web, `CLAUDE_CODE_REMOTE=true`) may block `render.janction.jp` (its proxy answers 403
  to CONNECT, or `curl` fails). The service is not down. Use the JANCTION Render tools from a claude.ai connector if this
  session has them (pass a bpy script as `scene_script`, a web file as `scene_url`); otherwise ask the user to add
  `render.janction.jp` to the environment's Allowed domains (Network access -> Custom; a running session follows within
  about a minute): https://render.janction.jp/claude-code-blender#cloud-sessions. Do not retry until they have.

The first call `render_preview(scene_url="https://render.janction.jp/samples/cube_scene.py", environment="compare")` checks the
connection in a few seconds.

## Standard flow

1. Find the scene: a bpy script you write (pass `scene_script`), a `.blend` or 3D file on the web (`scene_url`, https), or a
   local file (`scene_path`, stdio server only). Reuse the returned `scene_id` instead of sending the scene again.
2. `scene_info` when you did not write the scene: cameras, frame range, objects, lights, missing files. No render.
3. `render_preview` - up to 4 frames tiled in one image, seconds, free within the daily preview time. Look at the image.
   Every preview returns `critic` (`ok` / `check` / `fix`) with fix code; on `fix`, apply it and preview again.
4. Show the preview and confirm frames, resolution and samples with the user. Treat engine, color management, lighting,
   materials, world/volume and compositor as visual invariants. Never switch Cycles to EEVEE or remove a look-changing
   feature without explaining the visible tradeoff and getting explicit approval.
5. For an animation, render at least 10 contiguous frames through the intended final path before the full job. Verify that
   every frame exists and inspect for black, corrupt, duplicate-looking or visibly degraded frames. This short final still
   requires the approval in step 7 unless the user already authorized final rendering.
6. `render_estimate` - GPU seconds, wall time (`human`), queue wait, `calibration.final_path_measured`, `cost` (`free`,
   `estimated_yen`, `reserved_yen`, `balance_yen`, `within_caps`) and `tell_user` / `tell_user_ja`, the one sentence for the
   user (time and price). Give the user that sentence, nothing more. After the contiguous test, always estimate again. If
   `final_path_measured` is false the sentence says it is an unmeasured figure: never present it as the time the final will
   take, and do not quote the preview's `final_estimate` as the final's time either.
7. Ask before every final, even a free one: say the time and the price (0 yen when `cost.free` is true) and wait for a yes.
   Skip the question only when the user already said "render the final" in this conversation. If they set a budget, keep
   the job inside it (`reserved_yen` from `render_estimate`); on the terminal server or the HTTP API, also pass it as
   `max_yen`.
8. `render_final` - returns `job_id`. Tell the user how long it will take.
9. `render_status(job_id)` - report `eta.human`. If it says the GPU is lent out, tell the user the wait and stop polling.
10. `render_download(job_id)` - on the remote server, links that need no key and work for about 24 hours. On the terminal
    server the files land in the job's folder and the video of a final is also delivered to the user's Downloads folder
    (`JANCTION_RENDER_DELIVER` changes it; a given `out_dir` is used as is).
11. Verify delivery before claiming success: contiguous frame numbering, decoded frame count, resolution, FPS, duration and
    black frames. Report requested and actual totals separately. A completed job or critic `ok` alone is not proof of fidelity.
12. When a final is done, `render_status` and `render_download` carry `tell_user` / `tell_user_ja`: the measured time, the
    charge and the file (the delivered path on the terminal server, the link on the remote one). Give the user that one
    sentence as soon as the job is done, without waiting for them to ask; do not read out the job's own folder, and never
    invent a local path on the remote server (the user saves the link to their Downloads themselves).

For a model the user wants seen from all sides, pass `orbit=True`: the preview shows four angles and
`render_final(orbit=True)` renders one full turn (24 frames) as an MP4. "A turntable preview" means
`render_preview(orbit=True)` (one image with four angles), nothing more; the MP4 turn is a final, so it comes after the
question in step 6. Lighting: `environment="studio"` (or `sunset`, `overcast`, `night`); `environment="compare"` on a
preview shows all four in one image.

Purpose presets fill the camera, light, backdrop, frames and output for a purpose; what you pass still wins:
`preset="product"` (4 studio shots at 0/90/180/270 degrees on a plain backdrop; the final gives 4 PNGs at 1440x1440),
`preset="turntable"` (one full turn as a 720p MP4 on a plain backdrop), `preset="animation"` (the scene's own camera,
lights and frame range; the scene is read first when the range is not known). For product shots of something the user
has no model for: `asset_search("<item>")`, then
`render_preview(scene_script='import jr_assets; jr_assets.import_model("<id>")', asset_urls=["polyhaven:<id>"], preset="product")`.

Options for creators, only when the user wants them (preview replies suggest the ones that fit in `next_actions`):
`render_preview(variations=[...])` shows 2-8 looks of one frame in one sheet; let the user pick, then pass that variant's
`render_final` args (`colors` sets object colours). On `render_final`: `compare_to=<earlier final job_id>` adds a before/after
video, `deliver=["x", "vertical", "square"]` adds social cuts of an animation, `passes=[...]` (Cycles) gives multilayer EXR
and `output="prores4444"` a ProRes 4444 .mov, `auto_samples=True` (100 frames or more) picks the fewest samples that look the
same. Every final carries a delivery check (`report.json`, `report_sheet.png`): read its verdict before step 11. Lowering
samples is a look-affecting change: ask before using `auto_samples` on the user's scene.

A script that does not run is a failed job, not a result: a script that does not parse is refused at once
(`script_syntax_error` with `line` and `source_line`, no GPU time), and a script that raises fails with
`SCRIPT_ERROR`, the line and `nothing_rendered`. Fix the line and call again; never present an earlier image as that
result.

## Rules

- Do not run `render_final` before a preview of the same scene unless the user explicitly asks to skip it.
- For an existing `.blend`, report its actual frame range and any mismatch with the requested count before rendering. Work
  on a copy when a fix is needed; do not overwrite the source.
- Do not start anything that is not free without an estimate and the user's yes. Never raise spending caps
  (`POST /v1/me/limits`) or buy credit on your own; give the user the `checkout_url` and let them pay.
- Do not call `render_share` (a public page) unless the user asks to publish.
- Retry only errors marked `retryable: true`, at most twice, waiting as told (`retry_after_s`, `Retry-After`). Do not loop.
- Do not resubmit a final job that timed out on your side: check `render_status` or the job list first. On the terminal
  server or the HTTP API, send the same `idempotency_key` so a resubmission returns the first job instead of rendering (or
  charging) twice.

## When something fails

Errors carry `code`, `retryable` and `recommended_action`. Act on the action:

| code | what to do |
|---|---|
| AUTH_REQUIRED | Reconnect: the steps under "Is it connected?". |
| INSUFFICIENT_CREDIT | Tell the user the price; show `checkout_url` (they pay in the browser), or make the job smaller. |
| COST_LIMIT_EXCEEDED | The job is above the spending cap. Ask the user; offer fewer frames, lower resolution or samples. |
| QUOTA_EXCEEDED / RATE_LIMITED | Wait until `resets_at` or `retry_after_s`; say when. |
| JOB_TOO_LARGE | <!-- terms:skill_too_large_cell_en -->Too big for one instruction: at most 3,000 frames (run as parts of 240 under one job id), 1920x1080 on free time and 3840x2160 on prepaid credit; split only ranges above 3,000 frames or lower the size.<!-- /terms:skill_too_large_cell_en --> |
| INVALID_SCENE / SCRIPT_BLOCKED | Fix the script (see below); do not retry the same input. |
| MISSING_ASSET | Name the missing files; pass them in `asset_urls` or pack them into the .blend. |
| WORKERS_UNAVAILABLE | Tell the user the wait from `eta`; offer to check later. |
| NETWORK_BLOCKED | This environment's proxy blocks the service; retrying will not help. Follow `possible_fix` (connector tools, or allow the domain). |
| JOB_FAILED | Read `failure` (`code`, `recommended_action`, `fix_by`) and `log_tail`, fix, preview again. |

More cases: [references/troubleshooting.md](references/troubleshooting.md). Prompts that work: [references/examples.md](references/examples.md).

## Writing a scene script

```python
import bpy, math
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, 24
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 1))
cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
scene.collection.objects.link(cam); scene.camera = cam
cam.location = (6, -6, 4); cam.rotation_euler = (math.radians(60), 0, math.radians(45))
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
scene.collection.objects.link(sun)
import jr_assets; jr_assets.frame_camera()   # fit every object in the frame
```

- Build the scene, camera, lights and frame range only. The service sets the engine, resolution, samples and GPU; do not call
  `bpy.ops.render.render` or change render settings.
- Blender 5.0 API: animate with `obj.keyframe_insert("rotation_euler", frame=n)`; do not touch `action.fcurves` or
  `mat.use_nodes` (both changed in 5.x). Build materials through `mat.node_tree`.
- The sandbox has no network and no local files: pass web files in `asset_urls` (`assets` on the terminal server), or pack
  textures into a .blend.
- Props, materials and HDRIs without files: `asset_search("wooden table")` (Poly Haven, CC0), then `polyhaven:<id>` in
  `asset_urls` and `jr_assets.import_model('<id>')` in the script.
