---
name: access-review
description: "Review who has access to a sensitive system and remove access that no longer has a reason. Use when the user mentions access review, user access review, who has admin, recertify access, or asks for a access review. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'access-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Access Review

Review who has access to a sensitive system and remove access that no longer has a reason.

## When to use this skill

Use this skill when the user:

- access review
- user access review
- who has admin
- recertify access

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

- The system
- The access list they exported
- The roles that are still justified
- Leavers they know about

## Workflow


### 1. Step 1

Start from an export they provide. Do not ask for passwords to go look.
### 2. Step 2

Flag leavers, shared accounts, and standing admin with no named owner.
### 3. Step 3

Ask for a business reason for each high privilege. No reason, recommend removal.
### 4. Step 4

Shared logins are a finding. Recommend individual accounts.
### 5. Step 5

Record who approved the remaining access and the next review date.
### 6. Step 6

Do not disable accounts yourself. Hand the change list to the owner.

## Output

Deliver a **access review**.

- Purpose of this access review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an access review by 30 September 2026. A shared admin login is still used after three people left the company.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A shared admin login is still used after three people left the company.

The system: the one named in the ask. Version and owner not recorded
The access list they exported: Access review Q3; Endpoint patch ring 2; Phishing report 4412
The roles that are still justified: Aisha Rahman plus two others named in the thread. No distribution list attached
Leavers they know about: Phishing report 4412 and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Access review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Recommends unique accounts, lists the leavers for removal, and does not request the shared password.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The system | the one named in the ask. Version and owner not recorded | Needs confirmation |
| The access list they exported | Access review Q3; Endpoint patch ring 2; Phishing report 4412 | Carried into the draft |
| The roles that are still justified | Aisha Rahman plus two others named in the thread. No distribution list attached | Carried into the draft |
| Leavers they know about | Phishing report 4412 and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Start from an export they provide. Do not ask for passwords to go look**

**2. Flag leavers, shared accounts, and standing admin with no named owner**

**3. Ask for a business reason for each high privilege. No reason, recommend removal**

**4. Shared logins are a finding. Recommend individual accounts**

**5. Record who approved the remaining access and the next review date**

**Deliberately not done**
- Asking for passwords.
- A review with no removal list.
- Shared admin treated as normal.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Asking for passwords
- A review with no removal list
- Shared admin treated as normal

## Related skills

- `identity-hardening`
- `offboarding-checklist`
