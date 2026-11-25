---
name: blender-computer-use-artist
description: Create, revise, animate, render, and quality-check polished Blender stills or short videos through Computer Use, using screenshot-driven art direction and Blender Python for reliable construction. Use for Blender product renders, turntables, assembly animations, publishable product videos, stylized illustrations, environments, icons, motion shots, scene cleanup, look development, lighting, materials, camera composition, or final-render improvement when Codex must operate the Blender UI rather than only explain Blender.
---

# Blender Computer Use Artist

Produce a saved `.blend` file plus reviewed preview/final renders or a verified short video. Combine visual judgment with deterministic Blender Python; do not attempt a long fragile sequence of coordinate clicks when a short script can make the same edit reliably.

## Load the companion skill

Read and follow the `computer-use` skill before touching Blender. Use its `node_repl` + `sky` runtime for every GUI action and obey its action-time confirmation policy. In particular, pause immediately before deleting existing scene data, overwriting user work, or accepting a destructive Blender dialog.

Read only the references needed for the current task:

- Read [art-direction.md](references/art-direction.md) for the brief, style selection, quality rubric, and visual diagnosis.
- Read [blender-ui-playbook.md](references/blender-ui-playbook.md) before operating Blender or injecting Python.
- Read [reference-match.md](references/reference-match.md) whenever the user supplies an image or asks to match an existing work.
- Read [product-calibration.md](references/product-calibration.md) for reference-led products with published dimensions, detachable modules, articulated parts, or identity-critical silhouettes.
- Read [motion-shot.md](references/motion-shot.md) for turntables, assembly reveals, camera moves, social-video exports, frame-sequence rendering, or MP4 delivery.
- Read [version-compatibility.md](references/version-compatibility.md) before writing version-sensitive `bpy` code.
- Read [sources.md](references/sources.md) when deeper Blender guidance or research provenance is needed.

## Define the deliverable

Turn the request into a compact production brief before editing:

```text
subject / story:
deliverable: still | turntable | short shot
style: photoreal | stylized | graphic | clay/look-dev
aspect + pixels:
duration + fps + platform:
audio / captions:
must preserve:
references supplied:
deadline/compute constraint:
output directory:
```

Infer unspecified artistic choices when they are reversible. Ask only when a missing choice changes the subject, brand identity, required likeness, destructive scope, or delivery format. For a new still, default to one hero image, a 16:9 or user-context aspect ratio, a preview at 50% resolution, and a final PNG plus `.blend`. For an unspecified product motion shot, default to a silent 6–8 second 16:9 master at 30 fps, but art-direct vertical and square versions separately instead of auto-cropping.

## Choose the execution route

Use the least fragile route that preserves artistic control:

1. **Python-first construction** — preferred for primitives, product scenes, procedural materials, repeated objects, camera/light rigs, exact transforms, and render settings.
2. **Hybrid** — use Python for scene structure and UI tools for sculpting, posing, paint strokes, node tuning, or visual placement.
3. **UI-first** — reserve for operations whose value is inherently gestural or whose current state cannot be reconstructed safely in code.

Never hide the work in an opaque one-shot script. Divide it into named stages such as `01_blockout.py`, `02_materials.py`, and `03_lighting.py`. Make reruns idempotent: find or create named collections/objects, update owned data, and avoid touching unrelated user data.

## Use an atomic build contract

Treat the script and saved checkpoints as durable production memory. For every stage:

1. state one visible intent;
2. name the objects and anchors it owns;
3. perform no more than three related mutations before read-back;
4. inspect structure plus a screenshot;
5. record the gap or pass result before continuing.

For generated product scenes, make full rebuilds genuinely idempotent. Deleting a Scene alone is insufficient because Blender may retain orphaned object, material, world, and collection datablocks. Purge only the stage's explicit namespace, fail on unexpected `.001` suffix drift, and resolve semantic motion groups by parent ancestry, dedicated collection, or explicit tag rather than broad name matching.

For attached or aligned parts, derive placement from named faces, bounds, sockets, or planes. Numerically verify the intended gap/overlap; visual closeness is not proof of contact. Build and validate one complete repeated module before instancing it. Inspect hidden connections from profile, underside, or orthographic views when the hero camera cannot reveal them.

## Production workflow

### 1. Inspect and protect

