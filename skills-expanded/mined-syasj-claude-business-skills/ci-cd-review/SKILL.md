---
name: ci-cd-review
description: "Review a delivery pipeline for repeatability, secrets handling, and a safe production gate. Use when the user mentions CI review, CD pipeline, deployment pipeline review, GitHub Actions review, or asks for a pipeline review. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ci-cd-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# CI/CD Review

Review a delivery pipeline for repeatability, secrets handling, and a safe production gate.

## When to use this skill

Use this skill when the user:

- CI review
- CD pipeline
- deployment pipeline review
- GitHub Actions review

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

- The pipeline description or config the user shared
- Environments
- Who can deploy
- Secret handling as described

## Workflow


### 1. Repeatability

Can a new teammate see what runs on a change. Hidden manual steps are a finding.
### 2. Gates

What must pass before production. A pipeline that deploys on red tests is a finding.
### 3. Secrets

Secrets come from a named store, not from the repo. Do not ask the user to paste live secrets into the chat.
### 4. Environments

What differs between staging and production, as they described it. Do not assume parity.
### 5. Rollback

How a bad deploy is undone, and who can do it.
### 6. Access

Who can change the pipeline. A world-writable deploy script is a finding.

## Output

Deliver a **pipeline review**.

- Purpose of this pipeline review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a pipeline review by 30 September 2026. A pipeline file contains a copied cloud key and deploys even when tests fail.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A pipeline file contains a copied cloud key and deploys even when tests fail.

The pipeline description or config the user shared: the one named in the ask. Version and owner not recorded
Environments: the one named in the ask. Version and owner not recorded
Who can deploy: Aisha Rahman, engineering lead
Secret handling as described: Invoice job and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Pipeline review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Requires the key to be removed and rotated, and blocks deploy-on-red. Do not repeat the key.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The pipeline description or config the user shared | the one named in the ask. Version and owner not recorded | Needs confirmation |
| Environments | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Who can deploy | Aisha Rahman, engineering lead | Carried into the draft |
| Secret handling as described | Invoice job and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Repeatability**  
Can a new teammate see what runs on a change. Hidden manual steps are a finding.

**2. Gates**  
What must pass before production. A pipeline that deploys on red tests is a finding.

**3. Secrets**  
Secrets come from a named store, not from the repo. Do not ask the user to paste live secrets into the chat.

**4. Environments**  
What differs between staging and production, as they described it. Do not assume parity.

**5. Rollback**  
How a bad deploy is undone, and who can do it.

**Deliberately not done**
- Asking for live secrets.
- Approving a deploy-on-red pipeline.
- No rollback.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Asking for live secrets.
- Approving a deploy-on-red pipeline.
- No rollback.

## Related skills

- `secrets-handling`
- `release-checklist`
