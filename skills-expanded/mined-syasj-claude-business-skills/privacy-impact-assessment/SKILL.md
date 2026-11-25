---
name: privacy-impact-assessment
description: "Prepare a privacy impact note for a process that collects personal data, for counsel to complete. Use when the user mentions privacy impact, PIA, DPIA prep, new processing review, or asks for a privacy impact note. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'privacy-impact-assessment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Privacy Impact Assessment

Prepare a privacy impact note for a process that collects personal data, for counsel to complete.

## When to use this skill

Use this skill when the user:

- privacy impact
- PIA
- DPIA prep
- new processing review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The process
- Data elements
- People affected
- Recipients they named

## Workflow


### 1. Step 1

Describe the process and the purpose.
### 2. Step 2

List data elements and who they are about. Cut elements with no purpose.
### 3. Step 3

List recipients the user named. Do not invent vendors.
### 4. Step 4

Note retention if known, otherwise mark it unknown.
### 5. Step 5

Flag high-harm contexts they mentioned, such as children or precise location, for counsel. Do not complete a legal DPIA conclusion.
### 6. Step 6

Recommend a product change where minimization is obvious.

## Output

Deliver a **privacy impact note**.

- Purpose of this privacy impact note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a privacy impact note by 30 September 2026. A new form collects date of birth to personalize a color theme.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A new form collects date of birth to personalize a color theme.

The process: email to Priya Shah. No written steps after 1 Sep 2026
Data elements: Control 7.2 access review. Partly documented: the what is written down, the who is not
People affected: Issue log item 18, last reviewed 14 September 2026. No owner named since
Recipients they named: Priya Shah plus two others named in the thread. No distribution list attached
```

### Example outcome

**Privacy impact note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts the date of birth and sends any remaining legal question to counsel.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The process | email to Priya Shah. No written steps after 1 Sep 2026 | Needs confirmation |
| Data elements | Control 7.2 access review. Partly documented: the what is written down, the who is not | Carried into the draft |
| People affected | Issue log item 18, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Recipients they named | Priya Shah plus two others named in the thread. No distribution list attached | Needs confirmation |

**How this draft was built**

**1. Describe the process and the purpose**

**2. List data elements and who they are about. Cut elements with no purpose**

**3. List recipients the user named. Do not invent vendors**

**4. Note retention if known, otherwise mark it unknown**

**5. Flag high-harm contexts they mentioned, such as children or precise location, for counsel. Do not complete a legal DPIA conclusion**

**Deliberately not done**
- A legal conclusion dressed up as a PIA.
- Invented vendors.
- Keeping data with no purpose.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A legal conclusion dressed up as a PIA
- Invented vendors
- Keeping data with no purpose

## Related skills

- `privacy-by-design`
- `privacy-notice-draft`
