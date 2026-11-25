---
name: damas-backend
description: >-
  Conventions and patterns for the Damas-MSA backend services (apps/api, apps/ai)
  and shared rules engine (packages/rules) on Bun: Bun.serve fetch handlers,
  MongoDB via a Repo interface (Mongo in prod, in-memory in tests), optimistic
  locking on games (version → 409), Clerk JWT verification via JWKS, svix/Stripe
  webhook signature verification, the config-driven VariantConfig rules engine,
  the A* AI contract, Elo/hints, and bun test (incl. perft). USE THIS SKILL for
  any server, persistence, auth, game-loop, AI, or rules work in Damas-MSA —
  adding endpoints (e.g. /game/:id/hint), wiring Elo, verifying webhooks, Mongo
  collections/indexes, implementing variants, or writing engine/API/auth tests.
  Trigger for phrasings like "the move endpoint returns 409", "add a Mongo
  collection", "verify the Stripe webhook", "implement the international variant",
  or "write a perft test" — without naming the stack. Do NOT use for frontend or
  visual work (use damas-frontend), nor for standalone design deliverables (use
  the design:* skills).
---

# Damas-MSA — Backend conventions

Two Bun services plus a shared package:

- `apps/api` — the **authority**: auth, game loop, persistence (Mongo), ranking,
  Elo, cosmetics, proxy to the AI. Public.
- `apps/ai` — **stateless** A* microservice (`POST /move`). No users, no DB, no
  payments. Reachable **only** from the Backend (no published port in compose).
- `packages/rules` — the shared, **config-driven** checkers engine used by both.

Authoritative spec: `docs/PRD.md` §6–§10 and §14. The golden rule: **the Backend
validates everything; never trust the client.** The AI service shares the same
engine, so a move it returns is re-validated by the Backend before being applied.

## HTTP services (Bun.serve)

- Each service exports a `fetch(req) => Response` handler; `src/index.ts` wires
  `Bun.serve({ port, fetch })` and reads config from env (with sane localhost
  defaults). Keep `index.ts` thin — logic lives in `server.ts` and domain modules.
- The API handler is built by `createFetchHandler(repo, ai, auth, opts)` so tests
  can inject a `MemoryRepo`, a stub AI, and a dev auth. Don't hardcode
  dependencies inside the handler.
- Return JSON via a small `json(body, status)` helper; always include CORS headers
  and answer `OPTIONS` with 204.
- Domain errors use `ApiError(status, code)` and are caught at the top of the
  handler → `{ error: code }` with the right HTTP status. Add new failure modes as
  `ApiError` codes, not ad-hoc responses. Match existing codes
  (`unauthorized`, `version_conflict`, `active_game_exists`, `illegal_move`, …).

## Persistence: the Repo pattern

- All DB access goes through the `Repo` interface (`src/types.ts`). Two
  implementations: `MongoRepo` (prod) and `MemoryRepo` (tests) — **keep them in
  lockstep**; if you add a method, implement it in both with identical semantics.
