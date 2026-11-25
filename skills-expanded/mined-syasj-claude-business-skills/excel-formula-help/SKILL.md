---
name: excel-formula-help
description: "Write or fix a spreadsheet formula that solves the calculation the user described, with a plain-English explanation. Use when the user mentions excel formula, sheets formula, how do I formula, VLOOKUP, or asks for a formula help. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'excel-formula-help' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Excel and Sheets Formula Help

Write or fix a spreadsheet formula that solves the calculation the user described, with a plain-English explanation.

## When to use this skill

Use this skill when the user:

- excel formula
- sheets formula
- how do I formula
- VLOOKUP
- INDEX MATCH
- SUMIF
- formula help spreadsheet

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Productivity systems serve the person's actual constraints. Do not recommend surveillance of colleagues or hidden monitoring.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What the formula should return
- The column and row structure they described
- An example of the input and expected output if they have one

## Workflow


### 1. Confirm the structure

which column holds the lookup value, which holds the result, and whether the match is exact or approximate.
### 2. Step 2

Write the formula with named ranges or column letters they described. Do not invent a structure they did not state.
### 3. Step 3

Explain each argument in one sentence. If the formula has a bracket inside a bracket, explain it from the inside out.
### 4. Give a test case

this input should return this output.
### 5. Step 5

Warn if the formula will break when rows are added or deleted, and say what to change.
### 6. Alternatives

offer a simpler formula if one exists. SUMIF over a helper column beats a nested IF chain.

## Output

Deliver a **formula help**.

- Purpose of this formula help, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a formula help by 30 September 2026. A user wants to look up a price from a table and cannot remember whether to use VLOOKUP or INDEX MATCH.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A user wants to look up a price from a table and cannot remember whether to use VLOOKUP or INDEX MATCH.

What the formula should return: Q4 objective 2, last reviewed 14 September 2026. No owner named since
The column and row structure they described: Friday review block, recorded 14 September 2026. No supporting file attached
An example of the input and expected output if they have one: Q4 objective 2. Partly documented: the what is written down, the who is not
```

### Example outcome

**Formula help**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Both formulas with the user's column letters, a plain explanation of when each breaks, and a test case.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What the formula should return | Q4 objective 2, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| The column and row structure they described | Friday review block, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| An example of the input and expected output if they have one | Q4 objective 2. Partly documented: the what is written down, the who is not | Carried into the draft |

**How this draft was built**

**1. Confirm the structure**  
which column holds the lookup value, which holds the result, and whether the match is exact or approximate.

**2. Write the formula with named ranges or column letters they described. Do not invent a structure they did not state**

**3. Explain each argument in one sentence. If the formula has a bracket inside a bracket, explain it from the inside out**

**4. Give a test case**  
this input should return this output.

**5. Warn if the formula will break when rows are added or deleted, and say what to change**

**Deliberately not done**
- Assuming a column layout they did not describe.
- Macros the user did not ask for.
- A formula without an explanation.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Assuming a column layout they did not describe
- Macros the user did not ask for
- A formula without an explanation

## Related skills

- `spreadsheet-model-review`
- `data-quality-check`
- `sql-review`
