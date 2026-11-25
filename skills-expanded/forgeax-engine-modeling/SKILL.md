---
name: forgeax-engine-modeling
description: >-
  ForgeaX editable mesh modeling in .pack.ts builds: selectors, labeled operations, curves,
  surfaces, rigs, UVs, bakes, MeshAsset export and forgeax model tools. Use when creating,
  changing or checking a game mesh in code.
---

# forgeax-engine-modeling

`@forgeax/engine/modeling` is a deterministic, editable n-gon mesh kernel in pure TypeScript.
A `.pack.ts` build calls it as ordinary functions and returns `{ 'mesh/<key>': MeshAsset }`
(plus a scene and clip for rigs) to the existing Pack, Catalog and Renderer owners.

It is **not** an editor (no viewport to click in; you see your work only through
`forgeax model render`), not a CAD B-rep kernel (curves and surfaces tessellate
into the mesh), and not a runtime compiler (players load the exported mesh).

Contract SSOT: [`packages/modeling/README.md`](../../packages/modeling/README.md): data model, selection, session
contract and a reference map. Each consideration below links one `reference/*.md` file; open
it when the task needs it. Examples, smallest first, with what each teaches:
[`examples/README.md`](../../packages/modeling/examples/README.md).

Professional know-how (what to look at, trade-offs, thresholds, recovery from failure codes) is in
[`knowledge/`](../../packages/modeling/knowledge/); open the topic that matches the task:

| Task | Topic |
|:--|:--|
| Choosing an approach, blocking out from drawings | [design-methodology](../../packages/modeling/knowledge/design-methodology.md), [design-drawings](../../packages/modeling/knowledge/design-drawings.md) |
| Vehicles, hard-surface bodies, panel gaps | [vehicle-design](../../packages/modeling/knowledge/vehicle-design.md) |
| Smooth surfaces, patch networks, curvature quality | [surface-quality](../../packages/modeling/knowledge/surface-quality.md), [nsided-patches](../../packages/modeling/knowledge/nsided-patches.md) |
| Characters, stylized bodies, faces, hair | [stylized-character](../../packages/modeling/knowledge/stylized-character.md) |
| Mechanisms, joints, mobility | [mechanism-design](../../packages/modeling/knowledge/mechanism-design.md) |
| Detail catalog, animation presentation | [detail-catalog](../../packages/modeling/knowledge/detail-catalog.md), [animation-presentation](../../packages/modeling/knowledge/animation-presentation.md) |
| UV cuts, low poly, bakes | [uv-cuts-lowpoly](../../packages/modeling/knowledge/uv-cuts-lowpoly.md), [baking-uv](../../packages/modeling/knowledge/baking-uv.md) |
| Watertight meshes, tolerances | [watertight-tolerance](../../packages/modeling/knowledge/watertight-tolerance.md) |

## The smallest build

```ts
import { definePack, definePackageId } from '@forgeax/engine/pack/source';
import { model, sel } from '@forgeax/engine/modeling';

export default definePack({
  schemaVersion: '2.0.0',
  packageId: definePackageId('01900000-0000-7000-8000-00000000a0de'),
  parameters: [{ name: 'depth', type: 'f32', default: 0.03, minimum: 0.005, maximum: 0.1 }],
  build: ({ values: p }) => {
    const m = model();
    m.box({ size: [0.42, 0.3, 0.36], tag: 'shell' });
    m.inset(sel.tag('shell').and(sel.facing('+z', 10)).largest().one(), {
      thickness: 0.02, region: 'merged', label: 'visor',
    });
    m.extrude(sel.createdBy('visor', 'inner'), { distance: -p.depth, region: 'merged', label: 'visor-depth' });
    m.markSharp(sel.edges.dihedral('>', 40));
    m.uv.project({ mode: 'box', scale: 0.5 });
    m.assign(sel.createdBy('visor-depth', 'top'), 'glow');
    return m.finish({ key: 'helmet', normals: { mode: 'weighted' } });
  },
});
```

