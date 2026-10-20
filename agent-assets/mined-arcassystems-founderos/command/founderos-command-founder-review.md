---
description: Your own monthly performance review. Say "review my month" or run /founder-os:founder-review. Counts a scorecard from your own files, asks at most five coaching questions, files at most three commitments with dates. Private by default.
argument-hint: "[YYYY-MM to score a specific month]"
allowed-tools: ["Read", "Grep", "Glob", "Edit", "Write"]
---

# Founder OS founder review

Run the founder-review skill at `skills/founder-review/SKILL.md` end to end.

## Procedure

1. Read `skills/founder-review/SKILL.md`.
2. If `$ARGUMENTS` names a month (`YYYY-MM`), score that month. Otherwise score the month just ended.
3. If a review for that month is already recorded in `brain/log.md`, say so and stop unless the founder explicitly asks for a re-run.
4. Run step 1 (scorecard), then step 2 (at most five questions), then step 3 (commitments into `cadence/queue.md`).
5. Close with the `brain/log.md` entry.

## Rules

- Counts come from files. A measure with no instrument reports "no instrument", never a guessed number.
- At most 3 commitments, each titled `Review commitment: <words>` with a date.
- Never write any part of this review into a file another person reads.
- No em dashes or en dashes. No banned words.
