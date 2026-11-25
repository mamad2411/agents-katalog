---
name: threat-model-lite
description: "Sketch a defensive threat model for a feature: assets, actors, abuses, and controls. No exploit steps. Use when the user mentions threat model, what could go wrong security, abuse cases, security design review, or asks for a threat model note. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'threat-model-lite' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Lightweight Threat Model

Sketch a defensive threat model for a feature: assets, actors, abuses, and controls. No exploit steps.

## When to use this skill

Use this skill when the user:

- threat model
- what could go wrong security
- abuse cases
- security design review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The feature and its assets
- Actors
- Existing controls
- Data sensitivity they described

## Workflow


### 1. Assets

What must be protected: credentials, personal data, money, or availability, as they described.
### 2. Actors

Users, admins, and unauthenticated callers. Do not build a persona of a criminal how-to.
### 3. Abuses

What could go wrong in plain language, such as unauthorized access or tampering. No payloads, bypasses, or step-by-step intrusion.
### 4. Controls

Preventive and detective controls they can implement. Prefer known controls over novel tricks.
### 5. Gaps

The abuse with no control. That is the work list.
### 6. Hand-off

Residual risk is accepted by a named owner or sent to the security skill for review. This note is not a penetration test.

## Output

Deliver a **threat model note**.

- Purpose of this threat model note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a threat model note by 30 September 2026. A file-sharing feature has no answer for who can access a link.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A file-sharing feature has no answer for who can access a link.

The feature and its assets: Checkout service, recorded 14 September 2026. No supporting file attached
Actors: Aisha Rahman plus two others named in the thread. No distribution list attached
Existing controls: their one-page rule dated 2 Mar 2026. No exception log since
Data sensitivity they described: Checkout service. Partly documented: the what is written down, the who is not
```

### Example outcome

**Threat model note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Lists unauthorized access as a gap, recommends an access control and audit event, and includes no exploit procedure.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The feature and its assets | Checkout service, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Actors | Aisha Rahman plus two others named in the thread. No distribution list attached | Carried into the draft |
| Existing controls | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Data sensitivity they described | Checkout service. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Assets**  
What must be protected: credentials, personal data, money, or availability, as they described.

**2. Actors**  
Users, admins, and unauthenticated callers. Do not build a persona of a criminal how-to.

**3. Abuses**  
What could go wrong in plain language, such as unauthorized access or tampering. No payloads, bypasses, or step-by-step intrusion.

**4. Controls**  
Preventive and detective controls they can implement. Prefer known controls over novel tricks.

**5. Gaps**  
The abuse with no control. That is the work list.

**Deliberately not done**
- Exploit steps or payloads.
- A model with no assets.
- Claiming the feature is secure because the note exists.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Exploit steps or payloads.
- A model with no assets.
- Claiming the feature is secure because the note exists.

## Related skills

- `security-requirements`
- `secure-code-review`
