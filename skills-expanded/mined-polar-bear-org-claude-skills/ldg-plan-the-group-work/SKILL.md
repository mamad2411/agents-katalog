---
name: ldg-plan-the-group-work
description: Designs the group activities of a training session, producing one activity card per practice block (purpose, structure, the invitation in the trainer's words, group sizes, minutes per step, how the output is collected), an opener built on the work, a virtual variant and a fallback for a quiet room. Use for "run ldg-plan-the-group-work", "group activities for training", "icebreakers for training", "breakout room activities", "workshop activities", "1-2-4-All", "engage a quiet group", "group discussion that works", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Plan the Group Work

## When To Use
The plan says "group discussion, 20 minutes" and the opener makes people cringe. Use this when the session has a timed flow and each practice block still needs a real design: who talks to whom, about what exact question, for how long, and what comes back to the room. It answers: what do people actually do in this block, and how does every voice get in?

## When Not To Use
If there is no timed flow yet, run Plan the Session first; a card with no block to sit in is a game looking for a slot. If the practice is a conversation with role cards and an observer, Build the Role-Play fits better than a group structure.

## Inputs
- The session plan, or at least the practice blocks with their objective and their minutes.
- The group (role, number, in the room or virtual) and real cases, messages or mistakes from the job to build on.
If you have none of this, I start from the topic, the group size and the time for one block and mark the output as a first draft.

## Approach
Liberating Structures, a public set of facilitation structures. Each one fixes five things: the invitation, how the space and materials are arranged, how participation is distributed, how groups are configured, and the sequence of steps with their timing. 1-2-4-All is the simplest example: alone, in pairs, in fours, then the whole group. The judgement is choosing by purpose, because a structure is not a learning objective. The failure it prevents: "discuss in your groups" is announced, two people talk, four wait, and the trainer fills the silence by answering the question themselves.

## Workflow
1. Ask at most three questions: which blocks need a card and what should people be able to do after each, how many people and in what format, and which real case or mistake from the job can the activities use?
2. Start each card from the block's purpose and objective, in one line. No purpose, no activity: if a block has none, send it back to the session plan and do not decorate it.
3. Choose the structure by purpose: getting every voice on one question, comparing cases, or giving peer feedback on work. Say in one line why it fits, and what it would be wrong for.
4. Fill the five elements. The invitation is the exact question, in the trainer's words, answerable from people's own work. Then space and materials, participation (everyone has equal time), group configuration, and the steps with minutes you set to fit the block. For 1-2-4-All the order is alone, pairs, fours, all.
5. Say how the output is collected (a sheet per group, a shared document, three points called out) and which block uses it next. Output nobody uses teaches the room that group work is filler.
6. Build the opener on the work: a real case, message or mistake people react to in pairs. Never a personal-disclosure game, and nothing that puts one person on the spot.
7. Add a virtual variant per card (breakouts, chat, a shared document) and a fallback for a quiet room: drop back to pairs, written first, then one point per pair.

## Output Format
```markdown
# Group Work Cards
Session: [title] | Group: [role, number] | Format: [in the room / virtual] | Cards: [number]
## Opener, built on the work
Shown to the room: [real case, message or mistake] | Invitation: "[exact question]"
Answered: [alone, then pairs] | Minutes: [set by trainer] | Leads into: [block]
## Card [n]: [block name]
Purpose: [why this block exists] | Objective served: [objective] | Structure chosen: [name] | Why it fits: [one line]
Invitation (say this): "[the exact question, in the trainer's words]"
Space and materials: [layout, sheets, shared document] | Participation: [how everyone gets equal time] | Groups: [configuration]
| Step | Who | What they do | Minutes |
|---|---|---|---|
| 1 | [alone] | [task] | [minutes] |
| 2 | [pairs] | [task] | [minutes] |
| 3 | [fours] | [task] | [minutes] |
| 4 | [all] | [task] | [minutes] |

Output collected as: [form] | Used next in: [block, and how]
Virtual variant: [breakouts, chat or shared document, with the change to each step]
If the room is quiet: [drop back to pairs, written first]
## Decision
[Trainer] chooses the structure for each block and confirms the minutes per step by [date], before the slides are built.
```

## Done When
- Every practice block of the session plan has a card, and every card names a purpose and an objective.
- Each invitation is one question a person can answer from their own work.
- The minutes per step add up to the block's time in the session plan.
- The opener uses the work, and each card has a virtual variant and a quiet-room fallback.

## Quality Bar
- The structure is chosen for the purpose and the reason is written; novelty is not a reason.
- Minutes, group sizes and intervals are [placeholders] you set to fit the block.
- Nobody is asked to share personal information or to perform alone in front of the group.
- Claude drafts the cards; the trainer chooses and runs the activity, and nobody's contribution is counted or reported.

## Next
Run ldg-build-the-training-slides (Build the Training Slides) to build the deck around the activities, not the other way round.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