1. Open Blender with Computer Use and capture fresh app state.
2. Identify Blender version, current file path, active scene, render engine, cameras, lights, collections, and whether the file has unsaved changes.
3. Preserve existing work. Save a versioned copy before broad changes when the task is an edit. Do not overwrite the source `.blend` by default.
4. Create a dedicated collection prefixed `CU_` for generated content. Reuse it on reruns.
5. Establish absolute output paths under the user-approved workspace.
6. Run version discovery from [version-compatibility.md](references/version-compatibility.md) before setting engine, shader, color-management, or export properties.

### 2. Block out composition

Build only large forms, camera, floor/background, and one broad key light. Use real-world scale and descriptive names. Set camera framing before detail.

If a reference image exists, follow [reference-match.md](references/reference-match.md): analyze it in writing, crop a focused reference when the subject is small, match the camera, then converge from silhouette to structure to secondary breakup to detail. Upgrade an existing scene in place when practical instead of rebuilding it blindly.

For a dimensioned product, follow [product-calibration.md](references/product-calibration.md). Separate the published overall envelope from local component dimensions. Approve orthographic body and detachable-component views before the perspective hero; compute orthographic scale from both horizontal and vertical extents.

Render a low-cost clay preview. Inspect the actual render, not only the viewport. Do not proceed until all are true:

- the subject reads at thumbnail size;
- silhouette and negative space are clear;
- the focal hierarchy is obvious;
- perspective and lens choice fit the brief;
- no accidental tangencies or crop errors distract from the subject.

If the composition is weak, change camera and large forms rather than adding detail.

### 3. Build production geometry

Use non-destructive modifiers where useful. Apply transforms only when required by downstream operations. Add small bevels to manufactured edges so lighting can describe form. Keep polygon density proportional to screen size. Instance repeated geometry.

For every hero object, check:

- scale and normals are intentional;
- silhouette holds from the camera;
- close-up curvature is smooth;
- modifiers do not create intersections or shading artifacts;
- tiny details contribute at delivery resolution.

### 4. Develop materials

Start from Principled BSDF or an equally coherent physically based model. Separate base color, roughness, metallic, transmission, normal, and displacement roles. Use measured-looking values and restrained variation; avoid pure white, pure black, and perfectly uniform roughness unless the style requires them.

Judge materials under a neutral look-development light before dramatic lighting. Add imperfections at multiple scales only when they support material identity. Ensure image textures use correct color-space roles: color textures as color data, normal/roughness/masks as non-color data.

### 5. Light for form and story

Light in this order:

1. key light for direction and shape;
2. fill or environment for readable shadow detail;
3. rim/accent lights for separation;
4. practical/emissive lights only when motivated;
5. atmosphere or volume last.

Prefer large area sources and controlled contrast. Avoid adding lights to fix a bad material or exposure. Check highlights for clipping and verify that the background supports, rather than competes with, the subject.

### 6. Look development and polish

Render at least three meaningful preview variants that change one major variable at a time, such as camera, key direction, or background value. Save them with stable names. Compare them visually and select the strongest; do not average incompatible directions.

Then add only high-value polish:

- contact shadows and grounding;
- secondary reflections and edge highlights;
- deliberate depth of field with the focal subject sharp;
- restrained bloom/glare, vignette, grain, or color balance;
- background detail that reinforces depth and scale.

Use compositing to finish a sound render, not to rescue broken geometry, materials, or lighting.

For a reference-match or regression task, run [render_compare.py](scripts/render_compare.py) as a diagnostic after each meaningful candidate. Use its SSIM-like, difference-hash, color, and edge metrics only to detect convergence or drift. Never treat a similarity number as an artistic-quality score; the screenshot review remains authoritative.

### 7. Animate motion shots

Approve a still keyframe before animating. Then read [motion-shot.md](references/motion-shot.md) and choose a motion grammar: turntable, assembly reveal, camera orbit, feature close-up, or a restrained combination. Save an animation copy instead of overwriting the approved still scene.

Use the bundled tools where they fit:

- [product_motion_setup.py](scripts/product_motion_setup.py) for declarative roots, drop groups, camera keys, and light sweeps;
- [motion_keyframe_preview.py](scripts/motion_keyframe_preview.py) for sparse keyframe renders before committing compute;
- [motion_sequence_render.py](scripts/motion_sequence_render.py) for resumable PNG-sequence delivery;
- [encode_video.py](scripts/encode_video.py) and [video_audit.py](scripts/video_audit.py) for H.264 encoding and technical verification.
- [product_scene_preflight.py](scripts/product_scene_preflight.py) before animating a namespaced product scene, to catch suffix drift, orphaned owned objects, and unlinked shader outputs.

