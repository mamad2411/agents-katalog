---
name: rfp-response
description: "Decide whether to answer an RFP and, if yes, draft a response that is compliant, true, and selective. Use when the user mentions RFP response, RFI, security questionnaire narrative, bid response, or asks for a RFP response plan or draft. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'rfp-response' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# RFP Response

Decide whether to answer an RFP and, if yes, draft a response that is compliant, true, and selective.

## When to use this skill

Use this skill when the user:

- RFP response
- RFI
- security questionnaire narrative
- bid response

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

- The questions that matter
- Facts the company can support
- Deadline and submission rules
- Why this RFP is worth answering

## Workflow


### 1. Bid decision

If the mandatory requirements do not fit, recommend no-bid or a clarified exception. Do not fake compliance.
### 2. Answer the question

Each draft answer maps to a question. Do not paste a brochure over a yes-no item.
### 3. Evidence

Attach or cite only proof the user has. Unknowns stay unknown.
### 4. Exceptions

List exceptions visibly. Hidden exceptions are how bids are thrown out or, worse, how trust is lost.
### 5. Owners

Security, legal, and product own their answers. Do not let sales improvise a security claim.
### 6. Submit checklist

Format, deadline, and signatures the user confirmed. Do not invent a portal workaround.

## Output

Deliver a **RFP response plan or draft**.

- Purpose of this RFP response plan or draft, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a RFP response plan or draft by 30 September 2026. An RFP asks for a certification the company has not achieved and sales wants to answer 'yes, in progress' in the yes box.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

An RFP asks for a certification the company has not achieved and sales wants to answer 'yes, in progress' in the yes box.

The questions that matter: An RFP asks for a certification the company has not achieved and sales wants to answer 'yes, in progress' in the yes box
Facts the company can support: Cedar Clinic and one other, both unconfirmed as of 14 September 2026
Deadline and submission rules: 30 September 2026
Why this RFP is worth answering: An RFP asks for a certification the company has not achieved and sales wants to answer 'yes, in progress' in the yes box
```

### Example outcome

**Rfp response plan or draft**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Answers no or exception, explains the in-progress status outside the yes box, and flags a no-bid choice if the item is mandatory.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The questions that matter | An RFP asks for a certification the company has not achieved and sales wants to answer 'yes, in progress' in the yes box | Needs confirmation |
| Facts the company can support | Cedar Clinic and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Deadline and submission rules | 30 September 2026 | Carried into the draft |
| Why this RFP is worth answering | An RFP asks for a certification the company has not achieved and sales wants to answer 'yes, in progress' in the yes box | Needs confirmation |

**How this draft was built**

**1. Bid decision**  
If the mandatory requirements do not fit, recommend no-bid or a clarified exception. Do not fake compliance.

**2. Answer the question**  
Each draft answer maps to a question. Do not paste a brochure over a yes-no item.

**3. Evidence**  
Attach or cite only proof the user has. Unknowns stay unknown.

**4. Exceptions**  
List exceptions visibly. Hidden exceptions are how bids are thrown out or, worse, how trust is lost.

**5. Owners**  
Security, legal, and product own their answers. Do not let sales improvise a security claim.

**Deliberately not done**
- Claiming a certification the company does not have.
- A brochure pasted over every question.
- Hidden exceptions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Claiming a certification the company does not have.
- A brochure pasted over every question.
- Hidden exceptions.

## Related skills

- `vendor-security-review`
- `proposal-writer`
