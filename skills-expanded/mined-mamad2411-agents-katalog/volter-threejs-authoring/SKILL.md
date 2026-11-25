---
name: volter-threejs-authoring
description: Build, rig, animate, diagnose, and visually refine polished native Three.js scenes and procedural assets with direct Object3D code, reusable construction helpers, geometry libraries, and an inspect-render-critique loop. Use for procedural models, rigid mechanical armatures, environments, static props, stylized materials, lighting, cameras, scene composition, or an agent-focused Blender-like workflow. Use volter-3d-assets alongside this skill when the result should become a source document and a baked GLB. Do not use for Blender bpy work or imported skeletal retargeting.
---

# Volter Three.js Authoring

Author ordinary project source against Three.js. Treat the source module and
live `Object3D` graph as truth. Use helpers for leverage, not as a replacement
scene language.

## Establish the authoring surface

1. Read the project instructions and architecture.
2. Locate the Three root or modeling build entry, existing helpers,
   renderer setup, and verification commands.
3. Start or reuse the Volter editor immediately and keep it open.
4. Capture a fixed-camera visual baseline.
5. Inspect the live hierarchy, selected-object facts, renderer state, and
   console before changing code.

Never introduce a parallel entity tree, semantic operation log, generated
scene JSON, or wrapper around ordinary Three.js access for agent control. Give
important objects stable `Object3D.name` values or project metadata.

Also use `volter-3d-assets` for reusable source-backed assets,
`volter-animation-assets` for imported skeletons or clips, and
`volter-environment-art` for whole-scene art direction.

## Choose the lowest sufficient layer

Use these layers in order:

1. Use Three.js directly for transforms, parenting, materials, lights,
   cameras, curves, standard geometries, loaders, and animation.
2. Use an existing project helper for repeated high-value construction.
3. Use official Three.js addons before adding dependencies.
4. Use a proven specialist library for booleans, BVHs, topology repair, or
   asset optimization.
5. Add a helper only after the same construction or failure-prone calculation
   appears more than once.

Keep alternate library representations temporary. Return a normal
`BufferGeometry`, `Mesh`, `Group`, or other native `Object3D`.

Read [references/helper-catalog.md](references/helper-catalog.md) before adding
modeling capabilities or dependencies. That catalog answers *which op* — for
*which surfacing mode* (palette, shader look, tiling projection, card, decal,
provider retexture, procedural mask) and whether the asset needs UVs at all,
walk the eight modes cheapest-first in the `volter-3d-assets` skill's
`references/surfacing.md`.

## Author raw code

Write named functions that return real objects:

```ts
function createObservatory(materials: Materials): THREE.Group {
  const root = new THREE.Group();
  root.name = 'observatory';
  root.add(createTowerShell(materials.ivory), createTelescope(materials));
  return root;
}
```

Prefer hierarchy and local coordinates. Give each substantial assembly a
meaningful origin. Share materials intentionally. Seed authored randomness.
Use raw Three.js whenever a helper becomes awkward.

## Author shader looks as native GLSL

Keep shader source in ordinary `.vert`, `.frag`, or `.glsl` files and bind it
with `THREE.ShaderMaterial` directly. A sibling `name.vert.glsl` +
`name.frag.glsl` pair is the portable convention Asset Lab recognizes; it is
not a Volter format. Keep authored uniform defaults, defines, textures, and
material composition beside the owning material in TS/TSX, where the runtime
actually reads them. Never add a `.shader.json`, uniform sidecar, or generated
shader graph to duplicate those facts.

Open either GLSL file from Content to inspect the pair against a real WebGL
preview. Asset Lab is visual-only: it does not duplicate the project's coding
surface or write shader source. Edit the ordinary GLSL files with your normal
coding tools; the open preview reloads them, and compiler diagnostics name the
native file, stage, and source line. Use the reflected Inspector uniforms to
explore values, geometry, and time/resolution inputs, then move accepted
defaults into the owning TS/TSX—the controls are session-only by design.
Resolve every compiler diagnostic before judging the look in its real scene,
because neutral preview geometry cannot prove lighting, depth, transparency,
postprocessing, or the game's actual texture bindings.

## Compose postprocessing directly

When a game needs postprocessing, add `@react-three/postprocessing` to that
project and import its components directly. Do not create a Volter chain file,
effect registry, wrapper component, or JSON descriptor. The owning scene's JSX
is already the ordered chain; conditionally render one effect to bypass it and
move its JSX child to reorder it. Keep the finishing order restrained: render,
limited AO, bloom, color grade, anti-aliasing, then output color/tone conversion.

