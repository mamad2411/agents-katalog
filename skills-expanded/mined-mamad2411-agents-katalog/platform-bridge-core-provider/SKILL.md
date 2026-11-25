---
name: platform-bridge-core-provider
description: Single CoreProvider in the shared packages layer initializes API client, auth/workspace stores, WS connection, and QueryClient — each app wraps its root and injects platform adapters.
category: architecture
version: 1.0.0
tags: [react, provider, cross-platform, bootstrap, monorepo]
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

- Monorepo with multiple frontend apps (web + desktop + mobile) sharing business logic.
- Each app needs the same bootstrap order (API → auth → workspace → WS → queries) but has different framework-specific wiring.

## Steps

1. In `packages/core/platform/core-provider.tsx`, own the bootstrap sequence:
   ```tsx
   export function CoreProvider({
     storageAdapter,
     navigationAdapter,
     apiBaseUrl,
     wsBaseUrl,
     cookieAuth,
     children,
   }: CoreProviderProps) {
     // 1. API client + auth store
     const api = useMemo(() => createApiClient({ baseUrl: apiBaseUrl, storage: storageAdapter }), []);
     const authStore = useMemo(() => createAuthStore({ api, storage: storageAdapter }), []);
     // 2. Workspace store
     const workspaceStore = useMemo(() => createWorkspaceStore({ api, storage: storageAdapter }), []);
     // 3. QueryClient
     const qc = useMemo(() => createQueryClient(), []);
     // 4. WS client (depends on auth)
     const wsClient = useMemo(() => new WSClient(wsBaseUrl, { cookieAuth }), []);
     return (
       <QueryClientProvider client={qc}>
         <WSProvider ws={wsClient} auth={authStore} workspace={workspaceStore}>
           <NavigationProvider value={navigationAdapter}>
             <StorageProvider value={storageAdapter}>
               {children}
             </StorageProvider>
           </NavigationProvider>
         </WSProvider>
       </QueryClientProvider>
     );
   }
   ```
2. Each app wraps with its platform adapters:
   ```tsx
   // apps/web/app/layout.tsx
   export default function RootLayout({ children }) {
     return (
       <html>
         <body>
           <CoreProvider
             storageAdapter={browserStorageAdapter}
             navigationAdapter={webNavigationAdapter}
             apiBaseUrl={process.env.NEXT_PUBLIC_API_URL!}
             wsBaseUrl={process.env.NEXT_PUBLIC_WS_URL!}
             cookieAuth={true}
           >
             {children}
           </CoreProvider>
         </body>
       </html>
     );
   }
   ```
3. Apps never touch `QueryClient`, `WSClient`, or the auth/workspace stores directly — they consume them through the hooks the core package exposes.
4. Test harness wraps with `CoreProvider` using in-memory storage and a no-op navigation adapter.

## Example

Add a new platform (mobile React Native):
- Implement `rnStorageAdapter` (AsyncStorage-backed) and `rnNavigationAdapter` (React Navigation).
- Wrap app root with `<CoreProvider storageAdapter={rnStorageAdapter} ... />`.
- Everything else — queries, mutations, WS events, workspace switching — works.

## Caveats

- Adapters must be stable references (pass memoized instances, not inline objects) or every render tears down and rebuilds the core stack.
- Bootstrapping order matters: API before auth (auth uses API); auth before workspace (workspace depends on auth); QueryClient before WS (WS invalidates queries). Changing order breaks things subtly.
- This provider is where "the platform ends and the app logic begins" — resist adding app-specific bootstrapping here.
