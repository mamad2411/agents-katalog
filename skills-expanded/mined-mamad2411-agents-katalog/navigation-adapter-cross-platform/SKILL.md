---
name: navigation-adapter-cross-platform
description: NavigationAdapter in each app's platform layer lets shared view code call useNavigation().push() without importing next/navigation or react-router-dom.
category: architecture
version: 1.0.0
tags: [routing, navigation, cross-platform, nextjs, react-router, electron]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Monorepo with ≥2 frontend apps (web Next.js + desktop Electron, say) sharing view packages.
- You want shared views to call `useNavigation().push('/issues')` without knowing which framework is on the other side.

## Steps

1. Define the contract in a shared package (core or views):
   ```ts
   // packages/core/navigation/context.ts
   export interface NavigationAPI {
     push(path: string): void;
     replace(path: string): void;
     back(): void;
     pathname(): string;
   }
   const NavigationContext = createContext<NavigationAPI | null>(null);
   export function NavigationProvider({ value, children }: { value: NavigationAPI; children: ReactNode }) {
     return <NavigationContext.Provider value={value}>{children}</NavigationContext.Provider>;
   }
   export function useNavigation(): NavigationAPI {
     const ctx = useContext(NavigationContext);
     if (!ctx) throw new Error("useNavigation must be inside NavigationProvider");
     return ctx;
   }
   ```
2. Web app implements the adapter using Next.js APIs:
   ```ts
   // apps/web/platform/navigation.tsx
   import { useRouter, usePathname } from "next/navigation";
   export function WebNavigationAdapter({ children }: { children: ReactNode }) {
     const router = useRouter();
     const pathname = usePathname();
     const value: NavigationAPI = useMemo(() => ({
       push: (p) => router.push(p),
       replace: (p) => router.replace(p),
       back: () => router.back(),
       pathname: () => pathname,
     }), [router, pathname]);
     return <NavigationProvider value={value}>{children}</NavigationProvider>;
   }
   ```
3. Desktop app implements using react-router-dom:
   ```ts
   // apps/desktop/src/renderer/src/platform/navigation.tsx
   import { useNavigate, useLocation } from "react-router-dom";
   export function DesktopNavigationAdapter({ children }: { children: ReactNode }) {
     const nav = useNavigate();
     const loc = useLocation();
     const value = useMemo(() => ({
       push: nav,
       replace: (p: string) => nav(p, { replace: true }),
       back: () => nav(-1),
       pathname: () => loc.pathname,
     }), [nav, loc]);
     return <NavigationProvider value={value}>{children}</NavigationProvider>;
   }
   ```
4. Wrap each app's root with its adapter. Shared views consume `useNavigation()` and never import `next/*` or `react-router-dom`.
5. For workspace-aware routing, the adapter is the right place to auto-prepend the current slug:
   ```ts
   push: (p) => router.push(p.startsWith('/') ? `/${currentSlug}${p}` : p),
   ```

## Example

```tsx
// packages/views/issues/IssueRow.tsx — framework-agnostic
function IssueRow({ issue }) {
  const nav = useNavigation();
  return <button onClick={() => nav.push(`/issues/${issue.id}`)}>{issue.title}</button>;
}
```

## Caveats

- The adapter contract should stay small. If you find yourself adding framework-specific primitives (`searchParams`, SSR-only helpers), push them into the app layer instead.
- Desktop adapter should detect "cross-workspace push" (path starts with a different slug) and translate into open-new-tab or switch-workspace semantics, rather than a plain navigate in the current tab.
- Don't bypass the adapter with ad-hoc `window.history.pushState` — cross-platform invariants break silently.
