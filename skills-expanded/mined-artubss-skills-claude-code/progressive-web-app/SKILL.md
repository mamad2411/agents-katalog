---
name: progressive-web-app
description: "Construa Progressive Web Apps (PWAs) com suporte offline, instalabilidade e estratégias de cache. Dispare sempre que o usuário mencionar PWA, service workers, manifesto de app web, Workbox, 'adicionar à tela inicial' ou quiser que seu app web funcione offline, pareça nativo ou seja instalável."
risk: safe
source: community
date_added: "2026-03-17"
tags: [pwa, web-dev, service-worker, frontend, offline, caching]
tools: [gemini, cursor, claude]
---

# Progressive Web Apps (PWAs)

## Visão Geral

Um Progressive Web App é uma aplicação web que usa recursos modernos do navegador para entregar uma experiência rápida, confiável e instalável — mesmo em redes instáveis. Os três pilares obrigatórios são:

1. **HTTPS** — Obrigatório em produção para registrar service workers (localhost é isento para desenvolvimento).
2. **Web App Manifest** (`manifest.json`) — Torna o app instalável e define sua aparência na tela inicial do dispositivo.
3. **Service Worker** (`sw.js`) — Um script de background que intercepta requisições de rede, gerencia caches e habilita funcionalidade offline.

## Quando Usar Esta Habilidade

- Use quando o usuário quiser que seu app web funcione offline ou em redes instáveis.
- Use ao construir um projeto web mobile-first onde usuários devem conseguir instalar o app na tela inicial.
- Use quando o usuário perguntar sobre estratégias de cache, service workers ou melhorar performance e resiliência do app web.
- Use quando o usuário mencionar Workbox, manifesto de app web, sincronização em background ou notificações push para a web.
- Use quando o usuário perguntar "meu website pode ser instalado como um app?" ou "como faço meu site funcionar offline?" — mesmo que não use a palavra PWA.

## Checklist de Entregas

Toda implementação de PWA deve incluir, no mínimo, estes arquivos:

- [ ] `index.html` — Vincula manifest, registra service worker
- [ ] `manifest.json` — Metadados completos do app e conjunto de ícones
- [ ] `sw.js` — Service worker com handlers install, activate e fetch
- [ ] `app.js` — Lógica principal do app com registro do SW e tratamento do prompt de instalação
- [ ] `offline.html` — Página de fallback exibida quando a navegação falha offline (obrigatória — arquivo ausente causará falha na instalação)

---

## Etapa 1: Web App Manifest (`manifest.json`)

Define como o app aparece quando instalado. Deve ser vinculado de `<head>` via `<link rel="manifest">`.

```json
{
  "name": "My Awesome PWA",
  "short_name": "MyPWA",
  "description": "A fast, offline-capable Progressive Web App.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#ffffff",
  "theme_color": "#0055ff",
  "icons": [
    {
      "src": "/assets/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/assets/screenshots/desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

**Campos-chave:**
- `display`: `standalone` oculta a UI do navegador; `minimal-ui` mostra controles mínimos; `browser` é a aba padrão.
- `purpose: "maskable"` em ícones habilita ícones adaptativos no Android (a zona segura importa — mantenha o conteúdo no centro 80%).
- `screenshots` é opcional mas obrigatório para o diálogo de instalação aprimorado do Chrome em desktop.

---

## Etapa 2: Shell HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Awesome PWA</title>

  <!-- PWA manifest -->
  <link rel="manifest" href="/manifest.json">

  <!-- Theme color for browser chrome -->
  <meta name="theme-color" content="#0055ff">

  <!-- iOS-specific (Safari doesn't fully use manifest) -->
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="MyPWA">
  <link rel="apple-touch-icon" href="/assets/icons/icon-192x192.png">

  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <div id="app">
    <header><h1>My PWA</h1></header>
    <main id="content">Loading...</main>
    <!-- Optional: install button, hidden by default -->
    <button id="install-btn" hidden>Install App</button>
  </div>
  <script src="/app.js"></script>
</body>
</html>
```

---

## Etapa 3: Registro do Service Worker e Prompt de Instalação (`app.js`)

```javascript
// ─── Service Worker Registration ───────────────────────────────────────────
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('[App] SW registered, scope:', registration.scope);
    } catch (err) {
      console.error('[App] SW registration failed:', err);
    }
  });
}

// ─── Install Prompt (Add to Home Screen) ───────────────────────────────────
let deferredPrompt;
const installBtn = document.getElementById('install-btn'); // may be null if omitted

// Capture the browser's install prompt — it fires before the browser's own UI
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault(); // Stop automatic mini-infobar on mobile
  deferredPrompt = e;
  if (installBtn) installBtn.hidden = false; // Show your custom install button
});

if (installBtn) {
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log('[App] Install outcome:', outcome);
    deferredPrompt = null;
    installBtn.hidden = true;
  });
}
// Fires when the app is installed (via browser or your button)
window.addEventListener('appinstalled', () => {
  console.log('[App] PWA installed successfully');
  installBtn.hidden = true;
});
```

---

