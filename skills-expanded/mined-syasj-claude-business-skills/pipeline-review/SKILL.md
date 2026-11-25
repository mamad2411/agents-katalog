---
name: pipeline-review
description: "Review a pipeline so stages mean evidence, and stuck deals get a next action or an exit. Use when the user mentions pipeline review, stalled deals, stage hygiene, sales inspection, or asks for a pipeline review. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pipeline-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pipeline Review

Review a pipeline so stages mean evidence, and stuck deals get a next action or an exit.

## When to use this skill

Use this skill when the user:

- pipeline review
- stalled deals
- stage hygiene
- sales inspection

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The opportunity list with stages and ages
- The stage definitions
- The seller's stated next steps
- The period being forecast

## Workflow


### 1. Check definitions

A stage without an evidence requirement is a label. Say so.
### 2. Age

Deals older than the user's threshold need a reason to stay. No reason, recommend exit.
### 3. Next step quality

A next step has a date and a buyer action. 'Follow up' is not a next step.
### 4. Concentration

Note if the number depends on one deal. Do not hide concentration to make the team look diversified.
### 5. Hygiene actions

Advance, rewind, or remove. Rewinding is healthy.
### 6. Coaching point

One skill to practice, based on the pattern in the list, not a lecture on attitude.

## Output

Deliver a **pipeline review**.

- Purpose of this pipeline review, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a pipeline review by 30 September 2026. A pipeline has 30 opportunities and 18 have no dated next step.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A pipeline has 30 opportunities and 18 have no dated next step.

The opportunity list with stages and ages: Harbor Goods; Cedar Clinic; Redline Parts
The stage definitions: Harbor Goods, recorded 14 September 2026. No supporting file attached
The seller's stated next steps: Harbor Goods; Cedar Clinic. Both unassigned as of 14 September 2026
The period being forecast: month ending 14 September 2026
```

### Example outcome

**Pipeline review**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Rewinds or removes undated deals and names one coaching point about buyer-owned next steps.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The opportunity list with stages and ages | Harbor Goods; Cedar Clinic; Redline Parts | Needs confirmation |
| The stage definitions | Harbor Goods, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The seller's stated next steps | Harbor Goods; Cedar Clinic. Both unassigned as of 14 September 2026 | Carried into the draft |
| The period being forecast | month ending 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Check definitions**  
A stage without an evidence requirement is a label. Say so.

**2. Age**  
Deals older than the user's threshold need a reason to stay. No reason, recommend exit.

**3. Next step quality**  
A next step has a date and a buyer action. 'Follow up' is not a next step.

**4. Concentration**  
Note if the number depends on one deal. Do not hide concentration to make the team look diversified.

**5. Hygiene actions**  
Advance, rewind, or remove. Rewinding is healthy.

**Deliberately not done**
- Leaving zombie deals because removing them hurts the chart.
- Next steps with no buyer action.
- Changing stage definitions mid-meeting to save a forecast.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Leaving zombie deals because removing them hurts the chart.
- Next steps with no buyer action.
- Changing stage definitions mid-meeting to save a forecast.

## Related skills

- `forecast-call`
- `qualification-meddic`
