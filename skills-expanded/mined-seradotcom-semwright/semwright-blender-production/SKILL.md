---
name: semwright-blender-production
description: Author, inspect, measure and persist managed Blender assets through Semwright's typed native Composition profile, with explicit scope and evidence limitations.
---

# Blender production

This package is a development draft, not a production-readiness declaration. Discover the installed live catalog and strict argument schemas before use. Missing commands are a stop condition, not permission to substitute a script.

## Authoring loop

Inspect native source state first. Express bounded native entities, geometry, materials, bones, relationships and animation as `BlenderAuthoringSpec` data. Authoring aliases are not Project Graph logical IDs. Do not adopt an existing object by display name.

Call `driver.blender.composition.plan` with a typed intent, review its operations, dependencies and non-atomic write scope, and call `driver.blender.composition.apply` using the returned plan reference in the same authenticated session. A plan is not a policy grant. Do not supply an owner or principal, edit the plan, replay it, or silently replace a failed attempt with a new one.

Use inspect for bounded source-only readback. For exhaustive traversal of managed objects, bones, actions, curves, keyframes or selected properties, use `composition.inspect.page`: its provider-owned cursor is single-use and bound to authenticated owner, native session, domain and source fingerprint. On cursor replay, another session or any intervening drift, restart enumeration from a fresh first page; never interpret an omitted later page as absence. `composition.measure` explicitly distinguishes source and evaluated state: evaluation has a cost and requires its own mutation-capable authorization. For animation/deformation, pass an explicit sampled `{frame, rate}` where `rate` is the project `media-time::Rate`; the driver verifies that rate against Blender, evaluates that frame, reports exact rational sample time and restores the prior frame/subframe. For managed meshes, inspect typed custom attributes, `smooth_polygons`, `normal_digest` and `normal_method`; a source normal digest and an evaluated normal digest are different evidence scopes. Selected-frame evaluation does not establish all-time correctness. Bounds intersection is not mesh collision evidence. Request human/visual review for aesthetics; no automatic beauty verdict exists.

Incremental `transform` intents require the managed island/entity and exact observed fingerprint. On drift, ambiguity, shared-resource surprises or linked/read-only data, stop and reconcile. The only repair surface is `composition.repair.plan` → `composition.repair.apply` for a previously completed **transform** plan: it re-observes the exact current fingerprint, inherits the parent's PlanVault budget, and restores that already-declared transform only after an explicit repair request. It does not regenerate a created asset, copy shared data, remesh, delete parts, change materials/rigs, bake, or broaden authority. Root and repair plan refs are not interchangeable.

For a technical product-scene preview, reuse the existing public Blender capabilities through Broker/Driver Host: choose a revision-bound camera with `semantic.relation.set`, create or select a bounded World through semantic datablock/property surfaces when needed, apply bounded `render.settings`, then call `render` to a workspace PNG. A preview is evidence for visual review only; it is not a Composition PASS condition and must not be used to auto-score aesthetics.

## Persistence and export

TextureAsset v1 is external-reference-only: paths stay inside the granted workspace, bytes are hash-verified, and E does not silently pack or copy them. `composition.persist` creates a new `.blend` artifact in the owner-granted workspace; it is not overwrite or rollback. Native library serialization may expand indirect dependencies. Inspect the closure and preserve returned digest and inventory. Reopen in a fresh disposable driver process and compare actual fields; saving or returning an acknowledgment is not persistence verification.

Reuse `driver.blender.export.glb`. Review effective membership, parents, armatures, actions, modifiers and material/texture dependencies before export. Instancers, external/linked dependencies and unsupported closure must fail rather than silently export the whole scene. Keep the existing fixed exporter and its no-overwrite path.

Blender never writes a Godot project. Transfer artifacts through the public artifact route and D's public Godot API, recording distinct export/handoff/import/verification activities. No `send_to_godot` shortcut or hidden `.tscn` write.

`composition.validate` and `composition.verify` use F's trusted `EvidenceAdapter`/evaluator over native post-state; request echoes or client-provided evidence cannot mint PASS. C Project Graph admission remains a separate host-owned step: E can form a typed candidate only after host-resolved logical identities, and C's registered `ReceiptAdapter` decides admission. Read [typed authoring](references/typed-authoring.md) for the implemented boundary.