- `MemoryRepo` must `structuredClone` on read and write so tests can't mutate
  stored docs by reference (mirrors Mongo's value semantics).
- Collections follow PRD §8: `users`, `games`, `ranking`, `cosmetics`,
  `user_cosmetics`, `elo_history`. Create indexes in `MongoRepo.ensureIndexes`.

### Optimistic locking (PRD §14.10) — do not skip

`games` carries a `version`. Every mutating game update is a **compare-and-set**:
filter by `{ _id, version: expectedVersion }` and `$set` the new fields including
`version: expectedVersion + 1`. If `matchedCount !== 1`, another device already
moved → throw `ApiError(409, "version_conflict")`. This is what makes
cross-device resume safe; clients send the `version` they have and re-sync on 409.

### Atomic turn

In `playMove`, compute the **AI's reply before persisting**, then save the human
move + AI move in a single update. Either both land or neither — a resume never
sees a half-applied turn (PRD §10 consistency).

## Auth (PRD §5.1) — verify, never store

- `createClerkAuth({ issuer, jwks })` verifies the Bearer JWT against Clerk's
  JWKS with `jose`. The issuer is derived from the publishable key
  (`issuerFromPublishableKey`) so there's nothing extra to configure.
- Invalid/expired/forged/wrong-issuer → `getUserId` returns `null` → handler
  responds 401. The `sub` claim is the `clerk_user_id`, the key for every entity.
- Dev mode: `createDevAuth` (or `allowDevHeader: true`) accepts `x-dev-user`. This
  is gated by `ALLOW_DEV_AUTH=true` and must never be on in production.
- Never persist passwords/credentials — Clerk owns them.

## Webhooks — always verify signatures (PRD §10)

- **Clerk** (`/webhooks/clerk`): verify the **svix** signature — HMAC-SHA256 over
  `${id}.${timestamp}.${body}` with the base64 secret after `whsec_`, plus a
  timestamp tolerance to block replays. `user.created` → `upsertUser`;
  `user.deleted` → soft-delete (`pending_deletion` + 30-day grace, §14.6).
- **Stripe** (`/webhooks/stripe`): verify the Stripe signature; grant the cosmetic
  only on `checkout.session.completed`, never from the client. Use idempotency so
  retried events don't double-grant.
- Webhooks authenticate by **signature**, not user session — handle them before the
  session check in the router.

## The rules engine is config-driven (PRD §14.11)

- `packages/rules` exposes pure functions: `getLegalMoves`, `applyMove`,
  `createInitialState`, tablas detection, `perft`. They take a board/state, never
  hit IO. Both services import them — **one source of truth**, so they can't drift.
- Variants are a `VariantConfig` (`size`, `menCaptureBackward`, `flyingKings`,
  `mandatoryCapture`, `majorityRule`, `promotionEndsTurn`). Move generation, A*,
  and the heuristic must **read the config** — never hardcode 8×8 or "forward
  only". `english` is implemented; `international`/`spanish` flip flags (F6).
- Board encoding: owner-coded 2D `cells` (variable size), playable dark squares
  only, canonical orientation (human at bottom). See PRD §14.1.

## AI microservice & search (PRD §7)

- A* is a **fixed requirement** — don't propose minimax. The search is best-first
  on board states with `f = g - h`, bounded by per-difficulty node/depth budgets.
- `chooseMove(cells, preset, rng)` is pure and rng-injectable so tests are
  deterministic (pass a fixed `rng`). The `/move` contract is PRD §7.3.
- Difficulty presets (§7.4) vary budget, heuristic richness, opponent model, and
  fallibility — fallibility must still pick a **legal** move (and respect mandatory
  capture). Keep latency under the p95 < 800ms KPI; log `durationMs`.
- **Hints (§5.8)** reuse `/move` with `turn: "human"` and the hard preset.

## Testing (bun test) — PRD §14.9

- Run with `bun test`; tests live in each package's `test/`.
- **Rules engine:** unit-test move generation, mandatory/multi-capture, promotion,
  end/draw detection — and **perft** (node counts at depth N from known positions)
  to validate the generator. Add a perft baseline per new variant.
- **AI:** assert it never returns an illegal move, always honors mandatory capture,
  and respects the node budget; use a fixed `rng`.
- **API:** drive the handler with `MemoryRepo` + a stub AI + `createDevAuth`. Cover
  the happy path, `illegal_move`, `version_conflict`, abandon-confirm, surrender,
  ranking ordering, and ownership (can't touch another user's game).
- **Auth:** generate a local JWKS in-test (`jose` `generateKeyPair` +
  `createLocalJWKSet`) to verify accept/expired/forged/wrong-issuer.
- **Webhooks:** sign payloads in-test and assert tampered/missing-header rejection.

## Reference

- Existing code to match: `apps/api/src/{server,games,repo-mongo,repo-memory,auth,webhook-clerk}.ts`,
  `apps/ai/src/{search,heuristic,presets,server}.ts`, `packages/rules/src/*`.
- Run: `bun run dev:api` (3000), `bun run dev:ai` (3001); Mongo via Docker.
  Smoke test the stack: `bun scripts/smoke.ts`.
- Typecheck: `bun run typecheck`.
