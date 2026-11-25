---
name: campaign-brief
description: "Brief a campaign with one audience, one offer, one action, and a measurement plan. Use when the user mentions campaign brief, marketing campaign, campaign plan, launch campaign, or asks for a campaign brief. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'campaign-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Campaign Brief

Brief a campaign with one audience, one offer, one action, and a measurement plan.

## When to use this skill

Use this skill when the user:

- campaign brief
- marketing campaign
- campaign plan
- launch campaign

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The audience
- The offer
- The action you want
- Budget and channel constraints

## Workflow


### 1. One audience

Describe them by situation, not by a vague demographic alone.
### 2. One offer

What they get if they act. Multiple offers split the brief.
### 3. Insight

Why this audience would care now, using evidence the user has. Mark assumptions.
### 4. Channels

Only channels the team can staff. A channel list is not a plan.
### 5. Measurement

The action that counts, the baseline if known, and the date of the readout.
### 6. Claims

Point every factual claim at the claims review. Do not invent urgency.

## Output

Deliver a **campaign brief**.

- Purpose of this campaign brief, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a campaign brief by 30 September 2026. A team wants a campaign for 'awareness' with six channels and no offer.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants a campaign for 'awareness' with six channels and no offer.

The audience: people who already buy from Fieldnote
The offer: CAD 120, dates not set, cap not set
The action you want: Fall service page; Email to lapsed buyers. Both unassigned as of 14 September 2026
Budget and channel constraints: CAD 180,000 available. Not a signed plan
```

### Example outcome

**Campaign brief**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Forces one audience, one offer, staffed channels, and a readout date.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The audience | people who already buy from Fieldnote | Needs confirmation |
| The offer | CAD 120, dates not set, cap not set | Carried into the draft |
| The action you want | Fall service page; Email to lapsed buyers. Both unassigned as of 14 September 2026 | Carried into the draft |
| Budget and channel constraints | CAD 180,000 available. Not a signed plan | Needs confirmation |

**How this draft was built**

**1. One audience**  
Describe them by situation, not by a vague demographic alone.

**2. One offer**  
What they get if they act. Multiple offers split the brief.

**3. Insight**  
Why this audience would care now, using evidence the user has. Mark assumptions.

**4. Channels**  
Only channels the team can staff. A channel list is not a plan.

**5. Measurement**  
The action that counts, the baseline if known, and the date of the readout.

**Deliberately not done**
- Five audiences in one brief.
- Vanity metrics as the goal.
- Fake deadlines.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Five audiences in one brief.
- Vanity metrics as the goal.
- Fake deadlines.

## Related skills

- `marketing-experiment`
- `creative-brief`
