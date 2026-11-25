---
name: specter
description: >-
  Specter game backend platform (BaaS) — start here when integrating Specter into any game.
  Covers what Specter is, authentication (api-key header + Bearer token), environment base URLs,
  the standard response envelope, error codes and rate limits, and which Specter skill to use for
  player auth/accounts, game economy (currencies, items, stores), progression (tasks, achievements,
  battle pass), competitions (leaderboards, tournaments) and real-time multiplayer (matchmaking, parties).
---

# Specter — Game Backend as a Service

Specter is a backend platform for games. Instead of building your own backend, your game calls
Specter's REST APIs (and WebSocket server for multiplayer) for accounts, virtual economy,
missions/achievements, leaderboards, tournaments and matchmaking. Game content (currencies,
items, tasks, leaderboards…) is configured in the Specter dashboard at
https://console.specterapp.xyz; your game then reads and acts on that content via the client API.

## Base URLs

| Environment | Client REST API | Multiplayer (Socket.io) |
|---|---|---|
| Production | `https://api.specterapp.xyz/v2/client` | `https://multiplayer.specterapp.xyz` |
| Staging | `https://client.staging.specterapp.xyz/v2/client` | `https://staging.multiplayer.specterapp.xyz` |

Quick connectivity check: `POST {base}/app/welcome`.
Always use the **v2** client API. v1 exists but is legacy — do not build new integrations on it.

## The two credentials (read this first)

1. **`api-key` header** — required on **every** request. Issued per project + environment in the
   dashboard (dev / qa / production keys are different). Identifies which game/project the call is for.
2. **`Authorization: Bearer <accessToken>` header** — required for player-scoped endpoints
   (anything `player/me/*`, purchases, inventory changes, score posts…). Obtained from any
   `auth/login-*` or `auth/signup-*` endpoint. The JWT embeds `userId` + `projectId` and expires
   in ~1 hour — refresh with `auth/refresh-token`.

Endpoints listed as "API Key" auth in the references work without a user token (app-level catalog
reads, plus server-to-server lookups of other players' data).

**All client endpoints use `POST`** with a JSON body — even reads. Filters, pagination
(`offset`/`limit`) and the `attributes` array (opt-in response fields) go in the body.

## Response envelope

Every endpoint returns the same shape — branch on `status`/`code`, read payload from `data`:

```json
{
  "status": "success",
  "code": 200,
  "message": "Items list",
  "data": { ... },
  "errors": []
}
```

On failure: `"status": "error"` with `errors: [{ errorCode, errorMessage }]`. Gateway-level
failures (bad api-key, rate limit, billing) return a smaller `{ "error": "..." }` body — see
[references/errors.md](references/errors.md) for every code and exact body.

## Which skill to use

| You want to… | Use skill |
|---|---|
| Sign up / log in players (email, username, custom ID, Google, Apple, Steam, Discord, Facebook), link accounts, player profiles + custom data, friends | **specter-players** |
| Currencies, wallets, items, bundles, stores, purchases, inventory, gacha/loot boxes, real-money deposits/withdrawals | **specter-economy** |
| Tasks, missions, achievements, daily quests, streaks, battle pass, XP/levels, granting rewards, custom events | **specter-progression** |
| Leaderboards, tournaments, instant battles, prize distribution, schedules | **specter-competitions** |
| Matchmaking, parties, match sessions, real-time WebSocket events, score sync | **specter-multiplayer** |

## Quickstart: first integration in 3 calls

```bash
BASE=https://client.staging.specterapp.xyz/v2/client

# 1. Verify the api-key works
curl -X POST $BASE/app/welcome -H "api-key: $API_KEY"

# 2. Login-or-create a player with your own player id (silent login — most common for games)
curl -X POST $BASE/auth/login-custom \
  -H "api-key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"customId": "player-123", "createAccount": true}'
# → data.accessToken (createAccount:true signs the player up on first login)

# 3. Read the player's profile
curl -X POST $BASE/player/me/get-profile \
  -H "api-key: $API_KEY" -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" -d '{}'
```

## Verify a setup

To check whether a Specter project is configured correctly (api-key valid, currencies/tasks
defined, wallets provisioning), run the bundled smoke-test:

```bash
SPECTER_API_KEY=<key> node scripts/verify.mjs --env staging
# optional: --event <eventId> to send a test event end-to-end
```

It reports api-key validity, project info, currencies, test-player login, wallet provisioning,
and task configuration — use it to answer "is my Specter setup working?" before debugging client
code. For Claude to inspect/configure a project interactively (and create currencies/tasks), see
the `@specterapp/mcp` server shipped alongside these skills.

## Platform behaviors worth knowing

- **Asynchronous side-effects.** Signup initialization (wallets, default inventory, battle pass
  tiers), task validation, and leaderboard/tournament prize distribution all run on background
  queues. They complete in seconds-to-minutes — poll the relevant `get-*` endpoint rather than
  expecting instant consistency after a triggering call.
- **Rate limits** are token-bucket per app/IP/user. A 429 includes `retryAfterSeconds` — honor it.
- **CORS** for browser games requires your domain to be whitelisted in the dashboard.
- App-level catalog endpoints (`app/get-*`) are cacheable on your side; player-scoped data is not.

## References

- [references/authentication.md](references/authentication.md) — credential details, token lifecycle, auth matrix
- [references/environments.md](references/environments.md) — URLs, dashboard, API docs links
- [references/errors.md](references/errors.md) — every gateway + API error with exact bodies
- [references/endpoints-index.md](references/endpoints-index.md) — app-level endpoints covered by this skill


## Product manual (concepts & terminology)

The Specter **user manual** (the same docs game designers read in the dashboard) is bundled in
[references/manual-index.md](references/manual-index.md) — read it to understand the CONCEPTS and
intent behind this domain (what each type/feature means, how dashboard workflows map to the API),
then pair it with the endpoint references for exact request shapes.


## Client (v2) API — what you call FROM your game

The **game-side** endpoints (all `POST /v2/client/*`, authed with the project api-key + a player
access token for player-scoped calls) are indexed with full request DTOs + auth in
[references/client-api-index.md](references/client-api-index.md). Use these for code that ships in
the game/app. **Never call the `/v1/*` admin API from game code** — that's dashboard-only.
