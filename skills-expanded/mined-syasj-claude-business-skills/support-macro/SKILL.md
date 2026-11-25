---
name: support-macro
description: "Draft a support reply that answers the question, states the limit, and does not invent a policy. Use when the user mentions support macro, canned reply, help desk reply, customer reply draft, or asks for a support reply. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'support-macro' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Support Macro

Draft a support reply that answers the question, states the limit, and does not invent a policy.

## When to use this skill

Use this skill when the user:

- support macro
- canned reply
- help desk reply
- customer reply draft

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The customer's question
- The policy that applies
- What the agent can offer
- The tone

## Workflow


### 1. Step 1

Answer the question in the first lines.
### 2. Step 2

State the policy they supplied. If no policy was supplied, do not invent one.
### 3. Step 3

Say what the customer should do next.
### 4. Step 4

Include what you cannot do, plainly.
### 5. Step 5

Keep a human tone without fake empathy padding.
### 6. Step 6

Do not ask for passwords, full card numbers, or one-time codes.

## Output

Deliver a **support reply**.

- Purpose of this support reply, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a support reply by 30 September 2026. A customer asks for a refund and the draft apologizes for three paragraphs without stating the refund rule.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A customer asks for a refund and the draft apologizes for three paragraphs without stating the refund rule.

The customer's question: A customer asks for a refund and the draft apologizes for three paragraphs without stating the refund rule
The policy that applies: their one-page rule dated 2 Mar 2026. No exception log
What the agent can offer: CAD 180, dates not set, cap not set
The tone: plain, for people who already know the context. No house guide attached
```

### Example outcome

**Support reply — draft ready to send**

> To: the recipient named in the file
> From: Rita Santos, support lead, Fieldnote
> Date: 14 September 2026

---

Hello,

States the known rule or says the agent must check it, and asks for no secrets.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Rita Santos
support lead, Fieldnote

---

**How this draft was checked**

1. **Answer the question in the first lines**
2. **State the policy they supplied. If no policy was supplied, do not invent one**
3. **Say what the customer should do next**
4. **Include what you cannot do, plainly**

**Deliberately not done**
- Invented policy.
- Asking for a password.
- A reply that never answers.

Next: Rita Santos sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Invented policy
- Asking for a password
- A reply that never answers

## Related skills

- `service-recovery`
- `knowledge-base-article`
