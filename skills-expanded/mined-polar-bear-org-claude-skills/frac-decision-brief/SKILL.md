---
name: frac-decision-brief
description: Frames a decision for a client's leadership team, with the question rewritten around an outcome, why now, the owner and who approves, what is fixed and out of scope, three to five real options including the current course and stopping, the strongest case for and against each, the unknowns and what would change the choice. Use for "run frac-decision-brief", "frame this decision for the leadership team", "write a decision brief", "decision memo for the CEO", "we keep discussing the same question", "lay out the options", "what are we actually deciding", part of the Claude for Fractional Leaders Pack by 90n.
---

# Decision Brief

## When To Use
The leadership team has discussed the same question three times and nobody has framed it. Each meeting reopens it from a different end, the person with the strongest view speaks first, and the minutes say "to be continued". As the part-time member of the team, you are often the one with the distance to write it down. This answers: what exactly is being decided, by whom, among which options?

## When Not To Use
If the question is whether the company needs your seat or a full-time hire, run Fractional or Full-Time Brief. If the choice is already made and needs writing down, run Decision Record.

## Inputs
- The question as people currently put it, and what triggered it
- Who owns the decision, who must approve, and the date it is needed by
- The options already on the table, in their supporters' words, and your own first view
If you have none of this, I start from the question in your words, mark the owner and the options as unconfirmed and mark the brief as a first draft.

## Approach
Decision framing with real alternatives, from decision analysis, described generically: separate the trigger from the decision, state the choice around an outcome, name the owner, and compare options that truly differ. The judgment is to write each option as its strongest supporter would, including the current course and stopping. The failure this prevents is the brief that smuggles in its author's answer, with one real option and two shown only to lose.

## Workflow
1. Ask at most three questions: how is the question put today, and what set it off; who owns it and by when; what is your own first view? I record your view as yours and do not polish it into the frame.
2. Separate the trigger from the decision. A lost customer is a fact to look into; it is not proof that a product line must close.
3. Rewrite the question around an outcome and a real choice. State why now and what waiting costs. List what is already fixed and what is outside this decision.
4. Name the owner, who approves and who is consulted. If authority is unclear, the first output is that question to the CEO, before any option.
5. Set out three to five options that differ in what happens: include the current course and stopping, and a small reversible trial where one is possible. For each: what changes in practice, what it needs, and the strongest case for and against. Mark which steps can be undone.
6. List the unknowns with who could resolve each, then write what would change the choice. Add no recommendation unless the owner asked you for one, and then label it as yours. Draft in Claude Docs or as text.

## Output Format
```markdown
# Decision Brief
Client: [name] · Prepared for: [owner] · Date: [date] · Decide by: [date]
## The question
[Rewritten around an outcome] · Why now: [trigger, cost of waiting]
Owner: [role] · Approves: [role] · Consulted: [roles] · Fixed: [..] · Out of scope: [..]
## Options
| Option | What changes in practice | Needs | Strongest case for | Strongest case against | Can it be undone? |
|---|---|---|---|---|---|
| Current course | [..] | [..] | [..] | [..] | [..] |
| Stop | [..] | [..] | [..] | [..] | [..] |
| [Option] | [..] | [..] | [..] | [..] | [..] |
## Unknowns
| Unknown | Who could resolve it | By when |
|---|---|---|
| [unknown] | [role] | [date] |
## What would change the choice
- [Option] is right if [fact]
## Decision
[Owner] chooses by [date], or names the unknown to resolve first; [approver] confirms.
```

## Done When
- The question names an outcome and does not contain its own answer
- The owner and the approver are named, or the authority question is asked first
- The current course and stopping appear among three to five real options
- Every option has a case against as strong as its case for

## Quality Bar
- No option is drawn weak; a supporter of each would accept its description
- Facts, estimates and views are labelled as such
- No weighted score stands in for the owner's judgment
- Legal, regulatory or employment sides of an option: check with a qualified adviser
- Claude frames from what you give it about this client, invents no fact or figure, and the owner decides in the room, not on this page

## Next
Run frac-decision-record (Decision Record) to write the choice down the day it is made.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
