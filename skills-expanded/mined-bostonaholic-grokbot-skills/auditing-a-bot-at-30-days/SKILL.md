---
name: Auditing a bot at 30 days
description: >-
  Use monthly, or when a bot seems lazy, noisy, or ignored, to decide from run
  history whether each of its routines should stay, be rewritten, or be cut.
  Report only; changes nothing.
---
# Auditing a bot at 30 days

Use the run history, not memory of it. Report only; delete nothing.

## For every routine the bot owns
- How many of the last 20 runs succeeded (or unknown)
- How many produced output someone acted on or opened (or unknown)
- How many ended in "waiting for approval"
- Median run time (or unknown)

A routine that looks lazy is often one that has been quietly failing, so check failures before judging usefulness.

## Silence and autonomy score
Count over 30 days:
- messages to Matthew that needed nothing from him (unrequested updates, FYIs, long acks)
- messages to Matthew that asked for something (decisions, approvals, access, blockers)
- tasks finished without asking him anything

Score it **Quiet** if the first count is 0, **Noisy** if it's 1 to 3, and **Very noisy** above 3. Reward high autonomy with few asks. Any count above 0 is a fix to propose, with a link to each message.


**Access, not tasks (Matthew, Oct 25, 2026).** Score how the bot asks Matthew for help. Good: it names the specific permission or access it needs and where he grants it. Bad: it hands him a task to do for it. Watch for gaming, such as relabeling a task as "access" ("grant me access by doing X") or not asking at all and staying stuck. Counter-measure: count the asks that are really chores, and check that each access ask, once granted, led to the bot finishing the job itself.

## Answer in one line each
1. Which routine has produced nothing useful in 30 days?
2. Which one needs a person on every run, and at which step?
3. If you could delete one routine today, which one and why?
4. Can you say in one sentence what this bot is for?
5. What is its silence and autonomy score?

## Cut or rewrite signals
The rework costs more than the work saved; nobody reads the output; it needs a nudge every run; or its purpose doesn't fit in one sentence. Each is a role problem: propose the rewritten role or the routine to cut, and let the owner decide.

## Output
One short table per bot plus the four answers, with links to the run records. Mark every number observed or estimate.
