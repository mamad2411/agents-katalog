---
name: strat-recommendation-memo
description: Writes a one-page recommendation memo with the call and the ask in the first line, three reasons each tied to evidence a reader can open, every rejected option with its fair case and the one reason it lost, risks with owners, and a one-minute spoken answer to "why not the other option?". Use for "run strat-recommendation-memo", "write the recommendation memo for our strategy choice", "put the call and the ask in the first line", "what are we rejecting and why?", "how do I answer why not the other option?", "decision memo for leadership", "make the call on one page", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Recommendation Memo

## When To Use
The options are scored and stress-tested, and the next meeting will reopen it all unless one page says what to do. You need a call, not another discussion. It answers: what do we recommend, why, what did we turn down, and what exactly do we need from whom?

## When Not To Use
If the options have not been compared yet, use Decision Matrix; it compares and never recommends. If the owner has already decided and you need the reasons kept, use Strategy Decision Record. If you need the whole strategy argued for the leaders who sign it, use Product Strategy Document; this memo is one call on one choice.

## Inputs
- The Strategic Option Set and the Decision Matrix, do nothing included
- The Scenario Model, the Red Team Review and the Pre-Mortem, plus the evidence itself (interview themes, usage data), each with a link or file a reader can open
- The decision owner (a role), the date the decision is due and what you are asking for
If you have none of this, I start from the option you favour and your reasons, flag every reason without evidence and mark the output as a first draft.

## Approach
Bottom line up front, from US Army Regulation 25-50, "Preparing and managing correspondence", 2020 (https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42124-AR_25-50-007-WEB-13.pdf): the main point goes at the beginning. The alternatives and the reasoning stay visible, which is common decision practice with no single originator. The judgment is choosing three reasons a sceptic would accept and being fair to what lost. The failure this prevents: two pages of context ending in "next steps to be discussed", and a rejected option that returns at every meeting because nobody wrote down why it lost.

## Workflow
1. Ask at most three questions: who decides (role) and by when, what exactly you are asking for, and the word limit for the spoken answer.
2. Write the first line: the recommendation and the ask in one sentence. If it needs two, the call is not clear yet; say so and stop there.
3. Pick three reasons, each tied to one piece of evidence with its source. A reason that rests on an assumption alone is dropped or labelled "assumption". Say whether any reason rests on what customers did; if none does, write that in plain words. Do not restate the matrix scores.
4. Rejected options, do nothing included: the strongest case for each, as its best advocate would put it; the one reason it lost; what would make us revisit it. Options are described on their merits, never by who proposed them.
5. Risks from the Red Team Review and the Pre-Mortem: the response and an owner by role, with accepted risks listed as accepted. Then the ask: what, from whom (role), by when, and the review date.
6. The spoken answer to "why not the other option?": plain speech inside your word limit, fair to the option, ending on the reason it lost and the condition that would reopen it. In Claude Docs the draft is one shared document. It works the same in a plain chat.

## Output Format
```markdown
# Recommendation Memo
**We recommend [option] and ask [role] to [approve what] by [date].**
## Why
1. [Reason] | Evidence: [source a reader can open] | Rests on: [what customers did / data / assumption]
2. [Reason] | Evidence: [source] | Rests on: [basis]
3. [Reason] | Evidence: [source] | Rests on: [basis]
## Options we do not recommend
| Option | Strongest case for it | The one reason it lost | What would make us revisit it |
|---|---|---|---|
| Do nothing | [fair case] | [reason] | [observable condition] |
| [option] | [fair case] | [reason] | [observable condition] |
## Risks
| Risk | Response, or accepted | Owner (role) |
|---|---|---|
| [risk] | [response / accepted] | [role] |
## What we need
- [Money, people time or approval] from [role] by [date]
## If asked "why not the other option?"
[Spoken answer within [word limit] words: the fair case, the reason it lost, the revisit condition.]
## Decision
[Decision owner role] approves, amends or rejects the recommendation by [date]; review on [date].
```

## Done When
- The first line holds both the recommendation and the ask
- Each of the three reasons cites evidence a reader can open
- Every rejected option, do nothing included, has a fair case, one reason and a revisit condition
- The ask names a role and a date, and the spoken answer fits the word limit

## Quality Bar
- One recommendation per memo; two calls means two memos
- Revisit conditions are observable, not "if priorities change"
- No invented figures or quotes; contract or regulatory points: check with a qualified adviser
- Claude drafts the call; the owner makes it. Every reason cites evidence a reader can open.

## Next
Run strat-business-case (Business Case) to put the money case behind the recommended option.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
