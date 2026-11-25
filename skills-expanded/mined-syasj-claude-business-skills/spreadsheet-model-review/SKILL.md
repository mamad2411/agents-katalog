---
name: spreadsheet-model-review
description: "Review a spreadsheet model for structure, formula errors, and hard-coded values that should be inputs. Use when the user mentions spreadsheet review, excel review, check my model, formula audit, or asks for a spreadsheet review. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'spreadsheet-model-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Spreadsheet Model Review

Review a spreadsheet model for structure, formula errors, and hard-coded values that should be inputs.

## When to use this skill

Use this skill when the user:

- spreadsheet review
- excel review
- check my model
- formula audit
- spreadsheet audit

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

- The file or a paste of the key formulas
- The purpose of the model
- Outputs that matter
- Known errors or warnings

## Workflow


### 1. Step 1

Start from the outputs. Check that they trace back to assumptions, not to manually typed numbers buried in cells.
### 2. Step 2

Flag hard-coded values in formula cells. Those belong in an input section.
### 3. Step 3

Identify circular references and error values. Name the cell and the formula, not just the problem.
### 4. Step 4

Check cross-sheet references. A link to a renamed or moved sheet silently returns zero.
### 5. Step 5

Review error-handling. Divisions that can return a zero denominator need an IFERROR or an IF guard.
### 6. Step 6

Propose one structural change at a time. A model rebuilt all at once becomes untestable.

## Output

Deliver a **spreadsheet review**.

- Purpose of this spreadsheet review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, shares the FY2027 operating budget. Her analyst reports that changing the revenue assumption takes more than forty manual edits.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
File: FY2027 Operating Budget.xlsx (12 tabs)

Reported symptom: changing the revenue growth rate requires editing every month column.

Formulas pasted for review:
  P&L!B8   =4200*1.03          (repeated across C8:M8, 47 cells total)
  P&L!D22  =Sheet3!C4          (tab "Sheet3" was renamed to "COGS Detail")
  P&L!K34  =K32/K33            (K33 = headcount, can be 0 in a setup month)
  Assumptions tab: exists, unprotected, no named ranges
  Column A dates: rows 1-6 text "Jan-27", rows 7-12 serial 1/1/2027
```

### Example outcome

**Spreadsheet model review — FY2027 Operating Budget**
To: Priya Shah, controller, Northline Studio · Date: 14 September 2026

**Decision**
Two findings break the model today and must be fixed before anyone trusts Net Income. The rest are structural and can follow.

**Finding 1 — CRITICAL · Revenue hard-coded in 47 formula cells**

`P&L!B8` contains `=4200*1.03`, repeated across `C8:M8`. The growth rate lives inside the formula, so changing it means 47 edits and one of them will be missed.

Fix — move both numbers to inputs, then reference them:

```
Assumptions!B3  =4200     (revenue base, January)
Assumptions!B4  =1.03     (monthly growth rate)

P&L!B8  =Assumptions!$B$3 * (Assumptions!$B$4 ^ (COLUMN()-2))
```

One edit now updates all twelve months.

**Finding 2 — HIGH · COGS reference points at a tab that no longer exists**

`P&L!D22` is `=Sheet3!C4`. The tab was renamed to `COGS Detail`, so this returns `#REF!` and the error propagates silently into Net Income.

Fix: `='COGS Detail'!C4`, then define a named range so the next rename does not break it.

**Finding 3 — MEDIUM · Division with an unguarded zero denominator**

`P&L!K34` is `=K32/K33`, where K33 is headcount. A department in its setup month has zero headcount, which returns `#DIV/0!` and breaks the payroll summary.

Fix: `=IFERROR(K32/K33, 0)` — or `=IF(K33=0, 0, K32/K33)` if a zero should be visibly different from an error.

**Finding 4 — MEDIUM · Assumptions tab is unprotected**

Any user can overtype a formula or delete a range. Lock the formula cells and leave only the assumption inputs editable before this is shared more widely.

**Finding 5 — LOW · Mixed date types in column A**

Rows 1–6 hold the text `"Jan-27"`; rows 7–12 hold real date serials. Charts built on this column will sort wrongly. Standardise on serials with a `mmm-yy` display format.

**Order of work**

| # | Fix | Why first |
| --- | --- | --- |
| 1 | `#REF!` in COGS | It is wrong on screen today |
| 2 | Revenue inputs | Highest effort, highest payoff; everything else depends on it |
| 3 | `IFERROR` guard on K34 | Cheap, prevents a future break |
| 4 | Lock formula cells | Do before wider sharing |
| 5 | Date formats | Cosmetic until someone builds a chart |

**Deliberately not done**
- The model was not restructured beyond what was asked. One change at a time keeps it testable.
- No formula's intent was guessed. Where the purpose of a cell was unclear, it is listed for Priya to confirm rather than rewritten.
- No new tool was proposed. The spreadsheet is the right tool for this; it just needs its inputs separated.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Rewriting the model structure without being asked
- Guessing what a formula is supposed to do
- Proposing a new tool when the spreadsheet works

## Related skills

- `data-quality-check`
