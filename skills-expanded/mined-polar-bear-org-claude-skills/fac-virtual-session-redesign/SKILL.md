---
name: fac-virtual-session-redesign
description: Rebuilds an in-room session plan for a video call, producing shorter blocks and breaks you set, an interaction for every block with the tool named, a breakout plan with a written task and a scribe, the producer role and a plan B for each tool. Use for "run fac-virtual-session-redesign", "virtual training", "move my workshop online", "virtual facilitation", "keep a virtual session engaging", "breakout room instructions", "cameras on or off", "people multitask on video calls", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Virtual Session Redesign

## When To Use
The in-room day is moved online as it is, and by the second hour half the group is answering email. Use this when you already have a plan that works in a room and it now has to run on your video platform. It answers: what has to change block by block, and who runs the tools while you watch the group?

## When Not To Use
This skill converts a plan; it does not design one or change its purpose. With no plan yet, start with Training Session Plan or Workshop Agenda. The wider set of what-ifs, a technology failure among them, sits in Difficult Moments Plan; here plan B is one line per tool.

## Inputs
- The in-room plan or agenda, pasted, with its blocks and timings.
- The tools your video platform gives you (chat, polls, annotation, breakouts, a shared document), whether you have a producer, the headcount and the slot.
If you have none of this, I start from the list of blocks and the slot and mark the output as a first draft.

## Approach
The four proposed causes of video-call fatigue in Bailenson's 2021 theoretical paper on video-call fatigue, used as a redesign checklist: close-up eye contact, seeing yourself constantly, reduced mobility, higher cognitive load. It is an argument, not an experiment, and it gives no attention-span figure; neither do I. The failure this prevents: the same slides and the same talk, one person juggling chat, a poll and breakouts, and a trainer who never once looks at the group.

## Workflow
1. Ask at most three questions: what is the in-room plan, which tools and which producer do you have, and how many people in what slot?
2. Go through the plan block by block and ask four questions. Where does this block hold people in close-up eye contact, keep them watching themselves, pin them to the chair, or load them with extra effort to send and read signals?
3. Choose one counter-move per cause. A camera invitation, not a rule: say when cameras help and that off is fine. A reminder that self-view can be hidden. Blocks that let people stand, move or work off screen. Fewer things to watch at once, so one channel per block.
4. Give every block an interaction with the tool named generically (chat, poll, annotation, breakout, shared document), and set block and break lengths as `[minutes]`. A block with no interaction is a broadcast; say so and decide whether it should be a recording sent ahead.
5. Write the breakout plan: the task written where the group can see it once the room opens, a scribe chosen by the group, the time, what to bring back. A spoken instruction does not survive the move into a breakout room.
6. Name the producer: who runs chat, polls, breakouts and the waiting room so you can watch the group. With no producer, cut tools until one person can run it.
7. Write plan B per tool in one line, and note any block that could not be converted so it goes back to the plan.

## Output Format
```markdown
# Virtual Session Plan
Session: [title] | Converted from: [in-room plan] | On: your video platform | Group: [number] | Producer: [name / none]
## Fatigue check by block
| In-room block | Close-up eye contact | Watching yourself | Pinned to the chair | Effort to send and read signals | Counter-move chosen |
|---|---|---|---|---|---|
| [block] | [where] | [where] | [where] | [where] | [move] |
## Rebuilt flow
| Time | Block | Length | Interaction and tool | On or off screen | Who runs the tool |
|---|---|---|---|---|---|
| [time] | [block] | [minutes] | [chat / poll / annotation / breakout / shared document] | [on / off] | [trainer / producer] |
| [time] | Break | [minutes] | [none] | Off | [none] |
## Breakouts
| Block | Task as written for the group | Where they see it | Scribe | Time | Bring back |
|---|---|---|---|---|---|
| [block] | [task] | [shared document / chat] | Chosen by the group | [minutes] | [what] |

Camera invitation, said at the start: [the sentence you say: when cameras help, and that off is fine]
## Plan B
| Tool | If it fails |
|---|---|
| [tool] | [one line] |
## Decision
[Trainer] confirms block lengths, tools and the producer by [date]; [producer] rehearses the tools by [date].
```

## Done When
- Every block has been through the four questions and has a counter-move or a note that none is needed.
- Every block has an interaction with a named tool and a named person running it.
- Every breakout has a written task, a scribe chosen by the group, a time and something to bring back.
- Every tool has a plan B, and one person can run everything that is left.

## Quality Bar
- Block and break lengths are yours; no attention-span figure and no ideal length appear.
- The purpose of the session is not redesigned; a block that cannot be converted goes back to the plan.
- Whether a session may be recorded depends on place, contract and consent: check with a qualified adviser.
- Cameras are an invitation, never a rule; nothing tracks who has a camera on, who spoke or who typed, and no recording starts without consent.

## Next
Run fac-pre-work-invitation (Pre-Work and Invitation) to tell people what to expect and what to have ready.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).