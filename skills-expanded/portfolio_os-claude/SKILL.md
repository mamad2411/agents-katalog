# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- `npm run dev` — Vite dev server on `0.0.0.0:3000` (HMR can be disabled with `DISABLE_HMR=true`).
- `npm run build` — production build via Vite.
- `npm run preview` — serve the built bundle.
- `npm run lint` — `tsc --noEmit` (type-check only; there is no ESLint).
- `npm run clean` — removes `dist/`.

There is no test runner configured.

## Environment

`vite.config.ts` reads `GEMINI_API_KEY` from `.env.local` via `loadEnv` and inlines it as `process.env.GEMINI_API_KEY` at build time (see `.env.example`). `APP_URL` is also expected in deployed AI Studio environments. The `@` alias resolves to the project root.

## Architecture

This is a single-page Vite + React 19 + TypeScript app that renders a Windows 95-style "desktop OS" portfolio (SURF_PORT OS). It was scaffolded from Google AI Studio (see `README.md`), so the Gemini SDK (`@google/genai`) and `express` are listed as dependencies but are **not currently used** by the app code — the UI is purely client-side.

### File layout

Each component lives in **its own directory** as `ComponentName/ComponentName.tsx` with a barrel `index.ts` re-export (`export { default } from './ComponentName'`). This keeps external imports short (`from './components/Taskbar'`) and leaves room for colocated helpers, hooks, or subcomponents next to each component without polluting the parent folder.

```
src/
├── App.tsx                         orchestrator: state + composition of Header/Desktop/Taskbar
├── types.ts                        shared WindowState interface
├── main.tsx · index.css
├── apps/                           window content components (one per "app")
│   ├── WelcomeContent/
│   │   ├── WelcomeContent.tsx
│   │   └── index.ts
│   ├── ProjectsContent/
│   └── LogsContent/
└── components/                     UI primitives and layout
    ├── DesktopIcon/                clickable desktop icon
    ├── Window/                     draggable Win95 window frame
    ├── Header/                     top AppBar (dummy)
    ├── Desktop/                    <main> with icons + AnimatePresence of Window instances
    ├── Taskbar/                    <footer> — owns the clock useEffect
    ├── StartButton/                Start button + popup menu
    └── TaskTabs/                   open-window tabs in the taskbar
```

When adding a helper to a component, put it inside that component's folder (e.g. `components/Window/useDragBounds.ts`) and import it with a relative path. Only promote it out of the folder if a second component needs it.

### Key patterns

- `App.tsx` owns the authoritative state: `windows: WindowState[]`, `activeWindowId`, `isStartOpen`, plus the four window handlers (`openWindow`, `closeWindow`, `toggleMinimize`, `focusWindow`). All four recompute z-index by taking `Math.max(...zIndex) + 1`, so any new interaction that should bring a window forward must follow the same pattern rather than tracking focus separately.
- Window *content* components from `src/apps/` are instantiated as JSX at the time the `windows` state is initialized and stored inside each `WindowState.content`. They are not re-created on re-render, so **they cannot read live state from `App`** — to add interactivity inside a window, lift state into `App` and pass it via props or context.
- `Window.tsx` uses `motion/react` (`drag` + `dragMomentum={false}`) on the window root. Its prop is named `win` (not `window`) to avoid colliding with the global. The `Taskbar` (`<footer>`) and Start menu popup render as siblings, not portals, and rely on z-index (`z-1000` / `z-1001`) to stay above windows.
- The Win95 look is built from Tailwind v4 utilities plus a small set of custom classes in `src/index.css`: `retro-bevel-out`, `retro-bevel-in`, `window-shadow`, `dither-bg`, `win95-title-bar(-inactive)`, and a custom `::-webkit-scrollbar`. Reuse these instead of re-deriving bevel `box-shadow` values inline.
- Tailwind is wired through `@tailwindcss/vite` and configured via the `@theme` block in `index.css` (font families `font-sans` / `font-display` / `font-mono`); there is no `tailwind.config.*` file.

### Adding a new "app"

1. Create `src/apps/YourApp/YourApp.tsx` (default export) and `src/apps/YourApp/index.ts` with `export { default } from './YourApp';`.
2. In `App.tsx`: import it, add a `WindowState` entry to the initial `useState`, add a `<DesktopIcon>` in `Desktop.tsx` (or pass it through), and add an entry to `menuItems` in `StartButton.tsx` so it shows up in the Start menu. All three entry points call `openWindow(id)`.
