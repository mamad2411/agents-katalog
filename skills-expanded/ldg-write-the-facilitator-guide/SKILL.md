---
name: ldg-write-the-facilitator-guide
description: Writes a guide another trainer can run a session from, producing the purpose, cue and key points per segment, questions with what a good answer sounds like, activity set-ups word for word, timing flex that never cuts practice and four what-if notes. Use for "run ldg-write-the-facilitator-guide", "facilitator guide", "trainer guide", "leader guide", "facilitator notes", "another trainer will deliver my session", "instructor guide template", "what if the room goes silent", part of The Complete Claude Guide for L&D Pack by 90n.
---
# Write the Facilitator Guide
## When To Use
Trainers are told to read the SOP aloud from slides, because nobody wrote down what each part of the session is for or how to run it. Use this when the session plan, the activities and the deck exist and someone other than their designer will deliver. It answers: what does the trainer say, ask and do in each segment, and what do they do when the room goes off plan?

## When Not To Use
If there is no timed flow, run Plan the Session first; a guide written on top of a deck turns into a script. If several facilitators have to learn the programme before they deliver it, this guide is the input and Train the Trainers is the skill.

## Inputs
- The session plan, the group work cards and the slide outline, with the objectives, and who will deliver (role, how well they know the topic).
- Notes from the designer or the expert on where learners usually get stuck.
If you have none of this, I start from the objectives and a rough agenda and mark the output as a first draft.

## Approach
A facilitator guide built on the session plan, where every segment names the event of instruction it serves (Gagné's nine events, a university teaching-centre page), so the trainer knows its purpose and can adapt without breaking it. The judgement is how much to write: prompts where the trainer should think, exact words only where a muddled instruction costs the room its practice time. The failure it prevents: a stand-in trainer gets the deck the evening before, reads every bullet, has no idea what a good answer to the discussion question would be, and says "great, thanks" to all of them. The guide can be written in Claude Docs (beta), or any document.

## Workflow
1. Ask at most three questions: who will deliver and how well do they know the topic, is it in the room or virtual, and which segment worries the designer most?
2. Write each segment's header: its purpose, the event of instruction it serves, the time from the session plan, the cue to start (what the trainer says or shows first) and three to five key points as short prompts.
3. Add the questions to ask. Each has what a good answer sounds like and a follow-up if the answer is thin. Prefer questions about people's work to questions about the slide.
4. Write activity set-ups word for word, and only those: the task, the groups, the time, what to hand back. Take them from the group work cards and flag any that differ from the card.
5. Add timing flex per segment: what to cut if late, never the practice, and what to add if early. Any timing that differs from the session plan is flagged, not changed silently.
6. Write the four what-if notes, each as a move the trainer can make in the moment: a silent room, one voice dominating, the technology fails, a question you cannot answer.
7. Check the guide for participant tracking and remove it: no attendance judgements, no space for notes on individuals. List the facts the trainer will state so the expert can confirm them.

## Output Format
```markdown
# Facilitator Guide
Session: [title] | Length: [minutes] | Format: [in the room / virtual] | Written for: [trainer role]
Read with: [session plan, version] / [slide outline, version] / [group work cards] | Set-up before the day: [room or meeting, materials, handouts]
## Segment [n]: [name]
Purpose: [why this segment exists] | Event it serves: [event] | Time: [minutes] | Slides: [numbers]
Cue to start: [what you say or show first]
Key points (prompts): [prompt] / [prompt] / [prompt]
| Ask | A good answer sounds like | If the answer is thin |
|---|---|---|
| [question] | [answer] | [follow-up] |

Activity set-up (say this): "[task, groups, time, what to hand back]" | From card: [n]
If late, cut: [what, never the practice] | If early, add: [what]
## What-if notes
| Situation | Your move |
|---|---|
| A silent room | [move] |
| One voice dominating | [move] |
| The technology fails | [move] |
| A question you cannot answer | [move] |

Facts the trainer states, for the expert to confirm: segment [n], [fact], [source and place], [confirmed / open]
## Decision
[Designer or L&D lead] and [delivering trainer] walk through the guide together and agree the changes by [date], before the pilot.
```

## Done When
- Every segment names its purpose and the event of instruction it serves.
- Key points are prompts; only the activity set-ups are word for word, and they match the cards.
- Every segment has a cut if late, and no cut removes practice.
- Each what-if note is a concrete move, not advice.

## Quality Bar
- Someone who has not seen the slides can run the session from the guide and the plan.
- Every question has a model answer, so the trainer knows when to move on and when to dig.
- Facts are listed with a source for the expert; the guide adds none of its own.
- Claude drafts the guide; the trainer adapts it to the room, and it carries no notes on any participant.

## Next
Run ldg-plan-the-pilot (Plan the Pilot) to test the whole session with a group before the launch.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
