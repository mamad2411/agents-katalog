---
name: adopt-ai-rollout-decision
description: Prepares an AI rollout decision record with the pilot's evidence and its limits, how the next teams differ from the pilot teams, four options with trade-offs and support costs, prerequisites and pause rules. Use for "run adopt-ai-rollout-decision", "AI rollout decision", "should we roll AI out to everyone", "the pilot went well what next", "scale the AI pilot", "expand the AI pilot to more teams", "go or no go on the AI rollout", "rollout plan after the pilot", part of the Claude Guide for AI Adoption Pack by 90n.
---
# AI Rollout Decision
## When To Use
The pilot went well with volunteers and the sponsor wants everyone on it by next month. The results are real, and they come from people who chose to take part, on work that suited the change. The question this answers: what does the pilot actually support for the next teams, and what does the sponsor need in place before saying yes?

## When Not To Use
Not before a pilot exists: design the test with the AI Pilot Plan. Not when the results have not been read yet: run the AI Adoption Evidence Review first, because this record draws on it and does not redo it. If the sponsor only needs a one-page report, that is the AI Adoption Executive Update.

## Inputs
- The pilot's results on the agreed measures, with who took part and how they were chosen, and the teams proposed next, with what you know about their work, tools, capacity and managers.
- What ongoing support would cost (your own figures), the objections and open questions raised so far, and the sponsor's name and deadline.
If you have none of this, I start from one paragraph on what the pilot showed and who is next, and mark the output as a first draft.

## Approach
The idea is staged scale-up planned from pilot evidence, as set out in the scaling-up guidance of the World Health Organization and ExpandNet: what worked in a pilot was produced by particular people in particular conditions, and expanding means checking which of those conditions travel. The steps below are practitioner convention. The failure this prevents is the familiar one: enthusiasts pilot it on their best work, the result is announced as proof, and the rollout lands on teams with older tools, fuller diaries and managers who heard about it last.

## Workflow
1. Ask at most three questions: which decision does the sponsor lean towards and why, who are the next teams and were they asked or assigned, and what support did the pilot teams get that the next teams would not.
2. Put the pilot in one block: who took part and how they were chosen, how long, uptake, results on the agreed measures, the burden it placed on people, and what stays uncertain. Volunteers are named as volunteers. Then build the transfer table: pilot teams beside next teams on work complexity, tools and access, capacity, manager support, constraints, and volunteer versus assigned. Teams are compared as settings, never rated. Every large difference becomes a line under "must be retested".
3. Lay out four options: expand, expand in stages, revise, stop. For each, the evidence behind it, the trade-offs, the ongoing support costs in your own figures or placeholders, and the delivery it displaces. Stop is written as carefully as expand, or it is not an option.
4. Turn readiness into prerequisites: practical conditions (access in place, managers briefed, rules readable, practice time protected), each with an owner and a date. A condition nobody owns is a hope. Then write the pause rules: the conditions for pausing or reverting, including harm even when use is high, and who calls each. Measure definitions stay the same as in the pilot, so the next stage can be read against it.
5. Record dissent and open questions as they were raised, without softening. The sponsor decides. I draft an announcement only after you tell me the decision.

## Output Format
```markdown
# AI Rollout Decision
**Change:** [role, action, task] · **Sponsor:** [name] · **Decision due:** [date] · Draft status: [first draft / decided on date]
## The pilot, and its limits
Who took part and how chosen: [teams, volunteers or assigned], over [period]. Uptake at team level: [qualifying uses over eligible opportunities, source]. Results on the agreed measures: [measure, result, source, date]. Burden: [time, support]. What the pilot cannot show: [limits].
## Transfer table
| Dimension | Pilot teams | Next teams | Must be retested |
|---|---|---|---|
| Work complexity, tools and access | [description] | [description] | [yes, what / no] |
| Capacity, manager support and constraints | [description] | [description] | [yes, what / no] |
| Volunteer or assigned | [volunteer] | [assigned or invited] | [yes, what / no] |

## Options
| Option | Evidence for | Trade-offs | Ongoing support cost | What it displaces |
|---|---|---|---|---|
| Expand | [evidence] | [trade-off] | [your figure or placeholder] | [delivery] |
| Expand in stages | [evidence] | [trade-off] | [your figure or placeholder] | [delivery] |
| Revise | [evidence] | [trade-off] | [your figure or placeholder] | [delivery] |
| Stop | [evidence] | [trade-off] | [your figure or placeholder] | [delivery] |

## Prerequisites and pause rules
| Kind | Condition | Owner, or who calls it | By when, or what it triggers |
|---|---|---|---|
| Prerequisite | [access in place / managers briefed / rules readable / practice time protected] | [name] | [date, met or not yet] |
| Pause rule | [condition the sponsor set, including harm when use is high] | [name] | [pause or revert, and how] |

## Dissent and open questions
[Each objection and open question as raised, with who will answer it and when.]
## Decision
[Sponsor name] decides by [date]: expand, expand in stages, revise or stop. Next review on [date], against the same measure definitions as the pilot.
```

## Done When
- The pilot block says how people were chosen and what the pilot cannot show.
- Every difference in the transfer table has a retest line or a reason it needs none, and all four options carry trade-offs and a support cost.
- Each prerequisite and each pause rule has a named owner, and dissent appears in the words it was raised in.

## Quality Bar
- I do not make the decision and I promise nothing on the sponsor's behalf. No cost, saving or uptake figure appears that you did not supply; missing figures stay in brackets.
- Results stay at team level, with no list of who used it in the pilot and no rating of the next teams. "It worked" is always followed by "for whom, on what work, with what support".
- Where the rollout changes roles, working time or how staff are consulted: check with a qualified adviser.
- A pilot with volunteers is not proof for everyone; the sponsor decides, stopping stays an option, and dissent is on the record.

## Next
Run adopt-ai-habit-review (AI Habit Review) to check each quarter whether what was rolled out is still in use and still worth it.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).