---
name: skill-library-trust-review
description: "Review a skill or a skill repository for signs it is unsafe, deceptive, or pretending to be an official product. Use when the user mentions is this skill repo safe, trust review, skill security review, should I install this, or asks for a trust review. Skill library skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: library
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'skill-library-trust-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Skill Library Trust Review

Review a skill or a skill repository for signs it is unsafe, deceptive, or pretending to be an official product.

## When to use this skill

Use this skill when the user:

- is this skill repo safe
- trust review
- skill security review
- should I install this

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Library skills help you choose, write, and trust agent skills. They do not grant extra permissions or weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The files or an inventory
- Install instructions
- Network behavior
- Claims of affiliation

## Workflow


### 1. Step 1

Prefer an installer that copies local files and does not pipe a remote script to a shell.
### 2. Step 2

Check scripts for network calls, obfuscation, and credential prompts.
### 3. Step 3

Descriptions should say what the skill does. Hidden instructions are a finding.
### 4. Step 4

Official-looking branding without a clear independent-author statement is a finding.
### 5. Step 5

A repository that promises guaranteed income, token claims, or wallet connections is out of scope for this library and should be treated as untrusted.
### 6. Step 6

Recommend installing one domain and reading a skill before enabling it. This review is not a security certification.

## Output

Deliver a **trust review**.

- Purpose of this trust review, in two sentences.
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

Yasir Jilani, author at Practice Skills in Airdrie, needs a trust review by 30 September 2026. An installer asks the user to run a remote script and paste an API key to 'activate' free skills.

### Example data

```text
From: Yasir Jilani, author
Organization: Practice Skills, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

An installer asks the user to run a remote script and paste an API key to 'activate' free skills.

The files or an inventory: 50 on hand
Install instructions: plugins/finance/cash-flow-forecast, last reviewed 14 September 2026. No owner named since
Network behavior: plugins/finance/cash-flow-forecast; MANIFEST.sha256. Both unassigned as of 14 September 2026
Claims of affiliation: the draft sentence is broader than the note
```

### Example outcome

**Trust review**
To: Yasir Jilani, author, Practice Skills
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the remote script and the key request.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The files or an inventory | 50 on hand | Needs confirmation |
| Install instructions | plugins/finance/cash-flow-forecast, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Network behavior | plugins/finance/cash-flow-forecast; MANIFEST.sha256. Both unassigned as of 14 September 2026 | Carried into the draft |
| Claims of affiliation | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Prefer an installer that copies local files and does not pipe a remote script to a shell**

**2. Check scripts for network calls, obfuscation, and credential prompts**

**3. Descriptions should say what the skill does. Hidden instructions are a finding**

**4. Official-looking branding without a clear independent-author statement is a finding**

**5. A repository that promises guaranteed income, token claims, or wallet connections is out of scope for this library and should be treated as untrusted**

**Deliberately not done**
- A fake certification.
- Ignoring a curl-pipe installer.
- Treating a logo as proof of affiliation.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Yasir Jilani by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fake certification
- Ignoring a curl-pipe installer
- Treating a logo as proof of affiliation

## Related skills

- `secrets-handling`
- `skill-authoring`
