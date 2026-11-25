---
name: isd-storyboard-template
description: Drafts an e-learning storyboard with one row per screen (objective, screen type, on-screen text, visual, narration, interaction, build note, alt text), a coverage table by objective and a cut list. Use for "run isd-storyboard-template", "storyboard this course", "e-learning storyboard template", "turn the expert's slides into screens", "write the build notes for the developer", "it is narration over bullet points", "alt text for every image", "screen by screen plan", part of the Claude for Instructional Designers Pack by 90n.
---

# E-Learning Storyboard Template

## When To Use
The build starts from the expert's slides and ends as narration over bullet points. Use this before anyone opens your authoring tool, to decide screen by screen what the learner sees, hears and does, which objective each screen serves, and what the developer must build without guessing.

## When Not To Use
If the source has not been sorted and every slide is still "must include", run Source Content Triage first. Anything filmed or screen-recorded belongs in Training Video Script; the storyboard row only points to it. A deck for slide delivery is Course Slides Build.

## Inputs
- The objectives, and the lesson row from your course map with its practice and check.
- The approved source content, and any scenario script already written.
- Whether narration is used, and the constraints from your learner analysis (device, sound, time). In Claude Docs (beta) the storyboard can be a document your reviewers comment on.
If you have none of this, I start from one objective and the source slides, and mark the output as a first draft.

## Approach
Cognitive load theory (Sweller, van Merriënboer and Paas, 2019, Educational Psychology Review, ERIC EJ1217401) holds that new information passes through a limited working memory, so load added by the presentation itself costs learning. The storyboard is where that load is taken out: one idea per screen, a signal on what matters, short segments, no narration repeating the screen. The failure this prevents: a row that says "add an interaction here", a developer left to improvise, and a learner who gets click-to-reveal over the same bullets.

## Workflow
1. Ask up to three questions: which objectives this storyboard covers, whether there is narration, and who confirms the facts before the build.
2. Group the content under objectives. Content with no objective goes to the cut list with a reason and a place to live; a screen with no objective is cut. You decide what the learner sees, so I show you the cut list first.
3. Draft one row per screen, one idea per screen, and give each a type: tell, show, ask or practise. A second idea is a second screen.
4. Take out the load the presentation adds. Narration never repeats the on-screen text word for word; a visual explains something or goes; no decorative animation. For each visual I write what it shows and why it is there.
5. Put practice inside every section, not only at the end: each objective gets at least one practise screen before its check. A video screen points to its script and is not written here.
6. Write the build note in plain words that describe behaviour, never a tool's menu: what happens on click, what state changes, what the developer must not improvise ("on a wrong choice, show the consequence text, then let the learner try again"). Draft alt text per image, following W3C guidance on text alternatives: what the image tells the learner here, or "decorative, empty alt".
7. Close with coverage by objective and a count of tell screens against ask and practise screens. The count describes the draft; it is not a score and not a target. Every number, rule and step in the text is marked for the expert.

## Output Format
```markdown
# E-Learning Storyboard
Course: [name] | Lesson: [name] | Narration: [yes or no] | Version: [n] | Facts confirmed by: [role]
## Screens
| # | Objective | Type | On-screen text | Visual (what it shows and why) | Narration | Interaction | Build note | Alt text |
|---|---|---|---|---|---|---|---|---|
| 1 | [objective] | [tell, show, ask, practise] | [short text] | [image or diagram and its job, or "video, see script [ref]"] | [script, not a copy of the text] | [choose, sort, type, none] | [what happens, what changes, what not to improvise] | [text alternative or "decorative, empty alt"] |
## Coverage by objective
| Objective | Screens | Practise screens | Check | Flag |
|---|---|---|---|---|
| [objective] | [numbers] | [numbers] | [item ref] | [no practice, no check, or none] |

Tell screens: [count] | Show: [count] | Ask: [count] | Practise: [count]
## Cut list
- [content] | [reason: no objective, look-up, duplicate] | [where it lives now: job aid, reference page, nowhere]
## Facts for the expert
| Screen | Number, rule or step | Source | Confirmed |
|---|---|---|---|
| [n] | [claim] | [source or "to confirm with the expert"] | [yes, no, changed] |
## Decision
The expert, by role, confirms every fact in the screen text and narration by [date]. The designer decides what is cut and whether the build starts, by [date].
```

## Done When
- Every screen names its objective and its type, and no narration line repeats its screen text word for word.
- Every objective has a practise screen inside its own section.
- Every interactive screen has a build note a developer could follow without asking.
- Every image has alt text or is marked decorative.

## Quality Bar
- Interactions ask for a choice or a decision; "click to reveal the next paragraph" is a tell screen in disguise and is typed as one.
- Build notes describe what the learner experiences. They name no tool and no feature.
- Alt text is drafted here and tested on the build in Accessibility Check. The package and the tracking happen in your authoring tool and your LMS.
- The cut list travels with the storyboard, so the expert sees what went and where it lives.
- Claude drafts the screens; the expert confirms every fact before the build, and you decide what the learner sees.

## Next
Run isd-video-script (Training Video Script) for any screen that is a video.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