## Etapa 4: Service Worker (`sw.js`)

### Versionamento de Cache (crítico — sempre incremente ao fazer deploy)

```javascript
const CACHE_VERSION = 'v1';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;

// Files to pre-cache during install (the "App Shell")
const APP_SHELL = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/assets/icons/icon-192x192.png',
  '/offline.html', // Fallback page shown when network is unavailable
];
```

### Install — Pré-cache do App Shell

```javascript
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      console.log('[SW] Pre-caching app shell');
      return cache.addAll(APP_SHELL);
    })
  );
  // Activate immediately without waiting for old SW to die
  self.skipWaiting();
});
```

### Activate — Limpeza de Caches Antigos

```javascript
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
          .map((name) => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    })
  );
  // Take control of all pages immediately
  self.clients.claim();
});
```

### Fetch — Estratégias de Cache

Escolha a estratégia certa por tipo de recurso:

```javascript
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle GET requests from our own origin
  if (request.method !== 'GET' || url.origin !== location.origin) return;

  // Strategy A: Cache-First (for static assets — fast, tolerates stale)
  if (url.pathname.match(/\.(css|js|png|jpg|svg|woff2)$/)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // Strategy B: Network-First (for HTML pages — fresh, falls back to cache)
  if (request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Strategy C: Stale-While-Revalidate (for API data — fast and eventually fresh)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(staleWhileRevalidate(request));
    return;
  }
});

// ─── Strategy Implementations ──────────────────────────────────────────────

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    const cache = await caches.open(STATIC_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch {
    // Nothing useful to fall back to for assets
    return new Response('Asset unavailable offline', { status: 503 });
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(DYNAMIC_CACHE);
    cache.put(request, response.clone());
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || caches.match('/offline.html');
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cached = await cache.match(request);
  const fetchPromise = fetch(request).then((response) => {
    cache.put(request, response.clone());
    return response;
  });
  return cached || fetchPromise;
}
```

---

## Casos Extremos e Notas de Plataforma

### Particularidades do iOS / Safari
- Safari suporta manifests e service workers, mas **não suporta `beforeinstallprompt`** — usuários devem instalar manualmente via menu Compartilhar → "Adicionar à Tela Inicial".
- Use as meta tags `apple-mobile-web-app-*` (mostradas em `index.html` acima) para integração adequada com iOS.
- Safari pode limpar caches de service worker após ~7 dias de inatividade (Intelligent Tracking Prevention).

### Requisito HTTPS
- Service workers só registram em origens `https://`. `http://localhost` é a única exceção para desenvolvimento.
- Use uma ferramenta como `mkcert` ou `ngrok` se precisar de HTTPS localmente com um hostname customizado.

### Cache-Busting ao Fazer Deploy
- Sempre incremente `CACHE_VERSION` em `sw.js` ao fazer deploy de novos assets. Isso garante que o activate limpe caches antigos e usuários obtenham arquivos frescos.
- Um padrão comum é injetar a versão automaticamente via sua ferramenta de build (ex: Vite, Webpack).

### Respostas Opacas (requisições cross-origin)
- Requisições para origens externas (ex: CDN de fontes, APIs de terceiros) retornam respostas "opacas" que não podem ser inspecionadas. Faça cache delas com cuidado — uma resposta opaca falhada ainda recebe status `200`.
- Prefira `staleWhileRevalidate` para recursos cross-origin, ou use uma biblioteca como Workbox que trata isso com segurança.

---

## Workbox (Opcional: Atalho para Produção)

Para apps em produção, considere [Workbox](https://developer.chrome.com/docs/workbox) (biblioteca PWA do Google) em vez de implementar estratégias manualmente. Ela trata casos extremos, expiração de cache e versionamento automaticamente.

```javascript
// With Workbox (via CDN for simplicity — use npm + bundler in production)
importScripts('https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js');

const { registerRoute } = workbox.routing;
const { CacheFirst, NetworkFirst, StaleWhileRevalidate } = workbox.strategies;
const { precacheAndRoute } = workbox.precaching;

precacheAndRoute(self.__WB_MANIFEST || []); // Injected by build plugin

registerRoute(({ request }) => request.destination === 'image', new CacheFirst());
registerRoute(({ request }) => request.mode === 'navigate', new NetworkFirst());
registerRoute(({ request }) => request.destination === 'script', new StaleWhileRevalidate());
```

---

## Checklist Antes de Lançar

- [ ] Site é servido por HTTPS
- [ ] `manifest.json` tem `name`, `short_name`, `start_url`, `display`, `icons` (192 + 512)
- [ ] Ícones têm `purpose: "any maskable"`
- [ ] `sw.js` registra sem erros em DevTools → Application → Service Workers
- [ ] App shell carrega do cache quando a rede está com "Offline" em DevTools
- [ ] Fallback `offline.html` está em cache e é servido quando a navegação falha offline
- [ ] Auditoria Lighthouse PWA passa (Chrome DevTools → aba Lighthouse)
- [ ] Testado no iOS Safari (fluxo de instalação manual) e Android Chrome (prompt de instalação)