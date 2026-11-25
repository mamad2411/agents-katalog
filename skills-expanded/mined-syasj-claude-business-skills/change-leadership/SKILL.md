---
name: change-leadership
description: "Plan how a specific change will be adopted, including who loses something and how you will support them. Use when the user mentions change management, rollout to the org, people side of change, adoption plan, or asks for a change adoption plan. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'change-leadership' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Change Leadership

Plan how a specific change will be adopted, including who loses something and how you will support them.

## When to use this skill

Use this skill when the user:

- change management
- rollout to the org
- people side of change
- adoption plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The change in concrete terms
- Who must work differently
- What they lose or must learn
- Sponsor and timing

## Workflow


### 1. Describe the change in behavior

What will a specific person do differently on a Tuesday. If you cannot say, the change is not defined.
### 2. Name losses

Status, skill, convenience, or headcount effects the user has acknowledged. Do not pretend a hard change is only upside.
### 3. Pick sponsors

A sponsor who will not repeat the message is not a sponsor. Recommend a cadence of visible reinforcement.
### 4. Support the middle

Managers need a script, a FAQ grounded in decisions already made, and a way to raise exceptions.
### 5. Measure adoption

Choose one or two observable behaviors, not a survey score alone.
### 6. Plan resistance

Treat resistance as information. Design a channel for it. Do not draft ways to punish questions.

## Output

Deliver a **change adoption plan**.

- Purpose of this change adoption plan, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Mara Chen, founder at Northline Studio in Calgary, needs a change adoption plan by 30 September 2026. Finance is moving the company from monthly spreadsheets to a shared close calendar and managers are ignoring it.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Finance is moving the company from monthly spreadsheets to a shared close calendar and managers are ignoring it.

The change in concrete terms: requested 14 September 2026. Not yet approved
Who must work differently: Mara Chen, founder
What they lose or must learn: Finance is moving the company from monthly spreadsheets to a shared close calendar and managers are ignoring it
Sponsor and timing: open item, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Change adoption plan**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names Tuesday behaviors, manager support, the loss of local flexibility, and one observable adoption metric.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change in concrete terms | requested 14 September 2026. Not yet approved | Needs confirmation |
| Who must work differently | Mara Chen, founder | Carried into the draft |
| What they lose or must learn | Finance is moving the company from monthly spreadsheets to a shared close calendar and managers are ignoring it | Carried into the draft |
| Sponsor and timing | open item, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Describe the change in behavior**  
What will a specific person do differently on a Tuesday. If you cannot say, the change is not defined.

**2. Name losses**  
Status, skill, convenience, or headcount effects the user has acknowledged. Do not pretend a hard change is only upside.

**3. Pick sponsors**  
A sponsor who will not repeat the message is not a sponsor. Recommend a cadence of visible reinforcement.

**4. Support the middle**  
Managers need a script, a FAQ grounded in decisions already made, and a way to raise exceptions.

**5. Measure adoption**  
Choose one or two observable behaviors, not a survey score alone.

**Deliberately not done**
- A change plan that is only a slide about urgency.
- Hiding job impact.
- Measuring adoption with a single enthusiasm survey.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A change plan that is only a slide about urgency.
- Hiding job impact.
- Measuring adoption with a single enthusiasm survey.

## Related skills

- `stakeholder-map`
- `internal-comms-plan`
- `operating-cadence`
