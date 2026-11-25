---
name: strat-pre-mortem-analysis
description: Runs a pre-mortem on a product strategy before you commit and returns failure defined at a date, failure stories gathered independently and clustered, each marked hypothetical with its evidence or none, plus early signal, prevention, contingency with trigger, owner by role and residual risk. Use for "run strat-pre-mortem-analysis", "pre-mortem on our product strategy", "it is a year from now and the strategy failed, why?", "how could this fail before we commit?", "premortem template", "what early signals should we watch?", "run a pre-mortem with my team", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Pre-Mortem Analysis

## When To Use
You are about to commit people and a quarter to the strategy. The plan has survived the argument, and the doubts that remain are the ones nobody says in a meeting. This gives them a safe form: assume it failed, then explain how. It answers: which failures should we prevent, which should we watch for, and does any of it change the plan?

## When Not To Use
If the plan's assumptions and reasoning have not been challenged yet, use Red Team Review first. If you need the conditions the strategy depends on, each with a kill criterion and a date, use Strategic Bets; a pre-mortem holds failure stories and responses and does not restate the bets as risks.

## Inputs
- The strategy or leading option in a few lines, and what is about to be committed (people, time, money)
- What success was meant to look like, and the horizon
- The Red Team Review and Scenario Model if they exist, plus any evidence on file (interview themes, usage data, past launches)
If you have none of this, I start from the plan in one paragraph and your own first reason it could fail, and mark the output as a first draft.

## Approach
The project premortem described by Gary Klein in Harvard Business Review, 2007 (https://hbr.org/2007/09/performing-a-project-premortem): the team assumes the project has already failed and writes down plausible reasons why. Here it is aimed at a strategy commitment. The judgment is keeping a vivid story apart from a likely one, and turning each material story into something to watch or do. The failure this prevents: a lively workshop, a wall of notes, and a plan that goes ahead unchanged.

## Workflow
1. Ask at most three questions: what failure means and at which future date, who takes part (roles), and what is already committed and cannot move.
2. Write the frame: "It is [date] and the strategy failed: [what failed means]." Say plainly that this is a thought exercise, not a prediction.
3. Collect reasons independently. Each participant writes theirs before anyone shares. With one user, I ask for your own reasons first, then add candidates marked "added by Claude". Reasons are mechanisms (workload, dependencies, incentives, adoption, outside changes), never a named person or team at fault.
4. Cluster duplicates into failure stories. Mark every story hypothetical, then separate those with evidence on file (quote the source) from speculation. What customers did counts as evidence; how strongly someone feels does not.
5. Likelihood only as a range where evidence supports one, otherwise "unknown". No risk scores and no heat map.
6. For each material cluster: the early signal and where it is read, the prevention, the contingency with the trigger that starts it, the owner by role and the residual risk. Check what the prevention itself costs or breaks.
7. Close on three questions for the owner: do the findings change the plan, call for a pilot first, or need an expert check? Legal or regulatory points: check with a qualified adviser.

## Output Format
```markdown
# Pre-Mortem
**Strategy:** [leading option] | **Commitment:** [people, time, money] | **Participants:** [roles]
**Failure frame:** It is [date] and the strategy failed: [what failed means]. This is a thought exercise.
## Failure stories
| Story (hypothetical) | Mechanism | Evidence on file, or none | Likelihood (range / unknown) | Raised by (team / added by Claude) |
|---|---|---|---|---|
| [what went wrong] | [mechanism] | [source, date / none] | [range / unknown] | [origin] |
## Responses to material stories
| Story | Early signal and where it is read | Prevention | Contingency and its trigger | Owner (role) | Residual risk |
|---|---|---|---|---|---|
| [story] | [sign, source] | [action] | [action, when trigger is met] | [role] | [what remains] |
## What the prevention costs
- [Prevention]: [what it costs or breaks]
## Stories left without a response
- [Story, and why it is accepted or parked]
## Decision
[Strategy owner role] decides by [date before the commitment] whether the plan changes, a pilot runs first or an expert check is needed.
```

## Done When
- Failure and its date were written before any reason was collected
- Every story is marked hypothetical, with its evidence or "none"
- Each material story has a signal, a prevention, a contingency with a trigger and an owner by role
- The owner has answered: change the plan, pilot, or expert check

## Quality Bar
- Reasons are written before they are shared; the first voice in the room does not set the list
- A vivid story is not a likely one, and the table says which is which
- The bets are not copied in as risks
- No claim that the exercise makes the plan more accurate; it surfaces doubts to act on
- Every failure story is marked hypothetical with its evidence or none; the owner decides what changes before committing.

## Next
Run strat-recommendation-memo (Recommendation Memo) to write the call and the ask with these risks and responses in.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
