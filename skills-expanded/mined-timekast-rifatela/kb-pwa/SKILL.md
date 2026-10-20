---
name: kb-pwa
description: Portable Progressive Web App patterns for Next.js App Router apps — managed Service Worker decision tree (Serwist vs next-pwa vs manual), update-available UX as a 3-option decision tree (silent / hybrid managed with safety guards / strict prompt), offline fallback strategy per resource type, VAPID push setup, and `beforeinstallprompt` deferred install. Use when choosing PWA strategy for a new app or auditing SW/update UX. For kit-shipped infra → `sk-pwa`.
last-verified: 2026-05-20
---

# kb-pwa — Portable PWA Patterns

> Pair: [`sk-pwa`](../sk-pwa/SKILL.md)

Portable Progressive Web App patterns for Next.js (App Router) apps. Stack-anchored but project-agnostic — no paths into `src/`, no references to specific components of this kit.

---

## 1. Managed Service Worker — decision tree

| Situation                                | Choose                   | Why                                                                |
| ---------------------------------------- | ------------------------ | ------------------------------------------------------------------ |
| Next.js **App Router** (13+), modern TS  | **Serwist**              | TS-first, App Router aware, Workbox-compatible, active maintenance |
| Next.js **Pages Router**, legacy project | `next-pwa`               | Still works for Pages Router; avoid for new App Router work        |
| Custom requirements (non-standard cache) | Manual SW + `register()` | Full control; only when Serwist strategies don't fit               |

Rule: don't hand-write a SW if a managed solution covers the case — you will leak cache bugs.

---

## 2. Update-available UX — managed update con decision tree

Cuando se instala un SW nuevo, el viejo sigue controlando tabs abiertas. Tres patrones, en orden de preferencia:

| Patrón                                                      | Comportamiento                                                                                                                                  | User impact                                                    | Cuándo                                                             |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Silent** (`skipWaiting:true` + `clientsClaim:true`)       | Takeover inmediato sin consultar                                                                                                                | Pierde state en tabs activas, rompe bundles mixtos             | ❌ Anti-pattern fuera de dev                                       |
| **Hybrid managed** (recomendado)                            | Auto-reload silencioso solo bajo guards verificables (cold-nav + página recién mounted + única tab + sin interacción). Cualquier fallo → toast. | UX óptimo en cold reopen, cero pérdida en escenarios activos   | ✅ Default para PWAs con mix mobile standalone + desktop multi-tab |
| **Strict prompt** (`skipWaiting:false` + toast obligatorio) | Toast "Recargar" siempre, usuario decide                                                                                                        | Cero riesgo de auto-reload accidental; fricción en cold reopen | Acceptable si la app tiene state crítico permanentemente activo    |

### Hybrid managed — pattern

1. Escuchar `registration.waiting` (mount, pathname change, `visibilitychange`, `window 'focus'`).
2. Cuando llega un waiting SW, evaluar 4 guards safe-by-fail:
   - **Cold navigation:** `performance.getEntriesByType('navigation')[0]?.type === 'navigate'` (excluye reload manual y back/forward).
   - **Página recién mounted:** `Date.now() - mountedAt < 5_000` ms.
   - **Única tab del origin:** mensaje al active SW con `MessageChannel` (timeout ~1.5s); responde `{ count: clients.length }`; requiere `count === 1`.
   - **Sin interacción:** listeners en **capture phase** sobre `window` para `pointerdown`/`click`/`touchstart`/`keydown`/`beforeinput`/`input`/`paste`/`compositionstart`; primer evento flipa el ref.
3. Si los 4 pasan: enganchar `controllerchange` → `window.location.reload()`; luego `postMessage({ type: 'SKIP_WAITING' })` al waiting SW.
4. Si cualquiera falla (o excepción, o loop guard activo): surface non-blocking prompt ("Nueva versión — Recargar"). On click: mismo `SKIP_WAITING` + reload por `controllerchange`.
5. **Loop guard:** `sessionStorage` flag con TTL ~5 min para prevenir reload loops si la activación falla a medias.
6. **Recovery:** todo el silent path envuelto en try/catch; cualquier error cae al toast.
7. **SW handler `COUNT_CLIENTS`:** `event.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) => port.postMessage({ count: clients.length })))`. En catch: `count: -1` → el cliente lo interpreta como `Infinity` → toast.

### Strict prompt — pattern

