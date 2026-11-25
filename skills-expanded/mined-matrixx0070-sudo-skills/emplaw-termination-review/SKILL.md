---
name: emplaw-termination-review
version: 1.0.0
description: Review a proposed termination for legal risk before it happens, covering documentation, protected activity, WARN, final pay, and releases.
author: matrixx0070
tags: [employment-law, termination, warn-act, severance, compliance]
capabilities: []
---

## When to use
Use this when someone is about to fire, lay off, or non-renew a worker and wants the legal risk assessed before the action is taken. This skill checks documentation adequacy, timing against protected activity, WARN-Act notice duties, final-pay rules, and severance/release requirements. **Not for:** hiring or offers (use emplaw-hiring-review), classifying the worker (use emplaw-worker-classification), overtime or unpaid-wage disputes (use emplaw-wage-hour-qa), investigating misconduct or a complaint (use emplaw-internal-investigation), medical/family leave status (use emplaw-leave-tracker), or drafting the severance policy itself (use emplaw-policy-drafting).

## Method
1. Confirm the stated reason and pull the paper trail (reviews, warnings, PIP, policy). Decision point: if documentation is thin or contradicts the reason, mark HIGH and pause to build a defensible record.
2. Map recent protected activity — complaints, leave requests, injuries, whistleblowing, accommodation requests. Decision point: if any occurred within a suspicious window, treat retaliation risk as HIGH and escalate.
3. Check headcount and scope for WARN. Decision point: if 100+ employees and a mass layoff/plant closing, verify 60-day notice; else note state mini-WARN may still apply.
4. Determine final-pay timing for the operating state. Decision point: if the state requires pay on the last day (e.g., involuntary in CA), prepare the check before the meeting.
5. If offering severance, decide whether a release is included. Decision point: if the worker is 40+, apply OWBPA requirements to the release.
6. Confirm return of property, benefits/COBRA notice, and unemployment posture.
7. Apply the attorney-escalation gate: releases, protected-activity overlap, and mass layoffs — confirm with licensed counsel in the operating state; this is not legal advice.

## Example
A manager wants to fire a California employee two weeks after she requested medical leave, citing "attitude," with no prior write-ups. You flag retaliation/FMLA-proximity as HIGH, note the absent documentation, require final pay ready on the last day (CA involuntary), and — because she is 44 and a release is proposed — require OWBPA 21-day consideration and 7-day revocation. You route to counsel before proceeding.

## Pitfalls
- **Firing right after protected activity.** Close timing creates an inference of retaliation even when the reason is legitimate; document the independent basis first.
- **A release without OWBPA compliance.** For workers 40+, a waiver of age claims is invalid without the consideration and revocation periods (and group-layoff disclosures).
- **Missing state final-pay deadlines.** Several states require immediate payment on involuntary termination; late pay triggers penalties.
- **Overlooking state mini-WARN.** Some states set lower headcount/notice triggers than the federal 100-employee threshold.

## Output format
```
TERMINATION REVIEW — <worker> @ <state>, headcount <n>
STATED REASON: <reason>
RISK LEVEL: <LOW | MEDIUM | HIGH>
DOCUMENTATION: <adequate? gaps>
PROTECTED ACTIVITY: <activity + timing window>
WARN: <applies? notice status>
FINAL PAY: <state deadline + readiness>
SEVERANCE/RELEASE: <offered? OWBPA if 40+>
BENEFITS/COBRA + PROPERTY: <status>
GO / HOLD: <decision + conditions>
ATTORNEY GATE: Confirm with licensed counsel in <state>; not legal advice.
```

## Reference
General reference only, not tailored legal advice.
- **WARN Act**: employers with **100+ employees** must give **60 days'** written notice of a plant closing or mass layoff; some states have "mini-WARN" laws with lower thresholds and additional notice.
- **Protected activity / retaliation**: adverse action shortly after complaints (discrimination, harassment, wage), FMLA/ADA leave or accommodation requests, safety reports, or whistleblowing can support a retaliation claim under Title VII, FLSA, OSHA, and parallel statutes.
- **Final pay** timing varies by state — several (e.g., California) require immediate payment of all wages on involuntary termination, with waiting-time penalties for delay; others allow the next regular payday.
- **OWBPA** (releases of ADEA claims, workers **40+**): the worker must get at least **21 days** to consider (**45 days** in a group layoff), a **7-day** revocation period after signing, written advice to consult an attorney, and — in group programs — disclosure of the ages/titles of those selected and not selected. Thresholds and deadlines change — direct to current DOL and EEOC figures.
