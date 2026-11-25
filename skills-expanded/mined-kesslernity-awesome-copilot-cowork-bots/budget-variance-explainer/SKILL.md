---
name: budget-variance-explainer
description: Drafts the narrative behind a budget variance from the context the user supplies and the discussion in mail and meetings, never producing or changing the figure itself. Use when the user asks to explain a variance, draft the commentary for a budget review, write the story behind the numbers, or prepare variance notes before a finance meeting.
---

# Budget Variance Explainer

Writes the story behind a number somebody else owns.

🔴 **This skill never produces a figure.** The user supplies the variance. The skill explains it.
If asked to calculate, recalculate, forecast or correct a number, decline and say the finance
system is the source of truth.

## Inputs
- The variance, supplied by the user: line, period, budget, actual, difference
- Mail, meetings and files for the period, through **Email**, **Meetings** and **Enterprise Search**
- `references/config.md` for the cost-centre vocabulary and the house commentary structure

## Procedure
1. **Restate the variance exactly as given.** If a figure is missing, ask for it. Never derive one.
2. **Search the period** for discussion touching the line: approvals, delays, hiring, scope
   changes, supplier issues, one-off events.
3. **Assemble candidate causes**, each with the evidence link that supports it.
4. **Rank** by how directly the evidence speaks to the line. An approval email naming the cost
   centre outranks a general remark in a meeting.
5. **Write the commentary** in the house structure from config. For each cause: what happened,
   when, the evidence link, and whether it is expected to recur.
6. **State plainly what is unexplained.** If the evidenced causes do not account for the variance,
   say so and quantify the gap in the user's own figures.

## Output
Commentary in the house structure, then:

| Cause | When | Evidence | Recurring? | Accounts for |

Closing line: evidenced causes, and the unexplained remainder stated in the user's figures.

## Definition of done
Every cause carries an evidence link, the unexplained remainder is stated rather than smoothed
over, and no figure originated here.

**"Largely unexplained" is an honest and useful answer.** A variance commentary that explains
100% of everything is usually fiction, and finance reviewers know it.

## When there is no data
- No discussion found for the line: say the period carries no evidenced cause, and stop. Do not
  reach for a plausible-sounding reason.
- Evidence contradicts itself: present both and say they conflict.

## Boundaries
- **Never calculate, recalculate or forecast.** Not even arithmetic on supplied figures.
- Never state a cause as certain when the evidence is circumstantial. Label it.
- Never write commentary that attributes a variance to a named individual.
- Draft only. The commentary goes to the user, not into a reporting pack.

## Self-check
- Did any number originate in this output rather than from the user? If so, remove it.
- Does every cause have a link?
- Is the unexplained remainder stated plainly?
