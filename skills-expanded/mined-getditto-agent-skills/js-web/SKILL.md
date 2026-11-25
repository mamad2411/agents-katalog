---
name: js-web
description: >
  Integrates Ditto in browser JavaScript/TypeScript and React websites, including Vite and client-only Next.js boundaries. Covers WASM assets, in-memory storage, WebSockets, provider lifetimes and browser verification. Not Node or native setup.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Ditto in browsers and React websites

Use [js-sdk](../js-sdk/SKILL.md) for common APIs. **Browser storage is memory-only**:
closing/reloading loses unsynchronized local data. Do not promise IndexedDB, persistent
PWA offline relaunch, or native mesh radios. Sync uses WebSockets.

## Workflow

1. Inspect the framework, package manager and SDK lockfile. Use the browser entry from
   `@dittolive/ditto`; never import the Node `.node` entry into a client bundle.
2. Serve **the exact installed package's** `web/ditto.wasm` from your static assets.
   Pass its public URL in `initOptions: { webAssemblyModule: wasmURL }` to the shared
   runtime. Honor deployment base paths. Check MIME `application/wasm`, CORS for a
   different origin, cache versioning, compression and the deployment's WASM CSP policy.
3. Create one [runtime](../js-sdk/assets/runtime.ts) outside render. Mount
   [DittoProvider](../js-sdk/assets/DittoProvider.tsx) above routing. Provide loading and
   error UI; startup may include a WASM download. Keep context independent of DOM APIs
   so the same provider can be used by React Native.
4. Use useDittoQuery with a stable decoder and memoized arguments. Use separate broader
   app subscriptions for complex local queries. Use document IDs for React keys.
   Writes are local promises, not HTTP requests; show their failures and local success.
5. Production auth obtains a fresh user token through a backend. VITE_/NEXT_PUBLIC_
   variables are public client data. Use the supplied server URL; do not synthesize it.
6. Test Strict Mode, route remount, filter/account changes, failed WASM loading,
   network loss/reconnect, and reload data loss. Verify a production build with its
   actual base path, not only the development server.

## SSR and framework boundaries

Next.js: use a client boundary and import/load Ditto only in the browser after mount;
`'use client'` alone does not guarantee imported modules avoid server evaluation.
A dynamic import inside the client startup path or a client component loaded with
SSR disabled can isolate WASM initialization. Never create a global server instance
that accidentally shares a browser user's data across requests. Preserve loading UI
through hydration. The SDK is a local store, not a React Server Component data cache.

For Vite, copy version-matched WASM into public assets or resolve an imported asset URL.
The [browser fixture](references/browser-fixture.md) demonstrates the shared runtime,
provider, query updates and teardown against real WASM. It is a test shell, not a
complete production auth implementation. A tab refresh is a new memory store.

## Verification

The browser test drives real Chromium/WASM and React Strict Mode. Local query success
is distinct from remote sync; check an authenticated second peer for the latter.
Node-only tests cannot establish browser storage or WASM delivery behavior.

Sources: <https://docs.ditto.live/sdk/latest/install-guides/js>,
<https://docs.ditto.live/sdk/latest/compatibility/js-web>,
<https://react.dev/reference/react/StrictMode>.
