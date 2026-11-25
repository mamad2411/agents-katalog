# CLAUDE.md — Engineering guide for Luna

This file is loaded into Claude's context for every task in this repo. Read
**`DESIGN.md`** for visual + copy decisions, **`ARCHITECTURE.md`** for why
the code is shaped the way it is (including known gaps — read it before
assuming something is a bug), and this file for conventions and gotchas.

---

## What this repo is

Luna is a voice-first AI companion for calm, late-night conversations. Two
processes:

- **`server/`** — Pipecat bot (Python). Real-time voice pipeline + memory
  I/O. Stays simple — voice in, voice out, transcript persisted to
  Postgres, audio optionally uploaded to object storage.
- **`web/`** — Next.js 16 app (App Router). Splash · onboarding · live
  call surface · profile · settings. Server components by default, client
  components only where state demands.

Auth: first-party email/password with HTTP-only session cookies. DB: Neon
Postgres via Drizzle. No payments — usage is capped by operator-configured
limits (`MAX_CALL_SECONDS`, `DAILY_LIMIT_MINUTES`), not billing; see
`ARCHITECTURE.md` §1. Voice models: configurable per call.

---

## ⚠️ Next.js 16 is not the Next.js you know

`web/AGENTS.md` is short and load-bearing:

> This version has breaking changes — APIs, conventions, and file
> structure may all differ from your training data. Read the relevant
> guide in `node_modules/next/dist/docs/` before writing any code. Heed
> deprecation notices.

Before you write a route handler, server action, or anything that touches
`next/*` imports, check the actual installed version's docs. Do not
generate from training memory.

---

## Repo layout

```
luna/
├── ARCHITECTURE.md    Decision log — why the code is shaped this way
├── DESIGN.md          Visual + copy system
├── CLAUDE.md          (this file)
├── README.md          Public-facing
├── SETUP.md           Env + local-dev bootstrap
├── DEPLOY_COMPOSE.md  Single-VPS docker-compose deployment
├── server/            Pipecat bot — Python
└── web/               Next.js app
    ├── AGENTS.md      → "this is NOT the Next.js you know"
    ├── CLAUDE.md      → @AGENTS.md
    └── src/
        ├── app/                Next.js App Router
        │   ├── page.tsx                splash
        │   ├── call/page.tsx           live conversation (auto-connects)
        │   ├── onboarding/page.tsx     name + vibe — currently unreachable
        │   │                          from normal flow, see ARCHITECTURE.md §7
        │   ├── profile/page.tsx        home for authed users
        │   ├── profile/history/        per-session detail (recording playback)
        │   ├── memory/page.tsx         memory review + client-side "forget"
        │   ├── safety/page.tsx         public safety + data-handling page
        │   ├── scenes/page.tsx         optional pre-set scene picker
        │   ├── settings/page.tsx       prefs + theme
        │   ├── sign-in/, sign-up/      local auth forms
        │   ├── api/profile/            GET/PATCH user prefs
        │   ├── api/session/start/      issues HMAC token, applies usage limits
        │   └── api/session/:id/        GET + DELETE; /end finalizes duration
        ├── components/         see DESIGN.md §7 for inventory
        ├── hooks/use-pipecat.ts        WebRTC + RTVI client wrapper
        ├── hooks/use-voice-level.ts    WebAudio analyser (mic + bot stream)
        ├── lib/auth.ts                 ensureUser (local session → DB user)
        ├── lib/limits.ts               MAX_CALL_SECONDS / DAILY_LIMIT_MINUTES
        ├── lib/db/                     Drizzle schema + connection
        ├── lib/memory.ts               reflection + embedding + recall (ARCHITECTURE.md §3)
        ├── lib/openai.ts               embeddings + optional conversation LLM
        ├── lib/sarvam.ts               reflector chat + (despite the name) embeddings
        ├── lib/splash-copy.ts          time-of-day splash, LLM-cached
        ├── lib/time-of-day.ts          IST bucketing for profile/farewell
        ├── lib/prefs.ts                client-side prefs cache
        ├── lib/prefs-server.ts         server-side prefs read
        ├── lib/sessions.ts             session lifecycle helpers
        ├── lib/data.ts                 static personas/scenes
        ├── lib/brand.ts                env-driven brandName/botName
        └── proxy.ts                    auth proxy (returns JSON 401 for /api)
```

