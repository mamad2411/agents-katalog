---
name: observability-plan
description: "Specify the logs, metrics, and traces a service needs to debug a user-facing failure. Use when the user mentions observability plan, what should we log, metrics and traces, instrumentation plan, or asks for a observability plan. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'observability-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Observability Plan

Specify the logs, metrics, and traces a service needs to debug a user-facing failure.

## When to use this skill

Use this skill when the user:

- observability plan
- what should we log
- metrics and traces
- instrumentation plan

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

- The user-facing failure you must detect
- Existing signals
- Cardinality and privacy limits
- Who is on call

## Workflow


### 1. Question

The production question the signal must answer. Signals without a question are noise.
### 2. Golden signals

Latency, errors, traffic, and saturation only where they match the service. Do not dump a template.
### 3. Logs

Structured fields that help debug, excluding secrets, tokens, and full payment data.
### 4. Traces

Where a trace would beat another log line, if they already use tracing. Do not mandate a vendor.
### 5. Alerts

Page only on user pain or imminent user pain. A page on every warning trains people to ignore pages.
### 6. Ownership

Who responds, and where the runbook will live.

## Output

Deliver a **observability plan**.

- Purpose of this observability plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an observability plan by 30 September 2026. A plan logs the full Authorization header to 'make debugging easier'.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A plan logs the full Authorization header to 'make debugging easier'.

The user-facing failure you must detect: Checkout service, first seen 14 September 2026. No root cause recorded yet
Existing signals: Invoice job, last reviewed 14 September 2026. No owner named since
Cardinality and privacy limits: email and billing address. They said no health data
Who is on call: Aisha Rahman, engineering lead
```

### Example outcome

**Observability plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Forbids that header, specifies a request id, and pages only on user-facing errors.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The user-facing failure you must detect | Checkout service, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| Existing signals | Invoice job, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Cardinality and privacy limits | email and billing address. They said no health data | Carried into the draft |
| Who is on call | Aisha Rahman, engineering lead | Needs confirmation |

**How this draft was built**

**1. Question**  
The production question the signal must answer. Signals without a question are noise.

**2. Golden signals**  
Latency, errors, traffic, and saturation only where they match the service. Do not dump a template.

**3. Logs**  
Structured fields that help debug, excluding secrets, tokens, and full payment data.

**4. Traces**  
Where a trace would beat another log line, if they already use tracing. Do not mandate a vendor.

**5. Alerts**  
Page only on user pain or imminent user pain. A page on every warning trains people to ignore pages.

**Deliberately not done**
- Logging secrets or card numbers.
- Paging on every warning.
- A vendor mandate disguised as a plan.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Logging secrets or card numbers.
- Paging on every warning.
- A vendor mandate disguised as a plan.

## Related skills

- `logging-and-detection`
- `slo-error-budget`
