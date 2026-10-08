# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev        # Dev server (Vite, port 5173)
npm start          # Alias for dev
npm run build      # Production build → dist/
npm run preview    # Serve the production build locally
npm test           # Run Vitest in watch mode
npm run test:run   # Run Vitest once (CI mode)
npm run deploy     # test:run + Vercel deploy
```

## Environment Variables

Vite exposes env vars prefixed with `VITE_` via `import.meta.env`:

```
VITE_API_KEY       # GIPHY API key
VITE_ENDPOINT      # Backend API base URL (Node/Express on Heroku)
```

Rename your `.env` file entries from `REACT_APP_*` to `VITE_*`.

## Architecture

React 18 app built with **Vite 6** (migrated from CRA). Routing via **Wouter** (not React Router). No state management library — global state lives in React Context only. Tests run with **Vitest** (same API as Jest).

### Layer responsibilities

| Layer | Location | Purpose |
|-------|----------|---------|
| Pages | `src/pages/` | Route-level components (lazy-loaded) |
| Components | `src/components/` | Reusable UI, each with paired `.css` |
| Hooks | `src/hooks/` | All async/state logic extracted here |
| Services | `src/services/` | Raw `fetch()` calls to GIPHY API and backend |
| Context | `src/context/` | Global state — `UserContext` is the only active one |

### Key patterns

- **Service layer**: All API calls go through `src/services/`. No fetch calls inside components.
- **Custom hooks**: Business logic lives in hooks (`useGifs`, `useUser`, `useNearScreen`, `useSingleGif`). Components stay presentational.
- **Infinite scroll**: `useNearScreen` (IntersectionObserver) + `just-throttle` triggers pagination in `useGifs`. Offset-based, not cursor-based.
- **Auth**: JWT stored in `sessionStorage`. `useUser` handles login/logout/favorites. `UserContext` exposes user state globally.
- **Code splitting**: All pages are `React.lazy()`-loaded in `App.js` with `Suspense`.
- **Memoization**: Components are wrapped with `React.memo` by default — don't remove without profiling.
- **Modal pattern**: Uses a portal to `#modal-root` in `public/index.html`.

### Routing (Wouter)

```
/                    → Home (trending GIFs)
/login               → LoginPage
/register            → RegisterPage
/search/:keyword/:rating?  → Search results
/gif/:id             → GIF detail
```

### State storage

- `sessionStorage` — JWT token
- `localStorage` — last search keyword

### Import paths

`jsconfig.json` sets `baseUrl: "src"`, so imports are relative to `src/`:

```js
import useGifs from "hooks/useGifs"  // not "../../../hooks/useGifs"
```
