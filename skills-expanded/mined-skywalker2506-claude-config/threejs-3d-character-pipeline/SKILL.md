---
name: threejs-3d-character-pipeline
description: Build game-ready 3D character asset pipelines for Three.js projects. Use when Codex is asked to create or plan imagegen master character/master pose references, convert a character image to an optimized textured 3D mesh with TRELLIS.2, prepare Blender MCP or Blender Python cleanup/rigging, make a model animatable with Make-It-Animatable or Mixamo animations, export GLB/FBX assets, or scaffold a localhost Three.js previewer with drag-and-drop, orbit inspection, skeleton view, animation list, play/pause, and scrub controls.
---

# Three.js 3D Character Pipeline

> **Bu depo icin hat ayrimi (2026-08-17):** 3D model/mesh/rig BU hattan.
> 2D sprite animasyonu icin
> **[/spritesheet-character-generator](../spritesheet-character-generator/SKILL.md)**,
> video icin **[/animate](../animate/SKILL.md)**, tek gorsel icin
> **[/gorsel-uret](../gorsel-uret/SKILL.md)**.
> Kararsizsan: **[/uretim-hatti-sec](../uretim-hatti-sec/SKILL.md)**.
>
> Bu hat ortak GPU kuyruguna GIRMEZ; proje icinde kendi araclariyla calisir.
>
> **Mesh mi kod mu:** bu hat **mesh** uretir (TRELLIS.2 + Blender + GLB) — gercekci
> yuzey, doku haritalari, standart rig. **[/img2threejs](../img2threejs-setup/SKILL.md)**
> ise **kod** uretir: primitive ve prosedurel shader'lardan kurulu, okunabilir,
> diff'lenebilir bir TS factory. Stilize/dusuk poli bir prop ya da karakter, sifir
> bagimlilik ve versiyonlanabilir kaynak istiyorsan img2threejs; foto-gercekci doku
> ve Mixamo rig'i gerekiyorsa bu hat.

## Overview

Use this skill to move from a character idea to a previewable animated Three.js asset without pretending heavyweight AI/Blender/Mixamo steps are available when they are not. The normal output is a project-local `buildable/characters/<name>/` work area plus final `public/assets/characters/<name>/` GLB/texture/animation files.

## Dependency Gate

Start by checking what is actually available:

```bash
node <this-skill>/scripts/check-character-pipeline-deps.mjs
```

If Blender MCP is requested, check the Blender MCP addon status first when that tool exists. If it is not connected, tell the user to open Blender, enable/start the MCP addon, or fall back to Blender Python/CLI. Do not claim rigging or scene edits were done through MCP unless Blender was reachable.

TRELLIS.2, Make-It-Animatable, Mixamo, and Blender are external systems. If their dependencies, credentials, model weights, or GUI steps are missing, prepare the plan, prompts, and previewer anyway, then list the missing install/action items.

## Core Workflow

1. Analyze the target game/project.
   - Read existing Three.js asset conventions, renderer scale, camera style, control style, target device, and polygon/texture budgets.
   - Decide whether the character is humanoid, creature, prop-like, stylized, realistic, low-poly, or high-poly.

2. Create master references with `imagegen`.
   - Generate a full-body master character image.
   - Generate a neutral master pose: A-pose or T-pose for humanoids, clean side/front cues for creatures, no cropped limbs, no busy background.
   - Save project-bound references under `buildable/characters/<name>/references/`.

3. Generate a 3D asset route.
   - Read `references/asset-pipeline.md` when choosing TRELLIS.2, Make-It-Animatable, Mixamo, Blender cleanup, or optimization settings.
   - Use TRELLIS.2 for image-to-3D mesh with PBR textures only when its local runtime or trusted external service is available.
   - Prefer a clean silhouette and animation-friendly neutral pose over dramatic concept art.

4. Optimize for game use.
   - Retopologize/decimate to the chosen budget while preserving silhouette and deformation loops.
   - Keep PBR textures, bake where needed, and cap texture sizes for the target.
   - Export GLB for Three.js and FBX only for Mixamo or Blender interchange.

5. Rig and animate.
   - For humanoids, use Make-It-Animatable when installed and suitable, or use Mixamo when the user can log in/upload/download.
   - Use Blender MCP/Blender Python for cleanup, origin/scale normalization, armature inspection, weight QA, animation import, and GLB export.
   - Use Mixamo animations as separate FBX/GLB clips and retarget/bake into the final character when possible.

6. Preview locally.
   - Run:

```bash
node <this-skill>/scripts/scaffold-threejs-character-previewer.mjs <target-project>
```

   - Start the generated Vite previewer, drag/drop GLB or GLTF files, rotate with mouse, inspect skeleton, choose animation clips, play/pause, and scrub time.

## Output Shape

```text
buildable/characters/<character>/
  character-plan.md
  prompt-pack.json
  generation-log.md
  references/
  trellis/
  blender/
  mixamo/
  previewer/
public/assets/characters/<character>/
  <character>.glb
  animations/
  textures/
```

Follow existing project conventions if they differ, but keep an audit trail in `buildable/characters/`.

## Quality Checklist

- Master pose has separated limbs and no hidden hands/feet for rigging.
- Mesh has sane scale, upright orientation, centered origin, no giant hidden geometry, and no avoidable holes.
- Polygon count fits target platform and camera distance.
- Texture maps are game-sized, power-of-two when useful, and not full of baked lighting artifacts unless the game wants that.
- Armature names, bind pose, weights, and animation clips survive GLB export.
- Three.js previewer loads the asset, shows animation names, plays clips, scrubs time, and displays skeleton helper.
- Final files are in the project, not only in AI tool temp folders or Blender autosaves.

## References

- `references/asset-pipeline.md` - TRELLIS.2, Make-It-Animatable, Mixamo, Blender, optimization, and export guidance.
- `references/previewer.md` - expected Three.js previewer behavior and QA checks.

## Scripts

- `scripts/check-character-pipeline-deps.mjs` - reports missing Node, Blender, glTF-Transform, TRELLIS.2, Make-It-Animatable, and Mixamo-adjacent dependencies.
- `scripts/plan-3d-character.mjs` - creates a project-local plan, prompt pack, output folders, and generation log.
- `scripts/scaffold-threejs-character-previewer.mjs` - creates a minimal localhost Three.js GLB/GLTF animation previewer.
