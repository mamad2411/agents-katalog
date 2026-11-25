---
name: electron-platform-services-injection
description: Inject a PlatformServices facade (image processing, shell env, keychain, badge updates, error capture) into shared server-core code so the SAME RPC handler file runs unchanged in Electron main AND a headless Bun server.
category: electron
version: 1.0.0
version_origin: extracted
tags: [electron, platform-abstraction, dependency-injection, headless]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/server-core/src/services
imported_at: 2026-04-18T00:00:00Z
---

# Inject PlatformServices into shared server-core

## When to use
- You factored a server-core package out of your Electron app so it can also run headless.
- server-core handlers still need some "platform" behaviors - image resize, shell-env loading, OS notifications, native image cache.
- Want to avoid `if (isElectron)` branches inside server-core.

## How it works
1. Define a `PlatformServices` interface in server-core with every OS/runtime-dependent capability the handlers need:
   ```ts
   interface PlatformServices {
     imageProcessor: ImageProcessor;        // sharp or native electron image
     captureError?: (e: Error) => void;     // Sentry in Electron, console in headless
     updateBadgeCount: (n: number) => void; // dock badge, no-op in headless
     openExternal: (url: string) => void;   // shell.openExternal or xdg-open
   }
   ```
2. server-core exposes setter functions: `setSearchPlatform(p)`, `setImageProcessor(ip)`, `setSessionRuntimeHooks(hooks)`. These store into module-level `let` variables and default to no-op fallbacks.
3. At bootstrap, the app implementation passes its platform in:
   ```ts
   applyPlatformToSubsystems: (p) => {
     setFetcherPlatform(p); setSessionPlatform(p);
     setSessionRuntimeHooks({ updateBadgeCount: p.updateBadgeCount, captureException: p.captureError ?? (() => {}) });
     setSearchPlatform(p); setImageProcessor(p.imageProcessor);
   }
   ```
4. Electron main builds its `createElectronPlatform()` using `app.badge`, `nativeImage`, Sentry, `shell`.
5. Headless server builds a `createHeadlessPlatform()` that uses `sharp` for images, `console.error` for errors, no-ops for badges.
6. Handler code does `getImageProcessor().resize(buffer)` without caring which one it got.

## Example
```ts
// In server-core/src/services/index.ts
let imageProcessor: ImageProcessor = DEFAULT_NOOP;
export function setImageProcessor(ip: ImageProcessor) { imageProcessor = ip; }
export function getImageProcessor() { return imageProcessor; }

// In apps/electron/src/main/platform.ts
import sharp from 'sharp';
export const createElectronPlatform = (): PlatformServices => ({
  imageProcessor: { resize: async (buf, w, h) => sharp(buf).resize(w, h).toBuffer() },
  captureError: Sentry.captureException,
  updateBadgeCount: (n) => app.dock?.setBadge(n ? String(n) : ''),
  openExternal: shell.openExternal,
});
```

## Gotchas
- Default every setter to a safe no-op so forgetting to inject doesn't crash handlers.
- Keep PlatformServices SMALL - every method is a maintenance liability across the two implementations.
- Capture-error should never throw (it's on the error path); wrap any Sentry call in try/catch.
- Tests should use a `createMockPlatform()` that records calls so you can assert behavior without touching OS APIs.
- Resist the urge to make platform services async where sync would do - it ripples through handler signatures.
