---
name: isd-course-slides
description: Drafts a course deck slide by slide from your storyboard, with a build sheet of one idea per slide, notes kept apart from slide text, planned practice slides and an export check you run yourself. Use for "run isd-course-slides", "turn my storyboard into slides", "build the course deck", "one idea per slide", "my authoring tool starts from a deck", "split the slide text from the narration", "add practice slides to this deck", "check the PowerPoint export before I import it", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Slides Build
## When To Use
Part of the course is delivered as slides, or your authoring tool starts from a deck. The storyboard or the course map exists and you need the deck that follows it, not the expert's deck with a new title page. It answers: what goes on each slide, what is said and not shown, and does the exported file survive being opened?

## When Not To Use
Not for designing the course screen by screen: that is E-Learning Storyboard Template, and this skill builds from it. Anything filmed or screen-recorded belongs to Training Video Script. If the question is what a workshop should become on screen, run Live Session to E-Learning Conversion first.

## Inputs
- The storyboard or the course map, with its objectives, and the approved sources for any fact that will appear on a slide
- How the slides are used: presented by a person, read alone, or imported into your authoring tool
- Your house style as written rules you paste: fonts, colours, layout rules, the word limit per slide you work to
If you have none of this, I start from the objectives and one section outline and mark the output as a first draft. I do not start from the expert's deck.

## Approach
The method is cognitive load theory (Sweller, van Merriënboer and Paas, 2019, Educational Psychology Review) applied to slides, with the multimedia principles in plain form: one idea per slide, signal what matters, short segments, and no narration that repeats the words on screen. The judgment is in what comes off the slide. The failure this prevents is the one everybody has sat through: a paragraph on screen, the same paragraph read aloud, and the learner reading ahead of the voice and hearing neither.

## Workflow
1. Ask at most three questions: which storyboard or map this deck follows; how the slides will be used and by whom; what your written house style rules and word limit are. Nothing else is asked later.
2. Write the build sheet before any slide exists, one row per slide: the objective it serves, the one idea, the slide text, the visual and what it shows, the notes or narration, and the slide type (tell, show, ask, practise). A slide with two ideas becomes two rows; a slide with no objective is cut and listed. Keep slide text and spoken text apart: the slide carries a label and a visual; the notes carry the sentences. Where a storyboard row has the same wording in both, the slide loses it.
3. Plan the practice slides in, section by section: a question, a case to decide, a "what would you do" pause, with the answer on the following slide. Count tell slides against ask slides and show the count; you decide whether the balance is acceptable for this audience.
4. Draft the deck in Claude Slides (beta) from the build sheet, following your pasted style rules as far as it can. It works from the rules you wrote, not from your template file, so you finish the look in your own tool.
5. You run the export check and log it, because nobody can do this from inside the conversation: download the PowerPoint, open the file, confirm the text is still editable text, check the notes came through, check images carry alt text, then import one sample section into your authoring tool before building the rest.
6. List every rule, number, name and step that appears on a slide or in the notes for the expert, with its slide. Claude flags and never corrects; a gap reads `[to confirm with the expert]`.

## Output Format
```markdown
# Course Slides Build Sheet
Course: [name] | Built from: [storyboard or map, version] | Use: [presented / read alone / imported] | Date: [date]
## Build sheet
| No. | Objective | The one idea | Slide text | Visual and what it shows | Notes or narration | Type |
|---|---|---|---|---|---|---|
| [n] | [objective] | [idea] | [few words, within the limit you set] | [visual] | [spoken sentences] | [tell / show / ask / practise] |
## Practice slides
| Section | Slide no. | Question or case | Answer slide no. | Objective practised |
|---|---|---|---|---|
| [section] | [n] | [what the learner decides] | [n] | [objective] |

Tell slides: [count] | Ask and practise slides: [count] | Objectives with no practice slide: [list or "none"] | Cut from the slides, and where each item lives now: [list]
## Export check (run by the designer)
| Check | Result | Date | What to fix |
|---|---|---|---|
| File downloaded and opened | [pass / fail] | [date] | [note] |
| Text is still editable text | [pass / fail] | [date] | [note] |
| Notes came through, images have alt text | [pass / fail] | [date] | [note] |
| Sample section imported into your authoring tool | [pass / fail] | [date] | [note] |
## Facts for the expert
| Fact | Slide no. | Source | Status |
|---|---|---|---|
| [fact] | [n] | [source and place] | [confirmed / to confirm with the expert] |
## Decision
[Name, designer] decides by [date] whether the full deck is built from this sheet or the sheet changes first. [Name, expert] confirms the facts by [date]. Export check run by [name] on [date].
```

## Done When
- No slide text repeats its notes word for word
- Every objective has at least one ask or practise slide, or is listed as having none
- The export check is filled in by the designer, including the sample import, and the facts list is with the expert

## Quality Bar
- The deck follows the storyboard. The expert's deck is a source, never the skeleton. Image and media rights: check with a qualified adviser.
- Word limits and slide counts are yours, and visuals explain or they go. Never state that the export keeps editable text or that the deck follows your template file: the designer opens the file and checks.
- Claude drafts the deck; you open the export and check it yourself before it goes near a learner, and the expert confirms the facts.

## Next
Run isd-microlearning-series (Microlearning Series) to plan a short spaced series when a long module should not stay long.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
