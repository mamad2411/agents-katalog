---
name: pdes-design-options-tradeoffs
description: Builds a Design Options Trade-off Table with two to four options that differ in structure, flow or scope, criteria taken from your principles and brief, consequences in words with no made-up score, and what each option gives up. Use for "run pdes-design-options-tradeoffs", "show the options not just one design", "stakeholders think there is only one way", "compare design directions", "trade-off table for the review", "design space analysis", "why not option B", "what does each option cost", part of the Claude for Product Designers Pack by 90n.
---

# Design Options Trade-off Table

## When To Use
Stakeholders saw one design and think it is the only one, so every comment is a tweak. Run it before the review, while you can still show the room the real choice and what each path costs. It answers: what are the different ways to solve this, and what does each one give up?

## When Not To Use
If the choice is made and you need to record why, use Design Rationale Doc. If the problem itself is not agreed, use Problem Framing Brief first. For a small choice that is cheap to reverse, decide and move on; this table is for choices people will question.

## Inputs
- The design question, the brief behind it and who decides, by role, if you know
- Your options as they stand, in your words, with screens or links
- Your design principles, and any research or data you have, with personal data removed
If you have none of this, I start from the design question and your current design and mark the output as a first draft.

## Approach
Questions, Options and Criteria, the design space analysis of MacLean, Young, Bellotti and Moran (1991), as described on the originating lab's page (NAVER LABS Europe, Design Space Analysis): write the key issue as a Question, list the Options that answer it, and record the Criteria that argue for or against each. Consequences go in words, because a total of invented points hides the argument it claims to settle. The failure it prevents: three colourways of one layout presented as "options", which tells the room the decision was made without them. Optionally, Claude Design can put the real options side by side on a canvas beside the chat.

## Workflow
1. Ask three questions: what is the design question, which options do you already have (I keep your wording), and which requirements from the brief can no option break?
2. Write the Question as a question about the design issue, not a fix ("How does a returning user find a past order?" is an example). If it hides two questions, split it and run one table each.
3. Set the Options: yours first, then only ones that differ in structure, flow or scope. Include "keep the current design" where one exists, because doing nothing has consequences too. Two to four in total. If an option raises a follow-up Question, note it instead of burying it.
4. Set the Criteria from your principles and the brief. Separate requirements (failing one rules an option out) from preferences, and check that two criteria do not count the same benefit twice.
5. Fill each cell with a link and its consequence in words: + where the criterion argues for the option, - where it argues against. No numbers, no weights, no totals. Each cell cites research, data or a principle, or shows `[gap]`.
6. Write one line per option on what it gives up. Call an option dominated only where the evidence shows it has no advantage on any criterion.
7. List the gaps worth closing before the review and who can close them. Add a recommendation only if you want one, labelled as yours.

## Output Format
```markdown
# Design Options Trade-off Table
**Question:** [the design question] | **Prepared by:** [role] | **Decides:** [role] | **Decision due:** [date]
## Options
| Option | What it is | What it gives up |
|---|---|---|
| A. Keep the current design | [description] | [one line] |
| B. [name] | [description] | [one line] |
## Consequences
| Criterion | Requirement or preference | A | B | C | Evidence |
|---|---|---|---|---|---|
| [criterion from a principle or the brief] | [which] | [+ or - with the consequence in words] | [+ or -] | [+ or -] | [source or gap] |
## Gaps to close before the review
| What is unknown, or a follow-up question an option raises | Who can find out (role) | By when |
|---|---|---|
| [gap or question] | [role] | [date] |
## Designer's recommendation (optional)
[Option and reason, labelled as the designer's own view]
## Decision
[Role who owns the decision] chooses an option by [date]; [designer] records the choice and the reasons the same week.
```

## Done When
- Two to four options that differ in structure, flow or scope, including the current design if there is one
- Every cell has a + or - with a consequence in words and a source or a visible gap
- Requirements and preferences are told apart, and each option states what it gives up

## Quality Bar
- Your options appear in your wording before any added option
- No scores, weights or totals, even if asked to "just rank them"; the reasoning stays visible
- An option nobody has put in front of users says so; the table never implies it was tested
- Claude lays out the options and never picks one; the person who owns the decision chooses.

## Next
Run pdes-design-rationale-doc (Design Rationale Doc) to record the choice and why, once it is made.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
