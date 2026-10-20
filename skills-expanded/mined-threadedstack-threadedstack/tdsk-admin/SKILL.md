---
name: "tdsk-admin"
description: "Knowledge base for the admin SPA dashboard repo"
tags: ["react", "vite", "mui", "jotai", "tanstack-query", "frontend", "admin-dashboard", "billing", "quotas", "agents", "ai-chat", "skills", "schedules"]
---
# Admin Repo Skill

## Overview

- **SPA dashboard** for Threaded Stack (`@tdsk/admin`), built with Vite + React + MUI + Jotai + TanStack React Query
- **Authentication**: Neon Auth (`@neondatabase/neon-js`) with social OAuth (GitHub, GitLab, Google, Vercel) + email login
- **Path Alias**: `@TAF/*` via `alias-hq`; styling via Emotion + MUI theming; toasts via Sonner; analytics via PostHog
- **Data flow**: React Router v7 loaders -> API actions -> services -> TanStack cache -> Jotai store -> components
- 22 action domains, 48 component directories, 23 Jotai atom files, 29 service files

## Directory Structure

```
repos/admin/
├── configs/                    # Vite, biome, nginx, env loading (frontend.config.ts)
├── scripts/                    # addToProcess, loadEnvs, registerPaths, setupTests, testUtils
└── src/
    ├── index.tsx               # Bootstrap: StrictMode > Jotai Provider > AuthProvider > App + Version
    ├── App.tsx                 # ThemeProvider > GlobalStyles > RouterProvider
    ├── actions/                # ~256 files across 22 domains (api/ + local/ subdirs)
    ├── components/             # 48 directories, 210+ files
    ├── constants/              # endpoints.ts, envs.ts, monaco.ts, nav.tsx, onboarding.ts, providers.ts, query.ts, storage.ts, tools.ts, values.ts
    ├── contexts/               # AuthContext/Provider (Neon Auth)
    ├── hooks/                  # 43 files: chat/, components/, endpoints/, nav/, org/, permissions/, project/, sandboxes/, theme/
    ├── pages/                  # Account, Billing, Home, Layout, Login, Orgs/*, Profile, Projects/*, Providers, Settings
    ├── routes/                 # Routes.tsx (createBrowserRouter + lazy loading), loaders.ts (26 loaders)
    ├── services/               # 29 service files (singleton classes)
    ├── state/                  # 23 Jotai atom files + accessors.ts + selectors.ts + index.ts
    ├── theme/                  # GlobalStyles.tsx
    ├── types/                  # 18 type definition files (includes routes.types.ts with ERoutePath enum, sandbox.types.ts)
    └── utils/                  # api/, endpoints/, errors/, nav/, permissions/, sandbox/, text/, transforms/, user/
```

## Routing

**File**: `src/routes/Routes.tsx` -- uses React Router 7's `createBrowserRouter` with `SuspensePage` helper for lazy loading and `RouteError` boundary.

**Route Tree**:
```
/ (root) > Layout (SignedIn guard + Sidebar + Outlet)
├── / > Home
├── /orgs > Orgs list
├── /billing > Billing/subscriptions
├── /orgs/:orgId
│   ├── (index) > Org dashboard
│   ├── /members, /secrets, /domains, /providers, /sandboxes, /settings, /usage, /skills, /schedules, /api-keys, /agents
│   ├── /projects > Projects list
│   └── /projects/:projectId
│       ├── (index) > ProjectWorkspace
│       ├── /endpoints, /secrets, /domains, /functions, /agents, /sandboxes, /api-keys, /settings, /members
│       ├── /endpoints/:endpointId > EndpointLayout (index, /config, /test)
│       ├── /threads > ProjectThreads
│       │   ├── /:threadId > Thread detail
│       │   └── /:threadId/chat > Thread chat
│       └── /agents/:agentId > AgentLayout
│           ├── (index) > AgentDetailTab
│           ├── /threads, /chat, /skills, /schedules
│           └── /threads/:threadId (detail, /chat)
├── /settings, /profile
├── /auth/:pathname > Login
├── /account/:pathname > Account
└── * > Redirect to /
```

