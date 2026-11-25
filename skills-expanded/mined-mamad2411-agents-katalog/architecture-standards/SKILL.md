---
name: architecture-standards
description: ACTIVATE THIS SKILL if the user mentions: 'Zustand', 'Store', 'Hydration', 'Next.js 16', 'Database', 'ID', 'UUID', 'RPC', 'RLS', 'Supabase', 'Social', 'Privacy', or 'Realtime'.
---

# 🚨 ARCHITECTURE-STANDARDS OPERATIONAL RULES (MANDATORY)

## 0. Efficiency Directive (PRIORITY 0)
- **Identity:** If you are a sub-agent, you are the terminal **DELEGATE**.
- **Terminality:** Sub-agents are forbidden from using `invoke_agent`.
- **Parallel Discovery:** You MUST use parallel tool calls for file reads/searches.
- **Verification Sandbox:** You are permitted to use `write_file` ONLY for temporary files (e.g., `temp_fix.ts`).
- **Circuit Breaker:** If the same error occurs twice, STOP and report "Strategy Exhausted."
- **Diagnostic Signal:** All failures MUST include: [BLOCKER], [HYPOTHESIS], and [ACTION]. Failures MUST also provide:
    - **Zustand Store Dump:** (via `page.evaluate(() => useStore.getState())`)
    - **Network Trace:** (Summary of failed RPCs/APIs from logs)
- **Build Limit:** Never use the `--build` flag if a build has already occurred in the parent session.
- **Acknowledge:** Your first turn MUST state: "I have read and will obey the Efficiency Directive as the terminal DELEGATE."

## 0. Next.js 16 Middleware (Proxy)
- **`arch-next16-proxy`**: `proxy.ts` is the ONLY valid entry point for request-time logic (Middleware). 
- The `middleware.ts` convention is DEPRECATED and removed.
- Use `proxy.ts` in the root directory.

## 1. Role: Senior Software Architect
- You are the primary guardian of the project's architectural integrity and database security.
- Your goal is to ensure that all changes adhere to the "Supabase-Native" and "Next.js 16" patterns.

## 2. 🚨 NEGATIVE CONSTRAINTS (CRITICAL)
- **NEVER** create new Next.js API routes for CRUD logic; you MUST prioritize direct client-to-Supabase logic (RPCs/SDK).
- **NEVER** reference a `members` column on the `trips` table; you MUST use the `trip_members` join table.
- **NEVER** use `toISOString().split('T')[0]` for user-facing dates; you MUST use `formatDateLocal`.
- **NEVER** persist large data arrays in `localStorage`; you MUST only persist minimal metadata.
- **NEVER** use legacy string arrays for trip members; you MUST use the structured `TripMember` type.
- **NEVER** skip the `SET search_path = public, auth` directive in Postgres functions.
- **NEVER** call getter functions for reactive state; you MUST subscribe directly to state in `useMemo` dependencies.

## 3. Mandatory Research
- Before modifying a database schema, you MUST review the existing migrations in `supabase/migrations/` as the **Single Source of Truth**.
- Before adding a new UI component, you MUST check if it can be implemented as a "Presentational" component.

# Core Architectural & Database Standards

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Database & Security | CRITICAL | `arch-db` |
| 2 | State & Hydration | CRITICAL | `arch-state` |
| 3 | UI Patterns & Styling | HIGH | `arch-ui` |
| 4 | Social & Privacy | HIGH | `arch-social` |

## Technical Implementation Standards

### 1. Database & Security (`arch-db`)
*   **Supabase Native:** Prioritize direct client-to-Supabase logic. **NEVER** create new Next.js API routes for CRUD logic.
*   **RPC Search Paths:** All Postgres functions **MUST** set `SET search_path = public, auth` and use explicit `public.` prefixes.
*   **The Join-Table Rule:** Always use the `trip_members` table and `public.is_trip_member()` helper. **NEVER** reference a `members` column on the `trips` table.
*   **RLS Visibility Rule:** All `SELECT` policies MUST include a direct ownership check (`auth.uid() = user_id`) BEFORE complex function calls.
*   **Migrations SSOT:** `supabase/migrations/` files are the **SINGLE SOURCE OF TRUTH**.
*   **RPC Schema Parity:** Reflect all DB changes in `lib/database.types.ts`.
*   **API Nuclear Bypass:** Token-exchange routes MUST implement a bypass for `'mock-code'` BEFORE initializing the Supabase client.

### 2. ID System & Local Stability (`arch-db`)
*   **Dual-ID System:** Distinguish between `GooglePlaceId` (string) and `WineryDbId` (number).
*   **The Numeric ID Normalization Rule:** Normalize all relational IDs to `Number()` upon retrieval.
*   **The Local Date Stability Rule:** Always use `formatDateLocal(date)` and `getTodayLocal()`.

### 3. State Management & Hydration (`arch-state`)
*   **Next.js 16 Hydration:** **Avoid Hard Reloads.** Trigger refreshes via `page.evaluate` inside retry loops.
*   **Store Split:** Distinguish between `wineryDataStore` (Persisted Cache) and `wineryStore` (UI State).
*   **Merge on Hydrate:** `hydrateWineries` MUST merge markers with detailed data.
*   **The Ghost Status Rule:** Clear local `visits` if the server reports `user_visited: false`.
*   **Hydration Optimization:** **NEVER** persist large data arrays in `localStorage`.
*   **Reactivity Rule:** SUBSCRIBE DIRECTLY to state (e.g., `useStore((s) => s.data)`). Getter functions will NOT trigger re-evaluations.
*   **Store Exposure:** Every major store and the `supabase` client MUST be exposed to `window` for E2E.
*   **The Revision Lock Rule:** Track `lastActionTimestamp` to prevent "Flicker" race conditions in Realtime.
*   **The Modal Reset Rule:** Any "close" action in `useUIStore` (e.g., `closeModal`, `closeVisitForm`) MUST explicitly reset all feature-specific state (e.g., `activeVisitWinery`, `editingVisit`, `activeNoteWineryDbId`) to `null` to prevent stale UI flashes in subsequent renders.

### 4. UI Patterns & Styling (`arch-ui`)
*   **Container/Presentational:** UI components MUST be "Presentational" (no store calls). Container/Page components handle store connections.
*   **The Tailwind Mandate:** Use **Tailwind CSS v4** utility classes. Prioritize `shadcn/ui`.
*   **The DnD Hydration Rule:** Wrap `DragDropContext` in a `mounted` state check.

### 5. Social & Privacy Logic (`arch-social`)
*   **Collaborative Trips:** Use the structured `TripMember` type. Legacy string arrays are deprecated.
*   **Normalization:** All social relations use `trip_members`, `follows`, and `activity_ledger`.
*   **Visibility:** Use the `is_visible_to_viewer` RPC for Public/Friends/Private tiers.
