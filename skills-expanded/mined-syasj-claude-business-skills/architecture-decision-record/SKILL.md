---
name: architecture-decision-record
description: "Record an architecture decision with context, the decision, and the consequences, in a page. Use when the user mentions ADR, architecture decision record, record this technical decision, why did we choose this design, or asks for a architecture decision record. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'architecture-decision-record' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Architecture Decision Record

Record an architecture decision with context, the decision, and the consequences, in a page.

## When to use this skill

Use this skill when the user:

- ADR
- architecture decision record
- record this technical decision
- why did we choose this design

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision
- The context
- Alternatives
- Consequences

## Workflow


### 1. Title and status

Proposed, accepted, or superseded. Do not mark accepted if the user has not accepted it.
### 2. Context

The forces, from their system. No fictional scale numbers.
### 3. Decision

One paragraph. What you will do.
### 4. Alternatives

At least one rejected option and why.
### 5. Consequences

What becomes easier, what becomes harder, and the security or operability effect.
### 6. Revisit

What would supersede this record.

## Output

Deliver a **architecture decision record**.

- Purpose of this architecture decision record, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an architecture decision record by 30 September 2026. A team chose a queue technology in a meeting and nobody wrote why the simpler option lost.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team chose a queue technology in a meeting and nobody wrote why the simpler option lost.

The decision: A team chose a queue technology in a meeting and nobody wrote why the simpler option lost
The context: Checkout service, recorded 14 September 2026. No supporting file attached
Alternatives: two deals cited from memory. Neither has a written loss reason
Consequences: Invoice job. Partly documented: the what is written down, the who is not
```

### Example outcome

**Architecture decision record**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A one-page ADR with the rejected option, consequences, and status left as proposed until they accept it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision | A team chose a queue technology in a meeting and nobody wrote why the simpler option lost | Needs confirmation |
| The context | Checkout service, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Alternatives | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| Consequences | Invoice job. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Title and status**  
Proposed, accepted, or superseded. Do not mark accepted if the user has not accepted it.

**2. Context**  
The forces, from their system. No fictional scale numbers.

**3. Decision**  
One paragraph. What you will do.

**4. Alternatives**  
At least one rejected option and why.

**5. Consequences**  
What becomes easier, what becomes harder, and the security or operability effect.

**Deliberately not done**
- An ADR that is a tutorial.
- No alternative.
- Marking a draft as accepted.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An ADR that is a tutorial.
- No alternative.
- Marking a draft as accepted.

## Related skills

- `decision-log`
- `technical-design-doc`
