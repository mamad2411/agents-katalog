---
name: develop-obj-feature
description: Develop features for the OBJ 3D Product Configurator — an Astro + React Three Fiber app with Three.js engine, Redux/Zustand state, and Prisma backend. Use when modifying 3D scenes, decals, UI panels, or design persistence.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_dev_server, run_tests]
---

# Develop OBJ Feature

Use this skill when building or modifying features in the OBJ 3D Product Configurator.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/obj-configurator/rules/obj-project-rules.md`
- GLB format only for 3D models — no OBJ/MTL in new work
- Sprite-based preview during drag — never recalculate DecalGeometry per frame
- Memoize React components to prevent re-renders during 3D interaction
- Dispose Three.js resources on unmount (geometries, materials, textures)
- Debounce continuous transforms to 100ms before dispatching to Redux/Zustand

## Suggested Process

### 1. Identify layer — 3D engine, UI panel, state slice, Prisma schema, or Astro page
### 2. Read existing code in `src/design-hub/` for the relevant subsystem
### 3. Implement following engine rules and performance constraints
### 4. Test at 60fps — profile with Chrome DevTools if needed
### 5. Run `npm run check` before commit

## Failure Modes

- **Format regression to OBJ/MTL**: a 3D model is added in OBJ/MTL instead of the mandated GLB. **Mitigation:** the Core Rules forbid OBJ/MTL in new work; reject the change at code review.
- **DecalGeometry recomputed per frame**: a drag operation recalculates the decal geometry every frame. **Mitigation:** the Core Rules require sprite-based preview during drag; reject the change and refactor to a sprite.
- **Missing dispose on unmount**: a 3D component leaves geometries, materials, or textures in memory. **Mitigation:** the Core Rules require dispose on unmount; verify every effect that allocates 3D resources has a matching cleanup.
- **Continuous transform flood**: a drag dispatches to Redux/Zustand on every frame. **Mitigation:** the Core Rules require 100ms debounce; reject un-debounced transforms.
- **DPR uncapped on mobile**: a 3D canvas runs at native DPR on mobile, tanking performance. **Mitigation:** the Core Rules require DPR ≤ 2 on mobile; reject the change.

## Output Contracts

When this skill produces a structured handoff, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output proving the build and test pipeline passes.
- For the 3D subsystem changes, also emit **`contracts/schemas/performance-audit.json`** when frame rate or memory budget is touched.

Skip structured emission for trivial edits that do not cross a role boundary.
## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Prisma schema changes must be reviewed for row-level access; the OBJ configurator stores user designs and must not expose other users' rows.
- **ASI04 Supply Chain**: every Three.js, R3F, and Astro dependency must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: do not construct GLB/MTL loader configs from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the implementation result is consumed by 3D Engineer, Frontend, and Backend roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a 3D feature as "performance-validated" without the actual FPS evidence; surface the unverified checks.
## Checklist

- [ ] GLB format used for all new 3D models
- [ ] Three.js resources properly disposed on unmount
- [ ] React components memoized where appropriate
- [ ] Continuous transforms debounced before store dispatch
- [ ] Sprite-based preview used during drag operations
- [ ] Canvas DPR capped at 2 on mobile
- [ ] Prisma schema changes include migration
- [ ] `npm run check` passes

## Related Skills

- **debug-3d-scene**: debug Three.js rendering and material issues
- **optimize-3d-assets**: optimize models and textures for performance
- **integrate-r3f-three-legacy**: bridge R3F and legacy Three.js code
- **review-code**: review against project conventions
- **commit-code**: commit with proper conventions
