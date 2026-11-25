---
name: forgeax-engine-assets
description: >-
  ForgeAX authoring-to-runtime asset route with GUID identity and producer-owned recovery.
  Use when authoring, importing, cooking, loading, validating, or repairing any game asset.
---

# forgeax-engine-assets

## Procedural content

Choose the owner by when the content is known, not by how it is computed:

| Known | Owner | Reference | Change |
|:--|:--|:--|:--|
| At build time: props, level meshes, materials, seeded variants | `.pack.ts` `build` calling `@forgeax/engine/geometry` factories; `parameters` (for example `seed`) select variants | GUID `AssetGuid.derive(packageId, sourceKey)`; `await assets.load(guid, kind)` | Edit source or parameter `values`; the producer re-cooks and caches |
| During play: debris, growth, deforming water | `assets.create(meshAsset)` in a plugin; no Pack declaration, GUID or saved file | The returned handle; release it after the ECS binding takes its own reference | `writeRange` keeps vertex/index counts (per frame); `replace` changes topology |

- A Pack `build` is a pure function of its source and `values`: derive randomness from a
  seed parameter through `rng.create(seed)` (`@forgeax/engine/math`), never
  `Math.random()` or `Date.now()`. Runtime generation takes a gameplay seed so
  playthroughs and tests reproduce.
