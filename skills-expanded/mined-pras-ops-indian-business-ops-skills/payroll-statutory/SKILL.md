---
name: payroll-statutory
description: >-
  India payroll and its statutory deductions: salary structure (CTC vs gross vs net),
  Employees' Provident Fund (EPF/UAN), Employees' State Insurance (ESI), Professional Tax
  (state-wise), Labour Welfare Fund, gratuity and bonus, payslips, the monthly EPF ECR and ESI
  contribution, and estimating monthly salary TDS under section 192. Use for payroll, salary
  breakup, CTC, payslips, PF/EPF/UAN, ESI/ESIC, Professional Tax, gratuity, Form 16 for
  employees. For TDS on vendor/non-salary payments and the quarterly TDS returns themselves,
  use tds-compliance.
---

# Payroll and statutory deductions (India)

Running payroll in India is salary arithmetic plus a set of statutory contributions, each with its
own authority, return and deadline. This skill helps build the structure, compute deductions as
illustrations, and prepare the monthly filings — it does not give binding advice or file for the
user.

> [!IMPORTANT]
> Contribution rates, wage ceilings and eligibility thresholds are set by EPFO, ESIC, each state's
> Professional Tax law, and the Income-tax Act, and they change. Professional Tax and Labour
> Welfare Fund are **state-specific**. Never assert a current rate or ceiling from memory — confirm
> on the relevant portal (links below). The reference file holds dated snapshots only.
>
> **Labour Codes:** India's four Labour Codes are being brought into force and can change the
> statutory definition of *wages* (and the rule that certain allowances count toward it). That
> directly affects PF, ESI, gratuity and bonus. Treat the mechanics below as the established
> position and confirm the current wage definition and rates on the official portals before
> computing a real payroll.

## Salary structure first

Most payroll questions start with the breakup. Establish:

- **CTC vs gross vs net.** CTC (cost to company) includes employer contributions (employer PF,
  gratuity accrual, sometimes insurance); gross is before employee deductions; net ("in-hand") is
  after PF, PT, ESI and TDS. Be explicit about which one the user means — confusion here is the
  most common payroll error.
- **Components:** basic, HRA, and allowances. Basic drives PF, gratuity and several limits, so how
  the structure is split has real downstream effects.
- **Regime:** the employee's income-tax regime (old vs new) and declared investments change the
  monthly TDS under section 192.

## The statutory stack

For each employee, work out which of these apply, then compute as an illustration and prepare the
filing. Read [`references/pf-esi-pt.md`](references/pf-esi-pt.md) for the mechanics, wage bases and
where to confirm current rates.

1. **EPF (Provident Fund)** — employee and employer contributions on PF wages, filed monthly as the
   **ECR** on the EPFO portal; each employee needs a **UAN**. Applies once headcount crosses the
   coverage threshold.
2. **ESI** — health insurance contribution for employees below a wage ceiling, filed monthly on the
   ESIC portal. Applies once the establishment is covered.
3. **Professional Tax (PT)** — a **state** tax on employment, deducted from salary and paid to the
   state; slabs, periodicity and even existence vary by state.
4. **Labour Welfare Fund (LWF)** — small periodic contribution in some states.
5. **TDS on salary (section 192)** — see the `tds-compliance` skill; the employer estimates annual
   tax and deducts monthly. Form 16 is issued annually from TRACES.
6. **Gratuity and bonus** — gratuity accrues under the Payment of Gratuity Act (payable on exit
   after qualifying service); statutory bonus under the Payment of Bonus Act within wage limits.

## The monthly payroll run

A clean monthly sequence:

1. Finalise attendance / leave / variable pay for the cycle.
2. Compute gross per employee from the structure.
3. Compute statutory deductions (PF, ESI, PT) and TDS as illustrations — confirm live rates first.
4. Compute employer contributions (employer PF, ESI, gratuity accrual) for CTC/cost reporting.
5. Produce **payslips** showing earnings, deductions and net pay.
6. Prepare the filings: **EPF ECR**, **ESI contribution**, **PT** challan/return, and the TDS
   challan/return (per `tds-compliance`).
7. Reconcile: total of payslip deductions ↔ what's deposited with each authority.

## How to help, concretely

- **Design a structure:** given a target CTC or in-hand, lay out a sensible component split and show
  the CTC→gross→net waterfall, marking the statutory pieces as "confirm current rate".
- **Compute a run:** build the employee-wise sheet (gross, each deduction, employer share, net) and
  the figures each filing needs.
- **A payslip:** produce a clear itemised payslip template.
- **A query ("why did net drop this month?")** — trace it to the component that changed (a PT slab
  crossed, PF arrears, a TDS re-estimate) and explain.

## Guardrails

- Always ask which **state** for PT/LWF, and confirm EPF/ESI eligibility before applying them.
- Mark every rate, ceiling and slab "verify on the portal"; present deductions and tax as
  illustrations, not advice.
- For gratuity, bonus and final settlement, give the mechanism and recommend HR/payroll
  professional sign-off for an actual payout.
