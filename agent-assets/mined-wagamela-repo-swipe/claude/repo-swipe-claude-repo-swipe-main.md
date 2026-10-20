# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**RepoSwipe** is a Tinder-style discovery interface for discovering real software projects on GitHub. It's a monorepo containing:
- **rs-frontend**: React + Vite + TypeScript + Tailwind CSS v4 + Oxlint
- **rs-backend**: Node.js + Express API with GitHub integration and image proxy/processing

The core UX is a swipeable card deck where users can browse projects and make quick like/pass decisions.

---

## Development Commands

### Frontend (rs-frontend/)

```sh
cd rs-frontend
npm run dev      # Start Vite dev server (http://localhost:5173 by default)
npm run build    # Build for production (tsc -b && vite build)
npm run lint     # Run Oxlint
npm run preview  # Preview production build locally
```

### Backend (rs-backend/)

```sh
cd rs-backend
npm run dev      # Start with nodemon (watches for changes, PORT defaults to 3000)
npm start        # Start production server
```

**Frontend dev server proxies `/api` to `http://localhost:3000`** (configured in `vite.config.ts`).

---

## Architecture & Key Components

### Frontend Structure

**Component Hierarchy:**
- **App.tsx** – Main entry point; routes between root and NotFoundPage. Contains the Deck component.
- **Deck** – State management for the card experience (history, intro overlay, debug panel, responsive panels).
- **DiscoveryDeck** – Core card swipe logic; manages drag state, animations, and the stack of 3 visible cards.
- **SwipeCard** – Individual card presentation (project image, metadata, links).
- **CardBack** – Colored back of the stacked cards below the active card.

**Key Hooks:**
- `useProjects()` – Fetches paginated projects from `/api/projects` with caching, refill logic, and taste-based reranking.
- `useImagePreloader()` – Preloads images for the top 3 cards to ensure smooth swiping.
- `useImagePreloadLink()` – Adds a link prefetch hint for the active card's image.

