---
name: research-memo
description: "Write a research memo that separates evidence, interpretation, and what is still unknown. Use when the user mentions research memo, findings memo, synthesize this research, evidence memo, or asks for a research memo. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'research-memo' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Research Memo

Write a research memo that separates evidence, interpretation, and what is still unknown.

## When to use this skill

Use this skill when the user:

- research memo
- findings memo
- synthesize this research
- evidence memo

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question
- The evidence they gathered
- The method limits
- The audience

## Workflow


### 1. Step 1

Restate the question.
### 2. Step 2

Summarize evidence with sources they provided.
### 3. Step 3

Put interpretation in a labeled section.
### 4. Write the limits

sample, access, and time.
### 5. Step 5

Do not upgrade a small study into a law of the market.
### 6. Step 6

End with the next question or decision, not with a padded conclusion.

## Output

Deliver a **research memo**.

- Purpose of this research memo, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs a research memo by 30 September 2026. Five interviews are written up as proof an entire industry is shifting.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

Five interviews are written up as proof an entire industry is shifting.

The question: Five interviews are written up as proof an entire industry is shifting
The evidence they gathered: one PDF, 2 pages, dated 14 September 2026
The method limits: the method in the ask. No second design attached
The audience: people who already buy from Riverbend College
```

### Example outcome

**Research memo**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Limits the claim to those five interviews and lists what a larger study would need.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | Five interviews are written up as proof an entire industry is shifting | Needs confirmation |
| The evidence they gathered | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The method limits | the method in the ask. No second design attached | Carried into the draft |
| The audience | people who already buy from Riverbend College | Needs confirmation |

**How this draft was built**

**1. Restate the question**

**2. Summarize evidence with sources they provided**

**3. Put interpretation in a labeled section**

**4. Write the limits**  
sample, access, and time.

**5. Do not upgrade a small study into a law of the market**

**Deliberately not done**
- A law-of-the-market claim from a small sample.
- Sources you cannot see.
- Interpretation disguised as fact.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A law-of-the-market claim from a small sample
- Sources you cannot see
- Interpretation disguised as fact

## Related skills

- `executive-insight`
- `evidence-table`
