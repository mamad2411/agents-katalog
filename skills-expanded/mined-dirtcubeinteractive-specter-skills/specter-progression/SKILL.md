---
name: specter-progression
description: >-
  Specter progression systems — tasks, missions, achievements, daily/weekly quests, streaks,
  step series, task groups, custom game events, reward granting, battle pass tiers, XP and level
  systems, progression markers and ranks. Use for any "daily quests", "achievements", "missions",
  "battle pass", "season pass", "XP/levels", "player ranks" or "grant rewards" feature on Specter,
  and for designing task rules (how game events trigger task completion).
---

# Specter Progression — tasks, achievements, battle pass, levels

Base URL and headers: see the `specter` skill. Tasks, rules and rewards are **configured in the
dashboard**; the game's job is to (1) send events, (2) read status, (3) claim rewards.

## The core loop: events drive everything

```
game does something
  → POST /events/send-custom  (Bearer)  with event name + parameters
  → Specter queues the event and evaluates task rules asynchronously (rules engine)
  → matching tasks are marked completed; rewards granted per claim mode
  → game polls /tasks/get-status (or player/me/get-task-status) and updates UI
```

```json
POST /events/send-custom
{ "eventId": "match_finished", "customParams": { "score": 1500, "kills": 7, "won": true } }
```

`eventId` is the event's **dashboard-configured id (slug)**, e.g. `daily_streak_hit`. It is
NOT the `event.id` UUID that `get-tasks` returns inside task objects — sending that UUID fails
with `EventNotFoundException` (1119). Verified against staging. Put gameplay values in
`customParams` — task rule facts are matched against custom params. `specterParams` is for
platform-default parameters; don't put your own fields there.

**Validation is asynchronous** (queue + rules engine) — completion lands seconds later, not in
the response. Poll status when the player opens the quest screen; don't block gameplay on it.

## Task model (what you configure, what the engine does)

A task = trigger event + optional **parameters** (aggregations over the player's event history)
+ **business logic** (conditions). See [references/task-rules.md](references/task-rules.md) for
the full rule semantics. Task kinds:

| Kind | Behavior |
|---|---|
| One-time | Completes once per schedule cycle |
| Recurring | Resets each cycle (daily/weekly quests) |
| Cumulative (with parameters) | "Collect 1000 coins" — sums/aggregates event params over time |
| Streak / time-series | Last N events must *all* satisfy the condition |
| Step series | Staged progression through ordered steps |
| Task group / mission | Ordered set of tasks; group rewards on full completion |

Tasks can be **level-gated** (require a minimum level in a level system) and scheduled via
live-ops windows.

## Reading status & claiming

| Endpoint | Purpose |
|---|---|
| `get-tasks`, `get-missions`, `get-step-series`, `get-time-series` | Catalog of configured content (api-key) |
| `player/me/get-task-status` | Player's completion state per task (returns `status` and `instanceId` per schedule cycle) |
| `player/me/get-task-progress` | Numeric progress toward task parameters ("73/100") — use for progress bars |
| `player/me/get-task-group-status`, `player/me/get-time-series-progress` | Mission/step-series and time-series progress |
| `achievements/force-complete` | Client-authoritative completion (skip the rules engine — use sparingly, e.g. tutorial steps) |
| `achievements/grant-reward-by-source` | **The canonical "Claim" call** — server resolves the configured reward; pass `{ id, type: "task", instanceId }` (include `instanceId` for recurring tasks so the right cycle is claimed) |
| `achievements/grant-rewards`, `-single`, `-batch`, `-by-source-overrides` | Grant flows where the caller specifies reward contents — trusted/server contexts, not a player "Claim" button (a client naming its own reward amounts is a cheating vector) |
| `rewards` history endpoints | Audit what was granted |

Reward claim modes are set per task in the dashboard: **on-claim** (player presses "Claim" →
call grant) vs automatic. Current platform default in production: on-claim.

## Battle pass

`app/get-battlepasses` (seasons + status) → `battlepass/get-tier-list` (Bearer; tiers, XP
thresholds, free/premium reward tracks, player's unlocked state) → progress accrues via events →
`battlepass/unlock-battlepass-tier` to claim a tier's reward. New players are auto-enrolled in active
battle passes at signup.

## Levels & progression markers

- **Level systems** (`app/get-progression-systems`): XP curves / ranked divisions. Player
  position: `player/me/get-progress`.
- **Progression markers** (`app/get-markers`): named counters (XP, trophies…) backing those
  systems. Advance with `progression/update-marker` (Bearer) — e.g., +XP after a match. Level-ups
  computed server-side and can gate tasks, stores and content.

## Full endpoint details

All 21 endpoint DTOs and response examples: [references/endpoints-index.md](references/endpoints-index.md)
Task rule JSON semantics: [references/task-rules.md](references/task-rules.md)
Console walkthrough (event → task → reward, end-to-end verify): [references/dashboard-setup.md](references/dashboard-setup.md)
Working client code: [examples/javascript.md](examples/javascript.md)


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

## Task completion rules + reward claim flow

How a task actually COMPLETES (the coupled `config[]` + `businessLogic` rule, operators, cumulative/streak modes) and how its reward is CLAIMED (automatic vs on-claim, pending rewards via `get-reward-history`, claiming via `grant-reward-by-source`): [references/task-completion-and-rewards.md](references/task-completion-and-rewards.md). Verified against the backend.
