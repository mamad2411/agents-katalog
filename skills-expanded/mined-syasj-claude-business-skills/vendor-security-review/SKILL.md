---
name: vendor-security-review
description: "Review a vendor's security claims against the data you will share, without granting a fake certification. Use when the user mentions vendor security review, security questionnaire, third party security, vendor due diligence, or asks for a vendor security review. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'vendor-security-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Vendor Security Review

Review a vendor's security claims against the data you will share, without granting a fake certification.

## When to use this skill

Use this skill when the user:

- vendor security review
- security questionnaire
- third party security
- vendor due diligence

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

- The data the vendor will see
- Their claims and documents
- The use case
- The deadline

## Workflow


### 1. Step 1

Start from the data shared and the harm if it leaks.
### 2. Step 2

Compare their claims to the questions that matter for that data. A badge is not a review.
### 3. Step 3

Mark unanswered questions as gaps, not as passes.
### 4. Step 4

Recommend accept, accept with limits, or reject for this use. You cannot certify the vendor.
### 5. Note contract asks for counsel

breach notice, deletion, and subprocessors. Do not invent legal conclusions.
### 6. Step 6

Do not ask the vendor or the user for passwords to 'verify' controls.

## Output

Deliver a **vendor security review**.

- Purpose of this vendor security review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a vendor security review by 30 September 2026. A team wants to send customer files to a tool because its website says 'enterprise grade'.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to send customer files to a tool because its website says 'enterprise grade'.

The data the vendor will see: Access review Q3, recorded 14 September 2026. No supporting file attached
Their claims and documents: one PDF, 2 pages, dated 14 September 2026
The use case: Access review Q3, recorded 14 September 2026. No supporting file attached
The deadline: 30 September 2026
```

### Example outcome

**Vendor security review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Lists unanswered questions and refuses to treat the slogan as a control.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The data the vendor will see | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Their claims and documents | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The use case | Access review Q3, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The deadline | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Start from the data shared and the harm if it leaks**

**2. Compare their claims to the questions that matter for that data. A badge is not a review**

**3. Mark unanswered questions as gaps, not as passes**

**4. Recommend accept, accept with limits, or reject for this use. You cannot certify the vendor**

**5. Note contract asks for counsel**  
breach notice, deletion, and subprocessors. Do not invent legal conclusions.

**Deliberately not done**
- Treating a logo as a certification.
- A pass on unanswered questions.
- Asking for vendor passwords.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Treating a logo as a certification
- A pass on unanswered questions
- Asking for vendor passwords

## Related skills

- `third-party-risk`
- `data-processing-addendum`
