---
name: log-a-sick-day
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Record an employee sick day in the HR or timekeeping system with the correct date, hours, and leave type.

## Preconditions

- The employee has reported the sick day through the required channel.
- You are authorized to enter or verify sick leave.
- The applicable sick leave policy is known.

## Steps

1. **Open the employee record.** Search for the employee in the HR or timekeeping system. → *Expect:* the correct employee profile is visible.
2. **Select sick leave.** Choose the sick, medical, or illness leave type required by policy. → *Expect:* the leave code matches the reported absence.
3. **Enter date and hours.** Add the sick day date, partial-day hours if applicable, and pay code. → *Expect:* the entry reflects the actual absence.
4. **Add minimal notes.** Record only operational details such as "reported sick" or "manager notified." → *Expect:* no unnecessary medical details are stored.
5. **Submit or save.** Save the leave entry or submit it for approval if required. → *Expect:* the system shows saved, pending, or approved status.
6. **Confirm calendar impact.** Check that schedule, payroll, or team calendar reflects the absence if integrated. → *Expect:* downstream systems show the sick day or pending sync.

## Decision points

- If the absence may be protected leave → route to HR instead of treating it as routine sick time.
- If documentation is required by policy → request only the permitted documentation through the approved channel.
- If balance is insufficient → ask HR whether statutory sick leave, unpaid leave, or another code applies.

## Failure modes & recovery

- **F1 Wrong leave code:** detect sick time entered as vacation or unpaid leave → correct the code before payroll cutoff.
- **F2 Medical overshare:** detect diagnosis or treatment details in notes → remove unnecessary details according to policy.
- **F3 Missing approval:** detect pending status after cutoff → remind the approver or escalate to payroll.

## Verification

The employee's time record shows the correct sick leave date, hours, status, and leave code with no unnecessary medical details.

## Variations

- US: state and local paid sick leave rules may affect accrual, documentation, and protected use.
- Other countries: medical certificates, statutory sick pay, and employer reporting rules vary.
- Hourly employees: confirm shift hours and payroll cutoff before saving.

## Safety & privacy

Low risk for routine entry, but health information is sensitive. Collect the minimum needed, avoid diagnosis notes, and apply sick leave rules consistently without retaliation.
