---
name: store-opening-checklist
description: "Write a store opening checklist that confirms safety, cash, and the floor before doors open. Use when the user mentions store opening, open the store, morning checklist retail, shop opening, or asks for a opening checklist. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'store-opening-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Store Opening Checklist

Write a store opening checklist that confirms safety, cash, and the floor before doors open.

## When to use this skill

Use this skill when the user:

- store opening
- open the store
- morning checklist retail
- shop opening

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

- Safety checks they require
- Cash process
- Floor standards
- Who may open

## Workflow


### 1. Step 1

Safety and exits first.
### 2. Step 2

Cash counted under their dual-control rule if they have one.
### 3. Step 3

Floor standards that affect a shopper today.
### 4. Step 4

Do not write the safe combination or passwords into the checklist.
### 5. Step 5

Note who to call if a check fails.
### 6. Step 6

A failed safety check means delay opening, not a workaround.

## Output

Deliver a **opening checklist**.

- Purpose of this opening checklist, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs an opening checklist by 30 September 2026. A checklist says to prop an alarmed exit so deliveries are easier.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A checklist says to prop an alarmed exit so deliveries are easier.

Safety checks they require: Returns desk log. Partly documented: the what is written down, the who is not
Cash process: email to Diane Cho. No written steps after 1 Sep 2026
Floor standards: their one-page rule dated 2 Mar 2026. No exception log since
Who may open: Diane Cho, store lead
```

### Example outcome

**Opening checklist**
Harbor Goods · 14 September 2026 · Due 30 September 2026

**Decision**
Forbids propping the exit and names the person who can delay opening.

**Checklist**

- [x] **Safety checks they require** — Returns desk log. Partly documented: the what is written down, the who is not  
      Evidenced in the file
- [x] **Cash process** — email to Diane Cho. No written steps after 1 Sep 2026  
      Evidenced in the file
- [x] **Floor standards** — their one-page rule dated 2 Mar 2026. No exception log since  
      Evidenced in the file
- [ ] **Who may open** — Diane Cho, store lead  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Safety and exits first
2. Cash counted under their dual-control rule if they have one
3. Floor standards that affect a shopper today
4. Do not write the safe combination or passwords into the checklist
5. Note who to call if a check fails

**Deliberately not done**
- Passwords on the checklist.
- Opening through a failed safety check.
- No owner for a failed check.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Diane Cho closes the open items before 30 September 2026.

## Anti-patterns

- Passwords on the checklist
- Opening through a failed safety check
- No owner for a failed check

## Related skills

- `shift-brief-hospitality`
- `safety-toolbox-talk`
