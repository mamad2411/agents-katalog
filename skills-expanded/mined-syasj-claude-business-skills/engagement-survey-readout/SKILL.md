---
name: engagement-survey-readout
description: "Turn survey results the user provides into a few actions, without over-reading small slices. Use when the user mentions engagement survey, survey readout, employee survey results, eNPS results, or asks for a survey readout. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'engagement-survey-readout' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Engagement Survey Readout

Turn survey results the user provides into a few actions, without over-reading small slices.

## When to use this skill

Use this skill when the user:

- engagement survey
- survey readout
- employee survey results
- eNPS results

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The results they have
- Response rate and slice sizes
- Last cycle's actions
- What leadership can actually change

## Workflow


### 1. Lead with response quality

A slice with a tiny response rate is a hint, not a verdict. Say so.
### 2. Pick three movements

Up, down, or stuck, compared with their prior survey if they have one. No prior, no fake trend.
### 3. Pair scores with comments only if comments were provided

Do not invent themes.
### 4. Choose actions inside their power

One management habit and one system fix. A poster about values is not an action.
### 5. Close the loop

What employees will be told, by when. Asking for feedback and going silent is the failure mode.
### 6. Privacy

Do not identify a commenter from a small team. Aggregate or suppress.

## Output

Deliver a **survey readout**.

- Purpose of this survey readout, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a survey readout by 30 September 2026. A 12-person team had a low score and three comments, and a leader wants to name the complainer.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A 12-person team had a low score and three comments, and a leader wants to name the complainer.

The results they have: Jordan Hale, recorded 14 September 2026. No supporting file attached
Response rate and slice sizes: 40 in the last period. No prior period attached, so no trend
Last cycle's actions: Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026
What leadership can actually change: requested 14 September 2026. Not yet approved
```

### Example outcome

**Survey readout**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses identification, treats the sample carefully, and proposes one owned action plus a close-the-loop message.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The results they have | Jordan Hale, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Response rate and slice sizes | 40 in the last period. No prior period attached, so no trend | Carried into the draft |
| Last cycle's actions | Jordan Hale; Sam Okonkwo. Both unassigned as of 14 September 2026 | Carried into the draft |
| What leadership can actually change | requested 14 September 2026. Not yet approved | Needs confirmation |

**How this draft was built**

**1. Lead with response quality**  
A slice with a tiny response rate is a hint, not a verdict. Say so.

**2. Pick three movements**  
Up, down, or stuck, compared with their prior survey if they have one. No prior, no fake trend.

**3. Pair scores with comments only if comments were provided**  
Do not invent themes.

**4. Choose actions inside their power**  
One management habit and one system fix. A poster about values is not an action.

**5. Close the loop**  
What employees will be told, by when. Asking for feedback and going silent is the failure mode.

**Deliberately not done**
- Ranking managers from tiny samples.
- Identifying a commenter.
- A long list of actions nobody owns.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Ranking managers from tiny samples.
- Identifying a commenter.
- A long list of actions nobody owns.

## Related skills

- `stay-interview`
- `culture-diagnostic`
- `manager-one-on-one`
