# AGENTS.md - Movix

## Consignes Codex et documentation

Ce fichier est l'entrée des consignes de ce dépôt pour Codex. Il adapte le guide `CLAUDE.md` et les README ; les fichiers Claude restent disponibles pour Claude. Les préférences générales et le choix des modèles délégués relèvent du `AGENTS.md` global. Ne pas utiliser les noms de modèles ou d'outils Claude dans Codex.

Commencer par le [README principal](README.md), puis lire seulement la documentation des modules concernés. Vérifier les scripts et le code actuels en cas de divergence avec une ancienne description.

| Sujet | Documentation |
| --- | --- |
| Frontend, routage, état local | [Frontend](src/README.md) |
| Carte des services backend | [Services backend](API/README.md) |
| Auth, profils, sync, sources, Live TV, VIP | [Main API](API/Mainapi/README.md) |
| Rooms et synchronisation temps réel | [WatchParty API](API/watchpartyAPI/README.md) |
| Extraction vidéo, proxy et DRM | [Proxies Embed](API/proxiesembed/README.md) |
| Extensions Chrome et Firefox | [Extension](extension/README.md) |
| Tampermonkey et logique partagée | [Userscript](userscript/README.md) |
| React Native, WebView, Android et iOS | [App mobile](app/README.md) |
| Moteur Rust et sortie WebAssembly | [WatchParty Sync](wasm/watchparty-sync/README.md) |

## Overview

Movix is a French streaming platform monorepo: React 18 + TypeScript frontend (Vite), Node.js/Express + Python backends, browser extensions, Rust WASM sync engine, and Cloudflare Workers.

## Setup

```bash
npm install
```

Backend services have separate dependencies:
- `cd API/Mainapi && npm install`
- `cd API/proxiesembed && pip install -r requirements.txt`

## Commands

```bash
npm run dev              # Vite dev server (localhost:3000)
npm run build            # Production build -> dist/
npm run lint             # ESLint
npm run preview          # Preview build
```

WASM (requires Rust):
```bash
npm run wasm:watchparty-sync:setup
npm run wasm:watchparty-sync:build
```

Backend (run individually):
```bash
node API/Mainapi/server.js          # Port 25565
node API/watchpartyAPI/watchparty.js # Port 25566
python API/proxiesembed/server.py    # Port 25569
```

## Repository Structure

```
src/                        # React frontend
  pages/                    # Page components
  components/               # Reusable components
    ui/                     # Primitives (shadcn/ui + Radix)
    *Player.tsx             # Video players (HLS, VideoJS, LiveTV, etc.)
    skeletons/              # Loading placeholders
  context/                  # React Context providers
  hooks/                    # Custom hooks
  services/                 # Axios API services
  utils/                    # Business logic, helpers
    sources/providers/      # Media source providers
  config/                   # Runtime config, Firebase
  workers/                  # Web Workers
  i18n/locales/             # FR/EN translations
  types/                    # TypeScript definitions
  data/                     # Static data
  lib/                      # Utility (cn helper)
API/
  Mainapi/                  # Express API (Node.js)
    routes/                 # Route modules
    middleware/             # Auth, CORS, security, rate limiting
    utils/                  # Cache, proxy, concurrency
    config/                 # Redis
  watchpartyAPI/            # Socket.IO WatchParty
  proxiesembed/             # Python aiohttp proxy + DRM
    drmproxy/services/      # 30+ hoster extractors
extension/
  Chrome/                   # Manifest V3
  Firefox/                  # Manifest V2
userscript/                 # Tampermonkey
app/                        # React Native + WebView (Android/iOS)
server/                     # Serveur du frontend construit (Docker/Coolify)
wasm/watchparty-sync/       # Rust -> WASM sync engine
PreMid/                     # Discord Rich Presence
cloudflareproxy/            # Cloudflare Worker
functions/                  # Serverless edge handlers
public/                     # Static assets, SW, WASM output
```

## Code Style

### General
- ES modules everywhere (`"type": "module"`, use `import`/`export`)
- French is the primary language (UI strings, comments, route names)
- Tests répartis par module : appliquer la section « Vérification proportionnée ».
- Fichiers volumineux (HLSPlayer, WatchTv, Profile) : chercher puis lire les sections utiles.

### Frontend (src/)
- **Components**: PascalCase files and exports, functional only (no classes)
- **Hooks**: `use` prefix, camelCase (`useWatchParty.ts`)
- **Utils/Services**: camelCase (`extractM3u8.ts`, `commentService.ts`)
- **Constants**: SCREAMING_SNAKE_CASE
- **Imports**: use `@/` alias (maps to `src/`)
- **Styling**: Tailwind utility classes only, no CSS-in-JS
- **State**: React Context API (no Redux/Zustand)
- **UI primitives**: `src/components/ui/` follows shadcn/ui patterns with Radix
- **i18n**: all user-facing strings through `t()` from `useTranslation()`, keep `fr.json` and `en.json` in sync
- **API calls**: use service modules in `src/services/`, never raw Axios in components
- **Types**: define in `src/types/`, TypeScript strict mode enabled

### Backend - Main API (API/Mainapi/)
- Route modules export `configure(dependencies)` function receiving `{ pool, redis, io, ... }`
- MySQL via connection pool (`mysqlPool.js`) - always use parameterized queries
- Redis for caching and rate limiting
- Middleware stack: CORS -> Helmet -> Rate Limit -> Auth -> Routes
- JWT auth via `middleware/auth.js`

