---
name: gurudevi-quality-gate
description: >
  Architectural quality gate for Gurudevi Mobile. Activates when editing files in
  apps/gurudevi-mobile, src/hooks, src/lib, app/_layout, src/providers, or packages/core.
  Enforces blast-radius classification, DRY discipline, and feature spec contracts
  before any code is generated.
---

# Gurudevi Quality Gate

You are operating inside a **quality-gated workspace**. This document enforces architectural boundaries and progressive disclosure of technical context. Before generating any code, you must align with the capabilities and absolute limits of our technology stack.

---

## 1. The Tech Stack Matrix: Capabilities vs. Limits

### 1.1. PowerSync + Drizzle + SQLCipher (op-sqlite)
* **Capabilities:** 
  * Offline-first, reactive local-first query sync. JSI C++ database execution (<20ms).
  * Automatically replicates Postgres tables from Supabase to local SQLite file (`gurudevi-powersync.db`).
* **Absolute Limits & Constraints:**
  * **The Permission Proxy:** Direct database mutations (`insert`, `update`, `delete`) must flow through the Secure Drizzle Proxy (`createSecureDrizzleProxy`). This Proxy intercepts calls and verifies them against offline Cedar snapshots. If blocked, it throws a `LOCAL_WRITE_VIOLATION` `SovereignError`.
  * **Bootstrap Sequence:** Accessing `getPowerSyncDB()` or `getDrizzleDB()` before `bootstrapPlatform()` is run and `coreRuntime` is registered triggers the `PowerSync bootstrap guard` throwing an error.
  * **Web/Testing Mocking:** On the web (PWA/testing/Vitest), PowerSync runs a mock proxy database (`createWebPowerSyncDatabase`). Never write code expecting database persistence or actual sync in web/test envs unless mocks are explicitly wired.
  * **SQLite Drizzle Schema:** Tables must be declared in `packages/core/src/adapters/powersync/schema.ts` using pure Drizzle SQLite definition types. Postgres-specific features (JSONB, native Postgres arrays, pg-specific types) are strictly prohibited.

### 1.2. Sovereign Identity / ReBAC (Bonds & Perspectives)
* **Capabilities:** 
  * Multi-tenant security based on "Bonds" (relationship between user and school/classroom) and "Perspectives" (currently active viewpoint).
  * Fast local capability validation via Cedar engine snapshots.
* **Absolute Limits & Constraints:**
  * **No Raw Metadata Access:** Never read raw Supabase `Session.user` metadata for business or security checks. Always resolve the user context through the active bond state (`useStore.getState().activeBond` or `useAuth()`).
  * **TOBAC (Token-Based Access Control) Route Guard:** Global route-gating is handled in `_layout.tsx`. If a session token is expired, the route guard redirects to `/welcome`. Do not add inline auth routing checks inside screens; rely on the global router/guard.

### 1.3. Expo Router (File-based Navigation)
* **Capabilities:** 
  * Typesafe navigation (`href` matches folders). Deep link resolution.
* **Absolute Limits & Constraints:**
  * **Thin Root Shell:** `app/_layout.tsx` must remain a thin composition of providers. No inline business logic or side effects. If a feature needs global bootstrap, it MUST go to specialized providers or effects files (e.g. `src/providers/AppBootstrapEffects.tsx`).
  * **Route References:** Navigation between screens must use absolute path references (e.g. `/classroom`) instead of relative steps (e.g. `../classroom`).

### 1.4. Monorepo Layering (Turborepo + pnpm workspaces)
* **Capabilities:** 
  * Isolated package caching, modularized UI/core dependencies.
* **Absolute Limits & Constraints (Enforced by dependency-cruiser):**
  * **Layer 0 (`packages/core`, `packages/types-shim`):** Can never import from higher layers (`packages/ui`, `packages/classroom`, apps, etc.).
  * **Layer 1 (`packages/ui`):** Can never import from domains (`packages/classroom`, `packages/people`, etc.) or apps.
  * **No App Leaks:** Code under `packages/` can never import from `apps/` (like `apps/gurudevi-mobile`).
  * **Database Isolation:** Direct database imports from `packages/database` are forbidden outside `core` and `database` themselves. Apps and domains must access database types and objects through core type wrappers.
  * **Path Alias Standard:** All internal relative imports within packages and apps must use `@/*` path aliases (e.g. `import { foo } from '@/components/foo'`).
  * **Subpath Exports & Public APIs:** Cross-package imports must target declared package subpaths (`@repo/ui/components`, `@repo/core/logic`) or root package exports (`@repo/ui`). Literal deep `/src/` imports across package boundaries are strictly prohibited and verified by `pnpm check:deep-imports`.
  * **Copy-Paste & Duplication Prevention:** Duplicate blocks across files must be prevented (`pnpm run audit:duplication` / `jscpd`).
  * **Cognitive Complexity Budget:** Cognitive complexity must remain under 15 for all functions and React components.

