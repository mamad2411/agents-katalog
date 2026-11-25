---
name: fac-activity-debrief-questions
description: Writes a three-step debrief question sequence for each activity and for the close of the day (what happened, what it means, what you will do), with a follow-up for thin answers and a version for pairs. Use for "run fac-activity-debrief-questions", "debrief questions for this exercise", "what so what now what", "how do I debrief a role play", "the debrief fell flat", "reflection questions after an activity", "closing questions for my workshop", "nobody answers when I ask how was that", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Activity Debrief Questions

## When To Use
The exercise was lively and then the debrief is "so, how was that?" Three people say "good", and the point of the activity leaves with the flipchart. Use this once the activities are chosen, to write what you will ask after each one and at the close, so the room gets from what happened to what they will do.

## When Not To Use
Not for the debrief inside a role play: Role-Play Practice Kit keeps its own. Not for the team's review of how the session went: that is Facilitator Retro. Not for the written plan people take away: If-Then Action Plan does that. And the questions are prepared beforehand; you ask them, in your order, when the room is ready.

## Inputs
- Each activity: its instructions, what people produce, and the learning point or outcome it serves.
- The session's aim, what people should do differently at work, and the group: how many, in person or virtual, how willing to speak in plenary.

If you have none of this, I start from a one-line description of each activity and mark the output as a first draft.

## Approach
The sequence is What? So what? Now what?, as set out in the University of Edinburgh's Reflection Toolkit: the experience, what it means, the action. It was written for individual reflection, so each question is rewritten for a group and for this activity. Tannenbaum and Cerasoli's 2013 meta-analysis of debriefs found that structured debriefs focused on learning, not blame, improve later performance, and that structure and facilitation appear to matter. The failure this prevents: three bare headings on a slide, which get you three bare answers.

## Workflow
1. Ask up to three questions: which activities need a debrief and what each is for, what people should do differently at work afterwards, and how readily this group speaks in front of each other.
2. Write the "what" question for this activity, about what people did and saw: what did you do, what did you notice, what was the outcome. It must contain something only this activity has.
3. Write the "so what" question, which turns the event toward the work: what surprised you, what did you base your choice on, what would you do differently.
4. Write the "now what" question with a place and a moment in it: what will you do, where, the next time it comes up.
5. Add one follow-up per step for a thin answer ("say more about the moment when ...", "what made that hard?") and a pairs version of the whole sequence: the same three questions, `[minutes]` each way, one thing shared per pair.
6. Write the close of the day on the same three steps across the whole session, with its "now what" handing over to the action plan. Set `[minutes]` per debrief and mark it protected: an activity with no debrief is cut before a debrief is.
7. Hand over the check a person runs: you read each "what" question and ask "can someone answer this without having done the activity?" If yes, it is too generic and is rewritten.

## Output Format
```markdown
# Activity Debrief Questions
Session: [title] | Aim at work: [what people should do differently]
## [Activity name] (debrief: [minutes], protected; in pairs: [minutes] each way, one thing shared per pair)
| Step | Question to ask | Follow-up for a thin answer | Pairs version |
|---|---|---|---|
| What | [question only this activity allows] | [follow-up] | [same question, in pairs] |
| So what | [question] | [follow-up] | [same question, in pairs] |
| Now what | [question with where and when] | [follow-up] | [same question, in pairs] |
## Close of the day (debrief: [minutes], protected)
| Step | Question to ask | Follow-up for a thin answer | Pairs version |
|---|---|---|---|
| What | [across the whole session] | [follow-up] | [pairs] |
| So what | [question] | [follow-up] | [pairs] |
| Now what | [question that hands over to the action plan] | [follow-up] | [pairs] |
## Checks (run by the trainer)
| Activity | Can the "what" question be answered without doing the activity? | Rewritten |
|---|---|---|
| [activity] | [yes or no] | [new wording, if yes] |
## Decision
[Trainer name] sets the minutes for each debrief and names the activity that is cut first if time runs short, by [date]; in the room, [trainer name] decides plenary or pairs.
```

## Done When
- Every activity and the close has three questions in order, written for that activity.
- Each step has one follow-up, and each sequence has a pairs version.
- The trainer has run the check on every "what" question and rewritten the generic ones.
- The last "now what" hands over to a written action plan, and debrief minutes are set by the trainer and marked protected.

## Quality Bar
- No question can be answered with "good", "fine" or "interesting".
- One question at a time: no step stacks two questions in one breath.
- Questions ask about the work and the choice made, never about how someone performed.
- Claude writes the questions; you ask them and listen, and nothing about who answered or how is written down.

## Next
Run fac-if-then-action-plan (If-Then Action Plan) to turn the last "now what" into something people write down.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).