---
name: img2vfxblender
description: Turn VFX screenshots, annotated boards, or video frames into evidence-backed animated Blender VFX studies, reusable layer families, and an explicit NineTails preset handoff. Use for image-to-VFX reconstruction, transition timing, procedural rings/ribbons/dust/shields, layer isolation, or independent critique of an animated .blend. A Blender preview does not establish Niagara compatibility or gameplay readiness.
---

# img2VFXblender

Reconstruct the effect's **read across time**, with editable layers and defensible evidence. A convincing peak frame is insufficient when anticipation, motion, contact, cancellation or the tail is wrong.

Adapted from img2blender's source admission, feature mapping, deterministic checkpoints and independent critique. Replace its solid-object assumptions with temporal coverage, intentional translucency, layered contrast and gameplay readability. VFX cards may intentionally be open, emissive or camera-facing; do not demand watertight geometry, PBR-only shading, or equally convincing backs where the delivery contract does not need them.

## Choose the requested output

- **Study:** analyze references and produce a source-linked layer/timing contract. Stills are enough to propose motion; mark it as proposed. Do not force a Blender render or engine authoring onto an analysis-only request.
- **Blender prototype:** deliver an editable animated `.blend`, deterministic frame evidence, isolated layers, a Lite variant and an independent visual review. This is the default when asked to turn images into VFX in Blender.
- **Export / NineTails handoff:** additionally validate the requested mesh, texture/flipbook or animation export. Read [engine-handoff.md](references/engine-handoff.md). Do not promise automatic Blender-to-Niagara conversion.

The current request and existing authorization determine side effects. Headless Blender authoring does not require UI automation. Discover Blender and its actual version; inspect the existing file before editing, and save a sibling checkpoint. Do not open/control Unreal merely to finish a Blender study.

## Admit evidence and define the read

Read [evidence-contract.md](references/evidence-contract.md) before filling the contract. Inspect the actual original images; an AI-redesigned board is a presentation aid, never pixel-exact evidence. Preserve source IDs, hashes, source regions and original labels. Separate visible facts, author-reported motion, implementation hypotheses and new design choices.

For an existing study library, start with that library's guide and catalog, then pass the catalog explicitly to `from-study`. The S2/NineTails checkout is one supported host and keeps its study guide at `docs/references/vfx/ninetails-layered-study/`; this skill does not assume that host documentation is installed. Load only the selected source board/recipe, not all references by default.

Catalog labels such as `visible_read` are summaries to recheck, not automatic evidence upgrades. Move temporal verbs unsupported by footage into author-reported or proposed behavior. An unresolved warning/impact or trail/launch classification blocks committed engine/event binding, not a clearly labeled unbound visual study.

```text
python <skill>/scripts/vfx_contract.py from-study --catalog <catalog.json> --effect SP-02 --out <project>/contract.json
python <skill>/scripts/vfx_contract.py validate <project>/contract.json --stage study
```

For new references, use `init --name <name> --reference <image> --out <contract.json>` and fill the source observations and feature rows before validation. The initializer creates an incomplete intake, not an approved reconstruction.

Define one player-facing purpose and one primary read, then give each visual feature a stable ID, evidence class, source IDs, phase, priority and exact planned Blender object/node target. Account for distinguishing details, not only generic labels such as “magic ring.” Mark omitted particulars explicitly with a reason. Preserve unknown numeric values as null.

Use the shared layers as responsibilities, **not emitter counts**:

| Layer | Responsibility |
| --- | --- |
| L0 | Gameplay meaning: state, boundary, response opportunity and authoritative event. Keep simulation ownership outside cosmetics. |
| L1 | Primary shape: wall, opening, body silhouette, focal signal or actionable ring. |
| L2 | Directional motion: gather, expand, trail, fall or collapse. |
| L3 | Material/contact: coarse substance, fine detail, grounded residue and seams. |
| L4 | Optional accent: glint, flare, local distortion or light shafts. |

