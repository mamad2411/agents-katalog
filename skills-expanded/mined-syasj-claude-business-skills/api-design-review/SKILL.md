---
name: api-design-review
description: "Review an API for consistency, failure behavior, and compatibility, without turning the review into a style hobby. Use when the user mentions API review, API design, endpoint review, breaking change review, or asks for a API review. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'api-design-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# API Design Review

Review an API for consistency, failure behavior, and compatibility, without turning the review into a style hobby.

## When to use this skill

Use this skill when the user:

- API review
- API design
- endpoint review
- breaking change review

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

- The proposed contract
- Consumers
- Compatibility promises
- Auth model they use

## Workflow


### 1. Consumer job

What the caller is trying to do. Endpoints that do not serve a job are a finding.
### 2. Contract

Names, types, and error shapes. Inconsistent errors are a finding if their standard exists.
### 3. Failure

What the client should do on timeout, conflict, and unauthorized. Silence is a gap.
### 4. Compatibility

What breaks existing callers. A breaking change needs a version or a migration note.
### 5. Auth

Which identity is required. Do not suggest making an endpoint public to simplify a client.
### 6. Idempotency

Where retries could double-charge or double-create, ask for an idempotency story.

## Output

Deliver a **API review**.

- Purpose of this API review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an API review by 30 September 2026. A new billing endpoint has no idempotency key and retries would create a second charge.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A new billing endpoint has no idempotency key and retries would create a second charge.

The proposed contract: unsigned draft, 8 pages, no signature date
Consumers: Invoice job. Partly documented: the what is written down, the who is not
Compatibility promises: none written down beyond the ask
Auth model they use: Checkout service and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Api review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks on the double-charge retry and refuses any suggestion to skip authentication.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The proposed contract | unsigned draft, 8 pages, no signature date | Needs confirmation |
| Consumers | Invoice job. Partly documented: the what is written down, the who is not | Carried into the draft |
| Compatibility promises | none written down beyond the ask | Carried into the draft |
| Auth model they use | Checkout service and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Consumer job**  
What the caller is trying to do. Endpoints that do not serve a job are a finding.

**2. Contract**  
Names, types, and error shapes. Inconsistent errors are a finding if their standard exists.

**3. Failure**  
What the client should do on timeout, conflict, and unauthorized. Silence is a gap.

**4. Compatibility**  
What breaks existing callers. A breaking change needs a version or a migration note.

**5. Auth**  
Which identity is required. Do not suggest making an endpoint public to simplify a client.

**Deliberately not done**
- A public endpoint suggested for convenience.
- A breaking change with no migration.
- No error behavior.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A public endpoint suggested for convenience.
- A breaking change with no migration.
- No error behavior.

## Related skills

- `technical-design-doc`
- `secure-code-review`
