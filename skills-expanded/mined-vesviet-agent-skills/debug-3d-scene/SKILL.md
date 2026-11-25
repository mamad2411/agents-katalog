---
name: debug-3d-scene
description: Debug 3D scene behavior by tracing scene graph structure, transforms, raycasting, decals, materials, camera logic, render loops, and WebGL lifecycle issues. Use when a Three.js, React Three Fiber, WebGL, or WebGPU scene has rendering bugs, interaction bugs, clipping problems, context instability, or suspicious visual math.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_dev_server, run_tests]
---

# Debug 3D Scene

Use this skill when a 3D experience behaves incorrectly and the fix depends on understanding scene state, transforms, asset wiring, or render lifecycle rather than only surface UI symptoms.

## When to Use

- a Three.js / R3F / WebGL / WebGPU scene has rendering bugs
- interaction or raycasting bugs in a 3D scene
- clipping, context loss, or camera math problems
- suspicious material/transform/render-loop behavior

## Core Rules

- capture the exact 3D symptom before changing code
- verify coordinate systems, transforms, and scene hierarchy instead of trusting visual intuition
- isolate whether the bug lives in assets, scene graph, interaction math, materials, or lifecycle
- treat shared materials, shaders, merged geometry, and reused interaction hooks as blast-radius multipliers
- verify the original issue and nearby scene regressions before closing the fix
- Utilize Chrome DevTools Shader Editor tab to inspect **WebGPU** pipelines and WGSL/TSL shader compilation errors natively.
- Use **Spector.js** in development strictly for **WebGL2** pipelines (it does not capture WebGPU) to replay draw calls frame-by-frame, disabling it in production.
- Leverage R3F DevTools to analyze scene graphs, geometry vertex counts, material types, and render call counts.
- Inspect common AI-3D-slop root causes early: `new Vector3()`/`setState()` inside `useFrame`, `SRGBColorSpace` applied to normal/ORM maps, sloppy `near`/`far` Z-fighting, shadow acne bias, and `material.dispose()` leaking attached textures.

## Suggested Process

### 1. Define The 3D Failure

Clarify:

- what the user sees versus what is expected
- whether the issue is visual, interactive, performance-related, or lifecycle-related
- which scene, model, decal, material, camera path, or device profile is affected
- what behavior must stay stable while fixing it

### 2. Classify The Failure Layer

Decide where the failure most likely lives:

- scene graph or parent-child transform logic
- mesh geometry, normals, UVs, or winding
- material, texture, shader, or decal projection logic
- camera, controls, frustum, or clipping setup
- pointer interaction, raycasting, drag logic, or DOM-to-canvas bridge
- loading lifecycle, async race, disposal, or WebGL context behavior

### 3. Trace The Real 3D State

Inspect only what matters:

- object hierarchy and local vs world transforms
- scale, rotation, quaternion, and matrix conversion paths
- material reuse, texture assignment, and shader assumptions
- render loop subscriptions and camera/control updates
- asset format differences such as OBJ vs GLTF/GLB

### 4. Check Shared-Risk Areas

Look for common 3D regression sources:

- reused materials or shaders
- merged geometry or portal-based decal projection
- texture flip, color space, or normal map conventions
- mirrored geometry, negative scale, or winding order
- event listener leaks, RAF duplication, or missing disposal

### 5. Form And Test A Narrow Hypothesis

Test one likely cause at a time:

- wrong local/world-space conversion
- incorrect mesh target for decal or raycast
- stale texture/material instance
- asset orientation or scale mismatch
- missed cleanup or duplicate render/update path

### 6. Verify The Fix

Re-check:

- original bug path
- nearby models or scenes using the same logic
- mobile or low-end GPU behavior if relevant
- memory or context stability if lifecycle changed

### 2026: Advanced 3D Debugging and Diagnostics Tools

