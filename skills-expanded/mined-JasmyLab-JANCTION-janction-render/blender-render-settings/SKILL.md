---
name: blender-render-settings
description: Chooses and sets Blender render settings - Cycles or EEVEE, samples, adaptive sampling, denoising, light paths, motion blur and GPU devices - for previews and finals, and estimates render time from a measured frame. Use when a render is noisy, slow, too expensive, has fireflies, or when an agent must pick settings for a still or an animation.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-scene-preflight, blender-color-management, blender-animation-delivery
---

# Blender Render Settings

Preview cheap, finish right, and never trade the look for speed without asking. Samples, engine, clamping and bounce
limits all change what the picture looks like, not only how long it takes.

## Pick the engine

| Situation | Engine | Why |
|---|---|---|
| The user's scene already uses one | Keep it | Switching changes shadows, glass, volumes and bounce light |
| Photoreal stills, glass, liquids, interiors | Cycles | Path tracing gets indirect light and refraction right |
| Stylized, toon, motion graphics, quick drafts | EEVEE | Seconds per frame; good enough when the look is not physical |
| A draft of a long Cycles animation | EEVEE draft, labeled as a draft | Only to check timing and camera; never deliver it as the final |

Setting EEVEE from a script works across versions (the identifier changed between 4.x and 5.x):

```python
import bpy
s = bpy.context.scene
for engine_id in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
    try:
        s.render.engine = engine_id
        break
    except TypeError:
        pass
```

## Cycles: preview and final

| Setting | Preview | Final still | Final animation |
|---|---|---|---|
| `cycles.samples` | 16-64 | 256-1024 | 64-256 with denoising |
| `cycles.use_adaptive_sampling` / `adaptive_threshold` | on / 0.05 | on / 0.01 | on / 0.01-0.02 |
| `cycles.use_denoising` | on | on | on (check for flicker) |
| `cycles.max_bounces` | 4-8 | 12 (default) | 8-12 |
| `cycles.caustics_reflective/refractive` | off | on only for a glass or water hero | off |
| `render.use_persistent_data` | - | - | on (reuses BVH and textures between frames) |

```python
c = bpy.context.scene.cycles
c.samples = 128
c.use_adaptive_sampling = True
c.adaptive_threshold = 0.01
c.use_denoising = True
```

Look-changing levers. Ask before using them on the user's scene: lowering samples, `sample_clamp_indirect` (kills
fireflies and also dims bright bounce light), fewer bounces (darker interiors), turning off caustics or volumes,
`blur_glossy`. If fireflies appear, first look for a tiny bright light, an emissive surface or a caustic path.

Denoising across frames can shimmer on fine detail. Test 10 contiguous frames before a long render
(blender-animation-delivery).

## GPU on a local machine

```python
prefs = bpy.context.preferences.addons["cycles"].preferences
for kind in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
    try:
        prefs.compute_device_type = kind
        break
    except TypeError:
        pass
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type != "CPU"
bpy.context.scene.cycles.device = "GPU"
```

## EEVEE: what matters

`eevee.taa_render_samples` 64-256 for finals. Ray tracing (`eevee.use_raytracing`, Blender 4.2 and later) for reflections
and better contact light. Shadows and volumes cost time; check them at the final resolution, not only in a small preview.

## Estimate time from a measurement

Render one representative frame (or 10 contiguous frames for an animation) with the final settings at the final
resolution. Then: `time = seconds per frame x frames`, plus about 10 % for the first frame (scene load, BVH build).
Previews at lower samples or resolution do not scale linearly: noise, volumes and denoising cost differ. Tell the user
the measured number and how it was measured.

On JANCTION Render, `render_preview` is the cheap look and `render_estimate` gives time and price; estimate again after a
short final-settings test, because the measured time replaces the first guess. There, resolution, samples and engine are
arguments of `render_preview` and `render_final` (`width`, `height`, `samples`, `engine`); a scene script builds only the
scene, camera and frame range.
