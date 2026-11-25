---
name: platform-readiness
description: "Review whether a platform or internal tool is ready for other teams to depend on. Use when the user mentions platform readiness, internal platform review, is this ready for other teams, paved road review, or asks for a platform readiness review. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'platform-readiness' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Platform Readiness

Review whether a platform or internal tool is ready for other teams to depend on.

## When to use this skill

Use this skill when the user:

- platform readiness
- internal platform review
- is this ready for other teams
- paved road review

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

- The users inside the company
- The promised interface
- Support model
- Docs and SLOs they claim

## Workflow


### 1. User

The internal team and the job they will do on the platform.
### 2. Interface

The stable contract. If every consumer forks the internals, it is not ready.
### 3. Operability

On-call, migration path, and a stated limit. Do not invent an SLO.
### 4. Docs

A new team can complete the golden path from the docs the user has. Gaps are the finding.
### 5. Support

Who answers in the first month, and what is not supported.
### 6. Adoption

One team first, then a wider invite. A mandate with no golden path will be bypassed.

## Output

Deliver a **platform readiness review**.

- Purpose of this platform readiness review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a platform readiness review by 30 September 2026. A platform team wants every service to migrate next month, and the quickstart is a stub.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A platform team wants every service to migrate next month, and the quickstart is a stub.

The users inside the company: Checkout service, recorded 14 September 2026. No supporting file attached
The promised interface: none written down beyond the ask
Support model: Invoice job, last reviewed 14 September 2026. No owner named since
Docs and SLOs they claim: the draft sentence is broader than the note
```

### Example outcome

**Platform readiness review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the mandate, names the quickstart gap, and recommends one adopting team.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The users inside the company | Checkout service, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The promised interface | none written down beyond the ask | Carried into the draft |
| Support model | Invoice job, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Docs and SLOs they claim | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. User**  
The internal team and the job they will do on the platform.

**2. Interface**  
The stable contract. If every consumer forks the internals, it is not ready.

**3. Operability**  
On-call, migration path, and a stated limit. Do not invent an SLO.

**4. Docs**  
A new team can complete the golden path from the docs the user has. Gaps are the finding.

**5. Support**  
Who answers in the first month, and what is not supported.

**Deliberately not done**
- A company-wide mandate with no docs.
- An invented uptime promise.
- No owner for questions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A company-wide mandate with no docs.
- An invented uptime promise.
- No owner for questions.

## Related skills

- `technical-design-doc`
- `documentation-as-code`
