---
name: strat-product-vision
description: Drafts a Product Vision Board with vision statement options and what each one rules out, a target group described by need, needs marked confirmed or assumed, and the assumed needs to check with customers. Use for "run strat-product-vision", "write our product vision", "vision statement options", "product vision board", "what are we building toward", "every option looks equally reasonable", "a vision that rules something out", "is our vision a slogan", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Product Vision Board

## When To Use
The choices have no destination, so every option looks equally reasonable and nobody can say why one request should lose to another. Use this before you write options, when the product is new, has drifted or has changed hands. It answers one question: what change is this product for, for whom, and what does the business get from it?

## When Not To Use
A vision is the destination. It names no obstacle and no action, and it does not choose between routes. If the destination is agreed and the argument is about how to get there, run Strategic Options. If you need the business logic of one new bet on a page, the Lean Canvas fits better.

## Inputs
- Notes or summaries from customer conversations about who has the problem and what they do about it today
- The product as it is now (or the idea), and the business goals leadership has stated, in their words
- Any vision or mission lines that already exist, including the ones nobody quotes
If you have none of this, I start from a one-line product description and mark the output as a first draft with every need flagged "assumed".

## Approach
I use the Product Vision Board by Roman Pichler, as published on romanpichler.com: a vision statement on top, then four boxes for target group, needs, product and business goals. The statement describes the change for the target group, not the product, and the boxes expose the gaps, because a vision with no target group and no need behind it is a slogan. The failure it prevents is the line on the all-hands slide that suits every product ever made and has never turned down a single request. In Claude Docs the draft is one shared document. It works the same in a plain chat.

## Workflow
1. Ask at most three questions: who the product serves first, which customer conversations or data the needs come from, and how many statement options to compare (default three).
2. Fill the target group box as a group that shares a need, never a demographic profile. Where there are several groups, pick the primary one with the user and park the rest below the board, so the statement is not written for everyone.
3. Fill the needs box in the target group's own words where the notes allow. Any feature that slipped in moves to the product box with the question "which problem does this answer?" A need with no answer to that question in the notes stays visible as a gap.
4. Fill the product box with the few traits that meet those needs, and the business goals box with what the business gets. Keep needs and business goals apart: a goal such as [business goal] is never a customer need.
5. Write the statement options, one sentence each about the change for the target group, each with what it rules out. Test every option twice: could a new joiner repeat it from memory, and does it turn down at least one request the team gets today? An option that fails either test is reworked or dropped.
6. Mark every need "confirmed" with the interview or data behind it, or "assumed". The assumed needs become a list of conversations to have, each with a role and a date.

## Output Format
```markdown
# Product Vision Board
## Vision statement options
| Option | Statement (the change for the target group) | What it rules out | Repeatable from memory |
|---|---|---|---|
| A | [one sentence] | [a request the team gets today that this turns down] | [yes / no] |
## Board
| Target group | Needs | Product | Business goals |
|---|---|---|---|
| [group that shares a need] | [need in their words; confirmed with source, or assumed] | [key traits] | [goal, as stated by leadership] |
## Parked target groups
- [Group]: [why it is not the primary group now]
## Assumed needs to check with customers
| Need | Question to ask | Who asks (role) | By when |
|---|---|---|---|
| [need marked assumed] | [question] | [role] | [date] |
## Decision
[Role of the vision owner] approves one statement and the board by [date]; [role] reports back on the assumed needs by [date].
```

## Done When
- Every statement option is one sentence about a change for the target group, not a feature list
- Each option names one live request it would turn down
- The target group is described by need, not by demographics
- Every need is marked confirmed, with its source, or assumed
- The board names no obstacle and no action

## Quality Bar
- No superlatives in any statement: no "best", "leading" or "world-class"
- No invented customer quotes; a need without evidence carries the word assumed
- Needs and business goals never share a box
- The board fits on one page; cut entries before adding boxes
- Needs come from customers the team has talked to or are marked assumed; a named person approves the statement.

## Next
Run strat-strategic-options (Strategic Options) to write the routes to this destination as options that differ in kind.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
