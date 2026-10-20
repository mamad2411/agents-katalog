---
name: 3d-game-design
description: Master orchestrator for 3D/2D game development — engine selection, architecture, asset pipelines, physics, multiplayer, and deployment. Routes to 10 Three.js sub-skills and 7 reference guides.
---

# 3D Game Design — Master Skill

## Engine Selection Decision Tree

```
What type of game?
├─ 3D
│  ├─ Complex (physics, large worlds, multiplayer)
│  │  ├─ React app? → React Three Fiber (r3f) + Rapier
│  │  └─ Vanilla JS? → Three.js + Rapier
│  ├─ Simple 3D (product viewer, portfolio, WebXR)
│  │  └─ Three.js or Babylon.js
│  └─ AAA-like (PBR, particles, terrain)
│     └─ Babylon.js or PlayCanvas
├─ 2D
│  ├─ Complex (platformer, RPG, tilemap-heavy)
│  │  └─ Phaser 3
│  └─ Simple (UI-heavy, cards, casual)
│     └─ PixiJS v8
└─ Mixed 2D+3D → Three.js with CSS2DRenderer overlay
```

Load `references/engine_selection_guide.md` for the full feature matrix and benchmarks.

## Sub-Skill Delegation

| Task Category | Delegate To |
|---|---|
| Scene setup, cameras, coordinate systems | `threejs-fundamentals` |
| Built-in shapes, BufferGeometry, instancing | `threejs-geometry` |
| PBR materials, MeshStandardMaterial, envmaps | `threejs-materials` |
| Directional/point/spot lights, shadows | `threejs-lighting` |
| Texture loading, UV mapping, cubemaps | `threejs-textures` |
| Keyframe/skeletal animation, AnimationMixer | `threejs-animation` |
| GLTF/FBX/OBJ loading, DRACOLoader | `threejs-loaders` |
| GLSL shaders, ShaderMaterial, uniforms | `threejs-shaders` |
| Bloom, DOF, SSAO, EffectComposer | `threejs-postprocessing` |
| Raycasting, controls, mouse/touch input | `threejs-interaction` |

## Game Development Lifecycle

1. **Concept** — Choose engine (decision tree above), define scope
2. **Prototype** — Scaffold project: `python scripts/scaffold_project.py <engine> <name>`
3. **Assets** — Model in Blender → export GLTF → compress: `python scripts/asset_pipeline.py audit ./assets`
4. **Code** — Implement game loop, ECS, physics, input (load `references/game_architecture_patterns.md`)
5. **Polish** — Post-processing, audio, particles, UI overlay
6. **Deploy** — Build + package: `python scripts/build_deploy.py package-pwa`

## Script Quick-Reference

```bash
# Scaffold a new project
python scripts/scaffold_project.py r3f my-game --features physics,audio

# Audit assets for optimization opportunities
python scripts/asset_pipeline.py audit ./assets

# Compress GLTF files with Draco + KTX2
python scripts/asset_pipeline.py compress ./models --draco --ktx2

# Batch export from Blender
python scripts/blender_batch.py export scene.blend --output ./models

# Generate LOD chain
python scripts/blender_batch.py generate-lods character.blend --levels 3

# Build and package for itch.io
python scripts/build_deploy.py package-itch --output ./dist

# Generate optimized Vite config
python scripts/build_deploy.py configure --engine r3f --features wasm,hdr
```

All scripts support `--help` for full usage details.

## Reference Index

| When You Need | Load This Reference |
|---|---|
| Engine comparison, choosing technology | `references/engine_selection_guide.md` |
| Game loops, ECS, state machines, scenes | `references/game_architecture_patterns.md` |
| Blender modeling → web export workflow | `references/blender_to_web_pipeline.md` |
| Draco, KTX2, LOD, texture/poly budgets | `references/asset_optimization_guide.md` |
| React Three Fiber, drei, Zustand, Rapier | `references/r3f_ecosystem_guide.md` |
| Physics engines, procedural generation | `references/physics_and_procedural_guide.md` |
| Multiplayer, netcode, WebRTC, lobbies | `references/multiplayer_networking_guide.md` |

## Asset Configs

- `assets/configs/vite.game.config.ts` — Reference Vite config with WASM, GLB, HDR, KTX2 support
- `assets/configs/draco-compress.json` — Draco quality presets (low/medium/high/ultra)
- `assets/configs/ktx2-compress.json` — KTX2/Basis Universal presets by texture type
- `assets/configs/blender-export-presets.json` — GLTF export operator presets for Blender

## Project Templates

Scaffold with `python scripts/scaffold_project.py <engine> <name>`:

- **threejs** — Vanilla Three.js + Vite + TypeScript
- **r3f** — React Three Fiber + drei + Zustand
- **phaser** — Phaser 3 with Boot/Game/UI scenes
- **pixijs** — PixiJS v8 application starter
- **babylon** — Babylon.js with inspector toggle
