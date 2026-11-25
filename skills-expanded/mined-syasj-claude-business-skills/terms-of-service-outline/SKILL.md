---
name: terms-of-service-outline
description: "Outline customer terms from the product's actual behavior so counsel can draft, not the other way around. Use when the user mentions terms of service, customer terms outline, SaaS terms, user agreement outline, or asks for a terms of service outline. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'terms-of-service-outline' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Terms of Service Outline

Outline customer terms from the product's actual behavior so counsel can draft, not the other way around.

## When to use this skill

Use this skill when the user:

- terms of service
- customer terms outline
- SaaS terms
- user agreement outline

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What the customer buys
- How they accept terms
- Limits the product really has
- Support and uptime promises marketing already makes

## Workflow


### 1. Describe the service

What a customer can and cannot do, from product facts. Do not copy a famous company's terms.
### 2. Acceptance

Where the user says acceptance happens. If the product has no acceptance moment, flag that as a product gap.
### 3. Promises

List uptime, support, or outcome claims marketing already makes. Terms that contradict the website are a finding.
### 4. Customer duties

Acceptable use, accounts, and payment, in plain language. No hidden punitive clause the business did not ask for.
### 5. Liability and termination

Note that counsel must draft these for the jurisdiction. Provide the commercial intent only.
### 6. Banner the draft

Not for publication. Counsel writes the operative terms.

## Output

Deliver a **terms of service outline**.

- Purpose of this terms of service outline, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a terms of service outline by 30 September 2026. Marketing promises a 99.9 percent uptime on the homepage, and the product team has no status page or credit policy.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Marketing promises a 99.9 percent uptime on the homepage, and the product team has no status page or credit policy.

What the customer buys: Vendor terms, last reviewed 14 September 2026. No owner named since
How they accept terms: Contractor NDA, last reviewed 14 September 2026. No owner named since
Limits the product really has: Vendor terms. Stated in the ask, not documented anywhere else
Support and uptime promises marketing already makes: none written down beyond the ask
```

### Example outcome

**Terms of service outline**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag the homepage promise as a term that counsel and product must either support or remove.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What the customer buys | Vendor terms, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| How they accept terms | Contractor NDA, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Limits the product really has | Vendor terms. Stated in the ask, not documented anywhere else | Carried into the draft |
| Support and uptime promises marketing already makes | none written down beyond the ask | Needs confirmation |

**How this draft was built**

**1. Describe the service**  
What a customer can and cannot do, from product facts. Do not copy a famous company's terms.

**2. Acceptance**  
Where the user says acceptance happens. If the product has no acceptance moment, flag that as a product gap.

**3. Promises**  
List uptime, support, or outcome claims marketing already makes. Terms that contradict the website are a finding.

**4. Customer duties**  
Acceptable use, accounts, and payment, in plain language. No hidden punitive clause the business did not ask for.

**5. Liability and termination**  
Note that counsel must draft these for the jurisdiction. Provide the commercial intent only.

**Deliberately not done**
- Pasting another company's terms.
- Contradicting a published marketing promise without saying so.
- Calling the outline a finished agreement.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Pasting another company's terms.
- Contradicting a published marketing promise without saying so.
- Calling the outline a finished agreement.

## Related skills

- `marketing-claims-review`
- `privacy-notice-draft`
- `vendor-contract-playbook`
