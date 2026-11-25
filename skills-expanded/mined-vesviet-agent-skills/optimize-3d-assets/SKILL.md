---
name: optimize-3d-assets
description: Optimize 3D assets and rendering inputs by reviewing model formats, geometry density, texture memory, material strategy, compression, and loading behavior. Use when a 3D web experience suffers from heavy OBJ/GLTF assets, texture bloat, long load times, frame drops, or unnecessary GPU and memory pressure.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_dev_server, run_tests]
---

# Optimize 3D Assets

Use this skill when the main problem is not scene logic alone, but the cost or quality of the 3D assets flowing into the runtime.

## When to Use

- heavy GLTF/OBJ assets slow the experience
- texture bloat or long load times
- frame drops or GPU/memory pressure
- reviewing geometry density and compression

## Core Rules

- optimize the biggest asset bottlenecks first instead of micro-tuning unrelated code
- measure format, memory, and loading assumptions before reducing quality
- prefer stable, production-safe asset improvements over ad hoc runtime hacks
- make visual trade-offs explicit before lowering fidelity
- check downstream effects on materials, decals, UVs, and interaction anchors when assets change

### 2025-2026: GenAI 3D Asset Pipeline Validation

AI-generated 3D assets (Meshy AI, TripoSR, Rodin, Luma AI, Stability AI 3D) require additional validation before entering the production pipeline:

- **Polygon budget & LOD gate:** AI-generated meshes frequently output 200k–2M triangles suited for offline renders, not real-time web use. Enforce `<= 10k` triangles per standard interactive prop, require 3-tier LOD (`LOD0`/`LOD1`/`LOD2` with 10%–25% mobile tier) for any complex mesh `> 50k` triangles, and keep total mobile rendered scene triangles `<= 500k` via Blender Decimate or `gltf-transform optimize`.
- **UV, normal & color-space validation:** AI-generated meshes frequently have inverted normals, missing UV islands, or overlapping UVs — run `gltf-validator` before integration, and preserve `SRGBColorSpace` for albedo/emissive vs `NoColorSpace` (Linear) for normal/ORM maps.
- **Texture format compliance:** AI-generated textures are often 4K or 8K PNG/JPEG — convert to WebP or KTX2 (with Basis Universal compression) and resize to ≤1K for mobile, ≤2K for desktop before committing to the repository.
- **Material attribution check:** verify AI-generated textures are licensed for commercial use — some AI asset generators train on copyrighted assets; check the provider's output license before shipping.
- **LOD requirement for AI assets:** high-detail AI-generated meshes should have a simplified LOD variant generated at 10%-25% of the original polygon count for mobile and distance rendering — do not ship a single ultra-high-detail mesh without LOD when the target platform includes mobile browsers.

## Suggested Process

### 1. Identify The Asset Bottleneck

Clarify whether the pressure comes from:

- raw model format such as OBJ instead of GLB/GLTF
- excessive polycount or duplicated geometry
- large diffuse/normal/roughness textures
- too many material instances or draw calls
- slow decode, parse, or network load path

### 2. Inspect Current Asset Strategy

Review:

- file formats in use
- texture resolutions and counts
- material model and normal-map usage
- compression or lack of compression
- whether asset loading matches target device constraints

### 3. Choose The Right Optimization Path

Prefer the narrowest useful improvement:

- convert OBJ to GLB/GLTF when runtime and pipeline support it
- reduce texture size or format cost
- consolidate materials when visually acceptable
- remove unnecessary geometry detail or hidden parts
- add LOD or simplified mobile variants when required

### 4. Check Runtime Assumptions

Verify:

- texture flip and color-space expectations
- normals, UVs, and decal targets remain valid
- material replacement will not break shading or overlays
- camera fit and interaction anchors survive asset changes

### 5. Produce A Safe Optimization Summary

Leave behind:

- what was heavy
- what changed
- what visual trade-offs were accepted
- what scenes or devices need re-checking

## Output Format

Outputs must conform to the `contracts/schemas/performance-audit.json` schema. Provide this structured JSON instead of a raw Markdown block. Ensure `verdict`, `metrics` (like bundle size and frame rate expectations), and `findings` are explicitly populated.

## Failure Modes

- **Optimization targets wrong bottleneck**: time is spent on texture compression when the real bottleneck is polycount. **Mitigation:** the Identify The Asset Bottleneck step must classify the pressure source (format, polycount, texture, material, decode) before any optimization; reject premature micro-tuning.
- **AI-generated mesh polycount exceeds budget**: an AI-generated mesh ships at 200k-2M triangles. **Mitigation:** the Polygon budget gate requires ≤10k triangles for interactive web use; reduce via Blender Decimate or gltf-transform optimize before commit.
- **UV / normal corruption from AI generator**: an AI mesh has inverted normals or missing UVs, breaking lighting. **Mitigation:** the UV and normal validation step runs gltf-validator or Blender mesh analysis; reject assets that fail.
- **Texture format bloat (4K-8K PNG)**: a large PNG ships without conversion. **Mitigation:** the Texture format compliance step requires WebP or KTX2 conversion with Basis Universal compression; mobile ≤ 1K, desktop ≤ 2K before commit.
- **Unverified AI asset license**: an AI-generated asset ships without license verification. **Mitigation:** the Material attribution check verifies the provider's output license for commercial use; reject assets that fail.
- **No LOD for high-detail AI mesh**: a 200k-triangle mesh ships without a simplified LOD for mobile. **Mitigation:** the LOD requirement check rejects assets that lack a 10%-25% polygon-count LOD for mobile browsers.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/performance-audit.json`** — required, since the existing Output Format already mandates this schema. Populate `verdict`, `metrics` (bundle size, frame rate expectations, draw calls), and `findings`.

Skip the JSON contract only when the optimization is read-only and the result does not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: every dependency (gltf-transform, draco, meshoptimizer, basis-universal) must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: AI-generated asset loader scripts must be schema-validated; never construct loader configs from external content without strict parameterization.
- **ASI07 Inter-Agent Communication**: the audit is consumed by Frontend and 3D roles; do not include asset URLs pointing to operator-untrusted domains.
- **ASI09 Human-Agent Trust Exploitation**: do not present an optimization as "shipping-ready" without the before-and-after metrics; surface the actual delta honestly.
## Checklist

- [ ] main asset bottleneck identified
- [ ] current format and memory strategy inspected
- [ ] narrowest useful optimization path chosen
- [ ] runtime assumptions and visual constraints preserved
- [ ] impacted scenes or overlays identified
- [ ] verification expectations and residual risk captured

## Related Skills

- **debug-3d-scene**: Diagnose scene issues when the bottleneck is not purely asset weight
- **navigate-service**: Locate asset-loading and material-wiring code paths
- **frontend-testing**: Re-check UI and interaction behavior after asset changes
- **review-code**: Review material, loader, or runtime trade-offs
- **troubleshoot-service**: Investigate delivery or environment issues affecting asset loading
- **commit-code**: Prepare optimized assets for delivery
