---
name: adopt-ai-use-case-map
description: Builds an AI use case map, role by role, showing the recurring tasks, where AI helps and where it does not, what is off limits, who checks the output, and the first three use cases to try. Use for "run adopt-ai-use-case-map", "AI use case map", "where does AI help in this role", "I do not see what I would use it for", "AI use cases by role", "map tasks for AI", "first AI use cases to try", "what can my team use AI for", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Use Case Map

## When To Use
People say "I do not see what I would use it for", and the examples in the training are from someone else's job. You need a map that starts from what a role really does in a week, step by step, and shows where AI helps, where it does not, and what must stay out. It answers the question: which three uses are worth trying first here, and why those.

## When Not To Use
Not for committing a role to one change with a sponsor behind it: that is AI Adoption Brief. Not for the team's own commitment about what is fine: the map is your draft, and Team AI Agreement is where the team decides. For what the rules allow in detail, use AI Rules Explainer.

## Inputs
- For each role, a real week in the words of someone who does the job: the tasks that came back, not the job description.
- For two or three of those tasks, the steps and the material they use (sanitised).
- Your organisation's AI rules (or a note that there are none yet), and any use someone in the role has already tried.
If you have none of this, I start from one role and its recurring tasks as you describe them, and mark the output as a first draft.

## Approach
This is plain task-level mapping, built on the first judgement a person makes when working with AI: what to hand over, what stays with the person, and what must never go in. The unit is the step, not the job, because "write the monthly report" hides a step where AI drafts well and a step where a person must decide what the figures mean. The failure this prevents is the list of generic use cases copied from a slide, where the support agent is told AI can "write marketing copy" and concludes, reasonably, that it is not for them.

## Workflow
1. Ask up to three questions: which roles and what did a real week look like for each, what do your rules say about what can go into the AI tool, and which uses has anyone here already tried.
2. List each role's recurring tasks in the words people use, then split each task into steps. Keep the steps that involve a person deciding or talking to someone: they belong on the map as much as the ones AI can help with.
3. Fill four columns for each step. AI helps with: draft, summarise, compare, restructure, check or brainstorm, named precisely. AI does not do: judgement calls, contact with people, facts it cannot source. Off limits: starts from the organisation's rules, and where the rules are silent or unknown the entry is "ask first". Who checks the output: a role, never "nobody".
4. Mark every "AI helps" entry as tried by someone here, or untested. An untested entry is my suggestion and reads as one; it does not become a recommendation until a person in the role has tried it.
5. Pick the first three use cases by three plain criteria that you weigh: happens often, low harm if wrong, easy to check. I lay out how each candidate sits on the three in words. There is no numeric score, and you make the pick.
6. Record the reason for each pick, and one task where AI should not be used, with the reason. A map with no "not here" is not believed.
7. Mark what people in the role must confirm before the map is shared, and who will ask them.

## Output Format
```markdown
# AI Use Case Map
Status: [first draft / confirmed by people in the role on [date]] · Rules used: [document and date, or "none yet, all entries ask first"]
## Role: [role]
| Recurring task | Step | AI helps with | Tried here or untested | AI does not do | Off limits | Who checks the output |
|---|---|---|---|---|---|---|
| [task in the role's words] | [step] | [draft / summarise / compare / restructure / check / brainstorm: what exactly] | [tried / untested] | [judgement, contact with people, unsourced facts] | [rule, or "ask first"] | [role] |

(Repeat the table for each role.)
## First three use cases to try
| Use case | Role | Happens often | Low harm if wrong | Easy to check | Reason for the pick |
|---|---|---|---|---|---|
| [use case] | [role] | [in words] | [in words] | [in words] | [reason] |

## Where AI should not be used
- [Task or step], because [reason].
## To confirm with people in the role
- [Entry or assumption], asked by [name] by [date].
## Decision
[Name of the enablement lead] decides by [date] which three use cases are offered first, after people in each role have confirmed the map; each person in the role decides what they try.
```

## Done When
- Every step has all four columns filled, with "ask first" wherever the rules are silent.
- Every "AI helps" entry is marked tried or untested.
- Three use cases are picked, each with a reason against the three criteria in words.
- At least one task is named where AI should not be used, with the reason.

## Quality Bar
- Tasks are in the words of people who do them; anything taken from a job description is marked as such.
- Tasks and roles only: no named person, and no column for who is good at it.
- No number anywhere: no time estimate, no score, no claim about what a use will save.
- The map points to the rules and never writes one. Data protection and confidentiality questions: check with a qualified adviser.
- Each map covers what one role can read on a page; a second role gets its own table.
- The map shows where AI helps a task; people in the role confirm it and decide what they try.

## Next
Run adopt-barrier-diagnosis (AI Adoption Barrier Diagnosis) to find out why a mapped use still does not happen.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
