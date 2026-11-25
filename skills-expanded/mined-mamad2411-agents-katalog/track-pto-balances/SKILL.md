---
name: track-pto-balances
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 20min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Review and reconcile paid time off balances so employee accruals, usage, and corrections are accurate.

## Preconditions

- PTO policy, accrual rules, carryover limits, and pay period dates are known.
- You have access to the HRIS, timekeeping, or payroll system.
- Approved time-off records are available.

## Steps

1. **Open the PTO report.** Select the employee group, leave plan, and date range. → *Expect:* current balances and activity are visible.
2. **Check accrual rules.** Confirm accrual rate, service date, employment status, and eligibility. → *Expect:* each balance follows the applicable rule.
3. **Compare usage.** Match approved PTO requests against deductions from balances. → *Expect:* taken PTO is reflected correctly.
4. **Review exceptions.** Look for negative balances, missing accruals, duplicate deductions, carryover issues, or terminated employees. → *Expect:* anomalies are listed for review.
5. **Make approved corrections.** Enter corrections only with policy support or manager or HR approval. → *Expect:* corrected balances show an audit note.
6. **Notify stakeholders.** Inform payroll, HR, manager, or employee when a correction affects pay or scheduling. → *Expect:* impacted parties know the updated balance.
7. **Save the report.** Export or archive the reconciliation report in the approved location. → *Expect:* the audit trail is retained.

## Decision points

- If a balance affects final pay → confirm local payout rules before changing it.
- If the policy is ambiguous → ask HR or legal for interpretation before correction.
- If an employee disputes the balance → compare requests, approvals, accruals, and payroll records.

## Failure modes & recovery

- **F1 Duplicate deduction:** detect two deductions for one approved absence → reverse the duplicate with an audit note.
- **F2 Wrong accrual plan:** detect employee assigned to the wrong leave plan → update eligibility and recalculate according to policy.
- **F3 Unauthorized correction:** detect a manual edit without approval → reverse or escalate according to HR controls.

## Verification

The PTO report shows reconciled balances, exceptions are resolved or assigned, and any manual corrections have documented approval and audit notes.

## Variations

- US: state sick leave, vacation payout, unlimited PTO, and carryover rules vary.
- Other countries: statutory annual leave, public holiday interaction, and forfeiture limits may differ.
- Unlimited PTO: track approvals and usage patterns instead of accrual balances.

## Safety & privacy

Medium risk because PTO can affect pay and may reveal health or family absences. Restrict reports, avoid unnecessary leave reasons, and apply accrual and correction rules consistently.
