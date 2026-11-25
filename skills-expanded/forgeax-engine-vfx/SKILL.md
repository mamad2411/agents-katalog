---
name: forgeax-engine-vfx
description: ForgeAX code-first GPU VFX authoring, cooking, playback, and rendering. Use when creating, loading, debugging, or extending particle, ribbon, trail, beam, billboard, or mesh effects.
---

# ForgeAX VFX

## Choose the path first

| Effect | Path |
|:--|:--|
| Rain, snow, sparks, bubbles, dust or sandstorm, fire, smoke, magic motes; up to a few thousand particles per field; behaviour written in game TypeScript | `Points` sprites on a `point-list` mesh, moved with `writeRange` each frame (particles-core). No shader, no cook. |
| Tens of thousands of particles, GPU scene collision, force fields, ribbons, trails, beams, mesh particles, event sub-emitters | Cooked GPU VFX below. |

`Points` take a world (`sizeUnits: world`) or pixel size, square, circle or `soft`
(radial glow) sprites, per-point `color` (alpha fades) and `uv1.x` size streams, the
material texture across each sprite and the material's blend and depth-write state.
That covers Three.js `Points`/`PointsMaterial` effects; do not fake particles with pools
of small meshes. Switch to the GPU path when the CPU loop or its per-frame upload shows
up in a profile, or when the behaviour needs GPU-side data.

## Render happy path

VFX is a producer of a closed `RenderFeaturePlan` in the single
`RenderScene -> Standard Pipeline -> DeviceScope -> FrameReceipt`
path. The host performs `attach` and `draw`; use receipt-bound `inspect`,
`observe`, and `recover` for diagnostics. VFX never owns device, queue,
encoder, finish, or submit.

Use one path:

1. Author schema-v3 emitter metadata with `program: { module }`, required fixed bounds, schedule, and renderer GUIDs.
2. Author `vfx_spawn` and `vfx_update` in WGSL; import `forgeax_vfx::prelude` and shared shader modules with `#import`.
3. Cook with `createParticleCodeNativeCooker(modules)`; publish payload and `particle-effect/program.json` atomically.
4. Ordinary DevKit games already install one VFX assembly per execution realm; consume that owner. For explicit standalone assembly, create one `createVfxRuntimeHost({ camera })`, attach each `{ world, assets }`, and register `host.feature` through the owning App/Renderer assembly. Do not add a second host to an SDK game.
5. Load by GUID with `loadVfxGpuEffect`, allocate a shared `ParticleEffectAsset` ref, and spawn `ParticleEffectPlayer`.

Read [`packages/vfx/README.md`](../../packages/vfx/README.md) for the author ABI and lifecycle, [`packages/vfx-compiler/README.md`](../../packages/vfx-compiler/README.md) for reflection and cook errors, and [`packages/vfx-render/README.md`](../../packages/vfx-render/README.md) for GPU/render ownership.

One-shot bursts (sparks, hit flashes, an enemy dissipating; Three.js additive
`Points`/`Sprite`, Godot `GPUParticles3D.one_shot`) need no extra API: give the
emitter `schedule: { rate: 0, bursts: [{ time: 0, count }] }` and a billboard
renderer with `blend: 'additive'`, then spawn one `ParticleEffectPlayer` per burst
(a distinct `seed` varies it) and despawn it after the last scheduled birth plus its particle tail. Reused effects retain their authored burst times, looping and local transform conventions; an asset name does not imply a single short flash. Inspect the timeline before adapting it, and keep gameplay hit feedback synchronous. Authorized source or parameter adaptation may change schedules and recook them while retaining stable identity and provenance.
The complete files are recipe 5 of the
effects cookbook.

