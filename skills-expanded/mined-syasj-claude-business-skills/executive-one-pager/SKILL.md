---
name: executive-one-pager
description: "Compress a complex issue into a single page a busy executive can act on. Use when the user mentions one-pager, exec summary, brief the CEO, single page brief, or asks for a executive one-pager. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'executive-one-pager' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Executive One-Pager

Compress a complex issue into a single page a busy executive can act on.

## When to use this skill

Use this skill when the user:

- one-pager
- exec summary
- brief the CEO
- single page brief

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

- The audience and the decision they can make
- The source material or the user's facts
- The recommendation if there is one
- What must not be cut

## Workflow


### 1. Identify the reader

Write for the person who will decide, not for every stakeholder who wants a mention.
### 2. Put the point first

The top of the page states the situation, the recommendation, and the ask.
### 3. Support with three facts

Choose the three facts that would change the decision if they were wrong. Move the rest out.
### 4. Name the tradeoff

What the recommendation costs or risks. A one-pager with no tradeoff is an advertisement.
### 5. End with the action

Owner, date, and what 'done' means.
### 6. Cut jargon

If a term is internal, translate it. The reader should not need a glossary.

## Output

Deliver a **executive one-pager**.

- Purpose of this executive one-pager, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an executive one-pager by 30 September 2026. A general manager needs the CEO to approve a price test and currently has a 14-page appendix.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A general manager needs the CEO to approve a price test and currently has a 14-page appendix.

The audience and the decision they can make: people who already buy from Northline Studio
The source material or the user's facts: note from Mara Chen, 14 September 2026. No outside report
The recommendation if there is one: Cedar Clinic, recorded 14 September 2026. No supporting file attached
What must not be cut: open item, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Executive one-pager**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A one-page brief with the test, the risk, three facts, and a yes-or-no ask.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The audience and the decision they can make | people who already buy from Northline Studio | Needs confirmation |
| The source material or the user's facts | note from Mara Chen, 14 September 2026. No outside report | Carried into the draft |
| The recommendation if there is one | Cedar Clinic, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| What must not be cut | open item, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Identify the reader**  
Write for the person who will decide, not for every stakeholder who wants a mention.

**2. Put the point first**  
The top of the page states the situation, the recommendation, and the ask.

**3. Support with three facts**  
Choose the three facts that would change the decision if they were wrong. Move the rest out.

**4. Name the tradeoff**  
What the recommendation costs or risks. A one-pager with no tradeoff is an advertisement.

**5. End with the action**  
Owner, date, and what 'done' means.

**Deliberately not done**
- Shrinking a long memo by reducing the font.
- Including every stakeholder's paragraph.
- Hiding the ask in the last line.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Shrinking a long memo by reducing the font.
- Including every stakeholder's paragraph.
- Hiding the ask in the last line.

## Related skills

- `board-memo-writer`
- `decision-log`
- `management-reporting-pack`
