---
name: forgeax-engine-navigation
description: >-
  ForgeAX bounded graph/grid and static NavMesh navigation. Use when baking ground
  clearance, projecting routes, avoiding nearby characters, or following paths through physics.
---

# forgeax-engine-navigation

| Need | Entry |
|:--|:--|
| Authored network or weighted tile grid | `createNavigationGraph` / `createNavigationGrid`; query `findPath` with an expansion budget |
| Static finite-size ground navigation | Build selected indexed Mesh/world placement through `@forgeax/engine/import/navigation-bake`; return the POD as an ordinary Pack output |
| Fixed world-space surface query | Load `navigation-mesh`, pass `assets.read(handle)` to `createNavigationMesh`, then `project` / `ground` / `findPath` with explicit limits; this copied query remains fixed |
| Physical character | Install `physics3d` and `navigationCharacterPlugin(handle)` using the managed asset from `world.assets`; release the caller reference after installation; author NavigationCharacter + kinematic capsule; assign `setNavigationTarget` |
| Local point following | `NavigationAgent`, `navigationPlugin`, `setNavigationPath`; local Transform coordinates and speed |
| Bounded nearby-agent intent | `solveNavigationAvoidance`; consume actual velocity and inspect saturation; optional candidate admission must remain bounded |
| Runtime navigation edits | `assets.update` / `replace` revises polygon/settings content; actual queries and motor steps adopt once per changed active version; old routes cancel before motion even when sourceDigest stays unchanged |
| Pause / cancel / replacement | Idle/following toggles; empty setNavigationPath; `setNavigationMesh(world, handle).unwrap()` followed by explicit retarget |

A route supplies movement intent. `navigationPlugin` point following writes Transform directly and performs no collision resolution. For a solid actor, use the physical-character entry and size its collider and baked clearance from the actor's complete footprint, including scale and turning. Custom grid queries must enforce the same body clearance; a free centre cell does not prove the body fits. Geometry edits require updated collision geometry and navigation content through their owners; updating a rendered mesh alone updates neither.

Use the [Navigation contract](../../packages/navigation/README.md) for capsule scale,
KCC offset, fixed ordering, asset freshness and limits. Observe actual displacement
and blocked state; a congested local solver is not a traffic scheduler. Physical
controllers are excluded from the point follower. Invalid/unreachable/budget results
never prove arrival. Rebuild a faulted World through its owning App recovery route.

Run package tests and the contract's geometry, Catalog, real KCC, browser/Worker and
performance recipes. For unexplained visible output, capture the real frame through
RHI Debug before editing shaders/materials.