Record whether a view is a matched source camera or a proposed gameplay camera. When no video exists, do not block a useful prototype: choose explicit prototype durations and state that source timing fidelity is unassessed. Do not treat the old 0.1-second notes or 1.1 rotation ratio as measurements.

## Build through the smallest useful passes

Read the relevant family rows in [effect-families.md](references/effect-families.md), then [blender-authoring.md](references/blender-authoring.md) before scene edits.

1. **Primary read and timing:** block L1/L2, reference/playback camera, dimensions and event anchors. Check before-event, gather, event, residue and cleared frames. For loops include start/hold/end and repeated cycles. Do not hide a failed silhouette with glow.
2. **Layer composition:** add material/contact and optional accents; prove intentional attachment versus world-space residue. Keep body/ground proxies separate from the effect. Arrival is authored independently of departure when gravity and state timing differ.
3. **Robustness:** render Standard, actual Lite, no-accents and layer isolation. Check the declared oblique/near/far views, contrasting backgrounds, cancellation and retrigger where applicable. Simulations must be baked or evaluated sequentially from their start.
4. **Delivery:** reopen the final checkpoint, verify feature bindings and dependencies, and capture the same sample set again. Validate requested exports separately; a `.blend` or PNG sequence is not a tested Unreal preset.

Use versioned project directories/checkpoints. Do not overwrite admitted sources or a previous evidence packet. The bundled capture helper refuses an existing output directory.

```text
python <skill>/scripts/vfx_contract.py validate <project>/contract.json --stage prototype
blender --background <project>/effect_v01.blend --python-exit-code 1 --python <skill>/scripts/capture_vfx.py -- --contract <project>/contract.json --out <project>/evidence/v01
python <skill>/scripts/vfx_contract.py verify <project>/contract.json <project>/evidence/v01/manifest.json
```

The helper renders **declared scenes, cameras and frames**, audits named feature objects, and records hashes/settings/visibility. It does not invent effects, automatically implement missing test scenarios, or judge visual quality. Define actual scene variants before capture. `init`/`from-study` do not make a render-ready contract.

## Independent critique and refinement

Read [review.md](references/review.md) before judging a prototype. Dispatch a fresh independent visual critic that did not build the current scene, with admitted references, contract, captured evidence and prior comparison only. The critic must inspect images and temporal evidence; names, logs and hash checks are not visual proof. Use frame sampling to review a sequence when video tools are unavailable, and disclose that continuous playback was not reviewed.

Correct the critic's highest-impact causal defect, save a new checkpoint, and recapture identical roles/frames/settings. If evidence itself is insufficient, repair that first. A targeted correction may touch several coupled nodes; it must not bundle unrelated styling changes.

Default cap: three review rounds per prototype. Stop earlier when required reads, timing, layers and delivery pass. If the same root cause survives a correction, two rounds stall, or improvements trade one required view/phase for another, revisit the contract or report a conditional prototype. Do not claim “best possible” or silently reset the round counter. If independent review cannot run, mark it unreviewed rather than inventing another critic identity.

## Acceptance and handoff

Report separately: reference-study complete, Blender prototype validated, export validated, and engine integration validated. Only claim the levels actually demonstrated.

- Every critical feature has visible evidence at its required phase/view; no hard failure is averaged into an overall score.
- Essential shape, timing and semantic distinction survive Lite/no-accents and declared gameplay views.
- Cancellation, loop termination, residue anchoring and reset are proved for the applicable lifecycle; optional scenes are not mandatory for a still-only study.
- The checkpoint and dependencies reopen; the evidence packet matches their hashes and settings; all requested exports are inspected independently.
- Source motion uncertainty, inferred geometry and proposed semantic colors remain explicit. Blender render time is never reported as Unreal GPU performance.

For the reusable study library and the runnable skill self-test, read [self-test.md](references/self-test.md). These low-detail fixtures exercise the workflow; they are not AAA-quality effect assets or a universal implementation for every reference.
