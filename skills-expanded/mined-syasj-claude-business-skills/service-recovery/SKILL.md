---
name: service-recovery
description: "Plan recovery from a service failure with a truthful apology, a fix, and a remedy inside authority. Use when the user mentions service recovery, we failed a customer, apology and remedy, make it right, or asks for a recovery plan. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'service-recovery' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Service Recovery

Plan recovery from a service failure with a truthful apology, a fix, and a remedy inside authority.

## When to use this skill

Use this skill when the user:

- service recovery
- we failed a customer
- apology and remedy
- make it right

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What failed
- Who was affected
- The fix
- The remedy the team is allowed to offer

## Workflow


### 1. Step 1

State the failure plainly. Do not bury it in an apology paragraph.
### 2. Step 2

Say what you know and what you are still checking.
### 3. Step 3

Describe the fix and the time, if known. Do not invent a restoration time.
### 4. Step 4

Offer only an authorized remedy.
### 5. Step 5

Tell them how to ask a follow-up question.
### 6. Step 6

Feed the cause to the problem-management path so recovery is not the only response.

## Output

Deliver a **recovery plan**.

- Purpose of this recovery plan, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a recovery plan by 30 September 2026. A draft says 'everything is resolved' while the queue is still failing.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A draft says 'everything is resolved' while the queue is still failing.

What failed: Ticket 4412, first seen 14 September 2026. No root cause recorded yet
Who was affected: Rita Santos, support lead
The fix: Ticket 4412, recorded 14 September 2026. No supporting file attached
The remedy the team is allowed to offer: two people on shift, one off
```

### Example outcome

**Recovery plan**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
States the ongoing failure, omits the fake resolution, and offers only an authorized remedy.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What failed | Ticket 4412, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| Who was affected | Rita Santos, support lead | Carried into the draft |
| The fix | Ticket 4412, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The remedy the team is allowed to offer | two people on shift, one off | Needs confirmation |

**How this draft was built**

**1. State the failure plainly. Do not bury it in an apology paragraph**

**2. Say what you know and what you are still checking**

**3. Describe the fix and the time, if known. Do not invent a restoration time**

**4. Offer only an authorized remedy**

**5. Tell them how to ask a follow-up question**

**Deliberately not done**
- A fake restoration time.
- An unauthorized remedy.
- An apology that hides the failure.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fake restoration time
- An unauthorized remedy
- An apology that hides the failure

## Related skills

- `csat-recovery`
- `customer-communication-incident`