---

## Conventions

### Naming
- Files: kebab-case (`luna-splash.tsx`, `time-of-day.ts`).
- Components: `PascalCase`. Conversation-surface components prefixed
  `Luna*` (`LunaOrb`, `LunaSplash`, `LunaConversation`). Generic helpers
  unprefixed (`TopNav`, `RecordingPlayer`).
- Type aliases over interfaces unless extending.

### Server vs client components
- Default to server. Add `'use client'` only when the file uses hooks,
  browser APIs, or event handlers.
- Server pages call `ensureUser()`, `getDb()`, etc. directly. Never expose
  DB access through a client-side fetch unless there's a public-API
  reason to.

### Data flow
- **Auth:** local session cookie → `ensureUser()` returns a row in `users`.
  Use the returned `user.id` (UUID) everywhere.
- **Prefs:** server is the source of truth. Client mirrors via
  localStorage cache for instant paint. Always `await fetchPrefs()` to
  reconcile.
- **Memory:** reflections are written by the web app at session end
  (`reflectOnSession()` in `lib/memory.ts`), not by the bot — the bot
  never reads memory back from Postgres. See `ARCHITECTURE.md` §3 for the
  full reflect → embed → recall pipeline.
- **Usage limits:** `MAX_CALL_SECONDS` and `DAILY_LIMIT_MINUTES` are read
  fresh from env on every call (`lib/limits.ts`), never cached. There is
  no per-user spendable balance — both caps apply identically to
  anonymous and signed-in callers. See `ARCHITECTURE.md` §1.

### Time
- Always bucket via `bucketFor()` (lib/time-of-day.ts) or
  `timeOfDayFromHour(currentISTHour())` (lib/splash-copy.ts). Both
  compute IST regardless of server TZ.
- Never call `new Date().getHours()` for user-visible time bucketing.

