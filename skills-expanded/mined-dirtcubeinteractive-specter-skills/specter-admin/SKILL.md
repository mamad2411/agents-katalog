---
name: specter-admin
description: >-
  Specter admin/dashboard APIs — configure your game programmatically: create projects and API
  keys, define currencies, items, bundles and stores, create tasks/achievements/missions and
  task groups, battle passes, level systems, leaderboards, competitions/tournaments, schedule
  live-ops events, configure matches, and manage team members. Use when setting up or changing
  game CONFIGURATION via API (as opposed to player-facing client calls), bulk content creation,
  or automating dashboard workflows.
---

# Specter Admin — configure your game via API

## ⚡ First: use the Specter MCP server if it's connected

If the **`specter` MCP server** is available (tools named `specter_create_currency`,
`specter_create_item`, `specter_list_*`, `specter_login`, etc.), **use those tools** to configure
the backend — do NOT hand-roll the raw admin HTTP calls below. The MCP server handles
authentication for you (a one-time browser sign-in), auto-detects the project, and clears the
gateway. The raw API reference below is for when the MCP server is *not* connected, or for
generating standalone scripts.

**Never ask the user for their dashboard email/password.** Member auth happens through a browser
sign-in, not a pasted password. If a create/configure action needs auth:
- With the MCP server: just call a create tool — it triggers `specter_login` (browser) when
  needed, or tell the user to run `npx -p specter-skills specter-mcp login` once.
- Without the MCP server: tell the user to set up the `specter` MCP server (see the package
  README) and sign in — then ask again. Do not collect a password to call `member/sign-in`.

---

Everything the dashboard (https://console.specterapp.xyz) does, the admin API can do —
useful for bulk content import, IaC-style game config, and CI pipelines.

**This API mutates live game configuration.** Two standing rules when generating admin
integrations:
1. Always show the user what will be created/changed and get confirmation before calling
   mutating endpoints — especially `*/delete` (destructive, archive/soft-delete).
2. Run against a dev/staging project first; admin changes are immediately visible to clients
   using that project's api-key.

## Achievements — the four types (task / mission / step-series / time-series)

When a user asks to "configure an achievement / quest / mission / challenge / streak", first
pick the right type. There are **four**, split across **two endpoints**:

| Type | Endpoint | Discriminator | MCP tool | Use when… |
|---|---|---|---|---|
| **Single task** | `task/create` | — | `specter_create_task` | one objective → one reward ("win 10 matches", "log in today") |
| **Mission** | `task-group/create` | `typeId: 1` | `specter_create_mission` | a **pool** of tasks; player sees/does a subset per cycle ("daily missions", "rotating challenges", `noOfMissionsPerCycle`) |
| **Step series** | `task-group/create` | `typeId: 2` | `specter_create_step_series` | **sequential** — finish step 1 to unlock step 2 ("quest line", "tutorial chain") |
| **Time series** | `task-group/create` | `typeId: 3` | `specter_create_time_series` | per-window **streak** ("login 7 days in a row", "weekly, resets on miss"; `stageLength` + `interval`) |

**Routing signals:** "pool / pick N / rotate / daily missions" → mission. "then / after / locked
until previous / chapters" → step series. "streak / N days in a row / resets if you miss" → time
series. A single trigger→reward with no sub-steps → task.

**Two-step lifecycle — create does NOT go live.** `*/create` only defines the achievement
(`status: created`). You must then call **`specter_schedule_achievement`** (→ `task/schedule` or
`task-group/schedule`) with dates/recurrence to activate it. Always tell the user it's created
but not live, and offer to schedule it. `specter_stop_achievement` halts it (reversible);
`specter_delete_achievement` soft-deletes.

**Verified shape gotchas (these cause silent 500s if wrong — the MCP tools handle them for you):**
- `task/create` and each inner `taskDetails[]` need **present-but-empty** scaffolding because the
  controller reads `.length`: `rewardDetails:[]`, `levelDetails:[]`, `linkedRewardDetails:[]`, and
  `config` — but **`config` is `[]` (array) on a single task and on each inner taskDetails, while
  the group-level `config` is `{}` (object)**. Do not unify them.
- A reward's `currencyId` and `progressionMarkerId` are **INTEGER ids** (from `currencies/get` /
  `progression-marker/get`); `itemId` / `bundleId` / `rewardSetId` / `levelSystemId` are **UUIDs**.
  The MCP `rewards:[{currency|item|bundle|marker, quantity}]` param resolves these for you.
- A task's trigger is `customEventId` (a **custom event's UUID** from `app-event/get/custom`, NOT
  its slug) or `defaultEventId`; provide exactly one. Create the event first with
  `specter_create_event` if it doesn't exist.
- Recurrence `intervalUnitId` / time-series `stageIntervalUnitId` share one mapping (verified from
  the `leaderboardIntervals` seed): **1=day, 2=week, 3=month, 4=year, 5=all_time, 6=custom,
  7=minute, 8=hour.** (Some older docs say 1=hour — that is wrong.)
- `rewardClaim` is `automatic` | `on-claim`. **This project keeps only `on-claim` live** — default
  to `on-claim` and confirm before using `automatic`.

