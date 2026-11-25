---
name: fortax-salary-structuring
description: Break an Indian employee's CTC into salary components (basic, DA, HRA, allowances, reimbursements, bonus, employer PF and NPS, gratuity) and show what each does to PF wages, ESI coverage, professional tax and taxable salary under both tax regimes — as a formula spreadsheet with options and the special-allowance PF exposure, leaving the choice to the CA. Typical asks: "CTC breakup banao", "salary structure tax efficient karo", "basic kitna rakhein PF ke liye", "ESI se bahar kaise rakhein".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Salary structuring

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

A CTC number arrives from the client. You turn it into a component structure and show the CA exactly
what each component does to PF wages, ESI coverage, professional tax and taxable salary. You produce
the structure and the working. You do not decide the client's compliance posture — see Step 5.

## Step 1 — get the frame before the arithmetic

From the client's own records, take the states with employees, the PF and ESI codes, and whether the
establishment is covered at all (`fortax-payroll-registrations` if unsure). Then fix, for this employee:

- The offered CTC, annual or monthly, and what the client means by CTC — some include employer PF and
  the gratuity provision, some do not. Ask once, in writing.
- Date of joining, the wage month the structure starts from, and the location, because PT is a state
  levy and the state decides everything about it.
- Whether this is a new PF member or an existing UAN with a running membership.
- The tax regime opted for. It decides whether an exemption exists at all, and the regime rules change
  by AY, so look them up for this AY.

## Step 2 — the component set

Build from the firm's standard structure in its templates folder where one exists. Otherwise:

| Component | Nature | Treatment to verify |
|---|---|---|
| Basic salary and dearness allowance | Fixed monthly | The anchor for PF wages and gratuity, and often for HRA |
| House rent allowance | Fixed | Exempt only on conditions, on rent actually paid |
| Conveyance, children education, hostel | Fixed | Exemptions with conditions, regime and AY dependent |
| Special allowance | Balancing figure | The classic PF dispute component — see Step 5 |
| Leave travel allowance | Annual | Exempt on conditions, on actual travel, in a block of years |
| Reimbursements — fuel, phone, books, driver; meal coupons | On bill or monthly | Not salary if actually reimbursed against bills; coupons carry their own conditions and limit |
| Statutory, performance, joining and retention bonus | Annual, variable or one-off | Statutory bonus is in `fortax-gratuity-bonus-leave`; the rest are taxable on payment — check the effect on ESI, and recovery has its own treatment |
| Employer PF and employer NPS | Employer cost | Taxable above a combined employer-contribution limit; NPS carries its own ceiling, regime dependent |
| Gratuity provision | Employer cost | A provision, not pay; never a deduction from the employee |

Component names are stable and may be stated. **Every limit, rate, ceiling, percentage, exemption
amount and qualifying period attached to them is not.** Look each up for this AY and this state with
`python3 scripts/fortax.py kb "HRA exemption new regime" --topics itr` (quote its source and captured
date; on `weak` or `none`, read the department's own site or the Act) and record it in **Rules used**.

## Step 3 — what each component triggers

Work these four questions for every component, never from memory.

**PF wages.** Look up the definition of wages in force under the EPF Act for this period — basic and
DA alone or a wider base — how an allowance paid universally is treated after the litigation on
special allowance, whether a statutory wage ceiling applies, and whether the employer contributes
above it. Then say, component by component, in or out. Where inclusion is genuinely arguable, say so
and give the CA both readings; do not pick one silently.

**ESI coverage.** ESI applies where wages do not exceed a ceiling. Look up the ceiling for this period
and the wage definition used for it, which is not the PF definition. Note which components count,
whether the test is on monthly wages, and the contribution-period rule that keeps a member covered for
the rest of a period after crossing the ceiling. A structure that lands an employee just either side
of that ceiling is a decision to flag, not to make.

**Professional tax.** State levy. Identify the state, then read that state's slabs, wage definition,
frequency, and whether it levies PT at all. Never carry a slab across states.

**Taxable salary.** For each component — fully taxable, exempt on conditions, or not salary at all.
Where exempt on conditions, write the conditions and the evidence the employee must produce: rent
receipts and the landlord's PAN above a threshold, travel tickets, bills for reimbursements. The
answer differs by regime, so state the regime you computed on. A reimbursement paid without bills is
salary; say so.

## Step 4 — the working the CA gets

Write `<date>_salary_structure_<employee or grade>.xlsx` with live formulas, not values: the CTC
build-up monthly and annual, every component, employer cost shown apart from pay; a column each for
"in PF wages", "in ESI wages", "in PT base" and "taxable or exempt-on-condition"; monthly gross,
statutory deductions and net pay in hand; a tax estimate under both regimes side by side with the
assumption stated; the employer cost total tying back to the CTC offered (a check cell showing the
difference); and **Rules used**, carrying every rate, ceiling, slab, exemption limit and condition with
its source and date checked. Where this feeds an offer or appointment letter, `fortax-hr-letters` takes
its figures from here — never let the two disagree.

## Step 5 — the restructuring trap

Keeping basic low, or moving pay into allowances and reimbursements, reduces PF wages and sometimes
keeps an employee out of ESI, and clients ask for it constantly. The special allowance question has
been litigated: where an allowance is paid universally, ordinarily and necessarily to all employees in
a category, it has been held to form part of PF wages, so read the current position with `fortax.py kb`
or `fortax-deep-research` before advising. Retrospective demands, interest and damages fall on the
employer, not on the spreadsheet. And a structure built for one employee's tax outcome creates an
unequal set across the payroll, and an audit question later.

**Model the options and show the consequence of each. Do not recommend one.** Present at least two
structures — a straightforward one and the client's requested one — with the PF wages, ESI position, PT
and net pay of each, and the exposure attached to the second. Then say in one line that the choice is
the CA's and that you have not made it. If the client presses directly for the aggressive one, decline
and route it to the CA.

## Hand over

The structure file goes to the client's payroll folder for the FY (for example
`<Client>/<FY 2026-27>/Payroll/`), dated. Employee pay data stays there — never in a chat summary,
never in a message body; messages name the file.

- What was designed, on what CTC definition, for which state and which regime.
- The options modelled, the consequence of each, and the choice left open.
- **Check before issuing**: CTC ties to the client's offer; every component classified for PF, ESI,
  PT and tax with a source; that state's PT read this session; the regime stated; anything arguable
  flagged; **Rules used** complete; nothing committed to the employee.
