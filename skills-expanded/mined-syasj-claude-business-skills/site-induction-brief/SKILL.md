---
name: site-induction-brief
description: "Brief a contractor on the site rules the user listed, including what they must not bypass. Use when the user mentions site induction, contractor induction, site rules, orientation brief, or asks for a induction brief. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'site-induction-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Site Induction Brief

Brief a contractor on the site rules the user listed, including what they must not bypass.

## When to use this skill

Use this skill when the user:

- site induction
- contractor induction
- site rules
- orientation brief

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational drafts only. Do not bypass isolation, lockout, permits, or reporting duties. Do not write instructions to conceal a release or to operate outside the site's limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The rules they listed
- Required tickets
- The muster point
- Who stops a job

## Workflow


### 1. Step 1

List only rules they provided.
### 2. Step 2

Name the tickets required before entry.
### 3. Step 3

State the muster point.
### 4. Step 4

Say who can stop a job.
### 5. Step 5

Do not shorten a lockout rule.
### 6. Step 6

Do not add a rule you remember from another site.

## Output

Deliver a **induction brief**.

- Purpose of this induction brief, in two sentences.
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

A contractor starts Thursday. Their draft induction drops the lockout step to save ten minutes. The site rules Devon sent include lockout, a muster point at the south gate, and a H2S ticket before entry.

### Example data

```text
start: Thu 18 Sep 2026
rules he sent: lockout before any line is opened, muster south gate, stop-work authority is any person on site
ticket required: H2S, checked at the gate
draft change: drop lockout to save 10 minutes
```

### Example outcome

**Induction brief**
Before entry: H2S ticket checked at the gate. No ticket, no entry.
Lockout stays in the brief. It is not cut to save ten minutes.
Muster: south gate.
Who can stop a job: any person on site.
This brief uses his list only. It does not add another site's rules, and it does not shorten his.

## Anti-patterns

- A shortened lockout rule
- Entry without the ticket they require
- Muster left blank

## Related skills

- `hse-observation`
- `isolation-work-plan`
