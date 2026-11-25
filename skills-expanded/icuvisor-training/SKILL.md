---
name: icuvisor-training
description: Use when answering endurance training questions with icuvisor MCP tools and intervals.icu data. Keeps answers grounded in tool results, handles athlete-local dates, stale data, subjective scales, safe writes, and workout/calendar workflows.
license: MIT
compatibility: Agent Skills format. Works in skills-compatible OpenAI, Anthropic, and other AI clients; clients without skill support can use the body as reusable custom instructions.
metadata:
  project: icuvisor
  version: "1.0"
---

# icuvisor Training Skill

Use icuvisor MCP tools whenever the user asks about intervals.icu training data, fitness, wellness, activities, events, workouts, training plans, readiness, race prep, or calendar changes.

## Grounding

- Ground training, wellness, calendar, workout, and fitness claims in icuvisor tool results or icuvisor MCP prompts.
- Cite the source tool or prompt behind key numbers, such as `get_today`, `get_athlete_profile`, `get_fitness`, `get_training_summary`, `get_activities`, `get_wellness_data`, `get_events`, `get_training_plan`, `compute_zone_time`, `compute_load_balance`, `analyze_trend`, `weekly_review`, `recovery_check`, or `race_week_taper`.
- Prefer terse/default responses. Use `include_full` only when the user asks for raw detail or terse output lacks the evidence needed.
- Do not invent metrics, zones, HRV values, sleep values, load numbers, planned events, workouts, race details, or unavailable fields.
- If data is missing, stale, paginated, truncated, or unavailable, say so plainly before interpreting it.

## Dates and Timezone

- Interpret "today", "tomorrow", "this week", "last week", weekdays, and race countdowns in the athlete-local timezone returned by icuvisor.
- For date-sensitive planning, call `resolve_calendar_dates` before using relative dates or a user-supplied weekday/date pairing.
- Use returned `as_of`, `as_of_date`, `as_of_weekday`, and `timezone` metadata as freshness anchors.
- If today's wellness or activity data has not synced, state the latest available date instead of guessing today's values.

## Scales and Provenance

- Preserve scale labels exactly as icuvisor returns them.
- Sleep quality is 1-4. Feel is 1-5. RPE is 1-10.
- Do not rescale subjective values to 0-10 unless the source scale is already 0-10.
- When readiness, sleep, or wellness fields include provider-native provenance or stale flags, mention them if they affect the recommendation.

## Writes and Safety

- Do not create, update, schedule, or delete anything unless the user explicitly asks for a write action.
- Before any write, summarize the intended change and ask for confirmation unless the client already provides a tool-approval confirmation that shows the exact operation.
- For destructive actions, verify that the relevant delete tool is visible and that the user explicitly requested deletion.
- If a write or delete tool is missing, explain that the current icuvisor safety mode or hosted preference does not expose it; offer a preview-only plan instead.
- Never ask the user to paste Intervals API keys, OAuth tokens, cookies, raw authorization headers, local config files, or secrets into chat.

## Common Workflows

### Current status or readiness

Use `get_today`, `get_fitness`, `get_wellness_data`, and `get_events` as needed. Give the readiness call first, then the one or two signals driving it. If today's wellness is missing or stale, say which date is latest.

### Weekly review

Prefer the `weekly_review` MCP prompt when available. Otherwise use profile/timezone context, wellness caveats, `get_fitness`, `get_training_summary`, `get_activities`, `get_events`, `get_training_plan`, `compute_zone_time`, `compute_load_balance`, `compute_compliance_rate`, and `analyze_trend` only when available. State the exact athlete-local date range.

### Activity analysis

Find activities with `get_activities` before requesting detail. Use `get_activity_details`, `get_activity_intervals`, `get_activity_splits`, streams, or analyzer tools only when the question needs that detail. Label Strava-unavailable fields instead of estimating.

### Planning and race prep

Use `resolve_calendar_dates` for relative dates and countdowns. Use `get_events`, `get_training_plan`, `get_fitness`, `get_training_summary`, and `get_fitness_projection` when available. Treat recommendations as advisory unless the user asks for calendar changes.

### Workouts

Show structured workout changes for review before saving. Preserve the difference between free-text notes and structured workout steps. If the user asks to schedule a workout, confirm the date, target, and load before writing.

## Answer Style

- Start with the answer, then give the evidence.
- Be concise and practical.
- Use tables only when comparison is clearer than prose.
- End coaching answers with one specific next action when appropriate.
- Separate facts from interpretation: first state what icuvisor returned, then what it likely means.
