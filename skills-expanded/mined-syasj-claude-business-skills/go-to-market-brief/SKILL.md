---
name: go-to-market-brief
description: "Brief a launch or a new motion so sales, product, and marketing are aiming at the same buyer and offer. Use when the user mentions go to market, GTM brief, launch motion, how do we take this to market, or asks for a go-to-market brief. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'go-to-market-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Go-to-Market Brief

Brief a launch or a new motion so sales, product, and marketing are aiming at the same buyer and offer.

## When to use this skill

Use this skill when the user:

- go to market
- GTM brief
- launch motion
- how do we take this to market

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

- The offer
- The buyer and the trigger event
- The channel the team can actually staff
- The date and the success signal

## Workflow


### 1. Define the buyer

One primary buyer. Secondary audiences are noted, not given equal weight.
### 2. State the offer

What they buy, what is out of the box, and what problem it solves this quarter.
### 3. Pick a channel

Recommend the channel the team can staff now. A multi-channel plan with no owners is a poster.
### 4. Align enablement

What sales needs to say, what marketing must not claim, and what product must be true on day one.
### 5. Set a learning window

The first 30 or 60 days are a test. Name the number that would stop the motion.
### 6. Name gaps

Pricing, legal, support, or proof that is not ready. Do not launch those gaps into silence.

## Output

Deliver a **go-to-market brief**.

- Purpose of this go-to-market brief, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a go-to-market brief by 30 September 2026. A product is ready for a design-partner release and the teams disagree on who the buyer is.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A product is ready for a design-partner release and the teams disagree on who the buyer is.

The offer: CAD 49, dates not set, cap not set
The buyer and the trigger event: Kite Freight, recorded 14 September 2026. No supporting file attached
The channel the team can actually staff: two people on shift, one off
The date and the success signal: 30 September 2026
```

### Example outcome

**Go-to-market brief**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A brief with one buyer, one staffed channel, enablement limits, and a 60-day kill metric.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offer | CAD 49, dates not set, cap not set | Needs confirmation |
| The buyer and the trigger event | Kite Freight, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The channel the team can actually staff | two people on shift, one off | Carried into the draft |
| The date and the success signal | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Define the buyer**  
One primary buyer. Secondary audiences are noted, not given equal weight.

**2. State the offer**  
What they buy, what is out of the box, and what problem it solves this quarter.

**3. Pick a channel**  
Recommend the channel the team can staff now. A multi-channel plan with no owners is a poster.

**4. Align enablement**  
What sales needs to say, what marketing must not claim, and what product must be true on day one.

**5. Set a learning window**  
The first 30 or 60 days are a test. Name the number that would stop the motion.

**Deliberately not done**
- A GTM plan that is only a channel list.
- Claims marketing cannot support.
- No kill metric.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A GTM plan that is only a channel list.
- Claims marketing cannot support.
- No kill metric.

## Related skills

- `launch-plan`
- `positioning-statement`
- `sales-playbook`
