---
name: sales-email-sequence
description: "Write a short, truthful outreach or follow-up sequence that earns a reply without deception. Use when the user mentions sales email, follow-up sequence, outreach email, prospecting note, or asks for a email sequence. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sales-email-sequence' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sales Email Sequence

Write a short, truthful outreach or follow-up sequence that earns a reply without deception.

## When to use this skill

Use this skill when the user:

- sales email
- follow-up sequence
- outreach email
- prospecting note

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

- Who the reader is
- The observation that makes this relevant
- The single ask
- Proof you can include

## Workflow


### 1. Relevance

The first lines show why this person, why now, using a real observation. No 'I noticed you are a leader' filler if you noticed nothing.
### 2. One ask

A reply, a 20-minute call, or a referral. Not three asks.
### 3. Proof

One sentence of proof the user can support. No fake mutual connections.
### 4. Length

Short enough to read on a phone. Cut the company history.
### 5. Follow-ups

Two or three notes that add a new fact, not 'bumping this'. Then stop.
### 6. Compliance

No deception about why you are writing. No harvested personal secrets. Respect opt-out language the user must include if they say the law or policy requires it.

## Output

Deliver a **email sequence**.

- Purpose of this email sequence, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs an email sequence by 30 September 2026. A rep wants a five-email sequence that pretends the buyer asked for information.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A rep wants a five-email sequence that pretends the buyer asked for information.

Who the reader is: Samir Qureshi, account executive
The observation that makes this relevant: Harbor Goods, recorded 14 September 2026. No supporting file attached
The single ask: A rep wants a five-email sequence that pretends the buyer asked for information. Stated once, in the ask. Not written down anywhere else
Proof you can include: one customer email, 14 September 2026, no attachment beyond that
```

### Example outcome

**Email sequence — draft ready to send**

> To: the recipient named in the file
> From: Samir Qureshi, account executive, Fieldnote
> Date: 14 September 2026

---

Hello,

A three-note sequence with a real observation, one ask, and no fake inquiry, plus a stop after the third note.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Samir Qureshi
account executive, Fieldnote

---

**How this draft was checked**

1. **Relevance** — The first lines show why this person, why now, using a real observation. No 'I noticed you are a leader' filler if you noticed nothing.
2. **One ask** — A reply, a 20-minute call, or a referral. Not three asks.
3. **Proof** — One sentence of proof the user can support. No fake mutual connections.
4. **Length** — Short enough to read on a phone. Cut the company history.

**Deliberately not done**
- Fake mutual connections.
- A sequence that never stops.
- Deceptive subject lines.

Next: Samir Qureshi sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Fake mutual connections.
- A sequence that never stops.
- Deceptive subject lines.

## Related skills

- `discovery-call`
- `objection-handling`
