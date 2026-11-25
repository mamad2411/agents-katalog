---
name: prioritization-rice
description: "Prioritize a short list with RICE or a simpler cut, and show the math instead of hiding behind it. Use when the user mentions RICE, prioritize the roadmap, score these ideas, what should we build next, or asks for a prioritization note. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'prioritization-rice' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# RICE Prioritization

Prioritize a short list with RICE or a simpler cut, and show the math instead of hiding behind it.

## When to use this skill

Use this skill when the user:

- RICE
- prioritize the roadmap
- score these ideas
- what should we build next

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The candidate list
- Evidence for reach and impact
- Effort estimates
- Constraints

## Workflow


### 1. Bound the list

Prioritize items that serve the current bet. Off-strategy items are parked, not scored into existence.
### 2. Score honestly

Reach, impact, confidence, and effort use the user's evidence. Low confidence stays low. Do not inflate confidence to win an argument.
### 3. Show the arithmetic

The score is visible. A black-box rank is not RICE.
### 4. Override in the open

If strategy or a commitment overrides the score, write the override. Do not fudge the inputs.
### 5. Cut

A ranked list with no cut is not a decision. Recommend now, next, and not now.
### 6. Revisit

The date the scores expire.

## Output

Deliver a **prioritization note**.

- Purpose of this prioritization note, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a prioritization note by 30 September 2026. A stakeholder wants their idea scored 100 percent confidence so it sorts to the top.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A stakeholder wants their idea scored 100 percent confidence so it sorts to the top.

The candidate list: Activation checklist; Trial day-3 email; Usage limit warning
Evidence for reach and impact: one PDF, 2 pages, dated 14 September 2026
Effort estimates: Activation checklist, last reviewed 14 September 2026. No owner named since
Constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Prioritization note**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps confidence low, shows the math, and records any strategic override separately.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The candidate list | Activation checklist; Trial day-3 email; Usage limit warning | Needs confirmation |
| Evidence for reach and impact | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Effort estimates | Activation checklist, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Bound the list**  
Prioritize items that serve the current bet. Off-strategy items are parked, not scored into existence.

**2. Score honestly**  
Reach, impact, confidence, and effort use the user's evidence. Low confidence stays low. Do not inflate confidence to win an argument.

**3. Show the arithmetic**  
The score is visible. A black-box rank is not RICE.

**4. Override in the open**  
If strategy or a commitment overrides the score, write the override. Do not fudge the inputs.

**5. Cut**  
A ranked list with no cut is not a decision. Recommend now, next, and not now.

**Deliberately not done**
- Inflated confidence scores.
- A ranking with no cut.
- Fake precision to three decimals.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inflated confidence scores.
- A ranking with no cut.
- Fake precision to three decimals.

## Related skills

- `portfolio-prioritization`
- `roadmap-narrative`

## Optional local tool

A stdlib script is bundled at `scripts/rice_score.py`. It scores a CSV of `item,reach,impact,confidence,effort` that you already filled in. It does not invent reach or confidence. Example: `python3 scripts/rice_score.py items.csv --json`.
