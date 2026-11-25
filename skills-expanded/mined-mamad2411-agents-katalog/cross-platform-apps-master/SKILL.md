---
name: cross-platform-apps-master
description: >-
  Master hub for building professional desktop, mobile, and unified one-codebase apps. Use to ship
  desktop apps (Electron vs Tauri, packaging, code signing, notarization, auto-update), high-end
  mobile apps for iOS + Android (React Native/Expo, native modules, performance, push, offline,
  store deploy), and a SINGLE codebase that targets web + desktop + mobile (Expo Router + React
  Native Web + Tauri/Electron, or Flutter), plus app-store/Play/desktop distribution and CI/CD.
  Bundles 6 specialized skills (in skills/<name>/GUIDE.md). Use for any desktop/mobile/cross-platform build.
---

# Cross-Platform Apps — Master Hub (desktop · mobile · one codebase)

Ship **production** apps across every surface like a senior product engineer: correct architecture,
native integration, performance, signing/notarization, store submission, and CI/CD — not demos.

## How to use this hub

1. Start with **cross-platform-architecture** to pick the strategy and monorepo shape.
2. Open the surface-specific skill (desktop / mobile / unified).
3. Finish with **app-store-deployment** and **native-bridge-integration** as needed.
4. For framework deep-dives (RN, Expo, Flutter, Swift/Xcode) also use **`mobile-master`**.

## Bundled skills

- **cross-platform-architecture** ⭐ — Decide the approach (one codebase vs per-platform), monorepo
  (pnpm/Turborepo), shared business logic/types/design system, platform-specific files, and code-sharing %.  
  → `skills/cross-platform-architecture/GUIDE.md`
- **desktop-apps-pro** ⭐ — Desktop done right: **Electron vs Tauri** decision, IPC security, native
  menus/tray, auto-update, packaging, **code signing + macOS notarization**, Windows signing, performance.  
  → `skills/desktop-apps-pro/GUIDE.md`
- **mobile-apps-pro** ⭐ — High-end iOS + Android: RN/Expo (and when Flutter/native), native modules,
  performance (Hermes, lists, startup), offline/sync, push, deep links, secure storage, a11y.  
  → `skills/mobile-apps-pro/GUIDE.md`
- **unified-one-codebase** ⭐ — One codebase → web + desktop + mobile: Expo Router universal +
  React Native Web + Tauri/Electron wrapper (or Flutter), shared packages, `.native/.web` splits, responsive.  
  → `skills/unified-one-codebase/GUIDE.md`
- **app-store-deployment** — Ship it: App Store Connect + TestFlight, Play Console, EAS Build/Submit,
  desktop distribution (DMG/MSI/AppImage), signing/notarization, CI/CD, phased rollout.  
  → `skills/app-store-deployment/GUIDE.md`
- **native-bridge-integration** — Deep native access: Expo Modules / RN TurboModules / Tauri plugins —
  camera, BLE, biometrics, secure enclave, background tasks, and bridging platform SDKs safely.  
  → `skills/native-bridge-integration/GUIDE.md`

## Pairs well with

`mobile-master` (RN/Expo/Flutter/Swift/Xcode deep-dives), `fullstack-stacks-master` (shared TS stack +
API contract), `ui-master` + `tailwind-master` (design system, RN Web styling), `devops-master` (CI/CD),
`systems-platforms-master` (backend/data), `backend-api-master` (auth, APIs).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list.
