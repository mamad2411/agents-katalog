---
name: paid-media-brief
description: "Brief paid media with an offer, an audience hypothesis, a spend cap, and a stop rule. Use when the user mentions paid media, ads brief, paid social, search ads brief, or asks for a paid media brief. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'paid-media-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Paid Media Brief

Brief paid media with an offer, an audience hypothesis, a spend cap, and a stop rule.

## When to use this skill

Use this skill when the user:

- paid media
- ads brief
- paid social
- search ads brief

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

- The offer
- The audience hypothesis
- Spend cap
- The conversion event that matters

## Workflow


### 1. Offer

The ad promises only what the landing page delivers. Mismatch is a finding.
### 2. Audience

A hypothesis, labeled as such. Do not invent performance data.
### 3. Creative claims

Every claim must be supportable. No fake urgency.
### 4. Measurement

The event that counts, and the minimum data needed before anyone declares a winner.
### 5. Stop rule

The spend or result that pauses the test. Hope is not a stop rule.
### 6. Landing page

Point to the page review if the page is not ready. Do not buy traffic to a confused page.

## Output

Deliver a **paid media brief**.

- Purpose of this paid media brief, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a paid media brief by 30 September 2026. A team wants to scale spend after 12 clicks because one ad 'feels better'.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to scale spend after 12 clicks because one ad 'feels better'.

The offer: CAD 49, dates not set, cap not set
The audience hypothesis: people who already buy from Fieldnote
Spend cap: Email to lapsed buyers, recorded 14 September 2026. No supporting file attached
The conversion event that matters: Fall service page, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Paid media brief**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A brief with a stop rule and a minimum evidence line before scale, plus a claim check against the page.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offer | CAD 49, dates not set, cap not set | Needs confirmation |
| The audience hypothesis | people who already buy from Fieldnote | Carried into the draft |
| Spend cap | Email to lapsed buyers, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The conversion event that matters | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Offer**  
The ad promises only what the landing page delivers. Mismatch is a finding.

**2. Audience**  
A hypothesis, labeled as such. Do not invent performance data.

**3. Creative claims**  
Every claim must be supportable. No fake urgency.

**4. Measurement**  
The event that counts, and the minimum data needed before anyone declares a winner.

**5. Stop rule**  
The spend or result that pauses the test. Hope is not a stop rule.

**Deliberately not done**
- Ads that overpromise the page.
- No stop rule.
- Declaring a winner on a handful of clicks.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Ads that overpromise the page.
- No stop rule.
- Declaring a winner on a handful of clicks.

## Related skills

- `landing-page-cro`
- `marketing-experiment`
