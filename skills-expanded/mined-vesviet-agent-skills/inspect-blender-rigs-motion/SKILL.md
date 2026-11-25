---
name: inspect-blender-rigs-motion
description: Diagnose and repair Blender armatures, bone roll alignment, animation retargeting hierarchies, and root motion trajectories before game engine import. Use when validating skeletal meshes, fixing bone twists, or extracting root motion for Godot, Unity, or Unreal.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Inspect Blender Rigs Motion

Validate, repair, and normalize skeletal armatures, skinning weights, bone rolls, and root motion tracks in Blender via headless Python (`bpy`) scripts before importing into game engines.

## Core Rules

- **Applied Transforms Invariant**: Both the armature object and all skinned mesh objects must have unit scale `(1.0, 1.0, 1.0)`, zero rotation `(0, 0, 0)`, and aligned origins at the world origin `(0, 0, 0)` prior to export.
- **Consistent Bone Roll Alignment**: Enforce uniform primary and secondary bone axes across limb chains so quaternion interpolation and IK solvers do not twist joints during animation blending.
- **Root Motion Separation**: Dedicate a ground-projected `Root` bone at `(0, 0, 0)` parented above the `Hips`/`Pelvis` bone. Extract planar locomotion deltas onto the `Root` bone while keeping in-place vertical bounce on the pelvis.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when completing rig diagnostics and motion pipeline fixes.

## Suggested Process

### 1. Headless Armature & Mesh Transform Audit
Execute a headless Blender inspection script (`blender --background asset.blend --python inspect_rig.py`) to verify:
- Unapplied object scales or negative scales that invert surface normals.
- Maximum vertex influence limits ($\le 4$ bone weights per vertex for real-time GPU skinning) and normalized weight sums ($\sum w_i = 1.0$).

### 2. Hierarchy & Bone Roll Normalization
Standardize the deform skeleton hierarchy:
- Separate deform bones (`DEF-*`) from control/IK rig bones (`CTRL-*`, `MCH-*`), exporting only deform bones to the target engine.
- Recalculate bone rolls in Edit Mode (`bpy.ops.armature.calculate_roll`) so limb hinge axes align cleanly with local $X$ or $Z$ axes.

### 3. Animation Retargeting Validation
Map source motion-capture or library animations onto the target humanoid skeleton:
- Verify rest pose (T-pose or A-pose) quaternion parity before baking action keyframes.
- Bake constrained IK/FK channels to explicit per-frame FK bone transforms with clean euler discontinuity filtering.

### 4. Root Motion Extraction & Export Verification
Project hip translation trajectories onto the ground plane (`Root` bone) for locomotion clips, zero out lateral drift on idle/in-place clips, and export deterministic `.glb` / `.fbx` binaries with tangents enabled.

## Output Contracts

When completing Blender rig and motion inspection, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Armature and skinned meshes have applied transforms with `(1.0, 1.0, 1.0)` scale at world origin
- [ ] Vertex skin weights are normalized and capped at 4 bone influences per vertex
- [ ] Deform bone hierarchy is cleanly isolated from IK/control rig helper bones
- [ ] Bone roll axes are consistent across symmetric left/right limb chains
- [ ] Root bone tracks planar locomotion cleanly without pelvis double-transform drift
- [ ] Exported glTF/FBX passes headless engine import without scale or quaternion warnings

## Failure Modes

- **Unapplied transform export**: the armature or mesh ships with non-unit or negative scale, arriving in-engine $100\times$ oversized or with inverted normals. Mitigation: run the headless audit enforcing unit scale `(1.0, 1.0, 1.0)`, zero rotation, and origin alignment before any export.
- **Bone roll twist**: inconsistent primary/secondary axes across limb chains make quaternions flip and joints twist during animation blending. Mitigation: recalculate rolls in Edit Mode (`bpy.ops.armature.calculate_roll`) aligning hinge axes to local $X$/$Z$, symmetric across left/right chains.
- **Control rig exported**: IK/CTRL/MCH helper bones reach the engine, breaking skeleton mapping and bloating the runtime hierarchy. Mitigation: isolate `DEF-*` deform bones and export only those to the target engine.
- **Root/pelvis double transform**: locomotion deltas stay on the hips while a root bone also moves, so the character travels twice as far. Mitigation: dedicate a ground-projected `Root` bone above `Hips`, put planar deltas on `Root`, and keep in-place vertical bounce on the pelvis.
- **Weight limit overrun**: vertices exceed 4 bone influences, tripping GPU skinning limits or falling back to CPU skinning. Mitigation: cap influences at 4 and renormalize weight sums ($\sum w_i = 1.0$) during the audit.
- **Rest pose mismatch**: retargeting bakes onto a skeleton whose T-pose/A-pose differs from the source, mangling limbs. Mitigation: verify rest-pose quaternion parity before baking action keyframes.
- **Euler discontinuity artifacts**: baked curves contain euler flips that read as $360^\circ$ spin frames in-engine. Mitigation: apply euler discontinuity filtering when baking constrained IK/FK channels to FK transforms.

## Security Guardrails (OWASP ASI)

- **ASI05 RCE Guard**: untrusted `.blend` files can embed Python drivers and auto-run scripts. Mitigation: open them headless with script auto-execution disabled (`blender --background` with autoexec off); never enable embedded driver evaluation on downloaded assets.
- **ASI04 Supply Chain**: mocap libraries, rigged character packs, and Blender export add-ons are external inputs. Mitigation: verify provenance and license before ingestion and pin add-on versions used by the pipeline.
- **ASI07 Inter-Agent Communication**: rig audit results and skeleton mappings are consumed by engine-integration and gameplay roles. Mitigation: emit the schema-valid `implementation-result.json` contract with bone mapping metadata so importers validate against the declared skeleton.
- **ASI09 Human-Agent Trust Exploitation**: do not claim a rig is engine-clean without evidence. Mitigation: report the actual headless engine import result, including any scale or quaternion warnings that remain.

## Related Skills

- **integrate-game-engine**: deterministic 3D glTF/FBX importer configurations and skeleton mapping
- **develop-gameplay-systems**: root motion integration with character controllers and state machines
