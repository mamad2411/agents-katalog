---
name: standup-summary
version: 1.0.0
description: Turn raw notes about recent work into a crisp done / doing / blocked standup - concrete, honest about what actually shipped, with blockers stated so someone can help.
triggers:
  - standup
  - standup update
  - what did I do yesterday
  - daily update
  - write my standup
capabilities: []
inputs:
  - name: notes
    required: true
    description: Raw notes, commit messages, or a brain-dump of recent work.
  - name: audience
    required: false
    description: Who reads it (team channel, manager 1:1, client) to calibrate detail.
---

# Standup Summary

## When to use
Use this when you have a brain-dump, a list of commits, or rough notes about recent work and need the update a good teammate gives: short, concrete, honest about status, with blockers stated plainly enough that someone can actually unblock you.

**Not for:** performance self-reviews or promo packets (those need scope and impact over time, not yesterday's tasks); detailed status reports for stakeholders who need narrative and risk; or padding a slow day into false productivity. If nothing happened, say so briefly - inventing activity is worse than a short update.

## Method
1. **Sort every note into done / doing / blocked.** *Decision point:* when unsure whether something is finished, downgrade it to Doing - "done" is a promise, not a hope.
2. **Apply the done test:** merged, shipped, sent, or verified. "Almost", "just needs", "nearly" all mean Doing.
3. **Make each item concrete.** "Fixed the login timeout (PR #214, merged)" beats "worked on auth". Keep ticket and PR numbers.
4. **State blockers as what / who / since when.** *Decision point:* a blocker with no owner is a complaint - name who can clear it and when you asked. If nothing is blocked, omit the section entirely; no "no blockers" ceremony.
5. **Cap each section at three lines.** If there are more, keep the three that matter and roll the rest into one "plus small stuff: ..." line.
6. **Order by what the audience cares about,** and cut filler ("continued to make progress on", "various tasks").

## Example
**Input (raw):** merged the retry fix finally, started poking at the flaky e2e suite its something with timeouts, waiting on Dana for the API key to test payments, also reviewed two PRs

**Output:**
**Done:** Merged the retry fix; reviewed 2 PRs.
**Doing:** Investigating flaky e2e suite - looks timeout-related, narrowing it down.
**Blocked:** Payments testing needs the API key from Dana (asked yesterday).

## Pitfalls
- **Done inflation.** Filing in-progress work under Done because it is "basically finished" - then it slips and trust erodes.
- **Vague items.** "Worked on the backend" tells the team nothing and invites a follow-up question standup exists to avoid.
- **Orphan blockers.** "Blocked on stuff" with no owner or ask - nobody knows how to help.
- **Filler and over-length.** Ten low-value lines bury the two that matter; trim ruthlessly.

## Output format
```
**Done:** <finished, concrete, with PR/ticket ids>
**Doing:** <in progress, one line each, max 3>
**Blocked:** <what - who can clear it - since when>   (omit if nothing is blocked)
```
