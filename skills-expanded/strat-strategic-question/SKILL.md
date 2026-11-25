---
name: strat-strategic-question
description: Turns "we need a strategy for X" into a Strategic Question Frame with the one strategic question, the decision it feeds with its owner and date, the horizon, scope in, out and taken as given, and one alternative framing. Use for "run strat-strategic-question", "frame the strategic question", "what decision is this strategy for", "a leader asked for a strategy", "what is the real question here", "who owns this decision", "what is out of scope for the strategy", "give me another way to frame this", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Strategic Question Frame

## When To Use
A leader asks for "a strategy for X" and nobody in the room knows which decision is due. People start collecting slides, and each of them is answering a different question. This skill answers: what single question, once answered, lets a named role decide what, by which date, over which horizon?

## When Not To Use
If the question is already agreed and the team argues about where to look first, run Issue Tree: it splits the question, this skill only agrees it. This is a frame for a strategy diagnosis, so it is the wrong tool for a feature, a prototype test or a discovery sprint; a plain problem statement fits those better.

## Inputs
- The ask in the words it arrived in: the message, the meeting note or the slide.
- What is already decided and must be taken as given, plus any hard limit the owner has stated (date, budget, policy).
- The period the strategy should cover, and your own first view of the answer, even if it is "I do not know".
If you have none of this, I start from the ask alone and mark the output as a first draft.

## Approach
This is a decision frame, the first step in decision-quality practice: a decision can only be as good as the question it was asked to settle. The breadth test comes from the How might we method on designkit.org (https://www.designkit.org/methods/how-might-we.html), which asks for a question that allows a variety of answers and is still narrow enough to know where to start. The failure it prevents: "a strategy for the partner channel" becomes "build a partner portal" in the first meeting, the option hides inside the question, and a month of work answers something nobody owned. It runs in any Claude chat.

## Workflow
1. Ask at most three questions: what will someone decide with the answer and by when, what period should the strategy cover, and what is already decided and off the table?
2. Write the trigger apart from the decision. "Growth slowed" is a fact to look into, not proof of what to do. Keep both lines; most bad frames have merged them.
3. Rewrite the ask as one question that an answer with evidence could settle, with no option hiding inside it. Where a noun names a feature or a market, ask what result it was meant to produce and put that result in the question.
4. Name the decision it feeds: what will be decided, the owner as a role with the authority to decide, the date, and the cost of waiting past it. Then write what a good answer lets that owner decide.
5. State the horizon as the user set it, and sort scope into three lists: in, out, taken as given. If the date cannot hold everything in "in", move one item to "out" and say which.
6. Run the breadth test. If only one answer is possible, the question is too narrow: broaden it. If any project could sit under it, narrow it until you can say where the work starts.
7. Offer one alternative framing and say what it would make the team look at instead. The owner picks; I do not.

## Output Format
```markdown
# Strategic Question Frame
**The question:** [one question, answerable with evidence, no option inside]
**Trigger:** [the fact that started this, with its source or marked as an assumption]
**Horizon:** [period the strategy covers, as set by the owner]
## The decision it feeds
| Decision | Owner (role) | Due | Cost of waiting |
|---|---|---|---|
| [what will be decided] | [role] | [date] | [what slips if late] |
**A good answer lets** [role] decide [the choice].
## Scope
| In | Out | Taken as given |
|---|---|---|
| [item] | [item] | [decision already made, and by which role] |
**Breadth test:** allows a variety of answers [yes / no, what was broadened]; narrow enough to start [yes / no, where the work starts]
## Alternative framing
- [second way to ask it]: the team would look at [evidence, customers or numbers] instead.
## Decision
[Decision owner role] agrees or corrects the question, the horizon and the scope by [date]. No diagnosis work starts before that.
```

## Done When
- There is one question, evidence could settle it, and it names no feature, market or fix as the answer.
- The owner is a role with the authority to decide, with a date and a cost of waiting.
- The horizon is stated and all three scope lists hold at least one item.
- The question passed both halves of the breadth test, and one alternative framing is on the page.

## Quality Bar
- One question; two questions means two frames. The trigger sits apart from the decision and names its source or is marked as an assumption.
- Limits are in the owner's words. An unknown is written "unknown", never filled in.
- The owner is a role with authority to decide, never a judgement of the person in it.
- Claude drafts the frame; the decision owner agrees the question before any work starts.

## Next
Run strat-product-health-read (Product Health Read) to ground the question in the product's real state.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
