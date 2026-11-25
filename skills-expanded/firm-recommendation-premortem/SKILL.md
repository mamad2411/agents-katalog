---
name: firm-recommendation-premortem
description: Runs a pre-mortem on the option you are about to recommend, with failure defined at a date, the plausible ways it fails each marked hypothetical, the early signal for each, prevention, a contingency with its trigger, an owner by role, what stays exposed, and a success case listing what must go right. Use for "run firm-recommendation-premortem", "pre-mortem on my recommendation", "how could this recommendation fail", "stress test before I commit", "what am I not seeing", "risks of the option I favour", "play devil's advocate on my advice", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Recommendation Pre-Mortem

## When To Use
You have settled on the option and it feels right. That is the moment a colleague would ask, "and how does this go wrong?" Working alone, there is no colleague. Run this after the comparison and before the memo, to imagine the recommendation has failed and work out the most believable reasons why.

## When Not To Use
If you are still testing your reading of the problem, use Hypothesis Test Plan. To see which numerical assumption would switch the choice, run Sensitivity Analysis next; this one is about how the chosen route fails in practice.

## Inputs
- The option you favour and the outcome it is meant to produce
- The time horizon and the client's working constraints
- Risks already raised by the client or by you
If you have none of this, I start from the option in one paragraph and mark every failure route as a first-draft hypothesis.

## Approach
The pre-mortem was described by Gary Klein in "Performing a Project Premortem" (Harvard Business Review, September 2007): assume the plan has already failed, then explain why. Writing as if failure has happened makes doubts easier to voice than a polite risk review does. Every route here is a hypothetical, and a vivid story is not a probability. The failure it prevents is the recommendation whose first serious objection arrives in the client's boardroom.

## Workflow
1. Ask, in one go: which option, and what is it meant to achieve by when? What would you and the client both call failure? Which way of failing worries you most?
2. Define failure in one line with a date: on [date], [outcome] has not happened, or [harm] has. Without a definition, the exercise drifts into general worry.
3. Write your own failure route first, then let me add others across six sources: workload on the client's people, dependencies on other projects, incentives that pull the other way, adoption by those who must change, changes outside the client, and your own delivery. Each is labelled hypothetical.
4. Mark each route as resting on evidence you hold or on speculation, then merge duplicates. No likelihood numbers unless you supply the basis; otherwise it reads "uncertain".
5. For each route that matters, write the early signal someone could observe, the prevention, the contingency with the trigger that starts it, an owner by role, and what stays exposed even then. Check what each prevention itself costs or risks.
6. Write the success case: the three or four things that must go right, since a missing condition is as dangerous as a threat. Then ask whether any of this changes the option, calls for a pilot, or needs a specialist's view.

## Output Format
```markdown
# Pre-Mortem on the Recommendation
Option tested: [name] · Meant to achieve: [outcome] by [date]
Failure means: on [date], [what has not happened or what harm has]
## Ways it fails (all hypothetical)
| # | Route to failure | Source (workload / dependency / incentive / adoption / outside / delivery) | Evidence or speculation | Early signal |
|---|---|---|---|---|
| 1 | [mechanism] | [source] | [evidence held / speculation] | [what someone would see] |
## Responses
| # | Prevention | Contingency and its trigger | Owner (role) | Still exposed |
|---|---|---|---|---|
| 1 | [action] | [action, started when trigger] | [role] | [what remains] |
## What must go right
- [Condition] · currently [in place / not in place / unknown]
## Decision
[You] decide by [date] whether the recommendation stands, changes or becomes a pilot; [client decider role] accepts or declines each exposure that remains.
```

## Done When
- Failure is defined with a date
- Every route is labelled hypothetical and marked evidence or speculation
- Each route that matters has a signal, a prevention, a triggered contingency and an owner by role
- The success case lists what must go right

## Quality Bar
- No risk score and no invented likelihood
- Routes describe mechanisms, never the failings of a named person
- A prevention's own cost and risk are stated
- The output is a tested recommendation, not a forecast that failure will happen
- Every route is a hypothesis, and I state none of them as a finding; whether the recommendation stands is your call, and accepting the exposure is the client's.

## Next
Run firm-sensitivity-analysis (Sensitivity Analysis) to find the assumptions that would switch the recommendation.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
