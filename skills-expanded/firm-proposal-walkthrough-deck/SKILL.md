---
name: firm-proposal-walkthrough-deck
description: Plans a proposal walk-through deck of six to ten slides, with the client's problem first, a full-sentence headline per slide, options side by side on the same rows, the decision you need and by when, speaker notes with the question to ask and where to stop and listen, and a read version if it will be forwarded. Use for "run firm-proposal-walkthrough-deck", "turn my proposal into slides", "walk the client through the proposal", "deck for the proposal meeting", "speaker notes for my pitch", "slides they can forward afterwards", "build the proposal presentation", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Proposal Walk-Through Deck

## When To Use
The last proposal you emailed got "thanks, we will review" and then nothing. This time you have half an hour on the calendar to go through it together. Run this to decide what each slide says, in what order, and what you ask at each point, so that the meeting closes with a choice or a date for one.

## When Not To Use
If the proposal itself is unsettled, run Proposal Red Team Review first; slides only make a muddled case go faster. If the signer will read one page and never join a meeting, write the Proposal Executive Summary.

## Inputs
- The final proposal, the options with your prices, and the client's own figures from your notes
- Who will be in the meeting, and whether the deck will be passed on afterwards
- How you will build it: Claude Slides (PowerPoint or PDF download), or Claude for PowerPoint on your own template
If you have none of this beyond the proposal, I start from the proposal alone and mark the plan as a first draft.

## Approach
Show the outcome before the method, a habit borrowed from good product demonstrations and described generically: the client meets their problem and their result before any credentials. A deck that will be forwarded is a different object, which Duarte calls a Slidedoc: fuller text, readable with nobody presenting. Turning a finished proposal into a tight slide order is quick work for AI. The talking, the pauses and the listening are yours. The failure it prevents is the options appearing on the last slide with four minutes left.

## Workflow
1. Ask, in one go: presented live, read cold, or both? How many slides, between six and ten? How long is the meeting?
2. Set the order. Their problem and what it costs, in their figures. The outcome they would have. The route there, on one slide. The options side by side. The decision you need and the date. Your background last, and brief. Whatever does not serve the decision moves to an appendix or goes.
3. Write each headline as a full sentence that carries the point ("Rework is costing your team [their figure] a month", not "Background"). Figures come from the client's numbers or your proposal; a missing one stays in [brackets].
4. Build the options slide with one column per option and identical rows: included, left out, timing, price as you set it. Like sits next to like.
5. Write speaker notes per slide: two or three sentences to say, one question to ask, and where to stop and listen. On the options slide the note is to ask which fits before defending any of them.
6. If it will be forwarded, write the read version: same order, fuller text, no line that depends on "as I said". Then I hand you the plan to build in Claude Slides or in Claude for PowerPoint on your template, and you check every figure before anyone sees it.

## Output Format
```markdown
# Walk-Through Deck Plan
Client: [name] · Meeting: [date, length] · Use: [live / read / both] · Slides: [count]
## Slides
| # | Headline (full sentence) | On the slide | Figures from |
|---|---|---|---|
| 1 | [their problem and what it costs] | [two or three points] | [call record, date] |
| [n] | [the decision you need, and by when] | [the decision, the date] | [proposal] |
## Speaker notes
| # | Say | Ask | Stop and listen |
|---|---|---|---|
| 1 | [two or three sentences] | [question] | [yes / after the question] |
## Read version
- Slide [n]: [text added so it stands alone]
## Decision
[You] settle the slide count and the option to lead with by [date]; [client decider role] is asked in the meeting on [date] to choose an option or name the day they will.
```

## Done When
- The client's problem is on slide one or two, and your background comes last
- Every slide has a full-sentence headline, notes, a question and a source for its figures
- The final slide states the decision and a date
- A read version exists if the deck will be passed on

## Quality Bar
- Six to ten slides unless you say otherwise, one message each
- Options sit on identical rows, and none was added to steer the choice
- The notes include pauses; a walk-through that never stops to listen is an email read aloud
- No rival is named or compared on any slide
- Their problem first and their figures only; I invent no number for a slide, and you present it and send it yourself.

## Next
Run firm-executive-summary (Proposal Executive Summary) to write the page for the signer who was not in the room.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
