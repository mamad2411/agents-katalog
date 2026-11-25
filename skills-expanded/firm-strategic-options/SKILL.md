---
name: firm-strategic-options
description: Lays out three to five truly different ways the client could solve the problem, keeping the client's own options in their words and adding new routes per objective, the current course, stopping, a bounded pilot and doing it in house with their own AI, with what each needs, the strongest reason for and against, and what was excluded and why. Use for "run firm-strategic-options", "what are the client's real options", "they only see two options", "generate alternatives for this decision", "is my recommendation the only option", "options including doing nothing", "could they do this in house with AI", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Strategic Options

## When To Use
The client has framed it as "restructure or carry on", and neither appeals. Or you notice that every route you can think of ends with them hiring you. Run this when the problem is stated and tested, to put a handful of different ways forward on the table, written as fairly as you would want a rival's option written.

## When Not To Use
This lists ways to solve the client's problem. For ways to buy your work, with scope and prices, use Good-Better-Best Options. To compare the options once they exist, use Trade-Off Table.

## Inputs
- The problem statement with its decision frame
- The options the client has already mentioned, in their words
- What the client is trying to achieve, and the hard limits they named
If you have none of this, I start from the decision question and your own first two options, and mark the list as a first draft.

## Approach
Generating alternatives is a named step in structured decision making, whose sequence (problem, objectives, alternatives, consequences, trade-offs) is described on public agency pages such as the US Geological Survey's. The rule is to build options from the objectives, one at a time, before judging any of them. The failure it prevents is the false choice: three versions of your favourite, plus one option so weak it exists only to lose. Doing nothing and doing it themselves with their own AI are real routes and get the same care.

## Workflow
1. Ask, in one go: which options has the client already named? What are they trying to achieve, in their words? Which limits are truly fixed, and who said so?
2. Write the client's own options first, in their wording, each linked to the objective behind it. Do not improve or merge them yet.
3. For each objective separately, generate routes by changing one lever at a time: scope, timing, partner, process, sequence. Five cosmetic variants of one idea count as one.
4. Add the four standing options where they are feasible: the current course, stopping, a bounded pilot, and doing it in house with their own AI and people. Describe each with its real cost and consequence; staying put is never free, and the in-house route gets its strengths stated first.
5. Combine compatible ideas, separate choices that exclude each other from those that can run together, and filter against the fixed limits using evidence. Mark feasibility "unverified" where it is. An option is never dropped because a senior person is known to dislike it.
6. Keep three to five that truly differ. For each write what changes in practice, what it needs, who is affected, and the strongest reason for and against. List what was excluded and why, so the client can put it back.

## Output Format
```markdown
# Options for the Client's Problem
Decision: [question from the problem statement] · Decides: [role] · Date: [date]
## Objectives (theirs)
- [Objective, in their words]
## Options
| Option | What changes in practice | Needs (people, money, time) | Feasibility (evidence) | Strongest reason for | Strongest reason against |
|---|---|---|---|---|---|
| Current course | [description] | [needs] | [known / unverified] | [reason] | [reason] |
| In house with their own AI | [description] | [needs] | [known / unverified] | [reason] | [reason] |
| [Client's option, their words] | [description] | [needs] | [status] | [reason] | [reason] |
| [New route] | [description] | [needs] | [status] | [reason] | [reason] |
## Can run together / exclude each other
- [Option] with [option]: [together / one or the other]
## Excluded, and why
- [Option]: [limit it broke, and who set the limit]
## Decision
[You] decide by [date] which options go forward for comparison; [client decider role] may restore any excluded option or challenge a limit.
```

## Done When
- The client's own options appear in their wording
- The current course and the in-house route are written as carefully as the others
- Three to five options remain, and no two differ only in size
- Every exclusion names the limit and who set it

## Quality Bar
- Each option has a strongest reason against, including the one you favour
- No figure for cost or benefit appears unless the client or you supplied it
- No prices for your own work on this page; that belongs to the pricing desk
- An option's weakness is never exaggerated to flatter another
- I lay the options out from your facts and the client's words and invent no feasibility; which ones go forward, and which you recommend, is your judgment.

## Next
Run firm-trade-off-table (Trade-Off Table) to compare the surviving options on the client's own criteria.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
