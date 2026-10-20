---
name: "react-web-navigation-state-guidelines"
description: "Next.js App Router (default) or React Router routing + React Query + AuthContext for React web: typed routes, hrefs, layouts, guards, screen registry, server/local/global state split. Use when wiring navigation and app state for a React web app."
version: 1
created: "2026-07-10"
updated: "2026-07-10"
---

# React Web Navigation & State Guidelines

## Navigation

### Next.js App Router (default for greenfield)
File structure:
```
app/
  layout.tsx           # root shell: QueryClientProvider + AuthProvider + Header + Nav
  <segment>/page.tsx   # one per route/screen
  <segment>/[id]/page.tsx
```
- Build routes from `design_source.screens[].route`/`file`.
- Navigate with `next/navigation`:
```tsx
import { useRouter } from 'next/navigation';
const router = useRouter();
router.push('/incidents/new');
router.replace(`/incidents/${ref}`);
router.back();
```
- `<Link href="…">` for declarative navigation; never `window.location` for in-app nav.
- Modals/overlays: route group `(modal)` or in-screen state; `onCancel` returns without an API call.
- Interactive screens are Client Components (`'use client'`); data-fetch shells can be Server Components.

### React Router fallback (Vite)
Use `react-router-dom` typed routes + `useNavigate`/`Link`, lazy routes with `React.lazy`/`Suspense`, only when the TSA/ADR specifies Vite instead of Next.js.

### Screen registry
Single source of truth `{ storyId, componentName, routePath, epic }` — every in-scope story appears; tests assert full coverage.

## State
- **Server state:** React Query (TanStack Query) for ALL API data (queries + mutations). No server data in Redux/Zustand.
- **Local UI state:** `useState`/`useReducer` within components.
- **Global/shared:** React Context (`AuthContext`, `ThemeContext`) for cross-cutting concerns; Redux Toolkit/Zustand only if the ADR mandates.
- One hook per operation in `lib/hooks/`; components never call the API client directly.

## Auth & session
- Access token attached via the single axios instance interceptor (`Authorization: Bearer`); 401 → refresh → retry, else redirect to login.
- Token stored in httpOnly cookie or in-memory — **never** `localStorage`. Only `NEXT_PUBLIC_*` (Next) / `VITE_*` (Vite) values reach the browser; never secrets.

## Anti-patterns
- Untyped route strings scattered across components (centralize hrefs / registry).
- Raw `fetch`/`axios` in components instead of a typed hook.
- Navigating away on cancel of a destructive action before its confirm gate.
- Server data cached in Redux/Zustand instead of React Query.
