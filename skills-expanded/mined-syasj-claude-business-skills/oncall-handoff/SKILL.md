---
name: oncall-handoff
description: "Write an on-call handoff that tells the next person what is on fire, what is quiet, and how to escalate. Use when the user mentions oncall handoff, handoff notes, pager handoff, shift handoff engineering, or asks for a on-call handoff. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'oncall-handoff' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# On-Call Handoff

Write an on-call handoff that tells the next person what is on fire, what is quiet, and how to escalate.

## When to use this skill

Use this skill when the user:

- oncall handoff
- handoff notes
- pager handoff
- shift handoff engineering

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

- Open incidents
- Fragile systems
- Recent changes
- Escalation path

## Workflow


### 1. Open items

What is paging or degraded, the current theory, and the next check. Theories are labeled.
### 2. Recent changes

Deploys or migrations the next person should know about, from the user's list.
### 3. Fragile spots

Known risks for this shift, with the runbook link if one exists. Do not invent a runbook.
### 4. Escalation

Who to wake and for what. A handoff with no escalation path is incomplete.
### 5. Noise

Alerts that are known noise, so the next person does not chase them blind. Do not tell them to ignore a security alert without an owner.
### 6. Tone

Short and operational. No heroics required.

## Output

Deliver a **on-call handoff**.

- Purpose of this on-call handoff, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an on-call handoff by 30 September 2026. The outgoing engineer writes 'should be fine' after a migration that has not been verified.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The outgoing engineer writes 'should be fine' after a migration that has not been verified.

Open incidents: Checkout service, first seen 14 September 2026. No root cause recorded yet
Fragile systems: the one named in the ask. Version and owner not recorded
Recent changes: requested 14 September 2026. Not yet approved
Escalation path: Checkout service, first seen 14 September 2026. No root cause recorded yet
```

### Example outcome

**On-call handoff**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Lists the unverified migration, the check to run, and the escalation owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Open incidents | Checkout service, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| Fragile systems | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Recent changes | requested 14 September 2026. Not yet approved | Carried into the draft |
| Escalation path | Checkout service, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |

**How this draft was built**

**1. Open items**  
What is paging or degraded, the current theory, and the next check. Theories are labeled.

**2. Recent changes**  
Deploys or migrations the next person should know about, from the user's list.

**3. Fragile spots**  
Known risks for this shift, with the runbook link if one exists. Do not invent a runbook.

**4. Escalation**  
Who to wake and for what. A handoff with no escalation path is incomplete.

**5. Noise**  
Alerts that are known noise, so the next person does not chase them blind. Do not tell them to ignore a security alert without an owner.

**Deliberately not done**
- A handoff that says 'all quiet' when an incident is open.
- Invented runbook links.
- Telling the next person to silence a security page with no owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A handoff that says 'all quiet' when an incident is open.
- Invented runbook links.
- Telling the next person to silence a security page with no owner.

## Related skills

- `runbook-writer`
- `incident-postmortem`
