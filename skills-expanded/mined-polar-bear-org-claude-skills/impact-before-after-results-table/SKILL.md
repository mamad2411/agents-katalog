---
name: impact-before-after-results-table
description: Builds one table of what changed for a training programme from your own exports, producing each agreed measure before and after with its group size, the absolute and relative change beside any comparison, and a source and a voucher for every figure. Use for "run impact-before-after-results-table", "before and after training results", "training results table", "pre and post training data", "did the numbers change after training", "compare before and after the programme", "analyse my training data export", part of the Claude Guide for Training Impact Pack by 90n.
---

# Before-and-After Results Table

## When To Use
The exports are in, from your LMS, your survey tool and the data owner, and you need one table you could defend line by line. This skill answers a narrow question: for each agreed measure, what was the figure before, what is it now, for how many people, and who stands behind it.

## When Not To Use
Not for explaining why a figure moved: that is Training Contribution Analysis. Not for open text answers (Open Comment Themes) and not for putting a money value on the change (Training ROI Range). If the before figures were never captured, say so to the sponsor instead of building half a table.

## Inputs
- The Success Measures Agreement: the agreed measures, their units, and what "worked", "partly" and "did not" mean.
- The before and after figures per measure, at group level. Upload the export as a CSV file, or paste it.
- The comparison, if you have one (a comparison group's figures, or the periods behind a trend line), plus the source of each figure and the named person who vouches for it.
If you have none of this, I start from the figures you can paste and mark the output "no agreement on file: first draft".

## Approach
This is a before and after reading against a baseline, with the isolation method named, as the ROI Institute's methodology page asks, and with change described by its direction, its absolute size and its relative size, following "Communicating quality, uncertainty and change" from the UK Government Analysis Function. The table states what changed and stops there. The failure it prevents: a relative change on a tiny group, with no group size beside it, lands on a slide as the headline, and the first person to ask "out of how many?" takes the whole report down with it.

## Workflow
1. Ask three questions at once: what is your minimum reporting group, below which a group is merged or suppressed (you set it, I never supply one); which periods and which group definition do the before and after figures use; and what else changed in the work during that time (a new tool, a season, a staffing change in the group)?
2. Check that the figures can be compared before computing anything. The before and after periods must match in length, and in season where the work has one, and the group must be defined the same way both times. A mismatch is written into the row, not smoothed over. If the upload holds a row per person, I aggregate it, never reproduce the rows, and tell you the file should be aggregated before it is shared.
3. Build one row per agreed measure, in the agreement's order and wording: before, after, the group size for each, the source and the voucher. A figure with no voucher is marked `[no voucher yet]`.
4. Compute the change from your figures only. Absolute change is after minus before, in the measure's unit. Relative change is the absolute change divided by before, as a percentage. Both are shown together. Where before is zero, or the group is below your minimum, the relative change is not shown and the row says why.
5. Put the comparison beside the trained group where one exists: the comparison group's own change, or the value the trend line expected. Name the isolation method, or write "none". Your list of what else changed goes into the table itself, against the measures it could have touched.
6. Set each row against the agreement's verdicts (worked, partly, did not) and give it a claim strength: shown, suggested or unknown. With no comparison, a row is "suggested" at most.
7. Write the wording under the table: "estimate" where a figure is one, what can and cannot be concluded, and no trend from two points. Every cell the files could not fill stays blank and is listed as missing, with who could supply it.

## Output Format
```markdown
# Before-and-After Results Table
Programme: [name] | Before period: [dates] | After period: [dates] | Minimum reporting group: [you set] | Status: [agreement on file / no agreement on file: first draft]
## Results by agreed measure
| Agreed measure (unit) | Before (group size) | After (group size) | Absolute change | Relative change | Source | Voucher |
|---|---|---|---|---|---|---|
| [measure] ([unit]) | [your figure] ([n]) | [your figure] ([n]) | [after minus before] | [% or "not shown: reason"] | [source] | [name or "no voucher yet"] |
## Comparison and what else changed
| Agreed measure | Isolation method | Comparison change or expected value | What else changed in the period | Verdict in the agreement | Claim strength |
|---|---|---|---|---|---|
| [measure] | [comparison group / trend line / forecast / none] | [your figure or blank] | [your list] | [worked / partly / did not / not set] | [shown / suggested / unknown] |
## Suppressed or merged groups
[Group]: below the minimum reporting group, [merged with ... / suppressed]. One line per group.
## What this table can and cannot say
- Can be concluded: [statement of change, with "estimate" where it is one]
- Cannot be concluded: [cause, trend, or anything about a person]
## Missing
[Measure, column]: left blank because [not in the files]; [role] could supply it. One line per blank cell.
## Decision
[Name] decides whether these figures are complete enough to go to the sponsor, or which missing ones to chase first, by [date].
```

## Done When
- Every agreed measure has a row, even when the row is mostly blank.
- Every figure carries a group size, a source and a voucher, or says which is missing.
- Absolute and relative change appear together, or the row says why the relative change is not shown.
- No group below your minimum appears on its own, and each row has a verdict from the agreement and a claim strength.

## Quality Bar
- Measures keep the agreement's definitions and units. Nothing is redefined to make a figure look better.
- No causal verb in or under the table: no "thanks to", "led to" or "drove". It says "changed from [x] to [y]".
- A blank cell beats a guess. Nothing is estimated, rounded up or carried over from another period to fill a gap.
- Group rows only. No row, name, initials or employee number for a person, and no comparison of one person, manager or trainer with another. Privacy and data protection questions about the exports: check with a qualified adviser.
- Every figure is yours, with its source and voucher; a blank stays blank, and the table states change, never cause.

## Next
Run impact-open-comment-themes (Open Comment Themes) to read what people wrote beside the numbers.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
