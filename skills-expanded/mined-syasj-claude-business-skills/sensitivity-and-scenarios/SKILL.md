---
name: sensitivity-and-scenarios
description: "Show how a model moves when a few inputs move, without pretending the spreadsheet is a crystal ball. Use when the user mentions sensitivity analysis, what if this input changes, tornado chart, scenario versus sensitivity, or asks for a sensitivity note. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sensitivity-and-scenarios' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sensitivity and Scenarios

Show how a model moves when a few inputs move, without pretending the spreadsheet is a crystal ball.

## When to use this skill

Use this skill when the user:

- sensitivity analysis
- what if this input changes
- tornado chart
- scenario versus sensitivity

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The model outcome that matters
- The inputs the user can actually vary
- A base case from their numbers
- The range they consider plausible

## Workflow


### 1. Pick the outcome

Cash, margin, or runway. One outcome per pass.
### 2. Vary one input at a time first

That is a sensitivity. Combinations are scenarios and should be named, not hidden in a data table.
### 3. Use their ranges

Do not widen a range to make a picture look dramatic.
### 4. Rank the drivers

Which input moves the outcome most across the stated range.
### 5. Tell them what not to precise

If the top driver is a guess, more decimal places will not help.
### 6. Recommend a measurement

The useful next step is often to learn the top driver, not to add more tabs.

## Output

Deliver a **sensitivity note**.

- Purpose of this sensitivity note, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a sensitivity note by 30 September 2026. A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers.

The model outcome that matters: A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers. Stated once, in the ask. Not written down anywhere else
The inputs the user can actually vary: Operating cash, recorded 14 September 2026. No supporting file attached
A base case from their numbers: Harbor & Co receipt and one other, both unconfirmed as of 14 September 2026
The range they consider plausible: Operating cash, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Sensitivity note**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A one-way sensitivity on the user's ranges, the dominant driver, and a recommendation to measure that driver before adding detail.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The model outcome that matters | A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The inputs the user can actually vary | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| A base case from their numbers | Harbor & Co receipt and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The range they consider plausible | Operating cash, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Pick the outcome**  
Cash, margin, or runway. One outcome per pass.

**2. Vary one input at a time first**  
That is a sensitivity. Combinations are scenarios and should be named, not hidden in a data table.

**3. Use their ranges**  
Do not widen a range to make a picture look dramatic.

**4. Rank the drivers**  
Which input moves the outcome most across the stated range.

**5. Tell them what not to precise**  
If the top driver is a guess, more decimal places will not help.

**Deliberately not done**
- A tornado built from invented ranges.
- Calling a one-way table a scenario plan.
- False precision.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A tornado built from invented ranges.
- Calling a one-way table a scenario plan.
- False precision.

## Related skills

- `scenario-planning`
- `forecast-accuracy`
- `three-statement-model`
