---
name: build-heuristic-review
description: Walks your prototype against the 10 usability heuristics and writes up each problem with its screen and a proposed severity, an over-design check, a short accessibility pass and a ranked fix list. Use for "run build-heuristic-review", "review my prototype", "heuristic evaluation of these screens", "what is wrong with this prototype", "check usability before testing", "is this too cluttered", "quick accessibility check", "critique my screens", part of the Claude for Product Builders Pack by 90n.
---

# Prototype Heuristic Review

## When To Use
Claude says the prototype looks great and you are the only person who has seen it. Use this after the build and before any tester's time is spent. It answers: which problems could a careful reviewer catch today, so that users spend their sessions on the ones nobody could predict?

## When Not To Use
Once real sessions have happened, use Usability Test Findings: what users did outranks what a reviewer expected. Not for checking the look against your design system (use Design System Brief). If only one screen exists, a ten-minute read by a colleague is enough.

## Inputs
- The prototype: a link you may share with me, or screenshots of every screen in order, including empty, error and loading states
- The one task a user should complete, and who else can review it independently, by role
If you have none of this, I start from a written description of the screens and mark the output as a first draft.

## Approach
The method is heuristic evaluation as Nielsen Norman Group describes it (https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/), against its 10 usability heuristics (https://www.nngroup.com/articles/ten-usability-heuristics/), with its severity ratings (https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) and the W3C WAI Easy Checks (https://www.w3.org/WAI/test-evaluate/easy-checks/). The source asks for three to five evaluators working independently. I am one. The failure this prevents: a single reviewer's list, mine or yours, gets treated as proof that the prototype works.

## Workflow
1. I ask up to three questions. Which single task is in scope? Which screens and states can I see? Who gives the independent human pass, by role?
2. I go through the task once only to learn it, then a second time noting every element that breaks a heuristic, in order: visibility of system status; match between the system and the real world; user control and freedom; consistency and standards; error prevention; recognition rather than recall; flexibility and efficiency of use; aesthetic and minimalist design; help users recognize, diagnose and recover from errors; help and documentation.
3. For each problem I propose a severity from frequency, impact and persistence on the source's scale: 0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 catastrophe. One rater is unreliable, so every rating is marked "proposed".
4. Under heuristic 8, I run the over-design check: what can be removed without losing the task. Generated screens tend to add; this step subtracts.
5. I run a short accessibility pass on contrast, headings, keyboard focus and labels. The W3C page calls its checks "quick and easy, rather than exhaustive", so I write that a pass here is not an accessibility review.
6. You add at least one human pass, done without reading mine. I consolidate the lists, record how many evaluators there were, and rank the fixes by severity and effort. I close with the source's limits (a broken heuristic is not automatically a problem, and this does not replace user research) and with what only a real user can tell you.

## Output Format
```markdown
# Prototype Heuristic Review
Task in scope: [task] · Evaluators: [n], of which human: [n] · Screens seen: [list] · Not seen: [list]
## Problems
| # | Screen | What happens | Heuristic broken | Proposed severity (0 to 4) | Raised by |
|---|---|---|---|---|---|
| [n] | [screen] | [observation] | [heuristic] | [0 to 4, proposed] | [Claude / human pass] |
## Over-design check
- [Screen] · element that can go: [element] · what the task loses without it: [nothing / detail]
## Accessibility pass (quick, not a review)
| Check | Screen | What was seen |
|---|---|---|
| [contrast / headings / keyboard focus / labels] | [screen] | [observation] |
## Fixes, ranked
| Rank | Fix | Problem # | Effort | Fix before testing? |
|---|---|---|---|---|
| [n] | [fix] | [#] | [small / medium / large] | [yes / no] |
## What only a real user can tell you
- [Question this review cannot answer]

Limits: a broken heuristic is not automatically a problem, and this review does not replace user research.
## Decision
[Builder role] decides by [date] which fixes are made before the first session; [reviewer role] confirms the proposed severities or changes them.
```

## Done When
- One task was walked twice, and every problem names its screen and its heuristic
- Every severity is marked "proposed"; the evaluator count is stated; at least one human pass was added, or the review says plainly that none was
- The accessibility pass states it is not an accessibility review; whether one is required: check with a qualified adviser

## Quality Bar
- Nothing here is called a finding or a result: those words belong to sessions with users.
- Severity rates a problem on a screen, never the person who designed it.
- I describe what I can see; a state I was not shown is listed under "Not seen", not guessed.
- A review by Claude is not a test: real users still see it before anyone calls it ready.

## Next
Run build-claude-code-setup (Claude Code Setup) if the test needs a working version; it sets up a safe folder before any code exists.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