**Route paths** exist in both relative form (for nested children, e.g., `members`) and absolute form (for nav links, e.g., `/orgs/:orgId/members`) in the `ERoutePath` enum in `src/types/routes.types.ts`. The `buildRoute()` utility replaces `:orgId`, `:projectId`, etc. with actual IDs.

**Loaders** (`src/routes/loaders.ts` -- 26 loaders, 389 lines): Use `criticalFetch` (throws on error, renders errorElement) and `safeFetch` (returns undefined on error) patterns. Hierarchy: `rootLoader` (orgs) -> `orgScopeLoader` (sets active org, fetches projects + providers) -> entity loaders -> `projectScopeLoader` -> project entity loaders -> detail loaders.

## State Management (Jotai)

Three-layer design:
1. **Atoms** (`src/state/<entity>.ts`) -- `atomWithReset` for resettable state, derived atoms for computed values (e.g., `activeOrgState`, `projectEndpointsState`)
2. **Accessors** (`src/state/accessors.ts`) -- Imperative `get*/set*/reset*` for use outside React (actions, services). Includes scope-keyed accessors: `getContext*/setContext*` for org-scoped entities, `getProject*/setProject*` for project-scoped, `getThread*/setThread*` for messages.
3. **Selectors** (`src/state/selectors.ts`) -- `useRecState` (returns [value, setter, resetter]) and `useDerivedState` (returns [value, setter, noOp]) hooks for React components.

**23 atom files**: agents, apiKeys, app, assets, domains, endpoints, functions, invoices, messages, onboarding, orgs, projectMembers, projects, providers, quotas, sandboxes, schedules, secrets, skills, subscriptions, theme, threads, user. Each typically exports an entity state atom (`Record<string, Entity> | undefined`), an active ID atom, and derived atoms for org/project scoping.

**Global store**: `export const store = createStore()` in `src/state/accessors.ts`.

## API Service Architecture

Three-layer design:
1. **ApiService** (`src/services/api.ts`) -- Base fetch wrapper with Bearer auth (Neon Auth session token), TanStack QueryClient caching, URL resolution from `TDSK_CADDY_PX_HOST` > `TDSK_PX_URL` > `TDSK_PX_HOST:TDSK_PX_PORT`
2. **BaseApi** -- Adds `_onError()` toast notification via Sonner
3. **Domain APIs** -- 29 entity-specific service classes extending BaseApi, all exported as singletons

Key services (29 total): `OrgsApi`, `AgentsApi` (+ SSE `.run()`), `SandboxApi` (CRUD + lifecycle: start, stop, connect, status, sessions), `AgentWSService` (WebSocket sessions), `SkillsApi`, `SchedulesApi`, `FilesApi`, `TokenRefresh`, `ProjectMembersApi`.

**Cache key pattern**: `all: [path]`, `list: [path, 'list']`, `detail: [path, 'detail', id]`. TanStack defaults: staleTime 5 min, gcTime 30 min, no retry, refetchOnWindowFocus off.

## Authentication

- `createAuthClient(TDSK_AUTH_URL)` from `@neondatabase/neon-js/auth`
- `AuthProvider` wraps app with `NeonAuthUIProvider`, calls `auth.session()` on mount
- Social login buttons (GitHub, GitLab, Google, Vercel) + `EmailLoginForm`
- Protected routes via `SignedIn`/`RedirectToSignIn` in `Layout.tsx`

## Action Pattern

- **API actions** (`actions/<domain>/api/`) -- Async: call service -> update Jotai state -> return response
- **Local actions** (`actions/<domain>/local/`) -- Sync: direct Jotai mutations (upsert, remove, set)
- Components call API actions which internally delegate to local actions after successful responses

