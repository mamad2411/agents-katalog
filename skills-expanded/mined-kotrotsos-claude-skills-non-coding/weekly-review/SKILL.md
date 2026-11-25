---
name: weekly-review
description: Use this skill on Fridays or end-of-week to produce a personal weekly review covering what got done, what slipped, what to carry, what to kill, and who needs follow-up. Triggers on phrases like "weekly review", "Friday review", "wrap up the week", or when the user references their Friday wrap-up practice. Removes the first-paragraph problem that kills most weekly review practices.
---

# Personal Weekly Review

## When to use this skill

It is Friday afternoon, or whenever the user does their weekly close. Most knowledge workers know they should do a weekly review. Most stop after three weeks because starting from a blank page on Friday afternoon is too hard. This skill removes the first-paragraph problem by drafting the review from the week's actual data.

## Input the user provides

- The week's calendar entries (or pointers to them)
- Completed tasks if logged in a system
- Meeting notes from the week
- Slack threads or emails representing major conversations
- Optionally: open commitments from the prior week's review

## What this skill does

1. Reads through the week's data
2. Identifies what got done vs. what was planned
3. Surfaces what got dropped, slipped, or actively killed
4. Flags follow-ups the user owes to specific people
5. Suggests what to carry into next week vs. what to drop
6. Produces a 200-300 word review in the user's voice, ready to file or send to a chief of staff

## Output structure

```
# Week of [date range]

## What got done
- [Concrete deliverable 1]
- [Concrete deliverable 2]
- [Concrete deliverable 3]
- [Meeting / decision that mattered]

## What slipped
- [Planned thing that did not happen, with one-sentence reason]
- [Thing that got partially done]

## What I am carrying into next week
- [Specific commitment with deadline]
- [Specific commitment]

## What I am killing
- [Item being formally dropped, with rationale]

## Follow-ups I owe
- [Name]: [what I promised, by when]
- [Name]: [same]
- [Name]: [same]

## One thing I noticed
[Single observation about the week worth keeping. Not a lesson, not a moral. A noticing.]
```

## Calibration notes

- 200-300 words total. Longer reviews do not get written.
- The "What I am killing" section is the most important and the most skipped. Force it. If nothing is being killed, the user is accumulating commitments and will burn out.
- The "Follow-ups I owe" section is where this skill earns its keep operationally. Most weekly slips happen because the user forgot they promised someone something. Surface these explicitly.
- The "One thing I noticed" is not a takeaway. It is a small observation. Examples: "Three meetings this week were about onboarding." "The decision on vendor X has been deferred four times." "I keep saying yes to coffee chats that do not move work forward." This section gives the review value beyond task accounting.
- Voice should match the user's. Short. Direct. No moralizing. The review is for the user, not for performance.

## What this skill does NOT do

- Does not write a performance self-evaluation (different purpose)
- Does not produce a status report for managers (different audience)
- Does not generate goals or OKRs (separate planning practice)
- Does not predict next week's outcomes (review is retrospective only)

## When NOT to use this skill

- Week with major disruption (illness, family event, etc.) where normal cadence does not apply
- Vacation week (use a separate "return to work" prep instead)
- First week in a new role (use an onboarding journal instead)
