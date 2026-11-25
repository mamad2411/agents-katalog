---
name: decision-audit-trail
description: Use this skill after a real organizational decision has been made (vendor selected, architecture chosen, hire approved, strategy committed, project killed) to capture the reasoning while it is still fresh. Triggers on phrases like "audit decision", "document why we decided", "decision memo for [X]", or when the user references a recently made choice. Produces a one-page "Why we decided X" memo for future you, new hires, or board context.
---

# Decision Audit Trail

## When to use this skill

A non-trivial decision has just been made. In six months, someone will ask why. The person who made the call will be vague. The notes are scattered across Slack, Notion, email threads, and meeting recordings. This skill captures the reasoning at decision time, not six months later when it has decayed.

## Input the user provides

- The decision (one sentence, ideally with the specific choice made)
- The time window in which the decision was discussed (last week, last 30 days, last quarter)
- Optionally: pointers to relevant threads, docs, meeting notes

If the user just says "audit our vendor decision," ask one clarifying question about which vendor and the rough time window, then proceed.

## What this skill does

1. Walks back through the available material from the named time window
2. Pulls the relevant inputs:
   - Alternatives that were seriously considered (not the 30 long-listed options, the 2-4 that were real finalists)
   - The criteria used to evaluate them
   - Who pushed in which direction and why
   - What changed during the discussion (when did opinions shift, what data caused the shift)
   - The deciding factor (the thing that ultimately tipped the call)
3. Produces a one-page decision memo in the structure below.

## Output structure

```
# Decision: [Specific decision made]
*Decided by: [decision-maker]. Date: [decision date]. Time window reviewed: [start-end]*

## What we decided
One paragraph stating the decision in plain language and what it means operationally.

## Alternatives we seriously considered
- [Alternative 1]: brief description, why it was on the table, why we did not choose it
- [Alternative 2]: same
- [Alternative 3, if applicable]: same

## Criteria we used
- Criterion 1 (with rough weight)
- Criterion 2
- Criterion 3
Note which were stated upfront vs. which emerged during the discussion.

## What the discussion looked like
2-3 sentences on who pushed which way, what tensions surfaced, what shifted minds.

## The deciding factor
One paragraph naming the specific thing that tipped the decision. Be honest. If the deciding factor was a relationship, a deadline, or a gut call, name it as such rather than dressing it up as a criteria-driven choice.

## Risks we accepted
- Risk 1 and the mitigation (or acknowledged unmitigated risk)
- Risk 2

## What would change our mind
2-3 conditions under which this decision would be revisited.
```

## Calibration notes

- The deciding factor section is the most important. Most decision memos make the decision sound more rational than it was. Resist that. Future readers benefit from an honest account.
- One page is the cap. A two-page memo will not be read in six months.
- Distinguish between "the criteria we used" (true) and "the criteria we said we used" (the rationalized story). Where there is a gap, note it.
- For confidential or sensitive personnel decisions, flag clearly and recommend storing the memo in restricted access.

## When NOT to use this skill

- Trivial decisions (which restaurant for lunch)
- Decisions still under active debate (use a decision framing doc instead)
- Decisions where the reasoning is already well-documented elsewhere

The skill earns its place when the decision is real, made, and the trail is currently scattered.
