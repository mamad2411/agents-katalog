---
name: isd-job-aid-template
description: Drafts a job aid as a checklist, a decision table or a one-page flow, with the common mistake next to its step, a placement line, a test log from a real task and an upkeep table. Use for "run isd-job-aid-template", "job aid template", "make a quick reference for this task", "they need the answer in the middle of the task", "a checklist, not a module", "decision table for this process", "one-page flow for this procedure", "test this job aid on a real task", part of the Claude for Instructional Designers Pack by 90n.
---

# Job Aid Template

## When To Use
People need the answer in the middle of the task, and a module is the wrong place for it. The step is rare, the rule changed last month, or there are more details than anyone holds in their head. Use this to draft the thing they look at while they work, to decide where it sits, and to test it before it is relied on.

## When Not To Use
If you are still sorting a pile of source material to find what is look-up, run Source Content Triage first; this drafts one aid for one task. If the task needs judgement under pressure that no table can hold, practise it with Branching Scenario Script.

## Inputs
- The task (steps, choices, exceptions, the mistakes people make) and where it happens: the system, screen, counter or vehicle, and what the person already has in hand.
- Who owns the process, how often it changes, and someone new to the task who can try the aid.
If you have none of this, I start from the task described in a few lines, and mark the output as a first draft.

## Approach
Performance support at the moment of need: help that sits inside the work and is used while doing it. Action mapping, on its originator's public page, asks before any course whether a job aid alone would do. The judgement is format, placement and what to leave out. The failure this prevents: an aid that reads perfectly at a desk and is abandoned at step four, because it names a field the screen does not show and nobody watched a newcomer try it.

## Workflow
1. Ask up to three questions: what the person is doing and where when they need this, who owns the process and how often it changes, and who new to the task can test it.
2. Run the fit test. A job aid fits where the task is rare, changes often, has many details, or is costly to get wrong. You confirm which applies; if none does, I say so and the answer may be practice, or nothing.
3. Pick the format by the shape of the task: a checklist for fixed steps in order, a decision table for if-then choices, a one-page flow for a path that branches. The template holds all three; I fill one and say why.
4. Draft only what is needed during the task: one action per line, verb first, the common mistake next to the step where it happens. Background and reasons go to the "left out" line, with where they live. Steps I cannot find in your source are marked `[to confirm with the expert]`.
5. Set the placement and the upkeep: the exact point in the work and how the person reaches the aid without leaving the task, then the owner by role, the review interval you set and the trigger for an early update. In Claude Docs (beta) the aid can be a one-page document you export; where it is pinned or printed is yours to arrange.
6. Test it on a real task. Someone who does not know the task follows the aid once while you watch and say nothing, and you log where they stop. I do not run this test; I sort your log and propose the fix for each stop. The test is of the aid, never of the person.

## Output Format
```markdown
# Job Aid
Task: [task] | Format chosen: [checklist, decision table or flow] because [task shape] | Why a job aid fits: [rare, changes often, many details, costly to get wrong] | Version: [n] | Keep the format chosen and delete the other two
## Format A, checklist (fixed steps in order)
| Step | Do this | Watch out for |
|---|---|---|
| 1 | [verb first, one action] | [the common mistake at this step] |
## Format B, decision table (if-then choices)
| If | And | Then do | Watch out for |
|---|---|---|---|
| [condition] | [second condition or "any"] | [verb first, one action] | [the common mistake] |
## Format C, one-page flow (a path that branches)
1. [Verb first, one action]. If [condition], go to step [n]. If not, [action]. Watch out for [mistake].
## Left out, placement and upkeep
Left out: [what is not on the aid, and where it lives: reference page, course, nowhere]
Placement: [the point in the work, the channel, how the person reaches it without leaving the task]
Upkeep: owner [role] | review every [interval you set] | early-update trigger [process or system change] | last checked [date]
## Test on a real task
Followed by: [role, new to the task] | Watched by: [designer] | Date: [date]
| Step where they stopped | What they did or asked | Fix | In version |
|---|---|---|---|
| [step] | [observation] | [change to the aid] | [n] |
## Decision
The process owner, by role, signs every step and the placement by [date]. The designer decides the aid is ready after the test, or tests again, by [date].
```

## Done When
- One format is kept with its reason; every line starts with an action, and each common mistake sits next to its step.
- The aid fits one page or one screen, and the "left out" line says where the rest lives.
- The test log has at least one run by someone new to the task, with every stop fixed or explained, and an owner, a review interval and an update trigger are set.

## Quality Bar
- No paragraph of background on the aid. If it explains why, it has become a course.
- Words on the aid match the words on the screen or the equipment, letter for letter.
- A stop in the test is a fault in the aid. The log never names or rates the person who followed it.
- An aid nobody can reach mid-task has failed, however well it reads; an undated one is not issued.
- Claude drafts the aid; a person tests it on a real task, and the process owner signs every step.

## Next
Run isd-interactive-practice (Interactive Practice Activity) to prototype one practice activity before the build.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
