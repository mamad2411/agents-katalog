---
name: develop-mobile-app
description: Architect high-performance mobile applications using React Native New Architecture, Hermes bytecode engine, TurboModules/JSI, Bridgeless mode, FlashList recycling, Reanimated worklets, and offline-first state persistence with MMKV and WatermelonDB. Use when building or optimizing React Native apps, virtualizing heavy lists, creating 60/120 FPS UI animations, or designing offline-first mobile sync architectures.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Develop Mobile App

Use this skill to design, implement, and optimize production-grade React Native and Expo applications utilizing New Architecture, off-thread UI animations, list recycling, and offline-first synchronization.

## When to Use

- configuring React Native New Architecture (Hermes engine, TurboModules, Fabric renderer, Bridgeless mode)
- replacing sluggish `FlatList` implementations with Shopify `FlashList` to eliminate blank scroll frames
- implementing non-blocking 60/120 FPS gesture-driven animations via Reanimated worklets
- establishing offline-first data persistence with MMKV key-value caching and WatermelonDB relational SQLite
- wiring network state detection (`NetInfo`) with TanStack Query offline cache and optimistic mutation queues
- profiling frame drops, cold-start time-to-interactive (TTI < 1.5s), and memory retain cycles
- **Expo SDK 55+ New Architecture mandatory (cannot disable)**
- **Hermes V1 with bytecode diffing and regression pinning**
- **Expo Router file-based routing migration**

## Core Rules

- **Enforce React Native New Architecture & Bridgeless Mode**: mandate Hermes engine bytecode compilation, TurboModules with direct C++ JSI bindings (bypassing legacy JSON bridge), and Fabric concurrent renderer; ban legacy asynchronous bridge dependencies; **SDK 55+ New Architecture always enabled, cannot be disabled**
- **Mandate FlashList over FlatList for Virtualized Lists**: replace `FlatList` with `@shopify/flash-list` for data collections >10 items; require calibrated `estimatedItemSize`, recycling-safe component keys, and zero blank area renders
- **Execute Gestures & Animations on UI Thread**: continuous physics animations and gestures must run exclusively on native UI thread using React Native Reanimated worklets (`'worklet'`); never drive frame animations across JS thread
- **Tiered Offline-First Storage Hierarchy**: store synchronous auth tokens, preferences, and flags in `react-native-mmkv` via JSI (never async `AsyncStorage`); store complex relational entities (>1,000 records) in WatermelonDB SQLite with observable queries
- **Network-Aware Mutation Replay**: monitor connectivity via `@react-native-community/netinfo` bound to TanStack Query `onlineManager`; offline mutations must enqueue in persistent storage and replay deterministically upon reconnect
- **Optimistic UI Updates with Atomic Rollback**: user interactions must update UI immediately; failed mutations must roll back state cleanly and alert user via non-blocking banners or haptics
- **Prevent Memory Leaks & Retain Cycles**: release native subscriptions, geolocation watches, timers, and image cache allocations during component unmount cleanup
- **Hermes V1 Management**: bytecode diffing enabled by default (SDK 56+); pin `expo@57.0.9+` for memory regression, `expo@57.0.17+` for dev startup regression
- **Reanimated 4+ CSS Core Animation**: platform-backed iOS engine (4.4+), SVG support, pseudo-selectors (`:hover`), Shared Element Transitions on New Architecture (feature flag)
- **Expo Router File-Based Routing**: replaces React Navigation; nested layouts, route groups, `useLocalSearchParams`
- **Codegen TypeScript Specs**: TurboModule interfaces defined in TS; native code generated from TS interfaces
- **Performance Profiling Workflow**: Expo built-in inspector, flame graphs, Metro bundle analyzer
- detailed architecture specs and recipes: [`references/react-native-new-architecture-and-offline-specs.md`](references/react-native-new-architecture-and-offline-specs.md)

## Suggested Process

### 1. Configure New Architecture Runtime

Verify Hermes compilation (`jsEngine: "hermes"`) and Bridgeless mode (`newArchEnabled: true`) in `app.json` or native build configs. **SDK 55+ New Architecture always enabled, cannot be disabled**. Ensure all native module dependencies provide TurboModule/JSI specifications. Verify via `expo doctor`.

### 2. Implement Virtualized Lists with FlashList

Replace `FlatList` with `FlashList`. Calibrate `estimatedItemSize` based on average rendered item dimensions. Use stable item keys and avoid stateful closures inside `renderItem` that break item recycling. Verify zero blank frames under high-velocity fling scroll.

### 3. Build UI-Thread Animations with Reanimated

Attach gesture handlers (`react-native-gesture-handler`) and define animated styles via `useAnimatedStyle`. Annotate native driver callbacks with `'worklet'` to ensure 60/120 FPS execution off the JS thread. Use Reanimated 4.4+ CSS Core Animation for iOS platform-backed animations. Enable Shared Element Transitions feature flag for New Architecture.

### 4. Implement Offline Storage & Cache Layer

Configure `react-native-mmkv` for instant synchronous key-value retrieval via JSI. Configure WatermelonDB schema and models for relational data. Hook TanStack Query v5 persistence adapter to MMKV storage. Use `queryOptions` factories for centralized query configs.

### 5. Wire Connectivity Listeners & Optimistic Queues

