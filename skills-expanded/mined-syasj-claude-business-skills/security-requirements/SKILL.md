---
name: security-requirements
description: "Write defensive security requirements for a feature so engineering can build controls without exploit instructions. Use when the user mentions security requirements, secure design requirements, what security does this need, abuse cases to defend, or asks for a security requirements. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'security-requirements' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Security Requirements

Write defensive security requirements for a feature so engineering can build controls without exploit instructions.

## When to use this skill

Use this skill when the user:

- security requirements
- secure design requirements
- what security does this need
- abuse cases to defend

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

- The feature and its data
- Actors
- Existing controls
- Sensitivity the user described

## Workflow


### 1. Step 1

List assets and actors in plain language.
### 2. Write requirements as observable controls

authenticate, authorize, log, limit, and protect data.
### 3. Include failure behavior

deny by default, and what the user sees.
### 4. Step 4

Map each requirement to a test the team can run safely, such as an authorized versus unauthorized check.
### 5. Step 5

Do not include exploit steps, payloads, or bypass instructions.
### 6. Step 6

Name the owner who accepts any requirement they choose to defer.

## Output

Deliver a **security requirements**.

- Purpose of this security requirements, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a security requirements by 30 September 2026. A new export feature has no statement about who may export customer data.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A new export feature has no statement about who may export customer data.

The feature and its data: Access review Q3, recorded 14 September 2026. No supporting file attached
Actors: Aisha Rahman plus two others named in the thread. No distribution list attached
Existing controls: their one-page rule dated 2 Mar 2026. No exception log since
Sensitivity the user described: Endpoint patch ring 2, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Security requirements**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Requirements for authorization, audit, and a safe allow-and-deny test, with no attack procedure.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The feature and its data | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Actors | Aisha Rahman plus two others named in the thread. No distribution list attached | Carried into the draft |
| Existing controls | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Sensitivity the user described | Endpoint patch ring 2, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. List assets and actors in plain language**

**2. Write requirements as observable controls**  
authenticate, authorize, log, limit, and protect data.

**3. Include failure behavior**  
deny by default, and what the user sees.

**4. Map each requirement to a test the team can run safely, such as an authorized versus unauthorized check**

**5. Do not include exploit steps, payloads, or bypass instructions**

**Deliberately not done**
- Exploit steps.
- A requirement list with no tests.
- Deferring auth with no owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Exploit steps
- A requirement list with no tests
- Deferring auth with no owner

## Related skills

- `threat-model-lite`
- `secure-code-review`
