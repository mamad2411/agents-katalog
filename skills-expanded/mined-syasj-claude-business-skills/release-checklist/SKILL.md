---
name: release-checklist
description: "Run a release checklist that confirms scope, migrations, monitoring, and rollback before tagging. Use when the user mentions release checklist, ship checklist, release review, go no-go release, or asks for a release checklist. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'release-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Release Checklist

Run a release checklist that confirms scope, migrations, monitoring, and rollback before tagging.

## When to use this skill

Use this skill when the user:

- release checklist
- ship checklist
- release review
- go no-go release

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The intended scope
- Migrations
- Monitoring
- Rollback

## Workflow


### 1. Scope

What is in the release, matched to what was tested. Surprise commits are a stop.
### 2. Migrations

Order, backup or rollback, and the owner watching them.
### 3. Config and flags

What must be set in production. Do not include secret values. Name the keys only.
### 4. Monitoring

The dashboard or alert the owner will watch for the first hour.
### 5. Rollback

The command or flag path, already known, not invented during the incident.
### 6. Decision

Ship or hold, with the hold reason written.

## Output

Deliver a **release checklist**.

- Purpose of this release checklist, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a release checklist by 30 September 2026. A release includes a migration that the on-call has not seen, and the checklist says LGTM.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A release includes a migration that the on-call has not seen, and the checklist says LGTM.

The intended scope: this decision only
Migrations: Checkout service, last reviewed 14 September 2026. No owner named since
Monitoring: Invoice job. Partly documented: the what is written down, the who is not
Rollback: Invoice job, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Release checklist**
Fieldnote · 14 September 2026 · Due 30 September 2026

**Decision**
A hold until the migration owner is named and the rollback is written, with no secret values added.

**Checklist**

- [x] **The intended scope** — this decision only  
      Evidenced in the file
- [x] **Migrations** — Checkout service, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [x] **Monitoring** — Invoice job. Partly documented: the what is written down, the who is not  
      Evidenced in the file
- [ ] **Rollback** — Invoice job, last reviewed 14 September 2026. No owner named since  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Scope
2. Migrations
3. Config and flags
4. Monitoring
5. Rollback

**Deliberately not done**
- Secret values in the checklist.
- A ship decision with no rollback.
- Scope nobody tested.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Aisha Rahman closes the open items before 30 September 2026.

## Anti-patterns

- Secret values in the checklist.
- A ship decision with no rollback.
- Scope nobody tested.

## Related skills

- `launch-readiness`
- `feature-flag-rollout`
