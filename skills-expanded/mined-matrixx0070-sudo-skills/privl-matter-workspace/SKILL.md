---
name: privl-matter-workspace
version: 1.0.0
description: Set up and run a privacy matter workspace — organize intake, artifacts, deadlines, and decision log for a discrete privacy matter so nothing is lost or missed.
author: matrixx0070
tags: [privacy, legal, workspace, matter-management, deadlines, recordkeeping]
capabilities: []
---

## When to use

Use this to stand up the container for a discrete privacy matter — a DSAR, a breach, a DPIA, a vendor onboarding, a regulator inquiry — so every artifact, deadline, and decision lives in one auditable place. It is the connective tissue the other privl- skills feed into.

**Not for:** the substantive legal work itself (use privl-dsar-response, privl-pia-generation, privl-dpa-review), or org-wide program tracking. One workspace = one matter.

## Method

1. Open the matter with a header: type, opened date, owner, regime(s), and any hard statutory deadline.
2. Capture intake facts: who/what triggered it, data subjects/systems involved, and the requested or required outcome.
3. Establish the **deadline register** first — statutory clocks (DSAR month/45-day, breach 72-hour), internal milestones, and reminders keyed before each due date.
4. Create the artifact index: link every document produced (triage note, PIA, DPA review, correspondence, evidence) with version and date.
5. Keep a **decision log**: each material decision, who made it, the basis, and the date — this is your defensibility trail if a regulator asks.
6. Track open actions with owners and due dates; review status at each milestone.
7. On close, record the outcome, retention period for the matter file, and lessons for the program.
8. **Attorney-escalation gate:** flag in the workspace when a matter crosses into privilege (breach, litigation, regulator inquiry) and mark counsel-directed materials so privilege is preserved.

## Example

> **Matter:** Vendor breach affecting 4,000 EU customers.
> **Deadlines:** 72-hour SA notification (Art. 33) — clock started at awareness; subject notification assessment; DPA breach-notice check.
> **Artifacts:** forensic summary, risk assessment, notification drafts, regulator correspondence — all indexed.
> **Decision log:** "notify SA yes / individuals yes — high risk" with basis + timestamp.
> Marked counsel-directed; privilege preserved.

## Pitfalls

- Starting substantive work before the deadline register exists — missed clocks are the top failure.
- Scattering correspondence across inboxes instead of one indexed thread.
- No decision log, so you cannot show *why* a call was made when questioned.
- Mixing privileged counsel material with business documents, waiving privilege.

## Output format

```
MATTER — <id/name> | type: <DSAR/breach/DPIA/vendor/inquiry>
Opened: <date> | Owner: <> | Regime: <> | Hard deadline: <date>
Deadline register: <clock — due — reminder>
Artifacts: <doc — version — date — link>
Decision log: <decision — who — basis — date>
Open actions: <action — owner — due>
Privilege: <counsel-directed items>
Status: <open/closed + outcome + file retention>
```

## Reference

- **GDPR Art. 33** 72-hour breach notification to the supervisory authority; **Art. 34** notification to individuals; **Art. 30** records duty.
- **DSAR clocks:** GDPR one month (Art. 12(3)); CCPA/CPRA 45 days — mirror in the deadline register.
- **Accountability (Art. 5(2)):** the decision log is your demonstrable-compliance evidence.
- Mark breach/litigation/inquiry matters as attorney-directed to preserve privilege.
