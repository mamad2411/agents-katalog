---
name: expo-core
description: "Shared reference for the Expo cluster: EAS (Build/Submit/Update/Hosting), app config + config plugins, the Expo Go vs dev-client vs prebuild/CNG spectrum, SDK version policy, and Expo Router structure. USE WHEN configuring an Expo app, planning an EAS release, or upgrading the SDK — the platform model every Expo spoke shares. Pairs with react-native-core for the underlying RN runtime."
cluster: expo
version: 1.0.0
---

# Expo Core

Shared model for the `expo` cluster. The Expo spokes all sit on these concepts — keep them
consistent here. For the React Native runtime beneath Expo (New Architecture, Reanimated,
navigation), see `react-native-core`.

## 1. EAS — the cloud backbone

- **EAS Build** — cloud native builds (iOS/Android) without local Xcode/Android Studio. → `expo-cicd-workflows`
- **EAS Submit** — upload builds to App Store / Play Console. Needs store credentials.
- **EAS Update** — OTA JS/asset updates to installed apps, keyed to a **runtime version**. Only JS — native changes still need a new build. → `expo-deployment`
- **EAS Hosting** — host Expo Router API routes / web. → `expo-api-routes`

## 2. App config & config plugins

- Config lives in `app.json` / `app.config.js` / `app.config.ts` (the `.ts` form allows dynamic/env-driven config).
- **Config plugins** modify native project files at prebuild time — prefer them over hand-editing `ios/`/`android/` so the native side stays reproducible.
- `expo-tailwind-setup` and many libraries ship plugins; register them in `plugins: []`.

## 3. The managed ↔ bare spectrum (know where you are)

| Mode | Native dirs | Use |
|---|---|---|
| **Expo Go** | none | Fastest start; only Expo SDK modules, no custom native. |
| **Dev client** | generated | Custom native modules while keeping the Expo workflow. → `expo-dev-client` |
| **Prebuild / CNG** | generated from config | "Continuous Native Generation" — `ios/`/`android/` are build artifacts, regenerated from config + plugins. The recommended default. |
| **Bare** | committed & hand-edited | Full control; you own native upgrades. One-way from managed. |

Reach for a **dev client** the moment you need a native module Expo Go lacks.

## 4. SDK version is the source of truth

- An **Expo SDK** version pins a specific React Native version and a matched set of native deps. Don't mix versions across that boundary.
- Upgrade via `upgrading-expo` (the `expo install --fix` / upgrade flow), not ad-hoc `npm install`.
- **Runtime version** governs which OTA updates a build will accept — bump it when native changes.

## 5. Expo Router (app structure)

File-based routing under `app/`; layouts via `_layout.tsx`, native tabs/stacks, typed routes,
and server **API routes** (`+api.ts`). UI patterns → `building-native-ui`; server → `expo-api-routes`.

## 6. Native modules

Author native modules/views with the **Expo Modules API** (Swift / Kotlin / TS DSL) → `expo-module`.
This is the supported path to native code while staying in the Expo/CNG workflow.

## 7. Shared guardrails

- SDK version is canonical — it pins RN + native deps; upgrade through the official flow.
- Prefer **config plugins** over manual native edits (keeps prebuild reproducible).
- EAS Update ships **JS only**; native changes require a new build + runtime-version bump.
- Confirm store credentials/identifiers before EAS Submit.
- Managed → bare is effectively one-way — state it before ejecting.
- For RN-runtime concerns (Reanimated, gestures, New Architecture, navigation internals), defer to `react-native-core`.
