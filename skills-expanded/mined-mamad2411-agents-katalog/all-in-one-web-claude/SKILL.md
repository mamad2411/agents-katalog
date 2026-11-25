# CLAUDE.md — All-In-One web app (the single frontend)

Conventions and workflow for the unified frontend. Read before changing code. Keep this
file in sync when architecture, secrets, or deploy steps change.

## What this is

**The one deployable frontend for every tool in this repo.** One Vite + React + TS app,
one Vercel deploy, one login (Supabase Auth, single user jared@voltara.com.my). It merged
the two previously separate frontends on 2026-08-17:

- **Financial Desk** (`/fin`) — from `financial-tracker/` (backend still lives there)
- ~~Restock Monitor (`/lzd`)~~ — **removed 2026-08-29** along with the whole
  `lazada-monitor/` folder (Fly worker retired, lzd_ DB objects torn down — see
  `docs/lzd-teardown.sql`)
- **Earnings Vol Scanner** (`/evs`) — added 2026-08-26; backend in `evs-scanner/`
  (edge fn `evs-scan` does all the math — see that folder's CLAUDE.md)
- **Training** (`/training`) — added 2026-09-05; Hyrox/endurance hub (tabs: Overview
  [was "Week" until 2026-09-07] / Activities / Races / Settings): weekly plan
  generation, intervals.icu+Hevy sync, Google Calendar push, Telegram bot. Backend in
  `training/` (edge fns tr-connect / tr-sync / tr-plan-week / tr-telegram-webhook —
  see that folder's CLAUDE.md before touching anything tr_)

plus two pages of its own: the **Home launcher** (`/`) and **Infrastructure** (`/infra`),
which lists every external service (Supabase, Vercel, Finnhub, GitHub)
with live health read straight from the DB.

Each tool's *backend* docs stay canonical in its own folder: read
`../financial-tracker/CLAUDE.md` for fin_ data-flow/verdict rules and
`../evs-scanner/CLAUDE.md` for the earnings-scanner model before touching those pages.

## Layout

```
web/
├── vercel.json is NOT here — the deploy config is /vercel.json at the REPO ROOT
├── .env               ← committed on purpose; all values are public (see Secrets)
└── src/
    ├── App.tsx        # auth gate → Login; router; react-query provider
    ├── components/
    │   ├── Layout.tsx # THE shell: top pill nav + floating icon rail + sub-tab pills
    │   └── ui.tsx     # design-system primitives — single copy now
    ├── lib/
    │   ├── supabase.ts   # ONE client (publishable key + auth) + refreshNow()
    │   └── finSignal.js  # fin display helpers (cycleRead, fmtMoney, …)
    ├── pages/         Home.tsx (launcher) · Infrastructure.tsx (ops hub) · Login.tsx
    └── apps/
        ├── fin/       FinShell.tsx + Desk/News/Settings (.jsx, ported as-is)
        ├── evs/       Scanner/Trades/Settings (.tsx) + lib.ts
        └── training/  Dashboard/Activities/Races/Settings (.tsx) + lib.ts
```

- **`apps/fin/*.jsx` are plain JSX** (ported verbatim from the old app; `allowJs` is on,
  `checkJs` off). New code should be `.tsx`. Don't convert them casually — they carry
  hard-won gotcha comments.
- **FinShell** owns the fin section: fetches the four `fin_` tables on entry, passes them
  via Outlet context, and **portals the "Refresh now" button into `#header-actions`**
  (a slot div in Layout's header). The evs pages self-fetch with react-query instead —
  the two data patterns are both intentional (polling-friendly vs once-a-day data).
- **Routing**: `/fin`, `/fin/news`, `/fin/settings`, `/evs`, `/evs/trades`,
  `/evs/settings`, `/training`, `/training/activities`, `/training/races`,
  `/training/settings`, `/infra`.
  Nav, titles and sub-tabs all derive from `APPS` in
  `Layout.tsx`. A new tool = a folder under `apps/`, routes in `App.tsx`, an APPS
  entry, a tile in `Home.tsx`, and (if it uses services) entries in
  `Infrastructure.tsx` `SERVICES`.

## Auth — the whole app is behind one passwordless login

Everything (including the Financial Desk, which previously had no auth) sits behind the
Supabase Auth session. One client in `lib/supabase.ts` uses the **publishable key**; all
queries run as the `authenticated` role.

- **Login is dual-mode; password is the DEV default.** `Login.tsx` has both a password
  form (`signInWithPassword`) and the passwordless flow (`signInWithOtp` →
  `verifyOtp(type: "email")` — 6-digit code, or the magic link in the same email), with
  a toggle between them. `DEFAULT_MODE` at the top of the file is `"password"` while the
  app is undeployed (Jared's dev preference) — **flip it to `"otp"` at go-live**; that
  one constant is the whole switch. In the OTP flow, **`shouldCreateUser: false` is
  load-bearing**: it's what makes a stranger's email bounce ("That email doesn't have
  access") instead of minting an account. Keep **"Allow new users to sign up" OFF** in
  the Supabase dashboard too — the client flag only guards THIS app's calls, not the raw
  auth API. There is no change-password UI; passwords are
  managed in the Supabase dashboard (Auth → Users) if needed.
- Magic-link clicks redirect to the project's **Site URL** (Supabase dashboard → Auth →
  URL Configuration) — set it to the deployed Vercel URL or the link lands on the wrong
  host. The code path works regardless.
- The `fin_` RLS policies from 0001 had no `TO` clause → `public`, so fin pages work
  logged-in with no schema change — but the anon key alone also still works against
  those tables. **Migration `0008_fin_authenticated_rls.sql`** (in
  `financial-tracker/supabase/migrations/`) closes that: drops the anon policies and
  recreates them `TO authenticated` *pinned to the owner's email* via `fin_is_owner()`.
  No data change; cron/edge fn unaffected (service role bypasses RLS). If the login
  email ever changes, update `fin_is_owner()`.

## Secrets / env

`web/.env` is **committed**: URL, publishable key, and the legacy anon JWT are all public
by design (the anon JWT already sits in migration `0003`). Never put the service-role key
or any edge-function secret anywhere under `web/`. Vite inlines env at build time — rebuild
after changes.

**Two keys on purpose:** the client uses the publishable key, but `refreshNow()` sends
the **legacy anon JWT** as its Bearer — `fin-daily-signal` is deployed `verify_jwt: true`
and the publishable key is not a JWT. Don't "simplify" one away.

## UI: the "Finexy" design system (reskinned 2026-09-05)

Jared picked an Onpoint Studio Dribbble reference (their "Finexy"/"Monetra" fintech
dashboards) and the whole app was restyled to it. This section is the spec — follow it
for anything new so the suite keeps reading as one product.

### The one rule that makes everything else work: token remap

The palette lives ONLY in `src/index.css` `@theme`. The pre-reskin codebase was written
in `slate-*` (neutrals) and `indigo-*` (primary) utilities, and those names were kept and
**remapped**: `slate-*` now resolves to a warm gray-green scale, `indigo-*` to a deep
green family. So:

- **Write new code with `slate-*` / `indigo-*` names.** They ARE the theme. `text-slate-500`
  is muted copy, `bg-slate-50` is the canvas/inset panels, `text-indigo-600` is a link,
  `ring-indigo-500` is a focus ring.
- **Never hardcode hex colors or reach for Tailwind's raw cool grays** (`gray-*`,
  `zinc-*`, `neutral-*`) — they bypass the theme and will look alien.
- Retheming later = edit `@theme` once; zero component churn.

### Palette

| Token | Value | Use |
|---|---|---|
| `slate-50` | `#f4f5f1` | page canvas, inset panels inside cards |
| `slate-100/200` | warm grays | secondary pills, dividers, table headers |
| `slate-500/600` | warm mid-grays | secondary text |
| `ink` (= `slate-900`) | `#171a16` | headings, active nav pills, switches — the "black" |
| `accent` | `#c9f542` | THE lime: primary buttons, highlights on dark cards |
| `accent-hover` | `#b9e636` | primary button hover |
| `forest-600 → forest-950` | `#35573c → #0f1a12` | dark feature-card gradient |
| `indigo-600` (remapped) | `#4f7d20` | links, "act" accents, focus rings |
| `emerald / amber / red / orange` | Tailwind defaults | semantics: good/up · watch · bad/down · error |

Rules of thumb: text on `accent` is ALWAYS `text-ink`, never white (contrast). On forest
gradients use `text-white` for primary copy, `text-white/50`-ish for secondary, `accent`
for the highlight line, `border-white/10` for dividers. Semantic colours are never
decorative — emerald means good, red means bad, everywhere.

### Typography

**Plus Jakarta Sans** (Google Fonts `<link>` in `index.html`, weights 400–800; falls back
to Inter/system). Page titles and hero greetings: `font-extrabold tracking-tight`
(text-3xl/4xl). Card titles: `text-sm font-bold`. Numbers, tickers, dates, codes:
`font-mono` — unchanged from the old system.

### Shape

Round is the brand. Radius tokens are bumped globally in `@theme` (xl 1rem, 2xl 1.35rem,
3xl 1.75rem):

- Cards: `rounded-3xl` (the `Card` primitive does this), minimal border
  (`border-slate-200/50`) + whisper shadow. No heavy drop shadows anywhere.
- Everything interactive is a **pill**: buttons, nav tabs, badges, the icon rail —
  `rounded-full`. Icon tiles: `rounded-2xl`.
- Form inputs stay `rounded-lg`/`rounded-xl` (pills make multi-field forms look novelty).

### Components (`ui.tsx` — the single copy)

- `Button` variants: `primary` (lime/ink — the ONE main action per view), `secondary`
  (soft gray pill), `dark` (ink pill, for emphasis without lime), `danger`, `ghost`.
- `Card`/`CardHeader`, `StatCard`, `StatusBadge` (speaks every tool's vocabulary — stock,
  verdicts, print directions, PASS/FAIL, open/closed), `Switch` (ink when on), `Modal`,
  `Input/Select/Textarea`, `Spinner`, `EmptyState`, `DataRow`.
- **Dark feature card** — the signature surface, reserved for each tool's single most
  important element (currently the fin verdict). It is bespoke markup, not a primitive:

  ```jsx
  <div className="rounded-3xl bg-gradient-to-br from-forest-600 to-forest-950 text-white shadow-sm">
    {/* title text-sm font-bold · subtitle text-white/50 · headline text-accent
        · list dots bg-accent · dividers border-white/10 */}
  </div>
  ```

  Don't multiply these — one dark card per screen keeps it special.

### Dark mode

Class-based: `dark` on `<html>`, applied pre-paint in `main.tsx` (saved in
localStorage `aio:theme`; unset = follow system) and toggled from the rail's
top pill (sun/moon) or the profile dropdown on small screens. **Dark styling is
the same token remap**: `.dark` in `index.css` re-declares `surface`, the slate
scale, and the semantic tints/text-tones; `accent`/`ink`/`forest` stay constant.
Rules: card/pill surfaces use `bg-surface` (never `bg-white` — that class is
banned now); active ink pills need `dark:bg-accent dark:text-ink` companions
(ink-on-dark vanishes); `dark:*` variants are for those few static-color spots
only — everything else must come free via tokens. Check both modes when
touching UI.

### Shell (`Layout.tsx`)

TOP bar: lime logo tile + wordmark · the **active app's sub-tabs centered as a gray
pill group** (white active pill — there is no top section nav; Jared removed it
2026-09-06 as redundant with the rail) · `#header-actions` portal slot (fin's Refresh
button mounts there) · user chip with sign-out. At `md+` the **floating icon rail**
(white rounded-full column, sticky) carries the sections + theme toggle + sign-out —
it is the ONLY section nav on md+. Below `md`: sections become a scrolling white pill
group under the bar, and the sub-tabs render in-content beside the big page title
(both `md:hidden`/mobile-only — don't resurrect them on desktop). There is **no
drawer/sidebar** — the old z-order/hamburger gotchas are gone. Everything derives from
the `APPS` array: a new mini-app = one APPS entry (name/icon/items) + routes in
`App.tsx` + a Home tile + Infrastructure `SERVICES` entries.

Wide tables still scroll inside their card (`overflow-x-auto` + `min-w-[…]`), never the
page — but that's for *read-only* tables (the trade log). Tables with **inputs** must
reflow instead of scroll on phones (see the fin Settings levels editor: stacked
per-ticker blocks below `sm`, table from `sm` up). Stat-card grids go `grid-cols-2`
on phones, never a stack of four full-width cards.

## Local development

```bash
cd web && npm install && npm run dev     # or `npm run dev` from the repo root
npm run build                            # tsc -b && vite build — the bar before shipping
```

No test suite/linter/CI; a clean `npm run build` is the correctness gate.
`vite.config.ts` keeps `server.host/allowedHosts: true` for Codespaces previews.

## Deploying

Push to `main` → Vercel builds via the **root** `/vercel.json`
(`npm --prefix web install/build`, output `web/dist`, SPA rewrite included — required,
client-side routing). One Vercel project for everything; if the two pre-merge Vercel
projects still exist, delete them so only this one serves traffic.

Backends deploy separately and unchanged: edge functions via Supabase MCP
`deploy_edge_function`, schema via `apply_migration`. See each tool's CLAUDE.md.
