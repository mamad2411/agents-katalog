---
name: pmjob-work-walkthrough
description: Builds a Work Walkthrough Outline for a portfolio review or a project deep dive with a timed plan for two or three pieces of work, each told through stakes, your role, three decisions and the mistake, plus a slide outline, the likely questions and a check on what you may show. Use for "run pmjob-work-walkthrough", "portfolio review prep", "project walkthrough for a product interview", "present a project I led", "my portfolio only shows screens", "20 minute presentation of my work", "case study deck for an interview", "what am I allowed to show", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Portfolio and Project Walkthrough

## When To Use
You stopped designing every screen or writing every spec, and your walkthrough still shows screens and timelines. The hardest part of the work was a trade-off between three teams, and none of it is on a slide. It answers: in the minutes I am given, how do I show what I decided, what it cost and what changed?

## When Not To Use
For two minute answers to "tell me about a time when", use Interview Story Bank. For one small task that shows how you work with AI, use AI Work Sample. For a critique of someone else's live product, use App Critique.

## Inputs
- The slot as the recruiter gave it: minutes, format, who is in the room, whether slides are expected
- Two or three pieces of work with what you still hold: evidence rows, decision notes, review decks, launch notes, real outcome data
- What you may show outside a former employer, and what you are unsure about
If you have none of this, I start from your own account of one piece of work and mark the output as a first draft.

## Approach
A decisions-first case study, using the case contents NN/g describes in "5 Steps to Creating a UX-Design Portfolio" (the problem, your role, constraints, iterations, results, lessons) and the What, So what, Now what model from the University of Hull Library guide to reflective writing for the lesson. The judgment: a panel hiring an experienced person wants to hear how you think when the answer is not obvious, so screens appear only where one proves a decision. The failure it prevents is scrolling an existing file for the whole slot and reaching the outcome as the time runs out.

## Workflow
1. Ask at most three questions: the slot and format as the recruiter gave them, which two or three pieces of work you led and want to show, and what you are allowed to show.
2. Time first. You set the minutes per piece and keep room for questions. Public employer interview guides show the range: a 20 minute presentation of the most impactful product you led, a 45 minute portfolio review of the last three to four years, or a 10 minute case study with 10 minutes of questions. Your recruiter's word outranks all of them.
3. Per piece, open with the problem and the stakes in two or three sentences, then your role: how you collaborated and who decided what. Guides ask for a project you led, not only contributed to, and for your individual contribution stated clearly.
4. Three decisions per piece, each with the options you had and the trade-off you chose, including one concept or path not pursued. Then the mistake and what you did next. A talk with no setback gets taken apart in two questions.
5. The effect on users and the business from real data, `[placeholder]` where a number is missing, and what else moved the result. Then the lesson: What happened, So what it changed in how you work, Now what you do differently. One concrete change, not "communicate better".
6. Slide outline: one idea per slide, one slide per decision at most, a screen only where it proves that decision. Claude Slides or Claude Design can lay out the deck from the outline; the outline itself works in any chat.
7. Likely questions per piece (why that option, what was your part, how did you measure it, what would you do differently), then the "may I show this" check: each item cleared, unknown or not shareable, with the question to ask a former employer. Confidentiality and contract points: check with a qualified adviser.

## Output Format
```markdown
# Work Walkthrough Outline
**Round:** [portfolio review / project deep dive] · **Room:** [roles] · **Date:** [date]
**Time plan:** slot [minutes] = opening [minutes] + piece 1 [minutes] + piece 2 [minutes] + close [minutes] + questions [minutes kept]
## Piece [n]: [name, generalised if confidential]
**Problem and stakes:** [two or three sentences] · **My role and who decided what:** [your part; others by role; who made the final call]
| Decision | Options I had | Trade-off I chose | Path not pursued | Proof (screen, doc or none) |
|---|---|---|---|---|
| [decision] | [options] | [what it cost and why] | [option] | [reference] |
**The mistake:** [what happened and what I did next] · **Outcome:** [what changed for users and the business] · **Data:** [number or placeholder] · **Source:** [source] · **What else moved it:** [other factors]
**Lesson:** What [..] · So what [..] · Now what [..]
**Likely questions:** [question]: [my answer in one line] · [question]: [my answer in one line]
## Slide outline
| Slide | One idea | What is on it |
|---|---|---|
| [n] | [idea] | [text / chart / screen that proves a decision] |
## May I show this
| Item | Status (cleared / unknown / not shareable) | Question to ask, and whom |
|---|---|---|
| [slide, screen, figure or name] | [status] | [question for a former employer] |
## Decision
You decide which pieces go in and what stays off the slides, once every "unknown" above has an answer, by [date].
```

## Done When
- The minutes add up to the slot, with time for questions kept.
- Every decision has options and a trade-off, every piece has its mistake, and every outcome cites a source or stays a placeholder.
- Every item you plan to show has a status, and no "unknown" is left without a question and a person to ask.

## Quality Bar
- It is a talk built for this room, said aloud once against the clock before the day.
- "I" for your part, the team by role for theirs; no colleague is judged. No client or employer material is shown without clearance, and people are named only with their yes.
- The lesson names one real change in how you work, not a modest boast.
- Only what happened and what your data shows: missing numbers stay as placeholders, and you give the talk yourself.

## Next
Run pmjob-questions-to-ask (Questions to Ask) to prepare your side of the conversation.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
