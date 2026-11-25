---
name: approve-a-time-off-request
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Review and approve or decline a time-off request consistently with policy, coverage needs, and leave balance.

## Preconditions

- The employee submitted a time-off request in the required system.
- You can view team calendar, leave policy, and available balance if needed.
- You are authorized to approve the request.

## Steps

1. **Open the request.** Review employee name, leave type, dates, hours, and submission notes. → *Expect:* the requested absence details are visible.
2. **Check eligibility.** Confirm the leave type, notice period, and balance or entitlement according to policy. → *Expect:* the request is eligible, ineligible, or needs HR review.
3. **Check coverage.** Compare team calendar, deadlines, shifts, and blackout periods. → *Expect:* coverage impact is clear.
4. **Decide consistently.** [BRANCH: approve | decline | ask for changes] approve if policy and coverage allow, decline with reason if not, or request date adjustments. → *Expect:* the selected action matches policy.
5. **Submit the decision.** Click approve, decline, or request changes in the HR system. → *Expect:* the request status updates.
6. **Notify affected owners.** If needed, tell scheduling, payroll, or project owners about approved coverage changes. → *Expect:* downstream teams know the absence dates.

## Decision points

- If the leave may be legally protected → consult HR before declining.
- If multiple employees request the same dates → apply the documented priority rule consistently.
- If balance is insufficient → ask HR whether unpaid leave, advance PTO, or another leave type applies.

## Failure modes & recovery

- **F1 Wrong leave type:** detect vacation submitted as sick, protected, or unpaid leave → ask the employee or HR to correct the type.
- **F2 Coverage gap:** detect no qualified coverage after approval → arrange backup or discuss alternate dates.
- **F3 Inconsistent denial:** detect a denial based on personal preference → re-evaluate using policy and documented coverage facts.

## Verification

The HR system shows the correct approval status, leave dates appear on the relevant calendar, and payroll or scheduling owners have any required notice.

## Variations

- US: consider FMLA, ADA, state sick leave, military leave, and other protected leave rules before denial.
- Other countries: statutory leave entitlements, public holidays, and required notice periods vary.
- Shift work: confirm schedule coverage and overtime impact before approving.

## Safety & privacy

Low risk for routine PTO, but leave reasons may reveal health or family information. Do not ask for unnecessary details, apply rules consistently, and route protected or medical leave through HR.