### Backend - Python (API/proxiesembed/)
- Async/await with aiohttp (proxiesembed)
- Each hoster extractor is a standalone module in `drmproxy/services/`
- SOCKS5 proxy pool support, memory cache with TTL

### Extensions (extension/)
- Chrome = Manifest V3 (declarativeNetRequest, service worker)
- Firefox = Manifest V2 (webRequest, background page)
- Changes must be applied to both variants
- Core logic shared: `background.js`, `content.js`, `injected.js`, `extractors.js`

## Architecture

### Service Communication
```
Frontend (3000) ──> Main API (25565)       [REST + Socket.IO]
                ──> WatchParty API (25566)  [Socket.IO /watchparty]
                ──> Proxies Embed (25569)   [HTTP proxy/DRM]
                ──> Cloudflare Workers      [CORS relay]
Main API        ──> MySQL, Redis, TMDB, 30+ scraping sources
```

### Auth
BIP39 seed phrase or OAuth (Discord/Google) -> JWT -> localStorage. Axios 401 interceptor triggers global logout.

### WatchParty
Socket.IO rooms (host/viewers) + Rust WASM sync engine (clock calibration, drift correction) bridged via Web Worker.

### Video Playback
Multiple player implementations: HLS.js (primary), Video.js, Shaka Player, Dash.js, Mpegts.js. Player choice depends on source format.

### Deployment
Frontend on Cloudflare Pages (`CF_PAGES_COMMIT_SHA` for build ID). PWA with Workbox service worker.

## Repères complémentaires du projet

- Licence : CC BY-NC 4.0 ; conserver les crédits et se référer à `LICENSE`.
- Le frontend utilise Vite. `next.config.js` est un fichier historique, pas la configuration active.
- Points d'entrée : `src/main.tsx`, `src/App.tsx`, `src/routing/registry.tsx`, `API/Mainapi/server.js` et `API/Mainapi/app.js`. Les URLs runtime passent par `src/config/runtime.ts`.
- Les versions des bibliothèques sont celles des manifestes et lockfiles présents. Les anciens comptes de pages, providers ou composants ne sont pas des contraintes.
- Les packages ont leurs propres dépendances et scripts. `API/watchpartyAPI/` utilise les dépendances Node de la racine.
- Auth et profils traversent le frontend, `localStorage` et `/api/sync`. Préserver l'isolation des profils et les restrictions d'âge.
- Main API fonctionne en cluster, avec arrêt propre, MySQL, Redis et caches disque. Lire le cycle de vie avant de toucher les pools ou les ressources partagées.
- Une modification de lecture peut concerner les pages `src/pages/Watch/`, les players, Main API, le proxy Python et l'outillage navigateur.
- Le userscript est également embarqué dans l'app mobile : après modification de sa logique, vérifier le bridge et régénérer sa source via `node app/scripts/build-userscript.js` lorsque nécessaire. Ne pas éditer directement une source générée.
- Pour la Sync Pro, vérifier ensemble le serveur WatchParty, le hook, le worker et le moteur Rust. La sortie WASM attendue est `public/wasm/watchparty-sync/` ; conserver le repli JavaScript.
- Le fallback de domaine concerne `public/sw.js` et `src/services/blockDetection.ts`. Vérifier la configuration courante des miroirs et le parseur HTML/JSON avant modification. Les anciennes mentions de domaine ou de TTL ne font pas autorité.
- Les scripts `build:cf`, `build:coolify` et le serveur `server/index.js` couvrent plusieurs modes d'hébergement. Vérifier la cible avant toute action de déploiement.

## Vérification proportionnée

Il n'existe pas de commande `npm test` à la racine. Des tests ciblés existent notamment dans `tests/` et dans les modules backend ; les chercher dans la zone modifiée. Ne pas reprendre l'ancienne affirmation « aucun test ».

- Petite modification : contrôle ciblé, test existant pertinent ou relecture du diff selon le risque. Une modification de documentation seule ne demande pas de build applicatif.
- Frontend : lint ciblé si possible ; `npm run lint` et `npm run build` pour les changements qui nécessitent ces contrôles.
- Le build Vite ne remplace pas le contrôle TypeScript. Utiliser la configuration du package et la version locale de TypeScript pour un contrôle de types.
- Backend : privilégier les contrôles de syntaxe et tests du module ; ne pas démarrer tout le service pour un simple contrôle.
- WASM : reconstruire avec `npm run wasm:watchparty-sync:build` si le code Rust change.
- Distinguer les problèmes préexistants des régressions introduites, et indiquer les vérifications réellement exécutées.

## Environment Variables

Frontend: `.env` with `VITE_*` prefix (see `.env.example`)
Backend: separate `.env` per service (see `API/*/.env.example`)

Key frontend vars: `VITE_MAIN_API`, `VITE_TMDB_API_KEY`, `VITE_SITE_URL`, `VITE_WATCHPARTY_API`, `VITE_PROXIES_EMBED_API`, `VITE_TURNSTILE_SITE_KEY`

## Security Rules

- Always use parameterized SQL queries (never string concatenation)
- JWT authentication required on protected routes
- Rate limiting via Redis on auth endpoints
- Turnstile CAPTCHA for bot prevention
- Helmet + CORS middleware on all backend services
- Never commit `.env` files or secrets
