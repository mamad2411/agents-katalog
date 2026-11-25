---
name: raci-design
description: "Assign one accountable owner to a decision or process and stop at the roles that matter. Use when the user mentions RACI, who owns this, decision rights, accountable owner, or asks for a RACI. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'raci-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# RACI Design

Assign one accountable owner to a decision or process and stop at the roles that matter.

## When to use this skill

Use this skill when the user:

- RACI
- who owns this
- decision rights
- accountable owner

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision or process
- The people involved
- Where work stalls
- Who is currently blamed

## Workflow


### 1. Step 1

Define the decision narrowly. A RACI for a whole department is too vague.
### 2. Step 2

Assign exactly one accountable owner. Two A's are the finding.
### 3. Step 3

Consulted and informed lists stay short. A crowd is not a control.
### 4. Check the stall

the missing A or the extra C is usually visible in their story.
### 5. Step 5

Write what the owner may decide without another meeting.
### 6. Step 6

Revisit only if the decision rights are still unclear after a real case.

## Output

Deliver a **RACI**.

- Purpose of this RACI, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a RACI by 30 September 2026. A launch is late because product and marketing both think the other owns the date.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A launch is late because product and marketing both think the other owns the date.

The decision or process: A launch is late because product and marketing both think the other owns the date
The people involved: Tuesday shift, recorded 14 September 2026. No supporting file attached
Where work stalls: Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026
Who is currently blamed: Diane Cho, operations manager
```

### Example outcome

**Raci**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A RACI with one owner for the date and a short consulted list.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision or process | A launch is late because product and marketing both think the other owns the date | Needs confirmation |
| The people involved | Tuesday shift, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Where work stalls | Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026 | Carried into the draft |
| Who is currently blamed | Diane Cho, operations manager | Needs confirmation |

**How this draft was built**

**1. Define the decision narrowly. A RACI for a whole department is too vague**

**2. Assign exactly one accountable owner. Two A's are the finding**

**3. Consulted and informed lists stay short. A crowd is not a control**

**4. Check the stall**  
the missing A or the extra C is usually visible in their story.

**5. Write what the owner may decide without another meeting**

**Deliberately not done**
- Two accountable owners.
- A RACI that includes everyone.
- No decision written down.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Two accountable owners
- A RACI that includes everyone
- No decision written down

## Related skills

- `operating-cadence`
- `stakeholder-map`
