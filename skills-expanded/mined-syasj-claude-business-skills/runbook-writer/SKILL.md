---
name: runbook-writer
description: "Write a runbook a tired on-call engineer can follow, with checks, stops, and escalation. Use when the user mentions write a runbook, ops procedure, on-call runbook, support procedure engineering, or asks for a runbook. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'runbook-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Runbook Writer

Write a runbook a tired on-call engineer can follow, with checks, stops, and escalation.

## When to use this skill

Use this skill when the user:

- write a runbook
- ops procedure
- on-call runbook
- support procedure engineering

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

- The alert or symptom
- The checks that are safe
- The fix that is allowed
- Who to escalate to

## Workflow


### 1. Symptom

What the human sees, in the alert's language.
### 2. Impact

How to tell whether users are hurt, using signals they have.
### 3. Checks

Safe, read-only checks first. Do not include destructive commands as the first step.
### 4. Mitigation

The allowed mitigation, with the stop condition. No improvised production surgery.
### 5. Escalation

When to stop and call the owner.
### 6. After

What to record for the postmortem. Keep secrets out of the runbook.

## Output

Deliver a **runbook**.

- Purpose of this runbook, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a runbook by 30 September 2026. A draft runbook starts by deleting a production table if an alert fires.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A draft runbook starts by deleting a production table if an alert fires.

The alert or symptom: Checkout service, recorded 14 September 2026. No supporting file attached
The checks that are safe: Checkout service, recorded 14 September 2026. No supporting file attached
The fix that is allowed: Checkout service, recorded 14 September 2026. No supporting file attached
Who to escalate to: Aisha Rahman, engineering lead
```

### Example outcome

**Runbook**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Starts with read-only checks, removes the destructive first step, and escalates before any data deletion.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The alert or symptom | Checkout service, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The checks that are safe | Checkout service, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The fix that is allowed | Checkout service, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who to escalate to | Aisha Rahman, engineering lead | Needs confirmation |

**How this draft was built**

**1. Symptom**  
What the human sees, in the alert's language.

**2. Impact**  
How to tell whether users are hurt, using signals they have.

**3. Checks**  
Safe, read-only checks first. Do not include destructive commands as the first step.

**4. Mitigation**  
The allowed mitigation, with the stop condition. No improvised production surgery.

**5. Escalation**  
When to stop and call the owner.

**Deliberately not done**
- Destructive commands with no stop condition.
- A runbook that requires hero knowledge.
- Secrets embedded in the steps.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Destructive commands with no stop condition.
- A runbook that requires hero knowledge.
- Secrets embedded in the steps.

## Related skills

- `oncall-handoff`
- `incident-postmortem`
