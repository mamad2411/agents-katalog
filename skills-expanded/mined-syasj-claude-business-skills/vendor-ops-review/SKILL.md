---
name: vendor-ops-review
description: "Review a vendor's operational performance against the outcomes the company bought. Use when the user mentions vendor review, supplier performance, vendor QBR, operations vendor scorecard, or asks for a vendor operations review. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'vendor-ops-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Vendor Operations Review

Review a vendor's operational performance against the outcomes the company bought.

## When to use this skill

Use this skill when the user:

- vendor review
- supplier performance
- vendor QBR
- operations vendor scorecard

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The outcomes contracted
- Recent misses they know
- Volumes
- The internal owner

## Workflow


### 1. Step 1

Score outcomes, not the relationship vibe.
### 2. Step 2

Use their incidents, delays, and volumes. Do not invent a score.
### 3. Step 3

Separate a one-time miss from a pattern.
### 4. Step 4

Ask whether the internal team kept its side of the process.
### 5. Step 5

Recommend continue, fix with a dated plan, or replace as a question for procurement.
### 6. Step 6

Do not invent contract penalties. Flag them for the contract owner.

## Output

Deliver a **vendor operations review**.

- Purpose of this vendor operations review, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a vendor operations review by 30 September 2026. A vendor is labeled difficult, but the internal briefs arrive late every week.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A vendor is labeled difficult, but the internal briefs arrive late every week.

The outcomes contracted: unsigned draft, 8 pages, no signature date
Recent misses they know: Dock exception log. Partly documented: the what is written down, the who is not
Volumes: 45 in the last period. No prior period attached, so no trend
The internal owner: Diane Cho, operations manager
```

### Example outcome

**Vendor operations review**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Records the late briefs as an internal cause and limits the vendor claim to evidenced misses.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The outcomes contracted | unsigned draft, 8 pages, no signature date | Needs confirmation |
| Recent misses they know | Dock exception log. Partly documented: the what is written down, the who is not | Carried into the draft |
| Volumes | 45 in the last period. No prior period attached, so no trend | Carried into the draft |
| The internal owner | Diane Cho, operations manager | Needs confirmation |

**How this draft was built**

**1. Score outcomes, not the relationship vibe**

**2. Use their incidents, delays, and volumes. Do not invent a score**

**3. Separate a one-time miss from a pattern**

**4. Ask whether the internal team kept its side of the process**

**5. Recommend continue, fix with a dated plan, or replace as a question for procurement**

**Deliberately not done**
- A score with no data.
- Blaming the vendor for an internal miss.
- Invented penalties.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A score with no data
- Blaming the vendor for an internal miss
- Invented penalties

## Related skills

- `supplier-scorecard`
- `procurement-award-note`