Look at it: `forgeax model render --source <file>.pack.ts --json`, then read the PNGs it lists.
`forgeax help model <command>` gives exact flags ([tools](../../packages/modeling/reference/tools.md#forgeax-model--commands)).

## Invariants

- **Y-up, +Z is front**, meters, angles in degrees. `facing('+y')` is the top.
- **Selectors are expressions** re-evaluated at every call; never keep face or vertex ids.
  An empty selection fails (`model-selection-empty`); it never means "all" (`sel.all()`).
- **Identity is yours to name**: a `tag` survives derivation; an operation's `label` writes
  roles read back with `sel.createdBy(label, role)`. Unlabeled operations add no role.
- **Magnitudes have no defaults** (`distance`, `thickness`, sizes, segment counts).
- **The first failure poisons the session**; `finish()` returns that `ModelingError` with
  `code`, `hint` and `detail.site = { op, opIndex, label }`. Fix that call.
  `m.try(() => ...)` rolls back a block whose failure should pick another construction.
- **Topology edits leave new faces without UVs**: project or unwrap after the last edit;
  `finish()` requires complete `uv0`.
- **Output depends only on source and parameters**: no `Date`, `Math.random` or `fetch`;
  derive variation from a seed.
- **Budgets**: a Pack build has 15 s, each `forgeax model` rebuild 60 s, and a runtime rebuild
  should stay near 100 ms. Heavy work moves into a cooked `MeshJob`
  ([tools § Budgets](../../packages/modeling/reference/tools.md#budgets-and-isolation)).

## Considerations

Each modeling task raises some of these. They have no fixed order, and most tasks skip some.

**Purpose and viewing.** Who sees the asset, from how far, and whether it moves decide the
face budget, the detail level and whether it needs a rig or bakes. A prop seen at game
distance needs a clear silhouette and material breaks, not support loops
([export § Performance tiers](../../packages/modeling/reference/export.md#performance-tiers)); `node packages/modeling/bench/scale-f1.mjs --fixture f1 --out <file>` measures kernel scale on a large fixture).

**Form source.** Pack `parameters` hold the sizes worth tuning. Reference images become
design drawings; `m.threeView` intersects 2-3 orthographic outlines into a blockout and
`extrudeContour` turns one outline into a prism ([drawings](../../packages/modeling/reference/drawings.md),
example `body-blockout`).

**Shape strategy.** Match the construction to the form, and mix them freely:

| Form | Start from | Reference |
|:--|:--|:--|
| Boxy, machined, panelled | primitives, `inset`, `extrude`, `shell`, `mirror` | [operations](../../packages/modeling/reference/operations.md) |
| Cut-outs, holes, unions | booleans on closed operands | [booleans](../../packages/modeling/reference/booleans.md) |
| Tubes, frames, cables, springs, branches | `sweep`, `loft`, `pipeNetwork`, `array` | [sweep-deform](../../packages/modeling/reference/sweep-deform.md) |
| Organic bodies, heads, creatures | a low cage, then `subdivide`, creases, `arap`, deformers; low poly: `loft` sections, flat normals | [sweep-deform](../../packages/modeling/reference/sweep-deform.md) |
| Clothing, layers, hair cards | `shrinkwrap`, `layer`, `strands`, `knife` | [artist-editing](../../packages/modeling/reference/artist-editing.md) |
| Smooth class-A panels, car bodies | NURBS curves and surfaces, patch networks | [surfaces](../../packages/modeling/reference/surfaces.md) |
| Blobby merges, low-poly facets, retopology | `voxel`, `simplify`, `remesh`; `lowpoly({ slivers })` removes narrow faces | [voxels-remesh](../../packages/modeling/reference/voxels-remesh.md) |
| Grilles, vents, thin perforations too fine to model | `thinHole` / `thinHoleCheck` (a bake recipe, not geometry) | [uv-bake](../../packages/modeling/reference/uv-bake.md) (example `thin-vent`) |
| An existing mesh | `lift` | [operations](../../packages/modeling/reference/operations.md#lifting-existing-meshes) |

Symmetric forms: model one half and `mirror`. Build parts in separate functions and `append`
them; a function that builds into a session is the reuse unit
([export § Reuse](../../packages/modeling/reference/export.md#reuse-across-packs)).

**Detail.** Edge treatment (`bevel`, fillets, blends, support loops), panel and shut lines,
and the mechanical recipes (bolts, hinges, gears, pin joints) are in
[detail](../../packages/modeling/reference/detail.md). `markSharp` sets hard normals as author intent; there is no
weld-angle threshold.

**Motion.** Do not animate by rotating mesh faces. Bind parts to a `rig`, give joints limits
and key a path; its `finish` exports part meshes, a scene and a clip. Interference,
clearance and mobility checks belong to the same owner ([rig](../../packages/modeling/reference/rig.md), examples
`limb-choreography`, `door-hinge`, `transforming-limb`).

**Appearance.** Assign material slots with `assign(faces, slot)`. Procedural Standard
materials, textures and text are in [materials](../../packages/modeling/reference/materials.md). UV projection,
unwrapping, automatic charts (`uv.unwrap` / `uv.auto` accept opt-in `refine: 'slim'`), trim sheets, and baking a
detailed mesh onto a low one are in [uv-bake](../../packages/modeling/reference/uv-bake.md) (example `armor-bake`);
`cage-clip` and `stray-detail` bake issues now carry clustered findings with a fix `hint`.
For categorical surface masks, set `BakeSlot.materialId` explicitly and bake `materialId`;
appearance colors and the repeating default palette do not establish material identity.

**Seeing and verifying.** Render often and look; numbers alone do not reveal a wrong shape.
`forgeax model render` draws real Engine frames (orthographic sheets, wireframe, overlays,
sections, x-ray, zebra and curvature). `replay` shows every step, `select` tries a selector,
`history` maps faces to source lines, `validate` finds topology and self-intersection
problems (`validate({ shells })` reports `shell-overlap` when a union-once solid still carries overlapping shells), `diff` compares variants, and `pose` / `interference` check rigs
([tools](../../packages/modeling/reference/tools.md), [validation](../../packages/modeling/reference/validation.md)).
`m.checkpoint('name')` marks states the tools can render or select.

**Delivery.** `finish({ key, normals })` exports the mesh; normal modes, LODs and cooked jobs are
in [export](../../packages/modeling/reference/export.md); skinned LODs reduce joints with `reduceSkinForLod`
([rig](../../packages/modeling/reference/rig.md)). A rig scene needs the Pack to declare its
`sceneComponents` ([rig](../../packages/modeling/reference/rig.md)). `model render --materials auto` binds the
Pack's `material/<slot>` outputs to slots of the same name (`materialBinding` reports each slot);
`model render` also returns `renderer { backend, adapter, software }`; `software` is true on Lavapipe or SwiftShader, so label pixel-only findings from such a render;
bakes and the full scene show in `forgeax project preview` inside a game project (see `forgeax-engine-cli`).
An offline recipe producing meshes, materials and processed textures can use `AssetsJob`
and `assetsJobSources`; register it with `createMeshJobCooker` and forward its `cache` to
`bakeMaps`. Keep the recipe in the Pack's static import closure; one job serves its declared
outputs through the existing Pack producer, without a project-owned cache or baked defaults.

## Failure modes

| Symptom | Usual cause |
|:--|:--|
| `model-selection-empty` on `+z` | Z-up habit; the hint names the axis that would match |
| Faces picked by index break after an edit | Select by tag or label/role instead |
| `finish` fails on `uv0` | A topology edit after the UV call; project or unwrap last |
| `model-degenerate` on inset, shell or bevel | The magnitude exceeds what the face or wall allows; read `expected` |
| `model-work-budget` | Too many faces, or heavy work inside the build; reduce it or cook a `MeshJob` |
| Validate passes but the shape looks wrong | Validation checks topology, not the brief; render and compare |
| Faces stay on an earlier rig part | A misspelled label in a binding selected nothing; compare `rig.parts()` |
| Faceting or seams on curved forms | Missing sharp/smooth intent or too few segments; render `--overlays '["sharp"]'` |
| `forgeax: command not found` in an Engine checkout | Run `node packages/engine/dist/bin/forgeax.mjs` from the Engine root |
| `model-render-backend-unavailable` | No Vulkan device; [tools § render](../../packages/modeling/reference/tools.md) names the software driver |
| Render colors differ from the Pack's materials | `model render` defaults to `--materials palette`; pass `--materials auto`, name outputs `material/<slot>`, and a rig needs `finish({ materials })` ([rig](../../packages/modeling/reference/rig.md)) |
| `pack-parameter-invalid` on load | `parameters` must be a non-empty array; declare at least one tunable size |
| `model-capability-unavailable` | Outside this version (ABF/ARAP unwrap, native compute, MCP); build what exists |

The closed failure union and its `detail` shapes:
[README § Session contract and errors](../../packages/modeling/README.md#session-contract-and-errors).
