---
name: pdes-critique-notes-to-actions
description: Sorts raw critique notes into Critique Actions and Reply, with duplicates merged, every note placed as tied to an objective, preference, out of scope or open question, your call on each tied note (change, will not change and why, test), actions with owners and dates, and a three-line reply to the room. Use for "run pdes-critique-notes-to-actions", "sort my crit notes", "I got twenty comments at critique", "which feedback do I act on", "the feedback contradicts itself", "turn crit feedback into actions", "write the reply after crit", part of the Claude for Product Designers Pack by 90n.
---

# Critique Notes to Actions

## When To Use
You left crit with twenty comments, half of them contradicting each other, and the loudest one in your head. By Friday you will have redesigned around it unless something stops you. It answers: which notes touch the objectives I stated, what will I change and not change, and what do I tell the room?

## When Not To Use
If the comments came from stakeholders and someone above them decides, use Stakeholder Feedback Log: peer notes have no approver, those do. If nobody wrote the notes down, I cannot rebuild them: write what you remember first, or ask the room to send theirs.

## Inputs
- The raw notes from the session, yours or the recorder's, however messy, with names removed
- The objectives and the one question you stated, ideally your Critique Session Brief
If you have no objectives, I sort against the question alone and mark the output as a first draft.

## Approach
Feedback sorted against the stated objectives, the core of objective-led critique as Nielsen Norman Group describes it (Design Critiques, 2016). A note tied to an objective is a sign the work may miss its goal; a note tied to nothing is a preference, worth hearing and not acted on by default. I sort by whether a note points at an objective, not by whether it is right. The failure it prevents: a whole flow rebuilt around one strong opinion that touched no objective, while the quiet note about the error state went nowhere.

## Workflow
1. Ask three questions: what were the objectives and the one question, which notes came from people outside crit (they belong elsewhere), and by when does the team expect your reply?
2. Merge duplicates and keep the original wording. Record how many notes merged into each line, never who made them.
3. Sort every note into one of four buckets: tied to objective [n], preference, out of scope (you said so before the session), open question. A note that fits two is shown in both and you choose.
4. For each tied note you decide: change, will not change (with your reason), or test. I lay contradicting notes side by side under the objective they share; I do not decide which is right.
5. Turn each change and each test into an action with an owner and a date. Each open question gets an owner who will find the answer. Items marked "test" are written as the question a session with real users would settle.
6. Draft the three-line reply: what I heard, what I will change, what I will not change and why. You write line three and you send it. If the team has no reply window, ask for one before you leave the next session.

## Output Format
```markdown
# Critique Actions and Reply
**Work:** [artifact] | **Session:** [date] | **Notes received:** [count from your notes] | **Reply due:** [date]
## Objectives stated
1. [objective]
## Notes, sorted
| Note (original wording) | Merged from | Bucket | Objective | My call |
|---|---|---|---|---|
| [note] | [n notes] | [tied, preference, out of scope or open question] | [n or none] | [change, will not change with reason, or test] |
## Contradictions, side by side
| Objective | Note A | Note B | My call |
|---|---|---|---|
| [n] | [note] | [note] | [call and reason] |
## Actions
| Action | Type | Owner | Date |
|---|---|---|---|
| [what will be done] | [change, test or open question] | [role] | [date] |
## Reply to the room
1. What I heard: [one line]
2. What I will change: [one line]
3. What I will not change, and why: [your line]
## Decision
[Designer] confirms every call on the tied notes and sends the reply by [date]; [product manager] agrees by [date] which "test" items go into the next sessions with users.
```

## Done When
- Every note sits in a bucket in its original wording, none was added, and contradicting notes sit side by side under one objective
- Every tied note has your call, and every change, test and open question has an owner and a date
- The reply fits in three lines, you wrote line three and you are the one who sends it

## Quality Bar
- I never add a note nobody made, and never guess what the room meant
- Preferences stay visible in the table; they are not deleted and not promoted
- No "who said what", no count of who spoke, no description of anyone's manner
- Claude sorts the notes by objective; you decide what to act on, and items marked "test" go to real users

## Next
Run pdes-usability-test-plan (Usability Test Plan) to settle the "test" items with real users.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
