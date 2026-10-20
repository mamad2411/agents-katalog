# AGENTS.md

## Project Context

**TitanOS**  enterprise-grade field operating system (React + Vite + Supabase + Capacitor), not a feature pile.
Package ID for Google Play: `com.titanos.myapp`.

**FINAL OBJECTIVE:** cohesive OS for workers, contractors, drivers, businesses, and teams. Ship gate  secure, performant, intuitive, accessible, tested, polished, integrated (see `.cursor/rules/final-objective.mdc`, `docs/FINAL_OBJECTIVE.md`).

## Key paths

- `src/`  frontend
- `src/api/`  Supabase auth, entities, functions client
- `api/functions/`  Vercel serverless functions
- `supabase/migrations/`  database schema
- `android/`  Capacitor Android / Play Store project
- `.env.local`  secrets (never commit)

## Working notes

- Use `npm run dev` for local web
- Env: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` (see `.env.example`)
- For OAuth / Play: set `VITE_TITANOS_PUBLIC_ORIGIN` to the HTTPS site URL
- Free launch mode: `src/lib/plan.js` ? `FREE_LAUNCH = true`
- Lint/build before finishing significant changes: `npm run lint` && `npm run build`
- Play AAB: `npm run android:sign` ? `release/TitanOS.aab`
- Final objective: OS feel + ship gate (see `.cursor/rules/final-objective.mdc`)
- Founding 100: first users free membership (fees still apply); after 100 beta closes + PayPal live (`docs/FOUNDING_100.md`, migration 035)
- UI rule: every screen answers **What's happening? / What's next? / Where for more?** (see `.cursor/rules/three-question-ui.mdc`)
- Nav rule: **?3 taps**, clear title, Back, breadcrumbs when nested, no dead ends (see `.cursor/rules/navigation.mdc`)
- IA rule: domains **Live / History / Analytics / Reports / Communication / AI / Configuration / Administration / Labs** (see `.cursor/rules/information-architecture.mdc`)
- Perf rule: throttle GPS/telemetry, pause when hidden, no junk re-renders (see `.cursor/rules/performance.mdc`)
- DB rule: RLS least privilege, ownership checks, indexes on owner columns (see `.cursor/rules/database.mdc`)
- Security rule: hostile input, hashed portal tokens, settle on capture only (see `.cursor/rules/security.mdc`)
- Error rule: log + categorize + recover; never leak internals (see `.cursor/rules/error-handling.mdc`)
- Loading rule: skeletons / progress / retries / offline / sync  never blank while loading (see `.cursor/rules/loading-states.mdc`)
- Empty rule: why empty + what's next + create shortcut  never blank pages (see `.cursor/rules/empty-states.mdc`)
- Micro rule: every action gets feedback; motion ?200ms + reduce-motion (see `.cursor/rules/microinteractions.mdc`)
- Visual rule: one design language  tokens + PageShell/Card/Button/overlays (see `.cursor/rules/visual-consistency.mdc`)
- A11y rule: keyboard, SR, ?44px touch, contrast, focus, reduce-motion, responsive (see `.cursor/rules/accessibility.mdc`)
- Mobile rule: thumb zone, driving chrome, honest offline, one GPS watch (see `.cursor/rules/mobile-experience.mdc`)
- Driver Hub: Mission Control live-only; Explorer groups; auto trip/classify/rush/idle/digests (see `.cursor/rules/driver-hub.mdc`)
- Titan AI: server snapshot + pageContext; allowlisted actions; YOUR DATA vs GENERAL (see `.cursor/rules/titan-ai.mdc`)
- Comms: warm-mic PTT, reconnect/TURN, membership gate, channel notify (see `.cursor/rules/comms.mdc`)
- Search: instant local index  jobs/trips/messages/invoices/customers/voice/files/analytics/settings/AI (see `.cursor/rules/search.mdc`)
- Reporting: ExportMenu CSV/Excel/PDF-print/share/schedule via `src/lib/export` (see `.cursor/rules/reporting.mdc`)
- Settings: categorized + searchable catalog, docs/defaults/reset (see `.cursor/rules/settings.mdc`)
- Testing: `npm test` unit/integration pack; `npm run test:e2e` Playwright smoke (see `.cursor/rules/testing.mdc`)
- Observability: Sentry crash/perf/replay, structured logs, health, analytics, audit, flags, ops alerts (see `.cursor/rules/observability.mdc`)
- Code quality: no dead code, DRY shared utils, EditorConfig + ESLint, JSDoc critical APIs (see `.cursor/rules/code-quality.mdc`)
- Scalability: bounded lists, indexes, keyset pagination, durable rate limits, cloud trips (see `.cursor/rules/scalability.mdc`)
- Maintainability: ARCHITECTURE.md, MODULE barrels, shared UI, onboarding (see `.cursor/rules/maintainability.mdc`)
- Final QA: clear critical/high/medium; `docs/FINAL_QA.md` + `test:final-qa` (see `.cursor/rules/final-qa.mdc`)
