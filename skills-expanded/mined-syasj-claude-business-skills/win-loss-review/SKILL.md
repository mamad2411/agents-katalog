---
name: win-loss-review
description: "Review wins and losses to find a pattern the team can change, not a story that flatters the winner. Use when the user mentions win loss, why we lost, deal postmortem, win review, or asks for a win-loss review. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'win-loss-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Win Loss Review

Review wins and losses to find a pattern the team can change, not a story that flatters the winner.

## When to use this skill

Use this skill when the user:

- win loss
- why we lost
- deal postmortem
- win review

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

- The outcome
- Buyer feedback if any
- Competitor or status quo facts the user has
- What the team did at each stage

## Workflow


### 1. Facts first

What the buyer said, separately from the seller's theory.
### 2. Decision criteria

Which criteria actually decided it, if the buyer said so. If they did not, do not invent the reason.
### 3. Execution versus offer

Was this a selling-process miss or a product and price miss. Recommend the owner accordingly.
### 4. Pattern

Compare with other reviews only if the user supplied them. One deal is an anecdote until a pattern appears.
### 5. Change

One behavior or offer change. A list of twelve lessons will not be used.
### 6. No blame essay

Name the process gap. Do not humiliate a rep.

## Output

Deliver a **win-loss review**.

- Purpose of this win-loss review, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a win-loss review by 30 September 2026. The team lost three deals and wants to discount, but buyer notes mention slow security review.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The team lost three deals and wants to discount, but buyer notes mention slow security review.

The outcome: The team lost three deals and wants to discount, but buyer notes mention slow security review. Stated once, in the ask. Not written down anywhere else
Buyer feedback if any: CAD 79, from their sheet, not a guess
Competitor or status quo facts the user has: two deals cited from memory. Neither has a written loss reason
What the team did at each stage: two people on shift, one off
```

### Example outcome

**Win-loss review**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats security-review speed as the pattern to test and does not approve a discount from this evidence alone.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcome | The team lost three deals and wants to discount, but buyer notes mention slow security review. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Buyer feedback if any | CAD 79, from their sheet, not a guess | Carried into the draft |
| Competitor or status quo facts the user has | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| What the team did at each stage | two people on shift, one off | Needs confirmation |

**How this draft was built**

**1. Facts first**  
What the buyer said, separately from the seller's theory.

**2. Decision criteria**  
Which criteria actually decided it, if the buyer said so. If they did not, do not invent the reason.

**3. Execution versus offer**  
Was this a selling-process miss or a product and price miss. Recommend the owner accordingly.

**4. Pattern**  
Compare with other reviews only if the user supplied them. One deal is an anecdote until a pattern appears.

**5. Change**  
One behavior or offer change. A list of twelve lessons will not be used.

**Deliberately not done**
- A single lost deal turned into a new strategy.
- Blaming price without buyer evidence.
- A review with no change.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A single lost deal turned into a new strategy.
- Blaming price without buyer evidence.
- A review with no change.

## Related skills

- `competitive-battlecard`
- `pipeline-review`
