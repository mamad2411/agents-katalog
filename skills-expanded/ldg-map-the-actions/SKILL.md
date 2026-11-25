---
name: ldg-map-the-actions
description: Maps a course request from one business goal to what people must do, producing the measurable goal, the observable actions with why they are not happening, practice and minimum information per action, and a cut list for the expert's material (must-do, must-know, look-up, cut) with a reason and a parking place per cut. Use for "run ldg-map-the-actions", "action mapping", "action map", "from know to do", "cut this content down", "the SME sent a huge slide deck", "need to know versus nice to know", "content bloat", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Map the Actions

## When To Use
The sponsor wants a course, the expert sends a 147-slide deck, and you need to get from "they should know" to "they will do". Use this once the need is agreed and before any outline or storyboard exists. It answers: what must people do on the job to move the goal, what practice gets them there, and which of the expert's material stays?

## When Not To Use
The map starts from one measurable goal, so it is weak for pure awareness content with no business measure. To list and rate every task of a role, use Break Down the Task. Look-up items are only named here; Build the Job Aid makes the aid.

## Inputs
- The goal or problem line, and the measure the sponsor already watches.
- The role in scope and what the sponsor thinks people "should know".
- The expert's material: slides, documents, procedures, or at least a table of contents.
If you have none of this, I start from the sponsor's request and three actions you name, and mark the output as a first draft.

## Approach
Action mapping, from its originator's public page: start from a measurable business goal, list what people must do, ask why they are not doing it, design practice, and add only the information the practice needs. The cut list adds a working-memory test from cognitive load theory (Sweller, van Merriënboer and Paas, 2019). That research comes largely from classroom and lab tasks, so treat it as direction. The failure it prevents: the two decisions people get wrong every week sit on slide 112, behind the history of the department, and the session runs out of time at slide 60.

## Workflow
1. Ask at most three questions: which number should move and by when, which role must act differently, and which expert confirms the actions and rules on cuts?
2. Write one goal: "[measure] will [change] by [date] as [role] [do what]". Everything on the map links to it or is cut. If the sponsor cannot name a measure, stop and settle that first.
3. List the observable actions, verbs you could watch, never "understand" or "be aware of". Then mark the few that matter most for the goal; a map with twenty equal actions is a syllabus.
4. Per action, ask why it is not happening and name the fix: training, job aid or process change. Only actions blocked by skill or knowledge stay on the training path. My guesses about the work are marked for the expert to confirm.
5. For each training action, design the practice: a decision in a situation like work, with the consequence shown. Beside it, the minimum information that decision needs and where it lives.
6. Sort the expert's material into the cut list. Link each item to an action; no action means cut. Then four bins: must-do (practised), must-know (in the head during the task), look-up (job aid), cut. Run the working-memory test on every must-know item: is it needed in the head mid-task? If it can be looked up, it moves to look-up.
7. Give every cut a reason in the expert's terms ("accurate, and it lives in the reference page") and a parking place, so nothing true is thrown away and the expert has something to agree to.

## Output Format
```markdown
# Action Map and Cut List
Goal: [measure] will [change] by [date] as [role] [do what] | Sponsor: [role] | Expert: [role]
## Part 1: Actions
| Action (observable) | Matters most? | Why it is not happening | Fix | Confirmed by the expert? |
|---|---|---|---|---|
| [verb + object] | [yes / no] | [cause] | [training / job aid / process change] | [yes / to confirm] |
## Practice and minimum information
| Training action | Practice (decision in a work situation) | Consequence shown | Minimum information | Where it lives |
|---|---|---|---|---|
| [action] | [situation and choice] | [what happens after each choice] | [fact, rule or step] | [in the practice / job aid / reference] |
## Part 2: Cut list for the expert's material
| Item (slide, section, topic) | Linked action | Bin | In the head mid-task? | Reason in the expert's terms | Parking place |
|---|---|---|---|---|---|
| [item] | [action, or none] | [must-do / must-know / look-up / cut] | [yes / no] | [reason] | [reference page / appendix / job aid] |
## Disputed cuts
[Items the expert contests, with the action each one claims to serve.]
## Decision
[Sponsor] signs off the goal by [date]; [expert] accepts or contests each cut by [date] and rules on the disputed ones.
```

## Done When
- There is exactly one goal, with a measure and a date, and every action links to it.
- Every action is observable and has a reason and a fix; non-training fixes are named.
- Every practice asks for a decision, not recall, and carries only the information it needs.
- Every item of the expert's material sits in one bin, and every cut has a reason and a parking place.

## Quality Bar
- The goal measures a business result with the sponsor's own figure, never a named person and never an invented target.
- Cut reasons respect the expert: "accurate, and not needed in the moment", never "unnecessary".
- Nothing stays because it is interesting, recent or took long to write.
- Must-know survives only when it passed the working-memory test.
- Claude drafts the map and the cut list; the sponsor signs off the goal and the expert rules on every disputed cut.

## Next
Run ldg-interview-the-expert (Interview the Expert) to get the real decisions and mistakes behind each action.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
