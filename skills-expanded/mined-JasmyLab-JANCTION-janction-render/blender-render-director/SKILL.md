---
name: blender-render-director
description: Plans any Blender rendering job before anything is changed or rendered - a still, product shots, a turntable or an animation - and routes it to the right render skills in order. Use when a user asks an AI agent to render, preview or deliver images or video from a .blend, a bpy script or a 3D file (glTF, FBX, USD, OBJ), with a local Blender or with JANCTION Render's cloud GPUs.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-scene-preflight, blender-render-settings, blender-color-management, blender-lighting-recipes, blender-product-shots, blender-turntable, blender-clay-wireframe, blender-animation-delivery, blender-reference-match
---

# Blender Render Director

Plan first, keep the user's look, prove the result. A render is done when the pictures match what was asked and every
frame is there, not when a job says "finished".

## Workflow

```
1 READ      what the user asked: still / product shots / turntable / animation, size, frames, deadline, budget
2 INSPECT   the scene as it is (blender-scene-preflight) and report it before changing anything
3 PLAN      the brief below; name the skills you will use and what you will not change
4 PREVIEW   a cheap render of representative frames; look at it, compare with any reference
5 FIX       one subsystem at a time (camera, light, material, color, compositor), preview again
6 TEST      for animation: 10 contiguous frames through the final settings (blender-animation-delivery)
7 ESTIMATE  time and cost from the test, not from a guess; tell the user and wait for a yes
8 RENDER    the final
9 VERIFY    files, frame count, resolution, FPS, duration, black or broken frames; then report
```

## The brief (write it before step 4)

```
Goal:        product shots of the bottle, 4 angles, transparent PNG, 1440x1440
Source:      bottle.blend - Cycles, 1-1 frame, AgX, camera CAM_Main, 2 missing textures
Keep:        engine, materials, world, color management, compositor
Change:      add a shadow catcher; frame the camera; pack the 2 textures once found
Skills:      blender-scene-preflight -> blender-product-shots -> blender-lighting-recipes
Where:       local Blender for the preview, JANCTION Render for the 4 finals
Check:       edges clean on transparency, label readable, color matches the reference photo
```

## Routing

| The user asks for | Skills, in order |
|---|---|
| "Render this .blend" (unknown scene) | scene-preflight -> render-settings -> color-management |
| Product photos, e-commerce, packshots | scene-preflight -> product-shots -> lighting-recipes -> color-management |
| A 360 view or spinning model | product-shots (framing) -> turntable |
| A portfolio clay or wireframe pass | clay-wireframe |
| An animation, a shot, a sequence | scene-preflight -> render-settings -> animation-delivery |
| "Make it look like this picture" | reference-match -> lighting-recipes -> color-management |
| It is too dark, noisy, washed out | render-settings and color-management (diagnose before changing) |

## Where to render

- A local Blender with its own NVIDIA GPU is the fastest place for a single still or quick look; drive it through a
  Blender MCP that runs Python (for example `execute_blender_code` in blender-mcp) or `blender -b file.blend -P script.py`.
- Use JANCTION Render (cloud GPUs through MCP, API or CLI) when there is no NVIDIA GPU, when Cycles is slow, for long
  animations, or when the agent runs in the cloud without Blender. Tools: `scene_info`, `render_preview`,
  `render_estimate`, `render_final`, `render_status`, `render_download`. Presets: `product`, `turntable`, `animation`.
  New keys come with free GPU time; current amounts are at https://render.janction.jp/pricing?utm_source=skills.
- Do not edit the scene open in the user's Blender from a cloud job, and do not send a job to a paid service without
  telling the user the time and price first.

## Invariants (never change without asking)

- The render engine. Switching Cycles to EEVEE is faster and changes the look: soft shadows, glass, volumes and
  indirect light all shift. Explain the visible tradeoff and get an explicit yes.
- Lights, materials, world and volumes, color management (view transform, look, exposure), the camera and the
  compositor.
- The source file. Work on a copy (`bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)`); never overwrite the original.
- The frame range. If the user asks for 240 frames and the scene has 1-200, say so before rendering.

## Reporting

Report what was asked and what was delivered as separate numbers: "Asked: 240 frames. Scene range: 1-200. Delivered:
200/200 frames, 1920x1080, 30 fps, 6.67 s, 0 black frames." A critic or a job status saying `ok` is not proof; look at
the frames.
