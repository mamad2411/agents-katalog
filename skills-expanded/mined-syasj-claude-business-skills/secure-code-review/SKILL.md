---
name: secure-code-review
description: "Review a change for defensive security issues and request fixes, without writing an exploit. Use when the user mentions security review a PR, secure code review, auth review, secrets in code, or asks for a secure code review. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'secure-code-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Secure Code Review

Review a change for defensive security issues and request fixes, without writing an exploit.

## When to use this skill

Use this skill when the user:

- security review a PR
- secure code review
- auth review
- secrets in code

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Defensive use only. Do not write exploits, payloads, bypasses, malware, or intrusion steps. Describe controls, ownership, detection, and safe verification.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The change description
- Auth and data paths
- How secrets are handled
- Threats they are worried about

## Workflow


### 1. Step 1

Check authentication and authorization on the new path. Missing checks are a blocking finding.
### 2. Step 2

Look for secrets, tokens, or keys in the diff. Tell them to remove and rotate. Do not copy the secret into the review.
### 3. Check input handling at trust boundaries in general terms

validate, encode, and parameterize. Do not provide payloads.
### 4. Step 4

Review logging to ensure secrets and personal data are not written.
### 5. Step 5

Ask for a regression test of the denied path.
### 6. Step 6

If you suspect a vulnerability, describe the impact and the fix, not a working attack.

## Output

Deliver a **secure code review**.

- Purpose of this secure code review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a secure code review by 30 September 2026. A pull request logs a session token while debugging a login bug.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A pull request logs a session token while debugging a login bug.

The change description: requested 14 September 2026. Not yet approved
Auth and data paths: Access review Q3 and one other, both unconfirmed as of 14 September 2026
How secrets are handled: Endpoint patch ring 2, last reviewed 14 September 2026. No owner named since
Threats they are worried about: Endpoint patch ring 2. Partly documented: the what is written down, the who is not
```

### Example outcome

**Secure code review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Requires the log removed, the token rotated, and no token reprinted in the comment.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change description | requested 14 September 2026. Not yet approved | Needs confirmation |
| Auth and data paths | Access review Q3 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| How secrets are handled | Endpoint patch ring 2, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Threats they are worried about | Endpoint patch ring 2. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Check authentication and authorization on the new path. Missing checks are a blocking finding**

**2. Look for secrets, tokens, or keys in the diff. Tell them to remove and rotate. Do not copy the secret into the review**

**3. Check input handling at trust boundaries in general terms**  
validate, encode, and parameterize. Do not provide payloads.

**4. Review logging to ensure secrets and personal data are not written**

**5. Ask for a regression test of the denied path**

**Deliberately not done**
- Payloads or proof-of-concept exploits.
- Repeating a live secret.
- Approving a missing authorization check.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Payloads or proof-of-concept exploits
- Repeating a live secret
- Approving a missing authorization check

## Related skills

- `secrets-handling`
- `code-review-standard`
