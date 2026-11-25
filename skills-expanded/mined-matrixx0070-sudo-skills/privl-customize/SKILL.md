---
name: privl-customize
version: 1.0.0
description: Tailor the privacy-legal skill set to a specific organization — capture its regimes, roles, risk appetite, and escalation rules so every privl- skill runs against the right context.
author: matrixx0070
tags: [privacy, legal, configuration, customization, context, escalation]
capabilities: []
---

## When to use

Use this once per organization (and whenever its footprint changes) to record the context every other privl- skill needs: which laws apply, the controller/processor role, the sensitive-data footprint, the escalation thresholds, and who counsel is. It converts generic privacy skills into org-specific ones.

**Not for:** doing the substantive work (triage, PIA, DSAR, DPA), or a one-off assessment. This is the configuration layer, not an assessment.

## Method

1. Capture jurisdiction and applicable regimes: GDPR/UK GDPR, CCPA/CPRA and other US state laws, sector rules (HIPAA, GLBA, COPPA), and any others by geography of subjects.
2. Record the org's role(s): controller, processor, or both, and for which product lines — this changes which obligations and DPA clauses apply.
3. Map the sensitive-data footprint: special-category data, children's data, financial/government IDs, and whether AI/automated decisioning is in use.
4. Define the escalation matrix: what always goes to counsel (refusals, new automated decisioning, sensitive-data monetization, unmechanized transfers), what a privacy lead can clear, and named contacts + SLAs.
5. Set defaults each skill inherits: DSAR verification standard, retention baselines, breach-notification thresholds, and risk-appetite for legitimate-interest reliance.
6. **Decision point:** where the org's stated risk appetite conflicts with legal minimums, the legal minimum wins — record the tension for counsel.
7. **Attorney-escalation gate:** counsel must sign off on the escalation matrix itself — the thresholds that decide when to involve them are a legal decision.

## Example

> **Org:** B2B SaaS, EU + California customers, controller for its app / processor for customer data it hosts.
> **Sensitive:** no Art. 9 data; uses an AI support-summarizer (automated, non-decisioning).
> **Escalation:** all refusals + any move to automated decisioning → counsel (48h SLA); privacy lead clears routine access DSARs.
> **Defaults:** DSAR ID = account challenge; LI reliance allowed with balancing test on file.

## Pitfalls

- Guessing the regime footprint instead of mapping it to actual subject geography.
- Recording a single role when the org is controller for one product and processor for another.
- Setting a risk appetite that undercuts a legal minimum and treating it as authorization.
- Letting the org self-set escalation thresholds without counsel sign-off.

## Output format

```
PRIVL CONFIG — <org> | date | counsel-approved: <y/n>
Regimes: <GDPR/CCPA/sector...>
Role(s): <controller/processor per product line>
Sensitive footprint: <Art.9 / children / financial / AI-decisioning>
Escalation matrix: <always-counsel | lead-can-clear | contacts + SLA>
Defaults: <DSAR verification | retention | breach threshold | LI appetite>
Legal-minimum conflicts: <items for counsel>
```

## Reference

- **GDPR Art. 3** territorial scope; **Art. 4(7)/(8)** controller vs. processor definitions.
- **CCPA/CPRA** business/service-provider/contractor roles and applicability thresholds; other US state laws by subject residence.
- Sector overlays: **HIPAA**, **GLBA**, **COPPA**.
- The escalation matrix and any legal-minimum conflict must be approved by an attorney.
