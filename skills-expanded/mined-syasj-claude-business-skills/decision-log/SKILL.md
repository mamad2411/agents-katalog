---
name: decision-log
description: "Record an important decision so a later reader can see the choice, the alternatives, and what would reopen it. Use when the user mentions decision log, document this decision, why did we choose, decision record, or asks for a decision record. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'decision-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Decision Log

Record an important decision so a later reader can see the choice, the alternatives, and what would reopen it.

## When to use this skill

Use this skill when the user:

- decision log
- document this decision
- why did we choose
- decision record
- ADR for the business

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision in one sentence
- Alternatives considered
- Facts used
- Who decided and when

## Workflow


### 1. State the decision

One sentence, past or present tense, with the date and the decider. No preamble.
### 2. Record alternatives

At least one real alternative that was rejected, and why. If none was considered, say that plainly.
### 3. Cite facts

List only evidence the user provided. Do not backfill a rationale that sounds smarter than the actual one.
### 4. Name the reopen condition

What new fact would justify revisiting the decision. Decisions without reopen conditions become dogma.
### 5. Note consequences

Who must change what by when because of this decision.
### 6. File it

Suggest a location and a title the team can find later. Do not create a new bureaucracy around the log.

## Output

Deliver a **decision record**.

- Purpose of this decision record, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a decision record by 30 September 2026. A leadership team chose to pause a second product line after a renewal slipped, and they want the reason written down.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A leadership team chose to pause a second product line after a renewal slipped, and they want the reason written down.

The decision in one sentence: A leadership team chose to pause a second product line after a renewal slipped, and they want the reason written down
Alternatives considered: two deals cited from memory. Neither has a written loss reason
Facts used: Bright Axle and one other, both unconfirmed as of 14 September 2026
Who decided and when: 30 September 2026
```

### Example outcome

**Decision record**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Drove it, and the condition that would reopen it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision in one sentence | A leadership team chose to pause a second product line after a renewal slipped, and they want the reason written down | Needs confirmation |
| Alternatives considered | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| Facts used | Bright Axle and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Who decided and when | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. State the decision**  
One sentence, past or present tense, with the date and the decider. No preamble.

**2. Record alternatives**  
At least one real alternative that was rejected, and why. If none was considered, say that plainly.

**3. Cite facts**  
List only evidence the user provided. Do not backfill a rationale that sounds smarter than the actual one.

**4. Name the reopen condition**  
What new fact would justify revisiting the decision. Decisions without reopen conditions become dogma.

**5. Note consequences**  
Who must change what by when because of this decision.

**Deliberately not done**
- Rewriting history to make a messy decision look inevitable.
- Logging every tiny choice.
- Omitting the rejected alternative.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Rewriting history to make a messy decision look inevitable.
- Logging every tiny choice.
- Omitting the rejected alternative.

## Related skills

- `architecture-decision-record`
- `board-memo-writer`
- `founder-decision-review`
