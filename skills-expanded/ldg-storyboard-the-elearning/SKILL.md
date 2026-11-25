---
name: ldg-storyboard-the-elearning
description: Writes an e-learning storyboard with screen-by-screen text, visual, narration and interaction, the objective each screen serves, accessibility notes, a cut list and a build brief for your authoring tool. Use for "run ldg-storyboard-the-elearning", "elearning storyboard template", "e-learning storyboard", "storyboard this course", "screen by screen script", "narration script", "turn these slides into e-learning", "brief for the person building the course", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Storyboard the E-Learning

## When To Use
The build starts from slides and ends as a knowledge dump with voiceover. Use this before anyone opens the authoring tool, to settle on paper what the learner sees, hears and does on each screen, and which objective that screen serves. Changing a row in a table costs minutes; changing a built screen costs a review round.

## When Not To Use
For a deck a trainer presents live, use Build the Training Slides. If the course is already built and you need the check before release, use Check the AI Draft. If nobody has yet decided what people must do on the job, Map the Actions comes first, because the big cuts are made there.

## Inputs
- The objectives and the practice planned for this module (design document or curriculum map row).
- The source material: slides, procedure, the expert's notes, any scenario already written.
- The target length, whether narration is used, and the accessibility level you work to (A or AA).
If you have none of this, I start from one objective and the source slides, and mark the output as a first draft.

## Approach
The method is cognitive load theory (Sweller, van Merriënboer and Paas, 2019): new information passes through a limited working memory, so load added by the presentation hurts learning. The storyboard is the cheapest place to take that load out. Accessibility notes follow WCAG 2.2 (W3C). The failure this prevents: a voice reading four bullets aloud while the same four bullets sit on screen, a "next" button, and the only thing the learner does in the whole module is a quiz on the last screen.

## Workflow
1. Ask at most three questions: the target length ([minutes]), narration or not, and the accessibility level (A or AA).
2. Group the source content under the objectives. Content with no objective goes to the cut list with its reason; a screen with no objective is not drafted.
3. Draft one row per screen: objective, on-screen text, visual, narration, interaction, accessibility note. One idea per screen; a second idea is a second screen.
4. Remove the load the presentation adds. Narration never repeats on-screen text word for word. A visual explains something or goes. No decorative animation.
5. Put practice inside every section: a decision, a sort, a short scenario. Each objective gets at least one practice screen before its check, so the learner has tried before being asked.
6. Add the accessibility note per screen: a text alternative for meaningful images, captions and a transcript for audio, contrast, keyboard access to every interaction. Whether the course meets a legal requirement: check with a qualified adviser.
7. Write the build brief for the person working in your authoring tool: screens by objective, interaction types, assets to make, what is still to confirm. It is a brief a person follows; nothing is exported or connected.

## Output Format
```markdown
# E-Learning Storyboard
Module: [name] | Target length: [minutes] | Narration: [yes or no] | Accessibility level: [A or AA]
## Screens
| # | Objective served | On-screen text | Visual (what it explains) | Narration | Interaction | Accessibility note |
|---|---|---|---|---|---|---|
| [n] | [objective] | [short text] | [what it shows, and why] | [script, not a copy of the text] | [choose, sort, decide, none] | [text alternative, captions, keyboard] |
## Cut list
| Content | Reason (no objective, look-up, duplicate) | Where it goes instead |
|---|---|---|
| [content] | [reason] | [job aid, reference, nowhere] |
## Build brief for your authoring tool
| Objective | Screens | Practice screens | Check | Interaction types |
|---|---|---|---|---|
| [objective] | [numbers] | [numbers] | [item to write] | [types] |

Assets to make: [image, diagram, audio, per screen number]
Still to confirm: [fact or wording] with [expert name]
## Decision
[Expert name] confirms the facts on every screen by [date]; [designer name] decides by [date] when the build starts.
```

## Done When
- Every screen names the objective it serves, and everything else is on the cut list.
- No narration line repeats its screen text word for word.
- Every objective has a practice screen before its check.
- Every screen carries an accessibility note, and the build brief lists what is still to confirm.

## Quality Bar
- A visual earns its place by explaining; a picture that only fills the space is cut.
- An interaction asks for a choice or a decision, never a click to reveal the next paragraph.
- The cut list travels with the storyboard, so the expert sees what went and why.
- The brief is written for a person; it claims no export and no link to any tool.
- Claude drafts the screens; the expert confirms every fact and the designer decides when the build starts.

## Next
Run ldg-write-the-knowledge-check (Write the Knowledge Check) to write the checks for each objective.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
