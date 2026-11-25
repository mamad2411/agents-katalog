---
name: sbom-and-supply-chain
description: "Review a software supply chain concern using the inventory the user has, without pretending a scan you did not run. Use when the user mentions SBOM, supply chain review, dependency inventory, provenance review, or asks for a supply chain note. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sbom-and-supply-chain' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Software Supply Chain Note

Review a software supply chain concern using the inventory the user has, without pretending a scan you did not run.

## When to use this skill

Use this skill when the user:

- SBOM
- supply chain review
- dependency inventory
- provenance review

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

- The inventory or SBOM they have
- How artifacts are built
- Who can publish a release
- Known gaps

## Workflow


### 1. Step 1

Use only the inventory they provided. Do not claim you scanned the internet.
### 2. Step 2

Note missing owners, unpinned dependencies, and unpublished build steps.
### 3. Step 3

Recommend a repeatable build and a named publisher.
### 4. Step 4

Secrets in the build are a blocking finding. Do not print them.
### 5. Step 5

If they have no inventory, the first action is to generate one with their tools, not to invent components.
### 6. Step 6

Hand license questions to the open-source review skill rather than ruling on them.

## Output

Deliver a **supply chain note**.

- Purpose of this supply chain note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a supply chain note by 30 September 2026. A release is built on a laptop and nobody can list the dependencies.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A release is built on a laptop and nobody can list the dependencies.

The inventory or SBOM they have: 20 on hand
How artifacts are built: Endpoint patch ring 2, last reviewed 14 September 2026. No owner named since
Who can publish a release: Aisha Rahman, engineering lead
Known gaps: Access review Q3 is missing a source
```

### Example outcome

**Supply chain note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Makes inventory and a repeatable build the first actions, with no invented component list.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The inventory or SBOM they have | 20 on hand | Needs confirmation |
| How artifacts are built | Endpoint patch ring 2, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Who can publish a release | Aisha Rahman, engineering lead | Carried into the draft |
| Known gaps | Access review Q3 is missing a source | Needs confirmation |

**How this draft was built**

**1. Use only the inventory they provided. Do not claim you scanned the internet**

**2. Note missing owners, unpinned dependencies, and unpublished build steps**

**3. Recommend a repeatable build and a named publisher**

**4. Secrets in the build are a blocking finding. Do not print them**

**5. If they have no inventory, the first action is to generate one with their tools, not to invent components**

**Deliberately not done**
- A fake scan result.
- Invented components.
- Secrets printed in the note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fake scan result
- Invented components
- Secrets printed in the note

## Related skills

- `dependency-upgrade`
- `open-source-license-review`
