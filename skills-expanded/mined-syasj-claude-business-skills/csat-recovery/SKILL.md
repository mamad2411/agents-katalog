---
name: csat-recovery
description: "Plan a follow-up to a low satisfaction score that seeks the cause and stays inside the remedy policy. Use when the user mentions CSAT recovery, low survey score, detractor follow-up, unhappy customer follow-up, or asks for a recovery follow-up. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'csat-recovery' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Low Score Recovery

Plan a follow-up to a low satisfaction score that seeks the cause and stays inside the remedy policy.

## When to use this skill

Use this skill when the user:

- CSAT recovery
- low survey score
- detractor follow-up
- unhappy customer follow-up

## When not to use this skill

- Paying for review manipulation

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

- The score and any comment
- What the company can offer
- The owner
- Whether the customer opted into contact

## Workflow


### 1. Step 1

Contact only if their process allows it. Do not help evade an opt-out.
### 2. Step 2

Open with the specific issue if they wrote one. Do not be vague if the comment was specific.
### 3. Step 3

Ask what done looks like.
### 4. Step 4

Offer only remedies the user authorized.
### 5. Step 5

Record the cause so the tenth similar score becomes a system fix.
### 6. Step 6

Do not bribe a customer to change a public review. Refuse that request.

## Output

Deliver a **recovery follow-up**.

- Purpose of this recovery follow-up, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a recovery follow-up by 30 September 2026. A manager wants to offer a gift card if the customer edits a public review.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants to offer a gift card if the customer edits a public review.

The score and any comment: Ticket 4412, recorded 14 September 2026. No supporting file attached
What the company can offer: CAD 180, dates not set, cap not set
The owner: Rita Santos, support lead
Whether the customer opted into contact: Ticket 4412. Partly documented: the what is written down, the who is not
```

### Example outcome

**Recovery follow-up**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the review edit, asks about the cause, and stays inside authorized remedies.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The score and any comment | Ticket 4412, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| What the company can offer | CAD 180, dates not set, cap not set | Carried into the draft |
| The owner | Rita Santos, support lead | Carried into the draft |
| Whether the customer opted into contact | Ticket 4412. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Contact only if their process allows it. Do not help evade an opt-out**

**2. Open with the specific issue if they wrote one. Do not be vague if the comment was specific**

**3. Ask what done looks like**

**4. Offer only remedies the user authorized**

**5. Record the cause so the tenth similar score becomes a system fix**

**Deliberately not done**
- Changing a review for a perk.
- Contacting someone who opted out.
- An offer the team cannot honor.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Changing a review for a perk
- Contacting someone who opted out
- An offer the team cannot honor

## Related skills

- `service-recovery`
- `complaint-root-cause`
