---
name: "npm-build-error-triage"
description: "Diagnose and fix Node/npm build & test failures for React/React Native: install/lockfile, tsc type errors, ESLint, Jest/Vitest, Metro/Vite bundling, Expo. Use when a Node-based build fails."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# npm Build Error Triage (React / React Native)

## Triage order
1. **Toolchain:** Node LTS present; `npm ci` (clean install from lockfile). For RN: expo/rn-cli reachable via `npx`.
2. **Types:** `tsc --noEmit` errors -> fix types (no `any` escape hatch); ensure `@types/*` present.
3. **Lint:** ESLint errors -> fix; do not blanket-disable rules.
4. **Tests:** Jest/Vitest failures -> see *-test-stabilization skill (providers, mocks, async).
5. **Bundling:** Metro (RN) / Vite (web) errors -> check `metro.config.js`/`vite.config.ts`, path aliases (`tsconfig.paths`), and asset/extension resolution.
6. **Expo:** `expo-doctor`; align SDK/dependency versions; native module compatibility.

Fix the smallest failing slice; re-run `npm ci && tsc --noEmit && lint && test && build`. Never delete tests or types to pass.
