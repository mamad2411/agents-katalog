---
name: impact-business-data-request
description: Drafts the request for group-level business figures held by another team, producing a figures table per agreed measure (definition, unit, period, group), a short data dictionary, the message to the data owner and a log of what was received and who vouches for it. Use for "run impact-business-data-request", "business data request", "ask for data to evaluate training", "request kpi data from another team", "data request to a data owner", "training impact data", "get the before and after figures", "data dictionary for training measures", part of the Claude Guide for Training Impact Pack by 90n.
---

# Business Data Request

## When To Use
The measure that matters sits in someone else's system and you have never been given access. Use this when the agreed measures are set and you need to ask a data owner for the before and after figures in a way they can answer in one go, and to keep a record of what came back.

## When Not To Use
If you have not yet worked out which before figures are needed or whether a comparison exists, the ask will be vague: run Training Baseline Plan first. If the figures are already in, run Before-and-After Results Table. This skill makes the ask and logs the answer; it reads nothing.

## Inputs
- The agreed measures from your Success Measures Agreement, with source and data owner
- The before and after periods and group definitions from your Training Baseline Plan, the date you need the figures by, and the minimum reporting group
If you have none of this, I start from the one figure you most need and the team that holds it, and mark the output "no agreement on file: first draft".

## Approach
The ROI Institute's methodology sets out a data collection plan by objective and measure, method, source and timing; this skill applies it to the hardest row, the one another team owns. Two judgements shape it. First, the owner is asked to aggregate before sending, so no row per person ever reaches you. Second, the request says what the figures will not be used for, because a data owner who suspects their numbers will be turned on individuals says no, and is right to. The failure it prevents: "can you send me the sales data?", followed three weeks later by a file of named rows in a different period from your baseline.

## Workflow
1. Ask three questions at once: which agreed measures need figures from another team and who owns each, what are the before and after periods and the group definitions, and what minimum reporting group do you set?
2. Write one line per agreed measure: the exact definition, the unit, the before and after periods, the group definition. The periods must match the baseline plan in length and season; if they do not, I flag the mismatch and do not paper over it.
3. Specify the aggregate: a count, a share or an average for the group, with the group size beside it. Never a row per person. Groups under the minimum are merged by the owner before sending, and the request says so.
4. Draft a short data dictionary: field, what it means, how it is calculated, known quirks. Every entry I cannot ground in your input is marked "to confirm", and the owner corrects it; they know where the figure breaks, you do not.
5. Draft the message to the data owner: why you are asking, exactly what, by when, how it will be used, and what it will not be used for (no individual is assessed). It asks them to vouch for what they send or to name who does. It is a draft; you send it, and a conversation first usually works better than a cold message.
6. Set up the log: requested, received, date, version, who vouches, caveats the owner gave. A figure with nobody behind it is logged "no voucher yet" and is not used.
7. State the rule for surprises: if person-level rows arrive anyway, do not upload them; ask for the aggregate. While a request is pending its cell stays blank, in every table downstream.

## Output Format
```markdown
# Business Data Request
Programme: [name] | Requested by: [role] | Needed by: [date] | Group figures only
## Figures needed
| Agreed measure | Exact definition | Unit | Before period | After period | Group definition | Aggregate asked for (count / share / average, with group size) |
|---|---|---|---|---|---|---|
| [measure] | [definition] | [unit] | [from, to] | [from, to] | [group] | [aggregate] |
## Data dictionary (for the owner to correct)
| Field | What it means | How it is calculated | Known quirks | Confirmed by owner |
|---|---|---|---|---|
| [field] | [meaning, or "to confirm"] | [calculation, or "to confirm"] | [quirk, or "none known"] | [yes / not yet] |
## Message to the data owner (draft, sent by you)
[Why we are asking. Exactly what, per the table. By when. How it will be used: to evaluate the programme at group level. What it will not be used for: no individual is assessed, and we do not want rows per person. Please merge groups under [minimum you set] and tell us who vouches for the figures.]
## Log
| Measure | Requested on | Received on | Version | Voucher | Owner's caveats | Status |
|---|---|---|---|---|---|---|
| [measure] | [date] | [date, or blank] | [version] | [name, or "no voucher yet"] | [caveat] | [pending / received / refused] |
## Missing
- [Measure]: [what is outstanding, and what cannot be reported until it arrives]
## Decision
[L&D lead name] sends the request by [date]; [data owner name] decides by [date] what can be shared and who vouches for it.
```

## Done When
- Every line carries a definition, a unit, both periods and a group definition that match the baseline plan
- The request asks for aggregates with group sizes and says in words that no rows per person are wanted; the message states what the figures will not be used for and asks for a voucher
- The log exists with every received cell blank, and the dictionary marks what the owner must confirm

## Quality Bar
- The owner's caveats are logged in their words and travel with the figure into every later table
- No figure is estimated, rounded up or borrowed from another period while the request is pending
- Requests to add names, employee numbers or a per-person export are refused in one line, with the aggregate offered instead
- Privacy and data protection points, including what may be shared across teams: check with a qualified adviser
- Only group figures are requested, each with a named person who vouches for it; no figure is filled in while the request is pending

## Next
Run impact-before-after-results-table (Before-and-After Results Table) to put the figures that arrived into one table.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
