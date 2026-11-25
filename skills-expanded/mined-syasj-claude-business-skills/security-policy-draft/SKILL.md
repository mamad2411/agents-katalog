---
name: security-policy-draft
description: "Draft a short security policy for one topic, in language employees can follow, marked for the security owner. Use when the user mentions security policy, acceptable use draft, password policy draft, security rules, or asks for a security policy draft. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'security-policy-draft' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Security Policy Draft

Draft a short security policy for one topic, in language employees can follow, marked for the security owner.

## When to use this skill

Use this skill when the user:

- security policy
- acceptable use draft
- password policy draft
- security rules

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

- The behavior to govern
- Current practice
- The owner
- Consequences they already use

## Workflow


### 1. Step 1

Cover one topic. A policy for all of security will not be read.
### 2. Step 2

Write the required behavior in plain steps.
### 3. Step 3

State exceptions and who can approve them.
### 4. Step 4

Use only consequences the company already has. Do not invent legal penalties.
### 5. Step 5

Point to the reporting path.
### 6. Step 6

Mark the draft unofficial until the security owner adopts it.

## Output

Deliver a **security policy draft**.

- Purpose of this security policy draft, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a security policy draft by 30 September 2026. The company wants a password policy and currently shares a team login.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The company wants a password policy and currently shares a team login.

The behavior to govern: Access review Q3, recorded 14 September 2026. No supporting file attached
Current practice: Endpoint patch ring 2 and one other, both unconfirmed as of 14 September 2026
The owner: Aisha Rahman, engineering lead
Consequences they already use: Endpoint patch ring 2. Partly documented: the what is written down, the who is not
```

### Example outcome

**Security policy draft**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Bans shared logins, sets an owner, and leaves legal penalties to counsel.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The behavior to govern | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Current practice | Endpoint patch ring 2 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The owner | Aisha Rahman, engineering lead | Carried into the draft |
| Consequences they already use | Endpoint patch ring 2. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Cover one topic. A policy for all of security will not be read**

**2. Write the required behavior in plain steps**

**3. State exceptions and who can approve them**

**4. Use only consequences the company already has. Do not invent legal penalties**

**5. Point to the reporting path**

**Deliberately not done**
- A 40-page policy for one control.
- Invented penalties.
- No exception path.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A 40-page policy for one control
- Invented penalties
- No exception path

## Related skills

- `policy-writer`
- `secrets-handling`
