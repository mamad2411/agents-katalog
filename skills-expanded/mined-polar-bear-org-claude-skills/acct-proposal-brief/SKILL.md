---
name: acct-proposal-brief
description: Prepares a proposal brief with the customer's request in their words, who decides and on what criteria, facts each with a source, an assumptions register, the angle of your answer and the questions to ask before writing. Use for "run acct-proposal-brief", "proposal brief", "prepare a proposal", "scope this proposal", "what do I know before I write the proposal", "questions before a proposal", "frame my proposal", part of the Claude for Account Executives Pack by 90n.
---

# Proposal Brief

## When To Use
You are about to write a proposal from one call and your memory of it, and you sense that part of what you will write, the customer never said. Run this before the first page. It answers: what do we really know, where do we know it from, and what is left to ask?

## When Not To Use
For a reorder or a renewal on lines already known, go straight to Sales Quote Check. If the brief exists and you have approved it, run Sales Proposal.

## Inputs
- Your call notes, the customer's emails, and their written request or requirements if there are any.
- What you know about the decision: who decides, on which criteria, by when.
- Who owns the proposal on your side and the real date you will send it.
If you have none of this, I start from the customer's request in one sentence, as you remember it, and mark the output as a first draft.

## Approach
A proposal brief separates three things that always get mixed: what the customer asked for, what you know with its source, and what you assume. It is common proposal practice, described generically. A sentence you cannot tie to a meeting or an email ends up in the proposal as a fact, and the customer reads it thinking "we never said that". The assumptions register stops that slide and tells you when to call the customer before you write.

## Workflow
1. I ask at most three questions: how the request reached you and who spoke to the customer, who owns the proposal on your side, and the date you will really send it.
2. I write the request in one sentence, in the customer's words where your notes hold them, and separately the format expected: document, deck or quote only.
3. I fill the decision table: who decides (by role), the criteria they announced, the decision date. Whatever is missing reads "unknown, to ask", never guessed.
4. I list the facts, each with its source: "call of [date]", "email of [date]", "requirements, section [x]". A fact with no source drops into the assumptions.
5. Each assumption is written as [ASSUMPTION: what you believe, why, how to verify it]. The supposed budget, the reason for the request and the competitor in place go here, never among the facts. If assumptions outnumber facts I say so at the top of the brief.
6. I draft the questions to put to the customer before writing, in the order you would ask them.
7. I propose the angle of your answer in one sentence: what you believe about the customer's problem that a competitor would not say. You confirm it or rewrite it.

## Output Format
```markdown
# Proposal Brief
**Customer:** [name] · **Owner:** [name] · **Send date:** [date] · **Status:** [first draft / approved]
## The request
[One sentence, in the customer's words] · Format expected: [document / deck / quote only]
## Who decides
| Role | Announced criteria | Decision date | Source |
|---|---|---|---|
| [signs / buys / evaluates] | [criterion or "unknown, to ask"] | [date] | [source] |
## Known facts
| Fact | Source | Source date |
|---|---|---|
| [fact] | [call, email, document] | [date] |
## Assumptions to verify
- [ASSUMPTION: what you believe, why, how to verify it]
## Questions before writing
1. [question]
## Angle of the answer
[One sentence, confirmed or rewritten by you]
## Decision
[Name] decides on [date] whether to write now or call the customer first.
```

## Done When
- Every fact has a dated source; no unsourced fact is left in the table.
- Every empty decision cell reads "unknown, to ask".
- Any imbalance between facts and assumptions is flagged at the top, and the angle is confirmed or rewritten by you.

## Quality Bar
- The customer's words stay theirs; a rewording is marked as one.
- No estimate of the customer's budget: it sits in the assumptions with the question that tests it.
- Evaluators appear by role, criteria and dates, never by character.
- No assumption becomes a fact: each fact has its source, and nothing is invented to fill a gap.

## Next
Run acct-sales-proposal (Sales Proposal) to write the document from this brief.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
