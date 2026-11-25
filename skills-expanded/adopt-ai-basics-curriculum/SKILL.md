---
name: adopt-ai-basics-curriculum
description: Builds a short AI basics path by role around four judgements, with a practice on real work in each unit, a list of what is left out and why, and a refresh date with an owner. Use for "run adopt-ai-basics-curriculum", "AI basics curriculum", "AI training curriculum for our teams", "what should AI training cover", "AI learning path by role", "AI literacy programme outline", "replace the tool tour", "AI training that does not go out of date", part of the Claude Guide for AI Adoption Pack by 90n.
---
# AI Basics Curriculum
## When To Use
The AI training on offer is a tool tour and a list of prompts that will be out of date next month. You have been asked for "the basics" for several roles and you want a path that still holds after the tool changes. It answers: what should a person in this role be able to do on their own task, and which few units get them there?

## When Not To Use
If you need the minute-by-minute plan for one session, use Hands-On AI Session Plan: this skill gives the path across units and no timings inside them. If nobody has listed the tasks each role really does, run AI Use Case Map first, or the units will be tied to someone else's job.

## Inputs
- The roles in scope and their recurring tasks, ideally the use case map with its first three use cases per role.
- Your organisation's AI rules, including the never-put-in list, and who answers questions about them.
- The learning time that really exists per role, and any existing AI training material to sort into keep, move or drop.
If you have none of this, I start from one role and three of its real tasks and mark the output as a first draft.

## Approach
The path rests on four judgements a person makes when working with AI: what to hand over, how to ask, how to check, and what you stay responsible for. It is laid out by backward design, as described in the Vanderbilt University Center for Teaching guide: results first, evidence second, learning activities third. Judgement survives a tool update and a button tour does not. The failure this prevents: a launch webinar that walks through every feature and hands out forty prompts, after which people can name the menus and still do not know whether to trust the summary in front of them.

## Workflow
1. Ask at most three questions: which roles and which real tasks are in scope, how much learning time each role really has, and who will own the path and its refresh.
2. Write the results first. For each role, one line per judgement saying what the person can do on a named real task after the path. Write doing, never knowing: "decides which parts of [task] go to AI and which stay with them", not "understands AI limits".
3. Write the evidence second: for each role, a piece of real work checked against criteria the team already uses and discussed with the person. If the only evidence you can name is a quiz, the result is written for knowing; go back to step 2.
4. Only then build the units. At least one unit per judgement, each tied to a task from the use case map, each with a practice the person does on their own work. Put "what to hand over" first, because the never-put-in rule has to arrive before anyone pastes anything. The path differs by role only where the tasks differ.
5. Write the "left out, and why" list. Tool tours, feature lists and prompt collections date fast: send them to the shared library or a job aid and say so, so nobody reads the gap as an oversight.
6. Set unit lengths and pre-work as placeholders you fill from the time that exists, then the refresh date, the trigger for an early refresh (the tool changed, the rules changed) and the owner. Where AI literacy duties exist in law, for example the EU AI Act, Article 4, name it once as context: what it requires of your organisation is a point to check with a qualified adviser.
7. Read each unit against one test, "would this still be true after the tool's next update?", and move anything that fails to the left-out list.

## Output Format
```markdown
# AI Basics Curriculum
Roles: [roles] | Path owner: [role] | Learning time that exists: [per role, your figure] | Status: [first draft or reviewed]
## What people can do after the path
| Role | Real task | What to hand over | How to ask | How to check | What you stay responsible for |
|---|---|---|---|---|---|
| [role] | [task from the use case map] | [can do] | [can do] | [can do] | [can do] |

## What would show it
| Role | Piece of real work | Criteria the team already uses | Who discusses it with the person |
|---|---|---|---|

## Units
| Unit | Judgement | Tied to task | Practice on own work | Length | Pre-work | Roles |
|---|---|---|---|---|---|---|
| [n] | [one of the four] | [task] | [what the person does] | [you set] | [you set] | [all or named roles] |

## Left out, and why
| Left out | Why | Where it lives instead |
|---|---|---|
| [tool tour, feature list, prompt collection] | [dates fast, not tied to a task] | [shared library, job aid] |

## Refresh
Refresh date: [date] | Early trigger: [the tool changed, the rules changed] | Owner: [role]
## Decision
[Path owner] approves the units and the left-out list by [date]. [Sponsor] confirms the learning time per role by [date]. People in each role confirm the tasks are theirs before the first unit runs.
```

## Done When
- Every role has one result line per judgement, written as something a person does on a named task.
- Every unit is tied to a task from the use case map and has a practice on the person's own work.
- The left-out list says where each item lives instead, and a refresh date, an early trigger and an owner are filled in.

## Quality Bar
- Results before units: a unit that serves no result line is cut.
- Evidence of learning is a piece of real work discussed with the person. No test with a pass mark, no certificate ladder, no skill rating.
- No unit depends on a screen layout or a feature name; lengths and pre-work are placeholders you set, and session timings belong to each session's own plan.
- The path teaches judgement on real tasks; completion is never reported per person as adoption.

## Next
Run adopt-hands-on-session-plan (Hands-On AI Session Plan) to plan the first unit as a session where people touch the tool.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
