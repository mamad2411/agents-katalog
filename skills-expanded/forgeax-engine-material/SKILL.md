---
name: forgeax-engine-material
description: ForgeAX MaterialAsset authoring and visibility route. Use when creating, loading, or debugging materials, textures, lighting response, or material readiness.
---

# forgeax-engine-material

## Contract index

## Lighting asset entry points

Use these entry points:

1. Declare a one-sided rectangular light with `RectAreaLight`; `width` and `height` own its dimensions, and the optional `sourceTexture` (a 2D `TextureAsset` of any size: rgba8/bgra8 sRGB or linear, r8 grayscale, rgba16float/rgba32float clipped to [0, 1] take the CPU projection; KTX2 BC/ETC2/ASTC block formats are resampled from level 0 on the GPU, which needs compute and the device compression feature, otherwise one `feature-not-enabled` error and a white slice) tints diffuse and specular like Unreal's SourceTexture. u follows the light's local +X; an absent handle is uniform emission. Show the same image on an emitter quad yourself; the light does not draw its surface.
2. Bind `iesProfile` on `PointLight`, `SpotLight`, or `RectAreaLight`. Point/Rect use Transform orientation (+Z polar axis, +X toward +Y azimuth); Rect modulates its existing LTC result by the center-to-receiver direction. Spot retains `direction`, `rollDeg`, and its optional `cookie` (`TextureAsset`). IES shapes emission independently of occluder shadows; a pedestal lamp can set downward emission to zero. See [IES directional emission](../../packages/render/README.md#ies-directional-emission) for source format, capacity, and consumer limits.
3. Declare 27 `irradiance` values and `radius` through `LightProbe`; GPU slots, LTC, and the probe registry are not public API.

author -> publish -> admit -> accept -> verify are evidence stages. The IES producer creates cooked `IesProfileAsset` at build time; runtime loads it by GUID. Follow `.code`/`.detail`/`.hint` back to the producer for rebuild; fallback is not verification.

Keep one MaterialAsset subject and one Pack publication. Runtime bool/value
data, composed module slots, and a closed compiler context are inputs; macros,
feature defines, runtime cooking, and app-local fallbacks are not. Trace
`materialContractDigest`, `sourceClosureDigest`, `layoutIdentity`,
`programIdentity`, `cookIdentity`, and `materialPublicationIdentity` from
`current` to `generation`, repair the first producer divergence, cold-cook the
same GUID, and verify receipt, artifact, and provenance.

> [!IMPORTANT]
> The visible-object recipe is `MeshFilter` + `MeshRenderer` + `MaterialAsset`. Author one material payload, cook its effective contract, load it by GUID, and allocate the World handle. The recovery route is structured error inspection. Do not create an app-local shader artifact or bypass an engine resource defect in a demo.

## Shadow receiver bias

For a bright patch on a shaded surface, first capture the failing frame through
RHI Debug. Inspect the receiver, shadow-map depth and actual light UBO before
changing roughness, emission or shader code. Directional/Spot `depthBias` is a
normalized light-depth offset (default `0.00001`); it is not the Point shadow's
world-meter bias. A large normalized offset grows with the cascade depth span
and can erase an overhead occluder. Start from the component defaults, then
verify both the occluded surface and a directly lit control for self-shadow acne.
See [directional shadow units](../../packages/render/README.md#directional-shadow-quality-author--inspect--recover).

Generated Standard/Unlit casters preserve authored culling (`back` by default),
so their maps retain the light-facing entry depth. Exit-face-only maps can
misclassify receiver/filter samples inside a touching solid as lit. Keep
double-sided materials and explicit custom ShadowCaster state as authored;
point-face projection winding has a separate correction. Run the shared
`cube-plane-shadow-contact` Browser/Dawn regression for a contact-gap change: it
checks the central contact band and exposed ground/top controls in both render
paths, rather than accepting a single dark pixel or zero bias.

## Color-lighting parity handoff

For a direct-light material issue, use the [color-lighting parity entry](../../apps/parity/color-lighting/README.md), then follow its status recovery map. The `SceneCase` and `CaseReport` schemas are the report contract; repair the named material or producer owner and rerun the same case. Do not turn a missing producer capture into a material pass.

## Direct-light parity entry

When a visible material is used by a direct-light parity case, start with the
revision-pinned
[`three-r184-finite-range-authority.json`](../../apps/parity/color-lighting/cases/direct-light/calibration/three-r184-finite-range-authority.json)
and its executable authority test. The entry is `ready` only with a matching
Three revision/source hash, fixed config, and complete expected samples;
missing fields mean `blocked` and require evidence recovery.

The shared light vocabulary is:

| Field | Public meaning |
|:--|:--|
| `DirectionalLight.intensity` | Lux in a one-world-unit-per-meter scene |
| `PointLight.intensity` | Candela with positive meter range or no cutoff |
| `PointLight.decay` | Finite nonnegative f32 distance exponent; default `2`, `0` keeps only the range window, fractional values such as `1.4` are supported |
| `SpotLight.intensity` | Candela with meter range and KHR cone mapping |
| `color` | Linear RGB, without a global compensation factor |
| `cosInner` / `cosOuter` | Snapshot fields derived from imported cone radians |
| `direction` | Extract-normalized world direction consumed by both pipelines |

The runtime range factor is the Three r184 squared window
`clamp(1 - (d / c)^4, 0, 1)^2`; KHR's unsquared curve remains an import/reference
falsification and must not be used as the Forge runtime curve. Exposure belongs
to the camera tone/output stage after lighting, so material authoring and light
intensity do not receive an exposure multiplier.

Point decay reaches surface lighting, scene captures, volumes, and ray reference
through the same light slot. Existing consumer near-light safety floors remain;
this is not full-distance Three parity. See the [Render contract](../../packages/render/README.md#direct-light-parity-contract)
for validation and attenuation details.

For diagnosis, run the authority and light-snapshot tests, inspect the
normalized snapshot and its buffer projection, then compare independent
browser WebGPU and Dawn captures. Preserve the case `provenance`, named
`captures`, raw hash, analytic/ROI metrics, and `CaseReport.verdict`. Do not
replace a missing engine path with a custom mesh, fallback shader, or app-local
light profile.

## Optional physical features

Enable clearcoat, sheen, anisotropy, iridescence, or diffuse transmission through `staticSwitches: { feature: true }`
in the authored root or child, then cook and load that selection. Omitted
choices disable these layers; a scalar weight is runtime data. An explicitly
enabled zero weight keeps code available for animation. glTF import derives
these choices from the source extensions.

## Transmission/refraction

Use the existing `Materials.standard` entry with transmission, IOR, thickness, attenuation, and named
texture values. Smooth/rough refraction, edge fallback, and transparent ordering are renderer-owned;
inspect `renderer.inspect().transmission` for detached capability/resource/lifecycle facts. GLTF
transmission is producer-owned and must be repaired through source -> Pack -> GUID load, including the
structured BLEND rejection path.

On a 16-sampled-texture device, transmission shares the `metallicTexture` / `roughnessTexture` /
`alphaTexture` slots. Authoring one of those split maps on a transmissive material there drops
refraction and reports `MaterialSampledTextureBudgetExceededError` (`detail.conflicts` names the
maps); remove them or target a 21-texture device. Check before rendering with
`materialSampledTextureBudget(world, assets, handle)` or the `asset.material.preview` result's
`sampledTextureBudget`. Contract: `packages/render/README.md` §Standard sampled-texture budget.

## Diffuse transmission (foliage, paper, thin cloth)

Back-lit thin surfaces use `diffuseTransmission` (0..1) and `diffuseTransmissionColor`, with optional
`diffuseTransmissionTexture` (alpha, linear) and `diffuseTransmissionColorTexture` (RGB, sRGB), the
`KHR_materials_diffuse_transmission` model. It is opaque light passing through, not refraction: no
`transmission`, no depth-write change, no backdrop copy.

The factor is a split, not an extra term: reflected `(1 - factor) · baseColor`, transmitted
`factor · tint`, so a white leaf in a white sky stays at 1 on both sides. `factor = 1` is a lossless
frosted diffuser, never glass; use `transmission` for see-through. Leaves sit near 0.3-0.6. Unreal
two-sided foliage adds `SubsurfaceColor` on top of full diffuse (about 2x in a white furnace); convert
with `S = max(1, |Base| + |Sub|)`, `factor = |Sub| / (|Base| + |Sub|)`,
`baseColor = Base / (S · (1 - factor))`, `tint = Sub / (S · factor)` (`|c|` = largest channel), which
matches Unreal's path-traced balance, and do not port its GGX back-scatter peak (render README
§Factor semantics).

1. Author values with `Materials.standard({ diffuseTransmission, diffuseTransmissionColor, ... })` and
   `renderState.cullMode: 'none'` so the back face rasterizes.
2. Bind it to a cooked Standard alias root: module id containing `::standard-`, the five canonical
   user-region textures, and the diffuse-transmission parameter names. The built-in
   `forgeax::default-standard-pbr` root is layer-free, so values alone stay inert.
3. The layer is Forward-only; do not expect it in a Deferred GBuffer. Authored alias roots currently
   draw on the per-entity CPU lane and compile out clustered and rect-area lights (render README
   §Diffuse transmission); budget dense foliage accordingly.
4. Verify with the back-lit falsifier pattern in `apps/hello/foliage-transmission` (opaque control
   stays dark, factor 0 must fail), its white furnace (factors 0, 0.5, 1 match the opaque white
   control; `FALSIFY=additive` must fail), and its RHI Debug browser smoke, which checks the bound pipeline's
   module and 68/69 bindings.

A glTF source carrying the extension imports through the same fields; out-of-range values fail as
`gltf-material-physical-invalid`.

## Opaque Standard surface diffusion

Author ordinary `Materials.standard({ baseColor, subsurfaceRadius: [9, 6, 3], subsurfaceWeight: 1 })`
values in a Pack, cook and load the material by GUID, and assign it through `MeshRenderer`.
`subsurfaceRadius` is linear RGB support in presentation pixels, each finite in [0,12]; weight
is finite in [0,1]. Select the Deferred profile with `subsurfaceQuality: 'high'` or `'low'`.
The renderer scales the support to each view's actual internal extent. Zero radius or weight
uses the ordinary path without diffusion passes or new targets.

This lane diffuses direct and existing environment diffuse while preserving specular and
emissive. It requires compute/storage textures, float32 HDR filtering/blending,
`texture-formats-tier2` read-write storage and 32KiB
workgroup storage; missing capabilities fail explicitly. Its initial roster is opaque,
single-sample Standard rigid, instanced and skinned surfaces with at most 16 active quantized
RGB profiles per view. Positive demand with Forward, MSAA, blending, disabled depth writes,
single-layer medium, Diffuse GI, cube/planar captures or ray-reference programs fails rather
than silently changing the requested material. Thin diffuse transmission has its own local
backlighting semantics and is not surface diffusion.

For capture and diagnosis follow [the Render contract](../../packages/render/README.md#subsurface-surface-diffusion)
and the RHI Debug skill. Check the published material values, the second lighting-context
lane, the separated diffuse carrier and `cs_subsurface` bindings before changing author values.
The implementation acceptance record is ROI25 evidence;
an API description is not a measured quality, performance or complete-CI receipt.

## Projection and non-PBR materials

| Need | Entry |
|:--|:--|
| Texture without usable UVs (rocks, terrain, kitbash) | `Materials.standard({ ..., triplanar: { space: 'world' \| 'object', scale, sharpness } })` |
| Baked object-space normal map | `Materials.standard({ normalTexture, normalMapSpace: 'object' })` |
| Height relief on a flat polygon (trim bakes, grout, panel lines) | `Materials.standard({ normalTexture, displacementTexture, displacementScale, displacementBias, displacementMode: 'parallax' })`; geometry, shadows and bounds stay at the base mesh. Parallax constraints: needs `normalTexture` (`bumpTexture` ignored); no independent `metallicTexture` (use `metallicRoughnessTexture`); with transmission below the dedicated budget it falls back to normal mapping, reported in the material sampled-texture budget |
| Mirror/polished floor reflecting the scene | Pack-cooked `Materials.standard({ ..., planarReflection: true })` plus Camera `PlanarReflection` on the same plane; leave `target` unset for a Renderer-owned mirror sized by `resolutionScale` (render README §Planar reflection capture) |
| Glossy / brushed floor with a blurred reflection | Same, with `PlanarReflection.generateMipmaps: true`: roughness picks the mirror mip (`roughness × (levels − 1)`) instead of fading it out |
| Wet ground / rain puddles (ripple-distorted reflection) | Custom Standard Surface with `planarReflection: true`: ripple `normalWS` from `frameTime`, per-pixel `roughness` for wetness; set `PlanarReflection.distortion` on the camera |
| Diffuse only, no highlight | `Materials.lambert({ baseColor, ... })` |
| Lit look without lights (sculpt, preview) | `Materials.matcap({ texture, sampler })` |
| Debug the shading normal | `Materials.normal()` |

`space: 'object'` keeps the texture on a moving mesh; `'world'` keeps it in the
world. Triplanar refuses alpha masking and the slots it cannot project, and
object-space normals refuse `bumpTexture`, with `material-authoring-contract-invalid`
(`detail.parameter` names the option). Object-space normals also need a blue
channel: an RG-only normal texture (`rg8unorm`, `bc5-rg-unorm`, `eac-rg11unorm`,
Basis RG) fails readiness with `asset-invalid-value`
(`detail.reason: 'normal-texture-lacks-blue'`); keep RG normals in tangent space. Neither reaches the ray reference
(`ray-material-unsupported`). Matcap and Normal are unlit: no lights, no
shadow receipt. Evidence and falsifiers live in `apps/hello/material-projection`
(render README §Projection and the non-PBR material family).

## Order-independent transparency

Transparent draws composite in back-to-front sorted order by default. For
interpenetrating or cyclic transparent layers, set the view's
`Camera.transparency` to `TRANSPARENCY_WEIGHTED_BLENDED`. Do not reorder
entities or split meshes in the app. There is no per-material opt-in.

A draw accumulates only when all of these hold:
- its blend is straight over (`src-alpha / one-minus-src-alpha`) or
  premultiplied over (`one / one-minus-src-alpha`);
- depth writes are off;
- it is an unskinned built-in Standard or Unlit `fs_main` draw without `outputs`.

Every other transparent draw stays in the sorted pass after the composite.
Read `renderer.inspect().transparency.ineligible` for its reason:
`blend-not-eligible`, `depth-write-enabled` or `program-without-oit-output`.
Repair the material's render state, or accept sorted, rather than parsing
messages.

The result has exact coverage and a depth-weighted average color. It is not
the exact over-operator for overlapping layers. See the
[OIT section](../../packages/render/README.md#order-independent-transparency).

## Mental model

The recovery route is structured error inspection followed by source or cook
repair; it never adds a parallel material surface.

`MaterialAsset` owns `passes`, `parameters`, `values`, and optional `parent`.
The root owns the effective contract. A child inherits the root and supplies
only its changed values. A texture value is structured:

```ts
{
  texture: textureGuid,
  sampler: samplerGuid,
  coordinates: {
    set: 1,
    transform: { offset: [0.1, 0.2], scale: [2, 2], rotation: 0.25 },
  },
}
```

The coordinate set and transform remain attached to the named texture slot.
The glTF bridge, pack cook, runtime extract, and built-in PBR shader consume
that same data.

For a render target or reflection probe, the material consumes the public
`RenderTargetTextureSource` projection produced by the Renderer. The source is
bound to the named texture slot with its exact dimension and mip view; it is not
an asset handle or an app-local texture registry. A `3d` or `2d-array` target
binds to a `texture_3d` or `texture_2d_array` param (source `dimension: '3d'` /
`'2d-array'`); a material sampling a target is excluded from that target's own
capture. Probe sampling uses the
renderer-owned selected probe, roughness mip, local box projection, and
Skylight irradiance fallback. Read pixels only after the matching
`FrameReceipt.completed` promise resolves.

A Three `VideoTexture` on a mesh maps to a `VideoAsset` bound as the material
texture (`baseColorTexture`, emissive or a `texture_external` root param) on a
renderable that also carries `VideoPlayer` (`playing`, `loop`). Import the clip
with `forgeax asset add assets/clip.mp4` (`.mp4`/`.m4v`/`.webm`/`.ogv`; the
container is streamed, never inlined) or create `{ kind: 'video', url }` at
runtime. In a DOM realm call `installDomVideoSourceProvider(world)` from
`@forgeax/engine/graphics-extras`; it creates the muted inline `<video>` and
follows `VideoPlayer`. In the default Engine Worker App already installed
`installWorkerVideoSourceProvider`: the page owns the `<video>` (the Three
`VideoTexture` element) and transfers each new frame as a `VideoFrame`, one in
flight per consumer. Do not call the DOM installer there (it returns
`video-dom-unavailable`); read `provider.status(entity, clip)` for
`video-autoplay-blocked` / `video-load-failed` and call `provider.resume()` from
a gesture.

A caller `GPUTexture` or a video uses `renderer.importTexture({ kind:
'gpu-texture' | 'video', ... })`. Bind `{ source: importedHandle.source }`
through `assets.update(materialHandle, { values: { slot: source } })`;
ordinary slots copy video frames. Zero-copy video uses a root parameter of
type `texture_external`. Update the loaded material handle or use
`assets.copy` to preserve its admitted program contract; constructing a fresh
material from a detached payload does not transfer a cooked projection.
Branch on `external-texture-invalid` / `external-texture-state-invalid`
`detail.reason` ([Render external textures](../../packages/render/README.md#external-textures)).

Standard PBR always applies geometric specular anti-aliasing: roughness widens
by the screen-space normal spread in Forward, Deferred, IBL, and clearcoat.
Do not raise authored roughness or add a custom shader to hide sparkling
highlights on curved low-roughness surfaces. The contract lives in
`packages/shader/README.md` under Standard lit shader contract.

Specular IBL also compensates multiple scattering, so rough metal keeps its
energy: in a uniform environment a white metal matches the sky at every
roughness. Do not brighten rough metals with a higher `baseColor`, `intensity`,
or an emissive term to offset split-sum darkening; that loss no longer exists.

## Author, cook, load

```ts
const material: MaterialAsset = {
  kind: 'material',
  parent: parentGuid,
  values: { baseColor: [0.2, 0.55, 0.95, 1] },
};

assets.configurePackIndex('/pack-index.json');
const loaded = await assets.load(materialGuid, 'material');
if (!loaded.ok) {
  report(loaded.error.code, loaded.error.detail, loaded.error.hint);
  return;
}
const handle = loaded.value;
// Bind directly to MeshRenderer.materials; release the caller reference after binding.
```

For a quick visible surface, a project that mounts Engine Content
(`assetLibraries`) can load `EngineContent.materials.default` — a Standard
material with a mipmapped checker base color — or any `EngineContent.meshes.*`
mesh, whose `Default` slot already defaults to that material. Author a project
material with `parent` set to it to override values.

For a custom module, put `passes[].program.module` in the root contract. The
shader build publishes the module; the material cook publishes the record and
artifact. The application only performs the catalog load and readiness check.

## Points and Lines route

For first-class point or line authoring, route the request through the existing
asset and material owners:

1. Confirm the `MeshAsset` has `point-list`, `line-list` or `line-strip` topology.
2. Admit exactly one `Points` or `Lines` component with finite positive
   `size` or `width`. `Points.sizeUnits` / `Lines.widthUnits` select `pixels`
   (default) or `world`; `Points.shape` is `square`, `circle` or `soft`;
   `Lines.cap` selects `butt` (default) or `round` ends and joins. Points read
   the mesh `color` stream as a per-point tint and `uv1.x` as a size scale.
3. Select `Materials.unlit`; its render state supplies blending and depth
   writes and its base-colour texture maps across each point sprite. Do not
   author a replacement shader or mesh.
4. Let Standard extract, prepare, and record the retained expansion.
5. Use `renderer.inspect` and the RHI debug capture when source, derived,
   binding, or draw evidence is needed.

Admission is atomic. Unsupported topology, invalid style, lane conflicts, or a
missing unlit forward material return a structured refusal. Read `.code`,
`.expected`, `.hint`, and narrowed `.detail`; never infer support from a
message or silently substitute a generic mesh draw.

The direct WebGPU probe is runtime evidence. Clustered unlit, WebGL2 capability
restrictions, and RhiNull structural-only records are separate evidence rows;
RhiNull does not prove pixels or hardware timing. Recovery is inspect, repair
the named source or producer, rebuild or cold-cook, then retry the same
retained/prepared renderer owner. There is no new CLI, RPC, registry, cache, or
recovery ledger for this route.

## Built-in PBR slots

Built-in PBR names its coordinate records by texture slot: base color,
metallic roughness, normal, specular tint, emissive, and occlusion. Each record
contains offset, scale, rotation, coordinate set, and physical extent data.
The vertex input selects the requested coordinate set and clamps only when the
primitive has fewer sets than the material requires.

## Recovery checklist

| Symptom | Inspect | Recovery |
|:--|:--|:--|
| Black standard material | `DirectionalLight`, effective pass, render error | Add the required light or repair the pass, then draw again |
| `material-parent-not-found` | `detail.missingParent`, `detail.chain` | Fix the GUID and re-cook the child |
| `material-circular-inheritance` | `detail.chain` | Remove the repeated parent and re-cook |
| `material-value-unknown` | `detail.parameter` | Declare the parameter in the root contract or remove the value |
| `material-value-type-mismatch` | `detail.expectedType`, `detail.actualType` | Change the value and re-cook |
| `material-specialization-not-cooked` | requested material and selection | Run the cook path and publish the record and artifact |
| `material-specialization-stale-generation` | `detail.dependencies` | Re-cook after dependent sources settle |
| `gltf-material-uv-set-missing` | slot and available sets | Add the source UV set and re-import |

Read `.code`, `.expected`, `.hint`, and the narrowed `.detail`; this is the
recovery route, and it never parses a diagnostic message or silently replaces
an engine resource.

## Routing

- Material shape and error union: [`packages/types/README.md`](../../packages/types/README.md)
- Pack/cook record: [`packages/pack/README.md`](../../packages/pack/README.md)
- Shader module and reflection: [`packages/shader/README.md`](../../packages/shader/README.md)
- Runtime catalog: [`packages/assets-runtime/README.md`](../../packages/assets-runtime/README.md)
- Migration: `docs/material-asset-migration.md`

## Visibility is a render boundary, not a material field

Quick start: author `Visibility` through ECS, inspect its effective state from
the render package, and leave `MaterialAsset` unchanged:

```ts
import { Visibility, VisibilityStateValue, resolveVisibility } from '@forgeax/engine/render';

world.spawn({ component: Visibility, data: { state: VisibilityStateValue.hidden } }).unwrap();
const snapshot = resolveVisibility(world);
```

| Question | Authority | Recovery |
|:--|:--|:--|
| Why is an entity hidden? | `Visibility` intent plus `resolveVisibility` | Inspect `source` and hierarchy diagnostics |
| Why did a material fail? | Material/shader structured errors | Repair the cooked contract and retry |
| Why is the count unexpected? | `renderer.inspect().visibilityStats` | Inspect the renderer candidate path |

Do not replace a missing material, mesh, camera, or visibility path with a
demo-side stand-in. Visibility does not own camera, picking, lifecycle, assets,
or VFX shadow behavior. Those are out of scope for this material skill.
## Custom multiple outputs

`passes[].outputs` declares ordered named color outputs with format, optional
blend and writeMask. WGSL `@location(n)` selects index n. Cook validates the
selected fragment interface; load through the ordinary GUID route. Bind matching
RenderGraph targets through [public MRT](../../packages/render/README.md#public-material-mrt),
then inspect all attachments through RHI Debug rather than accepting color alone.

## Color writes and coplanar overlays

Use `renderState.colorWriteMask` (RGBA bits 1/2/4/8, default 15) for per-channel
writes. Mask 0 with depth writes enabled makes an invisible occluder; place it
before affected opaque geometry with the existing queue. Use `depthBias` (signed
32-bit constant units), `depthBiasSlopeScale`, and optional `depthBiasClamp` for
polygon offset. Zero defaults need no enable flag. Negative bias pulls forward
under conventional less-depth; an overlay usually disables depth writes.
With multiple outputs, this mask intersects each output's `writeMask`.

Generated shadow passes retain polygon offset and culling but own depth writes;
color suppression does not disable shadows. Derived temporal attachments write
all scene-data channels. See the [pass table and RHI Debug regression commands](../../packages/render/README.md#material-color-writes-and-polygon-depth-offset)
before interpreting masks on deferred/MRT attachments. Inspect both pipeline
state and live/fresh-replay pixels, including the zero-bias and write-off controls.

## Lane admission for Unlit and morph

An opaque rigid `Materials.unlit` draw (queue below `RenderQueue.Transparent`, declared program) takes the GPU-driven color and shadow lanes like Standard; skinned, blended, `Transparent`/`Overlay` queue or program-less Unlit stays on the CPU lane and keeps its direct order. A `MorphWeights` entity over Mesh `morphTargets` deforms through a renderer-owned compute stream under any material program and owns its batch; authors add no morph variant or shader code. Read the admitted lane and reason from `renderer.inspect()` `gpuDriven` rather than inferring it (render README §GPU-driven PBR / shadow / skin navigation).

## Material and punctual default behavior

Standard `roughness`, `emissiveIntensity`, and `sheenRoughness` default to 1.
Black emissive/sheen colors still disable their contribution; physical sheen
still needs its static switch. Explicit zero intensity remains zero.
Emissive is scene-linear and passes through exposure and the tone curve: under
ACES, large emissive surfaces above about 1.5 clip toward white and lose hue;
use 0.8-1.5 for panels and windows and 3-10 only for small bloom sources
(SDK runtime-light-emissive).
Glow meshes (beams, light pillars) add light: emission-only Surface (`return surfaceEmissionOnly(input, color, opacity)` from `forgeax_material::surface_v1`: the template still lights an additive Surface, the helper zeroes sun Fresnel glare and sky reflection), `one / one`
colour blend, `zero / one` alpha, peak under the bloom threshold, `renderState.fog: false` to skip scene fog (any forward draw; deferred opaque still fogs), alpha fading with
height on an open tapered mesh (SDK beam-pillar).

A Surface defines material properties only; it gets no sun, sky or camera. For a sea use the stock `model: 'single-layer-medium'` (sun glint, Skylight environment reflection, fog; render README "Sea sun and sky").

Point and spot lights default to no distance cutoff. Use an explicit finite
`range` to bound cluster membership and shading cost in many-light scenes.
A no-cutoff light reaches all camera clusters, including when its source is
outside the frustum. The default spot has a 60-degree outer and 0-degree inner
half-angle (falloff across the whole cone); `outerConeDeg` alone narrows it.
Equal angles give a hard cone; they are valid with shadows on or off and use a defined hard step in
surface and volume shaders. Spot shadow farPlane remains its own range.

## Capture faces

Which Features record into capture faces (planar mirror now; probe and cube are
a follow-up) is set per Feature by `RenderFeature.capture`: `'display-only'`
(default), `'all'`, or `{ faces: ['planar' | 'probe' | 'cube'] }`. GPU particles
declare `'all'`: they draw again in each recorded face, costing one extra
particle draw per face at the face resolution. Opt out with
`createGpuParticleFeature({ capture: 'display-only' })`. Post effects stay
display-only. See `packages/vfx-render/README.md`.
