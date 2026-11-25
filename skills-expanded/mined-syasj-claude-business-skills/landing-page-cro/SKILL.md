---
name: landing-page-cro
description: "Review a landing page for clarity, proof, and the single action, without dark patterns. Use when the user mentions landing page, conversion review, homepage critique, CRO review, or asks for a landing page review. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'landing-page-cro' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Landing Page Review

Review a landing page for clarity, proof, and the single action, without dark patterns.

## When to use this skill

Use this skill when the user:

- landing page
- conversion review
- homepage critique
- CRO review

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

- The page copy or a description
- The audience
- The action
- Proof available

## Workflow


### 1. First screen

Can a stranger see who it is for, what it does, and what to do. If not, that is the finding.
### 2. One action

Competing buttons are a finding. Recommend a primary action.
### 3. Proof near claims

A claim without nearby proof is a rewrite, not a design tweak.
### 4. Friction

Forms ask only for what the next step needs. Do not ask for sensitive data to download a brochure.
### 5. Dark patterns

Refuse fake countdowns, hidden costs, and confirm-shaming. Offer an honest alternative.
### 6. Test

If the user wants a test, define one change and the success event. Do not test five things at once.

## Output

Deliver a **landing page review**.

- Purpose of this landing page review, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a landing page review by 30 September 2026. A page has a countdown timer that resets every visit and three equal buttons.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A page has a countdown timer that resets every visit and three equal buttons.

The page copy or a description: Fall service page, recorded 14 September 2026. No supporting file attached
The audience: people who already buy from Fieldnote
The action: Fall service page; Email to lapsed buyers. Both unassigned as of 14 September 2026
Proof available: one customer email, 14 September 2026, no attachment beyond that
```

### Example outcome

**Landing page review**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the fake timer, picks one action, and pairs the main claim with real proof or deletes the claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The page copy or a description | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The audience | people who already buy from Fieldnote | Carried into the draft |
| The action | Fall service page; Email to lapsed buyers. Both unassigned as of 14 September 2026 | Carried into the draft |
| Proof available | one customer email, 14 September 2026, no attachment beyond that | Needs confirmation |

**How this draft was built**

**1. First screen**  
Can a stranger see who it is for, what it does, and what to do. If not, that is the finding.

**2. One action**  
Competing buttons are a finding. Recommend a primary action.

**3. Proof near claims**  
A claim without nearby proof is a rewrite, not a design tweak.

**4. Friction**  
Forms ask only for what the next step needs. Do not ask for sensitive data to download a brochure.

**5. Dark patterns**  
Refuse fake countdowns, hidden costs, and confirm-shaming. Offer an honest alternative.

**Deliberately not done**
- Fake scarcity.
- A page with three primary actions.
- Asking for payment card data in a contact form.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fake scarcity.
- A page with three primary actions.
- Asking for payment card data in a contact form.

## Related skills

- `marketing-claims-review`
- `marketing-experiment`
