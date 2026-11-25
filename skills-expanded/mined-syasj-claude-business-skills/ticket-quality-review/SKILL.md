---
name: ticket-quality-review
description: "Review support ticket quality for resolution, tone, and whether the article or product should change. Use when the user mentions ticket quality, QA support tickets, review these tickets, support QA, or asks for a ticket quality review. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ticket-quality-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Ticket Quality Review

Review support ticket quality for resolution, tone, and whether the article or product should change.

## When to use this skill

Use this skill when the user:

- ticket quality
- QA support tickets
- review these tickets
- support QA

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

- The tickets or summaries
- The rubric they use
- Recurring issues
- What agents are allowed to do

## Workflow


### 1. Step 1

Score against their rubric. If they have none, use resolution, accuracy, and next step, and label that as a proposal.
### 2. Step 2

Check that the reply answered the ask and did not invent a policy.
### 3. Step 3

Look for repeated issues that belong in a macro or a product fix.
### 4. Step 4

Note if agents are asking for secrets. That is a finding.
### 5. Step 5

Give coaching on the pattern, not a pile of nits.
### 6. Step 6

Recommend one article or product change if the tickets show a system gap.

## Output

Deliver a **ticket quality review**.

- Purpose of this ticket quality review, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a ticket quality review by 30 September 2026. Several tickets ask customers for their password to 'speed up' the fix.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Several tickets ask customers for their password to 'speed up' the fix.

The tickets or summaries: Ticket 4412, recorded 14 September 2026. No supporting file attached
The rubric they use: Ticket 4412, recorded 14 September 2026. No supporting file attached
Recurring issues: Ticket 4412, last reviewed 14 September 2026. No owner named since
What agents are allowed to do: Ticket 4420, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Ticket quality review**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag the password request as a stop-now finding and names the pattern.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The tickets or summaries | Ticket 4412, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The rubric they use | Ticket 4412, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Recurring issues | Ticket 4412, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| What agents are allowed to do | Ticket 4420, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Score against their rubric. If they have none, use resolution, accuracy, and next step, and label that as a proposal**

**2. Check that the reply answered the ask and did not invent a policy**

**3. Look for repeated issues that belong in a macro or a product fix**

**4. Note if agents are asking for secrets. That is a finding**

**5. Give coaching on the pattern, not a pile of nits**

**Deliberately not done**
- Coaching style before checking accuracy.
- Ignoring a secret request.
- A review with no pattern.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Coaching style before checking accuracy
- Ignoring a secret request
- A review with no pattern

## Related skills

- `support-macro`
- `knowledge-base-article`
