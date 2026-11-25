---
name: jobctl
description: Track the user's job applications in jobctl (app.jobctl.app) via the connected jobctl MCP tools. Use whenever the user mentions applying to a job, recruiter contact, interview scheduling, offers/rejections, salary asks, or asks what's next in their job search. Requires the jobctl MCP server to be connected.
---

# jobctl — job application tracking

jobctl is the user's job-application tracker. **You are the primary writer**: whenever the user mentions anything about their job search, record it via the `jobctl` MCP tools without being asked. The user reads and plans in the dashboard at https://app.jobctl.app.

## Core rules

1. **Record immediately.** "I applied to Bosch" → `add_application` (or `update_application` to `applied` if the card exists). Don't ask permission for routine tracking; do tell the user what you recorded.
2. **One card per company+role.** Before adding, `list_applications` to check for an existing card; the API also returns `duplicates` warnings — if present, update the existing card instead.
3. **Keep the timeline honest.** Recruiter calls, sent messages, feedback → `add_note`. Status changes are logged automatically.
4. **Save your analysis — it is product data, not chat.**
   - Vacancy fit assessment ("why this role fits, gaps, level/salary advice, process notes") → `match_notes` field (markdown, ≤20 KB) on add/update.
   - Company research (business, culture, comp bands, risks, interview process, sources) → `attach_analysis` (markdown, ≤100 KB, replaces previous).
5. **Always set `next_action` + `next_action_due`** so the user's "Needs your attention" list stays useful. Clear it when done, set the next one.

## Statuses

`started_apply` → `waiting_referral` (parked on a referral ask, not yet submitted) → `applied` → `waiting` → `interview_1` → `interview_2` → `offer` → `accepted`.
Terminal: `rejected`, `no_response`, `withdrawn`, `on_hold`. `archived` = old campaigns only (excluded from analytics).
Setting `applied` auto-stamps `applied_at` with today when empty.

## Raw one-liners

`add_application({raw: "..."})` parses: `"Company, Role, prio A|B|C, due <date>, remote|hybrid|onsite, via <source>, https://…, in <location>, applied <date>"`. Dates are DD/MM or natural ("friday"). Salaries are integer EUR (e.g. 120000).

## Interviews

`log_interview` with `scheduled_at` (ISO, timezone!), `attendees` `[{name, url?}]` (LinkedIn profiles), `links` `[{label?, url}]` (prep material, meeting link), `status` planned|done, `recap` after it happened. Max 10 per application. The soonest upcoming one drives the card's next-interview date.

## Good instincts

- Recruiter reached out from a company → contact + note, ask the user if they want to pursue.
- Rejection email → status `rejected` + note with the reason; never delete the card.
- User weighing an offer → put numbers into `salary_asked`/`salary_range_min`/`salary_range` and summarize trade-offs in a note.
- Job posting pasted → assess fit honestly (strengths AND gaps), add the card with your assessment in `match_notes`, recommend priority A/B/C and a salary ask.
