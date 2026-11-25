---
name: ethics-hotline-triage
description: "Triage a hotline report toward the right independent handler, without retaliation or a verdict. Use when the user mentions ethics hotline, speak-up report, ethics triage, hotline intake, or asks for a hotline triage. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ethics-hotline-triage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Ethics Hotline Triage

Triage a hotline report toward the right independent handler, without retaliation or a verdict.

## When to use this skill

Use this skill when the user:

- ethics hotline
- speak-up report
- ethics triage
- hotline intake

## When not to use this skill

- Retaliation
- Cover-up

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

- The allegation summary
- Who it names
- Safety issues
- The company's routing rules

## Workflow


### 1. Step 1

If someone is in immediate danger, point to emergency services and their safety process.
### 2. Step 2

Record the allegation without adding motive.
### 3. Step 3

Route away from anyone named in the report.
### 4. Step 4

Minimize personal data in the routing note.
### 5. Step 5

Refuse any request to identify or punish the reporter for reporting.
### 6. Step 6

This triage is not an investigation finding.

## Output

Deliver a **hotline triage**.

- Purpose of this hotline triage, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a hotline triage by 30 September 2026. A report names the division president, and the president asks to handle it personally.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A report names the division president, and the president asks to handle it personally.

The allegation summary: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
Who it names: Priya Shah, controller
Safety issues: Issue log item 18. Partly documented: the what is written down, the who is not
The company's routing rules: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Hotline triage**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Routes around the president and refuses retaliation against the reporter.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The allegation summary | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Who it names | Priya Shah, controller | Carried into the draft |
| Safety issues | Issue log item 18. Partly documented: the what is written down, the who is not | Carried into the draft |
| The company's routing rules | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. If someone is in immediate danger, point to emergency services and their safety process**

**2. Record the allegation without adding motive**

**3. Route away from anyone named in the report**

**4. Minimize personal data in the routing note**

**5. Refuse any request to identify or punish the reporter for reporting**

**Deliberately not done**
- A verdict at triage.
- Retaliation.
- Routing to the accused.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A verdict at triage
- Retaliation
- Routing to the accused

## Related skills

- `whistleblower-intake`
- `employee-relations-intake`
