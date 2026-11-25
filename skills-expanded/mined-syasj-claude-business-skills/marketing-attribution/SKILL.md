---
name: marketing-attribution
description: "Review an attribution claim so the team does not confuse a tracking rule with causality. Use when the user mentions marketing attribution, which channel works, multi-touch attribution, campaign ROI, or asks for a attribution review. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'marketing-attribution' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Marketing Attribution Review

Review an attribution claim so the team does not confuse a tracking rule with causality.

## When to use this skill

Use this skill when the user:

- marketing attribution
- which channel works
- multi-touch attribution
- campaign ROI

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The attribution rule they use
- The data they actually have
- The decision they want to make
- Known tracking gaps

## Workflow


### 1. Name the rule

First touch, last touch, or another rule they stated. A rule is not the truth.
### 2. Tracking gaps

What is untracked. Those gaps bound the claim.
### 3. Decision fit

Say whether the data can support the budget decision they want to make. If not, say what it can support.
### 4. Incrementality

If they have no holdout or other comparison, do not call a channel causal. Call it correlated under their rule.
### 5. Recommendation

A measurement improvement or a cautious budget test. Not a false ROI.
### 6. Language

Rewrite any sentence that says 'this channel created revenue' unless their design supports it.

## Output

Deliver a **attribution review**.

- Purpose of this attribution review, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs an attribution review by 30 September 2026. A team wants to cut content because last-touch credits it with little revenue, while sales says content starts most conversations.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to cut content because last-touch credits it with little revenue, while sales says content starts most conversations.

The attribution rule they use: their one-page rule dated 2 Mar 2026. No exception log since
The data they actually have: Fall service page, recorded 14 September 2026. No supporting file attached
The decision they want to make: A team wants to cut content because last-touch credits it with little revenue, while sales says content starts most conversations
Known tracking gaps: Fall service page is missing a source
```

### Example outcome

**Attribution review**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the causal cut, names the tracking gap, and proposes a cleaner test.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The attribution rule they use | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |
| The data they actually have | Fall service page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The decision they want to make | A team wants to cut content because last-touch credits it with little revenue, while sales says content starts most conversations | Carried into the draft |
| Known tracking gaps | Fall service page is missing a source | Needs confirmation |

**How this draft was built**

**1. Name the rule**  
First touch, last touch, or another rule they stated. A rule is not the truth.

**2. Tracking gaps**  
What is untracked. Those gaps bound the claim.

**3. Decision fit**  
Say whether the data can support the budget decision they want to make. If not, say what it can support.

**4. Incrementality**  
If they have no holdout or other comparison, do not call a channel causal. Call it correlated under their rule.

**5. Recommendation**  
A measurement improvement or a cautious budget test. Not a false ROI.

**Deliberately not done**
- Treating last touch as causality.
- Ignoring untracked deals.
- A false ROI number.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Treating last touch as causality.
- Ignoring untracked deals.
- A false ROI number.

## Related skills

- `marketing-experiment`
- `executive-insight`