### Error handling at boundaries
- `POST /api/session/start` returns one of:
  `{status: 'ok', sessionId, token, botUrl, body}` ·
  `{status: 'soft_gate', reason: 'rate_limited'}` (over the daily cap) ·
  `{status: 'error', error: 'unauthorized' | 'rate_limited' | 'session_conflict' | 'invalid_body' | 'server_misconfigured'}`.
  The web client (`connect()` in `hooks/use-pipecat.ts`) turns these into
  typed errors; the call surface (`components/luna-conversation.tsx`) maps
  `unauthorized` → redirect to `/sign-in`, `rate_limited` → an inline
  message (there's no `/paywall` to redirect to anymore), and
  `session_conflict` → an inline retry affordance. Keep this contract; do
  not throw raw HTTP errors at the user.
- Auth proxy in `proxy.ts` returns JSON 401 (not HTML redirect) for
  `/api/*` routes — required so client code can `await res.json()` safely.

### Copy
- Read **DESIGN.md §2** before writing any user-facing string. The
  banned-vocab list is enforced, with one exemption for safety copy
  (crisis resources, non-diagnostic disclaimers, the `/safety` page) —
  see DESIGN.md §2 for the exact carve-out.

---

## Safety-critical code

A few areas carry more weight than a typical change and need explicit
maintainer review before merge, no matter how small the diff looks:

- **`server/luna_bot/voice/safety.py`** — the two-tier crisis detector.
  See `ARCHITECTURE.md` §4 for how it works and why it's fail-safe by
  design.
- **Crisis-adjacent copy** — the crisis directive text in `safety.py`,
  the `/safety` page (`web/src/app/safety/page.tsx`), and the `safety`
  block in `web/src/lib/i18n.ts`. Crisis-resource contact details
  specifically need re-verification against each service's current
  published numbers before any change ships — see the `NOTE(safety)`
  comment above `DEFAULT_CRISIS_RESOURCES` in `safety.py`.
- **Memory and data-handling code** — anything touching transcripts,
  reflections, embeddings, or recordings: what's stored, for how long,
  who can read it, and how (or whether) it gets deleted. See
  `ARCHITECTURE.md` §7 for the current gaps (client-only "forget," no
  self-serve account deletion) — know about them before you touch
  adjacent code, don't silently paper over them.

**Product-level guardrail, carried over from the pre-open-source product
spec and still load-bearing:** the product should not encourage exclusive
emotional dependency on the AI, or imply it replaces real-world
relationships or support. Nothing in code enforces this today — it's a
design constraint to keep in mind for persona work (`lib/data.ts`),
memory, and copy, not something a linter will catch.

---

## Local dev

Start three things:
1. **Bot:** `cd server && python bot.py` (default `:7860`).
2. **Web:** `cd web && npm run dev` (default `:3000`).
3. **Database:** any Postgres with the `vector` extension, via env
   (`DATABASE_URL`).

The bot **must** be running for `/call` to work. If you see "Failed to send
ICE candidate: NetworkError" in the browser, the bot is not running —
start it before debugging the web side.

`SETUP.md` has the full env list.

---

## Known gotchas (don't relearn these)

1. **`NEXT_PUBLIC_BOT_URL=""` defeats `??` fallback.** Treat empty string
   as unset in the connect path.
2. **Auth redirects must not break API JSON contracts.** `proxy.ts` returns
   JSON 401 for `/api/*` routes — keep it.
3. **The `/call` screen never lands on `state.status === 'idle'`** in
   normal flow because we auto-connect on mount. Don't write code that
   depends on rendering an idle state there.
4. **Buttons stretching to ovals on narrow viewports.** A leftover
   `@media (max-width: 420px)` rule used to set `.call-action { flex: 1
   }`. It is removed; do not add it back.
5. **Mic button visual halo extends 26px above its row.** The chips row
   above must keep ≥32px bottom padding to avoid overlap.
6. **The orb is decorative, not a tap target.** All "tap" actions go to
   explicit buttons. Do not wire onClick to `<LunaOrb>`.
7. **Two time-of-day helpers exist with different bucket boundaries**
   (`lib/splash-copy.ts` vs `lib/time-of-day.ts`). They serve different
   surfaces. Sync only when the change is intentional for both.

---

## Verification before declaring done

- `cd web && npx tsc --noEmit && npm test && npx next build` — all three
  must pass for any `web/` change.
- `cd server && .venv/bin/python -m pytest -q` — must pass for any
  `server/` change.
- For UI changes: open the affected route in the browser and verify the
  golden path. Do not claim a UI fix landed based on diff inspection
  alone — the user has corrected this multiple times.
- For copy changes: grep the codebase for any banned phrases the change
  might have re-introduced. The list is in DESIGN.md §2.
- For animation/style changes: check both the default and `[data-mood]`
  variants — the four moods are not visually equivalent.

---

## Don't do this

- Don't add light theme. Luna is dark-only by product decision.
- Don't introduce a new color outside the mood-token system.
- Don't use the word "Luna" in user-facing copy — read brand from
  `BRAND_NAME` env via `readBrandFromEnv()`. (`BRAND_NAME` exists for
  white-labeling a self-hosted deployment; the project itself is still
  named Luna.)
- Don't write copy that pressures, guilts, or implies the AI misses or
  needs the user — there's no paywall to point that instinct at anymore,
  but it still applies to session-limit and soft-gate copy. Read
  DESIGN.md §2 banned phrases before touching any of it.
- Don't mock the database in tests. (Existing convention — integration
  tests hit a real DB.)
- Don't use `git add -A` — sensitive files (`.env*`) live alongside source.
