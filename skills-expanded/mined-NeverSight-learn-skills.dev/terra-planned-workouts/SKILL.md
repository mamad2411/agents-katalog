---
name: terra-planned-workouts
description: Build with the Terra API Planned Workouts product (pre-release) – define a structured workout once and Terra API pushes it to users' devices. Use when pushing planned or structured workouts to Garmin, COROS, Wahoo, Suunto, TrainingPeaks, Huawei, Zepp, Hevy, or Apple watches, building training plans or workout templates, working with intervals, warmups, targets (HR, power, pace, cadence, RPE, zones), FTP or threshold-based personalization, athlete parameters, swimming or strength templates, or handling provider coercion warnings when a device cannot represent a feature.
license: MIT
compatibility: Requires network access to docs.tryterra.co for the full Garmin exercise catalog and payload examples
metadata:
  author: terra
  version: "1.0.0"
---

# Terra API Planned Workouts

Push structured workouts directly to your users' fitness devices. Define a workout template once, and the Terra API syncs it to whatever device the user has connected: Garmin, COROS, Wahoo, Suunto, TrainingPeaks, Huawei, Zepp, Hevy, or Apple. This is a write-to-device product, the inverse of the read-focused Terra API Health & Fitness data flow.

> **Pre-release.** This product is pre-release. Endpoints, fields, and provider behavior may change before general availability. Facts here are drawn from the Terra API docs; verify against [docs.tryterra.co/planned-workouts-api](https://docs.tryterra.co/planned-workouts-api) before shipping.

## When to Apply

Reach for this skill when you are:

- Pushing a planned or structured workout to a user's watch or bike computer
- Building reusable workout templates or training plans in an app
- Working with intervals, warmups, cooldowns, and repeat blocks
- Setting HR, power, pace, speed, cadence, RPE, or zone targets
- Personalizing one template per athlete via FTP, max HR, or threshold values
- Handling `coercion_warnings` when a provider cannot represent a feature

## Two-Phase Workflow

Base URL `https://access.tryterra.co/api/v2`. Every request needs two headers: `dev-id` (your Terra developer ID) and `x-api-key` (your Terra API key).

**Phase 1 – Create a template (once).** `POST /workouts` with the workout structure returns a reusable `workout_id`. The template is generic: it holds structure and, where you want personalization, percentage-based targets.

**Phase 2 – Schedule to a user (per athlete).** `POST /workouts/{workout_id}/plan?user_id=X` applies that athlete's parameters (max HR, FTP, etc.) at scheduling time, converts percentage targets to absolute values, and pushes to the connected device. Returns a `planned_workout_id` (Terra API's ID) and a `provider_workout_id` (the device's ID).

```bash
# Phase 1: create a reusable template
curl -X POST "https://access.tryterra.co/api/v2/workouts" \
  -H "Content-Type: application/json" \
  -H "dev-id: YOUR_DEV_ID" -H "x-api-key: YOUR_API_KEY" \
  -d '{ "name": "Threshold Intervals", "sport": "cycling",
        "step_blocks": [{ "completion_condition": {"type":"reps","value":3},
          "steps": [{ "completion_condition": {"type":"time","value":600},
            "intensity_type": "active",
            "intensity_targets": [{"target_type":"power_percentage","value_low":95,"value_high":100}] }] }] }'
# → { "status": "success", "workout_id": "123" }

# Phase 2: apply this athlete's FTP and push to their device
curl -X POST "https://access.tryterra.co/api/v2/workouts/123/plan?user_id=USER_ID" \
  -H "Content-Type: application/json" \
  -H "dev-id: YOUR_DEV_ID" -H "x-api-key: YOUR_API_KEY" \
  -d '{ "planned_date": "2026-02-10", "ftp": 280 }'
# → 201 { "status": "success", "planned_workout_id": "67890", "provider_workout_id": "abc123" }
```

All Terra API IDs (`workout_id`, `planned_workout_id`) are serialized as JSON **strings**, because JavaScript clients lose precision on numbers past 2^53. The `plan` call returns HTTP 201 on success.

## Endpoints

| Method | Endpoint                          | Description                                                                                                                        |
| ------ | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/workouts`                       | Create a workout template, returns `workout_id`                                                                                    |
| GET    | `/workouts`                       | List all templates                                                                                                                 |
| GET    | `/workouts/{id}`                  | Get template details                                                                                                               |
| DELETE | `/workouts/{id}`                  | Delete a template. **Cascades** – see gotchas                                                                                      |
| POST   | `/workouts/{id}/plan?user_id=X`   | Schedule a template to a user, applying athlete params                                                                             |
| GET    | `/plannedWorkouts/{id}`           | Get one planned workout                                                                                                            |
| GET    | `/plannedWorkouts?user_id=X`      | List a user's scheduled workouts (optional `start_date` and `end_date` filters – **both required together**; one alone is ignored) |
| PATCH  | `/plannedWorkouts/{id}?user_id=X` | Update the scheduled date. **Only `planned_date`, never athlete params**                                                           |
| DELETE | `/plannedWorkouts/{id}?user_id=X` | Unschedule a workout for one user                                                                                                  |

## Data Model

A template is a hierarchy: `WorkoutTemplate → step_blocks[] → steps[] → intensity_targets[]`.

**WorkoutTemplate** – `name` (required), `sport` (required), optional `description`, `environment` (`indoor` / `outdoor` / `pool`), and `pool_length_meters` (swimming only). At least one block is required.

**step_blocks[]** – a group of steps executed together. The block's `completion_condition` controls repetition:

| Block condition                    | Behavior                      |
| ---------------------------------- | ----------------------------- |
| `{"type":"reps","value":4}`        | Repeat all steps 4 times      |
| `{"type":"time","value":1200}`     | Repeat until 20 minutes total |
| `{"type":"distance","value":5000}` | Repeat until 5 km total       |
| `{"type":"open"}` or omitted       | Execute once (no repeat)      |

**steps[]** – each step needs a `completion_condition` (defaults to `open` if omitted) and an `intensity_type` (required: `warmup`, `active`, `rest`, `recovery`, `cooldown`). Optional: `intensity_targets[]`, `notes`, `strength` (exercise details), `swimming` (stroke and equipment).

Completion condition types: `time` (seconds), `distance` (meters), `reps`, `calories`, `open` (manual lap), `hr_less_than` / `hr_greater_than` (BPM), `power_less_than` / `power_greater_than` (watts).

**intensity_targets[]** – the goal metric for a step. Three families:

- **Absolute** – `heart_rate` (BPM), `power` (watts), `speed` (m/s), `pace` (sec/km), `cadence` (rpm or spm), `rpe` (1-10). No athlete params needed.
- **Percentage** (needs athlete params at scheduling) – `heart_rate_max_percentage` (needs `max_heart_rate`), `heart_rate_threshold_percentage` (needs `threshold_heart_rate`), `power_percentage` (needs `ftp`), `speed_percentage` (needs `threshold_speed`).
- **Zone** – `heart_rate_zone` (1-5), `power_zone` (1-7). Providers convert to their native format.

Target value rules:

- **Absolute targets** accept either a single `value` or a `value_low`/`value_high` range. A single `value` auto-expands to a ±5% range on most providers, **except `rpe`, which stays a point value**.
- **Percentage targets** (`power_percentage`, `heart_rate_max_percentage`, `heart_rate_threshold_percentage`, `speed_percentage`) **reject a single `value` with a 400 at template creation**. Supply `value_low` and/or `value_high`; a lone bound is expanded to a ±5% range.
- Never send both `value` and `value_low`/`value_high` on the same target.
- For ranges, `value_low` must be **strictly less than** `value_high`.
- `pool_length_meters` is swimming-only; setting it elsewhere is invalid.
- Athlete metrics (`ftp`, `max_heart_rate`, `threshold_heart_rate`, `threshold_speed`, `pool_length_meters`) must be positive.
- Sanity ranges are **hard 400 rejections** at `POST /workouts`, not warnings: heart rate 30-250 BPM, power 1-2000 W, speed 0-15 m/s, pace 1-7200 sec/km, cadence 1-300, RPE 1-10, percentage targets 0-200%.

## Athlete Parameters

Templates are generic; personalization happens at scheduling time. Supply these in the `plan` request body:

| Parameter              | Unit   | Used by                                   |
| ---------------------- | ------ | ----------------------------------------- |
| `max_heart_rate`       | BPM    | `heart_rate_max_percentage` targets       |
| `threshold_heart_rate` | BPM    | `heart_rate_threshold_percentage` targets |
| `ftp`                  | watts  | `power_percentage` targets                |
| `threshold_speed`      | m/s    | `speed_percentage` targets                |
| `pool_length_meters`   | meters | swimming (overrides the template value)   |

Conversion is linear: `Absolute = Percentage × param / 100`. A `power_percentage` of 95-100 with `ftp: 280` becomes 266-280 W on the device; the same template scheduled with `ftp: 200` becomes 190-200 W. If a percentage target's required parameter is missing, the Terra API emits a coercion warning and falls back to a provider default rather than failing.

## Coercion Model

Providers differ in what they can represent. When a provider cannot express a feature exactly, the Terra API **adapts the payload, still creates the workout, and returns a `coercion_warnings[]` array**. Each warning is `{ "path": "...", "message": "..." }` pointing at the field that was changed and why.

```json
{
  "status": "success",
  "planned_workout_id": "12345",
  "provider_workout_id": "garmin_abc123",
  "coercion_warnings": [
    {
      "path": "workout.sport",
      "message": "Unsupported sport type: yoga. Defaulting to OTHER."
    }
  ]
}
```

Coercion is a success path, not an error. How you handle warnings is your choice: log them for debugging, surface a "some features were adjusted for your device" notice to users, or ignore informational ones. Read `references/coercion-scenarios.md` before relying on a feature that may not exist on the target provider.

## Gotchas

- **`DELETE /workouts/{id}` cascades and is irreversible.** It first removes every planned workout linked to that template from every user's device across every provider, then deletes the template. To unschedule one user without touching others, use `DELETE /plannedWorkouts/{id}` instead.
- **`PATCH /plannedWorkouts/{id}` updates only `planned_date`.** It never re-applies athlete parameters. To change targets or params, delete and re-plan.
- **Provider operations differ wildly.** Some providers do not support update, retrieve, or delete. An unsupported operation still returns a success response, so success does not always mean the device changed. Read `references/provider-compatibility.md` before targeting a specific provider.
- **COROS update = delete + recreate.** COROS has no in-place update, so an "update" deletes the old workout and creates a new one; the `provider_workout_id` changes.
- **Huawei is create-only, running-only, no scheduling.** No update, retrieve, or delete on the device. It ignores `planned_date` – the workout is available immediately and **always** returns a coercion warning noting this. Duplicate workout names per user are rejected with a 400. Non-running sports appear as a run.
- **Zepp has a 7-day sync window** (today to today + 6 days). Workouts scheduled outside the window are stored in Terra API's database but not pushed to the device until a later write or delete for that user triggers a window refresh. There is no background auto-sync.
- **Hevy is strength-only.** RPE targets are silently dropped with a warning, there are no block repeats (one block maps to one exercise, one step to one set), and it has no scheduling and no provider-side delete. Updates are supported: when a `provider_workout_id` exists, the existing Hevy routine is updated in place.
- **Apple syncs via the Terra iOS SDK.** The server queues the action; the SDK pushes to WorkoutKit and reports back via `POST /v2/plannedWorkouts/{id}/synced`. Until then `provider_workout_id` is `null`.
- **Garmin retrieve only returns workouts created by your own credentials.** Workouts made by other apps or on the device itself are invisible to your GET calls.
- **Deletes remove from Terra API's database but may leave the workout on the device** for providers without a delete endpoint (e.g. Huawei, Hevy).

## References

Read the reference file that matches your task before writing the request:

- **`references/provider-compatibility.md`** – the full operations matrix (create/update/retrieve/delete per provider) plus each provider's sport, target, completion, and structure support and special behaviors. Read this before targeting a specific provider.
- **`references/coercion-scenarios.md`** – the full catalog of coercion scenarios, handling patterns (log / surface / ignore), and a prevention checklist. Read this before relying on a feature a provider may not support.
- **`references/exercise-reference.md`** – exercise name normalization rules, the Garmin/Hevy flexibility table, and what happens when a name is not found. Read this before building a strength template.

Two things live in the docs rather than this skill, because they are large and change with the API:

- **The complete Garmin exercise catalog** (1,624 names, also used for Hevy): fetch https://docs.tryterra.co/planned-workouts-api/garmin-exercise-reference.md when you need to pick or verify a specific `exercise_name`.
- **Sport-specific payload examples** (running, cycling, swimming, strength, multi-sport): fetch https://docs.tryterra.co/planned-workouts-api/sport-specific-examples.md when you want a full working request body beyond the one in this file.

Full API documentation: [docs.tryterra.co/planned-workouts-api](https://docs.tryterra.co/planned-workouts-api) (append `.md` to any docs URL for a markdown version). If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch the docs instead.
