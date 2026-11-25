---
name: loss-prevention-incident
description: "Write a factual loss prevention incident log from the events the user described, without accusations beyond what evidence supports. Use when the user mentions loss prevention, LP incident, shrink report, theft incident log, or asks for a LP incident log. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'loss-prevention-incident' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Loss Prevention Incident Log

Write a factual loss prevention incident log from the events the user described, without accusations beyond what evidence supports.

## When to use this skill

Use this skill when the user:

- loss prevention
- LP incident
- shrink report
- theft incident log

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

- What was observed
- Timestamps and locations
- What evidence exists
- What action was taken

## Workflow


### 1. Step 1

Record only what was observed, on camera, or documented. Do not infer intent from observation alone.
### 2. Step 2

Timestamps and locations must come from the user. Do not guess.
### 3. Evidence category

confirmed, on camera, alleged, or witness account. Label each.
### 4. Actions taken

what happened and who authorized it. Do not recommend an arrest the policy does not support.
### 5. Step 5

No names of persons not yet confirmed as employees or involved parties.
### 6. Step 6

This is a log, not a court finding.

## Output

Deliver a **LP incident log**.

- Purpose of this LP incident log, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a LP incident log by 30 September 2026. A log says "the suspect stole the item" based on a single camera angle that does not show concealment.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A log says "the suspect stole the item" based on a single camera angle that does not show concealment.

What was observed: Returns desk log, last reviewed 14 September 2026. No owner named since
Timestamps and locations: five working days, due 30 September 2026
What evidence exists: one PDF, 2 pages, dated 14 September 2026
What action was taken: SKU 1044 cabin filter; End-cap display 3. Both unassigned as of 14 September 2026
```

### Example outcome

**Lp incident log**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Says "item not seen at checkout; camera angle does not confirm concealment; LP notified.".

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What was observed | Returns desk log, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Timestamps and locations | five working days, due 30 September 2026 | Carried into the draft |
| What evidence exists | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| What action was taken | SKU 1044 cabin filter; End-cap display 3. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Record only what was observed, on camera, or documented. Do not infer intent from observation alone**

**2. Timestamps and locations must come from the user. Do not guess**

**3. Evidence category**  
confirmed, on camera, alleged, or witness account. Label each.

**4. Actions taken**  
what happened and who authorized it. Do not recommend an arrest the policy does not support.

**5. No names of persons not yet confirmed as employees or involved parties**

**Deliberately not done**
- Inferring intent from observation.
- An arrest recommendation without policy support.
- Unnamed witnesses presented as confirmed.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inferring intent from observation
- An arrest recommendation without policy support
- Unnamed witnesses presented as confirmed

## Related skills

- `returns-desk-script`
