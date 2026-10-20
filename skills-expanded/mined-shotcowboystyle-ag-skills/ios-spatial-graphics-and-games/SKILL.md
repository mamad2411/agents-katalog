---
name: ios-spatial-graphics-and-games
description: Route, implement, or review iOS and visionOS spatial, AR, 2D game, 3D scene, custom Metal, and Game Center features. Use when a feature uses camera/world tracking, RealityKit entities, RealityView or ImmersiveSpace, SpriteKit, GameplayKit, Metal, controllers, or GameKit multiplayer and needs measured performance and physical-device proof.
allowed-tools: Read, Grep, Glob
---

# iOS Spatial, Graphics, and Games

## Overview

Use this skill to choose the smallest Apple graphics or game layer that meets the product outcome, while keeping device/session state, domain or simulation state, rendering, input, networking, accessibility, and proof separate.

`device/session availability -> domain or simulation state -> scene/renderer -> input/network event -> review/persistence`

## Read before acting

- Inspect the actual Xcode targets, platform/device family, deployment target, scene roles, camera usage description, capabilities, entitlements, asset formats, controller/input routes, persistence, Game Center configuration, and existing renderer/game loop.
- Read the [knowledge-base map](../ios-knowledge-base/references/README.md), [spatial graphics and games route](../ios-knowledge-base/references/40-framework-routes/06-spatial-graphics-and-games.md), [RealityKit/ARKit/spatial deep dive](../ios-knowledge-base/references/42-framework-deep-dives/04-realitykit-arkit-and-spatial.md), [Metal/SpriteKit/game deep dive](../ios-knowledge-base/references/42-framework-deep-dives/05-metal-spritekit-and-game-routes.md), and [spatial/graphics/game recipes](../ios-knowledge-base/references/70-code-recipes/18-spatial-graphics-and-game-recipes.md).
- For proof levels, read the [build/device/release checklist](../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md) and [accessibility checklist](../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md). Refresh the exact official Apple pages in the Sources section before relying on availability, scene roles, device support, input behavior, or Game Center rules.

## Route workflow

1. State the user outcome: 2D game, interactive 3D object, camera/world-tracked placement, visionOS window/volume, immersive space, custom shader/compute, or Game Center session.
2. Choose the highest-level route that meets a measured need: SpriteKit for 2D scenes/actions/physics; GameplayKit for state machines, entities/components, pathfinding, and deterministic game algorithms; RealityKit for interactive 3D/spatial entities; ARKit for supported camera/world understanding; SwiftUI plus `RealityView`/`SpriteView`/Metal integration for native shells; Metal only for direct GPU control or a measured rendering/compute requirement.
3. Record target configuration: platform, device family, scene role, camera/motion/input support, usage descriptions, capabilities/entitlements, asset/model formats, Game Center/account/server requirements, and non-spatial fallback. Mark availability as `to-verify` until the target SDK and hardware are checked.
4. Model separate state machines. For AR: idle, permission explanation, unsupported, initializing, running-normal/limited, interrupted, relocalizing, paused, stopped. For games: unauthenticated, authenticating, restricted/ready, matchmaking, connecting, playing, disconnected, ended. For rendering: loading, ready, frame work, resource failure, background, teardown.
5. Keep product state or simulation state authoritative. Build or rebuild `Entity`/component graphs and `SKNode` trees from stable app-owned IDs, semantic roles, transforms, and serialized game state; do not make generated scene hierarchies the only durable record.
6. Bound per-frame work. Avoid asset loading, pipeline compilation, large allocations, unbounded inference, or blocking I/O in the render/update loop. Define frame-drop, pause, interruption, background, low-power, thermal, memory-pressure, and slow-device behavior.
7. Make input and accessibility plural: touch, controller, keyboard/trackpad, system gestures, voice or alternative controls as appropriate; semantic labels, readable summaries, reduced motion, captions, contrast, non-color feedback, and a non-AR/non-spatial route for core actions.
8. Verify in layers: compile the real target, run deterministic scene/game fixtures, test state transitions and asset failures, then use the oldest supported and target physical devices. Record OS build, device, scene/lighting/environment, asset set, frame time, dropped frames, memory, GPU/CPU use, battery, thermal state, and input/accessibility observations.

## Fast path

Select the renderer and one frame-budgeted vertical slice with a capability gate and a 2D or phone fallback. Measure the update, render, input, and resource path on the target device class before adding assets, networking, multiplayer, or a second scene.

## Framework boundaries

### ARKit, RealityKit, and visionOS

- ARKit coordinates camera/motion/world understanding for supported configurations. `ARSession.run` is asynchronous; `pause()` stops processing but does not make a prior pose or placement permanently true. Treat tracking as normal, limited, interrupted, relocalizing, or unavailable.
- RealityKit owns high-level entities, components, systems, animation, physics, and spatial content. Keep a scene adapter between app-owned domain events and the entity graph; bound updates and do not mutate scene content from arbitrary view callbacks.
- SwiftUI windows and controls remain the native shell. Use `RealityView` for supported 3D content and `ImmersiveSpace` only when the outcome needs content outside a bounded window. Make immersive entry/exit asynchronous and observable; provide loading, error, dismissal, safety, and non-immersive routes.
- Camera frames, world maps, room/scene understanding, hand/eye/person observations, and spatial layouts can reveal private spaces and routines. Minimize capture and retention, redact logs, explain data movement, and provide deletion. A plane, mesh, anchor, or pose is framework data with uncertainty, not a measurement, identity, safety guarantee, or construction proof.

### SpriteKit, GameplayKit, Metal, and GameKit

- SpriteKit is the high-level 2D scene/action/physics route; host it in a SwiftUI shell when menus, settings, purchases, accessibility, or system navigation need native controls.
- GameplayKit algorithms should be testable without a renderer. Use deterministic fixtures or seeded randomness for state machines, pathfinding, entities/components, and reproducible bug reports.
- Metal exposes devices, command queues, buffers/textures, shaders, pipelines, and render/compute passes. Use it only for a measurable requirement, keep resources on the same `MTLDevice`, define synchronization/ownership, and profile before optimizing.
- GameKit authentication, Game Center restrictions, matchmaking, `GKMatch` transport, player account state, cloud/leaderboard state, and game simulation are separate. A match is not authoritative game truth; validate messages, bound rates/sizes, handle duplicate callbacks, player changes, joins/leaves, disconnects, and offline/restricted play.

Further sections — read when the above is not enough: `references/details.md`.
