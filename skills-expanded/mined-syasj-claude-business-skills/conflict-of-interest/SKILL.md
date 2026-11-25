---
name: conflict-of-interest
description: "Structure a conflict-of-interest disclosure so a reviewer can see the interest and the decision it touches. Use when the user mentions conflict of interest, COI disclosure, related party, disclose a conflict, or asks for a conflict disclosure. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'conflict-of-interest' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Conflict of Interest Disclosure

Structure a conflict-of-interest disclosure so a reviewer can see the interest and the decision it touches.

## When to use this skill

Use this skill when the user:

- conflict of interest
- COI disclosure
- related party
- disclose a conflict

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The interest
- The decision or process it touches
- Who else knows
- The review path

## Workflow


### 1. Describe the interest in plain language

financial, family, or outside role, as the user stated.
### 2. Step 2

Name the decision or vendor it could affect.
### 3. Step 3

Propose recusal or a review, using their policy if they supplied one.
### 4. Step 4

Do not help hide the interest.
### 5. Step 5

Minimize unrelated personal details.
### 6. Step 6

Record the reviewer's decision once they make it. Do not invent an approval.

## Output

Deliver a **conflict disclosure**.

- Purpose of this conflict disclosure, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a conflict disclosure by 30 September 2026. An employee wants the disclosure to omit that their sibling owns the bidding vendor.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An employee wants the disclosure to omit that their sibling owns the bidding vendor.

The interest: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The decision or process it touches: An employee wants the disclosure to omit that their sibling owns the bidding vendor
Who else knows: Priya Shah, controller
The review path: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Conflict disclosure — draft ready to send**

> To: the recipient named in the file
> From: Priya Shah, controller, Northline Studio
> Date: 14 September 2026

---

Hello,

Includes the sibling relationship and recommends recusal from the award.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Priya Shah
controller, Northline Studio

---

**How this draft was checked**

1. **Describe the interest in plain language** — financial, family, or outside role, as the user stated.
2. **Name the decision or vendor it could affect**
3. **Propose recusal or a review, using their policy if they supplied one**
4. **Do not help hide the interest**

**Deliberately not done**
- Hiding an interest.
- Unrelated personal details.
- A fake approval.

Next: Priya Shah sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Hiding an interest
- Unrelated personal details
- A fake approval

## Related skills

- `gifts-and-entertainment`
- `procurement-award-note`
