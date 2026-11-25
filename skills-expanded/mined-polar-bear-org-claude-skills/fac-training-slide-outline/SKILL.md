---
name: fac-training-slide-outline
description: Builds a slide-by-slide outline for a training session, producing content slides with a sentence headline and the evidence each needs, one instruction slide per activity, a cut list and accessibility notes. Use for "run fac-training-slide-outline", "training slides", "slide outline", "training deck outline", "fix my training deck", "too many bullet points", "I end up reading my slides aloud", "activity instruction slide", "accessible slides", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Training Slide Outline

## When To Use
The deck is the session, and the trainer ends up reading it aloud. Use this when the plan is agreed and the slides have to be built or rebuilt around it. It answers: what does each slide say in one sentence, what does it show, and which slides should not exist?

## When Not To Use
If the content still does not fit the minutes, settle that first with Session Time Budget; this outline does not reopen what stays. What the trainer says belongs in the Trainer and Facilitator Guide, and what people write in belongs in the Participant Handout.

## Inputs
- The session plan or agenda, with block names and the activity in each block.
- The existing deck or the content list, what the time budget already cut or moved, and any access needs people have told you about.
If you have none of this, I start from the objectives and the list of blocks, and mark the output as a first draft.

## Approach
Two public sources carry this: the assertion-evidence approach (Penn State's Leonhard Center), where the headline is a sentence stating the message and visual evidence sits under it with no bulleted list, and the W3C Web Accessibility Initiative's guidance on accessible presentations. Assertion-evidence was built for technical talks, so activity slides get their own pattern here. The failure it prevents: a topic title over six bullets, read aloud to people who finished reading it before you started.

## Workflow
1. Ask at most three questions: which plan block does each part of the deck serve, what has already been cut or moved to the handout, and is this shown in a room or on a video call?
2. Tag every slide to the plan block it serves. A slide that serves no block goes to the cut list with a destination: handout, follow-up or removed. Who asked for the slide is not a reason to keep it.
3. Write each content slide as a full-sentence headline that states the message. Test: read the headlines alone, in order; if they do not make the argument, the headline is still a topic.
4. Under each headline, describe the evidence it needs in words: a diagram, a photo of the real thing, a worked example. You make or find it; I do not generate images. No bulleted list, and detail goes to the handout.
5. Write one instruction slide per activity with four things only: the task, the groups, the time, what to bring back. It stays on screen for the whole activity.
6. Add the accessibility notes: little text per slide, large text, strong contrast, little motion, alt text for every image, materials sent ahead, visuals described aloud.
7. List every activity slide for the check you run before the deck is built: could someone who walked in late do the task from this slide alone? The agreed outline can then be built in Claude Slides (beta) or inside your own template with Claude for PowerPoint.

## Output Format
```markdown
# Training Slide Outline
Session: [title] | Blocks: [number] | Slides: [number] | Shown in: [room or video call]
## Slides
| No. | Plan block | Type | Headline as a full sentence, or the task | Evidence to make or find | Alt text |
|---|---|---|---|---|---|
| [n] | [block] | Content | [the message in one sentence] | [diagram, photo of the real thing or worked example, described in words] | [what the visual shows] |
| [n] | [block] | Activity | Task: [task] / Groups: [groups] / Time: [minutes] / Bring back: [output] | None | None |
## Cut list
| Slide or item | Why it serves no block | Destination |
|---|---|---|
| [item] | [reason] | [handout / follow-up / removed] |
## Accessibility notes
- [ ] Little text per slide, detail moved to the handout; large text, simple fonts, strong contrast, little motion
- [ ] Alt text written for every image; visuals described aloud; materials sent ahead to [who asked]
## Checks
| Activity slide | Could someone who walked in late do the task from this slide alone? | Answered by |
|---|---|---|
| [n] | [yes, or no and the fix] | [trainer] |
## Decision
[Trainer] approves the outline and the cut list by [date], before any deck is built; [trainer] tells [sponsor or content owner] what was cut and where it went by [date].
```

## Done When
- Every slide is tagged to a plan block or sits on the cut list with a destination.
- Every content slide has a sentence headline and described evidence, with no bulleted list.
- Every activity has one slide carrying the task, the groups, the time and what to bring back.
- The trainer has answered the late-arrival check for every activity slide.

## Quality Bar
- The headlines read in order tell the session's argument without the trainer.
- I set no slide count, no minutes per slide and no line limit; the plan's blocks set the size of the deck.
- No statistic, quote or result appears on a slide unless you supplied it; a missing fact is a bracketed placeholder.
- Example slides use no real participant's name or case.

## Next
Run fac-participant-handout (Participant Handout) to give everything that came off the slides a place people can use.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).