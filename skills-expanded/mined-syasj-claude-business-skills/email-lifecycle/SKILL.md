---
name: email-lifecycle
description: "Design a lifecycle email for one moment, with a true trigger, a useful message, and an honest unsubscribe path. Use when the user mentions lifecycle email, onboarding email, nurture sequence, retention email, or asks for a lifecycle email spec. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'email-lifecycle' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Email Lifecycle

Design a lifecycle email for one moment, with a true trigger, a useful message, and an honest unsubscribe path.

## When to use this skill

Use this skill when the user:

- lifecycle email
- onboarding email
- nurture sequence
- retention email

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

- The trigger event
- The reader's job at that moment
- The one action
- What must be true in the product before sending

## Workflow


### 1. Trigger

The event is real and timely. Do not email because a quota of sends exists.
### 2. Usefulness

The message helps the reader do the next step. A logo refresh is not a reason to email.
### 3. One action

One link that matters.
### 4. Truth

Do not imply the reader did something they did not do.
### 5. Frequency

Where this mail sits among others, so you do not stack three asks in a day.
### 6. Consent

Include whatever opt-out the user says their policy requires. Do not help hide an unsubscribe.

## Output

Deliver a **lifecycle email spec**.

- Purpose of this lifecycle email spec, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a lifecycle email spec by 30 September 2026. Marketing wants an 'we miss you' email to users who were never active, written as if they had a habit.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Marketing wants an 'we miss you' email to users who were never active, written as if they had a habit.

The trigger event: Fall service page, recorded 14 September 2026. No supporting file attached
The reader's job at that moment: Lena Ortiz plus two others named in the thread. No distribution list attached
The one action: Fall service page; Email to lapsed buyers. Both unassigned as of 14 September 2026
What must be true in the product before sending: Local search ad, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Lifecycle email spec — draft ready to send**

> To: the recipient named in the file
> From: Lena Ortiz, marketing lead, Fieldnote
> Date: 14 September 2026

---

Hello,

Refuses the fake habit and either changes the trigger or stops the send.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Lena Ortiz
marketing lead, Fieldnote

---

**How this draft was checked**

1. **Trigger** — The event is real and timely. Do not email because a quota of sends exists.
2. **Usefulness** — The message helps the reader do the next step. A logo refresh is not a reason to email.
3. **One action** — One link that matters.
4. **Truth** — Do not imply the reader did something they did not do.

**Deliberately not done**
- Fake personalization.
- Hidden unsubscribe.
- An email with no trigger.

Next: Lena Ortiz sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Fake personalization.
- Hidden unsubscribe.
- An email with no trigger.

## Related skills

- `sales-email-sequence`
- `customer-health-score`
