# AGENTS

High-signal facts for AI agents working in this repo. When in doubt, omit.

## Stack & setup

- **Express 5** (not 4 — `req.query.date` is `undefined` not `""` when param missing).
- **EJS v5** views in `src/views/` (set in `server.js`).
- **SQLite via sql.js** (WASM, in-process). Every non-transaction `run()` calls `persist()`, writing entire DB to disk. DB file at `src/db/barbersync.sqlite`.
- **Database auto-bootstraps** on import (`src/lib/database.js`): creates tables, seeds demo data, generates today's schedules. Self-heals if DB file is deleted.
- **No build step.** Frontend: Tailwind v4 browser CDN, DaisyUI 5, Alpine.js 3 — all via CDN in layout.
- **No linter, formatter, test framework, CI, bundler, TypeScript.** `npm test` always fails by design.
- **ESM** (`"type": "module"`). All imports use `import`/`export`.
- Dependencies: `express@^5.2.1`, `ejs@^5.0.2`, `express-ejs-layouts`, `bcryptjs`, `jsonwebtoken`, `dotenv`, `sql.js`.
- `.env` must exist with `JWT_SECRET` and demo passwords (`ADMIN_PASSWORD`, `USER_PASSWORD`, `OPERATOR_PASSWORD`). The "barber" role's demo username is `operator`.
- Package name is "barberin"; app is branded "BarberSync" in UI.
- `src/lib/env.js` auto-loads `dotenv/config` on import (side effect) — never import `dotenv` directly.

## Commands

```bash
npm install          # install deps
npm run dev          # node --watch server.js (auto-restart)
npm start            # node server.js (production)
npm test             # placeholder — always fails
```

App runs at `http://localhost:3000`. No build/watch step needed.

## Architecture

```
server.js            — entrypoint (middleware + route wiring)
src/routes/          — 6 route files aggregated by index.js
src/controllers/     — request handlers
src/middleware/      — authRequired, adminRequired, guestOnly, pageRoleRequired
src/services/        — 11 domain files (no monolithic dataService.js)
  bookingService.js  — Bookings, queue, history
  barberService.js   — Barbers, availability, salary
  scheduleService.js — Schedule generation & management
  userService.js     — Users, auth, registration
  serviceService.js  — Services CRUD
  paymentService.js  — Payments & orders
  dashboardService.js— Dashboard aggregation
  pageService.js     — Page-level data composition (get*PageData)
  adminService.js    — Admin barrel (re-exports from domain services)
  publicService.js   — Public barrel (re-exports)
  authService.js     — Auth barrel (re-exports)
src/lib/             — database.js, auth.js (JWT), timeSlots.js, demoCredentials.js, seed.js, env.js
src/db/              — SQL schema & seed files
src/views/           — EJS templates + partials/ + admin/
```

- **No monolith.** `dataService.js` was deleted. Every service file has real logic. Barrel files (`adminService`, `publicService`, `authService`) re-export from domain services only — update their imports when adding exports.
- **JWT in HttpOnly cookie** (`barbersync-token`). Also accepted via `Authorization: Bearer` header. `localStorage` mirrors the user for `BarberSyncStore` (defined in `partials/storageHelpers.ejs`).
- **Three roles**: `admin`, `user`, `barber`. Demo passwords in `.env` (displayed on login page).
- **`currentPage`** EJS variable must be passed in every `res.render()` — drives nav highlighting.
- **Route guards**: `/booking`, `/status`, `/dashboard`, `/about` require `user` role. Admin pages require `admin`. `/login`, `/register`, `/forgot-password` redirect to landing if already authed.

### Layout system

| Page type | Layout | Theme |
|-----------|--------|-------|
| Public pages (/, /booking, /status, etc.) | `layout.ejs` (default) | `cupcake` |
| Login/Register/Forgot password | `layout: false` — standalone | `business` |
| Admin pages | `layout: "admin/layout"` | `business` |

- **Login page has no layout** — `layout: false` means `storageHelpers.ejs` is NOT included. `BarberSyncStore` is undefined on the login page. The login handler uses optional chaining (`window.BarberSyncStore?.setCurrentUser()`) so this is safe.
- **Admin page "Keluar" buttons** must call `POST /api/auth/logout` to clear the HttpOnly cookie, not just navigate to `/` or `/login`.
- **Auth hydration**: `storageHelpers.ejs` runs an async IIFE on every page load that fetches `GET /api/auth/me`. On success, it populates `BarberSyncStore` + `window.__authUser`. The sidebar reads from both sources in its Alpine `x-init`.

### Routes

Refer to `README.md` for the full route table. Key patterns:
- Admin CRUD actions use **form POST + 302 redirect** (not fetch/PATCH) for page-backed actions: `/admin/queue/update-status`, `/admin/schedules/generate`, `/admin/schedules/:id/status`
- The same actions have **JSON API** equivalents under `/api/admin/` for programmatic use
- `/admin/kapster/toggle/:id` is a GET that redirects 302 (not a JSON endpoint)
- `/booking/create` is a form POST (not fetch) — the booking page creates a hidden `<form>` and calls `form.submit()`

## Business logic

- **Time slots**: 10:30–21:30, 30-min intervals (`TIME_START`, `TIME_END`, `SLOT_MINUTES` in `src/lib/timeSlots.js`).
- **Booking status flow**: `menunggu → dikonfirmasi → dalam_proses → selesai` (or `dibatalkan`). Completing/cancelling frees the schedule slot (status back to `tersedia`).
- **1 active booking per user** — `createBooking` rejects if user already has a non-terminal booking.
- **Schedules auto-generate** for today on DB bootstrap. Admin can generate for any date.

## Frontend conventions

- **UI copy**: All text in Indonesian. Preserve language.
- **Icons**: Emoji only. Never add icon libraries.
- **Themes**: `coffee`, `light`, `dark`, `cupcake`, `business`, `emerald` — stored in `localStorage`, applied via `data-theme`.
- **Alpine.js component names** by page: `homeApp` (index.ejs), `bookingApp` (booking.ejs), `statusApp` (status.ejs), **`profileApp`** (about.ejs — not `aboutApp`), `loginApp` (login.ejs).
- **Glassmorphism cards**: `bg-base-100/30 backdrop-blur-sm rounded-2xl p-6 border-2 border-base-content/10`
- **Sidebar search input** is decorative — no functionality wired.
- **Bottom navbar** has FAB "Antrian" button (`-mt-8`, larger circle).
- `status.ejs` reads queue data from `localStorage` via `BarberSyncStore`, NOT from the API.
- No `public/` or `static/` directory — all frontend assets are CDN-only.

## Gotchas

- Express 5: `req.query.date` is `undefined` (not `""`) when param missing — use optional chaining.
- **Login state check**: `booking.ejs`, `status.ejs`, `about.ejs` all check `storedUser.username` (not `email`). The JWT payload has `username` but NOT `email` or `nama`. Using `email` as a truthy check will fail for users whose email is empty in the DB.
- `/api/auth/me` now returns full user data from DB (via `getPublicUser()`), not just the JWT payload.
- Login saves JWT to **both** HttpOnly cookie (server) and `localStorage` (client-side store) independently.
- No CORS middleware — single-origin only.
- `server.js` sets `res.locals.demoUsers` globally — every view can access `demoUsers` without passing it to `res.render()`.
- Adding a page: create EJS in `src/views/`, add route in the appropriate `src/routes/` file, pass `title` + `currentPage`. If it returns data, add a `get*PageData` function in `pageService.js` (or the relevant domain service).
- Services import directly from each other (e.g., `scheduleService.js` imports from `barberService.js`). No circular deps currently — maintain this.
