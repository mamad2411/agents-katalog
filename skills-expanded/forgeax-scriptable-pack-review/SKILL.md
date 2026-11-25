---
name: forgeax-scriptable-pack-review
description: >-
  Review procedural asset and generator deliveries across build-time Scriptable Packs and Runtime Packs.
  Use when checking format, dependency closure, content provenance, parameters, consumption, or recovery.
---

# forgeax-scriptable-pack-review

**Scriptable Pack** is a code-authored asset format; **procedural** describes content created by rules and algorithms. Build-time `*.pack.ts`, directly generated runtime assets, and executable runtime generators are eligible for review. A valid Pack, successful execution, or accepted publication can still wrap prefabricated data or Base64. Assess format and procedural provenance separately.

This file includes the [Engine contract](#engine-contract) and [historical Palace evidence](#historical-palace-evidence), so it can be shared alone. Repository ownership is Engine `skills/forgeax-scriptable-pack-review`; Harness distributes shared workflow skills.

## Review intake

Record the following conditions, adopting choices the user already supplied. If the required type is unspecified, ask while continuing format and closure checks; do not issue an overall PASS before it is confirmed.

| Condition | Required facts |
|:--|:--|
| Object | Pack entry, repository/revision, delivery directory, whole package or the user's selected output scope |
| Required type | **Procedural asset**: a fixed recipe without public generation parameters; **procedural asset generator**: a public parameter interface that produces variants without source edits |
| Execution stage | **Build time**, **runtime**, or **both**; distinguish generating data before submission from admitting executable code and generating instances |
| Data policy | **Strictly procedural** by default; use **auxiliary data allowed** only with explicit user authorization, recording permitted kinds, purposes, and scope |
| Use | Target Engine/SDK version, promised outputs and consumer, quality/budget/platform constraints; runtime Host/realm (Node, browser main, Engine Worker), dev/build, program preparation, and persistence promises |

> [!IMPORTANT]
> Public generation parameters belong to the delivered interface. Internal function arguments, build context, constants, environment variables, output shader parameters, and camera controls do not establish generator classification. A public effective seed qualifies; a generator with complete defaults remains a generator.

Record **required type** and **actual interface type** independently. A mismatch is FAIL; do not reclassify the requirement. Ineffective public parameters are a generator defect, not grounds to review it as a fixed asset. A fixed instance's generation capability belongs to its parent; determine whether the reviewed delivery includes that parent's source and dependencies.

This skill produces review conclusions. Repairs, conversions, and publication follow the user's task scope. For first inspection or version differences, compare the embedded contract with the target version's definitions, validators, and actual production path. Historical evidence never establishes current API behavior or a delivery's PASS.

## Production paths

| Path | Formal production and consumption | Review focus |
|:--|:--|:--|
| Build-time Scriptable Pack | `definePack` -> Host Producer/Cook -> Pack v2/Catalog -> `load(guid, kind)` | Isolated cold production, Cook/artifact evidence, source closure |
| Direct runtime assets | Delivered algorithm -> Asset map -> `prepareRuntimePackContent` -> App `runtimePacks.producer.admit` -> combined Catalog/`load(guid, kind)` | Deliver the algorithm and inputs; standalone mesh/texture bytes do not prove procedural generation |
| Runtime Pack generator | Prepared JS artifact (DevKit converts TS) -> `admit` anchor -> `generate` parameter instance -> combined Catalog/`load(guid, kind)` | Complete program/fixed dependencies, public parameters, publication/recovery; admitting the generator does not execute `build` or emit its outputs |

Import's `RuntimePackProducer` owns runtime production; App assembles it into existing asset services. Invoke production explicitly outside asset loading and ECS frames. Consumption retains Registry/GUID ownership. Calling a geometry function or rendering temporary objects does not qualify Runtime Pack delivery.

Classify interface and execution path independently. A fixed recipe may compute runtime data before admission; public parameters on direct data generation still require generator checks. `producer.generate` requires an admitted anchor with nonempty `parameters`. Admitting a parameterless definition does not generate fixed assets; do not add meaningless parameters to fit the API.

## Common checks

Mark each applicable item PASS / FAIL / BLOCKED / N/A with file locations or execution evidence. Explain N/A applicability; unknown or unexecuted work is not N/A.

| ID | Check | Passing condition |
|:--|:--|:--|
| F1 | Source format | Target version discovers, loads, and validates the entry. Exports, schema, identity, parameters, build signature/result, or runtime source/program/instance structure satisfy the chosen path. Type assertions or `tsc` alone do not replace Host validation. |
| F2 | Output contract | Materialize all required outputs through formal production. Check promises, unique stable sourceKeys, kind/payload agreement, refs/component schemas, missing branches, overwritten duplicate keys, and empty outputs. `build` returns the complete output map, not a retired per-output declaration list. |
| C1 | Source closure | Recursively list actual local libraries, re-exports, dynamic loads, scripts, and inputs. Deliver them or obtain them through declared pinned dependencies, with portable paths/case. Runtime code includes verified executable JS closure and matching Host import identities; editable TS alone is insufficient. |
| C2 | Asset closure | Trace production reads and output refs to sibling outputs, delivered dependencies, or explicitly supplied external assets. Record GUID, source/package, fixed version, and resolution. Runtime generators declare all `runtime.dependencies`, including nondefault branches; admission retains exact GUID versions and recoverable closure. A GUID, temporary URL, or author's absolute path alone is insufficient. |
| C3 | Rebuildability | In an isolated directory or fresh Host/realm, clear derived caches and cold-produce/consume using only delivered algorithms, lawful inputs, locked dependencies, and declared environment. Exclude author caches, undelivered files, and implicit downloads. Declared fixed cooked dependencies are permitted carriers but still undergo P1/P2; promised source rebuilds require cold Cook evidence. Persistence additionally requires T4. |
| P1 | Provenance | Trace each key output from recipe/input through its actual generating function to Asset, using the rules below. Inspect libraries, package dependencies, parameter defaults, and remote payloads too. |
| P2 | Rule contribution | Identify the structural, sampling, or composition rules creating content: dimension-driven construction, curves, layout, noise, semantic material recipes. Iterating, decoding, copying, decompressing, or converting stored results alone is insufficient. |
| R1 | Stability/effects | Same source, dependencies, identity, and effective parameters yield equivalent payloads/refs across repeated and fresh-process/realm cold production. Seed randomness; exclude clock/global counters/environment accidents. Generation does not write source, randomize output identities, mutate a live World, or publish Catalog itself; the caller publishes through the formal producer. |
| R2 | Usability | Load the currently verified outputs through the consumer's normal Registry/`load(guid, kind)`. Check finite geometry/index bounds/required attributes, texture extent/format/byte length, and scene refs/hierarchy as applicable. Actually view, hear, or play promised visual/audio/motion results. Admission, Catalog rows, cache hits, and lastKnownGood previews do not prove current-request usability. |

Compare actual payloads and refs, not only package IDs/sourceKeys. Document exclusions for nonsemantic tool metadata. Floating tolerances require a target-contract basis and must not conceal differences.

## Procedural content versus disguised data

Judge **which information determines the content**, not extension, code size, array length, compression ratio, or the presence of loops.

| Content source | Strict-policy decision |
|:--|:--|
| Semantic dimensions, colors, material coefficients, seeds, a small set of control points/layout recipes, general algorithm constants | Allowed with semantics and generating rules. Per-vertex/pixel/sample final results cannot be renamed "control points". |
| Computed TypedArrays, indices, pixels, samples | Inspect upstream computation; binary outputs do not invalidate procedural source. |
| Runtime `blobs`, snapshot binary tables/Base64, verified JS artifacts, fixed cooked dependency bytes | Delivery/persistence carriers, not automatic failures. Trace the original chain: encoded algorithm outputs remain procedural; encoded prefabricated content remains data. |
| Inline Base64/hex/compressed strings, byte arrays, full vertex/index/pixel/audio sample tables | FAIL when they carry prefabricated asset content. Splitting strings, arithmetic rewriting, or moving data into libraries/npm does not change provenance. |
| One expression/call per face/pixel, huge switches, asset-specific fitted neural weights/coefficients | FAIL when they encode the result rather than generate it from rules. |
| Finished external models/images/audio, large survey/scan/map outlines/per-object coordinate tables | Data dependencies. Relevant content FAILs strict policy even when stored outside the package. |
| Pregenerated triangulations, roof partitions, lookup results | Distinguish general constants from asset-specific baked results. Evaluate the latter through their generating chain only when delivered logic/legal inputs regenerate them after cache deletion through the formal cold path, with evidence. Comments saying "generated" are insufficient. |
| Parameterized model selectors, prefab scalers, decoders | Parameters can work while P1/P2 still fail. Color, scale, or seed decoration does not qualify prefab content. |

1. Search encoded strings, numeric tables, TypedArray initializers, decoding/decompression, file/network reads. Treat hits as leads; trace consumers before deciding.
2. Identify rules, semantic recipes, and already-stored results for each key output; inspect both scene composition assets and layout sources.
3. In an isolated copy, test suspicious tables/caches against their claimed generating chain; meaningful dimensions/sampling-density changes may expose recomputation. This experiment neither makes a fixed asset a public generator nor proves every input.
4. Record procedural parts, data parts, and external dependencies separately. A small procedural object cannot qualify a prefabricated main delivery; closure is not provenance.

With **auxiliary data allowed**, check each use against the user's prior authorization and report "procedural + data mixture"; P2 still applies. Auxiliary data cannot replace the promised generating subject without bounds. Do not relax policy after discovering failure. A selected sub-output review covers all its dependencies and limits conclusions to that scope.

## Type-specific checks

### Procedural asset

| ID | Check | Passing condition |
|:--|:--|:--|
| A1 | Fixed recipe | Formal use needs no public generation parameters, source edits, implicit environment inputs, or guessed tool ordering. Direct runtime assets deliver the fixed generating/submission entry. |
| A2 | Fixed result | Default production covers the promised asset. Internal seeds/arguments are allowed. Verify R1; public variability is not required. Submitted bytes alone do not establish a rebuildable generating chain. |

### Procedural asset generator

| ID | Check | Passing condition |
|:--|:--|:--|
| G1 | Public contract | Names, types, defaults, semantics, legal domains, units, enum/range/coupling constraints, and asset-ref requirements are discoverable. Delivery docs may describe semantics; do not invent Engine schema fields. |
| G2 | Defaults | Formal invocation with omitted, explicit-default, inherited, and overridden values follows the target contract and produces complete usable results. |
| G3 | Effective changes | At least one legal contrast per claimed parameter changes actual geometry/materials/hierarchy/samples as specified; hashes/logs/metadata alone are insufficient. Test conditional inputs when active; enums may select algorithm recipes. |
| G4 | Domain/combinations | Cover default/interior/boundary numbers, every bool/enum choice, coupled constraint boundaries, and expensive combinations. State sampling and uncovered combinations for large spaces without claiming exhaustive coverage. |
| G5 | Invalid inputs | Wrong types, unknown names, illegal enums, nonfinite/out-of-range numbers, and violated combinations receive explicit contract-defined rejection/normalization; never silently substitute old cache or broken assets. |
| G6 | Instance isolation | Use the formal Host parameter/instance path for A -> B -> A, then reproduce A in a fresh process/realm. Cache identity covers source/program/instance/effective values/fixed dependencies/producer versions. Instance IDs/internal refs are correct, never hardcoded to the root. Runtime instances point to admitted anchors; resolved inheritance becomes effective defaults, not another live instance. |
| G7 | Resource bounds | Increasing segments/density/resolution/recursion has enforceable bounds/budget behavior. Sample the most expensive legal combinations and record time/memory/output size against delivery budgets, not a universal local timeout. |

G3 proves parameter effects; P1/P2 establish procedurality. For seed inputs, check same-seed reproduction and representative different-seed changes without requiring every seed to be unique. Direct library calls do not replace G6's formal interface.

## Runtime checks

Apply T1-T6 to runtime or two-stage deliveries; mark pure build-time delivery N/A. Subchecks depend on the promised capability; unknown or unexecuted work remains a gap.

| ID | Check | Passing condition |
|:--|:--|:--|
| T1 | Host/program preparation | Obtain `runtimePacks` in the actual App/realm and match `producer.inspect().imports` to module identities. Direct data needs no program host. Code delivery contains executable JS; DevKit actually converts TS. Normal generation/recovery introduces no filesystem, DDC, TS/shader compiler; runtime materials use cooked shader contracts. |
| T2 | Dependencies/consumption | Verify fixed dependencies for all branches, refs, and siblings. Load current outputs through App's combined Catalog/fetcher or `openPackage`. Data uses prepare/admit; generators use admit/generate, not an empty anchor publication. Prove plugin reading/publication/installation separately. |
| T3 | Failure/races | Same-identity reentry/conflicts, invalid parameters, and generation failures satisfy the contract without half-pack visibility or stale-result success. For asynchronous requests, test older/newer races, late completion after withdraw/disposal, and AbortSignal. Cancellation does not interrupt executing JS or require rollback of independently committed restore recipes. |
| T4 | Persistence/cold recovery | When promised, actually write/read portable snapshot/export data, clear derived caches, restore in a fresh scope, and consume by GUID. Check full payloads, internal refs, typed views, and fixed dependency versions. Preserve original definitions, JS programs, accepted instance inputs, and reachable closure. DDC/CacheStorage/GPU handles/Fibers are not save authority. Corruption, missing dependencies, and unsupported versions fail explicitly. |
| T5 | Consumer/lifetime | Apply parameter replacements through contract-defined refresh/reload and release old resources. Withdraw/provider disposal retires owned publication. Consumers and installed Fibers retain their own cleanup; publication does not automatically rebind World/Renderer or uninstall plugins. Restore does not install plugins. |
| T6 | Platforms/budget | Actually test promised Node/browser main/Engine Worker and dev/build combinations. Browser-authored new code requires native module delivery evidence; static code loading is insufficient. Rendering needs real browser/backend consumption; Node tests cannot replace it. Record applicable cold preparation/capture, warm generation, GUID load, explicit export, and GPU completion costs separately. |

Recoverable direct-asset snapshots can contain complete data without a delivered procedural algorithm: T4 does not replace C3/P1. For explicitly temporary content without persistence promises, T4 may be N/A but C3 still requires cold generation from delivered algorithms/legal inputs. Two-stage promises require separate evidence for both paths.

## Engine contract

Checked against Engine revision `df4c86bf12bf117ed229e2721e98d60ad1b0d7a0` on 2026-10-14. These are source-contract facts, not runtime acceptance for a reviewed delivery. Recheck the target revision's actual behavior when it differs.

| Concern | Contract to inspect |
|:--|:--|
| Code-authored definition | Import `definePack` from `@forgeax/engine/pack/source`. Scriptable definitions use `schemaVersion: '2.0.0'`, stable `packageId`, and `build(context)` returning synchronous/asynchronous `Result<sourceKey -> Asset \| PackCookSource>`. Optional `sceneComponents` describe custom scene schemas; custom cook sources require their NativeCooker. |
| Parameter capability | Omit `parameters` for fixed assets; `parameters: []` is invalid. Parameterized definitions have a nonempty list; fields include `name`, `type`, `default`, and applicable `minimum`, `maximum`, `values`, `kind`. Base context has `packageId`/`readByGuid`; parameterized context also has `values`. Material parameters are a separate layer. |
| Identity/output map | Host derives GUIDs from `(packageId, sourceKey)`; use `AssetGuid.derive(context.packageId, sourceKey)` for stable sibling refs. Do not randomize output IDs or hardcode root IDs for instances. Return the complete map; retired per-output GUID declarations and `externalAssets` are not definition fields. Runtime generators additionally declare all `runtime.dependencies`. |
| Editable/data source | Direct `.pack.json` uses schema v3 with `packageId` and `assets[sourceKey]`; instances use their own `packageId`, `parent`, sparse `values`. This authoring schema is distinct from cooked Pack v2 and the Scriptable definition's v2. |
| Runtime content | `prepareRuntimePackContent` validates/copies ordinary assets into a complete source/program/blob/dependency projection. `admit` checks generator/program/fixed dependencies without evaluation; `generate` resolves an admitted parameter anchor and publishes complete instance outputs. Runtime instances do not chain through live instances. |
| Inheritance | `resolvePackParameterInheritance` resolves authoring parents; `prepareRuntimePackAnchor` retains the program/dependency closure and turns effective values into anchor defaults. A new instance uses a new identity, the same anchor, and sparse overrides. |
| Executable authority | `RuntimePackProgram.artifact` is verified JS ESM: entry/export, module sources, fixed Host import identities, digest. `preparePackProgram` from `@forgeax/engine/pack/runtime` parses/seals JS without executing or converting it. `prepareRuntimePackProgram` from `@forgeax/engine/devkit/plugin-build` converts TS and retains original text; optional editable source is not compilation-equivalence proof. |
| Realm assembly | App `assembleRuntimePacks` returns `{ producer, catalog, fetcher }` through its existing asset provider; allow one assembly per realm Registry. `app.pluginContext.get('runtimePacks')` or game-plugin injection accesses it. Use the combined catalog/fetcher; `assetAssembly.catalogSource` remains the delivered base. Native Host imports preserve actual component/Cordis identities. |
| Browser programs | `@forgeax/engine/pack/runtime-browser` owns native browser module delivery through `prepareBrowserPackProgramScope`/`createBrowserPackProgramHost`. Prove actual main/Worker dev/build delivery separately; a static archive is not newly authored runtime-code qualification. |
| Publication/result | `admit`/`generate` receipts expose identity, status, publication evidence, and Catalog rows, not the full source payload. Inspect current execution (`pending`, `current`, `failed`, `cancelled`, `withdrawn`) separately from lastKnownGood. Use `snapshot`/`exportSource` to retrieve durable data. |
| Fixed dependency retention | Capture exact GUID versions and complete siblings/refs with the asset owner's `retain`/`exportSource`. Preserve delivered Pack, original artifact bytes, programs, and per-target `executions`/tool attachments; plugin siblings need prepared target coverage. Temporary URLs and a load-only program entry do not establish a durable closure. |
| Durable snapshots | `runtime-pack-source/2` preserves plain lossless JSON plus a little-endian binary table with typed-view paths/shared-backing Base64. Validate kinds, alignment, ranges, and complete table use; version 1 fails explicitly. `copyPackData` retains valid typed-view offsets/aliases while excluding unrelated backing bytes and rejects accessors/functions/sparse arrays/subclasses/shared mutable storage. |
| Recovery/effects | `snapshot`/`exportSource` preserve source/program/accepted instances/reachable recipes; `restore` re-admits into the new scope and may replay generators. Host owns actual storage. Cancellation fences publication/next recipe, not executing JS; restore commits each Pack independently. Consumer rebinding and plugin installation remain separate owners. |
| Structured failures | Read `code`, `expected`, `hint`, and `detail.cause`. Runtime codes include `runtime-pack-invalid`, `runtime-pack-conflict`, `runtime-pack-dependency-unavailable`, `runtime-pack-execution-failed`, `runtime-pack-cancelled`. Preserve evidence rather than substituting lastKnownGood. |

Source locations in an Engine checkout: `packages/pack/src/pack-authoring.ts`, `packages/pack/src/program.ts`, `packages/import/src/runtime-pack.ts`, `runtime-pack-content.ts`, `runtime-pack-snapshot.ts`, and `packages/app/src/runtime-packs.ts`. Detailed contracts: [Pack](https://github.com/ForgeAX/forgeax-engine/blob/df4c86bf12bf117ed229e2721e98d60ad1b0d7a0/packages/pack/README.md), [Import](https://github.com/ForgeAX/forgeax-engine/blob/df4c86bf12bf117ed229e2721e98d60ad1b0d7a0/packages/import/README.md), [App](https://github.com/ForgeAX/forgeax-engine/blob/df4c86bf12bf117ed229e2721e98d60ad1b0d7a0/packages/app/README.md), [DevKit](https://github.com/ForgeAX/forgeax-engine/blob/df4c86bf12bf117ed229e2721e98d60ad1b0d7a0/packages/devkit/README.md).

## Historical Palace evidence

<details>
<summary>Content-provenance examples from the 2026-09-15 Palace snapshot</summary>

Engine revision `2b613d2209e4335c2eab2c75ebaeb2eb269b2879`, path `apps/showcase/palace`. These source observations were not a complete executed Palace review. They do not establish the current showcase's contents or runtime API. Start with the pinned [Palace README](https://github.com/ForgeAX/forgeax-engine/blob/2b613d2209e4335c2eab2c75ebaeb2eb269b2879/apps/showcase/palace/README.md) for build instructions and asset provenance.

| File relative to the Palace directory | Evidence | Limit |
|:--|:--|:--|
| `assets/palace.pack.ts` | No public parameters; `buildPalace()` assembles meshes/materials/scene; a fixed seed generates grain texture. | Internal function arguments are not a public generator interface; the entry alone lacks its dependency closure. |
| `assets/architecture.ts` | `box`, `tube`, `column`, `rail`, `roof`, `hall` generate from dimensions/curves/bays/building rules; `buildPalace` is a fixed recipe. | It also consumes maps/precomputed data; reading generating functions alone cannot qualify the whole package. |
| `assets/environment.pack.ts` | `analyticDaylight()` calculates pixels from directions/sky formulas into a `Uint8Array`. | A binary result is not embedded prefab data; static reading does not prove consumption or appearance. |
| `assets/footprints.ts`, `assets/waterways.ts` | Map outlines/waterways are data inputs; record source, delivery, and data policy. | TypeScript tables are not generating algorithms. |
| `assets/roof-partitions.ts`, `assets/footprint-triangulations.ts` | Precomputed vertices/triangles/partitions need generator and cold-rebuild tracing. | Comments/digests do not prove regeneration after deletion. |
| `tools/roof-authoring/generate.mjs` | Uses `@matthewjacobson/str8` and `earcut` to derive partitions from footprints; tools/dependencies/inputs belong to rebuild closure. | An included tool is not evidence that formal Pack cold production runs it; map input remains data. |
| `assets/caihua.png.meta.json` | Sidecar points to external `forgeax-engine-assets/demo-assets/palace`; README also lists stone/plaque inputs. | Sidecars do not deliver source images; the snapshot is not wholly free of external assets. |

For this historical whole-package strict-policy scope, known map/image inputs fail provenance. The building rules remain useful procedural examples. Allowing auxiliary data still requires all other checks before PASS.

| Delivered situation | Calibrated decision |
|:--|:--|
| Fixed hall recipe, library-generated columns/roof, cold production and consumer evidence | Procedural asset; public parameters are unnecessary. |
| Same hall with public effective width/bays/seed | Apply G1-G7; complete defaults do not change classification. |
| Full-model Base64 hidden in a library with `decodeMesh` | C1 may pass while P1/P2 fail. |
| Rules/semantic recipe compute millions of pixels | Do not reject because of TypedArrays or output size. |
| Legal parameters/build whose values only enter logs | F1 may pass; G3 fails. |
| Parameter chooses/scales baked models | Parameter effects do not establish procedural provenance. |
| Entry needs undelivered `./lib/roof.ts` | C1 fails despite working on the author's machine. |
| Deleted "cache" breaks formal build; private author script can recreate it | C3 fails; the cache claim does not exempt P1. |
| Source/screenshots without usable execution environment | Static partial findings only; absent a proven failure, overall BLOCKED. Screenshots do not prove cold production. |

</details>

## Conclusion and report

| Overall | Condition |
|:--|:--|
| PASS | Required type is confirmed and matched; all applicable checks under the selected data policy pass with execution evidence. |
| FAIL | At least one applicable requirement is demonstrably unmet; retain remaining evidence gaps even when FAIL is already established. |
| BLOCKED | No failure is established, but type, dependencies, or critical execution evidence is unavailable; state what is missing and how to obtain it. |

Produce a concise Markdown report; no additional JSON is required:

```markdown
# ForgeAX procedural asset review

- Object / revision / delivery scope:
- Required type / actual interface type:
- Execution stage / production path:
- Data policy / authorized auxiliary inputs:
- Engine / SDK / source revision / actual Host / realm / dev-build environment:
- Overall: PASS | FAIL | BLOCKED

## Check results

| ID | Status | Evidence location / command and observed result | Issue / correction direction |
|:--|:--|:--|:--|

## Provenance and dependencies

| Output | Generating rules | Recipe / original data / cache | Delivery and resolution |
|:--|:--|:--|:--|

## Execution evidence and coverage limits

- Cold production / consumption / repetition; generator contrasts and boundary results.
- Runtime formal prepare/admit/generate, publication/current execution, cold snapshot recovery, withdrawal/cleanup, applicable platform evidence.
- Unexecuted checks, uncovered combinations, auxiliary data, conclusion scope.
```

Separate format, closure, procedural provenance, parameter, and runtime delivery findings. Partial passes never replace the overall conclusion. Source inspection cannot prove cold production, appearance, legal-input coverage, or recovery; examples and Engine tests cannot qualify another delivery.
