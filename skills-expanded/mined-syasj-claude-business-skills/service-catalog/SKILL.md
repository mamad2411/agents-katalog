---
name: service-catalog
description: "Write a service catalog entry that tells an internal customer what they can request, how long it takes, and what is not included. Use when the user mentions service catalog, internal service definition, what does this team offer, request path, or asks for a service catalog entry. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'service-catalog' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Service Catalog Entry

Write a service catalog entry that tells an internal customer what they can request, how long it takes, and what is not included.

## When to use this skill

Use this skill when the user:

- service catalog
- internal service definition
- what does this team offer
- request path

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The service
- Who may request it
- The standard lead time they can meet
- Exclusions

## Workflow


### 1. Step 1

Describe the service as an outcome, not as a department name.
### 2. Step 2

Say who may request it and how.
### 3. Step 3

Publish a lead time they have evidence they can meet. If they cannot, mark the time as unknown.
### 4. Step 4

List exclusions so hidden work does not arrive as emergencies.
### 5. Step 5

Name the owner and the escalation.
### 6. Step 6

Add how demand is reviewed when the queue exceeds capacity.

## Output

Deliver a **service catalog entry**.

- Purpose of this service catalog entry, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a service catalog entry by 30 September 2026. An internal team is judged on a two-day turnaround it has never hit.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

An internal team is judged on a two-day turnaround it has never hit.

The service: the one named in the ask. Version and owner not recorded
Who may request it: Diane Cho, operations manager
The standard lead time they can meet: 21 days
Exclusions: Tuesday shift is open. SOP 118 receiving was raised verbally and never logged
```

### Example outcome

**Service catalog entry**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
An entry with a truthful lead time or an explicit unknown, plus exclusions.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The service | the one named in the ask. Version and owner not recorded | Needs confirmation |
| Who may request it | Diane Cho, operations manager | Carried into the draft |
| The standard lead time they can meet | 21 days | Carried into the draft |
| Exclusions | Tuesday shift is open. SOP 118 receiving was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. Describe the service as an outcome, not as a department name**

**2. Say who may request it and how**

**3. Publish a lead time they have evidence they can meet. If they cannot, mark the time as unknown**

**4. List exclusions so hidden work does not arrive as emergencies**

**5. Name the owner and the escalation**

**Deliberately not done**
- A catalog with no exclusions.
- A lead time they cannot meet.
- A request path only insiders know.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A catalog with no exclusions
- A lead time they cannot meet
- A request path only insiders know

## Related skills

- `sla-design`
- `queue-health`
