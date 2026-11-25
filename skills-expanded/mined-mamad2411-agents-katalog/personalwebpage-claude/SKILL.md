# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Commands

- **Dev server:** `npm run dev`
- **Build:** `npm run build` · **Start production:** `npm start`
- **Lint:** `npm run lint` (ESLint with the React Compiler rules; `set-state-in-effect` is an error)
- **Tests:** `npm test` (Vitest, node environment, `**/*.test.ts`)

## What this is

namanh.dev, Nam's portfolio, built as **namOS**: a desktop operating system in the browser.
Next.js 16 App Router, React 19 with the React Compiler, TypeScript, Tailwind v3, deployed on
Vercel. Design spec: `docs/plans/2026-09-02-namos-redesign-design.md`. Implementation plan:
`docs/plans/2026-09-02-namos-implementation.md`.

## Architecture

```
app/layout.tsx          server: fonts, metadata, fetches grind + TikTok data, renders <StoreProvider><Desktop>
app/**/page.tsx         each route renders only <OpenApp app item /> (+ metadata, notFound for bad ids)
components/os/          the shell: store (reducer), StoreProvider (context + router sync), Desktop,
                        Menubar, Dock, DesktopIcons, WindowLayer, Window, useDrag, useClock, icons
components/apps/        one component per app + registry.ts (title, default rect, component)
data/                   all content: experiences, hackathons, projects, about, content, site, legal, trash
lib/coding.ts           live NeetCode 150 progress from GitHub (revalidate 1h)
lib/tiktok.ts           TikTok oEmbed thumbnails (revalidate 1h, never throws)
public/img/             wallpaper (Shanghai), hackathon photos, avatar, trash screenshots
```

### How a route becomes a window

`components/os/store.ts` owns the state: `windows: Win[]` (max 3), each `{ app, item?, z, maximized, boot? }`.
`appForPath(pathname)` maps a URL to `{ app, item }`; `pathFor(app, item)` maps back. The
`StoreProvider` initialises from the pathname (so deep links server-render the right window)
and lives in the root layout, so windows persist across client navigations. Route pages mount
`<OpenApp>` which dispatches `open` without touching the URL; dock clicks call `open()` which
also `router.push`es. Closing a window `router.replace`s to the next focused window's path or `/`.
`app/page.tsx` renders `null` on purpose: `/` only boots the Terminal on a fresh load.

Finder encodes its folder in the item: `"hackathons"`, `"projects"`, `"hackathons/<id>"`.
Text app items: `impressum`, `datenschutz`, `about-namos`, `404`.

### Phone mode

Below 768 px the same tree renders as a phone: CSS in `app/globals.css` (`@media (max-width: 767px)`)
turns the focused window into a full-screen sheet with a "‹ Home" button, hides unfocused windows,
and turns the dock into a home-screen grid when no window is open (`.os.has-window`).

### Styling

Tokens in `app/globals.css` `:root` (`--accent #FF5C2A`, `--surface`, `--ink`, `--term-*`).
OS chrome uses hand-written classes (`.os-*`, `.dock-*`, `.work*`, `.finder*`, `.term`); app
content uses Tailwind utilities with the extended palette in `tailwind.config.ts`. Fonts via
`next/font`: Bricolage Grotesque (`--font-display`), Hanken Grotesk (`--font-sans`),
IBM Plex Mono (`--font-mono`).

## Content rules

- Hackathons: wins only. Participated-only events are not listed (Nam's call).
- `@namb.tech` shows views, never followers. Sold-account numbers stay in `about.story` / `content.originStory`.
- Every stale-able number carries a `measuredAt` date in data and is rendered with it.
- Old routes (`/erfahrungen`, `/projekte`, `/competitions`, `/coding`, `/kontakt`) redirect in `next.config.ts`.

## Conventions

- All pages are server components; `"use client"` only inside `components/os` and `components/apps`.
- No `setState` directly in effect bodies (React Compiler lint). Use timers/callbacks or `useSyncExternalStore`.
- Prettier: 2 spaces, semicolons, double quotes, 100-char lines.
- Work on a branch and push for a Vercel preview; merge to `main` only when Nam says so.
