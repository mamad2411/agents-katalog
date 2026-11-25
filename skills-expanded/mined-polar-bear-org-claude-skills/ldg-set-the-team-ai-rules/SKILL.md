---
name: ldg-set-the-team-ai-rules
description: Prepares the L&D team's rules for working with AI, written with the team, producing a use map by task (Claude drafts, a person does, never), a never-put-in list, the check a person runs before anything ships, whose name is on the work, a disclosure line per output type and a review date. Use for "run ldg-set-the-team-ai-rules", "ai policy for l&d", "ai usage guidelines", "team rules for using AI", "AI working agreement", "disclose AI use in training", "what can we put into AI tools", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Set the Team AI Rules

## When To Use
Half the team uses AI quietly, the other half refuses, and nobody tells learners or sponsors what was AI-drafted. Each person has a private rule, and the private rules do not match. Run this to prepare one team session and write up what it agrees. It answers: which tasks Claude drafts, what a person always does, what never goes in, who checks before it ships, and what you tell the people who receive the work.

## When Not To Use
To check one draft before it ships, use Check the AI Draft; this sets the standing rules and points to that check. Whether a tool is allowed, and what data protection law requires, is the organisation's call: ask the policy owner and check with a qualified adviser before the team writes anything.

## Inputs
- The organisation's AI or data policy, if one exists (paste it or its key rules).
- The L&D tasks in scope, and how people work with AI on them today, said plainly: what helped, what went wrong.
- The output types you ship (course, deck, report) and who receives each.
If you have none of this, I start from the team's main tasks and mark the output as a first draft for the team session.

## Approach
The method is a team working agreement on AI, written by the team in one session: start from how people work with AI today, agree the rules together, publish them where the team works, and revisit them on a set date. Rules a team writes get followed; rules handed down get worked around. The judgement is to hear the people who refuse before the keen ones set the terms. The failure it prevents: a sponsor asks in a review whether the scenarios were written by AI, two people in the room give two different answers, and the course loses its credit over a question the team had never discussed.

## Workflow
1. Ask at most three questions: is there an organisation policy, which L&D tasks are in scope, and when can the team meet to write this together?
2. Prepare the opening round, without blame: how each person works with AI today, including who does not and why. Sceptics know where it fails, so their examples go on the board first. Nothing said here is recorded against a name.
3. Draft the use map for the team to correct, by task (intake notes, interview questions, objectives, storyboards, scenarios, question banks, slides, reports), in three columns: Claude drafts; a person does (talking to learners, experts and sponsors, running the room, deciding); never.
4. Build the never-put-in list: the organisation's policy first, then the team's additions (learner data, named people's results, confidential source material). Data protection points: check with a qualified adviser.
5. Set the check before anything ships, per output type: facts traced to a source and signed by the expert, a learner tries it, a pilot. Then the ownership rule: the person who ships the work has reviewed it, can explain it, and has their name on it.
6. Write one disclosure line per output type: what was AI-drafted and which person checked it, in one plain sentence a learner or a sponsor can read.
7. Set the review date and the home of the rules; a Project (redesigned, beta on select plans) is an optional place to keep them. The rules include no count of who uses AI or how much.

## Output Format
```markdown
# Team AI Rules
Team: [team] | Written together on: [date] | Organisation policy: [reference, or "none yet"] | Review date: [date]
## Use map
| L&D task | Claude drafts | A person does | Never |
|---|---|---|---|
| [task] | [what is drafted] | [the conversation, the room, the decision] | [what is off limits] |
## Never put in
- [organisation policy rule]
- [team addition] (data protection points: check with a qualified adviser)
## The check before it ships
| Output type | Check a person runs | Who runs it (role) |
|---|---|---|
| [course, deck, report] | [facts traced and expert sign-off, a learner tries it, a pilot] | [role] |
## Whose name is on the work
[The person who ships it has reviewed it, can explain it and owns it.]
## Disclosure lines
| Output type | Line the reader sees | Where it appears |
|---|---|---|
| [type] | [what was AI-drafted and who checked it] | [first screen, title slide, report footer] |
## Decision
[Named person] publishes the rules where the team works by [date]; the team reviews them on [date].
```

## Done When
- The team wrote or corrected every row; nothing is published from my draft alone.
- The never-put-in list starts from the organisation's policy, and every output type has a check, a role that runs it and a disclosure line.
- A review date is set and the Decision names a person.

## Quality Bar
- Rows name real L&D tasks, not general statements about AI.
- Ownership never passes to the tool: a named person can explain every piece of shipped work.
- Legal and data protection questions go to the policy owner or a qualified adviser; the rules never state law.
- The team writes the rules and a named person publishes them; nobody's use of AI is counted or monitored, and a person's name stays on every piece of work.

## Next
Run ldg-question-the-request (Question the Request) to go back to the front door with the rules in place.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
