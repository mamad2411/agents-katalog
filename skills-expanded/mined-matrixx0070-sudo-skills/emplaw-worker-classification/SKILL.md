---
name: emplaw-worker-classification
version: 1.0.0
description: Determine whether a worker is an employee or independent contractor, and whether an employee is exempt or non-exempt.
author: matrixx0070
tags: [employment-law, classification, flsa, contractor, exempt]
capabilities: []
---

## When to use
Use this when you need to decide how to classify a worker: employee versus independent contractor, and — for employees — exempt versus non-exempt from overtime. This skill applies the FLSA economic-reality test, the IRS common-law control test, the California ABC test, and the FLSA white-collar exemption duties tests. **Not for:** answering a specific overtime or break question once status is known (use emplaw-wage-hour-qa), reviewing a hire or offer (use emplaw-hiring-review), reviewing a firing (use emplaw-termination-review), investigating a complaint (use emplaw-internal-investigation), leave eligibility (use emplaw-leave-tracker), or drafting classification policy (use emplaw-policy-drafting).

## Method
1. Frame the question: contractor-vs-employee, exempt-vs-non-exempt, or both. Confirm the operating state.
2. For contractor-vs-employee, run the applicable test. Decision point: if the state uses the **ABC test** (e.g., California), start there — it is the strictest and defaults to employee unless all three prongs are met; else apply the FLSA economic-reality factors and the IRS common-law control test.
3. Weigh the factors as a whole. Decision point: if the worker's economic dependence and the hirer's control point to employee, stop treating them as a contractor.
4. If the worker is an employee, test exemption. Decision point: if paid below the current DOL salary threshold or not on a salary basis, they are **non-exempt** regardless of duties.
5. If salary-basis and threshold are met, apply the duties test for executive, administrative, or professional. Decision point: if the primary duty does not fit a category, classify non-exempt.
6. Record the deciding factors, not just the conclusion.
7. Apply the attorney-escalation gate: misclassification exposure is high-cost — confirm with licensed counsel in the operating state; this is not legal advice.

## Example
A California "consultant" works full-time, uses the company's tools, follows its schedule, and does core sales work. Under the ABC test the company cannot show prong B (work outside the usual course of business), so the worker is an **employee**. Paid $52,000 salaried, she is then tested for exemption: her primary duty is routine sales, not management or discretion, so she is **non-exempt** and owed overtime.

## Pitfalls
- **Relying on the contract label.** A "1099" agreement or the worker's preference does not control; the tests look at economic reality and actual control.
- **Assuming a salary means exempt.** Exemption requires the salary basis, the current threshold, AND a qualifying duties test — all three.
- **Applying the wrong state test.** California and several states use ABC; using the federal economic-reality test where ABC governs understates risk.
- **Ignoring that thresholds change.** The DOL salary threshold is revised periodically — always check the current figure.

## Output format
```
CLASSIFICATION — <worker/role> @ <state>
QUESTION: <contractor-vs-employee | exempt-vs-non-exempt | both>
TEST APPLIED: <ABC | FLSA economic-reality | IRS common-law | white-collar duties>
KEY FACTORS: <control / economic dependence / ABC prongs A,B,C>
CONTRACTOR-VS-EMPLOYEE: <conclusion + why>
SALARY BASIS + THRESHOLD: <met? current DOL figure>
DUTIES TEST: <executive | administrative | professional | none>
CLASSIFICATION: <employee non-exempt | employee exempt | contractor>
RISK: <LOW | MEDIUM | HIGH>
ATTORNEY GATE: Confirm with licensed counsel in <state>; not legal advice.
```

## Reference
General reference only, not tailored legal advice.
- **FLSA economic-reality test** (contractor vs employee): weighs the worker's economic dependence on the business — opportunity for profit/loss, investment, permanence of the relationship, degree of control, whether the work is integral to the business, and skill/initiative. No single factor decides.
- **IRS common-law control test**: three categories — **behavioral** control (how work is done), **financial** control (investment, expenses, profit/loss, payment method), and the **relationship** (contracts, benefits, permanency, integral work).
- **California ABC test** (Dynamex / AB5): a worker is an employee unless the hirer proves **(A)** freedom from control, **(B)** work outside the usual course of the hirer's business, and **(C)** the worker is engaged in an independently established trade. All three prongs required.
- **FLSA white-collar exemptions**: require a **salary basis**, a salary at or above the **current DOL threshold** (which changes — direct to the current DOL figure), and a **duties test** — executive (managing, directing 2+ employees, hire/fire authority), administrative (office work directly related to operations, exercising discretion on significant matters), or professional (advanced knowledge / creative). Failing salary basis or threshold defaults to non-exempt regardless of duties.
