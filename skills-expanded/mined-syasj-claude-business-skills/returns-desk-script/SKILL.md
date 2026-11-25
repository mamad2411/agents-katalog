---
name: returns-desk-script
description: "Script a returns conversation that follows policy and does not accuse the shopper. Use when the user mentions returns script, refund script, retail returns, desk conversation, or asks for a returns script. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'returns-desk-script' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Returns Desk Script

Script a returns conversation that follows policy and does not accuse the shopper.

## When to use this skill

Use this skill when the user:

- returns script
- refund script
- retail returns
- desk conversation

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent inventory, prices, or reviews. Do not write deceptive promotions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The policy
- What the colleague can see
- Authorized exceptions
- Tone

## Workflow


### 1. Step 1

State the policy they supplied.
### 2. Step 2

Ask only for information the return requires.
### 3. Step 3

Do not accuse theft in the script. Route suspected fraud to their loss-prevention process.
### 4. Offer the next step

refund, exchange, or decline, as policy allows.
### 5. Step 5

Escalate when the shopper's case does not fit the script.
### 6. Step 6

Do not collect unrelated personal data.

## Output

Deliver a **returns script**.

- Purpose of this returns script, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a returns script by 30 September 2026. A script tells associates to shame the shopper into keeping the item.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A script tells associates to shame the shopper into keeping the item.

The policy: their one-page rule dated 2 Mar 2026. No exception log
What the colleague can see: Returns desk log, last reviewed 14 September 2026. No owner named since
Authorized exceptions: SKU 1044 cabin filter is open. End-cap display 3 was raised verbally and never logged
Tone: plain, for people who already know the context. No house guide attached
```

### Example outcome

**Returns script**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
States the policy calmly and escalates exceptions without shame.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The policy | their one-page rule dated 2 Mar 2026. No exception log | Needs confirmation |
| What the colleague can see | Returns desk log, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Authorized exceptions | SKU 1044 cabin filter is open. End-cap display 3 was raised verbally and never logged | Carried into the draft |
| Tone | plain, for people who already know the context. No house guide attached | Needs confirmation |

**How this draft was built**

**1. State the policy they supplied**

**2. Ask only for information the return requires**

**3. Do not accuse theft in the script. Route suspected fraud to their loss-prevention process**

**4. Offer the next step**  
refund, exchange, or decline, as policy allows.

**5. Escalate when the shopper's case does not fit the script**

**Deliberately not done**
- A theft accusation in the script.
- Invented policy.
- Unrelated personal data.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A theft accusation in the script
- Invented policy
- Unrelated personal data

## Related skills

- `returns-process`
- `support-macro`
