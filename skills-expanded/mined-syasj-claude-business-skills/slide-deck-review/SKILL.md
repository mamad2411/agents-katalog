---
name: slide-deck-review
description: "Review a slide deck for logical flow, unsupported claims, and slides that do not carry weight. Use when the user mentions slide deck review, deck review, review my slides, PowerPoint review, or asks for a slide review. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'slide-deck-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Slide Deck Review

Review a slide deck for logical flow, unsupported claims, and slides that do not carry weight.

## When to use this skill

Use this skill when the user:

- slide deck review
- deck review
- review my slides
- PowerPoint review
- presentation review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Productivity systems serve the person's actual constraints. Do not recommend surveillance of colleagues or hidden monitoring.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The deck content or a summary of each slide
- The audience
- The ask at the end
- Any timing constraints

## Workflow


### 1. Step 1

Check that every slide has one point. A slide with four bullet points often has no point.
### 2. Step 2

Find the claim that is not supported. If a slide says 'fastest growing' it needs a source or a qualifier.
### 3. Step 3

Identify slides that exist for the presenter, not the audience. Cut or move to an appendix.
### 4. Step 4

Check the ask. The last slide should state what the audience does next and by when.
### 5. Step 5

Flag slides that require the presenter to explain them. A slide that needs a verbal decoder should be rewritten.
### 6. Step 6

Note the slide count against the time. A confident presenter can do one slide per two minutes. Rushing signals unresolved structure.

## Output

Deliver a **slide review**.

- Purpose of this slide review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a slide review by 30 September 2026. Slide 7 says 'customers love us' with no data and a smiley face.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Slide 7 says 'customers love us' with no data and a smiley face.

The deck content or a summary of each slide: one file, dated 14 September 2026. No earlier version attached for comparison
The audience: people who already buy from Northline Studio
The ask at the end: Slide 7 says 'customers love us' with no data and a smiley face. Stated once, in the ask. Not written down anywhere else
Any timing constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Slide review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Proposes one customer quote or an NPS number, or removing the slide if neither exists.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The deck content or a summary of each slide | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| The audience | people who already buy from Northline Studio | Carried into the draft |
| The ask at the end | Slide 7 says 'customers love us' with no data and a smiley face. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Any timing constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Check that every slide has one point. A slide with four bullet points often has no point**

**2. Find the claim that is not supported. If a slide says 'fastest growing' it needs a source or a qualifier**

**3. Identify slides that exist for the presenter, not the audience. Cut or move to an appendix**

**4. Check the ask. The last slide should state what the audience does next and by when**

**5. Flag slides that require the presenter to explain them. A slide that needs a verbal decoder should be rewritten**

**Deliberately not done**
- Marking slides as weak without saying what to change.
- Adding slides to fill gaps.
- Softening a false claim instead of removing it.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Marking slides as weak without saying what to change
- Adding slides to fill gaps
- Softening a false claim instead of removing it

## Related skills

- `presentation-structure`
- `marketing-claims-review`
- `executive-one-pager`
