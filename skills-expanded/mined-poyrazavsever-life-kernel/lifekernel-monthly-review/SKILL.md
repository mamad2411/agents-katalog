---
name: lifekernel-monthly-review
description: Review a month of evidence against the user's goals in a Life Kernel vault, decide what happens to each goal, and set the month's outcomes.
---

# Monthly review

Run only when the user starts it or accepts an offer you made because `ritual_status` showed it due. Expect 20-30 minutes. Converse in the user's language.

## Gather

1. Call `vault_list`, then `context_bundle` for the personal vault.
2. Call `ritual_agenda` with `ritual: "monthly-review"`. It returns the month's dates, whether the monthly note exists, the month's energy, focus, and circle counts, each active goal with the number of active projects linked to it, the month's weekly reviews with their status, and `insights` for the month (energy, focus against capacity, ritual consistency, tasks carried for days).
3. Read the completed weekly reviews and the goal notes that need a decision. Read only what you need.

## Think, then talk

Distinguish what the notes show from what you guess. Cover: what moved toward each goal, goals with no active project (`activeProjects: 0`), energy and capacity against the stated capacity, and weeks without a review. Quote dates and notes. Ask the user to correct your reading before you write anything.

## Decide

For each goal without movement, offer the options: keep it and start a project, park it (`status: "paused"`), finish it (`status: "done"`), or drop it (`status: "dropped"`). The user decides. Then agree on two or three outcomes for the coming month that fit observed capacity.

## Write

Follow the write protocol in the daily-circle skill.

- Create the monthly note on route `monthly` with the sections of the monthly review template; the route keeps one note per month (`reviews/2026-10.md`). If `reviewNote.exists`, update it instead.
- Change a goal's `status` or `target_date` with `set_frontmatter` on route `goal`; it needs the user's yes and `approved: true`.
- Record decisions on route `decision`.
- Update `schedule/Near-Term Plan.md` "This week" and `state/Current State.md` to reflect the month's outcomes.
- When the review is finished, set the monthly note's `status: "complete"`. If the user skips the month, set `status: "skipped"` and record the reason.

Close with the honest summary, the goal changes, and the month's outcomes.
