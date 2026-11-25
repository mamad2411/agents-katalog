---
name: build-prototype-spec
description: Writes the spec for one prototype, answer first, with problem and evidence, non-goals, numbered requirements that each carry one behaviour and a Given-When-Then check, open questions with an owner and a date, and a dated export kept as the record. Use for "run build-prototype-spec", "write the spec for my prototype", "put what we agreed in writing", "number the requirements", "write a pass or fail check for each requirement", "list the non-goals", "turn my flow into requirements", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Spec

## When To Use
The prototype will be judged against "what we agreed" and nothing was agreed in writing. Use it once the screens and their connections are listed and before the build starts. It answers: what must this prototype do, how will anyone check each thing, and what is deliberately left out?

## When Not To Use
If you are still deciding how real it must be or which surface to build on, run Prototype Brief. If the build is finished and you need to record what was actually made, run Engineering Handover Note. This spec is the agreement before the build, for one prototype, not a plan for what ships.

## Inputs
- The belief and pass line from your test card, and your screen-by-screen flow
- Evidence for the problem, as links: interview themes, support themes, usage answers
- What is already decided as out, and who has to agree the spec (by role)
If you have none of this, I start from the problem in one sentence and mark the output as a first draft, with every missing piece of evidence listed as an open question.

## Approach
A problem-first spec with testable requirements is a common practitioner convention. Each check takes the three-part shape from the Cucumber Gherkin reference (https://cucumber.io/docs/gherkin/reference/): Given a starting state, When one action, Then a visible outcome. Kept to what one test needs, it turns "it should be simple" into something two people can look at and agree on. The failure it prevents: a review where the builder says "that was never in scope" and the reviewer says "I assumed it was", with no page to settle it.

## Workflow
1. I ask at most three questions: which belief does this prototype test, who has to agree the spec, and which evidence can I link?
2. Write the answer-first paragraph: what the prototype is, for whom, which belief it tests and how we will know. If a feature is hiding in the problem statement, I pull it out and restate the need.
3. Problem and evidence, each claim with its link. A claim with no source becomes an open question. Customer needs appear as themes, never as a description of a named customer.
4. Non-goals: what a reasonable reader would assume is in. Most arguments at review time start here, so I write the ones that feel too obvious to say.
5. Requirements, numbered R1, R2 and on, one behaviour per row; "and" means two rows. Each gets a check: Given a known starting state, When one action happens, Then an outcome a person can see from outside. Vague words (fast, simple, clear) get a visible definition or move to open questions. The same ids carry into the prototype, the handover and the review, so they are never renumbered.
6. Open questions, each with an owner role and a date. Then a cut pass: this is a throwaway prototype, not a test suite, so any requirement the belief does not need comes out.
7. Fix the record. In Claude Docs you ask for the doc in the conversation, select text to comment, mention @Claude in a comment for an edit, and share with viewers or editors. There is no comment-only role, and on Team and Enterprise plans a doc cannot be shared outside the organisation. Export to Word, PDF, Markdown or Google Docs and keep a dated export as the agreed version. In any other chat, save a dated copy.

## Output Format
```markdown
# Prototype Spec
Prototype: [name] | Belief tested: [one line] | Agreed by: [role] | Dated export: [link, date]
## Summary
[What the prototype is, for whom, which belief it tests and how we will know, in one paragraph.]
## Problem and evidence
- [Problem in the user's terms, no feature inside] | Source: [link]
## Non-goals
- [Thing a reader would assume is in and is not]
## Requirements
| ID | Requirement (one behaviour) | Screen | Given | When | Then (visible from outside) |
|---|---|---|---| R1 | [behaviour] | [S1] | [starting state] | [one action] | [outcome a person can see] |
|---|---|
## Open questions
| Question | Owner (role) | Answer by |
|---|---|---|
| [question] | [role] | [date] |
## Decision
[Role who owns the test] and [engineering or design reviewer, by role] agree this version by [date]; any later change is a new dated export, not an edit to this one.
```

## Done When
- The first paragraph says what it is, for whom, which belief and how we will know
- Every requirement holds one behaviour and a check a person could mark pass or fail by looking
- Every evidence claim has a link or sits in open questions, and every open question has an owner role and a date
- A dated export exists and its link is in the header

## Quality Bar
- One behaviour per row, a Then that can be seen on screen, and every vague word defined in the row or moved to open questions.
- Requirement ids stay fixed once agreed; a dropped requirement keeps its number and is marked removed.
- No invented baselines, quotes or findings; how real it is and which surface it uses stay in the brief.
- I draft; the people named in the Decision read it together before it counts as agreed.
- This is a spec for a prototype: it says what to build to learn, and a named role agrees it; it is not a commitment to ship.

## Next
Run build-product-context-file (Product Context File) so Claude uses the product's own words in the build.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
