---
name: sop-writer
description: "Write a standard operating procedure a new person can run, with the stop conditions included. Use when the user mentions write an SOP, standard operating procedure, document this process, operating procedure, or asks for a standard operating procedure. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sop-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SOP Writer

Write a standard operating procedure a new person can run, with the stop conditions included.

## When to use this skill

Use this skill when the user:

- write an SOP
- standard operating procedure
- document this process
- operating procedure

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

- The outcome of the process
- The steps as performed today
- Exceptions
- The owner

## Workflow


### 1. Step 1

Name the outcome and the trigger that starts the work.
### 2. Step 2

Write steps in the order a new person would do them, including where the file or tool actually lives if the user said so.
### 3. Step 3

Add the check that shows the step worked.
### 4. Write stop conditions

when to halt and ask.
### 5. Step 5

Put exceptions in the procedure, not in someone's memory.
### 6. Step 6

Name the owner and the review date. A procedure with no owner will drift.

## Output

Deliver a **standard operating procedure**.

- Purpose of this standard operating procedure, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a standard operating procedure by 30 September 2026. A finance SOP says 'process the file' and the file location lives in one person's head.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A finance SOP says 'process the file' and the file location lives in one person's head.

The outcome of the process: email to Diane Cho. No written steps after 1 Sep 2026
The steps as performed today: Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026
Exceptions: Tuesday shift is open. SOP 118 receiving was raised verbally and never logged
The owner: Diane Cho, operations manager
```

### Example outcome

**Standard operating procedure**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A procedure with the trigger, the check, a stop condition, and an owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome of the process | email to Diane Cho. No written steps after 1 Sep 2026 | Needs confirmation |
| The steps as performed today | Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026 | Carried into the draft |
| Exceptions | Tuesday shift is open. SOP 118 receiving was raised verbally and never logged | Carried into the draft |
| The owner | Diane Cho, operations manager | Needs confirmation |

**How this draft was built**

**1. Name the outcome and the trigger that starts the work**

**2. Write steps in the order a new person would do them, including where the file or tool actually lives if the user said so**

**3. Add the check that shows the step worked**

**4. Write stop conditions**  
when to halt and ask.

**5. Put exceptions in the procedure, not in someone's memory**

**Deliberately not done**
- A procedure only the author understands.
- No stop condition.
- Steps that invent a system path.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A procedure only the author understands
- No stop condition
- Steps that invent a system path

## Related skills

- `process-map`
- `knowledge-base-article`
