---
name: ldg-build-the-job-aid
description: Builds one job aid for one task as a checklist, a decision table or a one-page flow chosen by the shape of the task, with where it lives in the workflow, a walk-through test, the owner, the review date and the trigger for an early update. Use for "run ldg-build-the-job-aid", "job aid", "job aid template", "quick reference guide", "checklist for this task", "cheat sheet", "performance support", "a checklist instead of a course", "people need the answer mid-task", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Build the Job Aid

## When To Use
People need the answer mid-task, not a 30-minute module. The step comes up twice a year, the rule changed last month, or there are more details than anyone can carry in their head. Use this to build the one thing a person looks at while doing the work. It answers: what goes on the page, in which format, and where does it sit so a hand can reach it?

## When Not To Use
If you are still deciding which content should be learned and which should be looked up, run Map the Actions or Break Down the Task first; this skill builds one aid for one task. If the task turns on judgement under pressure that no table can hold, practise it with Write the Scenarios.

## Inputs
- The task: its steps, choices and exceptions (the procedure, your expert notes, or the look-up items from an action map or a task breakdown)
- Where the task happens: the system, screen, desk, counter or vehicle, and what people already have open or in hand
- Who owns the process, who the expert is, and how often the content changes
If you have none of this, I start from the task described in a few lines and mark the output as a first draft.

## Approach
Performance support at the moment of need: help that sits inside the work and is used while doing it. Action mapping (its originator's public page) asks, before any course, whether a job aid alone would do. The judgement is in two places, the format and the placement, and both come from watching where the task happens. The failure this prevents: an aid written like a small course, three paragraphs of why before the first step, filed four clicks away, while the person with a customer waiting asks a neighbour instead.

## Workflow
1. Ask up to three questions: what the person is doing at the moment they need this, where they are and what they can see, and how often the content changes.
2. Confirm why a job aid fits. It fits when the task is done rarely, changes often, carries many details, or is costly to get wrong. You confirm which applies. If none does, I say so and stop: a task done many times a day lives in memory and needs practice.
3. Choose the format by the shape of the task: a checklist for fixed steps in order, a decision table for if-then choices, a one-page flow for branching paths. A task with two shapes gets the format of its hardest part.
4. Draft only what is needed during the task. Action verb first, one step per line, the common mistake beside the step where it happens. Reasons, history and policy text go elsewhere, with a pointer.
5. Set the placement: the exact point in the workflow and the channel (inside the system, pinned in the tool, printed at the station), reachable without leaving the task. If reaching it takes longer than guessing, people will guess.
6. Set the upkeep: an owner by role, a review interval you choose, and the trigger for an early update, which is a change in the process.
7. Prepare the walk-through test. A person who does the work runs a real task with the aid while you watch the aid, never the person. Where they stop, a step is missing. The expert then confirms every step.

## Output Format
```markdown
# Job Aid
Task: [task] | Used by: [role] | Format: [checklist / decision table / one-page flow] | Why a job aid fits: [rare / changes often / many details / costly error], confirmed by [role]
## The aid
| Step or condition | Do this | Watch out for |
|---|---|---|
| [step, or "if ..."] | [verb-led action] | [the common mistake here] |

Left off the page on purpose: [background], kept in [place]
## Where it lives
Moment in the workflow: [moment] | Channel: [where] | How it is reached mid-task: [route]
## Walk-through test
| Real task used | Where the person stopped | Change made to the aid |
|---|---|---|
| [task] | [step or "no stop"] | [change] |
## Upkeep
| Owner | Review every | Early-update trigger | Last checked | Expert who confirmed the steps |
|---|---|---|---|---|
| [role] | [interval] | [process change] | [date] | [name] |
## Decision
[Process owner name] approves the content and the placement by [date], after [expert name] has confirmed every step.
```

## Done When
- The reason a job aid fits is named and confirmed by a person, and the format matches the shape of the task
- The aid fits one page or one screen, and every line starts with an action
- The placement says where the aid is and how it is reached mid-task
- The walk-through has run on a real task, and an owner, a review interval and an early-update trigger are set

## Quality Bar
- No background on the page: if a line is not used during the task, it moves out
- The common mistake sits beside the step where it happens, never in a notes box at the bottom
- An aid nobody can find mid-task has failed, however well it reads; intervals and dates are yours, and a step I cannot trace to your source is marked "ask the expert"
- Claude drafts the aid; the process owner approves it and the expert confirms every step.

## Next
Run ldg-build-the-70-20-10-plan (Build the 70-20-10 Plan) to place the learning in real assignments.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
