---
name: build-decision-memo
description: Writes a one-page decision memo after a prototype test, producing the decision asked in the first lines, three options (build, change and test again, stop) with their cost as engineering states it, and the roles who decide, contribute and are informed. Use for "run build-decision-memo", "write the decision memo", "build, change or stop", "get a decision on my prototype", "who decides what happens to the prototype", "everyone likes it and nobody has decided", "go or no-go after the user test", part of the Claude for Product Builders Pack by 90n.
---

# Build, Change or Stop Decision

## When To Use
The prototype has been praised by everyone and decided on by no one. The demo went well, people nodded, and two weeks later it is still a link in a channel. This page answers: what exactly is being decided, by which one person, by when, and on what evidence?

## When Not To Use
Before the prototype exists, the page you need is Idea One-Pager, which asks for time to build and test. If the test has run and there is no agreed account of it yet, run Prototype Learning Card first: a decision page without evidence is a pitch.

## Inputs
- The learning card: the belief, the result against the pass line, what is still unknown
- The gap to production as engineering wrote it, and any cost in people time they have stated
- Who can say yes: the role with authority over the team's time
If you have none of this, I start from the question and the three options and mark the output as a first draft, with evidence and cost left in brackets.

## Approach
Bottom line up front, the standard in US Army Regulation 25-50 (armypubs.army.mil), puts the main point at the beginning so the page is understood in a single rapid reading. DACI decision roles from the Atlassian Team Playbook (atlassian.com/team-playbook/plays/daci) give the decision one Driver and one Approver. The judgment is in the options. A page that offers "ship the prototype" will get that answer, because it looks free. It is not on this page.

## Workflow
1. Ask three questions: what the learning card says about the pass line; what engineering has stated about the gap and its cost in people time; and which single role approves, by what date.
2. Title the page with the question, as the play does, and write the decision asked, of whom and by when in the first lines. A reader who stops after three lines should still know what they are being asked.
3. Set the roles: one Driver (gathers the information and gets a decision made by the date), one Approver (the single person who decides), Contributors (a voice, no vote), Informed (told the outcome). Two Approvers means no decision; push back until there is one.
4. Lay out exactly three options: build (engineering builds it properly), change and test again, stop. For each, write what it means in practice and what happens to the prototype. "Ship the prototype" does not appear, in any wording.
5. Fill the evidence from the learning card, quoted as run, and the gap from the gap note. Cost in people time is what engineering stated. If they have not stated it, the cell reads "not yet stated": do not estimate for them.
6. Add the Driver's recommendation if there is one, labelled as a recommendation and kept apart from the evidence. Earlier enthusiasm from anyone in the room is not evidence. Leave the outcome and its date blank for the Approver to fill in, then list who is told. In Claude Docs, ask for the page as a doc in the conversation and share it with the Approver and Contributors for comments.

## Output Format
```markdown
# Build, Change or Stop Decision
**Decision asked:** [Should we build, change and test again, or stop [idea]?] | **Of:** [Approver, role] | **By:** [date]
This is a decision about a prototype. Shipping the prototype is not an option on this page.
## Roles
| Driver | Approver | Contributors | Informed |
|---|---|---|---|
| [role] | [one role] | [roles] | [roles] |
## Evidence
Belief tested: [from the learning card] | Pass line: [threshold, set on date] | Result: [n] of [N], [met / not met / unclear] | Still unknown: [from the learning card]
## Gap to production
[Work items as engineering listed them, each with an owning role. No dates from the builder.]
## Options
| Option | What it means | Cost in people time (as engineering states it) | What happens to the prototype |
|---|---|---|---|
| Build | [engineering builds it properly] | [stated / not yet stated] | [reference only] |
| Change and test again | [what changes, which belief is retested] | [stated / not yet stated] | [revised, new round with real users] |
| Stop | [what is dropped, what is kept as learning] | [none / stated] | [access removed on [date]] |
Driver's recommendation (a recommendation, not the outcome): [option and reason, or "none"]
## Decision
The [Approver, by role] chooses build, change or stop by [date]. Outcome: [filled in by the Approver] on [date]. Told afterwards: [Informed roles].
```

## Done When
- The decision, the Approver and the date are readable in the first three lines
- There are exactly three options and none of them ships the prototype
- Every cost cell is either engineering's own statement or "not yet stated"
- The outcome line is blank until the Approver fills it

## Quality Bar
- One page. Detail moves to the learning card or the gap note, never to a smaller font.
- No invented cost, date, estimate or result; unknowns stay in [brackets].
- Roles describe who decides, not who was right. Nobody is assessed on the page.
- A named person decides between build, change or stop; shipping the prototype is not on the page, and engineers own what ships.

## Next
Run build-experiment-design (Experiment Design Plan) if the decision is build, to plan how the engineer-built version will be measured on real traffic.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
