---
name: voxel-diorama
description: When asked for a voxel diorama, voxel room or MagicaVoxel-look scene as one offline HTML page: path-trace it with Crow's voxel kit -- never hand-write a ray tracer or shaders.
---

Crow ships a path-tracing kit: three.js 0.186.1 + three-gpu-pathtracer 0.0.24 (pre-built)
and `crow-voxel-kit`, a voxel grid + mesher + studio. It gives global illumination, soft
and contact shadows, colour bleeding and a lamp glow with no shader code of your own.
Kit folder: `@CROW_KITS@/pathtracer` (scaffold in `scaffold/`, API in `voxel-kit.js`).

The page opens in LIVE mode: the static island is path-traced and keeps converging while
the camera rests, and only the animated parts (`d.part`) are rasterised on top; your
`d.animate` callback runs every frame and the mouse orbits. PHOTO mode pauses the animation
at t and path-traces the whole frame, parts included, until it converges. Key P or the
small "Foto"/"Live" button switch. URL: `index.html?mode=photo&t=2` opens the photo of
t = 2 s, `?mode=live` the live view, `?mode=raster` the old flat raster preview (for the
motion check), `&ui=0` hides the button. Opened by a person, the page fills the window at
the display's pixel ratio (cap 2); with `ui=0` (Crow's captures, the checker) it keeps the
fixed `width` x `height` canvas. The kit is the only renderer code you need: no
OrbitControls, no EffectComposer, no shaders.

## Steps

1. Copy the scaffold. `read_file` `@CROW_KITS@/pathtracer/scaffold/index.html` and
   `.../scaffold/scene.js`, `write_file` them as `src/index.html` and `src/scene.js` in the
   working area. Do NOT copy `crow-pathtracer.js`: `build_bundle` resolves the bare imports
   `crow-voxel-kit` and `crow-pathtracer` to the kit itself.
2. Plan on paper first (a short list in your reply): grid size, a palette of named hex
   colours, every prop with its voxel box, every animated part. DENSITY RULE: a room is at
   least 64 voxels wide (walls ~48 high); every main prop is at least 8-16 voxels in each
   dimension. Coarse voxels make objects unreadable -- a 3-voxel chair is a blob.
3. NOT-EMPTY RULE. The references are dense: every patch of ground carries something. Plan
   and build at least:
   - **40 named props** (`g.prop`) of **12 or more kinds**, **60,000 voxels** in total;
   - **terrain coverage >= 0.5**: at least half of the ground's top cells have a prop above;
   - the small details, many of each: rocks, grass tufts, flowers, bushes, fences, barrels,
     crates, lanterns, paths/stepping stones, signs, birds, a bench, a well. A loop may
     place 30 tufts -- they count as 30 props but ONE kind (names ending in a number are
     one kind).
