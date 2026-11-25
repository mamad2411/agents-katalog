---
name: content-calendar
description: "Build a content calendar from buyer questions and capacity, not from a need to post daily. Use when the user mentions content calendar, editorial calendar, what should we publish, content plan, or asks for a content calendar. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'content-calendar' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Content Calendar

Build a content calendar from buyer questions and capacity, not from a need to post daily.

## When to use this skill

Use this skill when the user:

- content calendar
- editorial calendar
- what should we publish
- content plan

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

- Buyer questions already heard
- Capacity in pieces per week
- Offers the content should support
- Channels that are actually maintained

## Workflow


### 1. Questions first

List questions sales and support hear. Those outrank topic brainstorms.
### 2. Capacity

Plan only what the team can draft, review, and proof. A daily cadence they cannot review is a quality problem.
### 3. Mix

A simple mix of proof, teaching, and offer. Do not pretend a formula is science.
### 4. Owners and dates

Each piece has a drafter and a reviewer. No owner, no slot.
### 5. Repurpose

One strong piece can feed a short note. Do not plan seven original ideas if capacity is one.
### 6. Claims

Flag pieces that would need evidence the company does not have.

## Output

Deliver a **content calendar**.

- Purpose of this content calendar, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a content calendar by 30 September 2026. A founder wants daily posts, and the only writer has four hours a week.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A founder wants daily posts, and the only writer has four hours a week.

Buyer questions already heard: A founder wants daily posts, and the only writer has four hours a week
Capacity in pieces per week: two people, no overtime figure
Offers the content should support: CAD 49, dates not set, cap not set
Channels that are actually maintained: plain, for people who already know the context. No house guide attached
```

### Example outcome

**Content calendar**
Fieldnote · 14 September 2026 · Due 30 September 2026

**Decision**
A calendar of one reviewed piece a week, based on real buyer questions, with repurposing instead of fake volume.

**Checklist**

- [x] **Buyer questions already heard** — A founder wants daily posts, and the only writer has four hours a week  
      Evidenced in the file
- [x] **Capacity in pieces per week** — two people, no overtime figure  
      Evidenced in the file
- [x] **Offers the content should support** — CAD 49, dates not set, cap not set  
      Evidenced in the file
- [ ] **Channels that are actually maintained** — plain, for people who already know the context. No house guide attached  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Questions first
2. Capacity
3. Mix
4. Owners and dates
5. Repurpose

**Deliberately not done**
- A daily calendar with one writer and no reviewer.
- Topics with no buyer question behind them.
- Unsourced statistics planned into posts.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Lena Ortiz closes the open items before 30 September 2026.

## Anti-patterns

- A daily calendar with one writer and no reviewer.
- Topics with no buyer question behind them.
- Unsourced statistics planned into posts.

## Related skills

- `seo-content-brief`
- `newsletter-editor`
