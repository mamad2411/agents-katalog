---
name: objection-handling
description: "Answer a sales objection with evidence and a question, not with pressure or made-up proof. Use when the user mentions handle this objection, buyer said no, competitor objection, too expensive, or asks for a objection response. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'objection-handling' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Objection Handling

Answer a sales objection with evidence and a question, not with pressure or made-up proof.

## When to use this skill

Use this skill when the user:

- handle this objection
- buyer said no
- competitor objection
- too expensive

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The objection in the buyer's words
- Evidence you really have
- What you still do not know
- The next step you want

## Workflow


### 1. Restate

Repeat the objection fairly so the buyer would recognize it.
### 2. Classify

Price, priority, trust, timing, or fit. Do not treat every no as a price problem.
### 3. Evidence

Respond only with proof the user has. If proof is missing, say what you will go find.
### 4. Question

Ask one question that tests whether the objection is the real one.
### 5. Next step

A small commitment, not a guilt trip.
### 6. Ethics

No false scarcity, no fake customers, no disparagement you cannot support.

## Output

Deliver a **objection response**.

- Purpose of this objection response, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs an objection response by 30 September 2026. A buyer says 'you are too expensive' before any outcome has been quantified.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A buyer says 'you are too expensive' before any outcome has been quantified.

The objection in the buyer's words: Harbor Goods is open. Cedar Clinic was raised verbally and never logged
Evidence you really have: one PDF, 2 pages, dated 14 September 2026
What you still do not know: Redline Parts, last reviewed 14 September 2026. No owner named since
The next step you want: Harbor Goods; Cedar Clinic. Both unassigned as of 14 September 2026
```

### Example outcome

**Objection response**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats the comment as unquantified, asks what it is being compared with, and does not invent a discount or a logo.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The objection in the buyer's words | Harbor Goods is open. Cedar Clinic was raised verbally and never logged | Needs confirmation |
| Evidence you really have | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| What you still do not know | Redline Parts, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The next step you want | Harbor Goods; Cedar Clinic. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate**  
Repeat the objection fairly so the buyer would recognize it.

**2. Classify**  
Price, priority, trust, timing, or fit. Do not treat every no as a price problem.

**3. Evidence**  
Respond only with proof the user has. If proof is missing, say what you will go find.

**4. Question**  
Ask one question that tests whether the objection is the real one.

**5. Next step**  
A small commitment, not a guilt trip.

**Deliberately not done**
- False scarcity.
- Invented customer logos.
- Arguing with the buyer before understanding the objection.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- False scarcity.
- Invented customer logos.
- Arguing with the buyer before understanding the objection.

## Related skills

- `discovery-call`
- `competitive-battlecard`