The full verified per-type request bodies are in
[references/admin-endpoints.md](references/admin-endpoints.md#achievements--the-four-types).

## Auth

Admin endpoints are **member**-scoped (a dashboard team member, not a player) and send
`Authorization: Bearer <token>`. Access is org-based with RBAC. Admin routes have **no `/client/`
prefix** and are versioned (v1 default).

**How to get that token — do NOT ask the user for a password:**
- **Preferred (MCP server):** the `specter` MCP server obtains and stores it via a one-time
  browser sign-in (`specter_login` / `npx -p specter-skills specter-mcp login`). Email/password,
  Google, and Apple all work, and nothing is pasted into the chat.
- The legacy `POST member/sign-in { email, password }` exists, but only the dashboard/login UI
  should call it. When you need admin auth, route the user through the MCP browser sign-in
  instead of collecting credentials.

## The standard setup workflow

Configuring a new game end-to-end, in dependency order:

```
1. app/add                    → project (returns default game + api keys)
2. currencies/add             → soft + hard currencies
3. items/add, bundle/create   → content
4. store/create               → storefront with categories
5. match/add                  → match templates (team size, matchmaking rules)  [if multiplayer]
6. level-system/create, progression-marker/create                              [if progression]
7. task/create, task-group/create        → achievements/missions (+ rewardDetails)
8. battlepass/create          → seasonal pass with tiers
9. leaderboard/create, competitions/create
10. live-ops/schedule         → activate scheduled content (tasks, competitions, battlepass)
11. member/invite/send        → team access
```

Most entities follow the same CRUD shape: `<entity>/add|create`, `<entity>/edit|update`,
`<entity>/get` (paginated: `projectId`, `pageNo`, `pageSize`, `search`), and sometimes
`<entity>/delete` (soft-delete). Nearly every request needs `projectId`.

## Orchestrating a whole game from a plain-English brief

When the user describes a game in one breath ("a gacha RPG with soft + hard currency, a gem store,
and daily quests"), don't just start firing create calls. Run this disciplined flow:

1. **Plan.** Decompose the brief into concrete entities in **dependency order** (currencies →
   events → items/bundles → stores → progression → tasks/missions → battlepass → leaderboards/
   competitions → schedule). Many things reference others, so earlier steps must exist first:
   tasks need their **event** and reward **currency**; bundles/stores reference items + currencies;
   battle passes reference a **level system**; rewards reference currencies (int id) / items (UUID).
2. **Preview & confirm.** Show the user the full list of what you'll create (names + key fields)
   and **get a single explicit confirmation before any mutation** — this honours the standing
   "no mutations without permission" rule and lets them correct names/amounts up front. Prefer the
   **staging** environment.
3. **Create in order**, reusing each step's returned ids/slugs in the next. With the MCP server the
   resolvers do the id-wiring for you (pass slugs/names; it resolves event slug→UUID, currency
   slug→int id, etc.). Create a missing trigger event (`specter_create_event`) before the task that
   needs it.
4. **Verify.** Run `specter_verify_setup` (or list each entity) to confirm counts, and surface
   anything that failed rather than reporting blanket success.
5. **Activate.** Remember create ≠ live: schedule tasks/groups (`specter_schedule_achievement`) and
   competitions/leaderboards (`live-ops/schedule`) the user wants live now.
6. **Prove it (optional but recommended).** Use the client/runtime tools to act as a test player —
   `specter_send_event` to fire a trigger, `specter_test_achievement` to confirm a quest responds,
   `specter_get_player_state` to check the wallet — so the user sees the config actually working.
7. **Hand off to the game.** Offer `specter_generate_client_code` (JS or Unity C#) so the dev can
   drop the matching client calls straight into their game.

Idempotency note: a soft-deleted task/currency keeps its slug reserved, so re-running a setup with
the same `taskId`/`currencyId` throws a "Validation error" — vary the slug or edit the existing
entity instead of recreating it.

## Live-ops scheduling

Content isn't live until scheduled. `task/schedule`, `task-group/schedule`,
`battlepass/schedule` take start/end dates + recurrence; competitions/leaderboards use
`live-ops/schedule` / `live-ops/reschedule` / `live-ops/pause` / `live-ops/cancel`.
Scheduling drives the instance cycles that client APIs report (`instanceId` in task status,
leaderboard intervals).

## Key cross-references

- Task `businessLogic` / `config` JSON uses the same rule semantics the client skill documents:
  see specter-progression `references/task-rules.md`.
- After admin changes, client catalog endpoints (`app/get-*`) reflect them immediately —
  but client-side caches (yours) won't.

## Full endpoint reference

- **Curated quick reference** (per-domain tables + the verified `task/create` shape and
  the slug-vs-UUID event gotcha): [references/admin-endpoints.md](references/admin-endpoints.md)
- **Complete generated reference** — every admin endpoint (215, grouped by domain) with its
  request DTO: required fields, types, enums, examples, and nested objects. Generated from the
  backend OpenAPI spec, so it's exhaustive even where examples are sparse:
  [references/endpoints-index.md](references/endpoints-index.md)

When you need the exact fields for an admin call, open the matching file under
`references/endpoints/` (e.g. `task-create.md`, `currencies-add.md`,
`leaderboard-create.md`). The spec's `required` list is the validator's bare minimum — some
endpoints also read arrays like `levelDetails`/`linkedRewardDetails` and throw if they're
absent, so when a "required" set looks too small, cross-check the curated reference above.


## Product manual (concepts & terminology)

The Specter **user manual** (the same docs game designers read in the dashboard) is bundled in
[references/manual-index.md](references/manual-index.md) — read it to understand the CONCEPTS and
intent behind this domain (what each type/feature means, how dashboard workflows map to the API),
then pair it with the endpoint references for exact request shapes.
