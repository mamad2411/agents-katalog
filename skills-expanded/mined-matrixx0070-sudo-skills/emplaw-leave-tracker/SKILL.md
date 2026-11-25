---
name: emplaw-leave-tracker
version: 1.0.0
description: Stand up and maintain an ongoing leave-of-absence tracker that computes FMLA/ADA/state-leave eligibility, entitlements, and deadlines across all employees.
author: matrixx0070
tags: [leave, fmla, ada, compliance, hr]
capabilities: []
---

## When to use
Use this when you need to build or run the master leave register — the single source of truth that holds every employee's leave eligibility, remaining entitlement balances, and open deadlines, and that you reconcile on a recurring basis. Use it when onboarding leave tracking for the first time, auditing balances, or rolling the 12-month leave year forward. **Not for:** logging one new request (use emplaw-log-leave, which appends a single record into the structure this skill defines); expanding into a new US state (emplaw-expansion-kickoff); updating an existing state footprint (emplaw-expansion-update); hiring abroad (emplaw-international-expansion); handbook edits (emplaw-handbook-updates); drafting a standalone policy (emplaw-policy-drafting); or the initial intake conversation (emplaw-cold-start-interview).

## Method
1. Confirm scope: covered entities, worksites, and total headcount within 75 miles of each site.
2. Decision point: if any worksite has 50+ employees within 75 miles, FMLA applies to that site; else FMLA does not, but ADA (15+ employees) and state programs may still apply — do not stop.
3. Define the leave-year method (calendar, fixed, anniversary, or rolling-backward) and record it once; it governs every balance.
4. For each employee, capture tenure and hours-worked to flag FMLA eligibility (12 months + 1,250 hours).
5. Decision point: if an employee sits in CA, NY, WA, or another paid-family-leave state, layer that entitlement and note stacking order against FMLA; else track federal + ADA only.
6. Set deadline reminders: eligibility notice, 15-day certification window, designation notice, recertification dates, and return-to-work checkpoints.
7. Attorney-escalation gate: before denying, exhausting, or terminating any leave, engage licensed employment counsel in the relevant jurisdiction — this skill is not legal advice.

## Example
A 60-person employer with 48 employees at HQ and 12 at a satellite 90 miles away: HQ triggers FMLA; the satellite does not. You set a rolling-backward leave year, flag three employees under 1,250 hours as FMLA-ineligible, and layer California PFL/CFRA for the HQ staff. The tracker surfaces one open 15-day certification deadline.

## Pitfalls
- **Counting company-wide, not by worksite.** FMLA's 50/75-mile test is site-specific; a large total can still leave a site uncovered.
- **Ignoring ADA when FMLA runs out.** Exhausted FMLA does not end the duty to consider leave as a reasonable accommodation at 15+ employees.
- **Mixing leave-year methods.** Inconsistent methods let entitlement quietly reset; pick one and lock it.
- **Missing certification clocks.** The 15-day certification and designation notices are hard deadlines, not courtesies.

## Output format
```
LEAVE TRACKER — <org> | Leave year: <method> | As of: <date>
Employee | Site | Tenure/Hours | FMLA elig? | State prog | FMLA used/left | Open deadlines
<name> | <site> | <mo>/<hrs> | Y/N | <CA-PFL/…> | <x/12wk> | <cert due, RTW>
Escalation: engage counsel before any denial/exhaustion/termination
```

## Reference
FMLA: employer covered at 50+ employees within 75 miles; employee eligible at 12 months + 1,250 hours; 12 weeks unpaid (26 weeks for military caregiver leave). ADA applies at 15+ employees and can require leave as a reasonable accommodation via the interactive process. State paid-family-leave programs (California, New York, Washington, and others) run alongside and may stack. Pregnancy is covered under the PWFA and PDA. Track notice/certification deadlines: 15-day certification window, designation notices. General reference only, not tailored legal advice.
