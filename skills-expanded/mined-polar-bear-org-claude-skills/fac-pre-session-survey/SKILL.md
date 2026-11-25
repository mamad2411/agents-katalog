---
name: fac-pre-session-survey
description: Writes a pre-session survey of five to seven questions for participants, the invitation line that goes with it and an aggregate summary template that feeds the design. Use for "run fac-pre-session-survey", "pre-workshop survey", "pre-training questionnaire", "questions to ask participants before training", "I have never met this group", "learner analysis", "collect real cases before the session", "ask about access needs", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Pre-Session Survey

## When To Use
You are designing for a group you have never met and the only description is a job title. Run this once the purpose is agreed and there is still time to change the design. It answers: what does this group do all day, which real situations do they want to work on, and what would stop anyone from taking part?

## When Not To Use
Not after the session: Session Feedback Form does that, and it rates the session. Not for the invitation itself or the "come with" ask, which belong to Pre-Work and Invitation and go out later. If the design is locked and no answer could change it, do not ask; and with a handful of people, three short conversations tell you more than a form.

## Inputs
- The session's purpose and topic, from your brief or the sponsor call note.
- Who is invited, by role or group, roughly how many, and when the design has to be settled.
- After the survey closes: the answers, exported without names.
If you have none of this, I start from the topic and the job title and mark the output as a first draft.

## Approach
This is learner analysis kept at the level of role and task: what the work involves, never who the person is. It leans on one finding from the 2005 meta-analysis of behaviour modelling training by Taylor, Russ-Eft and Chan, that scenarios trainees bring themselves are among the features linked to use at work, so the survey's main job is to collect real cases. The access question follows the W3C Web Accessibility Initiative's guidance on accessible presentations: real needs have to be asked for, not guessed. The failure this prevents is the practice case you made up, which the room dismisses in a minute as "not how it works here".

## Workflow
1. Ask three questions, all at once. What will people practise or produce in the session? Who reads the answers, and can the survey be anonymous? What minimum group size do you want before a role or team is shown on its own?
2. Write five to seven questions in this order: the role and what the work involves; a real situation they would like to work on, with no names and no confidential detail; what would make the time worth it; what they already do or know on the topic, as a description in their own words; access needs and anything that would make it hard to take part; one optional open line.
3. Refuse the questions that sort people. No personality, style, colour or type items, and no "rate your level" scale. If you want to know where the group starts, the description question tells you, and it tells you about the work.
4. Write the invitation line: who reads the answers, that they are anonymous by default, how the cases will be used (as practice material, reworded so no situation can be traced), and that nothing goes to anyone's manager.
5. Read each question as a participant would and cut any that would not change the design. Then check the whole survey can be answered in the time you set.
6. Build the summary template, and fill it once you paste the answers: themes by role with counts, the cases reworded into practice scenarios, the access needs as a to-do list with an owner. Any role or group under your minimum is merged into a larger one. Close with the design changes the answers point to, each tied to a theme, for you to accept or reject.

## Output Format
```markdown
# Pre-Session Survey
**Session:** [working title] | **Sent by:** [name] | **Closes:** [date] | **Read by:** [name or role] | **Time to answer:** [minutes]
## Invitation line
[Two or three sentences: why we ask, who reads the answers, anonymous by default, cases reworded and used as practice material, nothing goes to your manager.]
## Questions
| No. | Question | Answer type | What it changes in the design |
|---|---|---|---|
| 1 | What is your role, and what does a normal week involve? | Short text | [which examples and language fit] |
| 2 | Describe a real situation on [topic] you would like to work on. No names, no confidential detail. | Text | [the practice scenarios] |
| 3 | What would make this time worth it for you? | Short text | [what gets the most room] |
| 4 | What do you already do or know on [topic]? Describe it in a line or two. | Short text | [where the session starts] |
| 5 | Is there anything we should arrange so you can take part fully? | Text, optional | [room, materials, timing, format] |
| 6 | Anything else we should know? | Text, optional | [open] |
## Summary for the design
**Answers received:** [count] of [invited]. Groups under [minimum group size] are merged.
| Role or group | Theme | Count | What it means for the design |
|---|---|---|---|
| [role] | [theme in the group's words] | [count] | [change] |

**Practice scenarios, reworded:** 1. [scenario] 2. [scenario] 3. [scenario]
**Access to-do list:** [need, stated without a name] | [what is arranged] | [owner] | [by date]
## Decision
[Trainer name] decides by [date] which design changes are made from the summary, and confirms the access arrangements with [owner].
```

## Done When
- There are five to seven questions, in the order above, each naming what it changes in the design, and none types, rates or ranks the person answering.
- The invitation line says who reads the answers and how the cases are used.
- The summary shows themes and counts by role, with small groups merged at the minimum you set.

## Quality Bar
- Every question earns its place by changing something in the design. Curiosity is not a reason to ask.
- Cases are used as practice material only after rewording, and never with a name, a team or a client attached.
- Access needs become arrangements and are never listed next to a name in the summary.
- Survey answers are personal data, and access needs can be sensitive: for how to collect, store and delete them, check with a qualified adviser.
- Answers are read by role and theme to shape the design; no participant is profiled or typed, and nothing goes to their manager.

## Next
Run fac-training-session-plan (Training Session Plan) to design from what the group said.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).