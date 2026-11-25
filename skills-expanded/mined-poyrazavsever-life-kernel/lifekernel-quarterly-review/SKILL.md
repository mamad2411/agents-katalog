---
name: lifekernel-quarterly-review
description: Step back once a quarter to check direction, goal horizons, and the balance between areas in a Life Kernel vault, and set the next quarter's direction.
---

# Quarterly review

Run only when the user starts it or accepts an offer you made because `ritual_status` showed it due. Expect 30-45 minutes. Converse in the user's language.

## Gather

1. Call `vault_list`, then `context_bundle` for the personal vault.
2. Call `ritual_agenda` with `ritual: "quarterly-review"`. It returns the quarter's dates, whether the quarterly note exists, the quarter's energy, focus, and circle counts, active goals by horizon with their linked active projects, the quarter's monthly reviews, the active areas, and `insights` for the quarter.
3. Read the completed monthly reviews, `profile/Profile.md`, and the long-term goals. Read only what you need.

## Think, then talk

This is about direction, not tasks. Cover: whether short-term goals were met or should move to a longer horizon, whether long-term goals still matter and why, which areas received attention and which were neglected, and how observed capacity compares with what the user expected. Quote dates and notes, and ask the user to correct your reading before you write anything.

## Decide

Let the user restate what matters for the next quarter. Offer to change goal horizons (`horizon`), retire goals, or add a goal only when the user names it. Agree on a short direction for the quarter: what to pursue, what to protect, and what to stop.

## Write

Follow the write protocol in the daily-circle skill.

- Create the quarterly note on route `quarterly` with the sections of the quarterly review template; the route keeps one note per quarter (`reviews/2026-Q4.md`). If `reviewNote.exists`, update it instead.
- Change goals with `set_frontmatter` on route `goal` (`status`, `horizon`, `target_date`); it needs the user's yes and `approved: true`. Create a new goal on route `goal` only when the user asked for it.
- Record decisions on route `decision`, and update `state/Current State.md`.
- When the review is finished, set the quarterly note's `status: "complete"`. If the user skips the quarter, set `status: "skipped"` and record the reason.

Close with the direction for the quarter in three lines or fewer.
