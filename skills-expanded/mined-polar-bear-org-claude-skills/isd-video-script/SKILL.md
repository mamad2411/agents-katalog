---
name: isd-video-script
description: Drafts a training video script in two columns (what is heard, what is seen) with a spoken-word rewrite, a shot or screen-capture list, and caption and transcript text planned at script stage. Use for "run isd-video-script", "write a training video script", "two-column script", "it sounds like a manual when read aloud", "script this screen recording", "rewrite this narration for the ear", "shot list for the demo", "captions and transcript for this video", part of the Claude for Instructional Designers Pack by 90n.
---

# Training Video Script

## When To Use
The script reads well on paper and sounds like a manual when someone says it aloud. Use this for anything linear the learner watches: a demonstration, a screen recording, a talking head, an animated explainer. It answers one question: what is heard and what is seen, second column against first, before anyone records.

## When Not To Use
Screens the learner clicks through belong in E-Learning Storyboard Template, and a slide deck in Course Slides Build. Checking captions on the finished video is Accessibility Check; here they are written.

## Inputs
- The objective, and the source: the procedure, the expert's notes, a draft script or the storyboard row that points here.
- The kind of video, the segment length you want, and who is the voice or on camera.
If you have none of this, I start from one objective and the steps described in a few lines, and mark the output as a first draft.

## Approach
The rules are the general multimedia principles: cut the video into short segments, signal what matters at the moment it is said, and never narrate the text that is on screen. They rest on cognitive load theory (Sweller, van Merriënboer and Paas, 2019, ERIC EJ1217401). Captions, a transcript and the description of visual information are planned now, as W3C WAI's "Making Audio and Video Media Accessible" advises. The failure this prevents: a sentence with a bracket, a four-item list and a reference number in it, handed to a narrator who has to say it in one breath.

## Workflow
1. Ask up to three questions: the objective and the kind of video, the segment length you set ([target length]), and who confirms the facts.
2. Cut the content into segments, one point each. A segment can stand alone and ends before the next idea starts. Anything that serves no point goes to a short cut list, which you approve.
3. Draft the two columns row by row. Heard: narration, dialogue, sound. Seen: the shot or the screen capture, and any on-screen text. One row, one thing happening.
4. Rewrite the heard column for the ear: short sentences, one idea each, the subject first, contractions where natural, no brackets, no list of more than three, numbers said the way a person says them.
5. Read it aloud once, start to finish. I cannot hear it, so this step is yours: tell me the rows where you tripped or ran out of breath and I rewrite those lines. Nothing is recorded before this pass.
6. Keep on-screen text to a label or a key term, never the sentence being spoken, and place each highlight on the row where the narration names it.
7. Write the caption text from the final narration and a transcript that also describes what must be seen to follow. Where a visual carries meaning the audio does not, either say it or note the description. Then list the shots or captures in order and the facts for the expert by row.

## Output Format
```markdown
# Training Video Script
Video: [title] | Objective: [objective] | Kind: [demo, screen recording, talking head, animation] | Segment length: [target you set] | Version: [n]
## Script
| Row | Segment | Heard (narration, dialogue, sound) | Seen (shot or screen capture) | On-screen text | Visual carries meaning the audio does not? |
|---|---|---|---|---|---|
| 1 | [segment name, one point] | [spoken line] | [what the camera or the capture shows] | [label or key term, or none] | [no, or what must be described] |
## Read-aloud log
| Row | Line that tripped | Rewrite | Read again by |
|---|---|---|---|
| [n] | [original line] | [new line] | [designer, date] |
## Shot or capture list
| Order | Row | Shot or capture | Must be on screen | Sample data used |
|---|---|---|---|---|
| 1 | [n] | [framing, or the screen and the action] | [field, button, object] | [fictional, marked] |
## Captions and transcript
Caption text: [the final narration, row by row] | Transcript: [narration plus a description of visual information needed to follow]
## Facts for the expert
| Row | Number, rule or step said or shown | Source | Confirmed |
|---|---|---|---|
| [n] | [claim] | [source or "to confirm with the expert"] | [yes, no, changed] |
## Decision
The designer reads the script aloud and clears it for recording by [date]. The expert, by role, confirms the facts by [date]. Nothing is recorded before both.
```

## Done When
- Every row has a heard cell and a seen cell, each segment makes one point, and no on-screen text repeats the sentence being spoken.
- The read-aloud log is filled in, or says "read aloud, no changes".
- Caption and transcript text exist, visual-only meaning is said or described, and every fact is listed by row for the expert.

## Quality Bar
- A line you would not say to a colleague across a desk is rewritten, and the picture changes when the idea changes, not for decoration.
- Sample data in a screen capture is fictional and marked; no real customer or colleague record appears.
- No invented testimonial or quote. Real people on camera need consent and rights to their image: check with a qualified adviser.
- Automatic captions are a starting text; a person corrects them against this script.
- Claude drafts the script; you read it aloud before anyone records it, and the expert confirms the facts.

## Next
Run isd-knowledge-check-questions (Knowledge Check Questions) to write the checks for each objective.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
