---
name: isd-live-to-elearning
description: Maps a live session by what the room did, then drafts what replaces each part on screen, what stays live or goes to a manager conversation, the new outline, and a list of what is lost with who accepts it. Use for "run isd-live-to-elearning", "put the workshop online", "convert this classroom course to e-learning", "turn our live training into self-paced", "they want a recording of the slides", "what do we lose moving this online", "which parts must stay live", "convert instructor-led training", part of the Claude for Instructional Designers Pack by 90n.
---

# Live Session to E-Learning Conversion
## When To Use
"Put the workshop online" means a recording of slides. The session worked because of what happened in the room, and none of that is in the deck. It answers: what did participants do, what can a screen replace, what still needs a person, and who accepts what goes missing?

## When Not To Use
Not for deciding whether training is the fix at all: that is Course Brief. Once the conversion is decided, Course Curriculum Map lays out the lessons and E-Learning Storyboard Template writes the screens. If the session should simply stay live, say so and stop.

## Inputs
- The session plan or agenda with timings as they were really run, the deck, and the facilitator's notes, including the questions they ask and the answers they usually hear
- What participants did in each block (exercises, discussions, role plays, handouts), who asked for the conversion, and what they expect to gain from it
If you have none of this, I start from the facilitator's account of one run of the session and mark the output as a first draft, with unknown blocks tagged `[ask the facilitator]`.

## Approach
The mapping aid is Gagné's nine events of instruction, as set out in the Northern Illinois University guide: gain attention, inform learners of objectives, stimulate recall of prior learning, present the content, provide learning guidance, elicit performance, provide feedback, assess performance, enhance retention and transfer. Merrill's First Principles of Instruction (2002) supply the test for the result: a real problem, with demonstration and application kept in. The nine events are used here to find what lived in the room, not as a script for the new course. The failure this prevents: the slides go online, the three events the facilitator carried in person disappear, and the completion report looks fine.

## Workflow
1. Ask at most three questions: what the session is for and who attends, by role; what participants do in the room that people remember afterwards; what the requester expects the online version to change. Nothing else is asked later.
2. Inventory the session by what the room did, not by slide. For each block: what the facilitator did, what participants did, what feedback they got and from whom. A block where participants only listened is recorded as exactly that.
3. Map each block to the nine events and mark which events lived in the room and not in the slides. Guidance, performance and feedback are the usual three; show the gaps before proposing anything.
4. For each block choose one route and give the reason: replace on screen (with a decision, a scenario, a worked example, or a reflection with a model answer), keep live (a short session or a peer conversation), or hand to a manager conversation with a prompt sheet. You make the call on anything that depended on a person reading the room.
5. Write the loss list honestly: live feedback on a person's own attempt, discussion between peers, a facilitator adjusting to the group. Each loss gets a role who accepts it or a route that keeps it live.
6. Draft the new outline with the practice kept in and checked against the real problem, demonstration and application. The recording of the old session is at most a reference, never the course. Durations stay as `[duration you set]`. Then list the facts taken from the deck and notes for the expert, and name what the requester must agree to before design starts.

## Output Format
```markdown
# Live Session to E-Learning Conversion Plan
Session: [name] | Audience: [role] | Requested by: [role] | Sources read: [plan, deck, notes, versions] | Date: [date]
## What the room did
| Block | Facilitator did | Participants did | Feedback they got, and from whom | Events of instruction present | Event carried by the room only |
|---|---|---|---|---|---|
| [block] | [action] | [action] | [feedback] / [facilitator, peer, none] | [events] | [event or "none"] |
## Route for each block
| Block | Route | What replaces it | Reason | What is lost |
|---|---|---|---|---|
| [block] | [on screen / keep live / manager conversation] | [decision, scenario, worked example, reflection with model answer, short session, prompt sheet] | [reason] | [loss or "nothing"] |
## What is lost, and who accepts it
| Loss | Why a screen cannot do it | Kept live instead? | Accepted by | Date |
|---|---|---|---|---|
| [loss] | [reason] | [yes, how / no] | [role and name] | [date] |
## New outline
| Order | Part | Format | Practice the learner does | Objective | Duration |
|---|---|---|---|---|---|
| [n] | [part] | [on screen / live / manager conversation] | [practice] | [objective] | [duration you set] |

Manager conversation prompt sheet. Purpose: support for the learner on [task]. Prompts: [question 1], [question 2], [question 3]. Nothing from this conversation is reported back.
## Facts for the expert
- [fact], from [deck slide / notes]: [confirmed / to confirm with the expert]
## Decision
[Name, designer] decides by [date] the route for each block. [Name, sponsor] accepts each loss or pays to keep it live, by [date]. [Name, expert] confirms the facts by [date].
```

## Done When
- Every block of the session has a row in the inventory and a route
- Every event carried only by the room has a replacement, a live route or a named loss, and every loss has a role and a name against it
- The new outline keeps at least one piece of practice per objective, and no part of it is "watch the recording"

## Quality Bar
- The inventory describes what people did. Slide titles are not an inventory.
- No claim that the online version is shorter, cheaper or better by any ratio; durations are yours.
- The manager conversation is support for the learner, never a report on them.
- Reusing a recording with participants in it raises consent and rights questions: check with a qualified adviser.
- Claude maps what the room did; you decide what the learner still needs from a person, and a named person accepts what is lost.

## Next
Run isd-ai-accuracy-check (AI Content Accuracy Check) to trace every fact to an approved source once a draft exists.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
