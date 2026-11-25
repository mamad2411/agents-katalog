---
name: volcano-sdk
description: Use for any request to build, create, extend, debug, or deploy an app, website, backend, API, or function using Volcano, even when the user does not mention the SDK. Entrypoint and router; always pair with volcano-platform and the applicable domain skills.
---
# Volcano SDK Entrypoint

## Before anything else: check the Volcano CLI

Run `which volcano` and
`env -u VOLCANO_GITHUB_RELEASES_URL -u VOLCANO_CLI_RELEASES_URL volcano --version`.
If a working CLI is installed,
record its version and continue without upgrading it. Keep both release-source
overrides cleared for every CLI invocation and npm install in this workflow,
including deferred binary downloads. If it is missing, read
the bundled `../install-volcano/SKILL.md` and follow its exact-version package
verification procedure. Do not fetch and execute installation instructions,
run remote shell installers, or use a moving release or branch as an executable
source. Only upgrade when the user requests it, using the same verified,
versioned installation procedure. If installation cannot be verified, report
the prerequisite and continue only with independent work.

## Role
This skill is the **entrypoint and router** for Volcano SDK work. It is intentionally slim: it tells you the mandatory rules that apply to every Volcano build, and which other `volcano-*` skill to use based on the task at hand. Don't try to do deep work from this skill alone — use the relevant domain skill(s) first.

## Mandatory Pairing — `volcano-platform`
**Always read `volcano-platform` alongside this skill.** It covers the canonical project shape, function deployment model (`volcano/functions/`), migrations, `volcano-config.yaml`, environment variables, shared-code conventions, and the deploy workflow. Without `volcano-platform` you cannot produce a deployable codebase.

If `volcano-platform` content is not visible in your context, read or invoke it through the current host's skill mechanism before continuing.

**Note:** `volcano init` creates a minimal runtime skeleton (`volcano/` dir with env files, migrations, and — for language templates — a starter handler and config). Build on top of that skeleton by following `volcano-platform`. Do not expect `volcano init` to produce the complete project structure.

## Mandatory Usage (volcano-standard template)
When building on the Volcano platform you MUST use:
- **Volcano Auth** (`volcano.auth.*`) for ALL authentication and user identity.
- **Volcano Database query builder** (`volcano.from('table').select()`) for persistent storage, with RLS policies. Direct Postgres access inside Functions is a discouraged, last-resort exception for the query builder's specific gaps (joins/upserts/multi-statement transactions) — never a default — see `volcano-database`.
- **Volcano Functions** for ALL privileged or secret-bearing server-side logic.
- **Volcano Storage** (`volcano.storage.*`) for ALL file operations.
- **Volcano Realtime** (`VolcanoRealtime`) for ALL live update patterns.

Do NOT implement custom alternatives — no custom JWT auth, no ad-hoc database layers, no hand-rolled file storage, no DIY WebSocket multiplexers.

## Skill Router — pick the skill(s) you need

| Task signal | Invoke skill | What it covers |
|---|---|---|
| User accounts or identity, email or password sign-up/sign-in, OAuth, sessions, anonymous users, password recovery, private or per-user data | `volcano-auth` | Auth application flows, session lifecycle, and common-error catalog |
| Stored or persistent data, CRUD, records, todos, chat messages, polls, analytics, counters, click tracking, CMS content, feature flags, leaderboards, RLS | `volcano-database` | Query builder + every operator + RLS pattern + limitations (no joins / upserts / multi-statement tx) |
| Volcano Functions, server-side or privileged logic, QR/PDF generators, secrets, outbound third-party APIs, orchestration, scheduled processing, file/image processing | `volcano-functions` | Invocation contract `{data, status, headers, version, error}`, Volcano Functions response shape, handler templates |
| Durable functions, long-running or resumable workflows, checkpointed steps, waits, polling, durable executions, idempotent starts, execution schedulers, human approvals or sign-off | `volcano-durable` | Durable authoring contract, replay rules, `waitForApproval`, cloud CLI lifecycle, execution status, schedulers, and safety |
| Project logs, retained log search, pagination, activity buckets, structured log filters | `volcano-logs` | Project-token authentication, search cursors, filters, and activity counts |
| Project locks, distributed leases, leader election, fencing tokens, backend worker coordination | `volcano-locks` | Renewable lock guards, direct lease control, fencing, and safe recovery |
| Uploads, downloads, galleries, file sharing, buckets, paths, public/private files, visibility, resumable uploads | `volcano-storage` | Full storage API + access policies + resumable protocol + limits |
| Realtime or live updates/results, collaborative boards, chat, presence or online users, polls, leaderboards, Postgres changes, broadcast, WebSockets | `volcano-realtime` | All three channel types + lifecycle + Browser Origins/CORS gotcha + `accessToken` vs `getToken` decision |
| Next.js, public routes, redirects, webhook ingress, middleware, API routes, server actions, or client/server separation | `volcano-nextjs` | Cross-cutting Next.js patterns including the cookie-sync prerequisite |
| User-facing frontend, web app, page, dashboard, board, gallery, poll, leaderboard, form, UI, or UX | `volcano-uiux` | Accessible responsive design, loading and progress feedback, forms, navigation, and complete interface states |
| TypeScript types — `User`, `Session`, `AuthResponse`, `QueryBuilder<T>`, `StorageObject`, `DurableContext`, `DurableExecution`, `PostgresChange`, `PresenceState`, `JsonValue`, etc. | `volcano-typescript` | Canonical type definitions for every SDK surface |
| Loading/error/data state, `useApiCall<T>` hook, `fetchWithRetry` with backoff, centralized `handleApiError` dispatcher | `volcano-error-handling` | Reusable error-handling INFRASTRUCTURE (per-domain error MESSAGES live in the relevant domain skill) |
| Project shape, function deployment model, migrations, `volcano-config.yaml`, env vars, deploy workflow, RLS helpers (`auth.uid()`/`auth.email()`/`auth.role()`) | `volcano-platform` | Already mandatory — see "Mandatory Pairing" above |