Saltar la evaluación de guards y mostrar siempre el prompt. Apto cuando el costo de un reload silencioso accidental supera el beneficio UX.

1. Listen for `registration.waiting` or a `controllerchange` / custom `message` event.
2. Surface a non-blocking UI affordance ("New version available — Reload").
3. On user action: `postMessage({ type: 'SKIP_WAITING' })` to the waiting worker → then `window.location.reload()`.

### Bootstrap deploy note

El primer deploy que ship el hybrid path ejercita todavía el flow anterior (los clientes corren la versión previa del componente, sin guards). Recién a partir del segundo deploy se activa el silent path. Inherente al SW upgrade cycle.

---

## 3. Offline strategy — per resource type

| Resource type                     | Strategy                     | Rationale                                               |
| --------------------------------- | ---------------------------- | ------------------------------------------------------- |
| HTML (pages)                      | **StaleWhileRevalidate**     | Instant render, refresh in background                   |
| Static assets (JS, CSS, fonts)    | **CacheFirst** (immutable)   | Hashed filenames, safe to cache long-term               |
| Images                            | CacheFirst (with expiry)     | Bandwidth-heavy, rarely change                          |
| API — public GETs                 | NetworkFirst + cache         | Prefer fresh, fall back to cache offline                |
| API — authenticated / mutations   | **NetworkOnly**              | Never cache auth-scoped or write responses              |
| API — sensitive data (PII, money) | **NetworkOnly**, no fallback | Stale financial/PII data is worse than an offline error |

Ship a dedicated **offline fallback page** for navigation requests that fail all strategies.

---

## 4. Web Push with VAPID

Setup:

1. Generate VAPID keypair once (`web-push generate-vapid-keys`). Store **private key server-side only**.
2. Expose **public key** via env (`NEXT_PUBLIC_VAPID_PUBLIC_KEY` — safe to ship to client).
3. Client subscribes via `registration.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey })`.
4. POST the `PushSubscription` JSON to a Route Handler → persist per-user.
5. Server sends push via `web-push` using the private key + stored subscription.

Payload shape (keep small, < 4KB):

```ts
type PushPayload = {
  title: string;
  body: string;
  url?: string; // deep link opened on notification click
  icon?: string; // absolute URL
  tag?: string; // collapses duplicates
};
```

SW `push` handler: `event.waitUntil(self.registration.showNotification(title, { body, data: { url } }))`.
SW `notificationclick` handler: focus existing client if URL matches, else `clients.openWindow(url)`.

---

## 5. Install prompt — deferred pattern

`beforeinstallprompt` fires once per session and **must be captured synchronously**, but triggering the prompt without user intent is rejected by browsers and hurts engagement.

Pattern:

1. Listen for `beforeinstallprompt` → `event.preventDefault()` → store the event reference.
2. Render an "Install" affordance (button, banner) only when the reference exists.
3. On user click: `savedEvent.prompt()` → await `savedEvent.userChoice`.
4. Track `dismissed` state per user (localStorage) to avoid nagging.
5. Listen for `appinstalled` to clear the affordance.

---

## 6. Feature-flag gating — skip in dev

Service Workers cache aggressively and break HMR / hot reload. Guard registration behind an env flag:

- `NEXT_PUBLIC_PWA_ENABLED=true` in production + preview deploys.
- Default off (or unset) in local dev to keep dev loop fast.
- Registration code: `if (process.env.NEXT_PUBLIC_PWA_ENABLED === 'true' && 'serviceWorker' in navigator) { ... }`.

---

## 7. Anti-patterns

```
❌ self.skipWaiting() unconditional o sin guards verificables (cold-nav, mounted recently, single-tab, no-interaction) → loses user work
❌ Registering the SW in dev → stale cache breaks HMR
❌ Caching authenticated API responses → data leaks across users
❌ Caching sensitive data (PII, money, permissions) with any fallback
❌ Shipping VAPID private key in client bundle → anyone can send push as you
❌ Calling beforeinstallprompt.prompt() without user gesture → silent reject
❌ Hand-rolling a SW when Serwist covers the case → reinvented bugs
❌ No offline fallback page → white screen on first navigation offline
```

---

Cross-reference: [`sk-pwa`](../sk-pwa/SKILL.md) — kit-shipped PWA infrastructure (Serwist config, install/update components, VAPID wiring). [`sk-features-index`](../sk-features-index/SKILL.md) — feature catalog (`NEXT_PUBLIC_PWA_ENABLED`).
