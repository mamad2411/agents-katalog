---
name: offboard-a-departing-employee
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 1h
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Complete a departing employee's offboarding tasks so access, property, payroll, benefits, and knowledge transfer are handled.

## Preconditions

- The departure date, reason category, manager, and notice status are confirmed.
- HR, IT, payroll, facilities, and legal owners are known.
- You have access to the HRIS and offboarding checklist.

## Steps

1. **Open the employee record.** Confirm legal name, employee ID, manager, location, and final work date. → *Expect:* the offboarding record matches the departing employee.
2. **Create offboarding tasks.** Assign HR, IT, payroll, benefits, facilities, and manager tasks with due dates. → *Expect:* each required owner has a task.
3. **Coordinate access removal.** Schedule account deactivation, badge removal, device return, and system ownership transfer. → *Expect:* access actions are queued for the right time.
4. **Confirm final pay inputs.** Verify final hours, PTO payout, deductions, expenses, and severance if applicable. → *Expect:* payroll has the information needed for final pay.
5. **Arrange knowledge transfer.** Ask the manager to capture projects, files, contacts, deadlines, and handoff owners. → *Expect:* active work has a successor or status note.
6. **Send exit information.** Provide return instructions, benefits notices, final pay timing, and contact information. → *Expect:* the employee knows next steps.
7. **Complete deprovisioning.** ⚠️ *Irreversible:* confirm final date, legal hold, and manager approval before disabling accounts or wiping devices. → *Expect:* access is disabled according to schedule.
8. **Close the record.** Mark tasks complete and store required documentation. → *Expect:* the HRIS shows the employee as terminated or inactive.

## Decision points

- If the departure is involuntary → coordinate timing and language with HR, legal, security, and payroll.
- If a legal hold applies → preserve accounts, devices, and records according to legal instructions.
- If the employee owns critical systems → transfer ownership before disabling access.

## Failure modes & recovery

- **F1 Early access removal:** detect access disabled before the final work time → restore only if authorized and document the incident.
- **F2 Final pay error:** detect missing payout or deduction → escalate to payroll for correction or off-cycle payment.
- **F3 Unreturned property:** detect missing equipment after due date → follow asset recovery and payroll deduction rules where lawful.

## Verification

The HRIS shows the correct departure status, access is disabled or scheduled, property and payroll tasks are tracked, and required offboarding documents are stored.

## Variations

- US: final pay timing, COBRA, WARN, unemployment, and PTO payout rules vary by state.
- Other countries: notice, consultation, statutory severance, certificates, and data retention rules may differ.
- Contractor departure: use contract end, access removal, and asset return steps without employee benefits tasks.

## Safety & privacy

Medium risk because offboarding affects pay, benefits, access, and personnel records. Handle PII confidentially, avoid retaliatory treatment, preserve legally required records, and apply access removal consistently.