A 3D `.cube` color grade is an ordinary portable LUT. Open it from Content for
Asset Lab's visual before/after comparison; intensity and interpolation there
are session-only exploration. Load the accepted LUT with Three's
`LUTCubeLoader`, hand its `texture3D` directly to the library's `LUT` effect,
and author the accepted strength in TSX. Judge each bypass at the same camera,
pose, exposure, and simulation time. Asset Lab deliberately has no chain source
view: edit the ordinary TSX with the project's coding surface and watch the
running viewport reload it.

## Register reusable R3F prefabs

An R3F component becomes a Content prefab only when the project declares a
portable CSF story for it. Colocate `<Name>.stories.tsx`, set
`meta.component` to the component itself, and author at least one standalone
representative state. Update the story whenever the prefab's required props or
display contract changes.

The editor mounts the composed story off-screen and photographs that exact
state. It never infers prefab intent or appearance from export status, scene
placement, or a GLB path referenced by the component. A storyless component is
valid scene implementation, but it does not belong in Content. Keep model
files in Models; the component story may render a model, but does not turn the
model into the component or the component into an inferred prefab.

Use ordinary Storybook `args`, decorators, and loaders for required context.
For a suspending R3F loader, do not put `<Suspense>` around the story content:
the preview captures the first commit, so a committed fallback would be the
photographed subject.

## Build for visual quality

Establish these before micro-detail:

- a readable primary silhouette;
- asymmetry and at least three depth layers;
- a clear focal object and subordinate forms;
- intentional key, fill, and rim light;
- a restrained material palette with readable value and surface contrast;
- camera framing chosen for the composition, not merely fitting bounds.

Work through three frequency bands:

1. Primary forms carry silhouette, proportion, and composition.
2. Secondary forms explain construction: profiles, frames, ribs, supports,
   openings, joints, and material transitions.
3. Tertiary accents appear only where the intended camera can read them.

A primitive remains blocking geometry until it has deliberate proportions,
edge treatment, a believable relationship with adjacent forms, and suitable
surface response. Object count is not a quality metric; count visible authored
decisions.

Treat emissive materials, ambient occlusion, and bloom as accents. If an effect
erases ribs, frames, texture, or material boundaries, reduce the effect before
adding geometry.

## Author stylized rendering honestly

For cel shading, use a nearest-filter gradient ramp with `MeshToonMaterial`.
For hard linework, combine inverted back-face hulls for silhouettes with
`EdgesGeometry` for intentional internal creases.

Treat style as a runtime-wide contract, not a promise made by one builder.
Inventory the live material classes after every async GLB and modeled object
has loaded. A helper that exists but is never imported by the mounted root has
implemented nothing. Apply the policy to the real runtime graph and expose a
small debug report so playtests can prove which materials were converted,
preserved, or excluded.

Author the policy per material family and per material slot. Use harder ramps
for focal props, characters, and readable detail; use a softer, higher-floor
ramp for broad architectural planes so point lights do not create concentric
band stains or crush the whole foreground. Preserve intentional Basic,
transparent/glass, emissive, and special-effect materials. When replacing a
material, carry forward its maps, vertex colors, alpha test, AO/normal/emissive
inputs, side, depth, and blend settings. A mixed material array must preserve
and convert each slot independently.

Attach derived ink beneath source meshes so animation and transforms remain
automatic. Exclude transparent smoke, glass, skies, and soft background forms
unless the art direction explicitly requires outlines.

An ordinary inverted-hull `ShaderMaterial` that expands `position` and
`normal` is not skinning-safe. Reject `SkinnedMesh` at the outline helper
boundary unless the shader explicitly includes and proves skinning/morph
chunks; a caller-side entity whitelist is not sufficient. For character ink,
use a deformation-aware path and inspect it in bent shoulder, hip, elbow,
knee, wrist, and ankle poses. Expose and assert that a rigid-only path outlined
zero skinned meshes.

Specify silhouette width in pixels when framing can change. Derive view-space
offset from depth, projection scale, and drawing-buffer height; refresh the
height after resize. Keep creases thinner and fade them sooner than
silhouettes. Prefer dark hues related to each material family over uniform
black.

