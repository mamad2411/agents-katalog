---
name: integrate-r3f-three-legacy
description: Integrate or migrate between React Three Fiber and legacy imperative Three.js code by controlling scene ownership, render loops, loaders, interaction state, and cleanup boundaries. Use when a 3D web app mixes R3F with older Three.js modules, global bridge state, or imperative scene utilities and needs safe coexistence or staged migration.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_dev_server, run_tests]
---

# Integrate R3F Three Legacy

Use this skill when a 3D frontend mixes React Three Fiber with older imperative Three.js code and the real work is defining safe boundaries between the two systems rather than only fixing one component in isolation.

## When to Use

- a 3D app mixes R3F with imperative Three.js
- migrating legacy Three.js into R3F safely
- managing global bridge state between paradigms
- controlling scene ownership and cleanup boundaries

## Core Rules

- define one clear owner for render loop, scene mutation, and disposal in each code path
- do not let legacy globals and React state mutate the same 3D objects without an explicit contract
- treat loaders, materials, controls, and decal logic as shared-risk areas when bridging old and new systems
- preserve current interaction behavior while reducing architectural overlap
- verify migration or bridge changes against nearby flows, not only the target scene

### 2025-2026: AI-Generated 3D Scene Code Review

When AI tools generate R3F components or Three.js bridge code, apply these additional checks:

- **Context ownership & R3F v9 alignment:** verify that AI-generated R3F components use `useThree()` context correctly (`state.renderer` in R3F v9, not legacy `state.gl`) and do not create a second `<Canvas>` renderer that conflicts with the active scene context.
- **Disposal and cleanup correctness:** AI-generated 3D components frequently omit `useEffect` cleanup or only call `material.dispose()` while leaking textures — verify geometries, materials, **all attached texture maps**, and render targets are disposed on unmount.
- **Animation frame loop & zero-allocation ownership:** verify `useFrame` callbacks do not accumulate subscriptions across renders, never call React `setState()`, and never allocate `new THREE.Vector3()` / `.clone()` per frame.
- **Generative 3D asset pipeline gate:** for AI-generated 3D meshes (Meshy AI, Tripo, Rodin), validate polygon density (`<= 10k` triangles per standard interactive prop; `> 50k` requires 3-tier LOD), UV correctness, `NoColorSpace` on normal/ORM maps, and material attribution before integrating into the R3F/Three.js scene.

## Suggested Process

### 1. Map The Split Architecture

Identify:

- which files own the R3F canvas, scene, controls, and event flow
- which files still mutate Three.js objects imperatively
- what global stores, callbacks, or bridge objects connect UI and 3D state
- which behaviors must remain stable during the change

### 2. Classify The Boundary Problem

Decide what kind of mixed-system issue exists:

- duplicate scene ownership
- duplicate render/update loops
- state split across Redux, Zustand, globals, and object instances
- legacy utilities mutating meshes that R3F also manages
- loader/material/decal logic duplicated in both systems

### 3. Define Safe Ownership

For each concern, assign one owner:

- scene and camera ownership
- controls ownership
- model loading ownership
- material and texture mutation ownership
- interaction and raycast ownership
- cleanup and disposal ownership

### 4. Choose The Bridge Strategy

Use the smallest safe approach:

- **coexistence** when legacy code must remain temporarily but boundaries can be tightened
- **adapter layer** when legacy modules should be wrapped behind React-safe APIs
- **staged migration** when imperative scene logic should move gradually into hooks or components

### 5. Check High-Risk Shared Paths

Review:

- texture and material replacement logic
- decals, text rendering, and merged geometry helpers
- loaders that behave differently for OBJ versus GLTF/GLB
- event listeners, drag/drop handlers, and control enable/disable logic
- teardown for geometries, materials, textures, listeners, and cached assets

### 6. Verify Stability

Re-check:

- original bug or migration target
- adjacent tools using the same bridge state
- product switching, undo/redo, share/reload, or restore flows
- memory growth and duplicate listener/render-loop risk

## Output Format

```markdown
# <Change> - R3F Legacy Integration Brief

## Architecture Split
- R3F-owned areas:
- Legacy-owned areas:
- Shared bridge state:
- Preserved behavior:

## Boundary Risks
- Duplicate ownership:
- Shared mutable objects:
- Lifecycle or cleanup risks:
- Asset or material pipeline overlap:

## Integration Strategy
- Chosen approach:
- Why this approach is safer:
- What remains legacy for now:

## Verification
- Original issue or migration target checked:
- Adjacent flows re-checked:
- Memory / listener / render-loop checks:
- Residual risk:
```

## Failure Modes

- **Duplicate scene ownership**: R3F and legacy Three.js both try to own the same scene, causing double-render or material double-mutation. **Mitigation:** the Map The Split Architecture step must declare one owner per concern before any code change; reject integrations that leave ownership ambiguous.
- **Duplicate render loop**: both R3F and the legacy code register a render/update loop, causing frame duplication. **Mitigation:** the Define Safe Ownership step assigns loop ownership explicitly; verify only one `useFrame` chain is active per concern.
- **State split across React, Redux, Zustand, and globals**: shared state mutates from multiple owners, producing inconsistent renders. **Mitigation:** define a single source of truth for the bridge state; the Choose The Bridge Strategy step is the gate.
- **AI-generated Canvas wrapper creates a second renderer**: an AI tool wraps content in its own `<Canvas>` instead of reusing the existing one. **Mitigation:** the AI-Generated 3D Scene Code Review check explicitly tests for this; reject AI components that do not use the existing `useThree()` context.
- **Disposal missing in AI-generated components**: AI-generated 3D components omit `useEffect` cleanup for geometry, material, and texture. **Mitigation:** the Disposal and cleanup correctness check rejects components that do not dispose every owned resource; verify with a memory profile after merge.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/api-contract-spec.json`** when the integration introduces a new public API or props surface that other roles will consume.
- For human-readable handoff, use the R3F Legacy Integration Brief template in the existing Output Format block.

Skip structured emission for trivial wrappers that do not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: AI-generated 3D components must be schema-validated against the project's 3D component manifest; treat AI generators (v0, Copilot, Lovable-style) as untrusted sources.
- **ASI05 RCE Guard**: AI-generated 3D assets from external providers (Meshy AI, TripoSR, Rodin) must pass the Polygon budget gate, UV / normal validation, and material attribution check before being loaded; never load unvalidated AI meshes at runtime.
- **ASI07 Inter-Agent Communication**: the integration brief is consumed by Frontend and 3D roles; do not include asset URLs that point to operator-untrusted domains.
## Checklist

- [ ] R3F and legacy ownership boundaries mapped
- [ ] duplicate ownership or mutation paths identified
- [ ] bridge strategy chosen explicitly
- [ ] shared-risk paths checked
- [ ] cleanup responsibility verified
- [ ] original path and nearby regressions re-checked

## Related Skills

- **debug-3d-scene**: Trace transform, decal, lifecycle, and interaction bugs inside mixed 3D systems
- **optimize-3d-assets**: Reduce asset and texture cost when migration work exposes pipeline inefficiencies
- **navigate-service**: Map the 3D codebase before choosing ownership boundaries
- **frontend-testing**: Add regression coverage around bridge-sensitive interactions
- **review-code**: Review risky lifecycle, ownership, and cleanup changes
