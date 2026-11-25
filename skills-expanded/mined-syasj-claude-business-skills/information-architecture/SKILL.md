---
name: information-architecture
description: "Recommend an information architecture from user tasks, not from the company's org chart. Use when the user mentions information architecture, site map, navigation, IA review, or asks for a IA recommendation. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'information-architecture' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Information Architecture

Recommend an information architecture from user tasks, not from the company's org chart.

## When to use this skill

Use this skill when the user:

- information architecture
- site map
- navigation
- IA review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Design critique improves the work. Do not copy a third party's branded assets. Accessibility is part of done, not a later pass to skip.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Top tasks
- Current labels
- Evidence of confusion
- Constraints

## Workflow


### 1. Step 1

List tasks users come to finish.
### 2. Step 2

Group by those tasks, not by internal departments.
### 3. Step 3

Label in the user's words if you have them.
### 4. Step 4

Show what moves or gets cut.
### 5. Step 5

Note search versus navigation. Do not hide a bad structure behind a search box as the only plan.
### 6. Step 6

Test labels with a simple card sort or tree test plan if the stakes are high and they can run one.

## Output

Deliver a **IA recommendation**.

- Purpose of this IA recommendation, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs an IA recommendation by 30 September 2026. The nav has a tab for each internal department and users cannot find billing.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The nav has a tab for each internal department and users cannot find billing.

Top tasks: The nav has a tab for each internal department and users cannot find billing. Stated once, in the ask. Not written down anywhere else
Current labels: Empty-state copy and one other, both unconfirmed as of 14 September 2026
Evidence of confusion: one PDF, 2 pages, dated 14 September 2026
Constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Ia recommendation**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Groups billing under the task users named and demotes the org chart.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Top tasks | The nav has a tab for each internal department and users cannot find billing. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Current labels | Empty-state copy and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Evidence of confusion | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. List tasks users come to finish**

**2. Group by those tasks, not by internal departments**

**3. Label in the user's words if you have them**

**4. Show what moves or gets cut**

**5. Note search versus navigation. Do not hide a bad structure behind a search box as the only plan**

**Deliberately not done**
- Navigation that mirrors the org chart.
- A search box as the only fix.
- Labels nobody outside the company uses.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Navigation that mirrors the org chart
- A search box as the only fix
- Labels nobody outside the company uses

## Related skills

- `journey-map`
- `design-critique`
