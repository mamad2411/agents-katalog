---
description: Binance trading app — stack, paths, and safety
globs: "**/*.{ts,tsx,js,jsx,md,sql}"
alwaysApply: true
---

# Stack

- Next.js App Router (`app/`). Prefer Server Components.
- Use `"use client"` only when hooks or browser APIs are needed.
- UI: Tailwind v4 + shadcn-style components under `components/ui/`.
- Data: Supabase (`lib/supabase.ts`, `lib/supabase-admin.ts`). Edge bot: `supabase/functions/binance-bot/`.

# Paths (use `@/` alias)

- Hooks: `hooks/`, `hooks/dashboard-data/`
- API routes: `app/api/**/route.ts`
- Shared state: `lib/store/`
- Types: `lib/types.ts` or `types/` when you add them

# Auth and secrets

- Never print or commit real API keys, service role keys, or bot secrets.
- Client: only `NEXT_PUBLIC_*` keys. Server: env vars, never expose to client bundles.
- Edge function auth: project uses `x-binance-bot-secret` + `BOT_SECRET` pattern — do not paste values into rules or commits.

# Database

- Schema lives under `supabase/migrations/`. Prefer `supabase migration new` then SQL.
- After DDL: note RLS impact. Do not ship `service_role` to browser code.
- Tunable bot fields live in `bot_settings` (e.g. `min_ai_confidence`, `max_open_trades`).

# UI / demo

- `/demo` uses SWR + `AppLayout`. Match existing card/table patterns.
- Theme tokens from `globals.css` — avoid hardcoded hex for theme colors.

# File size

- Keep files under 300 lines; split near 250 lines (same as root `.cursorrules`).
  "CRITICAL: The bot must use DB take_profit_pct for exits. Do NOT use hardcoded 10% ROI."

# Session changelog

- Meaningful bot/app changes: add a dated `##` section to `docs/CHANGELOG_AI.md`. Trivial edits: skip or one line. Schema stays in `docs/CURRENT_STATE.md`.