Author stylized profiles per material family. Control lit/shadow color, band
threshold and softness, graphic highlight, rim, and thresholded specular
response. Preserve native Three.js lighting and shadows. `onBeforeCompile` is
version-sensitive; compile it in real WebGL after Three.js upgrades.

Run an ink-off diagnostic. The same fixed-camera frame must remain readable
through value grouping, shadow hue, highlights, and rims. Contours clarify
forms; they do not rescue confused materials.

Use only visual-inspection boundaries as workflow steps. One style iteration
produces and inspects, at the same camera and pose: the prior runtime frame,
toon with ink disabled, toon with ink enabled, and the full game composite.
Keep typecheck, shader compilation, material census, and scene validation
inside that same step; they are supporting checks, not separate milestones.
Reject broad-plane band stains, shadow crush, lost texture identity, mixed PBR/
toon assets, bind-pose outlines, or HUD/camera mismatch before continuing.

Use postprocessing as a finishing layer. A restrained order is render, limited
AO, restrained bloom, subtle color composite, SMAA, then output color/tone
conversion. Keep project-owned presentation separate from exported model
content.

## Rig at the correct deformation layer

- Use `Object3D` or `Bone` hierarchies for rigid articulated machinery.
- Use `SkinnedMesh` only for continuous deformation across a joint.
- Attach rigid accessories directly to their owning joint.
- Use morph targets for localized shape changes not naturally expressed by a
  joint.

Put pivots at physical joint centers and author child geometry in local
coordinates. A `THREE.Bone` does not require a `SkinnedMesh`; use bones when
armature semantics and `SkeletonHelper` aid inspection.

Keep pose policy separate from construction. Use a deterministic pose function
for procedural locomotion and exact comparisons. Use native `AnimationClip`
and `AnimationMixer` when motion must be blended, serialized, edited, or baked.
Apply contact or IK correction after the base pose.

Validate a full cycle. Sample every driven joint and end effector at exact
times; reject non-finite transforms, duplicate names, insufficient joint
range, and negligible contact travel. Inspect support and passing poses. Hide
rig helpers outside diagnostics.

Animation cadence is separate from render cadence. For stepped motion,
quantize pose time while rendering and responding at display refresh rate.
Derive transforms from stored base values; do not accumulate with `+=` unless
drift is intentional.

## Use the walking castle as removable source

The `castle` capability is a removable premade: editable construction,
rigging, ink, validation, and bake source that a project is expected to
remake. **It is not in your project until you add it** — `volter-game-editor add castle`
(invoking one of its registered tools through the CLI also adds it, loudly,
but reading its source is not an invocation). It adds its
required capabilities, copies transparent source into `src/lib/` and
`src/contributions/` and `src/tools/`, and registers the project tools without overwriting existing
files. Restart `volter-game-editor edit .`, open **Tools → Walking Castle Builder**,
validate, and bake. Never import the premade from the engine checkout at
runtime.

Edit `src/lib/castle/generate.ts` first for visual changes. Read
`rig.ts` only for mechanical or gait changes and `presentation.ts` only for a
castle-specific showcase. The generated GLB is a disposable output; the copied
TypeScript remains the project's source of truth. Read the bundle's
`src/lib/castle/README.md` and `src/lib/castle/PROVENANCE.md` before changing
its integration boundary.

## Add secondary motion as a project dependency

The `motion` capability ("Secondary motion", `volter-game-editor add motion`) is a removable
kit for spring-bone chains and
Jolt soft-body cloth. It preserves failure-prone setup and lifetime rules
without making hair, capes, garments, or physics tuning part of engine core.

Like every capability it is ADDED, not shipped: `volter-game-editor add motion` copies
`src/lib/motion/` in and
declares its two direct dependencies. Initialize Jolt in the project and pass
the resolved module into the cloth helper; import the VRM spring-bone library
directly when the project needs its manager or types.

Use spring chains for hair, tails, straps, and short strips. Use soft-body
cloth only when drape and collision justify the cost. Collider placement,
topology, materials, and tuning belong beside the character that uses them.
Always render moving acceptance evidence: these helpers can typecheck and pass
structural tests while still clipping, tunneling, exploding, or appearing
frozen.

## Render self-review is MANDATORY — the look protocol

After EVERY modeling milestone — a new mesh, a kit op applied, a material/
shading change, a fit or weld — render your work and LOOK at the pixels
before proceeding. Self-reports ("the topology is correct", "tests pass")
are not visual evidence; only a render is.

