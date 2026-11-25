---
name: policy-writer
description: "Draft a policy people can follow, with an owner, an exception path, and a review date. Use when the user mentions write a policy, policy draft, governance policy, company policy, or asks for a policy draft. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'policy-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Policy Writer

Draft a policy people can follow, with an owner, an exception path, and a review date.

## When to use this skill

Use this skill when the user:

- write a policy
- policy draft
- governance policy
- company policy

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The behavior to govern
- The owner
- The audience
- Related procedures

## Workflow


### 1. Step 1

State the purpose and who it applies to.
### 2. Step 2

Write requirements as behaviors.
### 3. Step 3

Point to the procedure for how. The policy should not be a novel.
### 4. Step 4

Add an exception path and an owner.
### 5. Step 5

Set a review date.
### 6. Step 6

Mark it draft until the owner adopts it. Do not invent regulatory citations.

## Output

Deliver a **policy draft**.

- Purpose of this policy draft, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a policy draft by 30 September 2026. A draft cites several laws from memory to sound serious.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A draft cites several laws from memory to sound serious.

The behavior to govern: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The owner: Priya Shah, controller
The audience: people who already buy from Northline Studio
Related procedures: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Policy draft**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the invented citations, names an owner, and stays short enough to follow.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The behavior to govern | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The owner | Priya Shah, controller | Carried into the draft |
| The audience | people who already buy from Northline Studio | Carried into the draft |
| Related procedures | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. State the purpose and who it applies to**

**2. Write requirements as behaviors**

**3. Point to the procedure for how. The policy should not be a novel**

**4. Add an exception path and an owner**

**5. Set a review date**

**Deliberately not done**
- A policy with no owner.
- Invented legal citations.
- Requirements nobody can perform.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A policy with no owner
- Invented legal citations
- Requirements nobody can perform

## Related skills

- `handbook-policy-draft`
- `security-policy-draft`