- Use `createMeshBuilder` for custom geometry; it derives packed layout and bounds and completes omitted triangle surface channels. Factories and `meshFromInterleaved` also emit the vec4 tangent stock materials need. See the [geometry contract](../../packages/geometry/README.md#meshbuilder).
- Attribute presence maps such as `DEFAULT_VERTEX_ATTRIBUTE_MAP` describe layout; empty lane placeholders do not supply nonempty runtime geometry. Use builder output or `unpackInterleavedVertexAttributes` with the canonical layout projection for existing packed vertices. Retain channel cardinality and submesh validation; do not copy handwritten stride tables.
- Runtime meshes can use Pack materials. Material `values` edits never move vertices.
- Incremental vertex batches share one global index space; follow the [MeshBuilder append contract](../../packages/geometry/README.md#meshbuilder), without assuming implicit index rebasing.
- Compiled recipes: procedural props and runtime meshes.

When authorized to adapt a copied author source to a different SDK, retain immutable originals and work outside active asset roots. Update real dependencies and APIs, regenerate locks with the package manager, compile and cook against the target SDK, then export/import the verified source closure with its identities and provenance. A locked-version rejection is not proof that adaptation is unsupported; changing only version labels or cloning GUIDs is not a migration.

## Collected pipeline recipes

Pass collected version-1 recipes through the build root's `pipelineLibrary` and
`backgroundPipelineLibrary`. DevKit owns compute entry projection and exact
content deduplication during cooking, including already-projected input. It keeps
first occurrence order, reindexes dependencies and retains original-source aliases;
startup overlap is removed only from the background output. Startup-owned
dependencies unused by the remaining recipes and aliases are also omitted, with
indices rewritten; unrelated unused rows remain. Do not add a
parallel game-side identity/cache owner or discard distinct state variants by label.
This is machine-independent preparation; final native compilation still belongs
to the target device. See the [collection contract](../../packages/devkit/README.md#collect-and-prepare-gameplay-pipelines).

## View Pack parameters

For a View parameter request, edit the selected Pack's `parameters` array. Start
from **Inspector → Expose**, which supplies the project, exact target, source,
reflected field type, current value and resolved `apply` path. The Pack panel's
**Add parameter with Agent** supplies source context when no field is selected.
Resolve the selected Engine with `forgeax project engine status --root <project> --json`
and use that installation; another CLI can have a different schema. Current implementation and command results establish
support; a proposed design or visible control alone does not.

| Desired effect | Declaration | Apply |
|:--|:--|:--|
| Change generated geometry, image or topology | `name`, `type`, `default`; read `context.values` in `build` | **Generate** |
| Adjust an existing field permitted by its domain owner | Same descriptor plus `apply: { asset, path }` | Immediately; **Save** persists |

For a Sun intensity field, add this descriptor to the existing array:

```ts
{ name: 'sunIntensity', type: 'f32', default: 3.2,
  apply: { asset: 'scene/showcase', path: ['entities', 'sun', 'components', 'DirectionalLight', 'intensity'] } }
```

Move the existing authored intensity into `default` and remove its original leaf
assignment. Keep the containing `DirectionalLight` object and all unrelated
code. Optional numeric `minimum`/`maximum` set bounds. Descriptors stay literal;
`packageId` may be a literal UUID, `definePackageId('…')`, or a file-local `const`
alias. Imported/computed identities remain buildable but need a statically
readable identity before View can save parameter defaults.

Run `forgeax asset inspect assets/scene.pack.ts --parameters-only --json` before
and after editing, using `--root <project>` when outside that project. It returns
generation/runtime modes, types, defaults, bounds, bindings and 1-based source
locations. It reads only that file and never imports code, scans sibling Packs,
generates or cooks. This checks declarations; it cannot prove generated target
existence, domain writability or preview application. Ordinary `asset inspect`
retains its existing inventory/JSON behavior.

View discovers external declaration changes automatically. Verify a live edit
on the same preview; check source bytes stay unchanged until **Save**, then
reopen. Generate when generation inputs changed. New generation-dependent
behavior uses the existing producer; ordinary parameters need no field-specific
View control, component or runtime handler. Preserve unsaved source/draft edits.

## Runtime identity and content

Use the App/Engine `assets` owner. `assets.create(content)` and
`await assets.load(guid, kind)` return caller-owned `AssetHandle` references;
bind those directly to ECS `asset(kind)` fields. A standalone World uses
`new World({ assets })`. `assets.read(handle)` returns detached content.
Commit changes through `update`, `replace`, or `writeRange`; do not mutate a read
or keep a caller-managed revision. Release the caller reference after a successful
binding; ECS retains its own reference.

Built-in kinds use literals such as `'mesh'`, `'material'`, and `'scene'`.
Custom kinds share one `defineAssetKind<P>('kind')` token between decoder
installation and `load`; runtime writes also require synchronous `prepare`.
Repeated `load` retains the same live identity and preserves gameplay edits.
Use `source(handle)` / `sourceOf(handle)` for adopted provenance and explicit
`reload(handle, { conflict: 'reject' | 'overwrite' })` to adopt a newer source
closure. Catalog changes alone do not overwrite runtime content. See the
[runtime contract](../../packages/assets-runtime/README.md#runtime-content).

Content generated during play (debris, per-wave ships, a reseeded town) needs no
Pack: a plugin injecting `assets` calls `create` on geometry factory or
`Materials` output and yields each `release`/`despawn` from its generator effect.
Edit existing handles rather than creating per frame. Static-switch materials,
identity, Worker publication and tangent facts are in
[content created during play](../../packages/assets-runtime/README.md#content-created-during-play).

## Engine Content library

Basic meshes (`cube`, `sphere`, `cylinder`, `cone`, `torus`, `capsule`,
`plane`, `quad`, `nine-slice-quad`, `triangle`), a mipmapped checker
texture/sampler and a default Standard material are ordinary Pack assets in
`@forgeax/engine-content`. Both SDK templates mount them with forge.json
`"assetLibraries": ["@forgeax/engine/content"]`; `asset list` then shows them
under `@forgeax/engine/content/<file>.pack.ts`. Reference them by the GUID
strings in `EngineContent` from `@forgeax/engine/content` and load them like
project assets. A project that removes the entry has none of them; library
sources are read-only, so copy one into an asset root to edit it. Failures:
`project-asset-library-unresolved` (install or bind the Engine, fix the
specifier) and `project-asset-library-invalid` (package has no
`forgeax.library.assetRoot`). In code, `createPrimitiveMesh(kind)` plus
`assets.create` still produces an unregistered runtime mesh. See the
[content contract](../../packages/content/README.md).

## Lighting asset route

Use these entry points:

1. Author `RectAreaLight` and `LightProbe` through the existing render ECS schemas.
2. Bind `SpotLight.iesProfile` to a build-time cooked `IesProfileAsset` and `SpotLight.cookie` / `RectAreaLight.sourceTexture` to a regular `TextureAsset` (one shared light-texture slice per handle; uncompressed sources are projected on the CPU, BC/ETC2/ASTC KTX2 sources are resampled on the GPU from level 0 when the device enables the matching compression feature); `rollDeg` expresses orientation only.
3. Use `inspect` to read `subject`, `execution`, `lifecycle`, `lastKnownGood`, and `sourceKey`, then invoke the owner's `rebuild`/`cold-cook`.

IES has no runtime source parser; cookies use the existing texture registry. Catalog is a projection, DDC is cache evidence, and Pack/Meta retain authored authority. Do not claim readiness without `accepted` or `verified` evidence.

For slow Meta startup in builds or live dev, enable `FORGEAX_WORKSPACE_TIMING=1`
and inspect `forgeax.pack-ddc.timing` in the owning log. Trace the adapter through
shared source-package production before changing cache policy; Meta publication
uses `DdcEntryInput` to derive its receipt digest from the staging capture, and the
DDC lifecycle validates staged publication before its ordinary lease/head fence.
Never pass an unchecked readback token or skip artifact closure checks. Both routes use
[the existing Pack product DDC](../../packages/import/README.md).

For unchanged live Meta publications, use `readImportPublication` and serve its
returned Pack and artifact bytes with the restored Catalog revision. Prepare HTTP
compression for those exact restored bodies. Require complete artifact and
output-digest agreement plus the DDC head fence; product hits alone are insufficient.
Misses, corruption, changed content and active writers keep ordinary publication.
Do not use rollback's `restoreImportPublication` as a warm-read operation.

For live resource transport, keep one fresh source fence per HTTP request and
recheck scope identity, generation, session state and authority before dispatch.
Reuse only the fence already completed by that request; do not share it across
requests or weaken artifact integrity. Keep accepted-byte recovery separate from
new production when a scope is degraded.
When projecting a Catalog into its runtime scope, preserve each producer's shared
publication envelope for that response and canonical source path. Per-row copies
make wire-table validation and JSON encoding repeat its entire output closure.
Keep current/LKG locators scoped and all receipt/failure fields intact; a new
projection or binding must build its own scoped envelopes.

> [!IMPORTANT]
> Material assets follow one route inside the catalog: authored `MaterialAsset` with `passes` and `values` -> cook record and artifact -> `load(guid, 'material')` -> runtime asset handle. Keep `parent` references, texture references, module identifiers, and per-slot `coordinates` transforms in the same package graph. For recovery, repair the producer or cook output, then retry loading or explicitly reload the existing handle.

## M5 asset authority index

Start with [`schemas/asset-authority.schema.json`](../../schemas/asset-authority.schema.json) and its gate [`check-asset-authority-audit.mjs`](../../scripts/forgeax/check-asset-authority-audit.mjs). Pack or external source plus Meta is author authority. Import and native cook produce validated outputs. DDC is disposable cache evidence, Catalog is a projection, and runtime only reads the validated projection. Editor writes go through the asset-authoring gateway.

For any category, inspect the `subject`, `execution`, `lifecycle`, `lastKnownGood`, and `sourceKey` fields before choosing recovery. The AI path is `inspect` -> `rebuild` or `cold-cook`; `preview-LKG` is read-only, while `override`, `promote`, and `stop-publish` are explicit gateway or publication operations. Do not infer identity from a suffix, path, cache hit, or message text.

For repeated production Meta imports, inspect the host's sealed producer identity
and existing Pack product DDC before proposing another cache. Follow the
[Import cache boundary](../../packages/import/README.md): a verified hit must
skip import and native Cook, while changed source, sibling bytes, Meta settings
or producer identities must miss. Retain importer/Cooker call counts in a
cold/warm regression and verify the current publication after cache restoration.

### Transmission/refraction

For transmission/refraction, preserve the same Standard values through GLTF parse, Pack cook, GUID
catalogue, and runtime inspection. Keep `sourceKey` as producer identity (not a file path), and repair
stale or invalid material output by rebuilding the producer or cold-cooking the same GUID.

### Mental model

The recovery route is producer-owned: validate the `MaterialAsset`, cook the
specialization, publish the record and artifact, then load by GUID. A Catalog
row is evidence and DDC is cache evidence; neither replaces author authority.

### Display-name projection

`deriveAssetName` is the display-name projection used by Catalog build.
Read the resulting `CatalogEntry.name` through `catalogEntry(guid)` or Catalog
enumeration. A producer-supplied `storedName` is authoritative for
an authored entry regardless of whether its package currently has one member or
many. When no stored name is available, a packaged asset falls back to the
package path basename; an asset without a package resolves to the empty string.
Keep this projection in the Pack owner and do not reimplement cardinality rules
in Editor or other consumers.

### Catalog source and evidence

`CatalogSource` is the runtime boundary for catalog navigation. The source
emits `CatalogDelta` rows (`added`, `changed`, and `removed`); it does not prove
that a payload is cooked or current. Register the source, call
`subscribeCatalog`, and only then call `enumerateCatalog` so the editor pinned consumer
cannot miss an update between its initial snapshot and its live subscription.
Merge both snapshots and deltas by GUID, and dispose the
subscription with the host.

```ts
const stop = assets.subscribeCatalog((delta) => mergeRowsByGuid(delta));
const snapshot = await assets.enumerateCatalog();
if (snapshot.ok) mergeRowsByGuid(snapshot.value);
```

Vite's dev transport uses `reloadAssetHost()` to refresh the source after an
import or HMR change; a static build still navigates the same Pack v2 rows.
When the source is not configured, keep the structured failure instead of
inventing a fallback row.

The Vite boundary has one producer and one Catalog projection. `pluginPack`
publishes the scoped dev/build result; `createCatalogClient` subscribes to the
dev delta stream and enumerates the initial snapshot without moving Vite into the
runtime. `runtimeBinding` carries the active scope and `generation`, so a late
publication from an old host is rejected. Preserve `sourceKey` as the semantic
source identity in Catalog facts; it is not a URL, filename, or GUID fallback.

`AssetEvidence` is the read-only join of source declaration, the catalog's
`packageUrl`/`cookReceiptUrl`, producer receipt freshness, and Pack artifact
verification. Use `lookup/verify --guid --project --catalog --json` (or the
injected runtime inspection surface) to distinguish `notCooked`, `ready/current`,
`ready/stale`, and `unknown`; `unknown` is not a pass. Repair the producer or
recook for `notCooked`/`stale`, then rerun the probe. A catalog locator alone
cannot upgrade missing or failed evidence to ready.

## Indexed producer recovery playbook

Use the same five-step loop for images, cubemaps, glTF, fonts, materials, and
native cooked assets:

1. **Inspect** source plus Meta, Catalog, DDC lifecycle, receipt, and artifact
   verification. Read `.code`, `.detail`, `.expected`, and `.hint` as data.
2. **Repair** the named importer, native cooker, source, or Meta declaration.
   The source package plus Meta is author authority; the producer owns output.
3. **Rebuild or cold-cook** through the producer. Remove invalid DDC evidence
   only as part of that producer-owned recovery, never by editing a generated
   Pack product into a substitute.
4. **Verify** GUID closure, receipt freshness, DDC integrity, Pack artifacts,
   and the Catalog lifecycle.
5. **Retry** the same GUID after verification. `lastKnownGood` is a read-only
   preview, and `unknown` is not a pass.

Producer readiness is a host concern. `before-consume` needs all required
importers/cookers registered before the consumer load; `on-demand` needs both
the producer route and the explicit dev transport. Runtime does not import
source files, write DDC, parse log strings, or replace a missing engine asset
with a custom mesh/material workaround.

## ScriptablePack authoring route

For delivery acceptance, use [forgeax-scriptable-pack-review](../forgeax-scriptable-pack-review/SKILL.md): classify fixed assets versus public generators and check provenance, dependency closure, formal consumption, parameters, and runtime recovery.

Keep the two authoring entities distinct. `ScriptablePack` is executable
`*.pack.ts` source: import `definePack` from `@forgeax/engine/pack/source`, keep
one stable `packageId`, optionally declare a non-empty `parameters` capability,
and return a complete `sourceKey -> Asset` map from `build(context)`. `Pack` is
editable `*.pack.json` source: a direct document stores `assets[sourceKey]`,
while an instance stores its own `packageId`, `parent`, and sparse `values`.
Neither source declares per-output GUIDs or `externalAssets`; the build boundary
derives GUIDs from `(packageId, sourceKey)`. Build-time instances resolve their
parent chain through the source producer. Runtime readers consume validated Pack
v2 through `assets.load(guid, kind)`; opt-in runtime generation belongs to the existing Import
producer, outside asset loading and the ECS frame.

| Action | Command or owner |
|:--|:--|
| Inspect identity and topology | `forgeax asset inspect <source.pack.ts> --json` |
| Read external content | `context.readByGuid(guid)` inside `build` |
| Serialize or cook an output kind | Registered `AssetOutputProducerRegistry` producer |
| Rebuild | Vite or CLI producer lifecycle |
| Load at runtime | Existing Catalog plus `assets.load(guid, kind)`; inspect content with `assets.read(handle)` |
| Admit data or generate after launch | App `runtimePacks` and Import `RuntimePackProducer`; [runtime production contract](../../packages/import/README.md#runtime-pack-production-and-durable-content) |
| Prepare JS / TS programs | `preparePackProgram` parses and seals JS without evaluation or conversion; `prepareRuntimePackProgram` from `@forgeax/engine/devkit/plugin-build` converts TS and preserves its source |
| Preserve resolved inheritance | `resolvePackParameterInheritance` then `prepareRuntimePackAnchor`; effective values become defaults, instances keep one anchor and sparse values |
| Save and recover runtime content | Host stores `snapshot()` or versioned `exportSource()` results; `restore()` re-admits fixed content into the new scope |

> [!IMPORTANT]
> `build` must not create GUIDs, write source, publish packages, or mutate a live World. A missing or extra output key, undeclared read/ref GUID, unused external declaration, or kind mismatch is a structured failure; repair the source contract and rebuild the same identity.

> [!NOTE]
> The filesystem Pack gateway's `asset.inspect` with a source path returns
> identity and revision. Add `sourceKey` to inspect one direct `.pack.json`
> output's authored `payload`; verify its returned GUID against the Catalog
> GUID before presenting the fields. A Pack instance returns inherited
> `effectiveValues` for that output. ScriptablePack source inspection never
> executes `build` to derive a payload.

Runtime-capable generators declare their complete `runtime.dependencies`, including
non-default parameter branches. Admission preserves verified JS artifacts and
fixed asset dependencies without evaluating the generator. Persist the original
Pack/program/instance closure before clearing derived caches; DDC is not a save
store. Recovery may replay generators and does not install plugin Fibers. View
uses the same Engine operations; writing project source still requires the
authoring gateway. Browser static program archive delivery remains a separate
qualification from runtime-authored program recovery.

Material producer caching also requires the Naga/WASM owner's verified executing
compiler fingerprint; JavaScript or WGSL bytes alone do not establish that identity.
Missing or invalid Native provenance must not reuse a previously compiled product.

For generated `material` and `mesh` outputs, register
`materialAssetOutputProducer` and `meshAssetOutputProducer` from
`@forgeax/engine/import` at the Vite host. Omit `assetSource` when the build is
self-contained; provide the host snapshot source before using
`reader.readByGuid`.

For ordinary prebuilt `.pack.json` dependencies, create the source in the
build-time owner with `createScriptablePackFileAssetSnapshotSource({
assetRoots })` from `@forgeax/engine-import`. It validates and indexes GUIDs
once, returns private Asset snapshots with deterministic generation/digest
evidence, and keeps missing, malformed, unreadable, and colliding files as
structured `Result` errors.

## MaterialAsset catalog recovery

Use `configurePackIndex('/pack-index.json')` and `load(guid, 'material')` for
both root and derived materials. A successful load returns a handle whose
admitted content has resolved `passes`, `values`, and per-slot `coordinates`,
complete references, a cooked artifact, and a receipt. Parent inheritance is
flattened at admission. On a
failure, switch on `.code`, read `.detail` and `.hint`, repair the producer or
cook output, and retry. Do not substitute a custom mesh or app-local shader
artifact when an engine resource is missing.

## Contract routing

Player packaging groups complete WGSL programs into bounded Zstd streams without
removing backend or capability variants. An artifact's stored `byteRange` locates
its group; optional `decodedRange` selects its original bytes after decompression.
Individual lengths and hashes remain authoritative. Use ordinary build/package,
load and asset verification; do not rewrite program identities or source bytes.

| Task | Load |
|:--|:--|
| Catalog subscription, refs, package identity, compression | `catalog-and-import.md` |
| Custom importers, sidecars, source resolution, byte decode | `catalog-and-import.md` |
| Mesh UV contracts and structured recovery | `runtime-and-mesh.md` |
| Lightmap UV validation across LODs, baked-data identity and staleness | [import lightmap UVs](../../packages/import/README.md#lightmap-uv-validation) and [render bake data](../../packages/render/README.md#baked-lighting-identity-and-staleness) |
| Runtime load, VFX, handles, video, nested scenes | `runtime-and-mesh.md` |
| Scene writeback, new kinds, custom loaders, evidence | `scene-and-custom-kinds.md` |

## Plugin assets

Start with the feature Pack. Use named Plugin exports in `.pack.ts` for small behaviors and
ordinary TypeScript modules for larger implementations. Read the [plugin contract](../../packages/plugin/README.md),
then discover `asset plugin create`, `asset plugin inspect`, and `project root set` through CLI help.
Pack owns configuration; project roots select execution. Reading a definition does not activate it.
New runtime plugins use the same module/config lowering and `startPluginAsset`
native Fiber lifecycle. Inline `toolContract` uses the existing declaration format;
its executor closure must be supplied. Complete fixed publications preserve all
siblings with program/tool attachments per existing build target. Each Context
only installs its target's qualified definitions; an empty tool contract still
records installation eligibility. Every plugin sibling needs at least one
prepared target for complete capture. Restore may expose a foreign definition
as metadata; mounting it without membership in the current target's tools map fails.

### Runtime Pack validation route

Run `pnpm --filter @forgeax/engine-devkit test:runtime-browser` under an owned
Xvfb display for the real Worker JS/TS x dev/build paths. The same gate belongs
to `pnpm test:browser` and Actions browser shard 1. Keep the full hello/learn
60-frame smoke and Dawn rosters; Node producer tests alone do not prove browser
module delivery or native plugin execution.

## Cached asset thumbnails

Use `engine.assets.thumbnails` with the current project ID and at most 32 GUIDs.
Subscribe to workspace `thumbnailEpoch` for progressive `queued` / `cooking` /
`ready` results. The Engine queue reuses ordinary resource/SceneAsset previews
and one retained renderer; do not add a View-side loader, renderer or cache.
Transparent PNGs are disposable DDC outputs. Source publication dependencies,
the Preview preset and producer bytes determine invalidation; inspect a failed
row's structured error before retrying the owning asset pipeline. See
[DevKit's thumbnail contract](../../packages/devkit/README.md#progressive-asset-thumbnails).

When compiler filesystem analysis needs imports, use the captured source
snapshot's `imports(path, { includeTypeOnly: true })` fact. Inventory owns runtime
import filtering; compiler policy keeps its conservative raw-import interpretation.
Always preserve current-byte and resolution verification at publication.
