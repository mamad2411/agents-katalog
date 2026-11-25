---
name: documentation-as-code
description: "Write or repair technical docs so a new teammate can complete a task without a hallway conversation. Use when the user mentions write docs, README review, developer documentation, runbook versus docs, or asks for a documentation update. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'documentation-as-code' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Documentation As Code

Write or repair technical docs so a new teammate can complete a task without a hallway conversation.

## When to use this skill

Use this skill when the user:

- write docs
- README review
- developer documentation
- runbook versus docs

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

- The task a new person must complete
- The current doc
- The commands or paths that are true
- The owner

## Workflow


### 1. Audience and task

What the reader is trying to do. A doc with no task becomes a junk drawer.
### 2. Truth

Steps match the repo or the user's confirmation. Do not invent flags, paths, or environment variables.
### 3. Prerequisites

What must exist first, including access, without asking for secrets to be pasted into the doc.
### 4. Failure

The common failure and the next check.
### 5. Ownership

Who updates the doc when the system changes.
### 6. Cut

Remove stale sections rather than adding a warning on top of a wrong step.

## Output

Deliver a **documentation update**.

- Purpose of this documentation update, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a documentation update by 30 September 2026. A README says 'run the script' and the script path does not exist.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A README says 'run the script' and the script path does not exist.

The task a new person must complete: A README says 'run the script' and the script path does not exist. Stated once, in the ask. Not written down anywhere else
The current doc: Checkout service, recorded 14 September 2026. No supporting file attached
The commands or paths that are true: Checkout service, recorded 14 September 2026. No supporting file attached
The owner: Aisha Rahman, engineering lead
```

### Example outcome

**Documentation update**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either uses the real path the user confirmed or marks the step unknown, and removes the stale command.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The task a new person must complete | A README says 'run the script' and the script path does not exist. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The current doc | Checkout service, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The commands or paths that are true | Checkout service, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The owner | Aisha Rahman, engineering lead | Needs confirmation |

**How this draft was built**

**1. Audience and task**  
What the reader is trying to do. A doc with no task becomes a junk drawer.

**2. Truth**  
Steps match the repo or the user's confirmation. Do not invent flags, paths, or environment variables.

**3. Prerequisites**  
What must exist first, including access, without asking for secrets to be pasted into the doc.

**4. Failure**  
The common failure and the next check.

**5. Ownership**  
Who updates the doc when the system changes.

**Deliberately not done**
- Invented commands.
- Secrets in the example env file.
- A README that does not say how to run the project.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented commands.
- Secrets in the example env file.
- A README that does not say how to run the project.

## Related skills

- `runbook-writer`
- `platform-readiness`
