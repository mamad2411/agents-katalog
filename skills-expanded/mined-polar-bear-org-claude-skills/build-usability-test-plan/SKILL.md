---
name: build-usability-test-plan
description: Writes a Five-User Usability Test Plan with test goals tied to the belief on your test card, task scenarios that do not give the path away, success criteria set before any session, a word-for-word moderator script with the think-aloud ask and neutral prompts, an observer note grid and a pilot. Use for "run build-usability-test-plan", "write a usability test script", "I have never moderated a session", "tasks for my prototype test", "what do I say in a user test", "think aloud script", "how do I test my prototype with users", "my script asks if they like it", part of the Claude for Product Builders Pack by 90n.
---

# Five-User Usability Test Plan

## When To Use
The prototype is ready, the sessions are booked, and your script says "click here and tell me if you like it". This skill answers: which tasks, which words and which notes will show where real target users get stuck, and what do you say when they do?

## When Not To Use
If you do not yet have real target users and their consent, run Tester Recruitment and Consent Note. If there is no belief or pass line to test against, run Prototype Test Card. A walk through the screens with no users is Prototype Heuristic Review, and it never replaces a session.

## Inputs
- Your test card (the belief, the task and the pass line) and the prototype as a link or screenshots, showing invented data only.
- Who takes part, how many, and how long each session is.
If you have none of this, I start from the one flow you most need to see someone use and mark the output as a first draft.

## Approach
Moderated usability testing as the GOV.UK Service Manual describes it (https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing), with thinking aloud (Nielsen Norman Group, https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/) and five users per round as a rule of thumb (Nielsen Norman Group, 2000, https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/). Give a goal, not a tour, then stay quiet while the person works. The failure this prevents: a first-time moderator who explains each screen, rescues every pause and comes back with five people who "liked it".

## Workflow
1. Ask at most three questions: which belief on the test card is this round testing; which part of the prototype does each task touch; who takes part, in one group or several?
2. Tie each test goal to the belief and to a part of the prototype. A goal with no belief behind it is cut. Three tasks seen properly beat seven rushed ones.
3. Write each task as a clear goal that is believable, hard enough to show problems, and gives no hint of how to do it: "You need to [goal]; go ahead." No words that appear on a button or a menu.
4. Write success criteria per task before any session: what counts as completed, completed with help, and not completed. "Help" is any hint from you beyond a neutral prompt.
5. Write the moderator script word for word: the introduction ("we are testing the prototype, not you"), the consent check, the think-aloud ask, then mostly silence. Neutral prompts only: "What are you thinking?" "What did you expect?" Never "do you like it" or "would you use it". When they struggle, wait, and decide in advance when you step in.
6. Build the observer grid per task: outcome against the criteria, path taken, hesitations, exact words with a time mark. Book a note-taker for each session if you can, so the moderator can watch.
7. Set the logistics and the pilot: sessions of 30 to 60 minutes with gaps of at least 15 minutes, and one pilot with a colleague to fix the tasks. The pilot is never a result. Five per round finds problems and measures nothing, and talking aloud changes timing, so no time on task is reported.

## Output Format
```markdown
# Five-User Usability Test Plan
**Prototype and version:** [name, version label] | **Belief under test:** [from the test card] | **Sessions:** [number per group, dates, minutes] | **Pilot:** [date, with a colleague; tasks changed after it]
## Test goals
| Goal | Belief it serves | Part of the prototype |
|---|---|---|
| [goal] | [belief] | [screen or flow] |
## Tasks and success criteria
| Task | Scenario as read aloud | Start point | Completed | Completed with help | Not completed |
|---|---|---|---|---|---|
| [number] | "You need to [goal]; go ahead." | [screen] | [criteria] | [criteria] | [criteria] |
## Moderator script
1. Introduction: "We are testing the prototype, not you. Nothing you do here is wrong." Consent check: [points to confirm].
2. Think-aloud ask: "[words]". Then silence. Neutral prompts: "What are you thinking?" "What did you expect?"
3. I step in when: [rule set in advance]. Never asked: "Do you like it?" "Would you use it?" Close: [one open question], thanks, what happens with their notes.
## Observer grid (one per session, by participant code)
| Task | Outcome | Path taken | Hesitations | Exact words and time mark |
|---|---|---|---|---|
| [number] | [completed / with help / not completed] | [path] | [where] | "[exact words]" [time mark] |
## Decision
[The builder, by role] fixes the tasks and criteria after the pilot by [date]; they do not change once the first real session starts.
```

## Done When
- Every goal traces to the belief on the test card, and every task has a scenario with the path unstated and success criteria dated before the first real session.
- The script holds no "do you like it", "would you use it" or leading prompt.
- The observer grid matches the tasks, and a pilot with a colleague is booked.

## Quality Bar
- The prototype shows invented data, never a participant's own account or records.
- The script tells participants they are not being tested, and nothing in the grid rates a participant.
- The pilot session is used to fix the tasks and is never counted or quoted as a finding.
- Consent is checked aloud before the session starts. Consent and recording law: check with a qualified adviser.
- Claude writes the tasks; real target users attempt them, and only what they did becomes a finding.

## Next
Run build-usability-findings (Usability Test Findings) to read what the sessions showed, task by task.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
