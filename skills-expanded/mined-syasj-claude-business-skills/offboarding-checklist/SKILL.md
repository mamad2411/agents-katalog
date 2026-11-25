---
name: offboarding-checklist
description: "Plan a respectful departure: access, knowledge, equipment, and a clean final pay question list. Use when the user mentions offboarding, employee exit, leaver checklist, termination logistics, or asks for a offboarding checklist. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'offboarding-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Offboarding Checklist

Plan a respectful departure: access, knowledge, equipment, and a clean final pay question list.

## When to use this skill

Use this skill when the user:

- offboarding
- employee exit
- leaver checklist
- termination logistics

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Last day
- Role and critical knowledge
- Systems the user says they can access
- Whether the exit is voluntary, as stated

## Workflow


### 1. Knowledge

What must be handed over before the last day, and to whom. A password share is not a handover. Reset access instead.
### 2. Access

List systems to remove on a schedule the user controls. Do not include instructions for locking someone out in a harmful or deceptive way.
### 3. Equipment and accounts

Company devices and accounts. Personal data is handled according to their policy, not by rummaging.
### 4. Final pay and benefits

Questions for payroll, not answers invented from labor law.
### 5. Exit conversation

A respectful outline. No gotcha interview. No request to badmouth the person to the remaining team.
### 6. Customer continuity

Who owns live work. Customers should not discover the gap themselves.

## Output

Deliver a **offboarding checklist**.

- Purpose of this offboarding checklist, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an offboarding checklist by 30 September 2026. A specialist with sole access to a billing tool is leaving in ten days.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A specialist with sole access to a billing tool is leaving in ten days.

Last day: Open coordinator role, last reviewed 14 September 2026. No owner named since
Role and critical knowledge: Jordan Hale and one other, both unconfirmed as of 14 September 2026
Systems the user says they can access: the one named in the ask. Version and owner not recorded
Whether the exit is voluntary, as stated: Jordan Hale. Partly documented: the what is written down, the who is not
```

### Example outcome

**Offboarding checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Transfers knowledge, schedules access removal without password sharing, and names the customer owner.

**Checklist**

- [x] **Last day** — Open coordinator role, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [x] **Role and critical knowledge** — Jordan Hale and one other, both unconfirmed as of 14 September 2026  
      Evidenced in the file
- [x] **Systems the user says they can access** — the one named in the ask. Version and owner not recorded  
      Evidenced in the file
- [ ] **Whether the exit is voluntary, as stated** — Jordan Hale. Partly documented: the what is written down, the who is not  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Knowledge
2. Access
3. Equipment and accounts
4. Final pay and benefits
5. Exit conversation

**Deliberately not done**
- Sharing passwords as the handover.
- A gossip script for the remaining team.
- Invented final-pay law.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Chris Adeyemi closes the open items before 30 September 2026.

## Anti-patterns

- Sharing passwords as the handover.
- A gossip script for the remaining team.
- Invented final-pay law.

## Related skills

- `onboarding-plan`
- `employee-relations-intake`
- `knowledge-base-article`
