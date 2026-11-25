---
name: fac-participant-handout
description: Builds the handout participants write in and take away, producing guided notes with gaps for their own cases, a worksheet per activity carrying the session's real question, the look-up content cut from the slides and a reserved action plan page in an accessible layout. Use for "run fac-participant-handout", "participant handout", "training handout", "participant workbook", "workshop worksheet", "guided notes", "my handout is just the slides printed", "accessible handout", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Participant Handout

## When To Use
The handout is the slides printed six to a page. Use this when the plan and the slide outline are agreed and people need something to work in during the session and find things in afterwards. It answers: what do participants write, what do they look up later, and what should not be on the page at all?

## When Not To Use
What is shown on screen belongs in the Training Slide Outline. The action plan page itself is written by If-Then Action Plan; this handout only reserves its place. Role cards and observer notes for practising a conversation come from the Role-Play Practice Kit.

## Inputs
- The session plan with its blocks, and each activity with the real question the group will work on.
- The look-up content moved off the slides with your source material for it, and whether people use print or screen, with any access needs they sent you.
If you have none of this, I start from the objectives and the list of activities, and mark the output as a first draft.

## Approach
The layout follows the W3C Web Accessibility Initiative's guidance on accessible presentations: detail moves off the slide into a handout with real headings, readable type and an adaptable format. What goes on each page follows cognitive load theory (Sweller, van Merriënboer and Paas, 2019): working memory is limited, so what does not serve the task competes with what does. The failure it prevents: a thick booklet people leaf through during the practice, in which the only thing they write is the date.

## Workflow
1. Ask at most three questions: what are the activities and the real question in each, which content came off the slides for looking up later, and will people use this on paper or on a screen?
2. Write the guided notes: the few key points per block, each followed by a gap people fill with their own case. A gap that asks them to copy a word from the slide is cut; the gap is for their work, not your sentence.
3. Build one worksheet per activity carrying this session's real question and criteria, never a generic template. Each states the task, the time and what to bring back, in the same words as the activity slide.
4. Lay out the look-up content so it is found fast on the job: headings phrased as the question someone will have, steps and tables in place of paragraphs.
5. Reserve one page for the action plan and leave it empty, then tag every page to its plan block. A page that serves no block comes out.
6. Apply the accessible layout: real headings, large simple type, strong contrast, an adaptable format as well as PDF, sent ahead to those who asked. Where your material has a gap, I mark the gap and invent nothing. It can be made as a document in Claude Docs (beta) or as a file created in the chat.
7. Hand over one worksheet for the check you run before printing: fill it in as a participant would, then judge whether it made you do the thing or copy the slide.

## Output Format
```markdown
# Participant Handout
Session: [title] | Pages: [number] | Used on: [paper or screen] | Also available as: [adaptable format]
## Guided notes: [block name] (page [n], built from [your source])
Key point: [the point in one line] | In my work, this shows up when: ____________
## Worksheet: [activity name] (page [n], plan block [block])
Task: [this session's real question] | Time: [minutes] | Bring back: [output]
| [Criterion or prompt from this session] | My case |
|---|---|
| [criterion] | ____________ |
## Look-up: [the question someone will have on the job] (page [n], plan block [block])
| When you need to | Do this | Where to find more |
|---|---|---|
| [situation] | [step] | [your source] |
## My action plan (page [n], the closing block)
[Reserved page, filled in during the close]
## Open questions
- [gap in the source material, marked and not filled]
## Checks
- [ ] [Trainer] filled in one worksheet as a participant: did it make me do the thing, or copy the slide?
## Decision
[Trainer] approves the handout for printing or sending by [date]; [trainer or coordinator] sends it ahead to those who asked by [date].
```

## Done When
- The four parts are present in order: guided notes, worksheets, look-up content, the action plan page.
- Every page is tagged to a plan block, and every worksheet matches its activity slide.
- Every line traces to your material, and gaps are marked as gaps.
- The trainer has filled in one worksheet and answered the check.

## Quality Bar
- Only what serves the task is on the page; the rest is cut or moved to look-up.
- Worksheets carry this session's question and criteria, in the group's own working language.
- Access needs are asked for, not assumed; the layout guidance is a starting point, not a test.
- What participants write stays with them; the handout is never collected as a record.

## Next
Run fac-session-openers (Icebreakers and Session Openers) to plan how the session starts.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).