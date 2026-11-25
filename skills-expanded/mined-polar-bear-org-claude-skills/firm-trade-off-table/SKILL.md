---
name: firm-trade-off-table
description: Compares the client's options in a consequence table, with criteria in the client's observable terms, musts kept apart from preferences, consequences per option with a source or a range, who bears each cost, dominated options removed and the value judgments left visible, with no weighted score unless you ask for one and own the weights. Use for "run firm-trade-off-table", "compare these options for the client", "trade-off table", "consequence table", "compare without a made-up score", "which option loses on everything", "who bears the cost of each option", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Trade-Off Table

## When To Use
The client asks for "a matrix" and expects a total at the bottom. You know that any weights you pick would simply produce the answer you already favour. Run this to compare the options honestly: what each one does to the things the client cares about, where the evidence is thin, and which judgment only they can make.

## When Not To Use
If the options are not yet distinct, go back to Strategic Options. To test whether one shaky estimate would flip the choice, use Sensitivity Analysis after this.

## Inputs
- The options that survived, with what each needs
- What the client said matters, in their words
- Evidence you hold for each consequence, with its source
If you have none of this, I start from two options and the outcomes you believe matter, and mark the table as a first draft with most cells "unknown".

## Approach
A consequence table puts objectives in rows and alternatives in columns and fills each cell with a predicted consequence; it is the comparison step of structured decision making, described here generically. Its discipline is to keep predictions (what will happen) apart from values (what matters more). A weighted score blends the two and can count one benefit twice under two names. The failure it prevents is the spreadsheet that proves the option its author preferred.

## Workflow
1. Ask, in one go: which outcomes matter most to the client, and why? Which requirements are non-negotiable? What evidence do you hold, and from where?
2. Define each criterion as something that can be observed, with a unit and a time horizon where there is one (monthly cost, weeks to first result, handovers per case). Separate outcomes from means; "a new system" is a means.
3. Split the criteria into musts and preferences. A must is pass or fail and is never traded. Check for pairs that measure the same benefit twice and merge them.
4. Fill each cell with the consequence for that option: a sourced fact, a range you can defend, or "unknown: ask [role]". A forecast and a value judgment never share a cell.
5. Add the distribution row: who gains, who carries the extra effort, who loses something, who has not been asked. Then remove an option only if the evidence shows it is no better than another on every criterion, and say which one beats it.
6. State the value judgments left for the client in plain words ("faster, or less disruption for the service team?"). Default to no score. If you ask for one, you supply the scales and weights, I show them beside the result and rerun it with the weights shifted.

## Output Format
```markdown
# Trade-Off Table
Decision: [question] · Options compared: [list] · Date: [date]
## Musts (pass or fail)
| Requirement | [Option A] | [Option B] | [Option C] |
|---|---|---|---|
| [must] | [pass / fail / unknown] | [status] | [status] |
## Consequences
| Criterion (unit, horizon) | [Option A] | [Option B] | [Option C] | Source or range |
|---|---|---|---|---|
| [criterion in their terms] | [consequence] | [consequence] | [consequence or unknown] | [source] |
| Who bears the cost | [group] | [group] | [group] | [source] |
## Removed as dominated
- [Option]: no better than [option] on any criterion (evidence: [source])
## Value judgments for the client
- [Trade-off in plain words]
## Decision
[Client decider role] makes the value judgments by [date]; [you] decide whether the table is solid enough to recommend from.
```

## Done When
- Every criterion is observable and each must is marked pass, fail or unknown
- Each cell holds a sourced fact, a defensible range or "unknown"
- No benefit is counted under two criteria
- The remaining value judgments are written as questions for the client

## Quality Bar
- No weighted total by default; a requested score shows your weights and a rerun with them shifted
- An option is called dominated only on evidence, never on preference
- People's basic interests are described, never converted into points
- Precision matches the evidence; no decimals on a guess
- Every consequence carries a source or reads unknown; I invent no figure, and the weighing belongs to the client and the recommendation to you.

## Next
Run firm-outside-view-check (Outside View Check) to test the forecast behind the leading option against completed cases.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
