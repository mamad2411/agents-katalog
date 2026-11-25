---
name: adopt-manager-follow-up
description: Prepares a manager's guide around one AI session or course, with the conversation before, the first real task after and the room made for it, the conversation after, check-ins inside existing meetings and a barrier log read in aggregate. Use for "run adopt-manager-follow-up", "manager follow-up after AI training", "what managers do after the AI session", "nobody used it after the training", "conversation before the AI course", "first task after AI training", "barriers to using AI after training", "make the AI training stick", part of the Claude Guide for AI Adoption Pack by 90n.
---
# Manager Follow-Up Guide
## When To Use
People come back from the AI session to a full diary and a manager who never asks what they tried, and by the second week the tool is closed again. Use this for one named session or course, before it runs, so each manager knows their part. It answers one question: what does the manager do before and after this session so that people get a real chance to use what they practised?

## When Not To Use
If you need the manager's standing role with no session attached (what to say to the team, what to show of their own use, what to ask in team meetings), run Manager AI Kit. If the barriers are already collected and need explaining, run AI Adoption Barrier Diagnosis; for exercises between sessions, run AI Practice Tasks.

## Inputs
- The session or course: title, date, what people practise in it, and who attends (by role).
- One or two real tasks where it should show up at work in the days after, and the meetings each manager already has with their people.
If you have none of this, I start from the session title and one task and mark the output as a first draft.

## Approach
This rests on transfer of training research (Blume, Ford, Baldwin and Huang, 2010): whether people use what they learned back at work relates to their motivation and to a supportive work environment. That evidence is correlational, the guide says so, and it promises no result. The judgment is that the manager's part must be small enough to happen: two short conversations, one cleared slot, one obstacle removed. The failure it prevents: a good session on Tuesday, a manager who books the person solid from Wednesday, and a completion record that everyone reads as success.

## Workflow
1. Ask three questions: which session is this and what do people practise in it, which real task could each role try first, and when do managers already meet their people?
2. Before. Write a short conversation ([minutes], you set it) with three questions at most, in the manager's words: why this session, what do you want from it, which real task will you try first. The person picks the task; the manager does not assign it.
3. First real task. Name a task that uses what the session covered, inside a window you set, and what the manager moves to clear room for it. If nothing can move, that is the first barrier to log, and it says more than any feedback form.
4. After. Four questions: what did you try, what happened, what got in the way, what do you need from me. The manager asks, listens and removes one obstacle. It is a conversation, never a quiz or a demonstration on demand, and "I chose not to use it" is an answer the manager hears out.
5. Check-ins. Place each one inside a meeting that already exists and give it one of three manager actions: ask about the task, remove an obstacle, or give credit for the try, including a try that failed.
6. Barrier log. Each entry holds a date, a category (time, tool, access, rule, workload, other) and the condition described, never the person. It goes to the enablement lead and is read in aggregate, with small groups suppressed below the size you set. No field records whether someone used AI or rates a conversation.

## Output Format
```markdown
# Manager Follow-Up Guide
Session: [title] | Date: [date] | For managers of: [roles] | Prepared by: [enablement lead]
## Before the session ([minutes], [days] before)
| Question the manager asks | Why it matters |
|---|---|
| [question] | [reason] |

## First real task
Task: [real task, chosen by the person] | Window: [days] after the session | Room made by: [what the manager moves or pauses; if nothing can move, log it below as the first barrier]
## After the session
| Question the manager asks | What the manager does next |
|---|---|
| What did you try, and what happened? | [listen; a failed try and "I chose not to use it" are both answers] |
| What got in the way, and what do you need from me? | [one obstacle removed or logged, support agreed] |

## Check-ins
| Date | Existing meeting | Manager action | What the manager does |
|---|---|---|---|
| [date] | [meeting] | [ask about the task / remove an obstacle / give credit for the try] | [action] |

## Barrier log (conditions only, read in aggregate, nothing reported below a group of [size you set])
| Date | Category | Condition that blocked use | Sent to enablement lead |
|---|---|---|---|
| [date] | [time / tool / access / rule / workload / other] | [condition, no name] | [yes / no] |

## Decision
[enablement lead] and [sponsor] decide how the logged barriers get fixed, and by whom, by [date]; each manager holds the conversation before the session by [date].
```

## Done When
- Both conversations are in words a manager would say, and the first task is real work, chosen by the person, with a window you set and room cleared for it.
- Every check-in sits in a meeting that already exists and names one of the three manager actions.
- The barrier log has categories, a condition and no field for a name or a judgment.

## Quality Bar
- The transfer evidence is described as correlational; no promised effect on use.
- The guide covers one session: no script for a first team talk, no example of the manager's own use, no standing questions for team meetings.
- No field records whether a person used AI and no conversation is rated; Claude drafts, the manager has the conversations.
- The log records conditions, never people, and is read in aggregate; nothing in the guide feeds a performance review.

## Next
Run adopt-freed-time-agreement (Freed Time Agreement) to decide together what happens to the time AI frees.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
