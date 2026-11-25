---
name: code-review-standard
description: "Review a change for correctness, risk, and clarity, and write comments a teammate can act on. Use when the user mentions code review, review this PR, pull request review, review comments, or asks for a code review. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'code-review-standard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Code Review Standard

Review a change for correctness, risk, and clarity, and write comments a teammate can act on.

## When to use this skill

Use this skill when the user:

- code review
- review this PR
- pull request review
- review comments

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

- The change and its stated intent
- Tests included or missing
- Risky areas: data, auth, migrations
- Team conventions the user pointed to

## Workflow


### 1. Intent

Restate what the change is for. If the description is empty, ask for it before nitpicking style.
### 2. Correctness

Walk the main path and the failure path. Point to the line and the concrete failure.
### 3. Risk

Call out auth, data loss, migrations, and secrets. Do not request a bypass of a security control.
### 4. Tests

Name the missing test that would have caught the bug you see. Do not demand tests for their own sake with no risk.
### 5. Comments

Specific, kind, and ranked. Blocking issues are separate from nits.
### 6. Scope

A drive-by rewrite is a suggestion, not a block, unless the change is unsafe.

## Output

Deliver a **code review**.

- Purpose of this code review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a code review by 30 September 2026. A PR changes an authorization check and has no test for the denied path.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A PR changes an authorization check and has no test for the denied path.

The change and its stated intent: requested 14 September 2026. Not yet approved
Tests included or missing: Status page, recorded 14 September 2026. No supporting file attached
Risky areas: data, auth, migrations: data: in the file; auth: not in the file; migrations: open
Team conventions the user pointed to: two people on shift, one off
```

### Example outcome

**Code review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks on the missing denied-path test and does not suggest skipping the check.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change and its stated intent | requested 14 September 2026. Not yet approved | Needs confirmation |
| Tests included or missing | Status page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Risky areas: data, auth, migrations | data: in the file; auth: not in the file; migrations: open | Carried into the draft |
| Team conventions the user pointed to | two people on shift, one off | Needs confirmation |

**How this draft was built**

**1. Intent**  
Restate what the change is for. If the description is empty, ask for it before nitpicking style.

**2. Correctness**  
Walk the main path and the failure path. Point to the line and the concrete failure.

**3. Risk**  
Call out auth, data loss, migrations, and secrets. Do not request a bypass of a security control.

**4. Tests**  
Name the missing test that would have caught the bug you see. Do not demand tests for their own sake with no risk.

**5. Comments**  
Specific, kind, and ranked. Blocking issues are separate from nits.

**Deliberately not done**
- Style nits before understanding intent.
- Approving a migration with no rollback note.
- Asking the author to disable a security check to get the diff smaller.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Style nits before understanding intent.
- Approving a migration with no rollback note.
- Asking the author to disable a security check to get the diff smaller.

## Related skills

- `pr-description`
- `secure-code-review`
