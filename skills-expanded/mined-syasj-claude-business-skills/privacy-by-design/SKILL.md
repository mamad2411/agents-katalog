---
name: privacy-by-design
description: "Review a feature for data minimization, purpose, and user-facing honesty before it ships. Use when the user mentions privacy by design, data minimization, privacy review a feature, collect less data, or asks for a privacy design note. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'privacy-by-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Privacy by Design

Review a feature for data minimization, purpose, and user-facing honesty before it ships.

## When to use this skill

Use this skill when the user:

- privacy by design
- data minimization
- privacy review a feature
- collect less data

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

- The data the feature collects
- The purpose
- Retention if known
- What the user is told

## Workflow


### 1. Step 1

List each data element and the purpose it serves. No purpose, recommend cutting it.
### 2. Step 2

Prefer the least identifying option that still meets the purpose.
### 3. Step 3

Check that the notice or UI matches the collection. A mismatch is a finding.
### 4. Step 4

Retention is a question if unknown. Do not invent a period.
### 5. Step 5

Access, export, and deletion are product questions to flag, not legal conclusions.
### 6. Step 6

Send jurisdiction-specific claims to counsel. Do not declare a law satisfied.

## Output

Deliver a **privacy design note**.

- Purpose of this privacy design note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a privacy design note by 30 September 2026. A feature stores a full ID document to personalize a greeting.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A feature stores a full ID document to personalize a greeting.

The data the feature collects: Access review Q3, recorded 14 September 2026. No supporting file attached
The purpose: A feature stores a full ID document to personalize a greeting. Stated once, in the ask. Not written down anywhere else
Retention if known: Endpoint patch ring 2. Stated in the ask, not documented anywhere else
What the user is told: Phishing report 4412, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Privacy design note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts the document, keeps the display name if needed, and flags the notice gap.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The data the feature collects | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The purpose | A feature stores a full ID document to personalize a greeting. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Retention if known | Endpoint patch ring 2. Stated in the ask, not documented anywhere else | Carried into the draft |
| What the user is told | Phishing report 4412, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. List each data element and the purpose it serves. No purpose, recommend cutting it**

**2. Prefer the least identifying option that still meets the purpose**

**3. Check that the notice or UI matches the collection. A mismatch is a finding**

**4. Retention is a question if unknown. Do not invent a period**

**5. Access, export, and deletion are product questions to flag, not legal conclusions**

**Deliberately not done**
- Collecting data for a future maybe.
- A UI that hides the collection.
- A fake legal clearance.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Collecting data for a future maybe
- A UI that hides the collection
- A fake legal clearance

## Related skills

- `privacy-notice-draft`
- `privacy-impact-assessment`