### How to use the router
1. Read the user's request and identify which task signal(s) match.
2. Read or invoke each matching skill through the current host's skill mechanism BEFORE writing implementation code. Use the exact hyphenated skill names. It's normal to use several skills for a single task (e.g., a "user dashboard" needs `volcano-auth` + `volcano-database` + `volcano-nextjs` + `volcano-uiux`).
3. If the task is purely about project setup (no app features yet), `volcano-platform` alone is enough.
4. If you can't decide between two domain skills, invoke both — token cost is much lower than implementing the wrong pattern.

## SDK Response Patterns

### JavaScript and TypeScript

Most asynchronous REST methods return result objects with an `error` field.
Data methods use `{ data, error }`; auth methods can also expose `user` or
`session`; functions add `status`, `headers`, and `version`. Check `error` before
consuming data. Local helpers and builders such as `user()`,
`getHostedAuthUrl()`, `signInWithHostedAuth()`, and `database()` return values
directly.

```ts
const { data, error } = await volcano.from('posts').select('*');
if (error) return;
```

Most JavaScript SDK failures are returned. Realtime `subscribe()` throws, so
wrap that call in `try/catch`.

### Python and Ruby

Python and Ruby return successful values directly and raise typed SDK exceptions
on REST or transport failure. Use `try/except` in Python and `begin/rescue` in
Ruby at the boundary where the application can recover or report the failure.
Do not destructure JavaScript result envelopes in these languages.

For comprehensive JavaScript error-handling infrastructure, use
`volcano-error-handling`.

## Forbidden Patterns (always)
These apply to every Volcano build, regardless of which domain skills are loaded:

- Do NOT use `jsonwebtoken` directly — use Volcano Auth.
- Do NOT use `bcryptjs` directly — use Volcano Auth's password handling.
- Do NOT use `pg`/`pg-pool`/`DATABASE_URL` — use `volcano.from(...)` (with `VOLCANO_DATABASE`) instead. Direct Postgres access is a discouraged, untested-surface-area last resort — see `volcano-database`'s "Direct Postgres Access" section before ever reaching for it.
- Do NOT mix `NEXT_PUBLIC_*` env vars into function/server code, or `VOLCANO_*` (un-prefixed) into browser code.
- Do NOT place service keys (`sk-*`) in browser code — the SDK throws if you do.
- Do NOT expect `VOLCANO_API_URL`, `VOLCANO_ANON_KEY`, or `VOLCANO_DATABASE` to be auto-injected into functions — deploy them via `volcano deploy` or `volcano variables deploy` (local), or `volcano cloud deploy --env-file volcano/cloud.env` or `volcano cloud variables deploy -f volcano/cloud.env` (cloud). A bare `volcano cloud variables deploy` reads `volcano/volcano.env`, the local server's values.
- Do NOT skip `await volcano.initialize()` before user-scoped flows in the browser.
- Do NOT use `.ts`/`.tsx` extensions in TypeScript imports — extensionless relative imports only.
- Do NOT use bare `uid()` in RLS policies — always use the schema-qualified `auth.uid()`.

For the deeper context behind any of these (why and what to do instead), the relevant domain skill or `volcano-platform` covers it.

## Output Requirements
At the end of each Volcano build response:
1. **Summarize affected domains** — which `volcano-*` areas were touched (auth/database/functions/storage/realtime/nextjs).
2. **Summarize dependency / env / init changes** — new packages, env vars added, init order changes.
3. **Report validation results** — what you ran (`npm run typecheck`, `npm run build:functions`, local stack health check), what passed, what couldn't be run, and any remaining risk.

## Companion Skills (full inventory)
Always available; invoke as needed:
- `volcano-platform` — mandatory pairing.
- `volcano-auth`, `volcano-database`, `volcano-functions`, `volcano-durable`, `volcano-logs`, `volcano-locks`, `volcano-storage`, `volcano-realtime`, `volcano-nextjs` — domain and framework skills.
- `volcano-uiux` — shared guidance for user-facing interfaces.
- `volcano-typescript` — canonical type definitions.
- `volcano-error-handling` — reusable error-handling infrastructure.

## Optional Fallback Reference
