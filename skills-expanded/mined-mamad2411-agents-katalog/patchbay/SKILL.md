# Patchbay

Audio patchbay editor - visualiserer og redigerer patch points for fysiske patchbays i et studie.

## Tech stack

- **Nuxt 4** (CSR-only, SSR: false)
- **Nuxt UI 3** for UI components
- **Supabase** for auth + data (one layout per user)
- **Pinia** for state management
- **Bun** as package manager and runtime
- **TypeScript**
- **Vercel** for deployment (CDG1 region)

## Project structure

```
app/
  components/patchbay/   # 15 Vue components (PatchbayView, PatchbayJack, etc.)
  composables/           # useTheme, usePatchbaySelection, usePatchbayDragDrop
  stores/patchbay.ts     # Main Pinia store - all state + actions
  types/patchbay.ts      # TypeScript types (PatchPoint, PatchRow, PatchBay, etc.)
  pages/                 # index (main), login, auth/callback
  layouts/               # default (app), auth (login)
  middleware/auth.ts     # Route guard
assets/css/patchbay.css  # Theme CSS variables (5 themes)
public/default-layout.json  # Default layout for new users
supabase/migrations/     # DB schema
```

## Key concepts

- **PatchPoint**: A single jack (label, signal type, normal type, notes)
- **PatchRow**: A row of up to 48 points, with section labels
- **PatchBay**: Always 2 rows (TOP/BTM), represents one physical bay
- **PatchbayLayout**: Collection of bays
- **Signal types**: mic, line, inst, cv, none
- **Normal types**: full, half, free
- **Themes**: default (amber), t-green, t-blue, t-tape, t-paper

## Data flow

1. Layout loads from Supabase on mount (or creates default)
2. All edits go through Pinia store actions
3. Store debounce-saves to Supabase (500ms)
4. Theme persisted to localStorage + DB

## Commands

```bash
bun run dev      # Start dev server
bun run build    # Production build
bun run preview  # Preview production build
```

## Conventions

- Components are in `app/components/patchbay/` with `Patchbay` prefix
- All state mutations go through the Pinia store, never directly
- CSS uses custom properties prefixed with `--pb-` in patchbay.css
- Use Nuxt UI 3 components where possible
- IBM Plex Mono is the only font
