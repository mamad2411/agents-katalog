---
name: blender-pro
description: Pro-level Blender guidance — hard-surface & organic modeling, PBR texturing/baking, Rigify rigging, animation, Geometry Nodes, and bpy scripting for automation and export pipelines (glTF/FBX/USD).
---

# blender-pro

## Purpose
Expert guidance for production-grade 3D work in Blender 4.x: modeling, UV, texturing, shading, baking, rigging, animation, simulation, Geometry Nodes, and Python (`bpy`) scripting. Use for asset creation, render setup, and build/export pipelines feeding web (Three.js / React Three Fiber / Spline) or game engines.

## Capabilities

### Modeling
- Hard-surface with boolean + bevel workflow (Bool Tool, Hard Ops/BoxCutter patterns)
- Subdivision surface modeling with correct edge flow, support loops, and crease usage
- Retopology via shrinkwrap + poly build, or Quad Remesher
- Sculpting with multires, dyntopo, and layered detail
- Non-destructive stacks (modifiers: Mirror → Array → Bevel → Subdivision → Weighted Normal)

### UV & Texturing
- UV unwrap strategies: seam planning, island packing, UDIM for film/hero assets
- PBR material authoring in Principled BSDF (Metallic/Roughness workflow)
- Texture baking: normal, AO, curvature, cavity, position, thickness → for use in Substance Painter, Mixer, or in-Blender painting
- Procedural materials with node groups + color ramps + Musgrave/Voronoi/Noise
- Displacement: true (adaptive subdivision + displace node) vs. bump/normal only

### Rigging & Motion
- Rigify meta-rigs (human, bird, cat, quadruped) + generated control rigs
- Custom bone setups: IK/FK switching, stretchy IK, pole targets, constraints chain
- Weight painting + automatic weights + bone envelopes
- Shape keys + drivers for facial animation
- NLA editor for layered/clipped animation (locomotion cycles, additive layers)
- Physics/motion: cloth, soft body, rigid body, hair, grease pencil animation
- Procedural animation via drivers, constraints, and Geometry Nodes

### Geometry Nodes (4.x)
- Scattering (trees, rocks, crowd systems) with instancing
- Procedural modeling (cables, greebles, modular walls)
- Simulation Zones for physics-like behavior (flocks, fluid-esque flow)
- Field-based attribute manipulation (capture, interpolate, domain conversion)

### Rendering
- **Cycles**: samples, adaptive sampling, denoising (OptiX/OIDN), light portals, light groups
- **Eevee Next**: screen-space/raytraced GI, light probes, virtual shadows
- Compositor: glare, lens distortion, vignette, color grading, AOV passes
- Camera: depth of field (f-stop driven), motion blur, anamorphic

### Export & Pipelines
- glTF 2.0 for web (Three.js / R3F / Spline / model-viewer) — Draco/Meshopt compression
- FBX for Unity/Unreal
- USD/USDZ for cross-DCC and AR
- Alembic for heavy cached sims
- Scripted batch export via `bpy`

### Python / bpy Automation
- Headless rendering: `blender -b scene.blend -o //out/ -f 1`
- Batch processing scenes, material remapping, asset library generation
- Custom operators, panels, add-ons
- Import/export pipeline scripts

## Instructions

1. **Ask which output target first** — web (glTF, tight polycount, baked lighting), film (Cycles, UDIM, hero asset), or game (FBX/USD, LODs, clean topology). This changes every downstream decision.
2. **Favor non-destructive workflows.** Use modifier stacks, shape keys, Geometry Nodes, and linked data so changes stay editable.
3. **Poly budget discipline.** For web: hero model ≤ 50k tris, environment props ≤ 5k tris each. Bake high-poly detail into normal maps.
4. **PBR is authoritative.** Only use Principled BSDF unless the target engine requires custom shaders. Keep textures in linear color space except base color (sRGB).
5. **Rigging parity.** If exporting to web/engine, test rig compatibility early — glTF supports skeletons + morph targets; custom constraints do not export.
6. **Scripted reproducibility.** For anything repeated more than twice (rename, export, material swap), write a `bpy` snippet instead of manual clicking.
7. **Version with care.** `.blend` files are binary — keep iterations (`scene_v03.blend`) and export human-readable siblings (`.glb` + `.json` material manifests) for review.
8. **Reference assumed versions.** Blender 4.2+ LTS, Principled BSDF v2, Eevee Next, Geometry Nodes with Simulation Zones.

## Usage Examples

### 1. Batch glTF export via bpy
```python
import bpy, os

OUT = "/Users/you/exports/"
os.makedirs(OUT, exist_ok=True)

for coll in bpy.data.collections:
    if not coll.name.startswith("export_"):
        continue
    # isolate collection
    bpy.ops.object.select_all(action='DESELECT')
    for obj in coll.all_objects:
        obj.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(OUT, f"{coll.name}.glb"),
        use_selection=True,
        export_format='GLB',
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_apply=True,          # apply modifiers
        export_animations=True,
        export_skins=True,
        export_morph=True,
    )
```

### 2. Non-destructive hard-surface modifier stack
```
Mirror (X)
└─ Array (count driven by empty)
   └─ Bevel (weight-based, limit method: Angle 30°)
      └─ Subdivision Surface (viewport 2 / render 3)
         └─ Weighted Normal (keep sharp)
```

### 3. Rigify quadruped setup (checklist)
- Add meta-rig: `Add → Armature → Rigify → Quadrupeds → Cat/Wolf`
- Align bones to mesh in Edit Mode (do NOT apply scale until done)
- Apply scale + location on both mesh and armature before `Generate Rig`
- Parent mesh with Automatic Weights; fix weights via Weight Paint → Bleed/Smooth
- Pose test extreme keyframes (shoulder lift, spine twist) before baking anim

### 4. PBR bake setup for glTF
```
High-poly → Low-poly (shrinkwrap-retopo'd)
Cage: duplicate low-poly + solidify 0.02
Bake passes:
  - Normal (tangent space) → _normal.png (linear, Non-Color)
  - AO → _ao.png (Non-Color)
  - Diffuse (direct/indirect OFF, color ON) → _basecolor.png (sRGB)
  - Roughness → _roughness.png (Non-Color)
Combine AO*Diffuse in compositor if target shader lacks AO slot
```

### 5. Geometry Nodes scatter (procedural rocks)
```
Distribute Points on Faces (density attribute)
→ Instance on Points (rock collection, pick random)
→ Rotate Instances (random Euler, axis-weighted)
→ Scale Instances (random, clamped 0.4–1.6)
→ Realize Instances (only before export — keeps viewport fast)
```

### 6. Sine-driven procedural motion via driver
```python
# On object.location.z
# Driver expression:
sin(frame / 10) * 0.5 + var   # var = another object's Z for chained motion
```

### 7. Headless batch render
```bash
blender -b shot_010.blend \
  -E CYCLES \
  -o //renders/shot_010_#### \
  -F PNG \
  -s 1 -e 240 -a
```

### 8. Export-for-web checklist
- [ ] Apply all transforms (`Ctrl+A → All Transforms`)
- [ ] Merge by distance (0.0001) — remove duplicate verts
- [ ] Recalculate normals outside (`Shift+N`)
- [ ] Smooth shading + Auto Smooth 30° OR custom normals
- [ ] Bake lighting to vertex colors or lightmap UV (channel 2) if static
- [ ] Compress textures: KTX2/Basis for glTF, max 2K for hero, 1K for props
- [ ] Strip unused materials/images via `File → Clean Up → Purge Unused`
- [ ] Test in `gltf-viewer` or `model-viewer` before handoff
