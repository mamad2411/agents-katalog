---
name: godot-3d-rendering
description: 3D look in Godot 4.7 - renderer choice (Forward+/Mobile/Compatibility matrix), Environment (AgX, glow, fog, SSAO/SSR/SDFGI), lights incl. AreaLight3D, GI (SDFGI, VoxelGI, LightmapGI), HDR output, materials, glTF/Blender import suffixes, LOD and occlusion culling. Use for 3D scenes, lighting, materials, model import or visual quality.
license: MIT
compatibility: Godot 4.7+.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# 3D rendering (4.7)

Shaders and VFX are in `godot-shaders-vfx`, and frame-time work is in `godot-performance`. Headless runs don't render, so ask the user for screenshots, or use a Godot MCP screenshot tool if one is connected.

## Pick the renderer first (`rendering/renderer/rendering_method`)
| Feature | Compatibility | Mobile | Forward+ |
|---|---|---|---|
| Targets | web (the only option), low-end | phones and tablets, **XR (recommended)** | desktop and console |
| SDFGI, VoxelGI, SSR, SSIL, volumetric fog, TAA, FSR2 | no | no | yes |
| LightmapGI | render only (bake on RD hardware) | yes | yes |
| SSAO | yes | no | yes |
| Decals, compositor effects, HDR 2D, DOF blur | no | yes | yes |
| Glow, fog (depth and height), tonemapping, MSAA 3D | yes | yes | yes |
| Omni and spot lights per mesh | 8 | 8 (256 per view) | clustered, 512 per cluster |
| AreaLight3D shadows | none | approximate penumbra | PCSS |
Set a per-platform override with `rendering_method.mobile`. Check the current choice with `project_inspect.py`. Windows uses D3D12 by default for new projects (4.6+), and macOS/iOS use Metal.

## Environment recipe (WorldEnvironment → Environment)
- Sky: `Sky` + `ProceduralSkyMaterial` (stylized), `PhysicalSkyMaterial` (realistic, pairs with physical light units) or `PanoramaSkyMaterial` (HDRI). Set background mode Sky and ambient/reflected light from the sky.
- Tonemap: `TONE_MAPPER_AGX` for natural highlights (tune `tonemap_agx_white`/`tonemap_agx_contrast`, 4.6+). Use Filmic/ACES only to match an existing look.
- Glow: since 4.6 it blends before tonemapping and defaults to Screen mode with lower intensity. Keep `glow_intensity` low and use emissive materials with energy above 1 for bloom.
- Forward+ extras: SSAO and SSIL (contact shadows, bounce), SSR (wet floors; it had a big rework in 4.6, with a half-resolution option), volumetric fog plus `FogVolume` for light shafts, and SDFGI for large dynamic GI.
- `CameraAttributesPractical` (DOF, auto exposure) or `CameraAttributesPhysical` (real f-stop, shutter and ISO) go on the WorldEnvironment or the Camera3D.

## Lights and shadows
- `DirectionalLight3D` (sun): `directional_shadow_mode` PSSM 4 splits. Keep `directional_shadow_max_distance` as small as the game allows (100–200 m), because that improves shadow resolution.
- Omni and spot lights: turn shadows on only for the lights that matter. Use `distance_fade_*` for lights far away.
- **`AreaLight3D` (4.7):** rectangular soft light from screens, windows and neon. Set `area_size`, an optional `area_texture` and `area_normalize_energy`. It costs more than omni or spot lights, so use few of them.
- Static lights are baked into `LightmapGI` with `light_bake_mode = BAKE_STATIC`. Dynamic lights stay `BAKE_DYNAMIC`.

## Global illumination choice
| Need | Use |
|---|---|
| Static level, best quality, any renderer except Compatibility baking | `LightmapGI` (bake in the editor; needs UV2: enable "Lightmap UV" on import) |
| Dynamic objects in a mid-size static area | `VoxelGI` (bake, Forward+) |
| Huge or open world, time of day, no baking | SDFGI (Environment, Forward+) |
| Reflections on shiny surfaces | `ReflectionProbe` (set `interior` for indoor areas), plus SSR |
Combine them: lightmaps for static lighting, light probes or VoxelGI for dynamic objects, and ReflectionProbes everywhere glossy.

## Materials (StandardMaterial3D / ORMMaterial3D)
- ORM-packed textures go in `ORMMaterial3D`. Albedo is sRGB. Normal, ORM and roughness maps import as linear (Godot detects normal maps when you assign them).
- Transparency: prefer `TRANSPARENCY_ALPHA_SCISSOR` or `ALPHA_HASH` (foliage, depth-sorted for free). Use `ALPHA` only for glass and VFX, because it causes sorting issues and no shadows.
- Use `material_override` (whole mesh) and `set_surface_override_material(i, m)` per instance. Don't edit a shared material at runtime unless every user should change. `duplicate()` it first.
- Stencil (4.5+): `stencil_mode = STENCIL_MODE_OUTLINE` or `STENCIL_MODE_XRAY` gives outlines and see-through-walls without custom shaders.
- `Decal` nodes project on any surface (not in Compatibility).

## Import (glTF 2.0 / .glb preferred)
- In Blender, export GLB with +Y up and applied transforms. Godot imports to `.godot/imported`. Configure through the Import dock or the "Advanced Import Settings" (per-mesh LOD, collisions, materials, animation clips).
- Name suffixes in the source file create nodes automatically: `-col`, `-convcol`, `-colonly`, `-convcolonly` (collision), `-rigid`, `-navmesh`, `-occ`/`-occonly` (occluders), `-noimp` (skip), `-loop`/`-cycle` (looping animation).
- Importing `.blend` directly needs Blender installed and `filesystem/import/blender/enabled`. Use GLB in CI.
- Keep edited materials across reimports with the scene import option `materials/extract = 1` (Extract Once), or Advanced Import → per-material "Save to file". List all import options with `api_lookup.py ResourceImporterScene`.
- For asset creation and export from Blender, see the `blender-export-pipelines` skill if it's installed.

## Scaling detail
- Automatic mesh LOD is generated on import. Tune it per viewport with `mesh_lod_threshold`, where higher values are more aggressive.
- `visibility_range_begin/end` (+ fade) handles HLOD and impostors and culls far props.
- Occlusion culling: enable `rendering/occlusion_culling/use_occlusion_culling`, add `OccluderInstance3D`, and bake. It helps indoor and urban scenes.
- Resolution scaling: `Viewport.scaling_3d_mode` (FSR 1, FSR2 on Forward+, MetalFX on Apple) plus `scaling_3d_scale`. Anti-aliasing: MSAA 3D, `screen_space_aa` (FXAA, SMAA 4.5+) or TAA (Forward+).

## HDR output (4.7)
Turn on `display/window/hdr/request_hdr_output` (or `Window.hdr_output_requested`). It's supported on Windows, macOS, iOS, visionOS and Linux Wayland, and falls back to SDR automatically. Check `DisplayServer.window_is_hdr_output_supported()` and expose a toggle and brightness options in settings.

Environment, lighting presets, material and LOD code (compiled by the tests): [references/recipes.md](references/recipes.md)
