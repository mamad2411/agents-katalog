---
name: fortax-gratuity-bonus-leave
description: Compute gratuity (Payment of Gratuity Act), statutory bonus (Payment of Bonus Act) and leave encashment (state shops and establishment Act, Factories Act or policy) for one employee's full and final or a whole payroll, with part-year rules, the tax exemption split, and the year-end provision schedules and journal entries. Typical asks: "gratuity calculate karo", "F&F me gratuity kitni banegi", "bonus kitna dena padega", "leave encashment provision banao".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Gratuity, bonus and leave encashment

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

The Payment of Gratuity Act, 1972, the Payment of Bonus Act, 1965, and leave under the applicable state
shops and establishment Act or the Factories Act each define their own wage base, eligibility and limits.
**Never carry a figure or a definition from one to another.** Act names, form names and the shape of
each formula are stable and may be stated. Every multiplier, ceiling, floor, percentage, qualifying
period, wage limit and due date is not — look each up for the period with
`python3 scripts/fortax.py kb "gratuity maximum limit" --topics pf` (quote its source and captured date;
on `weak` or `none`, read the Act or the department's own site) and record it in **Rules used**.

First, from the client's own records, take the states with employees, coverage under each Act and the FY.
Confirm each Act applies to this establishment at all; coverage triggers are statutory and vary. An Act
that does not apply still leaves the contractual entitlement in the appointment letter — read that too.

All computations go in a spreadsheet with live formulas or a short script, never mental arithmetic.

## 1. Gratuity

| Data needed | Source | Why |
|---|---|---|
| Date of joining | Appointment letter, employee master | Length of service |
| Date of leaving, or the valuation date, and the reason for cessation | Relieving letter, or FY end for a provision; HR record | The other end of the period; death, disablement and superannuation differ from resignation |
| Last drawn wages, by component | Salary register for the last month | The Act's wage definition picks the components |
| Whether the establishment is covered, and any gratuity trust or insurer policy | Registration file, client records | Covered and uncovered are computed differently; funding changes the accounting, not the liability |

**Formula shape.** Last drawn wages as the Act defines them, multiplied by a statutory fraction of a
month per completed year of service, multiplied by the years of service, subject to a statutory
maximum. Look up the fraction, the maximum, the qualifying period of continuous service and the wage
definition before computing — they differ for covered and uncovered establishments, and the maximum has
been revised. Where the contract or the client's policy is more generous, the contract governs; read it.

**Part years.** The Act rounds part years by its own rule, and that rule differs by coverage. Look it
up; do not round to the nearest year by instinct. Continuous service is as the Act defines it, not
simply calendar span — long absence, transfers between group companies and breaks in employment all
need checking.

**Death and disablement**: the qualifying period is relaxed and the Form F nomination matters, so treat
these as escalations to the CA with the computation attached, not as routine.

**Tax.** Gratuity is exempt to a limit (section 10(10)), and that limit and its conditions differ for
government employees, employees covered by the Act, and others. Look it up for the AY; the excess is
salary and goes through `fortax-payroll-monthly-run` for TDS.

## 2. Statutory bonus

**Data needed.** Each employee's wages month by month for the accounting year, from the salary
register; days actually worked and deemed worked, from attendance and leave records; dates of joining
and leaving; whether the establishment and each employee are covered; allocable and available surplus
from the audited accounts where set-on and set-off matter; last year's bonus and any set-on carried forward.

**Formula shape.** For each eligible employee, bonus wages for the year — taken at the lower of actual
wages and a statutory calculation ceiling where one applies — multiplied by the bonus percentage, which
sits between a statutory minimum and maximum and rises within that band where surplus supports it.
**Look up the eligibility wage limit, the calculation ceiling, the minimum and maximum percentages, the
minimum days worked to qualify and the payment window before computing any of it.** New establishments
have an infancy exemption with its own conditions; check it. Disqualification for specified misconduct
exists — never apply it without the client's written instruction.

**Part years.** Eligibility turns on days actually worked in the accounting year against a statutory
minimum, so compute days from attendance, not from months. A leaver's bonus is due for the part year
worked; carry it into the full and final settlement. The Act also prescribes registers of allocable
surplus, of set-on and set-off, and of bonus paid, plus an annual return — form names may be stated
once verified, and the due date is looked up (or taken from the calendar in `fortax-hr-compliance-calendar`).

## 3. Leave encashment

**Data needed.** Opening leave balance, leave credited in the year, leave availed, lapses under the
carry-forward cap, closing balance, the encashable part of it, and the wage base the policy or the
state's Act uses.

**Formula shape.** Encashable leave days multiplied by wages per day, where wages per day is the stated
wage base divided by the stated number of days in a month. The accrual rate, the carry-forward cap, the
encashable proportion and the divisor all come from the state Act or the client's policy — read both,
use the more beneficial where the policy is silent, and state them from the document. Leave accrues over
the period actually worked, usually against days worked, so compute a joiner's or leaver's credit from
attendance for the part year.

**Tax.** Encashment during service is fully taxable salary; on retirement or resignation an exemption
applies to a limit (section 10(10AA)), on conditions that differ for government and other employees.
Look it up for the AY and route the taxable part through salary TDS.

## 4. Provisions for the books

These accrue whether paid or not. Prepare the entries; the CA decides policy and the actuarial route.

| Provision | Basis | Note |
|---|---|---|
| Gratuity | Actuarial valuation where the applicable accounting standard requires it, else a computed estimate | Say which basis. Where an actuarial report exists it governs — do not recompute over it |
| Bonus | Best estimate of the year's liability at the percentage the client approved | Reverse last year's provision against the actual paid |
| Leave encashment | Closing encashable balance at year-end wages | Only the encashable portion, not the whole balance |

For each: opening provision, charge for the year, amounts paid or utilised, closing provision, with a
journal entry (`fortax-journal-entry`) and a schedule tying to the trial balance. Disclosure and the
standard applied come from `fortax-financial-statements`. Flag any funded plan separately; payment from a
fund still needs the liability recognised. Whether a provision is deductible, and when payment must
happen for it to be allowed (section 43B), is a tax question with statutory conditions — look them up,
never assert them.

## Hand over

Workings to the client's payroll folder for the FY (for example `<Client>/<FY 2026-27>/Payroll/`), dated,
as formulas with an assumptions block. Employee-level amounts stay in that folder — never in a chat
summary or a message body, and raw client files are never renamed or deleted.

- What was computed, for whom, on what basis, and which Act was held to apply.
- Anything escalated: death or disablement gratuity, disqualification, an unclear service break, a
  policy more generous than the Act, a missing actuarial report.
- **Check before paying**: service dates against the personnel file; the wage base against each Act's
  own definition, not a shared one; part years rounded by the Act's rule, not by instinct; coverage
  confirmed; the taxable portion carried into salary TDS; provision entries tying to the trial balance;
  **Rules used** carrying every multiplier, ceiling, percentage, qualifying period and due date with
  its source and the date checked.
