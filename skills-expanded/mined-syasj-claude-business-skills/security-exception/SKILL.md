---
name: security-exception
description: "Record a security exception with an owner, an expiry, and a compensating control. Use when the user mentions security exception, risk acceptance, waive a control, temporary exception, or asks for a security exception record. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'security-exception' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Security Exception

Record a security exception with an owner, an expiry, and a compensating control.

## When to use this skill

Use this skill when the user:

- security exception
- risk acceptance
- waive a control
- temporary exception

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

- The control
- The reason
- The compensating step
- The requested duration

## Workflow


### 1. Step 1

State the control and the gap in one sentence.
### 2. Step 2

Require a business reason more specific than urgency, or record that the reason is weak.
### 3. Step 3

Name a compensating control that reduces the same harm.
### 4. Step 4

Set an owner and an expiry. No expiry, no exception.
### 5. Step 5

Note what will be true at review time.
### 6. Step 6

Refuse exceptions whose purpose is to hide an incident or deceive a customer or auditor.

## Output

Deliver a **security exception record**.

- Purpose of this security exception record, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a security exception record by 30 September 2026. A team wants to skip MFA forever because a vendor integration is inconvenient.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to skip MFA forever because a vendor integration is inconvenient.

The control: their one-page rule dated 2 Mar 2026. No exception log since
The reason: Access review Q3, recorded 14 September 2026. No supporting file attached
The compensating step: Access review Q3; Endpoint patch ring 2. Both unassigned as of 14 September 2026
The requested duration: Access review Q3, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Security exception record**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A time-boxed exception only if a compensating control exists, otherwise a refusal of the permanent waiver.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The control | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |
| The reason | Access review Q3, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The compensating step | Access review Q3; Endpoint patch ring 2. Both unassigned as of 14 September 2026 | Carried into the draft |
| The requested duration | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. State the control and the gap in one sentence**

**2. Require a business reason more specific than urgency, or record that the reason is weak**

**3. Name a compensating control that reduces the same harm**

**4. Set an owner and an expiry. No expiry, no exception**

**5. Note what will be true at review time**

**Deliberately not done**
- A permanent waiver.
- An exception used to hide an incident.
- No compensating control.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A permanent waiver
- An exception used to hide an incident
- No compensating control

## Related skills

- `policy-exception-log`
- `vulnerability-triage`
