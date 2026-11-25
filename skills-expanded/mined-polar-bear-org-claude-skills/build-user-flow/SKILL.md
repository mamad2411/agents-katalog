---
name: build-user-flow
description: Maps one journey from entry to done as a screen-by-screen flow, with each screen's purpose, the control that leaves it and where that leads, the dead ends, the empty, error and loading state per screen and one large-data case. Use for "run build-user-flow", "list every screen before I build", "what happens after the first click", "map the user flow", "write the wireflow", "which states am I missing", "find the dead ends in my flow", part of the Claude for Product Builders Pack by 90n.
---

# Screen-by-Screen User Flow

## When To Use
The idea is clear in your head and falls apart the moment you list what happens after the first click. Use it after the brief has fixed how real the prototype must be and before any screen is drawn. It answers: which screens exist, what does the user press on each, and where does that take them?

## When Not To Use
If you have not decided how much has to work or which surface to build on, run Prototype Brief first. If you need what each screen must do and how to check it, that is Prototype Spec; this flow carries no pass or fail checks. For several separate journeys, run it once per journey rather than cramming them onto one page.

## Inputs
- The one task the user is trying to finish, and what "done" looks like for them
- Where they start (a link, a home screen, a notification), the brief, and any sketches or sample content you have
If you have none of this, I start from the task in one sentence and mark the output as a first draft, with every guessed screen flagged.

## Approach
A wireflow, as Nielsen Norman Group describes it (https://www.nngroup.com/articles/wireflows/), joins screen layouts with a simple flowchart: each arrow starts at the specific control the user acts on and ends at the result. To that I add the states the Anthropic Academy tutorial asks for before hand-off (https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux): empty, error, loading, and a different data volume. The failure it prevents: five beautiful screens of the happy path, and a tester who mistypes one field in the first minute and lands on nothing.

## Workflow
1. I ask at most three questions: what single task is this journey, where does the user enter, and what do they see when they are done?
2. Keep it to one task flow per page. The format suits a task and grows unwieldy for many separate pages, so a second journey gets its own run. I say so rather than squeeze it in.
3. Walk the journey in order and write one row per screen: its purpose in a few words, the exact control the user acts on (the button or field by its label, never "they continue"), and where that leads.
4. Name the kind of result for every arrow: a new screen, the same screen with changed content, or feedback such as a confirmation or an error. "Same screen, changed" is the one people forget, and it is where most prototypes go blank.
5. Mark decision points, where one screen has more than one way out, and give each exit its own row. Then mark dead ends: any screen with no way forward or back.
6. Add three states per screen: empty (nothing to show yet), error (the action failed), loading (waiting). A state you decide to skip is written as skipped with a reason, not left out.
7. Add one large-data case: the same flow with far more rows than the sample, and what the screen does then. If you are working in Claude Design, walk it through this full journey so each screen is drawn in context.

## Output Format
```markdown
# Screen-by-Screen User Flow
Task: [what the user is trying to finish] | Entry: [where they start] | Done: [what they see at the end] | Date: [date]
## Flow
| # | Screen | Purpose | Control acted on | Leads to | Result type |
|---|---|---|---|---|---|
| S1 | [screen] | [purpose] | [button or field label] | [S2, or stays on S1] | [new screen, changed content, feedback] |
Guessed, not yet agreed: [screen numbers] | Owner: [role]
## Decision points
| Screen | Choice | Exit A leads to | Exit B leads to |
|---|---|---|---|
| [screen] | [what the user chooses between] | [screen] | [screen] |
## Dead ends
- [Screen with no way forward or back] | Fix: [the missing control, or "open"]
## States
| Screen | Empty | Error | Loading |
|---|---|---|---|
| [screen] | [what shows] | [what shows, and the way out] | [what shows] |
## Large-data case
[The screen and the volume, for example a list with far more rows than the sample] | What it does: [behaviour] | Example content is sample content only.
## Decision
[Role who owns the test] agrees this is the one journey to build, and which skipped states are acceptable, by [date]; a second journey is a separate page.
```

## Done When
- A reader can trace the journey from entry to done without asking you a question
- Every arrow starts at a named control and ends at a named result
- Every screen has its three states filled in or marked skipped with a reason
- No dead end is left without a fix or an owner, and one large-data case is written

## Quality Bar
- One journey per page; a second task is a second flow.
- Controls are named by their label on screen, so the flow can be pasted straight into a build prompt.
- Screens and connections only; what each must do and how to check it stays out. Guessed screens are flagged as guesses.
- Example rows hold sample content: no real names, emails or account details.
- The flow is a plan for a prototype that real users will try; it does not describe what engineers will ship.

## Next
Run build-prototype-spec (Prototype Spec) to turn the flow into numbered requirements.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
