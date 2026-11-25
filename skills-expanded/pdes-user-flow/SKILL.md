---
name: pdes-user-flow
description: Write one task as a user flow with entry points, numbered steps paired with system responses, lettered decision branches, error and recovery paths, exits and the assumption behind every branch, ready to draw as a wireflow. Use for "run pdes-user-flow", "user flow", "map the flow for this feature", "wireflow", "task flow", "what are the unhappy paths", "we only have the happy path", "flow diagram for this task", part of the Claude for Product Designers Pack by 90n.
---

# User Flow

## When To Use
You have a brief and a blank canvas, and the happy path is the only path anyone has described. The ticket says "user invites a teammate" and stops there. This skill answers the question the brief skipped: what are all the ways through this task, including the ones where something goes wrong or the person changes their mind?

## When Not To Use
Not when the task runs across channels or over weeks, with waiting, emails and other people in between. That is a journey, and the User Journey Map fits it. Not for what a single screen shows while loading, empty or failing either: UI States and Edge Cases covers that once the flow is settled.

## Inputs
- The brief or ticket for the task, as written, and every entry point you know
- Business and technical rules that create branches (permissions, limits, validation)
- Any evidence of what people do today (session notes, support themes, analytics), and the product context file if you have one
If you have none of this, I start from a one-line description of the task and mark the output as a first draft with every branch shown as an assumption.

## Approach
The method is the user flow as Nielsen Norman Group defines it (User Journeys vs. User Flows, 2023): one task, in one product, short in time, drawn as a wireflow or a task diagram. A flow records what people do and how the system answers, and leaves thoughts and feelings to the journey. The judgement lies in the branches. A flow with no back, no failure and no "left and came back tomorrow" is a storyboard of the demo, and engineering will meet the rest in the build with no design to follow.

## Workflow
1. I ask up to three questions: the single task and where it ends, every place it can start from, and which rules or permissions change the path.
2. Scope check against the definition. If the task spans channels or weeks, I say it is a journey and stop, instead of forcing it into a flow.
3. The main path as numbered steps. Each step is a pair: what the user does, how the system responds. A step with no response is not finished.
4. Decision points get lettered branches (3a, 3b). Every branch states the assumption behind it and whether anyone has seen a user take it.
5. Three questions at every step: what if it fails, what if the user goes back, what if they leave and return later. Each gets a branch, or "not needed" with the reason.
6. Exits and ways back: where the task ends well, where it is abandoned, and how a person who left finds it again.
7. I lay it out as a table that maps one to one onto a diagram (node, action, response, next node) and list the open questions with who can answer each.

## Output Format
```markdown
# User Flow
Task: [one task] · Product: [product] · User group: [group] · Ends when: [end condition]
## Entry points
- [E1] · From: [screen or link] · The user already has: [state or data]
## Steps
| Node | User does | System responds | Next node | Assumption behind it |
|---|---|---|---|---|
| [1] | [action] | [response] | [2] | [assumption, or seen in source] |
| [3a] | [choice at a decision point] | [response] | [4] | [assumption] |
| [3b] | [other choice] | [response] | [node] | [assumption] |
## Error and recovery branches
| At node | What if | Branch, or "not needed" with the reason | Seen in evidence |
|---|---|---|---|
| [node] | [fails, goes back, leaves and returns] | [branch] | [source, or assumed] |
## Exits and the way back
- [Node] · Kind: [done, abandoned, blocked] · How the user returns: [route]
## Open questions
- [Question] · Who can answer: [role]
## Decision
[The product manager] confirms the task boundary and the rule-driven branches by [date]. [The engineering lead] says which branches are not possible as drawn by [date].
```

## Done When
- Every step has both halves (the action and the system response) and was asked the three questions, each with a branch or a reason
- Every branch states its assumption and whether it was seen in evidence
- The table can be drawn as a diagram with no extra decisions

## Quality Bar
- One task only. A second task found on the way gets its own flow. No screens are designed here: the flow says what happens, and you decide how it looks.
- System responses are concrete ("shows the invite as pending"), never "handles it". A rule I cannot trace becomes an open question.
- Works in a plain chat. Optionally, the Figma connector can create a FigJam diagram from the table, and Claude Design can draw the flow on a canvas.
- A flow on paper is a hypothesis; branches nobody has seen a user take are marked as assumptions.

## Next
Run pdes-ux-writing (UX Writing Copy Deck) to write the words on each step.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
