---
name: isd-learner-analysis
description: Drafts a learner analysis for one course, with learner groups by role and task, the context each will take it in, every line marked evidence or assumption, the design consequences and five questions to ask real learners. Use for "run isd-learner-analysis", "learner analysis", "audience analysis for a course", "who are the learners", "the brief says all staff", "learner context analysis", "what device will they use", "questions to ask learners", "learner persona", part of the Claude for Instructional Designers Pack by 90n.
---

# Learner Analysis

## When To Use
The brief says "all staff" and nobody has asked who will actually sit in front of the screen. Use this once a course is agreed and before any design choice is made. It answers: who does the task this course touches, where and when will they take it, and how much of what we believe about them has anyone checked?

## When Not To Use
If the problem itself is not agreed, run Course Brief first; this skill describes people, not the go or no-go. If the course is built and you want real learners to try it, that is Learner Pilot Test. Access needs are recorded here as constraints only; testing the build belongs to Accessibility Check.

## Inputs
- The audience line from the brief, the task or tasks the course touches, and whatever you really know: role lists, shift patterns, device and site facts, notes from managers, earlier feedback in aggregate.
- Who you could reach for a short conversation: three to five people who do the task.
If you have none of this, I start from the audience line and the task, mark the output as a first draft, and say at the top that it is all assumption.

## Approach
Learner and context analysis, from the analysis phase of instructional systems development (the 1975 Interservice Procedures written at Florida State University, ERIC record ED122022): describe who performs the task and the conditions they work and learn in before deciding how to teach it. The judgment is in separating what you know from what you suppose, and in talking to people who do the work. The failure it prevents: a narrated module with a headset icon on screen one, sent to people who share one terminal on a noisy floor and get ten minutes between tasks.

## Workflow
1. Ask at most three questions: which task does the course touch, which roles do that task and which do not, and which of your facts came from a person or a document rather than a guess?
2. Break "all staff" into groups by role and by the task. A group that does not do the task is out of scope and listed as such, with the reason, so nobody adds it back later.
3. For each group in scope, fill the same lines: what they already do and know about the task, the context of use (device, place, noise, shared or own screen, connection), real time available and when, language and reading needs, access needs, and what they have been told about why the course exists.
4. Tag every line. Evidence names where it came from (a document, a manager by role, a site visit). Anything else is an assumption. If most of the page is assumption, the first line of the output says so.
5. Write design consequences: one line for each finding that changes a design choice, for example no audio where people share a floor. A finding that changes nothing is left out of this table. You decide which consequences bind the design.
6. Draft five questions for three to five real learners, about the task and the conditions, not about opinions of training. Name who will ask them, by role. Claude writes the questions; a person asks, then pastes the notes back so assumption tags can change to evidence. A persona, if you want one, is a composite labelled "fictional, built from assumptions".

## Output Format
```markdown
# Learner Analysis
Course: [working title] | Task: [task] | Drafted by: [role] | Date: [date] | Evidence status: [mostly evidence / mixed / all assumption, not yet checked with learners]
## Groups
| Group (role) | Does the task? | In scope | Reason |
|---|---|---|---|
| [role] | [yes / sometimes / no] | [in / out] | [why] |
## Per group in scope
| Group | Line | What we have | Evidence or assumption | Source |
|---|---|---|---|---|
| [role] | Already does and knows; what they were told about why | [finding] | [evidence / assumption] | [document, manager by role, visit, or none] |
| [role] | Device, place, noise, screen, connection | [finding] | [evidence / assumption] | [source] |
| [role] | Real time available, and when | [finding] | [evidence / assumption] | [source] |
| [role] | Language, reading and access needs (as constraints) | [finding] | [evidence / assumption] | [source] |
## Design consequences
| Finding | Design choice it changes | Binding or to check |
|---|---|---|
| [finding] | [choice] | [binding / check with learners first] |
## Five questions for real learners
| Question | What the answer would change | Asked by | Asked of |
|---|---|---|---|
| [question about the task or the conditions] | [design choice] | [role] | [role, three to five people] |
## Decision
[Designer] decides which consequences bind the design once [role] has asked the five questions, by [date].
```

## Done When
- Every group is marked in or out of scope with a reason.
- Every line carries an evidence or assumption tag and, for evidence, a source.
- Each design consequence points to a specific choice, and the five questions have a named asker by role and a date.

## Quality Bar
- Groups are roles and tasks only; no individual is described and no protected characteristic is inferred.
- No invented personas, names, quotes or statistics; a composite is labelled fictional, and times, device counts and group sizes are yours or stay in brackets.
- What nobody could tell you is listed as unknown, with who might know, never filled in.
- Collecting or storing anything about identifiable learners raises data protection questions: check with a qualified adviser.
- Claude organises what you know and marks what is assumed; you talk to real learners, and nothing invented is passed off as research.

## Next
Run isd-action-mapping-workshop (Action Mapping Workshop) to turn the need into actions with the sponsor.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
