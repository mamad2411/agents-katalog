---
name: identity-hardening
description: "Plan identity hardening around administrators, joiners and leavers, and phishing-resistant sign-in where they can support it. Use when the user mentions identity hardening, MFA rollout, admin access, joiner leaver identity, or asks for a identity hardening plan. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'identity-hardening' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Identity Hardening

Plan identity hardening around administrators, joiners and leavers, and phishing-resistant sign-in where they can support it.

## When to use this skill

Use this skill when the user:

- identity hardening
- MFA rollout
- admin access
- joiner leaver identity

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Defensive use only. Do not write exploits, payloads, bypasses, malware, or intrusion steps. Describe controls, ownership, detection, and safe verification.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The identity provider they use
- Who has admin
- Joiner and leaver process
- Exceptions they know about

## Workflow


### 1. Step 1

Start with admins and remote access, not with a poster about passwords.
### 2. Step 2

Map joiner, mover, and leaver to access changes. A leaver delay is a finding.
### 3. Step 3

Recommend phishing-resistant factors if their provider supports them, as a question, not a product pitch.
### 4. Step 4

Shared accounts are replaced or given a named owner and a review date.
### 5. Step 5

Exceptions get an expiry.
### 6. Step 6

Do not ask for one-time codes or passwords to implement the plan.

## Output

Deliver a **identity hardening plan**.

- Purpose of this identity hardening plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an identity hardening plan by 30 September 2026. Contractors keep admin access for months after the contract ends.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Contractors keep admin access for months after the contract ends.

The identity provider they use: Access review Q3, recorded 14 September 2026. No supporting file attached
Who has admin: Aisha Rahman, engineering lead
Joiner and leaver process: email to Aisha Rahman. No written steps after 1 Sep 2026
Exceptions they know about: Access review Q3 is open. Endpoint patch ring 2 was raised verbally and never logged
```

### Example outcome

**Identity hardening plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Ties leaver dates to access removal and refuses any request for live codes.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The identity provider they use | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Who has admin | Aisha Rahman, engineering lead | Carried into the draft |
| Joiner and leaver process | email to Aisha Rahman. No written steps after 1 Sep 2026 | Carried into the draft |
| Exceptions they know about | Access review Q3 is open. Endpoint patch ring 2 was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. Start with admins and remote access, not with a poster about passwords**

**2. Map joiner, mover, and leaver to access changes. A leaver delay is a finding**

**3. Recommend phishing-resistant factors if their provider supports them, as a question, not a product pitch**

**4. Shared accounts are replaced or given a named owner and a review date**

**5. Exceptions get an expiry**

**Deliberately not done**
- Asking for one-time codes.
- A plan that ignores leavers.
- Permanent exceptions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Asking for one-time codes
- A plan that ignores leavers
- Permanent exceptions

## Related skills

- `access-review`
- `offboarding-checklist`
