---
name: frontend-pwa-workbox
description: Use when building a PWA with Workbox — caching strategies, service worker lifecycle, manifest, install prompt, offline fallback, update flow.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [react, typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [react, typescript, ts-vite, frontend-tanstack-query, frontend-msw, ux-essentials, ux-wcag-a11y]
---

# PWA with Workbox

**Iron Law: never cache responses that carry auth (`Authorization` header, session cookie) with `CacheFirst` or `StaleWhileRevalidate`. The cache has no identity scope — a logged-out user can read another user's last response. Auth-bearing routes are `NetworkOnly` or explicitly versioned per-user.**

**Versions:** Current `Workbox 7.3` · `vite-plugin-pwa 0.21` · No LTS series — _Workbox 7 is the only supported major; v6 reached EOL. `vite-plugin-pwa` is the canonical integration for Vite projects. Always pin both — minor bumps occasionally swap precache manifest hashing._

## Service worker lifecycle (the three states that matter)

```
register → install → waiting → activate → fetch
                       ↑                     ↓
                  new SW arrives        controls page
```

| Phase      | Trigger                                         | What runs                                            | Page already loaded?                  |
| ---------- | ----------------------------------------------- | ---------------------------------------------------- | ------------------------------------- |
| `install`  | first visit or new SW found                     | precache assets via `self.skipWaiting()` if you want | No — old SW (if any) still in control |
| `waiting`  | install done, old SW still controls open tabs   | nothing                                              | Old SW serves fetches                 |
| `activate` | all old tabs closed OR `clients.claim()` called | cleanup old caches                                   | New SW now controls                   |
| `fetch`    | any request from a controlled page              | strategy handler runs                                | Yes                                   |

**The default behavior (no `skipWaiting`):** the new SW waits until every tab is closed before activating. Users with the app pinned in a tab will run the old SW forever. Decide deliberately — see Update flow below.

## Caching strategies — when to use which

| Strategy               | Use for                                                                   | Don't use for                     |
| ---------------------- | ------------------------------------------------------------------------- | --------------------------------- |
| `CacheFirst`           | Hashed assets (`/assets/app-9f8a.js`), fonts, immutable images            | HTML, anything that changes       |
| `NetworkFirst`         | API JSON where freshness matters but offline-tolerant is OK; `index.html` | Auth-bearing user-data routes     |
| `StaleWhileRevalidate` | Avatar images, public list endpoints that are OK slightly stale           | Auth-bearing routes; payment data |
| `NetworkOnly`          | Auth, mutations (`POST`/`PUT`/`DELETE`), real-time                        | Static assets                     |
| `CacheOnly`            | Pre-warmed dictionaries, offline-only data                                | Anything that changes             |

**Rule of thumb:** if the URL has a hash in it, `CacheFirst`. If it returns JSON, `NetworkFirst` with a short cache window. If it carries credentials, `NetworkOnly`.

## Vite setup (`vite-plugin-pwa`)

```ts
// vite.config.ts
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "prompt", // 'autoUpdate' = silent; 'prompt' = ask user
      injectRegister: "auto",
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.example\.com\/public\//,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-public",
              networkTimeoutSeconds: 3,
              expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 },
            },
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/private"),
            handler: "NetworkOnly", // auth-bearing — never cache
          },
        ],
      },
      manifest: {
        name: "MyApp",
        short_name: "MyApp",
        description: "Short description",
        start_url: "/",
        display: "standalone",
        theme_color: "#0f172a",
        background_color: "#ffffff",
        icons: [
          { src: "/icons/192.png", sizes: "192x192", type: "image/png" },
          { src: "/icons/512.png", sizes: "512x512", type: "image/png" },
          { src: "/icons/512-maskable.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
        ],
      },
    }),
  ],
});
```

**Precache vs runtime cache:** precache = `globPatterns` ships with the SW manifest and installs on first load (versioned per build hash). Runtime cache = `runtimeCaching` handlers populate caches lazily on first fetch.

## Install prompt (the deferred pattern)

The browser fires `beforeinstallprompt` _exactly once_ per visit when criteria are met. You must capture and defer it — calling `prompt()` outside a user gesture is silently rejected.

```ts
// app/installPrompt.ts
let deferred: BeforeInstallPromptEvent | null = null;

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferred = e as BeforeInstallPromptEvent;
  // tell your UI to show an "Install" button
  window.dispatchEvent(new Event("pwa-installable"));
});

export async function triggerInstall(): Promise<"accepted" | "dismissed" | "unavailable"> {
  if (!deferred) return "unavailable";
  await deferred.prompt();
  const { outcome } = await deferred.userChoice;
  deferred = null;
  return outcome;
}
```

In React: a button onClick calls `triggerInstall()`. Never call it on mount. iOS Safari never fires `beforeinstallprompt` — show platform-specific instructions ("Share → Add to Home Screen") instead.

## Update flow (the UX trap)

| Approach                                                       | UX                                                      | When                                                           |
| -------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------- |
| `registerType: 'autoUpdate'` + `skipWaiting` + `clients.claim` | Page silently swaps SW; on next nav user sees new build | Read-only content (docs, marketing)                            |
| `registerType: 'prompt'` → show "Update available" toast       | User clicks Reload → new SW takes over                  | App with in-progress work (forms, editor)                      |
| No skipWaiting, no prompt                                      | New SW lies dormant until all tabs close                | Bad — users on a single pinned tab run stale code indefinitely |

**Use `prompt`** for apps with in-flight content (rich-text editors, forms) — silent auto-update mid-edit would lose state. Use `autoUpdate` only for read-only content.

```ts
// app/registerSW.ts (vite-plugin-pwa generates this hook)
import { useRegisterSW } from "virtual:pwa-register/react";

const { needRefresh, updateServiceWorker } = useRegisterSW();
// render a toast when needRefresh[0] is true; onClick calls updateServiceWorker(true)
```

## Offline fallback

```ts
// in vite.config.ts workbox block
workbox: {
  navigateFallback: "/offline.html",
  navigateFallbackDenylist: [/^\/api\//, /^\/auth\//],
}
```

Ship a hand-written `public/offline.html` (no JS dependencies). It's the page shown when the user navigates and the network + cache both miss.

## Versioning + cache busting

- Precache automatically versions (file hashes in the manifest). New build → new SW → old caches deleted on activate.
- Runtime caches need explicit cleanup. Bump `cacheName` (`"api-public-v2"`) when the response shape changes — old entries linger otherwise.
- `expiration: { maxAgeSeconds }` is a _soft_ hint — entries can survive longer if the cache isn't pressured. Don't rely on it for security.

## Anti-patterns

- **`StaleWhileRevalidate` on a logged-in user endpoint.** Different user on same device sees stale private data. Hard fail.
- **Caching `Authorization`-header responses.** Same problem. `NetworkOnly` is the only safe choice.
- **`skipWaiting` + `clients.claim` everywhere "for snappier updates".** Loses in-flight form state. Decide per app.
- **No SW update prompt at all.** Users run the version they first installed for months.
- **Forgetting the manifest `start_url`.** Installed app launches at whatever URL was open at install time; bookmarks break.
- **No 512×512 maskable icon.** Android crops your icon weirdly.
- **Testing the SW only in dev.** Vite dev mode disables SW by default. Test with `vite build && vite preview`.
- **Caching API responses without `expiration`.** Cache grows unbounded; some browsers evict the whole origin.
- **Asserting `'serviceWorker' in navigator` once and trusting it.** Safari private mode lies. Wrap registration in try/catch.

## Red flags

| Thought                                   | Reality                                                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| "I'll cache everything for snappiness"    | You just leaked another user's data when they log in on the same browser.                                           |
| "Auto-update is fine, users won't notice" | The user halfway through writing a report will.                                                                     |
| "Workbox handles auth caching for me"     | It does not. You decide which URL patterns are safe.                                                                |
| "The install prompt isn't firing"         | iOS Safari never fires it. Chrome only fires once per session and only if criteria are met. Show a manual fallback. |
| "I'll debug the SW in dev mode"           | `vite-plugin-pwa` disables SW in dev by default. Use `vite build && vite preview`.                                  |

## Hand-off

For build setup and Vite plugin config: `Skill(ts-vite)`. For React-side update toast UI: `Skill(react)`. For API mocking the SW during tests: `Skill(frontend-msw)`. For server-state caching (independent of SW): `Skill(frontend-tanstack-query)`. For installability and a11y of the install button: `Skill(ux-wcag-a11y)`.
