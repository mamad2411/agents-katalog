---
name: ios-project-target-architect
description: Architect or audit an Apple-platform project before implementation by choosing the correct Xcode targets, Swift modules and packages, extensions, schemes, configurations, capabilities, privacy resources, test plans, and evidence gates for a feature. Use when an iOS/iPadOS/watchOS/macOS/visionOS/CarPlay/App Clip/widget/Live Activity/companion feature needs a target-aware build route or when project structure and proof are unclear.
allowed-tools: Read, Grep, Glob
---

# iOS Project, Target, and Module Architect

## Overview

Shape the project around the user outcome and the Apple surface that owns it. Keep shared domain truth separate from target-specific process, UI, lifecycle, entitlements, and proof.

`outcome -> target graph -> module graph -> capability/configuration -> surface lifecycle -> executable evidence`

## Read before acting

- Inspect the real repository and preserve existing dirty work. Locate the `.xcodeproj` or `.xcworkspace`, `Package.swift` files, schemes, build configurations, deployment targets, supported destinations, target membership, source/resource folders, entitlements, `Info.plist` files, privacy manifests, extensions, App Groups, tests, fixtures, and generated artifacts.
- Read the [project-shape foundation](../ios-knowledge-base/references/00-foundations/03-project-shape-and-module-boundaries.md), [target and extension route matrix](../ios-knowledge-base/references/40-framework-routes/11-project-target-and-extension-route-matrix.md), [Xcode target/module plan](../ios-knowledge-base/references/90-templates/xcode-target-and-module-plan.md), [target-aware feature scaffold](../ios-knowledge-base/references/90-templates/target-aware-feature-scaffold.md), and [configuration/artifact checklist](../ios-knowledge-base/references/60-verification/06-target-configuration-and-artifact-checklist.md).
- Refresh the exact official Apple or Swift page for any API, target type, platform condition, entitlement, privacy requirement, build setting, or system surface you intend to use. Mark unresolved symbols or availability as `to-verify`; do not infer them from a framework name.

## Route workflow

1. Write the outcome, entry point, primary action, accepted result, failure consequence, offline requirement, privacy sensitivity, supported platforms, and whether the feature must run in the app, an extension, a companion, or a system-owned surface.
2. Inventory the existing project before proposing a target. Record project/workspace, app targets, framework or library targets, package products, extensions, tests, schemes, configurations, bundle identifiers, deployment targets, resources, entitlements, privacy manifests, and App Groups.
3. Draw a target graph. For every target, record platform/device family, process/host, bundle identifier, source and resource membership, linked products, capabilities, signing identity, lifecycle, and the evidence needed to prove it. Put dependencies in one direction: target-specific surface -> shared feature/domain modules -> platform adapters -> system frameworks.
4. Draw a module graph. Keep models, deterministic domain rules, persistence protocols, and feature use cases in shared modules. Keep SwiftUI screens, extension entry points, lifecycle delegates, OS-specific adapters, entitlements, and process-only state at the owning target boundary.
5. Select the narrowest target route:
   - Put ordinary UI, navigation, persistence, and feature orchestration in the main app target unless another process or system-owned entry point is required.
   - Use a framework or Swift package product for reusable domain, feature, or platform-adapter code with a clear dependency boundary.
   - Use an app extension only when the host/system invokes it; identify its host, extension point, process lifecycle, shared data route, and unavailable APIs.
   - Use WidgetKit, ActivityKit, App Intents, Share, File Provider, App Clip, watchOS, CarPlay, visionOS, or another companion/system target only when the user outcome requires that surface. Do not create a target merely to organize files.
6. Route dependencies. Prefer source package products when the source boundary is appropriate; inspect binary package products separately. Record minimum platform versions, product names, resource handling, transitive dependencies, license/provenance notes, and whether each target actually links the product.
7. Map the capability configuration. For each target, identify entitlements, capability toggles, usage descriptions, background modes, associated domains, App Groups, privacy manifest declarations, account/service setup, and protected-data boundaries. Put a requirement on the owning target and record the smallest verification action.
8. Map schemes and configurations. Identify Debug, test, preview/fixture, profile, and Release purposes; use `.xcconfig` files for intentional shared settings; make scheme actions and test-plan selection explicit. Never hide a target or entitlement change in an undocumented local setting.
9. Build the feature handoff: `surface input -> adapter or framework operation -> normalized evidence/proposal -> deterministic validation -> shared domain/use case -> persistence or side effect -> derived target/system presentation`.
10. Model lifecycle and failure states before implementation: unavailable, denied, restricted, not configured, loading, partial, stale, interrupted, cancelled, backgrounded, process-recreated, expired, conflict, and completed. Define start/stop/cancel/retry behavior and a fallback that does not pretend the capability succeeded.
11. If implementation is requested, create the smallest target/module slice that satisfies the outcome. Preserve the existing project shape, avoid circular dependencies, and keep system/extension entry points thin. If only planning or audit was requested, stop after producing the route and verification ledger.
12. Verify proportionally and report evidence by boundary: source, compile, unit/UI test, preview/fixture, simulator, physical device, two-device/accessory/vehicle, system invocation, signed artifact, TestFlight/App Store, and production. Record device, OS, build, target, configuration, task, result, and artifact path for each claim.

## Fast path

Draw the target dependency graph and mark its first compile-critical path. Prefer the existing target, package, scheme, and configuration; add a target or extension only when ownership or a system-host requirement demands it. Validate the graph before implementing feature code so a wrong target does not become the expensive discovery step.

## Configuration and proof ledger

For each target, fill this minimum record:

| Field | Record |
| --- | --- |
| Identity | Target name, product, bundle ID, platform/device family, deployment target |
| Inputs | Sources, resources, package products, linked frameworks, generated files |
| Process | Host, extension point, lifecycle, background/system invocation |
| Configuration | Schemes, configurations, `.xcconfig`, signing, capabilities, entitlements |
| Privacy | Usage descriptions, privacy manifest, App Group/data scope, retention/deletion |
| Tests | Test targets/plans, fixtures, accessibility, performance, route-specific checks |
| Evidence | Exact build/device/system/artifact claim, environment, date, result, next gap |

Do not report “builds,” “works on device,” “the widget/extension/system route works,” “the entitlement is active,” or “release-ready” until the matching evidence exists. Documentation establishes an API route; it does not establish compilation, signing, authorization, physical hardware behavior, system delivery, or App Review approval.

Further sections — read when the above is not enough: `references/details.md`.
