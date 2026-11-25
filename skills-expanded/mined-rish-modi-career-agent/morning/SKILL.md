---
name: morning
description: AM briefing that surfaces yesterday's open items, stale roles (>7 days untouched), and a single suggested first move. Read-only — surfaces context, persists nothing. Use when I say "/morning", "what's on my plate", "where did I leave off", or similar start-of-session prompts.
---

# Morning Briefing

## When to use
At the start of a work session, when the user wants to know what's open and where to start. Trigger phrases: "/morning", "what's on my plate today", "where did I leave off", "what's open".

For end-of-day logging, use `daily-summary` instead.

## What it produces
A short briefing — three sections, ~10–15 lines total. **Read-only**: doesn't write any files, doesn't modify state.

### Section 1: Carrying over from yesterday
Read the most recent file in `$PERSONAL/career/daily-log/` (sort by filename — they're ISO date-stamped). `$PERSONAL` is the personal-docs sibling directory defined in `CLAUDE.md`; resolve it once at the start of the session. Extract the `## Next steps` section and present each item as a checkbox.

If no daily log exists yet, say so explicitly ("No prior daily log found") and skip this section.

### Section 2: Stale items (>7 days)
Scan `$PERSONAL/applications/<company>/<role>/role.md` files. Flag any role where **all three** of these are true:
- `date_added` in frontmatter is more than 7 days ago
- No `resume.md` exists in the same folder
- The `## Notes` section is empty or unchanged from initial creation

These are roles that got triaged but never acted on. Cite each file path so the user can decide: act, archive, or ignore.

If nothing qualifies as stale, **omit this section entirely**.

### Section 3: Suggested first move
**One** concrete action, not a list. Pick the highest-leverage thing from sections 1 and 2 — usually a yesterday-open-loop that's blocking forward motion, or the most promising stale role.

Include a rough effort estimate ("~45 min", "~1 hr") so the user can decide if there's time for it now.

If the user has nothing pending (clean slate, no carryover, no stale items), suggest a fresh activity grounded in `$PERSONAL/career/goals.md`, e.g., "Start a Job Description analysis for a Tier 1 company you haven't explored yet."

## Output format

```
## Carrying over from yesterday
- [ ] Build Stripe Staff tailored resume
- [ ] Practice 2 medium graph problems before Friday's Anthropic onsite

## Stale (>7 days)
- $PERSONAL/applications/airbnb/staff-trust-safety/role.md — analyzed 2026-05-02, no follow-up

## Suggested first move
Stripe resume. You said yesterday it's blocking your apply. ~45 min.
```

## Anti-patterns

- **Don't suggest a list of first moves.** Pick one. The user can decide what's next after that.
- **Don't lecture or motivate.** No "let's have a great day", no "you've got a lot on your plate." Facts and a starting point. Nothing else.
- **Don't override intent.** If the user responds with "actually I want to do coding prep instead," pivot immediately. The briefing is a starting point, not a directive.
- **Don't replicate the full daily summary.** If they want a full recap, they can open the log file. This is a 30-second briefing, not a re-read.
- **Don't show items already completed.** If a carryover item was finished, leave it off.
