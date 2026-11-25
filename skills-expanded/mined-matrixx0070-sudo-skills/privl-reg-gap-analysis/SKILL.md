---
name: privl-reg-gap-analysis
version: 1.0.0
description: Assess an existing privacy program against applicable regulations — map obligations to current controls, rate each gap by risk, and produce a prioritized remediation plan.
author: matrixx0070
tags: [privacy, legal, gap-analysis, compliance, gdpr, ccpa, remediation]
capabilities: []
---

## When to use

Use this when an organization has some privacy documentation and controls in place and needs to know where it falls short of the laws that apply to it. It is the compliance health check that turns a scattered program into a prioritized remediation backlog.

**Not for:** building the first data map from nothing (privl-cold-start-interview), assessing one new activity (privl-use-case-triage), or the deep risk analysis of a single high-risk activity (privl-pia-generation). Run gap analysis when you have material to assess.

## Method

1. Determine which regimes apply: GDPR (EU/UK subjects, establishment, or offering/monitoring), CCPA/CPRA (California thresholds), and any sector rules (HIPAA, GLBA, COPPA for children).
2. Build the obligation checklist per regime: RoPA (Art. 30), lawful bases documented, privacy notices, DSAR process + timelines, consent/opt-out mechanisms, DPAs with processors, transfer mechanisms, breach-notification procedure, DPO/appropriate reps, DPIA process, security (Art. 32), retention schedule.
3. Map current state to each obligation: present / partial / absent, with evidence.
4. Rate each gap by risk = likelihood of enforcement/harm x severity (fine exposure, subject harm, breach likelihood).
5. **Decision point:** sequence remediation — quick high-risk wins first (e.g., missing opt-out, no breach process) before long structural work.
6. Assign owners and target dates; note dependencies.
7. **Attorney-escalation gate:** unlawful ongoing processing, missing breach-notification capability, undisclosed sensitive-data or children's-data handling, or transfers with no mechanism → escalate to counsel, not just the backlog.

## Example

> **Org:** mid-size retailer, GDPR + CCPA apply.
> **Findings:** RoPA partial; DSAR ad-hoc, no timeline tracking; no "Do Not Sell/Share" link (pixels active); DPAs missing for 4 vendors; breach process undocumented.
> **Priorities:** P1 opt-out link + breach process (enforcement-visible), P2 DSAR SLA tooling, P3 RoPA completion + DPAs.
> Undisclosed pixel-based sharing routed to counsel.

## Pitfalls

- Assessing against GDPR only when CCPA/sector rules also bite.
- Rating gaps by effort instead of risk, so cheap high-risk fixes wait.
- "Policy exists" counted as compliant when the practice does not match the policy.
- Producing a gap list with no owners or dates — nothing gets fixed.

## Output format

```
GAP ANALYSIS — <org> | regimes: <GDPR/CCPA/...>
Obligation: <item> | State: <present/partial/absent> | Evidence: <>
  Risk: <likelihood x severity> | Priority: <P1-P3>
Remediation: <action — owner — date — dependency>
For counsel: <unlawful/breach/transfer items>
```

## Reference

- **GDPR** Arts. 30 (RoPA), 6/9 (bases), 12-22 (rights), 28 (processors), 32 (security), 33-34 (breach), 35 (DPIA), Chapter V (transfers).
- **CCPA/CPRA** notice, opt-out of sale/sharing, sensitive-PI limits, service-provider contracts, 45-day DSAR.
- Sector overlays: **HIPAA**, **GLBA**, **COPPA** (children under 13).
- Escalate unlawful processing, missing breach capability, and unmechanized transfers to an attorney.