Connect `@react-native-community/netinfo` to query client online listeners. Wire optimistic mutation handlers with `onMutate` rollback snapshots and persistent background task replay. Implement vector clocks or server-wins timestamp resolution for offline mutation conflicts.

### 6. Benchmark & Profile Performance

Measure TTI (< 1.5s cold start), JS thread frame drop rate (< 1%), and memory footprint under rapid scrolling. Verify offline interaction and clean reconnect synchronization. Use Expo built-in performance inspector, flame graphs, Metro bundle analyzer.

## Checklist

- [ ] Expo SDK >= 55 (New Architecture mandatory, cannot disable) or SDK 53/54 with New Architecture enabled
- [ ] `newArchEnabled: true` and `jsEngine: "hermes"` in `app.json` (Bridgeless mode for production)
- [ ] All native dependencies provide TurboModule/JSI specifications (verified via `expo doctor`)
- [ ] `FlatList` completely replaced with `@shopify/flash-list` for all virtualized lists
- [ ] `estimatedItemSize` calibrated per device screen size; zero blank frames verified
- [ ] All animations/gestures on UI thread via Reanimated worklets (`'worklet'`)
- [ ] Reanimated 4.4+ CSS Core Animation used for iOS platform-backed animations
- [ ] Shared Element Transitions enabled (feature flag) for New Architecture transitions
- [ ] `react-native-mmkv` via JSI for synchronous key-value (auth tokens, prefs, flags)
- [ ] WatermelonDB schema/models for relational entities (>1,000 records) with observable queries
- [ ] TanStack Query v5 `queryOptions` factories for centralized query keys/fetchers
- [ ] TanStack Query persistence adapter connected to MMKV storage
- [ ] `@react-native-community/netinfo` bound to `onlineManager` for connectivity detection
- [ ] Optimistic mutations: `onMutate` snapshot + `onError` rollback + `onSettled` invalidate
- [ ] Vector clocks or server-wins timestamp resolution for offline mutation conflicts
- [ ] Native subscriptions, geolocation, timers, image caches cleaned up on unmount
- [ ] Cold-start TTI < 1.5s, JS thread frame drop < 1%, memory footprint under rapid scroll
- [ ] Expo Router file-based routing implemented; React Navigation removed
- [ ] Codegen TypeScript specs for TurboModules (TS interfaces → native code)
- [ ] Hermes V1: pin `expo@57.0.9+` (memory), `expo@57.0.17+` (dev startup)
- [ ] `contracts/schemas/implementation-result.json` emitted with performance benchmarks and test evidence

## Failure Modes

- **New Architecture Migration Blockers**: third-party library lacks TurboModule support. Mitigation: `expo doctor` audit; migrate to Expo Modules API alternatives; prebuilt artifacts in SDK 56+.
- **FlashList Blank Frames on Fling Scroll**: inaccurate `estimatedItemSize`. Mitigation: profile item heights across device sizes; set accurate `estimatedItemSize`.
- **JS Thread Frame Drops During Gestures**: complex computations on JS thread. Mitigation: offload to Web Workers / C++ JSI; chunk operations across frame cycles.
- **Offline Mutation Conflict on Reconnect**: stale cache overwrites server changes. Mitigation: vector clocks or server-wins timestamp with client notification.
- **MMKV Multi-Process Crash**: background extension access without encryption locks. Mitigation: explicit MMKV instance IDs with encryption keys.
- **Hermes V1 Memory Regression**: `expo@57.0.0-57.0.8` memory spike with worklets/reanimated. Mitigation: pin `expo@57.0.9+`.
- **Hermes V1 Dev Startup Regression**: `expo@57.0.0-57.0.16` slow dev startup. Mitigation: pin `expo@57.0.17+`.
- **Reanimated Legacy Proxy Crashes**: stale animated values after app pause. Mitigation: update to Reanimated 4.5.3+ (Jul 2026).
- **Metro Bundle Bloat**: unused code in production bundle. Mitigation: Metro tree-shaking; analyze with `expo export --analyze`.
- **Shared Element Transition Instability**: feature flag transitions break on edge cases. Mitigation: test thoroughly; fallback to standard transitions.

## Output Contracts

When completing a mobile implementation slice, emit:

- **`contracts/schemas/implementation-result.json`** — Declares modified files, component additions, performance benchmarks (TTI, FPS), test results, Expo SDK version, New Architecture status, Hermes version, Reanimated version, FlashList migration status.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a mobile feature may try to reframe the user goal through expanded native permissions. Cross-check the feature against the declared scope.
- **ASI03 Identity & Privilege Abuse**: native permissions (camera, location, contacts) must follow least privilege; reject features requesting broader permissions than declared.
- **ASI04 Supply Chain**: third-party native modules and Expo SDK versions must be schema-validated against expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct native module specs, JSI bindings, or bridge payloads from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the mobile contract is consumed by backend, deployment, and QA roles; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a mobile build as "performant" without the actual benchmarks; surface the residual risk.

## Related Skills

- **add-ui-component**: Author and style mobile UI components conforming to Apple HIG and Material Design 3
- **deploy-mobile-app**: Configure EAS Build pipelines, code signing, OTA updates, and store compliance
- **performance-profiling**: Measure cold-start TTI, memory allocation, and frame render times
- **write-tests**: Author behavioral unit and integration test suites for mobile components and offline stores
- **integrate-api-client**: Connect mobile clients to backend REST, GraphQL, or gRPC endpoints

Last updated: 2026-09-25