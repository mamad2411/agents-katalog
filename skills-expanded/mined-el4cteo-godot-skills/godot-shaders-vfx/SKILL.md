---
name: godot-shaders-vfx
description: Shaders and VFX in Godot 4.7 - shading language (spatial, canvas_item, particles, sky, fog), instance/global uniforms, screen/depth textures, stencil_mode, includes, ready effects (dissolve, outline, water, toon), GPU particles, compositor effects, shader stutter fixes, headless shader validation. Use for .gdshader files, materials effects or particles.
license: MIT
compatibility: Godot 4.7+. Python 3.9+ for scripts/shader_check.py.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Shaders and VFX (4.7)

**Validate after every edit:** `python scripts/shader_check.py [paths]` compiles each `.gdshader` with the engine's shader compiler, headless, and returns `{file, line, msg}`. Errors inside `#include`d `.gdshaderinc` files point at the include. Looks still need a real GPU, so ask the user to check them visually.

## Shading language essentials
- The first line is `shader_type spatial | canvas_item | particles | sky | fog;`. Entry points are `vertex()`, `fragment()`, `light()` (custom lighting) and `start()/process()` (particles).
- `render_mode` (spatial): `unshaded`, `cull_disabled`, `depth_draw_always`, `blend_add`, `diffuse_toon`, `specular_toon`, `world_vertex_coords`, … An invalid mode is a compile error, so the checker catches it.
- Uniform hints: `source_color` (**required on color and albedo textures**, or colors come out wrong), `hint_range(a, b, step)`, `hint_normal`, `hint_default_white/black`, `filter_nearest`, `repeat_enable`. Group them in the inspector with `group_uniforms Name;` … `group_uniforms;`.
- Screen reads: `uniform sampler2D s : hint_screen_texture, filter_linear_mipmap;`, `hint_depth_texture` and `hint_normal_roughness_texture` (Forward+). They replace `SCREEN_TEXTURE`/`DEPTH_TEXTURE` from Godot 3. canvas_item screen reads need a `BackBufferCopy` only when several effects stack.
- Per-instance values without duplicating materials: `instance uniform float flash;` set with `set_instance_shader_parameter("flash", 1.0)` (3D). Project-wide values: `global uniform vec4 wind;` declared in Project Settings → Shader Globals and set with `RenderingServer.global_shader_parameter_set`.
- `varying` passes data from vertex to fragment. `#include "res://shaders/lib.gdshaderinc"`, `#define` and `#ifdef` work. Godot shaders are GLSL-like but not GLSL: there are no `in`/`out` globals, and built-ins are UPPERCASE (`ALBEDO`, `UV`, `VERTEX`, `NORMAL`, `TIME`, `SCREEN_UV`, `MODEL_MATRIX`, `INV_VIEW_MATRIX`).
- **Stencil (4.5+):** `stencil_mode write, compare_always, 1;` on the mask material, `stencil_mode read, compare_equal, 1;` on the revealed one (portals, x-ray, outlines). StandardMaterial3D has ready-made `STENCIL_MODE_OUTLINE`/`XRAY` presets.
- Visual shaders are for artists. When writing shaders as an agent, use text `.gdshader` files: they're diffable and checkable.

## Particles
- Use `GPUParticles2D/3D` + `ParticleProcessMaterial` by default (they work on all renderers in 4.x). Use `CPUParticles*` only for exact CPU control or many tiny emitters in the Compatibility renderer (convert with `convert_from_particles`).
- One-shot bursts: `one_shot = true`, `explosiveness = 1`, `emitting = true`, then free on `finished`. Pre-warm ambient effects with `preprocess`.
- Shape the effect with `emission_shape`, `color_ramp` (Gradient), `scale_curve`, `turbulence_enabled`, sub-emitters (on collision or end) and trails (`trail_enabled` + ribbon or tube mesh). 4.7 adds 3D particle scale and rotation: `use_scale_3d`, `use_rotation_3d`.
- Collision: `collision_mode` on the material, plus `GPUParticlesCollisionBox3D/Sphere3D/SDF3D/HeightField3D` nodes in the level. Attractors: `GPUParticlesAttractor*3D`.
- Set `visibility_aabb`/`visibility_rect` large enough, or particles pop out of view (Particles menu → Generate AABB). Use `amount_ratio` to scale intensity without a restart.
- Spawn from code: `emit_particle(xform, velocity, color, custom, flags)` with `amount` as the pool size, for impacts at arbitrary points.

## Post-processing
- Simple: a full-screen `ColorRect` (canvas_item shader with `hint_screen_texture`) on a `CanvasLayer`. That's enough for vignettes, CRT and color grading LUTs.
- Proper 3D post: `Compositor` + `CompositorEffect` (experimental; Forward+ and Mobile) running a compute shader through `RenderingDevice` at `EFFECT_CALLBACK_TYPE_POST_TRANSPARENT` and similar points. See the reference skeleton.
- Prefer Environment features (glow, fog, adjustments with a LUT, DOF) before writing custom post effects.

## Shader stutter (first-time compile hitches)
- 4.4+ uses ubershaders and pipeline precompilation automatically.
- 4.5+ has the **shader baker**: turn on the export option `shader_baker/enabled` per preset (`api_lookup.py --search shader_baker`). It pre-compiles for the target driver, with much faster first loads on D3D12 and Metal.
- Keep the number of unique shaders and material variants low. Toggling `#define`-style features at runtime creates new pipelines. Uniform changes are free.

## Common effects (see the reference)
dissolve with an edge glow, hit flash (instance uniform), 2D outline, spatial rim and fresnel, scrolling-UV water with depth fade, toon `light()`, vertex wind sway with a global uniform, full-screen vignette, stencil x-ray.

Shader library (validated by shader_check in the tests): [references/shaders.md](references/shaders.md). VFX scripts (impact burst, flash driver, compositor effect skeleton): [references/vfx.md](references/vfx.md)
