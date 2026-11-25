---
name: pdes-design-pushback-brief
description: Writes a Design Pushback Brief with the request in its own words and the goal behind it, the risk to users and to the business from real evidence or a visible gap, two alternatives that meet the goal, what you will and will not do, who decides if you still disagree and how the disagreement is recorded. Use for "run pdes-design-pushback-brief", "push back on a design request", "asked to ship a deceptive pattern", "say no to a stakeholder", "this change will hurt users", "rushed AI feature", "disagree and commit", "escalate a design disagreement", part of the Claude for Product Designers Pack by 90n.
---

# Design Pushback Brief

## When To Use
You are asked to ship a deceptive pattern, a rushed AI feature or a change you believe will hurt users. Run it before you reply, while you can still choose your tone and your route. It answers: what exactly is the risk, what could we do instead, and who decides if we still disagree?

## When Not To Use
If it is one comment among many from a review, triage it in the Stakeholder Feedback Log; not every note needs a stand. If the matter involves danger, harassment or serious misconduct, go to the right human route first (your manager, the people team, a legal or ethics contact). This brief is for a disagreement about the work.

## Inputs
- The request in the words it was made (message, ticket, meeting note), who asked by role, and the goal behind it if anyone stated it
- Real evidence of risk: test findings, support contacts, analytics, complaints, accessibility issues, each with its source
- Who has authority over this decision, by role
If you have none of this, I start from the request alone, mark the goal and the evidence `[to confirm]` and mark the output as a first draft.

## Approach
"Have Backbone; Disagree and Commit" from the Amazon Leadership Principles: respectfully challenge a decision when you disagree, even when that is uncomfortable, and once a decision is made, commit to it. It is paired here with a proportionate escalation route: an observable trigger and the lowest person with authority to resolve it. You argue with the request and its effects, never with the requester. The failure it prevents: a bare "no" in a public thread with no alternative, a design question turned into a standoff, and the pre-ticked consent box shipping anyway with no record that anyone objected.

## Workflow
1. Ask up to three questions: what goal sits behind the request, what evidence of harm do you hold, and who can decide if you and the requester still disagree?
2. Quote the request verbatim and state the goal behind it. Then name the kind of objection: user harm, business risk or capacity. A taste preference is none of the three, and I will say so if that is what this is.
3. Write the risk to users and to the business. Each line is backed by evidence you pasted or marked `[gap]`. Legal, privacy, consumer protection and accessibility concerns become questions that end "check with a qualified adviser"; they are never stated as fact.
4. Draft two alternatives that meet the requester's goal with less harm, each with its cost in time or scope. An alternative that ignores the goal is only a refusal with extra steps.
5. State what you will do and what you will not do, plainly. No threats, no ultimatums, no audience.
6. Set the escalation route: an observable trigger (for example "the request is still in the sprint on [date]"), the lowest role with authority to resolve it, usually your manager or the product manager first, and a short note with the facts, the impact and the decision needed.
7. If the decision goes the other way, record the dissent as an entry in the decision log and write what you commit to. One exception: anything you believe is unlawful or unsafe goes to an adviser, not to "commit".

## Output Format
```markdown
# Design Pushback Brief
**Request:** "[verbatim]" | **Asked by:** [role] | **Goal behind it:** [goal or to confirm] | **Objection:** [user harm / business risk / capacity]
## Risk
| Risk to | What could happen | Evidence (source) or [gap] |
|---|---|---|
| Users | [effect] | [evidence] |
| The business | [effect] | [evidence] |
| Legal or regulatory question | [question], check with a qualified adviser | [source or gap] |
## Alternatives that meet the goal
| Option | How it meets the goal | Cost (time, scope) | Harm it avoids |
|---|---|---|---|
| [A] | [how] | [cost] | [what] |
| [B] | [how] | [cost] | [what] |
## Will do and will not do
- Will do: [list] | Will not do: [list]
## Escalation route
**Trigger:** [observable event, date] | **To:** [lowest role with authority] | **Note:** [facts, impact, decision needed]
## If the decision goes the other way
[Where the dissent is recorded, what you commit to, what goes to an adviser instead.]
## Decision
[Role with authority] chooses between the request and the alternatives by [date]; [designer] records the outcome and any dissent in the decision log the same day.
```

## Done When
- The request is quoted and its goal is stated or marked to confirm
- Every risk line carries evidence or a visible `[gap]`
- Two alternatives meet the requester's goal, each with its cost, and the trigger is something anyone could observe

## Quality Bar
- The brief is about the request and its effects, never the requester's character or motives
- Proportionate: the lowest authority that can resolve it, never a public pile-on
- Legal and regulatory points are questions that end "check with a qualified adviser"
- Claude states the risk from real evidence and never invents harm; the named decider makes the call and your dissent is recorded.

## Next
Run pdes-design-impact-writeup (Design Impact Write-Up) once the work has shipped, to report what it delivered.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
