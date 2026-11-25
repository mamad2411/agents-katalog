---
name: semwright-video-production
description: Use when an agent must author, render, measure, validate, repair, or verify a managed Motion Canvas production through Semwright's semantic motion lifecycle.
---

# Video production

Use the live `driver.motion-canvas.*` catalog. Do not reconstruct command schemas from this Skill.

1. **DISCOVER** the available Motion Canvas capabilities and describe the narrow operations you will use.
2. **INSPECT** the managed project. If a high-level Film binding exists, treat it as the editable authoring source; do not patch the derived model behind its back.
3. **PLAN** substantial motion work with `composition.plan`. Keep narrative labels, temporal constraints, logical subject identity, assets, fonts, cues and output profile explicit.
4. **REVIEW** the returned plan and dependency/budget data. A plan is not authority and cannot widen Broker grants.
5. **APPLY** only the server-issued, fresh plan. Re-inspect on stale project/session/generation/fingerprint instead of replaying.
6. **RENDER** through the existing render job interface. Rendering is a separate compute operation, not a dry-run side effect.
7. **MEASURE** native renderer observations linked to the exact render/source digest. Desired transforms, opacity or text are not measurements.
8. **VALIDATE** required constraints and coverage. UNKNOWN remains non-PASS when a font, pixel contribution, overlap relation, cue or range cannot be proven.
9. **REPAIR** only a fresh deterministic finding with one bounded repair. Preserve the original cumulative budget and re-render afterward.
10. **VERIFY** the resulting artifact, not merely the generated TypeScript. Record frame range, exhaustive/sampled coverage and artifact digests.
11. Use `artifact.handoff` for cross-driver files. Provider artifact tokens are not filesystem paths.
12. For final encoded delivery, use the MLT/video-domain route and decode/inspect the result separately. A successful Motion Canvas render is not final AV verification.

Prefer semantic layout, exact rational time, native text, declared assets and replay-safe rendering. Do not inject JavaScript, shaders, shell commands, URLs, hidden encoders or coordinate-click automation into the authoring payload.

Read [authoring and evidence](references/authoring-and-evidence.md) and [limitations](references/limitations.md) when needed.
