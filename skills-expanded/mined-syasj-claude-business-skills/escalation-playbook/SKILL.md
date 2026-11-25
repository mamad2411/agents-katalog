---
name: escalation-playbook
description: "Write an escalation path with levels, clocks, and the decision each level can make. Use when the user mentions escalation playbook, escalate a ticket, severity path, customer escalation, or asks for a escalation playbook. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'escalation-playbook' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Escalation Playbook

Write an escalation path with levels, clocks, and the decision each level can make.

## When to use this skill

Use this skill when the user:

- escalation playbook
- escalate a ticket
- severity path
- customer escalation

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

- Severity definitions
- Who is on each level
- Clocks they can staff
- Customer communication owner

## Workflow


### 1. Step 1

Define severity by impact, not by who shouted.
### 2. Step 2

Each level has a clock and a decision it can make.
### 3. Step 3

Name the customer communication owner so engineering is not surprised by a promise.
### 4. Step 4

Include how to de-escalate when impact falls.
### 5. Step 5

Record what must be true before waking an executive.
### 6. Step 6

Do not design a path that hides a safety or security issue from the proper owner.

## Output

Deliver a **escalation playbook**.

- Purpose of this escalation playbook, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs an escalation playbook by 30 September 2026. Every angry email is marked severe, so the on-call ignores the queue.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Every angry email is marked severe, so the on-call ignores the queue.

Severity definitions: Ticket 4418. Partly documented: the what is written down, the who is not
Who is on each level: Rita Santos, support lead
Clocks they can staff: two people on shift
Customer communication owner: Rita Santos, support lead
```

### Example outcome

**Escalation playbook**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Defines severity by impact and reserves executive escalation for a written trigger.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Severity definitions | Ticket 4418. Partly documented: the what is written down, the who is not | Needs confirmation |
| Who is on each level | Rita Santos, support lead | Carried into the draft |
| Clocks they can staff | two people on shift | Carried into the draft |
| Customer communication owner | Rita Santos, support lead | Needs confirmation |

**How this draft was built**

**1. Define severity by impact, not by who shouted**

**2. Each level has a clock and a decision it can make**

**3. Name the customer communication owner so engineering is not surprised by a promise**

**4. Include how to de-escalate when impact falls**

**5. Record what must be true before waking an executive**

**Deliberately not done**
- Severity set by loudness.
- An executive ping with no path.
- Hidden security issues.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Severity set by loudness
- An executive ping with no path
- Hidden security issues

## Related skills

- `incident-response-coord`
- `sla-design`
