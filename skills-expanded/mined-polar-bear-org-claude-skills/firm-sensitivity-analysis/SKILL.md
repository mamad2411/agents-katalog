---
name: firm-sensitivity-analysis
description: Tests how firmly your recommendation stands, with the assumptions carrying it, each varied across a range you can defend, the point where another option becomes the better one, facts kept apart from priorities, the evidence worth getting before the deadline and its cost, a bounded pilot where one fits, and the recommendation classed as stable, conditional or unresolved. Use for "run firm-sensitivity-analysis", "what would change my mind", "sensitivity analysis on my recommendation", "which assumption matters most", "when would the other option win", "is more research worth it before I recommend", "should we pilot first", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Sensitivity Analysis

## When To Use
A sharp client will ask it sooner or later: "what would have to be true for you to recommend the other one?" If you cannot answer, the recommendation sounds like a preference. Run this after the pre-mortem, to find the two or three assumptions the advice hangs on and how far each can move before the advice changes.

## When Not To Use
To check a single forecast against finished cases, use Outside View Check. If the disagreement is about what matters and not about facts, more analysis will not settle it; take the value judgments from the Trade-Off Table back to the client.

## Inputs
- The options, the trade-off table and your current recommendation
- The estimates behind it, with their sources
- The client's deadline and what further evidence would cost in time and money
If you have none of this, I start from the recommendation and your two strongest reasons, and mark the result as a first draft.

## Approach
Sensitivity analysis and the value of further information are conventions of decision analysis, described generically: change one assumption at a time across a defensible range and watch whether the preferred option changes. Evidence is worth collecting only if a plausible result would alter the choice before the deadline. The failure it prevents runs both ways: recommending on an assumption that a single phone call would overturn, or commissioning a month of research that could not change anything.

## Workflow
1. Ask, in one go: what makes the recommended option better than the runner-up today? Which estimates is that built on? When does the client have to decide?
2. List the assumptions carrying the recommendation and tag each as a fact that could be checked or a priority that someone holds. More data cannot settle a difference in priorities; those go back to the client as a judgment.
3. Vary one factual assumption at a time across a range you can defend, holding the others visible, and find the switching point: the value at which the runner-up becomes the better option. Say whether that value is inside the plausible range.
4. Where two assumptions move together, test them as a pair. Do not stack unrelated worst cases and present the result as likely.
5. For each assumption with a reachable switching point, name the evidence that would pin it down, what it costs in time and money, and whether it can arrive before the deadline. Where it fits, outline a bounded pilot: cost ceiling, measure, stop condition, owner, and what it cannot tell you about full scale.
6. Class the recommendation: stable (holds across every range tested), conditional (holds if a named condition is met) or unresolved. Show the boundary in a sentence the client can repeat.

## Output Format
```markdown
# What Would Change the Recommendation
Recommendation tested: [option] over [runner-up] · Client decides by: [date]
## Assumptions carrying it
| Assumption | Fact or priority | Current value (source) | Defensible range | Switching point | Inside the range? |
|---|---|---|---|---|---|
| [assumption] | [fact / priority] | [value, source] | [low to high] | [value at which runner-up wins] | [yes / no] |
## Evidence worth getting
| Assumption | Evidence | Cost and time | Before the deadline? | Could it change the choice? |
|---|---|---|---|---|
| [assumption] | [what to obtain, from whom] | [your estimate] | [yes / no] | [yes / no] |
## Pilot, if one fits
[Scope · cost ceiling · measure · stop condition · owner (role) · what it will not show]
## Verdict
[Stable / conditional on [condition] / unresolved] · In one sentence: "[what would change the recommendation]"
## Decision
[You] decide by [date] whether to recommend now, recommend with the condition stated, or obtain [evidence] first; [client decider role] settles the priorities marked above.
```

## Done When
- Each assumption is tagged fact or priority
- Each factual assumption has a range, a switching point and a note on whether it is reachable
- Evidence is listed only where it could change the choice in time
- The verdict is one of three words, with the boundary in one sentence

## Quality Bar
- Ranges are ones you can defend, with their basis; none is supplied by me
- No expected value is fabricated for further research
- Linked assumptions are tested together; unrelated worst cases are never multiplied
- A pilot states what it cannot show at scale
- Every value and range is yours or the client's; I invent none, and whether to recommend now or learn more is your decision.

## Next
Run firm-recommendation-memo (Recommendation Memo) to put your position on one page with what would change it.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
