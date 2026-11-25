---
name: ldg-build-the-training-slides
description: Builds the outline of a training deck from the session plan, producing a slide-by-slide outline tied to the session blocks, one idea per slide, practice and question slides, speaker notes as prompts, a list of what moves to a handout or job aid and a cut list. Use for "run ldg-build-the-training-slides", "training presentation", "training slides", "training deck", "slides for a workshop", "turn this SOP into slides", "death by PowerPoint", "fix my training deck", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Build the Training Slides

## When To Use
The deck is the SOP pasted onto slides and the trainer reads it aloud. Use this when the session plan and the activities exist and the slides have to serve them, or when an inherited deck has to be cut down to what the room needs to see. It answers: which slides does this session need, what goes on each, and where does everything else go?

## When Not To Use
If the content is self-paced screens with narration, run Storyboard the E-Learning; a live deck and an e-learning screen follow different rules. If there is no timed flow yet, run Plan the Session first, or the deck will become the plan.

## Inputs
- The session plan and the group work cards, or at least the blocks with their objectives.
- The source material: the SOP, the expert's deck, the existing slides.
- Your slide rules, typed in: fonts, colours, layout notes, the maximum words per slide you accept.
If you have none of this, I start from the topic, the objectives and the session length and mark the output as a first draft.

## Approach
Research-based principles for multimedia instruction (Mayer, 2008, American Psychologist), four of them: cut what is not needed for the objective (coherence), mark what is essential (signalling), do not put the spoken words on the slide as well (redundancy), and present in short segments. The studies were short lab lessons, so treat it as direction. The judgement is deciding what a slide is for: the thing people must look at while the trainer talks. The failure it prevents: every paragraph of the procedure gets its own slide, the room reads ahead of the trainer, and the one step people get wrong is in the same grey type as the revision history.

## Workflow
1. Ask at most three questions: which session plan does the deck serve, what source material must it draw on, and what slide rules should the outline carry?
2. Outline from the session plan, not from the source. Each slide names its block and the objective it serves; a slide with neither goes to the cut list with a reason.
3. One idea per slide, with a title that states the point as a sentence. If the title needs "and", it is two slides.
4. Apply coherence and signalling. Decoration, history and extra detail go to the cut list or the handout. Mark one thing per slide: the step, the number, the decision.
5. Apply redundancy. The slide carries the picture or the few words; what the trainer says goes into speaker notes as short prompts, never a script to read. List every fact on the slides with its source, for the expert to confirm.
6. Apply segmenting. After each short segment place a practice or question slide that shows the invitation from the matching activity card. Reference content moves to a handout or a job aid, listed with where it lands.
7. Hand over the outline. In Claude Slides (beta) the deck can be built from this outline in the conversation and downloaded as PowerPoint or PDF, or as a presentation file, if file creation is on. The outline carries your slide rules as written instructions.

## Output Format
```markdown
# Training Slide Outline
Session: [title] | Serves session plan: [version or date] | Slides: [number] | Length: [minutes]
## Slide rules (given by you)
Fonts: [rule] | Colours: [rule] | Layout: [rule] | Words per slide, at most: [number you set]
## Outline
| No. | Block | Objective served | Type | Title that states the point | On the slide | One thing marked | Speaker prompts |
|---|---|---|---|---|---|---|---|
| [1] | Open | [objective] | Problem | [title] | [picture or few words] | [what is marked] | [prompt] / [prompt] |
| [n] | Show | [objective] | Content | [title] | [picture or few words] | [what is marked] | [prompt] / [prompt] |
| [n] | Practise | [objective] | Practice or question | [title] | [the invitation from card n, or the question] | [time for the step] | [what a good answer sounds like] |
## Off the slides: moves and cut list
| Content | Goes to | Reason |
|---|---|---|
| [reference table, full procedure] | [handout / job aid] | [needed at the desk, not in the room] |
| [slide or content cut] | [cut, parked in: place] | [serves no block or objective / decoration / said aloud already] |

Facts for the expert to confirm: slide [no.], [fact as written], [source and place, or "not traced"]
## Decision
[Trainer] approves the outline against the session plan and [expert] confirms the facts by [date], before the deck is built.
```

## Done When
- Every slide names a block and an objective, and everything else is on the cut list with a reason.
- Each title states one point, and no slide repeats in text what the trainer will say.
- A practice or question slide follows each segment.
- Every fact on a slide has a source or is marked "not traced".

## Quality Bar
- Speaker notes are prompts a trainer can glance at, not sentences to read out.
- Slide counts, words per slide and segment lengths are yours to set; the outline states no norm.
- The research is direction from short lab lessons, never a promise about what people will retain.
- Claude drafts the outline and the deck; the trainer checks every slide against the session plan, and the expert confirms the facts.

## Next
Run ldg-write-the-facilitator-guide (Write the Facilitator Guide) so another trainer can run the session from the deck and the plan.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