**Design System:**
- Tailwind CSS v4 with custom config (stored as inline values, not a separate config file).
- Dark theme: background (#101014), neutral (#1B1B25), surface (#1F1F2E).
- Violet accent: primary (#5E6AD2), primary-hover (#4E5BBF).
- Typography: Inter (UI), JetBrains Mono (code/metadata).
- Spacing: 4px base unit (scales: 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px).
- Border radius: 4px (chips), 6px (buttons/inputs), 8px (cards/panels), 12px (modals).

**Layout:**
- Responsive 3-column grid on desktop (`lg:grid-cols-[13rem_minmax(0,1fr)_12rem]`): left sidebar (past cards), center (deck), right sidebar (project info).
- Mobile collapses to single column with slide-in modals for left/right panels.
- Deck is sized to `h-[min(56vh,38rem)] w-[min(92vw,28.5rem)]` (responsive to viewport).

**Animation & Interaction:**
- Swipe threshold: 100px horizontal movement.
- Card tilt: max ±18° (tilt increases with drag).
- Flyout duration: 450ms; smooth spring ease.
- Keyboard: A/← (pass), D/→ (like), Ctrl+Shift+D (debug toggle).
- History tracking: Shows past swiped cards with color indicator (green = like, red = pass).

### Backend Structure

**Routes:**
- `/api/health` – Health check.
- `/api/projects/first` – Single project (for initial load); 1-min cache.
- `/api/projects?query=...&sort=...&per_page=...&refresh=...&light=...` – Paginated projects; 5-min cache.
  - Query params: `query` (search), `sort`, `per_page` (default pagination), `refresh` (bypass cache), `light` (minimal fields).
- `/api/image-proxy` – Image proxy with caching (see cache.js).

**Services:**
- `github.js` – `getProjects()` function that fetches from GitHub API, filters/sorts, and transforms projects.
- `image-proxy.js` – Proxies images through Sharp for resizing/format conversion.
- `cache.js` – In-memory cache with TTL support.

**Key Dependencies:**
- Express 5.x
- Sharp (image processing)
- dotenv (environment variables)
- nodemon (dev-only)

---

## Design Guidelines

### Violet Issue Design System
The interface uses a dark, developer-focused aesthetic with:
- **Colors**: Violet primary accents on dark charcoal/black surfaces.
- **Density**: Compact components (28-36px heights) to maximize visible information.
- **Typography**: Inter throughout; JetBrains Mono for code/metadata.
- **Elevation**: Layered backgrounds, not shadows (dark interfaces use color layering).
- **Motion**: Snappy, <150ms transitions. Avoid decorative animation.

See **DESIGN.md** for full spec (colors, typography scales, component details, spacing).

### Anti-Vibecoded Design Principles
**Do NOT:**
- Use harsh gradients, generic blobs, or decorative shapes.
- Default to purple+black without intent.
- Add rounded corners indiscriminately.
- Fill empty space with shadows or ornamental effects.
- Blindly apply trendy UI patterns (bento grids, terminal styling, "it's not X, it's Y" copy).
- Use fake testimonials, metrics, or dashboards.
- Animate every element on hover or add unnecessary sparkles/neon.

**Do:**
- Design every visual decision with intent (ask "why?" not "what trendy pattern fits?").
- Use hierarchy (typography, spacing, scale, contrast) instead of borders/backgrounds.
- Make components feel cohesive.
- Test the design without decoration — if it collapses, decoration was hiding weak structure.

See **DESIGN_AVOIDS_GUIDELINE.md** for 30 specific patterns to avoid and guiding principles.

---

## TypeScript & Linting Configuration

**TypeScript (rs-frontend/):**
- Target: ES2023
- Module: ESNext
- JSX: react-jsx (automatic runtime)
- Strict checks: No unused locals/parameters, no fallthrough cases, erasable syntax only.
- Module resolution: Bundler (for Vite).
- See `tsconfig.app.json` for full config.

**Oxlint:**
- Plugins: react, typescript, oxc
- Rules: `react/rules-of-hooks` (error), `react/only-export-components` (warn, with const export allowlist).
- Run: `npm run lint`

---

## Image Handling

**Frontend:**
- Images are fetched from GitHub/proxied through `/api/image-proxy`.
- `useImagePreloader()` preloads images for the top 3 cards before they're visible.
- `useImagePreloadLink()` adds a `<link rel="prefetch">` hint for the active card image.
- Images are served with cache headers (see backend routes).

**Backend:**
- `/api/image-proxy` proxies and optionally resizes images with Sharp.
- Cache-Control headers: 1 min (first project), 5 min (paginated projects).
- Also hardened with s-maxage for edge caching.

---

## State & Data Flow

**Frontend State (App/Deck):**
- `activeIndex` – Currently displayed card index.
- `history` – Array of swiped cards with id, index, name, direction (left/right).
- `showIntro` – Intro overlay visibility (stored in sessionStorage).
- `debugOpen` / `outlines` – Debug UI toggles.
- `leftPanelOpen` / `rightPanelOpen` – Mobile sidebar states.

**Pagination & Refill:**
- `useProjects()` fetches projects in chunks and automatically triggers refill when remaining cards drop below 8.
- Uses `requestIdleCallback` to avoid janky refill during interaction.

**History:**
- Past cards are stored in a list and can be revisited by clicking.
- Clicking a past card removes it from history and jumps back to that index via `DiscoveryDeck.jumpTo()`.

---

## Recommendation Algorithm

The deck adapts to what the user likes. All model state lives in `rs-frontend/src/lib/taste.ts` and is session-only (an in-memory `TasteProfile`, never persisted).

**Feature extraction** – Each project becomes a weighted bag of features: `topic:` (from the repo's GitHub topics, weight 1.0), `lang:` (scaled by the language's byte share, 0.6), `owner:` (0.35), and `word:` (stopword-filtered tokens from the name and description, 0.3).

**Learning** – Every swipe calls `recordSwipe()`: a like adds `+1 x featureStrength` to each of the project's features, a pass adds `-0.55 x featureStrength`. Before the update, all existing weights decay by 0.94, so recent swipes outweigh old ones and the deck follows where a session is heading. Weights are clamped to ±6.

**Reranking** – `rerankProjects()` scores each unseen card with `tanh(dot(profile, features) / sqrt(featureCount) / 2)` and greedily reorders. Three things keep it from becoming a filter bubble or a jarring UI:
- `frozenUntil` (activeIndex + 2) protects cards already on screen and preloaded.
- A stable per-project noise term (0.35 amplitude, hashed from `owner/name`) keeps unrelated cards in play without reshuffling the tail on every swipe.
- A diversity penalty (0.22 per overlapping topic across the last 3 placements) prevents long runs of near-identical cards.

**Query steering** – Reordering only works on repos already fetched, so refills are steered too. `pickSteerTopic()` samples a topic from the profile weighted by affinity (sampled, not argmax, so multi-interest sessions keep seeing everything) and `useProjects.loadMore()` passes it as `?topic=`. The backend converts it to a `topic:<t> stars:>300 pushed:>...` GitHub search and tops up from the general feed when the topic is too niche to fill a batch.

**Batch paging** – `?batch=N` offsets the GitHub search start page (and is part of the backend cache key), so successive refills return new repos instead of the same cached page.

The debug panel (Ctrl+Shift+D) shows the current top topics and their weights.

---

## Common Development Tasks

### Adding a New API Endpoint
1. Add route in `rs-backend/src/routes/index.js`.
2. Create service function in `rs-backend/src/services/` if needed.
3. Set appropriate Cache-Control headers.
4. Call from frontend via `fetch("/api/your-endpoint")`.

### Modifying the Card Component
- Edit `rs-frontend/src/components/SwipeCard.tsx`.
- Ensure responsive sizing (uses Tailwind classes, no hardcoded pixel widths).
- Images are lazy-loaded via `useImagePreloader()` hook.

### Changing Colors or Spacing
- Colors and spacing are inlined in Tailwind classes (no separate `tailwind.config.js`).
- Update Tailwind class values in components or create utility overrides in global CSS.
- Refer to DESIGN.md color palette for brand colors.

### Adding New Keyboard Shortcuts
- Edit the `useEffect` hook in `Deck` (App.tsx, lines 357–402).
- Add new key handlers and dispatch to `controlsRef.current`.
- Update action bar hint text and keyboard shortcut hints.

### Deploying
- Frontend: `npm run build` generates dist/; deploy to static host.
- Backend: `npm start` runs server; set `PORT` env var as needed.
- Ensure `/api` proxy points to your backend URL in production.

---

## Notes for Future Sessions

- **No tailwind.config.js**: All Tailwind config is done via inline classes and values.
- **Image proxy caching**: Backend uses in-memory cache; restart server clears it.
- **Session storage**: Intro overlay state persists in sessionStorage (`rs-intro-seen`).
- **Responsive design**: Uses Tailwind's `sm:` and `lg:` breakpoints; test on mobile.
- **TypeScript strict mode**: No unused vars/params allowed; keep types tight.
- **History data**: Limited by UI (list-based); no persistence across page reloads.

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `rs-frontend/src/App.tsx` | Main entry, state management, keyboard shortcuts |
| `rs-frontend/src/components/DiscoveryDeck.tsx` | Card swipe logic, drag physics, animation |
| `rs-frontend/src/hooks/useProjects.ts` | Pagination, refill, caching, rerank + query steering |
| `rs-frontend/src/lib/taste.ts` | Taste profile, scoring, reranking, topic steering |
| `rs-frontend/vite.config.ts` | Build config, API proxy setup |
| `rs-frontend/tsconfig.app.json` | TypeScript strict settings |
| `rs-backend/src/server.js` | Express app startup |
| `rs-backend/src/routes/index.js` | API routes |
| `rs-backend/src/services/github.js` | GitHub API integration |
| `DESIGN.md` | Full design system spec |
| `DESIGN_AVOIDS_GUIDELINE.md` | Anti-vibecoded design principles |

