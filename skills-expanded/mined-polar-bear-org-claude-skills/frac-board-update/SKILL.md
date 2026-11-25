---
name: frac-board-update
description: Builds a one-page board update for a fractional leader in six fixed blocks (the number against the commitment, the arithmetic behind it, the main constraint, what moved, ranked risks with early signals and the decisions asked), with definitions footnoted and kept stable and an appendix, where the leader owns the numbers and the CEO owns the asks. Use for "run frac-board-update", "a few slides for the board", "board update template", "board report for my function", "one page for the board meeting", "prepare the board update for the CEO", "monthly board memo", part of the Claude for Fractional Leaders Pack by 90n.
---

# Board Update

## When To Use
The CEO asks for "a few slides for the board" by Thursday. Left alone, that becomes a deck that grows each month, with last quarter's definitions quietly changed and the bad news on slide eleven. This answers: what does the board need on one page to see where the function stands and what it is asked to decide?

## When Not To Use
If a number has just turned and the board meeting is weeks away, run Early Warning Note to the CEO now. If the reader is the CEO alone, run Monthly Value Report.

## Inputs
- The commitment the board holds the function to, and the figures to date with their source
- How the number is built in this function (the steps or drivers a director could recompute)
- The risks you see, and the decisions the CEO wants from the board
If you have none of this, I start from the commitment and the latest figure, leave the other blocks bracketed and mark the page as a first draft.

## Approach
A one-page board report in six fixed blocks, identical every month so directors read the changes, as an agency's article on reporting a fractional role to a board sets it out; a public playbook for fractional executives describes the same thing as a short monthly memo. The source was written for one function, so the arithmetic block is rebuilt for yours. The failure this prevents has three forms: the page grows into a deck, a definition shifts between meetings, and bad news arrives late. One rule sits above the rest: you own the numbers, the CEO owns the asks and presents them.

## Workflow
1. Ask at most three questions: what commitment does the board hold this function to; which decisions does the CEO want from this meeting; has any definition changed since the last page?
2. Block 1, the number against the commitment: the period, the cumulative figure and the gap. A month shown without the cumulative gap hides the story.
3. Block 2, the arithmetic: the few drivers that produce the number in your function, in one small table, each traceable to a system, so any director can rebuild it. A revenue seat shows the steps from lead to closed deal; a finance seat shows what moved cash; a people seat shows the flow from open role to start date; an operations seat shows volume, time and failures.
4. Block 3, the constraint: one sentence naming the single thing that caps progress, with the evidence. A mood is not a constraint. If it has been the same for several meetings, say so: either the moves against it were too small or the diagnosis was wrong.
5. Blocks 4 and 5: what moved, as effects and not as work done; then three risks at most, ranked, each with the early signal you are watching.
6. Block 6, the asks: decisions, not updates. For each, the options, what each costs and what deferring costs. The CEO edits and presents them. Footnote every definition; if one changed, show both series this once. Keep the page to one side and move the rest to an appendix; build it in Claude Docs, or Claude Slides if the board expects slides, and the CEO sends it ahead.

## Output Format
```markdown
# Board Update
Client: [name] · Function: [function] · Period: [month] · Numbers: [you] · Asks: [CEO]
## 1. Number against commitment
Commitment: [figure] · This period: [figure] · Cumulative: [figure] · Gap: [figure]
## 2. The arithmetic
| Driver | Value | Source |
|---|---|---|
| [driver a director could recompute] | [value] | [system] |
## 3. Constraint
[One sentence naming the single constraint] · Evidence: [measurement]
## 4. What moved
- [effect, with figure]
## 5. Risks
| Rank | Risk | Early signal |
|---|---|---|
| [1] | [risk] | [what you would see first] |
## 6. Asks (owned and presented by the CEO)
| Decision asked | Options and cost of each | Cost of deferring |
|---|---|---|
| [decision] | [options] | [consequence] |
Definitions: [measure: definition, window, source; changed since last time? both series shown]
## Decision
[CEO] approves the page and presents the asks on [board date]; [you] answer questions on the numbers if invited.
```

## Done When
- All six blocks are present, in order, on one side
- Every figure has a source, every measure a footnoted definition, and there are no more than three risks, each with an early signal
- Each ask is a decision with options and the cost of deferring

## Quality Bar
- The same six blocks every month; nothing is re-baselined quietly, and "what moved" lists effects while work done goes to the appendix
- Bad news is on the page the month it is true, in block 1 or block 5
- Governance or disclosure questions about what a board must be told: check with a qualified adviser
- Every number comes from this client's systems as you give it, nothing from another client's board page is reused, and neither you nor Claude speaks to the board in the CEO's place

## Next
Run frac-early-warning-note (Early Warning Note) when a number on this page turns between meetings.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
