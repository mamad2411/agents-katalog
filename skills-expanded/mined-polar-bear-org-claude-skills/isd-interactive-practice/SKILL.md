---
name: isd-interactive-practice
description: Drafts one practice activity as a Claude artifact to prototype and pilot, with the spec behind it, a test log you fill in, and a plain note on where it can and cannot live. Use for "run isd-interactive-practice", "prototype a practice activity", "make a decision activity I can click", "build a sorting exercise to try", "try this practice idea before the build", "turn this scenario node into something clickable", "can learners open a Claude artifact", "quick interactive practice for my course", part of the Claude for Instructional Designers Pack by 90n.
---

# Interactive Practice Activity
## When To Use
You want to try a practice idea this afternoon, before anyone opens the authoring tool. You have one objective and a hunch about the activity, and you would rather click through a rough version than argue about it in a meeting. It answers one question: does this practice idea work, and is it worth building for real?

## When Not To Use
Not for a course component learners will be tracked on: this is a prototype, and it stays one. For a full chain of linked decisions written out for a developer, use Branching Scenario Script. For watching real learners try the whole built course, use Learner Pilot Test.

## Inputs
- The objective this activity practises, and the action on the job behind it
- The real mistakes people make on this task, from your expert's notes or a scenario node, and the source for every rule, number or step the activity will use
- Who will try the prototype, by role, and whether they have a Claude account
If you have none of this, I start from one objective in your words and mark the output as a first draft, with every option tagged `[to confirm with the expert]`.

## Approach
The method is application with feedback, from Merrill's First Principles of Instruction (2002): people learn a task by doing it on a real problem and seeing what happens. The feedback follows Shute's 2007 research report on formative feedback, which separates verifying a response, explaining the answer, giving a hint and showing a worked example, and notes that what works depends on the learner and the task. The spec is the durable deliverable and the artifact is a sketch of it. The failure this prevents: a lovely clickable thing gets shown to the sponsor, everyone assumes it is the course, and three weeks later someone discovers it cannot go where the learners are.

## Workflow
1. Ask at most three questions: which objective and which single decision or sort the learner makes; which real mistakes the wrong options come from; who will try the prototype and where. Nothing else is asked later.
2. Write the spec before anything is built: the objective, the situation in the learner's work language (marked fictional), the options, the consequence and the feedback for each, and what "done" looks like. If you cannot say what the learner decides in one line, the idea is not ready and the spec says so.
3. Pick one of three shapes and say why: a single decision with consequences, a sort (items into categories, with feedback on each miss), or a short scenario of two or three linked decisions. Choose the smallest shape that still makes the learner commit to something.
4. Write the feedback to three rules: show the consequence before the explanation; say why, not only right or wrong; give a hint before the answer where the task allows a second try. A wrong option nobody would pick is cut. Every rule, number and step is listed for the expert, never corrected or filled in.
5. Draft the activity as an artifact in the Claude conversation, from the spec and nothing else. Leave out scoring, names, leaderboards and saved attempts: the activity stores nothing about who chose what. Claude Design is an option if you want a clickable prototype with a standalone HTML export.
6. You test it as a learner would, and Claude does not do this for you: every option clicked, every path ended, keyboard only once, on a phone once. Paste your notes and I sort them into the test log as what broke and what confused, with the fix against the spec first and the artifact second. The output closes with the "where it can live" note in plain words and the decision: rebuild from the spec, change the idea, or drop it.

## Output Format
```markdown
# Interactive Practice Activity Spec and Test Log
Activity: [name] | Version: [n] | Date: [date] | Status: prototype, not a course component
## Spec
| Element | Content |
|---|---|
| Objective and job action | [objective] / [action] |
| Shape, and why | [single decision / sort / short scenario]: [reason] |
| Situation the learner sees (fictional), and what "done" looks like | [who, where, what is at stake] / [what the learner has decided or sorted] |
## Options and feedback
| Option or item | Real mistake behind it | Consequence shown first | Feedback that says why | Hint before the answer | Rule, number or step used, and its source |
|---|---|---|---|---|---|
| [option] | [mistake, from the expert's notes] | [what happens in the story] | [why] | [hint or "no second try"] | [fact] / [source, or to confirm with the expert] |
## Test log (filled in by the designer)
| Pass | Date | What broke | What confused | Fix to spec or artifact |
|---|---|---|---|---|
| Every option clicked, every path ended | [date] | [note] | [note] | [fix] |
| Keyboard only | [date] | [note] | [note] | [fix] |
| On a phone | [date] | [note] | [note] | [fix] |
## Where it can live
- It opens only for people who have a Claude account. Sharing is by link or invitation and follows your organisation's settings. Nothing is tracked and nothing reports to your LMS. The package and the tracking happen in your authoring tool and your LMS.
- For a course, rebuild it in your authoring tool from this spec. If you used Claude Design, a standalone HTML export exists; whether your authoring tool or LMS accepts it is yours to test: [tested / not tested].
## Decision
[Name, designer] decides by [date]: rebuild from the spec, change the idea, or drop it. [Name, expert] confirms the facts by [date]. Tested by [name] on [date].
```

## Done When
- The spec stands alone: a developer could rebuild the activity without opening the artifact
- Every wrong option traces to a real mistake, and every fact has a source or a `[to confirm with the expert]` tag
- Every test pass is logged by the designer with its date, and the "where it can live" note is in the output, unsoftened

## Quality Bar
- The situation and its characters are marked fictional; no real customer, colleague or incident is recognisable.
- Never promise an export to a standard e-learning package, embedding in a course page, or that people without Claude can open it.
- No scoring, no names, no saved attempts: the activity collects nothing about a learner.
- This is a prototype you test yourself: nothing is tracked, no learner's choices are stored, and the course version is built and checked in your authoring tool.

## Next
Run isd-course-slides (Course Slides Build) to build the deck when part of the course is delivered as slides.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
