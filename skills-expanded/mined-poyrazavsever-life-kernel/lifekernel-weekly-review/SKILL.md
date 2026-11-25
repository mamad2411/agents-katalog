---
name: lifekernel-weekly-review
description: Review one week of evidence in a Life Kernel vault and adjust next week's commitments to real capacity.
---

# Weekly review

Run only when the user starts it, typically after a daily circle on their chosen review day (see `system/Method.md`), or accepts an offer you made because `ritual_status` showed it due. Converse in the user's language.

## Gather

1. `vault_list`, then `context_bundle` for the personal vault (raise `recentDaily` to 7).
2. Call `ritual_agenda` with `ritual: "weekly-review"`. Its `insights` hold the week's numbers: energy and its weekday pattern, focus against stated capacity, ritual consistency, and tasks planned again and again, with `observations` that already cite their evidence. It returns the week's dates and key, whether this week's review note exists (update it instead of creating another), each day's `energy`, `focus_hours`, and `circle` with totals, tasks completed this week, tasks overdue by the week's end, active projects untouched all week, the week's decisions, outcomes other vaults sent here (`outcomes`, each linking to its source), last week's commitments, and stated and observed capacity, each with its source.
3. Read the daily, project, and session notes behind anything you want to discuss. Read only what you need.
4. Read `system/Method.md` for the review rules.

## Think, then talk

Distinguish what the notes show from what you guess. Cover: outcomes completed, work that stalled and the reasons the user gave, energy and start patterns (from the daily fields, citing dates), days without a circle, overdue tasks, unexpected work, open loops, and planned versus observed capacity. Report one or two patterns the evidence supports; start from `insights.observations`, quote their numbers and dates, and never stretch them into a diagnosis. Quote dates, not impressions. Ask the user to correct your reading before you write anything.

## Decide

Propose a small set of commitments for next week that fits *observed* capacity, not the stated one. Respect the method's rules and the protected buffer. Do not silently carry over unfinished work; choose again. The user decides; record what they accept as decisions and leave the rest as proposals.

## Write

Follow the write protocol in the daily-circle skill.

- Create the weekly note on route `review` using the weekly review template sections. The route keeps one note per ISO week (`reviews/2026-W40.md`); `sourceDate` picks the week.
- Update `schedule/Capacity.md` "Observed capacity" (route `plan`), citing the review note.
- Update `schedule/Near-Term Plan.md` and `state/Current State.md`.
- Record decisions on route `decision`. A new decision starts `proposed`; when the user accepts it, set `status: "accepted"` and `decided_on` with `set_frontmatter`. Both need the user's yes and `approved: true`.
- Link project changes to the canonical project note instead of copying tasks.
- When the review is finished, set the weekly note's `status: "complete"` with `set_frontmatter`. If the user skips the week, set `status: "skipped"` and record the reason; it is evidence, not failure.

Close with: the honest summary, the patterns, next week's commitments, and what you changed.
