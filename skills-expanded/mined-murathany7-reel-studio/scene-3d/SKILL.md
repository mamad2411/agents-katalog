---
name: scene-3d
description: Build a 3D shot for a video - live in the composition with Three.js (engines/three.js) or as a pre-rendered Blender plate (engines/blender). Covers toon, photoreal and neon looks, product and CAD models, camera moves, physics, and keeping every frame deterministic.
---

# 3D shots

## Three.js (live layer)

- Use `threeLayer(el, { update(t), background, fov })` from `/engines/three.js`. Add an import map for `three`
  (see `examples/engines-demo/index.html`).
- `update(t)` sets every transform from `t`. Camera moves: keyframe with a GSAP tween on a plain object
  (`tl.to(cam, { x: 4, z: 8, duration: 2 }, 3)`) and copy it into `camera.position` in `update`.
- Models: `GLTFLoader` from `three/addons/loaders/GLTFLoader.js` (add `"three/addons/": "/core/node_modules/three/examples/jsm/"`
  to the import map). Wrap the load in `Studio.wait(...)`. Put model files in the brand's `assets/models/` or the production's `composition/`.
- The look (`looks/README.md`) decides the rendering style; the same model can go any of these ways:
  - Cartoon (`looks/toon-3d`): `toon(color, { steps })` + `outline(mesh, { thickness })`. Hard light: one `DirectionalLight` + low `AmbientLight`.
  - Realistic (`looks/photoreal`): `await realistic(renderer, scene)` (wrap in `Studio.wait`: ACES tone mapping, a
    studio environment for reflections, soft shadows) + `pbr(color, { metalness, roughness, clearcoat })`. A key light
    with `castShadow`, a cool rim light from behind, a `ShadowMaterial` floor over a CSS gradient. Keep the camera
    above grazing angles (glossy faces turn white), move slowly, render the final with `Studio.setup({ motionBlur: true })`.
  - Neon (`looks/neon-noir`): `emissive(color, intensity)` + `threeLayer(el, { post: bloom({ strength, threshold }) })`,
    `scene.fog`. Keep `threshold` ≥ 0.2 and emissive ≤ 2 or everything blooms white.
- Animated GLB clips: create an `AnimationMixer`, then in `update` call `mixer.setTime(t - start)`. Never `mixer.update(delta)`.
- HTML tags that follow 3D points: in `update(t)`, call `camera.updateMatrixWorld()` and the parent's
  `updateMatrixWorld()` before `vector.applyMatrix4(obj.matrixWorld).project(camera)`. Three.js refreshes these only
  inside `render()`, so without it a tag follows the previous frame. Example: `productions/bike-logger/REEL-002-engines`.
- CAD meshes as JSON (vertices + indices): `toNonIndexed()` + `computeVertexNormals()` gives crisp flat facets.
  Render with `threeLayer(..., { pixelRatio: 2 })` for supersampled edges.
- Physics: bake it (simulate at a fixed 1/120 s step into an array before the first frame) and look up by `t`.
- Talking character: load `/engines/lipsync.js` and the line's `.visemes.js` (from `scripts/lipsync.sh`) with
  classic `<script>` tags, then in `update(t)`: `LipSync.paramsAt(cues, t, "mouth", { offset })` → `{ open, wide,
  round }` (0…1) onto morph targets (`mesh.morphTargetInfluences`) or a mouth mesh's scale. See `engines/README.md`,
  *Lip sync*.

## Blender (plate)

- A scene script defines `build(ctx)`; copy `engines/blender/example_scene.py`. `ctx` gives `toon(rgb)`,
  `key(obj, "location", t, value)`, `size`, `fps`, `duration`, `frames`, `scene`.
- Render: `engines/blender/render.sh scene.py composition/plates/<name>.mp4 --size 1080x1920 --duration 4 [--engine EEVEE|CYCLES|WORKBENCH]`.
  Draft at `--size 540x960`, final at full size.
- Backdrop colour: show it to the camera only (Light Path "Is Camera Ray" mix, as in the example), or it lights the
  scene and flattens toon bands.
- Colour management is set to *Standard* so brand hex colours come out as typed. For a photoreal plate, switch to
  `ctx["scene"].view_settings.view_transform = "AgX"` in `build`, render with `--engine CYCLES`, and use area lights
  and camera depth of field.
- Physics and simulations: bake them in the scene script before rendering.
- Talking character: `import lipsync as L` in the scene script (`run.py` puts `engines/blender/` and the script's
  own folder on the path), `cues = L.load("productions/…/audio/vo.visemes.json")`, then
  `L.key_shape_keys(head, cues, ctx, offset=VO_START)` keys shape keys `open`, `wide`, `round` on every frame
  (`names={"open": "Jaw"}` for other names). Anything else: `L.params_at(cues, t, offset=…)` per frame with `ctx["key"]`.
- In the composition: `<video src="plates/<name>.mp4">` + `Studio.video(el, { start })`. Plates have no alpha; put
  text and characters on top with HTML layers.

## Check

Render the key beats as stills and look at them. For Three.js, render one frame twice and compare md5s. Note render
times in the production log.
