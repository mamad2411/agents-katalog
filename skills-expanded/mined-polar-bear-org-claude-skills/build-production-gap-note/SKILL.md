---
name: build-production-gap-note
description: Writes a Prototype vs Production Note that reads the test result against the dated pass line, lists what the prototype does not prove and what is faked, and sets out the gap to production as work items with an owning role and no dates. Use for "run build-production-gap-note", "people are calling my prototype version one", "what does this prototype not prove", "gap to production", "is this ready to ship", "it looks finished but it is a prototype", "what does engineering still have to build", "write the this is a prototype note", part of the Claude for Product Builders Pack by 90n.
---

# Prototype vs Production Note

## When To Use
It looks finished, so someone has started calling it "version one". The link is travelling further than you sent it. This skill answers: what did the prototype prove, what can it not show, and what stands between it and something customers could rely on?

## When Not To Use
If nothing has been tested yet, run Prototype Test Card: this note reads a result, it does not set a pass line. If engineers need to know how to open it and why it was built this way, run Engineering Handover Note. For what the team learned, run Prototype Learning Card.

## Inputs
- The test card with its dated pass line, and the result of the sessions as run.
- A list of what is faked, hardcoded or played by a person, and who has seen the prototype so far, by role.
If you have none of this, I start from a one-line description of the prototype and mark the output as a first draft.

## Approach
Three public sources set the boundary. The Test Card (Strategyzer, https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card) gives the pass line the result is read against. The GOV.UK Service Manual (https://www.gov.uk/service-manual/design/making-prototypes) says prototype code "does not need to meet the same standards as production code" and "Do not just copy prototype code into production." The Scrum Guide (https://scrumguides.org/scrum-guide.html) describes the Definition of Done as the state of the work when it meets the quality the product requires. The failure this prevents: "it works" in a meeting becoming "it is ready" in an email, then a date on a plan.

## Workflow
1. Ask at most three questions: what was the pass line and what happened in the sessions; what in the prototype is faked; who is treating it as finished, and which role in engineering can say what production requires?
2. Open with "This is a prototype." It is the first line of the note and the sentence that goes on every share of the link.
3. Proved: set the result as run beside the pass line as written and dated. Mark it met, not met or unclear. Nothing softer, and no second pass line.
4. Does not prove: one line each for scale, reliability, security, real data, edge cases and support load, saying why the prototype cannot show it. A line may read "not relevant, because", but it may not be missing.
5. Faked: list every part that is hardcoded, sample data or a person behind the screen, and what a user would notice if it were real.
6. Definition of Done: the prototype has not met the team's. Engineering states what theirs requires. I leave that cell open for them and do not guess it.
7. The gap: write each missing piece as a work item with an owning role. No dates and no estimates from you. Security items end with: check with your engineering or security lead.

## Output Format
```markdown
# Prototype vs Production Note
**This is a prototype.** | **Prototype:** [name] | **Written on:** [date] | **Seen so far by:** [roles]
## What it proved
| Belief tested | Pass line (set on [date]) | Result as run | Reading |
|---|---|---|---|
| [belief] | [threshold] | [n] of [N] [behaviour] | [met / not met / unclear] |
## What it does not prove
| Area | Why this prototype cannot show it | What would show it |
|---|---|---|
| Scale | [reason] | [test or build] |
| Reliability | [reason] | [test or build] |
| Security | [reason] | [check with your engineering or security lead] |
| Real data | [reason] | [test or build] |
| Edge cases | [reason] | [test or build] |
| Support load | [reason] | [test or build] |
**Faked:** [part]: [hardcoded / sample data / played by a person]
## Gap to production
| Work item | Owning role | What the team's Definition of Done requires (engineering fills in) |
|---|---|---|
| [item] | [role] | [open] |
## Decision
[Engineering lead, by role] confirms or corrects the gap list by [date they set]. [Decision owner, by role] then chooses build, change or stop. Copying the prototype into production is not an option on this page.
```

## Done When
- The first line reads "This is a prototype." and the same sentence is ready to paste on every share.
- The result sits beside a pass line dated before the sessions.
- All six areas have a line and every faked part is listed. The Definition of Done column is left for engineering, and every gap item has an owning role and no date.

## Quality Bar
- No result is invented, predicted or rounded up. Enthusiasm in a meeting is not a result.
- Owners are roles. The note does not rate anyone's work, including the builder's.
- Anything on personal data or consent ends with: check with a qualified adviser.
- A prototype is never called production; the gap list has owners and no dates, and engineers own what ships.

## Next
Run build-engineering-handover (Engineering Handover Note) to tell engineers what exists, how to open it and why it was built this way.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
