---
name: vite-spa
description: Vite + React Router SPA conventions, as an alternative to Next.js App Router for projects using a Vite single-page app with a separate API. Covers routing, persona-based code-splitting, guard components, Vitest-in-Vite-config, and a shared HTTP client. Use when the project has a vite.config.ts and no app/ or pages/ directory.
---

Apply the following conventions to Vite SPA projects (`react-router-dom`, no Next.js). Check `package.json` first — if `next` is a dependency, use the App Router conventions instead; this skill is for the Vite path only.

## Routing (react-router-dom, not file-based)

There is no file-system router here — routes are declared explicitly, typically in one `AppRoutes.tsx`:

```tsx
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';

const AppRoutes = () => (
  <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route element={<RequireAuth />}>
      <Route path="/dashboard" element={<DashboardLayout />}>
        <Route index element={<DashboardHome />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Route>
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
);
```

`<Outlet />` in a layout route renders the matched child — the same composition pattern as a Next.js layout, but explicit rather than folder-derived.

## Guard components

Auth and capability checks are wrapped route elements, not per-page `if` checks. A guard reads context/state, and either renders `<Outlet />` (continue to the matched children) or redirects:

```tsx
const RequireAuth = () => {
  const { user, isLoading } = useAuth();
  if (isLoading) return <FullPageSpinner />;
  if (!user) return <Navigate to="/login" replace />;
  return <Outlet />;
};

const RequireRole = ({ role }: { role: string }) => {
  const { user } = useAuth();
  if (!user?.roles.includes(role)) return <Navigate to="/dashboard" replace />;
  return <Outlet />;
};
```

Nest guards to compose requirements (`<RequireAuth>` wrapping `<RequireRole role="admin">`). Never gate on a client-only check without also enforcing the same rule server-side — a guard is UX, not the security boundary.

## Persona-based code-splitting

An anonymous or public visitor must never download the JS for authenticated-only routes. Split at the route-subtree boundary with `React.lazy` + `Suspense`, not per-component:

```tsx
const AdminDashboard = lazy(() => import('./features/admin/AdminDashboard'));
const MemberDashboard = lazy(() => import('./features/member/MemberDashboard'));

<Route
  path="/admin/*"
  element={
    <Suspense fallback={<FullPageSpinner />}>
      <AdminDashboard />
    </Suspense>
  }
/>;
```

Rule of thumb: lazy-load at the level of "does this persona ever see this subtree" — a public marketing route, an authenticated dashboard, and an admin-only area are three separate chunks. Don't lazy-load individual buttons or small leaf components; the `Suspense` fallback flicker isn't worth it below the route level.

## Vitest lives inside `vite.config.ts`

There is no separate `vitest.config.ts` — the `test` key nests inside the same `defineConfig` call that configures Vite itself, so both share plugins (notably `@vitejs/plugin-react`) and path aliases automatically:

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': '/src' } },
  test: {
    environment: 'jsdom',
    setupFiles: './src/test-utils/setup.ts',
    globals: true,
  },
});
```

If a project *does* have a separate `vitest.config.ts`, that's usually a sign the Vite config's plugins/aliases got out of sync with the test config — prefer merging them back into one file unless there's a documented reason (e.g. a different plugin set for tests) not to.

## State: don't assume a library that isn't there

Plain React Context is a legitimate, idiomatic default for auth/session state in a Vite SPA — it doesn't need Redux, Zustand, or any other store to be "correct." Before reaching for a data-fetching or state library, check what's actually installed (`package.json` dependencies) rather than porting patterns from a different stack:

- No `@tanstack/react-query` in `package.json` → don't introduce it for a single feature; use `useState`/`useEffect` with the shared HTTP client below, or ask before adding a new dependency.
- An `AuthContext` + `useAuth()` hook, backed by `useState`/`useReducer` and a `useEffect` that syncs to `localStorage`/a cookie, is enough for session state in most SPAs this size.

## Shared HTTP client, not ad-hoc `fetch`

One configured client module — not `fetch()` calls scattered through components — owns the base URL, auth header, and global error handling:

```ts
// src/lib/apiClient.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

const request = async <T>(path: string, init?: RequestInit): Promise<T> => {
  const token = getStoredToken();
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
  });

  if (res.status === 401) {
    clearStoredToken();
    window.location.assign('/login');
    throw new ApiError(401, 'Unauthorized');
  }
  if (!res.ok) throw new ApiError(res.status, await res.text());
  return res.json() as Promise<T>;
};

export const apiClient = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(body) }),
};
```

Every feature imports `apiClient`, never calls `fetch` directly — that's what makes the 401 handler, base URL, and auth header a single edit instead of a grep-and-replace across the app. Vite exposes env vars via `import.meta.env`, and only `VITE_`-prefixed ones reach the client bundle (the same client/server split concern as `NEXT_PUBLIC_`, enforced by the bundler instead of by convention).