Players advance once per World frame: the `vfx-gpu-runtime` Update system runs
after `FixedUpdate` and steps each simulating player by `Time.delta` times its
`timeScale`, so particles move at render rate. Bound hitches with
`TimePolicy.maxDeltaSeconds`; do not add a VFX-side step clock. Each intent
records `delta`, `initialDelta` and cycle `elapsed`; device recovery replays the
same dispatch count and cycle time over even steps.
Presentation retirement must use the same frame time and `timeScale` as playback.
A fixed-tick counter does not measure VFX progress when fixed work is dropped.

Every particle topology fogs at its own depth through the shared
`translucent_fog`; alpha blending adds in-scattering and additive blending only
attenuates. Particles never need an effect-side fog term.

> [!IMPORTANT]
> Behavior belongs in WGSL code, not a node/operator graph. Do not add CPU mirrors, runtime compilation, backend-name checks, direct RHI access, particle readback, or demo-side render workarounds.

Switch on structured error codes and use `detail` plus `hint`. Unknown source fields fail closed. Batch B accepts executable billboard advanced fields and independent ribbon, trail, and beam topologies. It does not add CPU fallback, runtime compilation, raw author bindings, CPU particle mirrors, gameplay readback, graph authoring, or VFX RPC.

For static-scene collision, import `forgeax_vfx::data::scene_sdf` and supply
`createVfxRuntimeHost({ camera, sceneSdf: { read(world) } })` with a fixed World
range and explicit budgets. Cook geometric fields on ordinary Mesh GUIDs through
Import; sampled-visibility data cannot qualify collision. Renderer owns retained
scene projection, sharing, graph production and fence retirement. Follow
[the host contract](../../packages/vfx-render/README.md#managed-scene-sdf-collision)
for bounded response, approximation error and structured unavailable results.
Use RHI Debug to inspect the actual producer/consumer work before changing the
collision shader; a successful replay alone does not establish collision quality.

For editor/tool inspection, narrow registry payloads with `isVfxGpuEffectAsset`
and project them through `describeVfxGpuEffect`. The immutable descriptor owns
the emitter tree, timeline, dependencies and executable/partial/unavailable
capability truth without exposing compiler objects or raw WGSL bytes.

For wind, attraction or vortex motion, declare emitter `forceFields` and import
`forgeax_vfx::data::force_fields`; call `vfx_apply_force_fields` before the authored
integration. Produce saved constant/radial/vortex textures with build-time
`createVfxVectorFieldTexture` from `@forgeax/engine/vfx-compiler`, publish ordinary
texture GUIDs, and load the effect GUID. The owning [field contract](../../packages/vfx/README.md#managed-force-fields)
defines transforms, units, sampling and limits. Diagnose a failed field through
its structured plan cause and the ordinary asset producer. Run
`smoke:fields` for the bounded independent trajectory/capture probe and
`scripts/smoke-fields-browser.mjs` against the prepared DEV/build server for
transport and paired pixels; use the maintained per-owner GPU lease entry.

Inspect runtime state with `host.inspect(world)`. The aggregate is keyed by host
generation, player handle, asset GUID and emitter ID; do not collapse it back to
one latest intent or treat a realm-local handle as cross-World identity. Recover
through the owning generation/LKG path. For asset changes, run
`node scripts/asset-cook-contract.mjs`; a package-local scripts path is invalid.
For a live, same-generation preview control, acquire `host.acquireControl(world)`
and use its typed `patchPlayerParameters` or `submitChannel` methods. Their
generation and structured errors are the evidence boundary; do not reach
through `VFX_GPU_RUNTIME_RESOURCE_KEY` to mutate an instance directly.
Verify with:

```sh
pnpm --filter @forgeax/hello-boss-lightning smoke:browser
pnpm --filter @forgeax/hello-boss-lightning smoke
pnpm --filter @forgeax/hello-boss-lightning smoke:falsify
node apps/hello/boss-lightning/scripts/smoke-public-only.mjs
pnpm metrics:check
pnpm metrics:run
```

Browser and Dawn are required because Null structural success cannot prove compute validation, topology draws, or pixels. Visual evidence records `advanced-renderers-visible`, `live-patch-continuity`, `event-sub-emitter-visible`, and `hmr-last-known-good-visible` with a PNG and falsifier result. Program v3 custom billboard sorting is executable only when the source declares one typed `VfxCustom` sort field; the compiler and managed GPU pass reject ambiguity instead of silently falling back to emitter order.

## Time, parameters and a textured custom billboard

- Time: `ctx.time` (Player elapsed, honours `timeScale`/pause), `ctx.time_whole` +
  `ctx.time_fract` (precise split), `ctx.world_time*` (world clock), `ctx.delta`. Loop
  with `vfx_loop_phase(ctx.time_whole, ctx.time_fract, rate, offset)`; never-ending
  particles use `lifetime = vfx_forever()`. Do not burst once with `lifetime = 1e9` and
  derive life from `particle.age`: f32 age loses precision over long sessions.
- Parameters: declare `parameters: { name: { type: 'vec4<f32>', default: [...] } }` on
  the effect source, read `vfx_parameters().name` in any emitter, override per Player with
  `parameters: vfxPlayerParameters({ name: [...] })` (JSON string field, also valid in
  scenes and packs). One effect then serves many placements; do not smuggle position or
  scale through `Player.seed`. Errors surface as `vfx-parameters-invalid`;
  `validateVfxPlayerParameters(json, fields)` checks offline (`fields` = declared `{ name, type }[]`).
  Parameter types accept `vec4<f32>` or `vec4` (max 32 parameters). Read diagnostics with
  `world.getResource('VfxGpuRuntime').diagnostics()`; helpers include `vfx_loop_phase` and
  `vfx_loop_angle` (radians).
- `loadVfxGpuEffect(assets, guid)` takes a GUID string or an `AssetGuid`.

Textured custom `particle-billboard` material (smoke sprite), three files:

1. `smoke.wgsl` with `#define_import_path game::smoke`, importing
   `forgeax_view::common::{View, view}`, `forgeax_view::fog::{translucent_fog, ndc_world}` and
   `forgeax_material::parameters::{material, smokeTexture, smokeTexture_sampler}`;
   `vs_main`/`fs_main` read the particle vertex inputs (`position`, `right`, `up`, `color`).
2. `smoke.wgsl.meta.json`: importer `shader`, `importSettings.materialShaderIdentifier`
   `game::smoke`, and `paramSchema` listing `{ "name": "smokeTexture", "type": "texture" }`.
3. Pack entry, kind `material`, pass `name: "particle-billboard"`,
   `program: { module: "game::smoke", vertexEntry: "vs_main", fragmentEntry: "fs_main", bindings: "render-material" }`,
   `renderState` with `cullMode: "none"`, `depthWriteEnabled: false`, a premultiplied blend
   (`one` / `one-minus-src-alpha`), `parameters: [{ name: "baseColor", type: "color" }, { name: "smokeTexture", type: "texture" }]`
   and `values: { baseColor: [1,1,1,1], smokeTexture: "<texture guid>" }`, with the texture
   guid also listed in the asset `refs`.

Material parameter types are `bool`, `f32`, `i32`, `u32`, `vec2`, `vec3`, `vec4`, `color`,
`texture`, `texture_2d_array`, `texture_3d`, `texture_cube`, `texture_external`. The type is
spelled `texture`, not `texture2d`; a texture value is the bare GUID string (or a texture
descriptor object); vectors and colors are number arrays. The `material-value-type-mismatch`
error hint lists these forms.

## Capture faces

Which Features record into capture faces (planar mirror now; probe and cube are
a follow-up) is set per Feature by `RenderFeature.capture`: `'display-only'`
(default), `'all'`, or `{ faces: ['planar' | 'probe' | 'cube'] }`. GPU particles
declare `'all'`: they draw again in each recorded face, costing one extra
particle draw per face at the face resolution. Opt out with
`createGpuParticleFeature({ capture: 'display-only' })`. Post effects stay
display-only. See `packages/vfx-render/README.md`.