- **WebGPU Debugging**: Use the native Chrome DevTools Shader Editor tab (available in Chrome 124+). This enables inspection of GPU pipelines, binding groups, and shader compilation errors natively without the need for external tooling.
- **Spector.js for WebGL Diagnostics**: For WebGL-based pipelines, inject Spector.js in development builds. It records and replays draw calls frame-by-frame to identify state and binding issues. Ensure it is entirely disabled in production builds due to the significant performance overhead.
- **React Three Fiber (R3F) DevTools**: Integrate the `@r3f/dev-tools` panel. This provides a real-time visual inspection of the scene graph, geometry vertex counts, material types, active shaders, and render call counts directly in the browser interface.

## Output Format

Outputs must summarize the root cause and mitigation, and if the debug involves performance/memory bottlenecks, output must be accompanied by a `contracts/schemas/performance-audit.json` payload.

```markdown
# <Problem> - 3D Scene Debug Brief

## Symptom
- Expected behavior:
- Actual behavior:
- Affected scene / model / interaction:

## Failure Layer
- Suspected layer:
- Preserved behavior:

## Evidence
- Relevant files or systems:
- Transform / material / interaction observations:
- Shared-risk areas:

## Hypothesis
- Most likely root cause:
- Why:

## Verification
- Original issue re-checked:
- Nearby regressions re-checked:
- Residual risk:
```

## Failure Modes

- **Symptom misattributed to render layer**: a visual bug is treated as a render problem when the cause is data, layout, or asset format. **Mitigation:** always classify the failure layer (scene graph, geometry, materials, camera, interaction, lifecycle) before changing code; the Suggested Process step 2 enforces this.
- **Shared material or shader edited in isolation**: an edit to a shared material causes regressions in adjacent models. **Mitigation:** run the Shared-Risk Areas check (step 4) and verify neighboring models that reuse the same material; the blast-radius warning is in Core Rules.
- **GPU memory leak from missing dispose**: a debug fix that adds geometry/material/texture without cleanup leaks GPU memory. **Mitigation:** verify disposal paths in the lifecycle review (step 6); reject changes that add resources without matching `dispose()` calls.
- **WebGL context loss misattributed to a render bug**: a context loss is treated as a scene issue when the cause is the platform, not the scene. **Mitigation:** check `WEBGL_lose_context` events and platform limits; treat context loss as platform-side until proven otherwise.
- **R3F DevTools / Spector.js shipped in production**: a debug build accidentally ships with the dev hooks. **Mitigation:** verify the production build excludes Spector.js and R3F DevTools; the Core Rules for these tools call this out explicitly.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/performance-audit.json`** when the debug surfaces a performance or memory bottleneck. The `verdict`, `metrics` (draw call count, GPU memory), and `findings` fields are required.
- For human-readable handoff, use the 3D Scene Debug Brief template in the existing Output Format block.

Skip structured emission when the debug only produces a single fix that does not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI05 RCE Guard**: do not execute dynamic shader code or WebGPU shader strings sourced from external content without strict schema validation; AI-generated shaders must compile in a sandboxed build before production.
- **ASI07 Inter-Agent Communication**: the debug brief is consumed by Frontend and 3D roles; do not include any 3D model paths that point outside the operator's own asset domain.
- **ASI09 Human-Agent Trust Exploitation**: do not present a debug summary as "root cause confirmed" without the actual scene-state evidence; surface unverified hypotheses as `[INFERENCE]`.
## Checklist

- [ ] exact 3D symptom captured
- [ ] likely failure layer classified
- [ ] real scene state inspected
- [ ] shared-risk areas checked
- [ ] narrow hypothesis tested
- [ ] original issue and nearby regressions re-checked
- [ ] Native WebGPU pipelines and shaders are inspected via Chrome DevTools Shader Editor when using WebGPU.
- [ ] Spector.js is integrated for dev-mode WebGL frame capture and disabled for production.
- [ ] R3F DevTools is utilized to monitor scene graph, vertex count, and render calls.

## Related Skills

- **optimize-3d-assets**: Improve source assets when geometry or texture quality is the real problem
- **troubleshoot-service**: Debug non-graphics runtime or integration issues around the scene
- **frontend-testing**: Add regression checks around interaction-sensitive fixes
- **review-code**: Review risky transform, shader, or lifecycle changes
- **navigate-service**: Map the 3D code path before debugging
