---
name: pdes-design-quality-bar
description: Writes a Design Quality Bar for the work you are held to, with yes or no checks by stage (explore, refine, ready to build) drawn from the ten usability heuristics, WCAG 2.2 at your team's level, design system use, content and the product's principles, plus a proposed must-pass list for the person who owns quality to confirm. Use for "run pdes-design-quality-bar", "write down the quality bar", "what does raise the bar mean", "design quality checklist by stage", "definition of done for design", "what must pass before handoff", "heuristics and accessibility checklist", "is this good enough to build", part of the Claude for Product Designers Pack by 90n.
---

# Design Quality Bar

## When To Use
"Raise the bar" is said every quarter, nobody has written the bar, and you learn the standard by being corrected in review. You want it on one page before the next review moves it again. It answers: what does my work have to meet at each stage, and which checks must pass before it goes to build?

## When Not To Use
If the argument is about what the product chooses (speed over control, guidance over freedom), write Design Principles first: the bar checks work, it does not settle stands. If you want one pass over one task before tomorrow's review, use Design Self-Critique.

## Inputs
- The product's design principles, the design system's documented rules and the accessibility level your team has committed to, where they exist
- Review comments you keep getting, pasted as they were written, with names removed
If you have none of this, I start from the ten heuristics and WCAG 2.2 at the level you name, and mark the output as a first draft.

## Approach
The 10 usability heuristics published by Nielsen Norman Group and the W3C's WCAG 2.2 success criteria, mapped to three stages of one piece of work. Every line is a yes or no check or a question, never a score out of ten: a six starts a negotiation, a "no" starts a fix. The failure it prevents is the flow that passed three reviews on taste and met its first keyboard user after launch, because nobody asked about focus order until the build was done.

## Workflow
1. Ask three questions: which stages does your work really pass through (default explore, refine, ready to build), which accessibility level has your team committed to, and which review comments keep coming back?
2. Explore, is it the right problem and direction: a few questions only, each tied to the brief or a principle. A heavy checklist at this stage kills the exploring.
3. Refine, does it work: each heuristic turned into a question about this work, under its exact name. Visibility of System Status; Match Between the System and the Real World; User Control and Freedom; Consistency and Standards; Error Prevention; Recognition Rather than Recall; Flexibility and Efficiency of Use; Aesthetic and Minimalist Design; Help Users Recognize, Diagnose, and Recover from Errors; Help and Documentation. Add content checks: labels, errors and empty states in plain words.
4. Ready to build, is it complete: WCAG 2.2 success criteria at your team's level, named by number; system use (components, tokens by name, documented exceptions); every state designed; copy final.
5. Split ready to build into must-pass and nice-to-have. I propose the split from your recurring comments and mark every line "proposed": the person who owns quality confirms it, not you and not me.
6. Write how you will use it: as numbered objectives at crit, as checks you answer before a review. No pass rates per person and no tally of whose work fails.
7. State the limits on the page: heuristics find usability issues, not strategy or brand fit, and a checklist pass is not an accessible product. Accessibility duties vary, so check with a qualified adviser.

## Output Format
```markdown
# Design Quality Bar
**Product area:** [area] | **Accessibility level:** [the team's stated level] | **Status:** proposed | **Quality owner:** [role]
## Explore: is it the right problem and direction?
| Check (yes, no or a question) | Source |
|---|---|
| [does it answer the problem in the brief?] | [brief or principle] |
## Refine: does it work?
| Check | Heuristic or content rule |
|---|---|
| [question about this work] | [heuristic name as NN/g writes it] |
## Ready to build: is it complete?
| Check | Source | Must-pass or nice-to-have |
|---|---|---|
| [check] | [WCAG 2.2 criterion, system rule or principle] | [proposed] |
## How I use it
- At crit: [checks offered as objectives]. Not covered by this bar: strategy, brand fit, use by real people, conformance.
- Before a review: [checks answered, with the gaps listed]
## Decision
[Design lead or product manager, whoever owns quality] confirms or edits the must-pass list and the accessibility level by [date]; the bar is looked at again on [date].
```

## Done When
- Every stage has checks, the fewest at explore and the most at ready to build, each a yes or no or a question with its source beside it
- All ten heuristics appear under their exact names, each as a question about this work
- Every must-pass line reads "proposed" and the quality owner is named by role

## Quality Bar
- No scores out of ten, no thresholds I made up, no pass rates
- WCAG is cited as numbered success criteria at the team's stated level, never as "accessible"
- Recurring review comments become checks about the work, with no trace of who made them or who received them
- Accessibility law and duties end with "check with a qualified adviser"
- Passing the bar means the checks were answered, not that users can use it; the work is checked, never the designer

## Next
Run pdes-design-self-critique (Design Self-Critique) to run the work through the bar yourself.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
