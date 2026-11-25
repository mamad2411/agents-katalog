---
name: fortax-payroll-monthly-run
description: Run a client's monthly payroll in India — read attendance, joiners, leavers and arrears; build a formula-driven salary register from gross to net with PF, ESI, professional tax and salary TDS; tie the register to the bank file, ECR, ESI file, PT and TDS challans and the salary journal; and prepare payslips, the bank transfer file and draft challans and returns, stopping before any payment or portal submit. Typical asks: "is mahine ki salary banao", "payroll run karo", "PF ESI challan working chahiye", "payslips generate karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# Payroll monthly run

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Attendance to payslips to the bank file to the challan working to the draft returns — all of it is
yours. Not yours: the portal submit, the challan payment, the OTP or DSC, the release of the bank
file. Take the month to those and hand over. Registration is `fortax-payroll-registrations`, not this skill.

## Step 1 — fix the period, then read the inputs

From the client's own records (registration certificates, last month's register, the permanent file)
take the PF code, ESI code, TAN, PT registration numbers and the states with employees. Fix the wage
month, the FY and the AY and print all three in every file name and header. Employees in more than one
state means more than one PT working. Then read the client's own files. Never retype what you can read.

| Input | Usual source | What breaks without it |
|---|---|---|
| Employee master | HR sheet, last month's register | Wrong UAN, IP number, PAN, bank account |
| Attendance, days paid, leave and LOP | Biometric export, muster, leave tracker | Wrong gross and PF wages, silent overpayment |
| Joiners with date of joining | Appointment letters | Missing UAN, missing IP registration |
| Leavers with date of leaving and F&F | Resignation, relieving file | Blocked PF claim, unpaid dues |
| Revisions and arrears | Increment letters | Arrear month wrongly taxed |
| Variable pay, incentive, OT | Sales or ops sheet | Understated ESI and PT |
| Declarations, proofs, previous employer income | Employee declarations | Wrong TDS on salary |
| Loans, advances, recoveries | Client instruction | Net pay disputes |

Compare this month's master to last month's. Every addition, deletion and CTC change must be
explained by a document; an unexplained change is a flag to the CA, not something you absorb.

## Step 2 — gross to net, per employee

Build the register as a spreadsheet with live formulas, not pasted values, with an assumptions block on
top. Earnings for the days paid, plus arrears and variable pay, give gross. Statutory deductions are PF
employee share, ESI employee share, PT and TDS on salary; other deductions are loan, advance, canteen
and notice recovery. Net pay is gross less all deductions. Employer cost — employer PF, employer ESI,
EDLI and administrative charges where applicable, gratuity and bonus provisions — is shown separately.
It is cost, not a deduction; never net it off pay.

**Look up every rate and ceiling for this wage month before you compute.** The PF rate, the wage base
it applies to and any wage ceiling; the ESI employee and employer rates, the wage ceiling that decides
coverage, and the contribution-period rule that keeps a member covered after crossing it mid-period;
EDLI and admin charges; the PT slab per state; the salary TDS rates, regime and rebate for that AY.
Run `python3 scripts/fortax.py kb "ESI contribution rates" --topics pf,esi` (or `--topics itr,tds` for
salary tax) and quote its source and captured date; on `weak` or `none`, read epfindia.gov.in,
esic.gov.in, the state PT site or the Income-tax Act for that period. Record each in **Rules used** with
its source and date checked. Never from memory, never a state's slab carried across. Which components
enter PF wages comes from `fortax-salary-structuring`.

**TDS on salary** (section 192): estimated annual income less exemptions and deductions, tax for the AY,
less what is already deducted, spread over the months left. Recompute every month — joiners, arrears,
proof submission and a regime change all move it. Where an employee declared previous employer income,
use it and say so.

## Step 3 — the reconciliation that must tie before anything is paid

Nothing is paid and nothing is filed until all seven agree. A difference is a blocker. Put each tie in
the workbook as a formula that shows the difference.

| Tie | Left | Right |
|---|---|---|
| A | Register net pay total | Bank file total, and its line count to headcount |
| B | Register PF employee + employer + EDLI + admin | PF challan working, and the ECR total |
| C | Register ESI employee + employer | ESI contribution file and challan working |
| D | Register PT deducted, per state | That state's PT challan working |
| E | Register salary TDS | TDS challan working, and the 24Q quarter running total |
| F | Register gross and employer cost | Salary journal entry debits |
| G | Opening headcount + joiners − leavers | Closing, and the count in each statutory file |

Recompute totals from the rows; never copy a summary line. Where a tie fails, use
`fortax-reconciliation` to find the difference and name the cause before adjusting anything.

## Step 4 — outputs

Salary register; payslips in the firm's format; the bank transfer file in the bank's own layout,
validated for IFSC format, account length, no blank or duplicate beneficiary and a total tied to the
register; the ECR text file; the ESI contribution file; a PT statement per state; the TDS challan
working; the salary journal entry (see `fortax-journal-entry`); and a variance note against last month.
Use a short script for the file validations rather than eyeballing them.

## Step 5 — challans and returns

Each deduction triggers a payment and a return. The sequence is stable; dates and rates are not.

| Head | Payment | Periodic return |
|---|---|---|
| PF | Challan after the ECR upload on the EPFO unified portal | The ECR is itself the monthly return |
| ESI | Challan after the contribution file on the ESIC portal | Monthly filing, plus any half-yearly return in force |
| PT | State challan | State return, at that state's frequency |
| TDS on salary | Income tax challan against the client's TAN | Quarterly 24Q; Form 16 after year end (see `fortax-tds`) |

Also in the month it happens: UAN generation and KYC for joiners, exit marking for leavers, ESI IP
registration for new coverable employees. A missed exit blocks the member's own claim later. Take every
due date from `fortax.py kb` or the portal for that month, with the source, or from the client's
calendar built with `fortax-hr-compliance-calendar`. Interest and damages for late PF or ESI payment are
looked up, never recalled.

## Hand over

Employee-level pay, PAN, Aadhaar, UAN and bank details stay inside the client folder. Never paste a
salary figure, a bank account or an employee list into a chat summary or a message body. Draft messages
carry totals and file names; the CA shares the file through the firm's own secure channel. Outputs go
to the client's payroll folder for that FY (for example `<Client>/<FY 2026-27>/Payroll/<MM-YYYY>/`),
dated; raw client files are never renamed.

- What is computed, what is filled on which portal, what is blank and why, the exact next click.
- **Check before paying**: all seven ties agree; joiners and leavers reconciled to documents; bank
  file totals and account details verified; every rate, ceiling, slab and due date in **Rules used**
  with its source and date checked; a separate PT working per state; nothing submitted or paid.
