---
name: Goals & Habits Tracker
description: Plan and track yearly and quarterly (3-month) goals with weekly check-ins and habit tracking, backed by a local SQLite database. Use when the user asks for yearly planning, quarterly/3-month planning, weekly reviews/check-ins, creating a new habit, stopping a behavior, logging habit progress, or summarizing goal/habit progress.
category: Productivity
keywords: planning, goals, habits, habit-tracking, tracking
tags: coaching, productivity, accountability
---

# Goals & Habits Tracker (Chat-Only, SQLite)

## Quick start
- Do not ask the user to run any commands; run these yourself as needed.
- Initialize (optional; the agent will auto-bootstrap on first chat):
  - `bash .codex/skills/goals-habits-tracker/scripts/goals bootstrap`
- View current dashboard (active goals, active habits, current-week habit summary):
  - `bash .codex/skills/goals-habits-tracker/scripts/goals dashboard`
- Habit progress summaries:
  - This week: `bash .codex/skills/goals-habits-tracker/scripts/goals habit-week`
  - This month: `bash .codex/skills/goals-habits-tracker/scripts/goals habit-month`
- Add a yearly goal:
  - `bash .codex/skills/goals-habits-tracker/scripts/goals add-goal --horizon year --year 2026 --area "Business" --focus "Own Apps" --title "Ship my app v1" --why "..." --success "..." --notes "..."`
- Add a 3-month goal (rolling window from today):
  - `bash .codex/skills/goals-habits-tracker/scripts/goals add-goal --horizon quarter --start today --months 3 --area "Health" --focus "Weight" --title "Reach 93-94 kg" --success "..."`
  - Note: quarter goals are auto-linked to a year goal (same year, best match by area/focus/title). If no suitable year goal exists, the tool will create one.
- Add a habit:
  - `bash .codex/skills/goals-habits-tracker/scripts/goals add-habit --area "Health" --focus "Training" --name "Gym" --kind build --cadence weekly --target 3 --notes "Strength + cardio"`
- Add a "stop doing" habit (quit habit; log `0` for success days, `>0` for slip days):
  - `bash .codex/skills/goals-habits-tracker/scripts/goals add-habit --name "Doomscrolling after 10pm" --kind quit --cadence daily --target 0`

## Operating rules (for Codex)
- Treat this as **chat-first coaching**:
  - Ask a few high-signal questions, propose a plan, then persist it.
  - Recommend keeping an "active set" small (top 3 priorities + 3-5 habits), but allow a larger plan/backlog if the user already plans that way (like the Area/Focus tables).
- Before writing new records, summarize what you'll save (titles, dates, cadence/targets) and ask for a quick "yes/no", unless the user explicitly says to just save it.
- Always start by reading current state:
  - `bootstrap`, then `dashboard`.
- Use the DB as the source of truth and return **JSON from scripts**, then translate it into a human-friendly summary in chat.

## First-run onboarding (chat-based)
When the skill triggers and there is no data yet:
1. Run `bootstrap`.
2. If `needs_onboarding == true`, run onboarding as a short conversation:
   - Ask **one question per assistant message**.
   - Include a 1-2 sentence explanation and a default choice.
   - After each user answer, persist it immediately via `prefs-set` / `areas-set`.
