---
name: run-payroll
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 1h
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Process a scheduled payroll run accurately so employees are paid and required records are updated.

## Preconditions

- Payroll calendar, pay period, and cutoff are confirmed.
- Time, salary changes, deductions, new hires, terminations, and bonuses are entered or approved.
- You have payroll system access and authorization to submit payroll.

## Steps

1. **Open the payroll run.** Select the correct company, pay group, pay period, and pay date. → *Expect:* the payroll batch matches the scheduled run.
2. **Import approved inputs.** Pull approved time, PTO, commissions, bonuses, deductions, reimbursements, and employee changes. → *Expect:* payroll inputs load without unresolved errors.
3. **Review exceptions.** Check missing timecards, negative net pay, unusual hours, bank changes, tax errors, and terminated employees. → *Expect:* exceptions are listed and assigned for resolution.
4. **Correct approved issues.** Make only documented corrections or send unresolved items to the proper owner. → *Expect:* the batch has no blocking errors.
5. **Preview payroll.** Generate gross-to-net, tax, deduction, employer cost, and variance reports. → *Expect:* totals are available for review.
6. **Obtain approval.** Route the preview to the payroll approver or finance reviewer. → *Expect:* approval is recorded.
7. **Submit payroll.** ⚠️ *Irreversible:* confirm pay date, bank funding, employee count, and approval before submission because funds and filings may initiate. → *Expect:* the system shows payroll submitted or processing.
8. **Save reports.** Store required payroll reports and confirmation numbers in the approved location. → *Expect:* audit records are complete.

## Decision points

- If bank funding is insufficient → pause submission and escalate to finance.
- If an employee's pay is wrong → correct before submission when possible or prepare an off-cycle correction.
- If tax setup errors appear → consult payroll provider or tax specialist before submitting.

## Failure modes & recovery

- **F1 Missing timecards:** detect unapproved or absent hours → chase approvers or pay according to documented policy.
- **F2 Negative net pay:** detect employee net pay below zero → review deductions and adjust according to policy.
- **F3 Submitted error:** detect incorrect payroll after submission → contact provider immediately and run reversal, void, or off-cycle correction if available.

## Verification

Payroll status is submitted or processed for the correct pay period, approval is recorded, confirmation numbers exist, and payroll reports are saved.

## Variations

- US: include federal, state, local tax, garnishment, overtime, and final pay timing rules.
- Other countries: statutory contributions, payslip format, holiday pay, and payroll filing deadlines vary.
- Off-cycle payroll: limit the run to approved corrections or special payments.

## Safety & privacy

Medium risk because payroll involves money, bank data, tax identifiers, and employment records. Use dual review, restrict payroll reports, verify PII carefully, and avoid discriminatory or inconsistent pay adjustments.
