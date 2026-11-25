---
name: lifekernel-onboarding
description: Interview a new user and fill a Life Kernel vault with their profile, goals, responsibilities, availability, and chosen planning method.
---

# Onboarding

Use when the user asks to set up or personalize a new vault, or when `system/Method.md` is blank. Expect 15-30 minutes. Accept voice transcripts and answers in any order. Converse in the user's language; note headings stay as the templates have them.

Setup: call `vault_list`, choose the vault, call `context_bundle`, and read what is already filled so you never re-ask it.

## Interview, in batches

Ask two or three related questions at a time, never a form. Cover, in roughly this order:

1. **Roles and responsibilities.** What they do now (work, study, family, health, community, content) and what has no end date. These become areas.
2. **Goals.** What they want in the short term (up to ~3 months), medium term (3-12 months), and long term. Ask why each matters and how they would know it is done.
3. **Projects.** Bounded efforts in progress, each with its outcome and next action.
4. **Availability.** Fixed commitments, flexible windows, protected rest, known exceptions.
5. **Capacity.** What a good day and a bad day look like. Record stated capacity as stated; observed capacity comes later from reviews.
6. **Friction.** What keeps going wrong in planning today.
7. **Privacy.** Topics to keep off-limits (`ai_access: none`) or restricted.
8. **Method** (below).

Separate what the user stated from what you suggest. Leave unknown values blank. Never infer sensitive facts about health, money, or relationships. A rough timing such as "in June" or "in January" is not a date: never choose a day, a month-end, or a year for the user. Leave `target_date` blank (or ask), and write the rough timing in the goal's text.

## Choosing a planning method

Do not impose one. Offer options with their trade-offs and let the user pick or mix:

- **Themed days**: each weekday has a main theme; good for many unrelated areas.
- **Time blocks**: protected windows per area; good for fixed schedules and deep work.
- **Daily top three + weekly outcomes**: light and outcome-focused; good for people who dislike schedules.
- **Minimal**: only the daily circle and a weekly review; good for starting small.

Also ask: when (if at all) they want a morning plan, their usual circle time and length, which questions to always or never ask, their weekly review day and time, whether they want monthly and quarterly reviews, quiet hours when nothing should prompt them, what the agent may update without asking (default suggestion: the near-term plan, current state, ticking tasks the user says they finished, and project next actions), what it must always confirm (default: profile, accepted decisions, goals), and the tone they want.

Record the rhythm as `system/Method.md` frontmatter with `set_frontmatter` on route `method`, so `ritual_status` can tell when each ritual is due. Leave a key blank to turn that ritual off.

| Key | Example | Meaning |
| --- | --- | --- |
| `morning_plan_time`, `morning_plan_days` | `"08:30"`, `"weekdays"` | Morning plan; days are `daily`, `weekdays`, `weekends`, `mon,wed`, or `mon-fri` |
| `daily_circle_time`, `daily_circle_days` | `"21:30"`, `"daily"` | Evening circle |
| `weekly_review_day`, `weekly_review_time` | `"sun"`, `"20:00"` | Weekly review |
| `monthly_review_day`, `monthly_review_time` | `"last-sun"`, `"19:00"` | Monthly review; day is a number, `last`, `first-mon`, or `last-sun` |
| `quarterly_review_day`, `quarterly_review_time` | `"last-sun"`, `"18:00"` | Quarterly review, in the quarter's last month |
| `quiet_hours` | `"23:00-08:00"` | No prompts in this window |

## Propose, then write

Show a compact map: areas, goals by horizon, projects, availability summary, and the method. Create only areas and projects that have real content. Ask for confirmation once.

Then write, following the write protocol in the daily-circle skill:

- `system/Method.md` (route `method`), `profile/Profile.md` (route `profile`), `schedule/Availability.md` and `schedule/Capacity.md` (route `plan`), `state/Current State.md` (route `state`): fill sections with `update_section`, copying headings exactly.
- One note per goal (route `goal`), area (route `area`), and project (route `project`) using the templates' sections; link each from `goals/Goals`, `areas/Areas`, or `projects/Projects` with `append`. Pass known frontmatter as `fields`: `horizon` and `target_date` for goals, `next_action` and `due` for projects. Write project tasks as checklist items (`- [ ] Task 📅 2026-10-04`).
- A session note (route `session`) recording that onboarding happened and what was decided.
- Routes with policy `review` need the user's yes from the confirmation step, then `approved: true`.

Finish by telling the user the one thing to do next: start the first daily circle tonight.
