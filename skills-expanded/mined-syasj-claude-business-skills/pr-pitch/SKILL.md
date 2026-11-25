---
name: pr-pitch
description: "Draft a press pitch that has news, a real spokesperson, and no inflated claims. Use when the user mentions press pitch, PR pitch, media pitch, reporter email, or asks for a press pitch. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pr-pitch' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# PR Pitch

Draft a press pitch that has news, a real spokesperson, and no inflated claims.

## When to use this skill

Use this skill when the user:

- press pitch
- PR pitch
- media pitch
- reporter email

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

- The news
- Why a reader would care
- Spokesperson
- Facts that can be checked

## Workflow


### 1. News test

What is new, and why now. A product description is not news by itself.
### 2. Reader

Which reporter's audience would care, in the user's words. Do not invent a relationship with a journalist.
### 3. Facts

Every number is checkable. Remove the rest.
### 4. Spokesperson

A named person who can speak on the record. No fake quotes.
### 5. Ask

A short interview or a factual briefing, not a demand for coverage.
### 6. Honesty

No embargo games the user does not understand, and no misleading exclusives.

## Output

Deliver a **press pitch**.

- Purpose of this press pitch, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a press pitch by 30 September 2026. A founder wants a pitch saying the company 'leads the market' with no data and no spokesperson.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A founder wants a pitch saying the company 'leads the market' with no data and no spokesperson.

The news: A founder wants a pitch saying the company 'leads the market' with no data and no spokesperson
Why a reader would care: A founder wants a pitch saying the company 'leads the market' with no data and no spokesperson
Spokesperson: Local search ad. Partly documented: the what is written down, the who is not
Facts that can be checked: Email to lapsed buyers and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Press pitch — draft ready to send**

> To: the recipient named in the file
> From: Lena Ortiz, marketing lead, Fieldnote
> Date: 14 September 2026

---

Hello,

Removes the leadership claim, requires a spokesperson, and states only checkable news.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Lena Ortiz
marketing lead, Fieldnote

---

**How this draft was checked**

1. **News test** — What is new, and why now. A product description is not news by itself.
2. **Reader** — Which reporter's audience would care, in the user's words. Do not invent a relationship with a journalist.
3. **Facts** — Every number is checkable. Remove the rest.
4. **Spokesperson** — A named person who can speak on the record. No fake quotes.

**Deliberately not done**
- Fake quotes.
- Invented reporter relationships.
- A pitch with no news.

Next: Lena Ortiz sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Fake quotes.
- Invented reporter relationships.
- A pitch with no news.

## Related skills

- `marketing-claims-review`
- `corporate-narrative`
