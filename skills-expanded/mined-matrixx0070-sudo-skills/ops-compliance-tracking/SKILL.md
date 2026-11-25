---
name: ops-compliance-tracking
version: 1.0.0
description: Track audit readiness against SOC 2, ISO 27001, or GDPR with a living control register and prioritized remediation.
author: matrixx0070
tags: [operations, compliance, audit, soc2, iso27001, gdpr]
capabilities: []
---

# Compliance Tracking

## When to use
Use this to assess readiness for an audit or certification (SOC 2, ISO 27001, GDPR), maintain a living control inventory, or prioritize remediation before an auditor arrives.

**Not for:** writing the policies themselves, legal interpretation of a regulation, or a security risk assessment (use ops-risk-assessment). This tracks control *status and evidence*, not control *design*.

## Method
1. **Select framework and scope.** Name the standard, the trust criteria / annex / articles in scope, and the systems and data covered. *Decision:* scope tightly — every system in scope is evidence you must produce.
2. **Enumerate controls.** List each required control with ID, intent, and the accountable owner.
3. **Assess status per control.** Mark implemented / partial / missing, and record the evidence that proves it (policy, log, config, ticket).
4. **Identify gaps.** For every partial or missing control, describe the deficiency and its exposure.
5. **Prioritize remediation.** Rank gaps by risk *and* auditor visibility; assign owner, target date, and effort. *Decision:* a low-risk but always-sampled control outranks a high-risk obscure one before an audit.
6. **Verify evidence freshness.** Confirm each artifact is current, retrievable, and dated within the audit window.
7. **Compute readiness.** Report % controls satisfied and a go / not-ready verdict for the audit date.

## Example
SOC 2 Type II, Security criteria, 61 controls. 52 implemented, 6 partial, 3 missing = 85% satisfied. Highest-priority gap: CC6.1 access reviews — evidence exists but last review was 8 months ago (window is quarterly), and auditors always sample it. **Action:** run Q-review now, owner = IT lead, due in 5 days. **Verdict: not-ready until CC6.1 and the 3 missing controls close.**

## Pitfalls
- **Evidence that is stale or unretrievable.** A control "implemented" 10 months ago with no recent artifact fails on sampling.
- **Confusing policy with practice.** A written policy nobody follows is a finding, not a pass — evidence must show operation.
- **Flat prioritization.** Treating all gaps equally burns the runway; weight by risk and sampling likelihood.
- **One-time snapshot.** Type II covers a period; a point-in-time check misses control lapses across the window.

## Output format
```
Header:         framework | scope | audit date
Readiness:      % satisfied | verdict (go | not-ready)
Control register: ID | control | owner | status | evidence | last verified
Gap list:       control | deficiency | risk | owner | due date
Remediation:    prioritized roadmap with dates
Evidence gaps:  artifacts missing or stale
Next actions
```
