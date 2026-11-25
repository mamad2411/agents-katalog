---
name: pdes-design-review-deck
description: Builds a Design Review Deck that puts the decision asked, your recommendation and the date on slide one, then the problem and outcome, the options and what the recommendation gives up, real evidence with gaps shown, the feedback in scope today and next steps with owners, in a short and a working version. Use for "run pdes-design-review-deck", "design review deck", "present my design to stakeholders", "stakeholder review presentation", "slides for design sign-off", "the room argues about colours", "bottom line up front deck", "short version of my design review", part of the Claude for Product Designers Pack by 90n.
---

# Design Review Deck

## When To Use
You present to stakeholders and the room argues about colours instead of the decision. Run it when the options are clear and you need someone to approve, change or reject a direction. It answers one question: what am I asking this room to decide, and which feedback is in scope today?

## When Not To Use
If you want peers to improve work in progress, that is a crit, so use Critique Session Brief. If you have not yet written down why the design is the way it is, write the Design Rationale Doc first; a deck presents that argument and cannot stand in for it.

## Inputs
- The decision you need, the date you need it by, who approves it (by role), who else is in the room and how long the slot is
- The problem, the outcome aimed for, the options you considered and your reasons, as notes or documents
- The research and data you want to show, each with its source, the screens for each option and, if you have them, the objections you already know
If you have none of this, I start from the decision asked and the options and mark the output as a first draft.

## Approach
Bottom line up front, as US Army Regulation 25-50 (para 1-38) sets it out: the main point at the beginning, in the active voice, understood in a single rapid reading. It is paired with the split Nielsen Norman Group draws in its guidance on design critiques (2016): a critique improves the work, a review approves it. The failure this prevents is familiar. Twenty minutes go on the shade of a button because nobody told the room the question was "do we ship the shorter flow?"

## Workflow
1. Ask three questions: what exactly do you need decided and by when, who approves it and who else will be in the room, and how long is the slot?
2. Write slide one first: the decision asked, your recommendation, the date needed. One sentence each, active voice. If you cannot write these three sentences, the deck is not ready and I say so.
3. Problem and outcome on one slide: who has the problem, what it costs them, what success looks like. No design on this slide.
4. Options: two to four, with consequences in words and what the recommended option gives up. No scores, because a score invites a debate about the scoring.
5. Evidence: only what you pasted, each line with its source. A missing number stays `[placeholder]` and a missing study is shown as a gap. Known objections get an answer here, stated as positions held by a role.
6. Risks and open questions, then a "Feedback in scope today" slide: approve, change or reject the direction, and what is out of scope (visual polish, when polish is not the question).
7. Next steps with owners and dates, then two cuts on one storyline: a short version (three to five slides) and a working version with the detail. One message per slide, written as a sentence. You check every evidence line against its source before the deck is shown. Build the outline in any chat, in Claude Slides (download as PowerPoint or PDF), or use Claude Design to put the real options side by side.

## Output Format
```markdown
# Design Review Deck
**Decision asked:** [one sentence] | **Recommendation:** [one sentence] | **Needed by:** [date] | **Approver:** [role] | **Slot:** [length]
## Short version
| # | Slide title (a sentence) | Key message | Content and source |
|---|---|---|---|
| 1 | [The decision we need today] | [decision, recommendation, date] | [your notes] |
| 2 | [Problem and outcome] | [one sentence] | [source] |
| 3 | [Options and what we give up] | [one sentence] | [options, consequences in words] |
| 4 | [What the evidence shows] | [finding, or the gap] | [research or data, source, or [placeholder]] |
| 5 | [Risks, open questions, next steps] | [one sentence] | [owner (role), date] |
## Working version, added slides
| After slide | Added detail | Source |
|---|---|---|
| [#] | [flows, states, data tables, objection answered] | [source] |
## Feedback in scope today
- In scope: [approve, change or reject the direction; named questions]
- Out of scope: [items for crit or a later round]
**Evidence gaps, shown on the evidence slide:** [claim you cannot yet support, what is missing, which role could supply it]
## Decision
[Approver, by role] approves, changes or rejects [the direction] at the review on [date]; [designer] records the outcome by [date].
```

## Done When
- Slide one states the decision, the recommendation and the date, one sentence each
- Every number and finding traces to something you pasted, every gap is visible, and in-scope and out-of-scope feedback are both named
- The short and working versions tell the same story in the same order

## Quality Bar
- Each slide title is a sentence that carries the message, never a topic label
- Stakeholders appear by role, and an objection is a position, never a comment on character
- Accessibility or legal claims are written as questions that end "check with a qualified adviser"
- Claude builds the deck from your real evidence; nothing in it is called tested, accessible or ready to ship unless it was.

## Next
Run pdes-stakeholder-feedback-log (Stakeholder Feedback Log) to capture what the room said.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