---

## 2. Pre-Generation Demarcation & Decision Checklist

### Step 1: Classify the Blast Radius
Identify which zone the target file belongs to:

| Zone | Files | Agent Latitude |
|---|---|---|
| 🔴 RED | `app/_layout.tsx`, `src/providers/SanctuaryProvider.tsx`, `packages/core/src/logic/`, `packages/database/`, `supabase/migrations/` | Zero autonomy. Propose only. Human approves every line before merge. |
| 🟡 AMBER | `src/hooks/`, `src/lib/`, `features/`, `packages/*/src/` | Generate + test. Human reviews diff before merge. |
| 🟢 GREEN | `src/screens/`, `src/components/`, `app/(tabs)/`, `src/ui/` | High autonomy. Verify output compiles and renders. |

*If RED zone:* Stop. Write a proposal document first. Do not write implementation code until the user explicitly says "proceed."

### Step 2: Check for Existing Utilities (DRY Mandate)
Before writing ANY new function, hook, or utility, check the utility map in Section 4. If a function already exists that covers the need, reuse it.

### Step 3: Write a Feature Spec (For RED/AMBER Zones)
If you are modifying AMBER/RED zone logic, require this spec format before generating code:
```markdown
# FEATURE SPEC: [Name]
## Blast Zone: RED | AMBER | GREEN
## Target File: `[exact path]`
## Reuses: [list existing hooks/utils/types this will call]
## Does NOT: [explicit prohibitions — e.g., "does not add to _layout.tsx"]
## Complexity Budget: max [N] lines, cognitive complexity < 15
```

---

## 3. Verification Protocol

After writing code, run the following verification steps:
1. **TypeScript compilation:** Run `pnpm check-types` (which runs `pnpm turbo run check-types`) to check types.
2. **ESLint Static Analysis:** Run eslint on changed files. Ensure cognitive complexity (threshold 15) is enforced.
3. **Copy-paste Detection:** Run `jscpd [changed files] --min-lines 8 --min-tokens 50 --reporters console` to verify no duplicate blocks are added.

---

## 4. Verified Core Utility Map

| Need | Verified File Path | Usage Notes |
|---|---|---|
| **Auth State & Session** | [useAuthLifecycle.ts](file:///c:/Users/Naween/projects/polymath-platform/packages/core/src/hooks/useAuthLifecycle.ts) | Manages unified session resolution and PostHog/Sentry user identity. |
| **Global State Store** | [useStore.ts](file:///c:/Users/Naween/projects/polymath-platform/packages/core/src/store/useStore.ts) | Access via `useStore((state) => state.user)`. Contains available bonds and perspective. |
| **Notification Manager**| [PushNotificationManager.ts](file:///c:/Users/Naween/projects/polymath-platform/packages/core/src/logic/managers/PushNotificationManager.ts) | Use for local/remote push registration and dispatch. |
| **Isomorphic DB** | [database.ts](file:///c:/Users/Naween/projects/polymath-platform/packages/core/src/adapters/powersync/database.ts) | `getPowerSyncDB()` and `getDrizzleDB()`. Intercepts mutations for offline permission checks. |
| **Web DB Mock** | [database.web.ts](file:///c:/Users/Naween/projects/polymath-platform/packages/core/src/adapters/powersync/database.web.ts) | Web proxy database shim that returns empty arrays or stubs. |
| **Schema Definitions** | [schema.ts](file:///c:/Users/Naween/projects/polymath-platform/packages/core/src/adapters/powersync/schema.ts) | SQLite table definitions. Keep it database-agnostic. |
| **Global Shell Shell** | [_layout.tsx](file:///c:/Users/Naween/projects/polymath-platform/apps/gurudevi-mobile/app/_layout.tsx) | Thin provider/navigation composition. Do not inject business logic. |