**Everything below happens inside YOUR project directory.** The one command
is `volter-game-editor screenshot`, and the module lane is the asset loop:

1. Look at a builder: `volter-game-editor screenshot src/models/<thing>.ts` runs that
   module's default export headlessly in Node, exports the `Object3D` it
   returns to an in-memory GLB, and photographs it in your live editor
   session. `--export <fn>` picks a non-default export. Nothing is written
   under `public/` and no provenance record is created — a look is not an
   export. (It needs a live session for this project: `volter-game-editor edit .`.)
2. Look at a baked file: `volter-game-editor screenshot <path.glb>` — front/right/top/
   3-quarter plus a contact sheet, through the Asset Lab.
3. Ask for canonical angles rather than ad-hoc ones: `--shots <set>`
   resolves the registered `project.<set>.previewShots` tool, and a lib that
   registers a set gets it by default. `--size`/`--width`/`--height` frame
   it; `--compare <ref.glb>` scores silhouette IoU against a reference.
4. READ every printed PNG before the next edit: silhouette, shading, nothing
   clipped or inside-out, vert/tri budget. A defect you can see is a defect —
   fix it before building more on top of it.
5. Framing is automatic from your mesh's bounding box — if a render looks
   empty or mis-framed, your geometry (scale/position/origin) is wrong, not
   the camera. The corollary is a real blind spot: an asset lane auto-frames
   its subject, so it can NEVER show you a wrong origin, a floating contact
   plane, or a scale that disagrees with the world. Only a scene shot can —
   `volter-game-editor screenshot` with no target (play mode, whole stack) or `volter-game-editor
   screenshot <entityId>` (one entity where it stands, under the scene's own
   lighting).

> Engine-repo aside — not for game projects. When you are working inside the
> Volter engine checkout itself (no game project, no editor session), the
> equivalent is `node packages/engine/e2e/turntable/capture.mjs <subject>`,
> run from the checkout root; it boots and tears down its own server. Point
> it at your own builder with `capture.mjs file --module
> /<repo-relative-path>.ts --export <fn>`, add `--zooms full,top,detail`
> (detail takes `--focus x,y,z`) for close-ups, and `npx biome check --write
> <your-file>.ts` before finishing, since unformatted engine files block the
> repo's lint for everyone.

## Run the refinement loop

For every meaningful iteration:

1. Build or typecheck.
2. Reload or rebuild the raw source graph.
3. Inspect names, bounds, hierarchy, camera, renderer statistics, warnings,
   and failed requests.
4. Freeze procedural motion at a known time.
5. Capture the same viewport and camera as the baseline.
6. Identify the largest visible defect.
7. Make the smallest source change that tests the diagnosis.
8. Repeat until the pixels are visibly better.

When the project has `@volter/game-live`, make the shared editor view the evidence
boundary instead of taking an unrelated page screenshot:

```ts
const shown = await editor.present({
  version: 1,
  document: { kind: 'tool', id: 'walking-castle-builder' },
  viewport: { camera: 'isometric', frame: 'document' },
});
const actual = await editor.currentView();
const capture = await editor.captureActiveDocument();
```

Treat `actual` as the postcondition and `capture.document` as provenance for
the pixels. `present()` is an intent, not proof: the active document may have
degraded, failed to mount, or been changed by the human. Keep the returned
share link with critique notes so the same subject, camera, diagnostic, and
utility can be reopened for the next cycle.

Do not declare success because code is shorter, more reusable, or produces
fewer commands.

## Validate the deliverable

Before finishing:

- run project production/type validation;
- verify no runtime or WebGL shader errors;
- verify stable names and direct graph inspection;
- verify derived ink is non-interactive and follows source transforms;
- verify outline width at default and materially different framing;
- verify material design with ink disabled;
- verify every loaded asset participates in the intended runtime material-family policy;
- verify broad planes have no band stains or crushed readable shadow detail;
- verify rigid-only outline paths report zero outlined `SkinnedMesh` objects;
- compare finishing effects at one exact pose;
- verify deterministic rebuild and bounded animation;
- verify a full-cycle report has finite, meaningful ranges and travel;
- verify cleanup and disposal;
- compare final browser-rendered evidence against the baseline;
- record generally useful helpers in the catalog while keeping one-off
  assemblies project-owned.

When a helper improves one scene but harms another, keep it local until its
contract is understood.
