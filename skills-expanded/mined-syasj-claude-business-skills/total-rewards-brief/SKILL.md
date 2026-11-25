---
name: total-rewards-brief
description: "Explain a person's total rewards in plain language using only components the company actually offers. Use when the user mentions total rewards, benefits explanation, comp statement, rewards brief, or asks for a total rewards brief. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'total-rewards-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Total Rewards Brief

Explain a person's total rewards in plain language using only components the company actually offers.

## When to use this skill

Use this skill when the user:

- total rewards
- benefits explanation
- comp statement
- rewards brief

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

- Components the company offers
- The person's eligible parts
- What must not be promised
- Questions employees keep asking

## Workflow


### 1. List real components

Pay, variable, time off, and benefits they confirmed. Do not add perks from other companies.
### 2. Separate guaranteed from variable

A bonus target is not a promise unless they say it is guaranteed.
### 3. Equity

Describe it only to the extent they explained vesting and value. Do not invent a share price.
### 4. Plain language

Write the explanation an employee can read without a glossary.
### 5. Questions

Answer only what policy answers. The rest go to HR. Do not give tax advice on benefits.
### 6. Privacy

Do not include another employee's pay in the brief.

## Output

Deliver a **total rewards brief**.

- Purpose of this total rewards brief, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a total rewards brief by 30 September 2026. Employees think the target bonus is guaranteed because the offer conversation was casual.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Employees think the target bonus is guaranteed because the offer conversation was casual.

Components the company offers: CAD 120, dates not set, cap not set
The person's eligible parts: Jordan Hale, recorded 14 September 2026. No supporting file attached
What must not be promised: none written down beyond the ask
Questions employees keep asking: Employees think the target bonus is guaranteed because the offer conversation was casual
```

### Example outcome

**Total rewards brief**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the target as variable, lists only real benefits, and sends tax questions to a qualified advisor.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Components the company offers | CAD 120, dates not set, cap not set | Needs confirmation |
| The person's eligible parts | Jordan Hale, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| What must not be promised | none written down beyond the ask | Carried into the draft |
| Questions employees keep asking | Employees think the target bonus is guaranteed because the offer conversation was casual | Needs confirmation |

**How this draft was built**

**1. List real components**  
Pay, variable, time off, and benefits they confirmed. Do not add perks from other companies.

**2. Separate guaranteed from variable**  
A bonus target is not a promise unless they say it is guaranteed.

**3. Equity**  
Describe it only to the extent they explained vesting and value. Do not invent a share price.

**4. Plain language**  
Write the explanation an employee can read without a glossary.

**5. Questions**  
Answer only what policy answers. The rest go to HR. Do not give tax advice on benefits.

**Deliberately not done**
- Implied guarantees.
- Invented share prices.
- Tax advice on benefits.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Implied guarantees.
- Invented share prices.
- Tax advice on benefits.

## Related skills

- `compensation-band`
- `offer-letter-checklist`
- `handbook-policy-draft`
