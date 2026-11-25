---
name: pdes-design-principles
description: Writes Design Principles for your product area with four to seven stands, what each one gives up, a "this, not that" pair from your own screens and a conflict check that says which principle wins where. Use for "run pdes-design-principles", "write design principles for my product", "every review is a taste argument", "our principles are platitudes", "sharpen our design principles", "this not that examples", "what does this product choose", "criteria for critique", part of the Claude for Product Designers Pack by 90n.
---

# Design Principles

## When To Use
Every review turns into a taste argument because nothing written says what this product chooses, so the most senior preference wins by default. Run it when people agree on the goal and still fight about how the product should behave. It answers: which stands does this product take, and what does each one give up?

## When Not To Use
If you need the stage-by-stage checklist that work is checked against, use Design Quality Bar; principles feed it and do not replace it. If nobody has agreed what problem the work solves, principles will not settle it: start with Problem Framing Brief.

## Inputs
- The product area, its users and its purpose, in a few lines
- Three to six decisions the team argued about, with the screens or notes you can paste
- Any principles that already exist, and research on what users need here, with personal data removed
If you have none of this, I start from the product's purpose and two contested decisions and mark the output as a first draft.

## Approach
Product-specific design principles as Nielsen Norman Group sets them out (Rosala, 2020, nngroup.com/articles/design-principles): identify the core values, say how each affects users, name the recurring trade-offs and who wins them, then write, compare and iterate with others. The GOV.UK Government Design Principles serve as an example of format only: a short imperative line plus a short explanation. The judgment is that a principle nobody could disagree with decides nothing. "Simple and delightful" is the failure this prevents: a line on a wall that never once settled a review.

## Workflow
1. Ask three questions: which decisions keep being argued again, where will the principles be used (critique, reviews, rationale), and who owns design direction for this area?
2. If principles already exist, test and sharpen those instead of writing new ones. Otherwise mine the contested decisions: for each, name the two good things that were in tension. Describe the decision, never who argued which side. A value with no tension behind it is dropped.
3. For each value, write how it affects users and what happens without it, in one sentence, from the research you pasted. Where there is none, write `[evidence gap]` instead of a user need that sounds right.
4. Draft each principle as a stand: "[value] even when it costs [what we give up]", and say which user group or goal wins the trade-off. Run the opposite test: if the opposite is absurd, it is a platitude, so cut it or sharpen it.
5. Keep four to seven; the NN/g page warns that ten or more get forgotten. Merge overlaps and drop the weakest.
6. Add one "this, not that" pair per principle from your real screens: one that follows it, one that breaks it. A missing pair stays `[example needed]`.
7. Run the conflict check in pairs: which principle wins, in which context. Then turn each principle into a critique objective and a criterion for comparing options, and draft the note that asks the team to react; you send it.

## Output Format
```markdown
# Design Principles
**Product area:** [name] | **Drafted by:** [role] | **Proposed to:** [team and role who owns design direction] | **Version:** [date] | **Status:** [draft / agreed]
## Principles
| # | Principle (the stand) | What it gives up | Who or what wins | Why it matters to users | Evidence |
|---|---|---|---|---|---|
| 1 | [value even when it costs X] | [the cost accepted] | [user group or goal] | [one sentence] | [source or evidence gap] |
## This, not that
| Principle | This (follows it) | Not that (breaks it) |
|---|---|---|
| [#] | [real screen or decision] | [real screen or decision, or example needed] |
## Conflict check
| Pair | Which wins | In which context |
|---|---|---|
| [#1 against #3] | [#] | [when] |
## How they are used
| Principle | As a critique objective | As a criterion for options |
|---|---|---|
| [#] | [the question to ask of a screen] | [the criterion wording] |
## Decision
[Role who owns design direction] agrees or changes the set with the team by [date]; [designer] revisits it on [date].
```

## Done When
- Four to seven principles, each with what it gives up and a user reason or a visible gap
- Every principle has a real "this, not that" pair or `[example needed]`
- Every pair of principles has a stated winner and a context, and each principle has a critique objective and a criterion wording

## Quality Bar
- Each principle passes the opposite test: a sensible team could choose the other way
- Examples come from your product only; public sets are a format reference, never copied in
- Past arguments appear as decisions, with no names attached to sides
- Claude drafts the wording; the team that uses the principles chooses them, and a user reason with no evidence shows as a gap.

## Next
Run pdes-design-options-tradeoffs (Design Options Trade-off Table) to use the principles as criteria when real options are compared.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
