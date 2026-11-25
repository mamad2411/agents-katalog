---
name: fac-spaced-retrieval-plan
description: Plans recall after a session by choosing the few things people need from memory, writing a recall question or short scenario for each and setting widening gaps the trainer chooses. Use for "run fac-spaced-retrieval-plan", "spaced repetition", "retrieval practice", "spaced retrieval after training", "recall questions after a workshop", "quiz questions to send after training", "they could do it in the room and froze later", "reinforcement questions without an LMS", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Spaced Retrieval Plan

## When To Use
People could do it in the room and freeze a month later, in front of a real customer or a real team. Use this once the session content is settled, to decide which few things must still be in people's heads when the moment comes and how they will be asked to pull them back out. It answers one question: what do people recall, through which prompt, and after which gaps?

## When Not To Use
If you need the messages that carry the prompts (dates, senders, opt-out), run Post-Session Follow-Up Sequence; this plan writes no logistics message. If people can look the answer up mid-task, it does not belong here: put it in Participant Handout.

## Inputs
- The session's learning points and the handout or slides, so look-up content can be separated out.
- The real mistakes people make with this skill, in your words or the sponsor's.
- How long people need to keep this ready, and how you can reach them (email, chat, a slot in a team meeting).
If you have none of this, I start from the session title and three things people practised, and mark the output as a first draft.

## Approach
Cepeda and colleagues' 2006 review of spacing and Dunlosky and colleagues' 2013 review of learning techniques found that spacing and practice testing help, and that the useful gap grows with how long material must be kept. That evidence comes from students and verbal tasks, so the plan takes it as a direction, gives no standard schedule and promises no retention figure. The failure it prevents is the "reinforcement" email that resends the key slides: people reread them, feel they know it, and have practised recognising, which is not what the job asks of them.

## Workflow
1. Ask at most three questions: how long must people keep this ready, which mistakes cost most when it is forgotten, and through which channel will the prompts reach people?
2. Choose the three to five things needed FROM MEMORY in the moment. Test each one: could they stop and look it up mid-task? If yes, it goes to the handout and off this plan.
3. Write one recall prompt per thing. It asks people to answer or decide, never to reread. Prefer a short scenario built on a real mistake over "what is the definition of".
4. Give each prompt its answer, one line on why, and one line on where it shows up at work. An answer with no "why" teaches the wording.
5. Set the gaps. They widen across the time people must remember, and the longer that time, the wider the later gaps. You set each gap as `[days]`; nothing here is a standard. Each thing returns more than once, with the scenario varied so people recall the idea and not the sentence.
6. Say how results are read, if any are gathered: by question and in aggregate, groups under `[minimum group size]` suppressed. A question most people miss is a session problem, and it goes on your list for the next run.
7. Hand over the check you run before anything is sent: answer each prompt cold and ask "did I have to think, or did I recognise the slide?" Recognition prompts are rewritten.

## Output Format
```markdown
# Spaced Retrieval Plan
Session: [title] | People must keep this ready for: [period] | Channel: [email / chat / meeting slot]
## What must be in people's heads
| # | The thing | The moment at work that needs it | Moved to the handout instead |
|---|---|---|---|
| 1 | [thing] | [moment] | [look-up content, if any] |
## Recall prompts
| # | Thing | Prompt (question or scenario) | Answer and why | Where it shows up at work |
|---|---|---|---|---|
| 1a | [thing] | [scenario built on a real mistake] | [answer, then why] | [task] |
| 1b | [thing] | [varied scenario] | [answer, then why] | [task] |
## Gaps
| Send | Gap from the last one | Prompts |
|---|---|---|
| [first] | [days] after the session | [1a, 2a] |
| [second] | [days] | [3a, 1b] |
## Reading results
By question, in aggregate. Groups under [minimum group size] suppressed. A prompt most people miss goes to: [change in the session].
Limits: the evidence comes from students and verbal tasks; this plan promises no retention result.
## Decision
[Trainer] sets the gaps and approves the prompts after answering each one cold, and [sender] agrees the channel, by [date].
```

## Done When
- The plan holds three to five things, and each names the moment at work that needs it from memory.
- Every prompt asks for an answer or a decision; none asks people to reread or rewatch.
- Every gap is a number of days you set, the gaps widen, and each thing returns in a varied scenario.
- You have answered every prompt cold and rewritten the ones you only recognised.

## Quality Bar
- Prompts are built on real mistakes, not trick questions.
- The plan can be sent by email or chat by one trainer; it needs no LMS.
- No forgetting or retention figure, and no gap offered as a rule.
- The limit of the evidence is written on the plan itself.
- Answers are practice: read by question and in aggregate, never reported against a named person.

## Next
Run fac-manager-briefing-note (Manager Briefing Note) because recall alone does not create use at work.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).