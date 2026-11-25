---
name: pdes-usability-test-plan
description: Writes a moderated Usability Test Plan with test goals tied to design questions, task scenarios that leave the path unstated, success criteria set before testing, a moderator script with a think-aloud ask and neutral prompts, and an observer note grid with sample and pilot notes. Use for "run pdes-usability-test-plan", "write a usability test script", "usability test plan for my prototype", "task scenarios for user testing", "think aloud script", "how many users do I need to test with", "my script is a guided tour", "prep my user testing sessions", part of the Claude for Product Designers Pack by 90n.
---

# Usability Test Plan

## When To Use
The prototype is ready, the sessions are booked, and the script is a guided tour: "here is the dashboard, click the filter, what do you think?" Run this before anyone sits down with a participant. It answers: which tasks, which words and which notes will show where people get stuck in your design?

## When Not To Use
If nobody has said what the prototype is meant to prove or how real it must be, use Prototype Brief first. If no real person is available this round, do not swap in an AI pass and call it a test: run Design Self-Critique and label the result an inspection.

## Inputs
- The design questions you want answered, and the flow under test (a link, screenshots, or a frame list)
- Who takes part, how many sessions are booked and how long each one is
- Optional: the Figma connector, which reads frames, variables and components, to list the frames in the flow
If you have none of this, I start from the one flow you most need to watch someone use and mark the output as a first draft.

## Approach
Moderated usability testing as the GOV.UK Service Manual describes it, with thinking aloud and the five-user rule and its limits, both from Nielsen Norman Group. A task is a goal a person believes in, with no hint at how to reach it, followed by your silence. You are testing your own work, so your bias is the main risk: you moderate and stay quiet, and someone else takes the notes. The failure this prevents: a designer who walks five people through the happy path, hears "looks nice", and reports the design as tested.

## Workflow
1. Ask up to three questions: what design questions must this round answer, which flow and frames are under test, and who takes part (one user group or several).
2. Tie each test goal to a design question and a part of the flow. A goal with no question behind it is cut.
3. Write the tasks to the GOV.UK rules: a clear goal, relevant and believable, hard enough to show problems, and no hint at how to complete it. Several smaller tasks in a logical order. Strike any word that also appears as a label on screen.
4. Write success criteria per task before testing: what counts as completed, completed with help, not completed. Once sessions start, the bar does not move.
5. Write the moderator script: an intro that says the design is being tested, not the person; a consent check before recording; the think-aloud ask; neutral prompts; open questions after each task. No "do you like it". Stay mostly quiet and step in only if someone is completely stuck.
6. Build the observer note grid per task, and assign roles: you moderate, one note-taker, observers who stay silent. Thinking aloud is unnatural, filtered and open to moderator bias, so no time on task is reported from these sessions.
7. Set the sample and the pilot: about five people per round find most problems, three rounds of five beat one round of fifteen, and each distinct user group needs its own participants. That is a rule of thumb that measures nothing. Sessions of 30 to 60 minutes, at least 15 minutes between. Run one pilot, then fix the tasks.

## Output Format
```markdown
# Usability Test Plan
**Design under test:** [flow, version] | **User groups:** [groups] | **Sessions:** [n per group, dates] | **Length:** [minutes]
## Test goals
| Goal | Design question | Part of the flow |
|---|---|---|
| [goal] | [question] | [screen or step] |
## Tasks and success criteria
| # | Scenario as read aloud | Start point | Completed | Completed with help | Not completed |
|---|---|---|---|---|---|
| 1 | "You need to [goal]. Go ahead." | [screen] | [criteria] | [criteria] | [criteria] |
## Moderator script
1. Intro: "We are testing the design, not you." Consent check before recording: [items].
2. Think-aloud ask: [words]. Neutral prompts: "What are you thinking?" "What did you expect to happen?"
3. Tasks 1 to [n], each followed by [open question]. Close: [open question], thanks.
## Observer note grid
| Task | Outcome | Path taken | Hesitations | Quote and timestamp |
|---|---|---|---|---|
| [#] | [completed / with help / not completed] | [path] | [where] | "[verbatim]" [mm:ss] |
## Sample and pilot
[n per group and why; moderator, note-taker and silent observers by role; what this round cannot show; pilot date and what changed after it]
## Decision
[Designer running the sessions] fixes the tasks after the pilot by [date]; [product manager] confirms the design questions this round must answer by [date].
```

## Done When
- Every task has a believable goal, an unstated path and success criteria written before testing
- The script has no "do you like it", no "would you use it" and no prompt that names a control
- A note-taker other than you is named, the grid matches the tasks, and a pilot is booked

## Quality Bar
- The prototype shows invented test data, never a participant's or customer's real account
- The plan says in plain words that five people find problems and measure nothing; no percentages and no time on task come out of it
- Consent is asked before any recording starts; what to record and how long to keep it, check with a qualified adviser
- Claude writes the tasks; real people attempt them, and only what they did becomes a finding

## Next
Run pdes-accessible-test-sessions (Accessible Test Sessions) so disabled people are in this round.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