3. Onboarding questions (in order):
   - Week start:
     - Ask: "Do you want weeks to run Mon-Sun (recommended) or Sun-Sat?"
     - Explain: This affects weekly check-ins and weekly habit summaries.
     - Persist: `prefs-set --week-start mon|sun`
   - Timezone (optional):
     - Ask: "What's your timezone in IANA format (e.g. Europe/Madrid)? You can also say 'skip'."
     - Explain: Used for scheduling reminders/weekly check-in preferences later.
     - Persist: `prefs-set --timezone <iana>` (or empty if skipped)
   - Quit-habit tracking style:
     - Ask: "For 'stop doing X' habits, do you want to track (A) occurrences per day (0=clean, 1+=slips) or (B) boolean (0/1)?"
     - Explain: Occurrences gives more signal; boolean is simpler.
     - Persist: `prefs-set --quit-habit-tracking occurrences|boolean`
   - Areas/categories (optional):
     - Ask: "Do you want to define areas/categories now? If yes, list them comma-separated. Or say 'skip'."
     - Explain: Helps group goals like your Area/Focus tables; can always add later.
     - Persist: `areas-set --area ...` (or leave as empty list)
   - Weekly check-in preference (optional):
     - Ask: "Do you want a default weekly check-in day/time? Or say 'skip'."
     - Explain: Purely a preference; it doesn't create reminders by itself.
     - Persist: `prefs-set --weekly-checkin-day ... --weekly-checkin-time ...` (or empty if skipped)
4. Mark onboarding complete via `onboarding-complete`.
5. Start planning by asking for:
   - 3 example goals in the format `Area | Focus | Goal/Task` (Area/Focus optional if not using categories)
   - 1-3 habits to start tracking

## Intent -> actions
- "I want to do planning for the year":
  - `dashboard` -> use `references/prompts.md` (yearly) -> `add-goal` (year) + `add-habit` + `add-checkin --period year`
- "I want to do plans for another 3 months":
  - `dashboard` -> use `references/prompts.md` (quarterly) -> `add-goal` (quarter; auto-links/creates year parent) + `add-habit` + `add-checkin --period quarter`
- "I want to get new habit":
  - Ask kind/cadence/target -> `add-habit` -> optionally `link-habit-goal`
- "I want to stop doing {something}":
  - Create a quit habit via `add-habit --kind quit --target 0` (or a small allowed target) -> explain how to log it via `log-habit`

## Workflows
- Yearly planning / quarterly planning / weekly check-in prompts live in `references/prompts.md`.
- Schema details live in `references/schema.md`.

Recommended persistence pattern:
1. Collect answers in chat.
2. Create/update goals/habits via `add-goal` / `add-habit` (+ optional linking).
3. Save the planning/check-in session via `add-checkin` with a short `--summary` plus structured `--json` (file or stdin).

## Commands
- Setup:
  - `scripts/setup.sh`: create `.skills-data/goals-habits-tracker/` + `.env`
  - `scripts/goals`: wrapper that auto-runs setup when needed
- Database actions (all print JSON):
  - `init`, `bootstrap`, `dashboard`
  - `prefs-get`, `prefs-set`, `areas-get`, `areas-set`
  - `onboarding-complete`
  - `add-goal`, `list-goals`, `update-goal`
  - `add-goal-update`, `list-goal-updates`
  - `add-habit`, `list-habits`, `update-habit`, `link-habit-goal`
  - `log-habit`, `habit-week`
  - `add-checkin`, `list-checkins`

## Local data and env
- Store all mutable state under <project_root>/.skills-data/<skill-name>/.
- Keep config and registries in .skills-data/<skill-name>/ (for example: config.json, <feature>.json).
- Use .skills-data/<skill-name>/.env for SKILL_ROOT, SKILL_DATA_DIR, and any per-skill env keys.
- Install local tools into .skills-data/<skill-name>/bin and prepend it to PATH when needed.
- Install dependencies under .skills-data/<skill-name>/venv:
  - Python: .skills-data/<skill-name>/venv/python
  - Node: .skills-data/<skill-name>/venv/node_modules
  - Go: .skills-data/<skill-name>/venv/go (modcache, gocache)
  - PHP: .skills-data/<skill-name>/venv/php (cache, vendor)
- Write logs/cache/tmp under .skills-data/<skill-name>/logs, .skills-data/<skill-name>/cache, .skills-data/<skill-name>/tmp.
- Keep automation in <skill-root>/scripts and read SKILL_DATA_DIR (default to <project_root>/.skills-data/<skill-name>/).
- Do not write outside <skill-root> and <project_root>/.skills-data/<skill-name>/ unless the user requests it.
