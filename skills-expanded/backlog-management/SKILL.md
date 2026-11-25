---
name: backlog-management
description: "Keep the backlog useful instead of letting it become a graveyard of ideas nobody will build. Covers backlog hygiene, grooming practices, and knowing when to kill items. Use when the backlog has hundreds of stale items, sprint planning takes forever, or the team doesn't trust the backlog."
---

# Backlog Management

Keep the backlog sharp, honest, and useful — not a guilt-inducing pile of good intentions.

## How to use

- `/backlog-management` Apply backlog management constraints to this conversation.
- `/backlog-management <context>` Improve backlog practices for the described situation.

## Constraints

### Backlog Hygiene
- MUST review and prune the backlog at least monthly. Stale items erode trust.
- Any item untouched for 90 days SHOULD be either re-prioritized or killed
- MUST limit backlog size. If it takes more than 15 minutes to scan, it's too long.
- SHOULD separate the "ready to build" backlog from the "idea parking lot"
- NEVER treat the backlog as a promise. It's a prioritized list of options.

### Item Quality
- Every backlog item MUST have: clear problem statement, acceptance criteria, and rough effort estimate
- SHOULD tag items by: theme, user segment, business impact, and status
- MUST ensure top 10 items are detailed enough to start working on immediately
- Items below top 20 SHOULD be epics or themes, not detailed tickets
- NEVER let vague items ("improve the dashboard") stay in the backlog. Sharpen or kill.

### Grooming Practices
- MUST run regular grooming sessions to refine upcoming items
- SHOULD involve engineering in grooming — they catch feasibility issues early
- MUST split items that are too large to fit in a sprint
- SHOULD estimate effort collaboratively, not have PM assign estimates unilaterally
- NEVER let grooming become a multi-hour ceremony. Timebox to 30-60 minutes.

### Saying No
- MUST close items that won't get built in the foreseeable future
- SHOULD have a clear process for declining requests: acknowledge, explain, document
- MUST distinguish between "not now" and "never" — communicate which one clearly
- NEVER accumulate items out of guilt or fear of saying no
- SHOULD track patterns in rejected items — if the same request keeps coming back, investigate

### Anti-Patterns
- The Infinite Backlog: 500+ items that nobody has read in months
- The Guilt Backlog: keeping items because someone important asked for them years ago
- The Ungroomed Sprint: pulling items into a sprint that haven't been refined or estimated
- The Living Jira Cemetery: items marked "in progress" that nobody is actually working on
- The Wishlist: a backlog full of ideas with no prioritization, estimation, or acceptance criteria
