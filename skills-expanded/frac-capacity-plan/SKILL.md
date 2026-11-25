---
name: frac-capacity-plan
description: Builds a capacity plan across all the clients of a fractional leader, setting contracted days per client against the days you can do focused work, with fixed meetings, preparation and switching time counted once, your own allowance for the unplanned, the gap, the options (move, reduce, renegotiate, release) and a monthly ledger. Use for "run frac-capacity-plan", "can I take a fourth client", "capacity planning for fractional work", "how many clients can I handle", "four clients fit the calendar and not the week", "am I overcommitted", "capacity ledger for my clients", part of the Claude for Fractional Leaders Pack by 90n.
---

# Client Capacity Plan

## When To Use
Four clients fit the calendar and still do not fit the week. Each contract looks reasonable alone; together they leave no room for preparation, for the switch between companies, or for the week when two of them have a crisis. Use it before you say yes to a new client, and each month after.

## When Not To Use
If the total fits and you need the shape of the week, run Week Plan Across Clients. If one client alone takes more than it pays for, run Weekly Review Across Clients to see it, then Scope Change Request to price it.

## Inputs
- Per client, by name or code: contracted days per month, fixed meetings, and any known peak (board dates, a launch, year end)
- Your working days in the period after leave, and the time your own business takes
- Your logged days for the last month or two, if you keep them
If you have none of this, I start from your contracted days and your own estimate of the rest, label every estimate as an assumption and mark the plan as a first draft.

## Approach
Capacity against availability, with a ledger kept monthly, as a fractional marketplace's guidance and a public playbook for fractional executives describe it. Availability is the time you could work; capacity is the time you can do focused, decision-grade work. The gap between them is real, and its size is yours: the sources give percentages as rules of thumb, and none is used here. The failure this prevents is quoting availability to a new client and paying for it in evenings.

## Workflow
1. Ask at most three questions: which period are we planning; what are your working days in it after leave; is a new client or a change of days on the table?
2. Start from working days and subtract, once each: fixed client meetings, preparation and follow-up, switching time between clients, your own business (selling, admin, learning). Say for each figure whether it comes from your log or is an estimate.
3. Subtract an allowance for the unplanned, taken from your own recent weeks. With no history, we use your stated assumption and label it. I apply no universal buffer.
4. What remains is focused days. Set it against contracted days per client, month by month, and mark the months where two clients peak together.
5. Show the gap in days, with the arithmetic. A plan that only fits on the optimistic estimate is flagged as overcommitted.
6. Lay out the options per client: move days to another week or month, reduce the scope, renegotiate days or fee, release the client. Each change to a client's days is theirs to agree; I draft nothing to them here.

## Output Format
```markdown
# Client Capacity Plan
Period: [months] · Working days after leave: [n] · Internal page, not shared with any client
## From availability to capacity
| Line | Days | From log or estimate |
|---|---|---|
| Working days | [n] | [calendar] |
| Fixed client meetings | [n] | [log / estimate] |
| Preparation and switching | [n] | [log / estimate] |
| Own business | [n] | [log / estimate] |
| Allowance for the unplanned | [n] | [your recent weeks / assumption] |
| Focused days left | [n] | [arithmetic] |
## Ledger by client and month
| Client (name or code) | Contracted days | Known peak | [Month 1] | [Month 2] | [Month 3] |
|---|---|---|---|---|---|
| [client] | [n] | [date, reason] | [days] | [days] | [days] |
Gap: focused days [n] against contracted days [n] = [n] · Months where peaks collide: [list]
## Options
| Client | Move | Reduce | Renegotiate | Release |
|---|---|---|---|---|
| [client] | [what, when] | [what] | [days or fee, yours to set] | [by when] |
## Decision
[You] decide by [date] whether the new commitment fits and which option to raise with which client.
```

## Done When
- Every line is counted once and is marked log or estimate
- The allowance for the unplanned comes from your own weeks or is labelled an assumption
- The gap is shown with its arithmetic, month by month, and the plan fits without evenings or weekends as routine

## Quality Bar
- No universal percentage, client count or "typical" load is applied
- An overload is shown as a resource gap, never as a question of your discipline
- Options that change a client's days are proposals until that client agrees
- Fees appear only if you give them, and none is suggested
- Clients appear by name or code with days only; no client's content enters another's row, and the page is never sent to a client

## Next
Run frac-week-plan (Week Plan Across Clients) to give those days a shape with fewer switches.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