Inspect at least the first frame, one transition frame, the midpoint, one late frame, and the final frame. Do not render the full sequence until framing, contact, exposure, and motion continuity pass those checks.

### 8. Final render and verification

Use the current stable engine available in the installed Blender version. Prefer Cycles for a realism-critical final; use Eevee when the style or turnaround benefits from it. For Cycles, use adaptive sampling and denoising as tools, then inspect whether denoising erased fine detail. Increase samples only when visible noise remains.

Run [scene_audit.py](scripts/scene_audit.py) inside Blender before final delivery. Resolve every `BLOCKER` and explain any intentional `WARN` item.

Render the final to a lossless format. Re-open or display the saved render and inspect it at fit-to-screen and 100% crop. Confirm:

- output dimensions and alpha are correct;
- no missing textures, pink surfaces, fireflies, banding, or obvious denoise smearing;
- focus, edges, and important texture detail survive at final resolution;
- the output exists at the reported absolute path;
- the `.blend` is saved after the final settings change.

Capture evidence appropriate to the asset: hero/beauty, an opposite three-quarter or proportion-revealing profile, and a solid/wire overview when geometry matters. Add close contact views for assemblies and a side-by-side reference comparison when matching an image.

For video, prefer a lossless PNG sequence as the durable master. Inspect for missing or duplicate frames, then encode a broadly compatible H.264 `yuv420p` MP4 with fast-start metadata. Run `video_audit.py` and decode the complete file before delivery. Report whether the master is silent and whether platform-specific crops remain outstanding.

For an attached animation, verify evaluated world-space seating coordinates at the opening and return frames. Preserve child world pose with an explicit `matrix_parent_inverse`; then animate unlock, axial clearance, lateral reveal, reverse lateral motion, axial reseating, and relock in that physical order. Add a moving internal collar or light baffle when an oblique camera could see through a zero-thickness contact plane.

## Computer Use control loop

After every one or two UI actions, fetch fresh Blender state before choosing the next action. Never reuse stale accessibility indexes. Prefer keyboard shortcuts and Blender Python over coordinates. Use screenshots whenever the accessibility tree does not expose the viewport, render, modal, or editor state.

For each production stage:

1. stage a small Python file in the approved workspace;
2. switch the hovered Blender area to Python Console with `Shift+F4`;
3. execute it with the command pattern in [blender-ui-playbook.md](references/blender-ui-playbook.md);
4. read the console result and capture fresh app state;
5. switch to camera view or render result and visually inspect;
6. save a checkpoint only after the stage passes its quality gate.

If a script fails, stop issuing further scene mutations. Capture the full traceback, fix only the failed stage, and rerun it. Do not restart Blender unless state is corrupted and the user-approved checkpoint is saved.

## Quality gate

Use the rubric in [art-direction.md](references/art-direction.md). Delivery requires:

- no technical blocker;
- at least 80/100 overall;
- at least 12/20 in composition, lighting, and materials individually;
- two visual review cycles after blockout;
- a saved final render or verified video and editable `.blend`;
- for motion, at least five reviewed keyframes, a complete frame sequence, and a passing video audit.

Issue an explicit verdict:

- `SHIP` — all gates pass;
- `SHIP WITH NOTES` — no blocker or major defect, with documented minor gaps;
- `NO-SHIP` — any blocker, unverified major visual claim, or unresolved camera/silhouette miss.

Do not claim “high quality” merely because the render completed. Report the achieved style, output paths, Blender version/engine, key compromises, and validation performed.

## Failure recovery

- **Wrong editor or shortcut context:** capture state, move focus to the intended area, and retry once.
- **UI controls missing:** use version-appropriate `bpy` properties or search the current manual; do not guess repeated coordinates.
- **Black render:** verify active camera, light/world energy, exposure, render visibility, clipping, and compositor connections.
- **Pink render:** resolve missing image paths or pack approved assets.
- **Noisy render:** find the noisy light/material path, enlarge sources or simplify caustic paths, then adjust sampling.
- **Flat render:** revisit large-form lighting, value grouping, material roughness, and camera separation before adding post effects.
- **Slow/crashing render:** save, reduce subdivision/volume steps/texture size for preview, use instances, and isolate the expensive feature.
- **No FFmpeg render format:** keep the approved PNG sequence and use `encode_video.py`; never silently change the requested codec or dimensions.
- **Motion flicker or jumps:** inspect adjacent source frames around the defect, verify interpolation and parenting, then rerender only the affected range before re-encoding.