22 action domains: agents, apiKeys, assets, auth, domains, endpoints, functions, messages, onboarding, orgs, profile, projectMembers, projects, providers, quotas, sandboxes, schedules, secrets, skills, subscriptions, threads, users.

## Navigation

**NavService** (`src/services/nav.ts`): `context()` builds nav context from Jotai state; `route(route, ctx?)` builds + navigates to parameterized route; `to()`, `is()`, `not()`, `has()`, `back()`, `home()`, `signin()` for navigation helpers.

**Sidebar** uses rail navigation with `RailNavSections` (Home, Org, Project) and `TSubNavGroup` groupings:
- **Org groups**: Resources (Projects, Sandboxes, Providers, Skills, Agents), Security (Secrets, API Keys, Domains), Management (Members, Schedules, Usage, Settings)
- **Project groups**: Development (Sandboxes, Endpoints, Functions, Agents), Security (Secrets, API Keys, Domains), Management (Members, Settings)

## Key Components

**Sandboxes**: Split into `OrgSandboxDrawer` (org-level management) and `ProjectSandboxDrawer` (project-level management) with accordion sub-components: `SandboxConfigAccordion`, `SandboxContainerAccordion`, `SandboxGuiAccordion`, `SandboxProviderAccordion`, `SandboxSkillsAccordion`. `ConnectModal` for SSH credentials + session management. Built-in sandboxes have restricted editing.

**ProjectWorkspace**: Project landing page with Quick Actions bar (Sandboxes, Endpoints, Functions, Agents), Sandboxes panel with runtime badges, Recent Threads placeholder.

**Agent Chat**: `useAgentChat` hook calls `agentsApi.run()` (SSE via `POST /_/orgs/:orgId/agents/:agentId/run`), processes event types: text, toolCallStart, toolCallArgs, toolResult, error, thread. `AgentWSService` provides WebSocket alternative.

**Skills/Schedules**: List views with create/edit/delete drawers. Org-scoped, accessible at `/orgs/:orgId/skills` and `/orgs/:orgId/schedules`, also as tabs under agent detail.

**GuiConfigForm**: Generative UI configuration form.

## Key Patterns

- **Action split**: Every domain has `api/` (async, calls service + updates state) and `local/` (sync, direct Jotai mutations).
- **Loaders for data loading**: React Router v7 loaders run before route renders; `criticalFetch` throws on error, `safeFetch` returns undefined.
- **Lazy loading**: All pages use `React.lazy()` wrapped by `SuspensePage` with `<Loading fixed full />` fallback. Pages must use default exports.
- **Template mustache syntax**: `Templates` service handles `{{variable}}` interpolation for secret/endpoint values.
- **Component co-location**: Each component has its own directory with sub-components and `index.ts` barrel. Styled components in `.styles.tsx` files using `styled()`.
- **Event handler naming**: Callbacks use `on` prefix: `onBlur`, `onDeleteClick`, `onSuccess`.
- **useAsyncAction**: Common hook wrapping async operations with `{ loading, error, run }` state.

## Environment Variables

Available in Admin (`src/constants/envs.ts`):

| Variable | Purpose |
|----------|---------|
| `TDSK_AUTH_URL` | Neon Auth API URL (required) |
| `TDSK_AUTH_PROVIDERS` | Comma-separated OAuth providers (default: `github`) |
| `TDSK_AD_APP_VERSION` | App version from package.json (required) |
| `TDSK_AD_BASE_PATH` | Base path for deployment (default `/`) |
| `TDSK_PX_URL` | Proxy URL |
| `TDSK_PX_HOST` / `TDSK_PX_PORT` | Proxy host/port |
| `TDSK_CADDY_PX_HOST` | Caddy proxy host (takes priority in apiUrl resolution) |
| `TDSK_BE_API_ADMIN_PATH` | Backend admin API path |
| `TDSK_POSTHOG_KEY` / `TDSK_POSTHOG_HOST` | PostHog analytics |