4. Write the scene in `src/scene.js`, content section only:
   - `const g = new VoxelGrid()`; `g.box(x0,y0,z0, x1,y1,z1, colour, kind)`, `g.put`,
     `g.cyl(cx,cz,r, y0,y1, ...)`, `g.blob(cx,cy,cz, rx,ry,rz, ...)`, `g.clear(...)`.
     y is up; corners inclusive. `colour` is `'#rrggbb'` or `(x,y,z) => colour|null`
     (use `hash(x,y,z)` for variation). `kind`: `'matte'` (default), `'metal'`, `'glass'`,
     `'emit'`.
   - Terrain (floor, island, cliffs) is built OUTSIDE any prop. Every object on it goes in
     `g.prop('crate', () => { g.box(...); ... })` -- the name, its voxel count and bbox are
     recorded; props may nest. Coverage is measured against the terrain, so an island built
     inside a prop has no terrain and coverage `null`.
   - `const d = createDiorama(g, { width: 1024, height: 1024, background: '#ddd6c8' })`.
     Night: a dark `background`, dark `domeTop`/`domeBottom`, `domeIntensity` ~0.15, a dim
     cool `keyIntensity`, and the lamps/spots carry the light.
   - Lamps: `d.addLamp({ x, z, bottom, top })` -- it builds the SOLID glowing shade and puts
     the spot light just below it. Build the pole/base yourself up to `bottom - 1`.
   - Daylight: `d.addAreaLight({ at: [x,y,z], lookAt: [x,y,z], intensity: 30, width: 18, height: 18 })`
     just outside a window opening.
   - A beam: `const beam = d.addSpot({ at: [x,y,z], lookAt: [x,y,z], angle: 12, intensity: 3000 })`
     (`angle` = half-angle in degrees). `addLamp`, `addAreaLight` and `addSpot` return the
     light's rig (a `THREE.Group` at `at`): `beam.rotation.y = t` sweeps it around `at`.
   - Animated parts: build each moving thing in ITS OWN grid (same voxel coordinates), then
     `const p = d.part('beam cone', partGrid, { pivot: [x,y,z] })` -> a `THREE.Group` that
     turns around `pivot` (default: the part's centre). One part per independently moving
     thing: one per firefly, one per water frame. A hidden part (`p.visible = false`) is
     left out of the photo too. `p.userData.home` is its start position (world units; one
     voxel = `d.voxelSize`).
   - `d.animate((t, dt, scene) => { ... })` runs every live frame and once at the photo's
     t. Drive everything from `t` (seconds): `beam.rotation.y = t * 0.8`,
     `frames.forEach((f, i) => f.visible = i === Math.floor(t * 6) % frames.length)`,
     `fly.position.y = fly.userData.home.y + 0.3 * Math.sin(t * 2 + i)`.
     NEVER `Date`, `Math.random` or your own timers: Crow captures animation at a frozen,
     stepped page clock, and only `t` moves with it. Use `hash(i, 0, 0)` for per-particle
     variety.
   - `d.start()` last. It throws, with the reason, on anything that would render wrong.
5. Build: `build_bundle` entry `src/index.html`, out `index.html`. That one file is the
   deliverable; it opens offline from file://. Edit `src/`, build again, never patch
   `index.html`.
6. Verify:
   - Motion: `render_page` `index.html?mode=raster&ui=0`, `frames` 4, `frame_ms` 500,
     `width`/`height` = the canvas size. `read_image` the contact sheet: the beam, the water
     and the particles must be in different places in the 4 frames.
   - Photo: `render_page` `index.html?mode=photo&t=2&ui=0`, `wait_ms` 20000, one frame.
     Night or dark scenes with small lights need more samples: use `wait_ms` 60000-120000
     (60-120 s; kit pages may wait up to 120000; ~15 samples/s at 1024^2). Never shrink the scene to
     fit a short capture -- the page itself keeps converging in the browser.
     Read the console lines:
     - `renderer:` must name the GPU (NVIDIA/AMD/Intel), not SwiftShader/llvmpipe;
     - `[crow-pt] samples=` should be >= 200 at 20 s (measured ~15 samples/s at 1024x1024 on
       an RTX 5090; 60k triangles cost the same as 9k); `lost=0`, or a restore followed;
     - `[crow-scene] {...}`: `props`, `propKinds`, `voxels`, `coverage`, `parts`,
       `animated`, `errors` -- hold them against the NOT-EMPTY targets.
     Then `read_image` the photo and check, item by item, against the user's reference
     image if there is one: colour bleeding, dark contact shadows in creases, soft shadow
     edges, a warm light pool under each lamp, a clean background, no grain or bright specks,
     every prop recognisable by name, no bare patch of ground.
   - The whole check in one command (a goal's `check:`):
     `python3 @CROW_KITS@/pathtracer/check_diorama.py index.html` -- PASS/FAIL per check
     (gpu, samples, props, kinds, voxels, coverage, motion, repeat, photo, errors), exit 0
     only when all pass. It borrows VRAM from the local crow-nest serve like a Crow turn:
     `--serve URL` (default `$CROW_SERVE_URL`, else http://127.0.0.1:8099/v1; `none` =
     never borrow). Dark scenes: add `--wait-ms 90000 --min-samples 1000`.
   `window.__SCENE__` (voxels, props with bbox, coverage, parts, animated, mode) and
   `window.__PT__` (samples, samplesPerSecond, fps, renderer, lost) hold the same numbers.
7. Fix what the check found in `src/scene.js` and repeat 5-6. Change content and light,
   not the kit.

## Traps (each one measured, 2026-09-25)

- vertexColors: the room rendered BLACK in 1 of 3 starts. The kit makes one material per
  palette colour; never add a mesh with `vertexColors`, InstancedMesh or a non-Standard
  material (`start()` refuses them).
- A spot light inside a hollow lamp shade: persistent fireflies (PSNR 30.6 dB); below a
  solid shade: 38.6 dB. Use `addLamp`, do not place lamp lights by hand; put an `addSpot`
  beam outside the lantern glass, in front of solid voxels.
- Bright emissive voxels are fireflies (the library does not importance-sample them).
  Keep `emit` dim (the kit caps emissiveIntensity at 1) and light with lamps/spots/area
  lights. Fireflies/particles may be `emit` voxels; they glow, they do not light.
- Animation from `Date.now()`, `Math.random()` or `setInterval` counters: the 4 preview frames
  do not repeat and Crow's motion check cannot trust them. Only `t` (and `dt`).
- The source page `src/index.html` shows nothing from file:// (module imports are
  blocked). Always render the built `index.html`.
- `build_bundle` needs an esbuild on this machine. If it reports none, tell the user --
  do not concatenate the library by hand.
