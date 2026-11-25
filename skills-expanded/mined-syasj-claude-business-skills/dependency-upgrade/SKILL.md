---
name: dependency-upgrade
description: "Plan a dependency upgrade around risk, changelog, and rollback, not around a version number badge. Use when the user mentions dependency upgrade, bump this library, framework upgrade, renovate plan, or asks for a upgrade plan. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dependency-upgrade' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dependency Upgrade

Plan a dependency upgrade around risk, changelog, and rollback, not around a version number badge.

## When to use this skill

Use this skill when the user:

- dependency upgrade
- bump this library
- framework upgrade
- renovate plan

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

- The dependency and versions
- Why the upgrade is happening
- Breaking changes the user found
- How the app is tested

## Workflow


### 1. Reason

Security fix, bug, or support window, as the user stated. Do not invent a CVE.
### 2. Breaking changes

List the ones they found in notes or a changelog they pasted. If none were read, the plan starts by reading them.
### 3. Blast radius

Which parts of the product use it.
### 4. Test

The regression checks that matter for that blast radius.
### 5. Rollback

How to return to the old version, and what data changes would make rollback hard.
### 6. Secrets and scripts

Do not run untrusted upgrade scripts blindly. Read install scripts before recommending them. No curl-pipe-shell.

## Output

Deliver a **upgrade plan**.

- Purpose of this upgrade plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an upgrade plan by 30 September 2026. A bot opened a major upgrade and nobody has read the changelog.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A bot opened a major upgrade and nobody has read the changelog.

The dependency and versions: Checkout service is open. Invoice job was raised verbally and never logged
Why the upgrade is happening: A bot opened a major upgrade and nobody has read the changelog
Breaking changes the user found: requested 14 September 2026. Not yet approved
How the app is tested: Invoice job, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Upgrade plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the merge until breaking changes are read and a rollback is named.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The dependency and versions | Checkout service is open. Invoice job was raised verbally and never logged | Needs confirmation |
| Why the upgrade is happening | A bot opened a major upgrade and nobody has read the changelog | Carried into the draft |
| Breaking changes the user found | requested 14 September 2026. Not yet approved | Carried into the draft |
| How the app is tested | Invoice job, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Reason**  
Security fix, bug, or support window, as the user stated. Do not invent a CVE.

**2. Breaking changes**  
List the ones they found in notes or a changelog they pasted. If none were read, the plan starts by reading them.

**3. Blast radius**  
Which parts of the product use it.

**4. Test**  
The regression checks that matter for that blast radius.

**5. Rollback**  
How to return to the old version, and what data changes would make rollback hard.

**Deliberately not done**
- Inventing a CVE.
- Recommending curl piped to a shell.
- An upgrade with no rollback story.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inventing a CVE.
- Recommending curl piped to a shell.
- An upgrade with no rollback story.

## Related skills

- `sbom-and-supply-chain`
- `test-strategy`
