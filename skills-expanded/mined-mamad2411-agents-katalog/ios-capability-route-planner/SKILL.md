---
name: ios-capability-route-planner
description: Turn an iOS app idea or feature request into an Apple-native capability route, framework/symbol choices, SwiftUI and Liquid Glass surface plan, on-device AI boundaries, permission/entitlement/privacy matrix, lifecycle/fallback contract, and proportional verification plan. Use when planning, reviewing, or debugging a native iOS/iPadOS/watchOS/CarPlay/App Clip/spatial feature before implementation or when a project has framework, system-surface, device, or evidence confusion.
allowed-tools: Read, Grep, Glob
---

# iOS Capability Route Planner

## Overview

Turn an idea into a capability route and evidence plan before framework choices harden into implementation. Preserve native Apple behavior, original product identity, privacy boundaries, and honest device/system/release claims.

`outcome -> narrow Apple route -> state/data boundary -> native surface -> permission/entitlement -> lifecycle/fallback -> verification evidence`

## Read before acting

- Inspect the actual repository and target: Xcode project/workspace, schemes, deployment target, platforms/device families, modules, persistence, networking, extensions, entitlements, `Info.plist`, privacy manifest, assets, existing system surfaces, and current tests.
- Read the [knowledge-base map](../ios-knowledge-base/references/README.md), [capability-first Apple SDK atlas](../ios-knowledge-base/references/40-framework-routes/10-capability-first-apple-sdk-atlas.md), [framework availability and device-proof matrix](../ios-knowledge-base/references/40-framework-routes/08-framework-availability-and-device-matrix.md), and the relevant [deep-dive indexes](../ios-knowledge-base/references/41-framework-deep-dives/README.md), [device/system routes](../ios-knowledge-base/references/42-framework-deep-dives/README.md), and [system framework routes](../ios-knowledge-base/references/43-system-framework-deep-dives/README.md).
- For design work, read the [native screen composition atlas](../ios-knowledge-base/references/21-design-deep-dives/08-native-screen-composition-atlas.md), [functional Liquid Glass interactions](../ios-knowledge-base/references/20-liquid-glass/05-functional-glass-interactions.md), and [accessibility/adaptation recipes](../ios-knowledge-base/references/70-code-recipes/12-accessibility-adaptive-and-native-design-recipes.md).
- For intelligence work, read the [AI feature lifecycle](../ios-knowledge-base/references/30-on-device-ai/09-ai-feature-lifecycle-and-availability.md), [AI evaluation discipline](../ios-knowledge-base/references/30-on-device-ai/10-on-device-ai-evaluation-and-model-update-discipline.md), and [reviewable multimodal pipeline](../ios-knowledge-base/references/31-on-device-ai-recipes/06-reviewable-multimodal-ai-pipeline.md).
- Refresh the exact official Apple/Swift pages in the [source registry](../ios-knowledge-base/references/sources/official-source-registry.md) before relying on a symbol, availability condition, entitlement, system surface, or iOS 26 behavior.

## Route workflow

1. State the outcome in one sentence. Record the entry point, primary action, accepted result, consequence of error, offline requirement, privacy sensitivity, and supported platforms.
2. Classify the capability: present/edit, persist/sync, capture/analyze, communicate, locate/map/weather, use protected data, control a device, transact/authenticate, expose to the system, share/export, run in the background, build spatial/graphics/game content, or extend to a companion surface.
3. Select the narrowest Apple route. Prefer SwiftUI/UIKit/system-owned surfaces, PhotosUI/file import, Vision/Core ML, Speech/Translation, MapKit/Core Location, HealthKit/Contacts/EventKit, StoreKit/PassKit/AuthenticationServices, App Intents/WidgetKit/ActivityKit, and the relevant device/companion framework before inventing a custom service.
4. Name concrete symbols and rejected alternatives. Record why the route owns the capability, what it does not own, and which API signatures/availability annotations still require an Xcode check.
5. Draw the handoff: `input -> framework observation/operation -> normalized app evidence -> deterministic validation -> domain truth -> derived presentation -> system/companion handoff`.
6. Build the state matrix before the happy path. Include checking, ready, denied, restricted, unsupported, unavailable, not-ready, loading, partial, stale, interrupted, cancelled, expired, empty, invalid, conflict, and completed states where relevant.
7. List every permission, usage description, entitlement, background mode, App Group, associated domain, merchant/account/service setup, language/asset condition, hardware requirement, and server dependency. Mark unknowns `to-verify` rather than inferring them from a framework name.
8. Design the native surface. Use semantic controls, system typography, adaptive containers, correct navigation/tab/toolbar/sheet ownership, Dynamic Type, VoiceOver, reduced motion/transparency, localization, keyboard/pointer/controller input, and a manual fallback. Use Liquid Glass system adoption first; add custom glass only to a functional related group that needs it.
9. Choose proportional evidence. Separate source, compile, preview/fixture, simulator, physical device, two-device/accessory/vehicle, system surface, signed artifact, TestFlight/App Store, server/account, and production proof.
10. Produce the route plan and stop before implementing unless the user explicitly asked for the build. If implementation is requested, keep the first slice narrow and make the route’s verification gates executable in the target project.

## Fast path

For one feature, compare no more than the plausible capability lanes against outcome ownership, target availability, setup cost, fallback, and required proof. Pick the first route that satisfies the outcome with the least irreversible configuration, then record the other lanes as rejected or deferred. Expand the matrix only when a new requirement changes that decision.

## Architecture and proof contract

Return a compact table or document with these fields:

| Field | Required content |
| --- | --- |
| Outcome and consequence | User task, primary action, acceptable failure, and reversibility. |
| Selected route | Frameworks, concrete symbols, target platforms, rejected alternatives, and API questions. |
| Data boundary | Source, representation, normalization, persistence, sync, retention, deletion, and derived values. |
| UI/system boundary | SwiftUI/UIKit/system/extension/Watch/CarPlay/spatial surface, navigation, review, deep link, and fallback. |
| State/lifecycle | Permission, availability, start/stop/cancel/interrupt/background/process/account/asset states. |
| Trust boundary | Deterministic validation, authorization, confirmation, idempotency, conflict, and side-effect policy. |
| Configuration | Entitlements, usage descriptions, privacy manifest, background modes, App Groups, domains, accounts, and server dependencies. |
| Tests | Fixtures, unit/UI/accessibility/performance tests, simulator, physical/two-device/system tests. |
| Evidence gaps | Exact claims not yet proven and the next smallest verification action. |

Further sections — read when the above is not enough: `references/details.md`.
